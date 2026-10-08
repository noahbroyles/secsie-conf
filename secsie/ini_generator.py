"""
ini_generator.py

Contains code relative to writing configuration text in the `ini` dialect that secsie reads with `mode='ini'`.

There is no single ini standard, so the promise made here is a narrow one: whatever this module writes, the secsie
ini reader reads back as the same data. If a value can not be written in a way that makes that true, an exception is
raised instead of silently writing something different.

To keep the writer and the reader from drifting apart, the checks below use the very same regular expressions
(from `modes.py`) that the reader uses to recognize numbers, booleans, nulls, and sections.
"""
from __future__ import annotations

import re
import math
from decimal import Decimal

from secsie.modes import MODES

_INI = MODES['ini']

# The reader turns a value that matches any of these into a number, bool, or None, so a *string* that matches one of
# them has to be quoted to stay a string.
_SPECIAL_VALUE_EXES = (_INI['FLOAT_EX'], _INI['INT_EX'], _INI['NULL_EX'], _INI['TRUE_EX'], _INI['FALSE_EX'])

# The reader strips whitespace around every '=' on a line, so whitespace touching an '=' inside a value is lost.
_PADDED_EQUALS_EX = re.compile(r'\s=|=\s')


def _fail(where: str, problem: str) -> ValueError:
    """
    INTENDED FOR INTERNAL USE ONLY

    Build the error raised when a value can not be written faithfully. All messages share one shape so they read
    consistently: which key was the problem, and why.
    """
    return ValueError(f"Cannot generate ini: the value for '{where}' {problem}.")


