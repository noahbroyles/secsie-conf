from __future__ import annotations

from os import PathLike
from pathlib import Path

from secsie.ini_generator import generate_ini
from secsie.modes import MODES


def _format_value(value, where: str) -> str:
    """
    INTENDED FOR INTERNAL USE ONLY

    Render a single Python value the way the parser expects to read it back: None becomes `null` and bools become
    `true`/`false`. Everything else is rendered with `str`.

    :param value: The value to render
    :param where: The key (or `section.key`) the value belongs to, used in error messages
    :raises ValueError: if a string contains a space followed by `#`, because it would be read back as a comment
    """
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, str):
        if ' #' in value or value.startswith('#'):
            raise ValueError(
                f"Cannot generate config: the value for '{where}' contains a space followed by '#' ({value!r}). "
                f"That starts an inline comment in secsie, so the rest of the value would be lost."
            )
    return str(value)


def generate_config(conf_obj: dict, indent: str | None = None, mode: str = 'secsie') -> str:
    """
    Generate and return a valid config from an object.

    The config is written in the secsie language by default. Pass `mode='ini'` to write the `ini` dialect that
    secsie reads with `mode='ini'` instead (see `secsie.ini_generator.generate_ini` for what that involves).

    Empty string values are written as commented out lines (at the top level and in sections), so they are not
    present when the generated config is parsed again. Comments and formatting from a file that was parsed earlier
    are not preserved either, only the data is.

    Keys that are not in a section are always written before the first section, whatever their order in the
    dictionary, since there is no way to write a key after a section without it becoming part of that section.

    :param conf_obj: The dictionary to parse into a configuration language string
    :param indent: The character(s) to use for indentation. Can be tab or spaces. Defaults to a tab character, '\t', for
        secsie and to no indentation for ini
    :param mode: The configuration language to write, 'secsie' or 'ini'
    :return: a string of configuration code
    :raises ValueError: if the mode is not 'secsie' or 'ini'
    :raises TypeError: if a section contains a dict, since secsie does not support nested dicts
    :raises ValueError: if a string contains a space followed by `#`, since it would be read back as a comment
    """
    if mode not in MODES:
        raise ValueError(f"Unknown mode {mode!r}, it must be one of: {', '.join(MODES)}")

    if mode == 'ini':
        return generate_ini(conf_obj, indent='' if indent is None else indent)

    if indent is None:
        indent = '\t'

    conf = ''
    sections = {}

    # Attributes that aren't in a section have to come first. A section only ends where the next one begins, so
    # anything written after a section header (even after a blank line) would be read back as part of that section.
    for key, value in conf_obj.items():
        if isinstance(value, dict):
            sections[key] = value
        elif isinstance(value, list):
            conf += f'{key} = {", ".join(_format_value(i, key) for i in value)}\n'
        else:
            conf += f"{';' if value == '' else ''}{key} = {_format_value(value, key)}\n"

    for key, section in sections.items():
        conf += f"\n[{key.replace(' ', '')}]\n"
        for k, v in section.items():
            where = f"{key}.{k}"
            if isinstance(v, dict):
                raise TypeError(
                    f"Cannot generate config: '{where}' is a dict, but nested dicts are not supported. "
                    f"Secsie only has one level of sections, so a section's values must be strings, numbers, "
                    f"booleans, None, or lists."
                )
            elif isinstance(v, list):
                conf += f'{indent}{k} = {", ".join(_format_value(i, where) for i in v)}\n'
            else:
                conf += f"{';' if v == '' else ''}{indent}{k} = {_format_value(v, where)}\n"
        conf += "\n"

    return conf


def generate_config_file(conf_obj: dict, output_file: str | PathLike[str], indent: str | None = None,
                         mode: str = 'secsie'):
    """
    Generate and write a config file from a dictionary of keys and values

    :param conf_obj: The dictionary to render into a configuration language
    :param output_file: The file to write to
    :param indent: The character(s) to use for indentation. Can be tab or spaces. Defaults to a tab character, '\t', for
        secsie and to no indentation for ini
    :param mode: The configuration language to write, 'secsie' or 'ini'
    """
    output_file = Path(output_file)
    # Generate before opening the file, so a value that can't be written never leaves a half written file behind
    conf = generate_config(conf_obj, indent=indent, mode=mode)

    # '#' comments are common in secsie, but ';' is the comment character every ini reader understands
    comment_char = ';' if mode == 'ini' else '#'

    with open(output_file, 'w') as f:
        f.write(f"{comment_char} {output_file.name} auto-generated by secsie\n{conf}")