def _format_float(value: float, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render a float in the plain `digits.digits` form the reader recognizes as a float.
    `repr` is not enough, because it switches to exponent notation (`1e-07`, `1e+16`) for very small and very large
    numbers, which the reader would take for a string.
    """
    if not math.isfinite(value):
        raise _fail(where, f"is {value!r}, which ini has no way to represent")

    text = repr(value)
    if 'e' in text or 'E' in text:
        # Decimal can expand the exponent into plain digits without losing any precision
        text = format(Decimal(text), 'f')
    if '.' not in text:
        # A whole number like 1e+16 expands to just digits, which would be read back as an int
        text += '.0'
    return text


def _needs_quotes(text: str) -> bool:
    """
    INTENDED FOR INTERNAL USE ONLY

    Whether writing a string as-is would make the reader read something different back.
    """
    return (
        text == ''  # a blank value after the '=' is not a string, so write "" instead
        or text != text.strip()  # the reader trims surrounding whitespace, quotes protect it
        or text.startswith('#')  # would turn the rest of the line into a comment
        or ',' in text  # would be split into a list
        or any(special.match(text) for special in _SPECIAL_VALUE_EXES)  # would become a number, bool, or None
    )


def _format_string(text: str, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render a string value, adding quotes only when they are needed. The reader keeps a quoted value as a plain string
    and does no further interpretation, which is what makes quoting safe.
    """
    # The reader has no way to escape a quote, and it strips every quote from both ends of a quoted value. Whether the
    # string needs quotes or not, a quote at either end would be lost or mistaken for a quoted value.
    if text.startswith('"') or text.endswith('"'):
        raise _fail(where, "starts or ends with a quote character, which ini has no way to escape")

    return f'"{text}"' if _needs_quotes(text) else text


def _format_list_item(item, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render one item of a list. Items are written bare, because the reader does not look for quotes inside a list, so a
    string that could not be written bare can not be a list item.
    """
    if isinstance(item, str):
        if item == '' or item != item.strip() or ',' in item or any(s.match(item) for s in _SPECIAL_VALUE_EXES):
            # Empty items are dropped by the reader, whitespace is trimmed, commas split the item in two,
            # and number-like words are converted to their types.
            raise _fail(where, f"has a list item {item!r} that would be read back differently, "
                               f"since list items can not be quoted in ini")
        return item

    if isinstance(item, (dict, list)):
        raise TypeError(f"Cannot generate ini: the value for '{where}' has a {type(item).__name__} inside a list. "
                        f"Lists can only hold strings, numbers, booleans, and None.")

    return _format_scalar(item, where)


def _format_scalar(value, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render a value that is not a string, list, or dict. The result is exactly what the reader converts back to the
    same Python value.
    """
    if value is None:
        return 'null'
    if isinstance(value, bool):  # must come before int, since bool is a subclass of int
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _format_float(value, where)

    raise TypeError(f"Cannot generate ini: the value for '{where}' is a {type(value).__name__}, which ini can not "
                    f"hold. Values must be strings, numbers, booleans, None, or lists of those.")


def _format_value(value, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render the right-hand side of a `key = value` line, and make sure that what is rendered survives being read.

    :param value: The value to render
    :param where: The key (or `section.key`) the value belongs to, used in error messages
    """
    if isinstance(value, dict):
        raise TypeError(f"Cannot generate ini: '{where}' is a dict, but nested dicts are not supported. "
                        f"Ini only has one level of sections, so a section's values must be strings, numbers, "
                        f"booleans, None, or lists.")

    if isinstance(value, list):
        if len(value) == 0:
            # A lone comma is a list with no items (the reader drops the blank pieces on either side of it)
            return ','
        text = ', '.join(_format_list_item(item, where) for item in value)
        if text.startswith('"'):
            # The reader takes any value that begins with a quote for a quoted string, and would not make a list of it
            raise _fail(where, "has a list that starts with a quote character, which would be read as a quoted string")
        if len(value) == 1:
            # Without a comma, a single item would be read as a plain value instead of a list. The reader ignores a
            # trailing comma in ini, so this one only marks it as a list.
            text += ','
    elif isinstance(value, str):
        text = _format_string(value, where)
    else:
        text = _format_scalar(value, where)

    # These are properties of the finished text, so they are checked once, here, no matter what kind of value it was
    if '\n' in text or '\r' in text:
        raise _fail(where, "contains a line break, and every value has to fit on one line")
    if text.startswith('#') or ' #' in text:
        raise _fail(where, "contains a space followed by '#', which starts a comment even inside quotes")
    if _PADDED_EQUALS_EX.search(text):
        raise _fail(where, "has whitespace next to an '=', which the reader strips")
    return text


def _check_key(key, where: str) -> None:
    """
    INTENDED FOR INTERNAL USE ONLY

    Make sure a key is something the reader can read back as that same key.
    """
    if not isinstance(key, str) or key == '':
        raise TypeError(f"Cannot generate ini: keys must be non-empty strings, got {key!r}.")
    if any(c.isspace() for c in key) or '=' in key:
        raise ValueError(f"Cannot generate ini: the key '{where}' contains whitespace or an '=', "
                         f"neither of which are allowed in key names.")
    if key[0] in '#;':
        raise ValueError(f"Cannot generate ini: the key '{where}' starts with '{key[0]}', "
                         f"which would make the whole line a comment.")


def _check_section_name(name) -> None:
    """
    INTENDED FOR INTERNAL USE ONLY

    Make sure a section name is one that the reader recognizes as a section header.
    """
    if not isinstance(name, str) or not _INI['SECTION_EX'].match(f'[{name}]'):
        raise ValueError(f"Cannot generate ini: {name!r} is not a valid section name. "
                         f"Section names can only contain letters, numbers, spaces, '_', and '-'.")


def generate_ini(conf_obj: dict, indent: str = '') -> str:
    """
    Generate and return config text in the `ini` dialect that secsie reads with `mode='ini'`.

    Reading the result with `parse_config(text, mode='ini')` gives back the same data that was passed in. Only the
    data is kept, not comments or formatting. Strings are quoted when they have to be, so that they stay strings.

    Top level keys are written first, because anything written after a section header belongs to that section.
    A section with no keys is written, but the reader has nothing to put in the result for it, so it is not read back.

    :param conf_obj: The dictionary to write. Its values can be strings, numbers, booleans, None, and lists of those,
        or (for the top level only) dicts of those, which are written as sections
    :param indent: The character(s) to indent the keys in each section with. Defaults to no indentation
    :return: a string of ini configuration text
    :raises ValueError: if a value, key, or section name can not be written so that it is read back the same
    :raises TypeError: if a value is of a type ini can not hold, such as a dict nested inside a section
    """
    top_level = [(key, value) for key, value in conf_obj.items() if not isinstance(value, dict)]
    sections = [(key, value) for key, value in conf_obj.items() if isinstance(value, dict)]

    lines = []

    for key, value in top_level:
        _check_key(key, key)
        lines.append(f"{key} = {_format_value(value, key)}")

    for name, section in sections:
        _check_section_name(name)
        if lines:
            lines.append('')  # keep a blank line between a section and whatever came before it
        lines.append(f"[{name}]")

        for key, value in section.items():
            where = f"{name}.{key}"
            _check_key(key, where)
            lines.append(f"{indent}{key} = {_format_value(value, where)}")

    return '\n'.join(lines) + '\n' if lines else ''
