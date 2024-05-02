"""
parser.py

Contains code relative to parsing configuration language.
"""
from __future__ import annotations

from typing import Any
from os import PathLike
from secsie.modes import MODES
from secsie import InvalidSyntax


def _parse_value(value: str, mode: str = 'secsie') -> Any:
    """
    INTENDED FOR INTERNAL USE ONLY

    Determine whether a value is of a special type. If so, will convert the value to that type and return it.
    If not, will return the original value.
    """
    if MODES[mode]["FLOAT_EX"].match(value):
        return float(value)
    elif MODES[mode]["INT_EX"].match(value):
        return int(value)
    elif MODES[mode]["NULL_EX"].match(value):
        return None
    elif MODES[mode]["TRUE_EX"].match(value):
        return True
    elif MODES[mode]["FALSE_EX"].match(value):
        return False
    elif ',' in value:
        # This is a comma separated list of items
        return [_parse_value(v.strip()) for v in value.split(',') if ((mode == 'ini' and len(v.strip()) > 0) or (mode == 'secsie'))]
    else:
        # The value is not special, it's just a regular string
        return value


def _write_to_conf_(conf: dict, line, line_number: int, section=None, mode: str = 'secsie') -> dict:
    """
    INTENDED FOR INTERNAL USE ONLY

    Reads a line from a config language and processes it by writing it to the current config dictionary
    """
    key_value = [c.strip() for c in line.split('=')]

    if len(key_value) < 2:
        raise InvalidSyntax(f'"{line}" - bad section descriptor or value assignment', line_number)

    key, value = key_value[0], '='.join(key_value[1:])  # We want to allow '=' in our values

    if ' ' in key:
        raise InvalidSyntax("spaces not allowed in keys", line_number)

    if mode == 'ini':
        # Attempt to get ini strings right
        if value.startswith('"'):
            # This is an ini string, we need to remove the quotes
            value = value.strip('"')

    # Determine if the value is of a special type
    value = _parse_value(value, mode)

    # Store the value in the config dictionary, under the appropriate section, if any
    if section is None:
        conf[key] = value
    else:
        if not conf.get(section, False):
            conf[section] = {}
        conf[section][key] = value

    return conf


def parse_config(config: str, mode: str = 'secsie') -> dict:
    """
    Parse a string containing configuration text and return a dictionary of config keys and values.

    :param config: The config to parse
    :param mode: Determines what configuration language is being used. Can be either 'secsie' or 'ini'
    :return: The config as a dict
    """
    lines = [line.strip() for line in config.split('\n')]
    conf = {}

    c_section = None
    lineno = 0
    for line in lines:
        lineno += 1
        # Check for whole line comments
        if line.startswith('#') or line.startswith(';'):
            continue
        # Handle inline comments
        line = line.split(' #')[0].strip()
        if line == '':  # Skip blank lines
            continue
        # Check to see if this is a section
        if MODES[mode]["SECTION_EX"].match(line):
            c_section = MODES[mode]["SECTION_EX"].findall(line)[0]
            continue
        conf = _write_to_conf_(conf, line, line_number=lineno, section=c_section, mode=mode)

    return conf


def parse_config_file(conf_file: str | PathLike, mode: str = 'secsie') -> dict:
    """
    Read a config file and return a dictionary of the values inside.

    :param conf_file: A file path to a configuration file
    :param mode: The language of the config file, 'secsie' or 'ini' are supported
    :return: The config as a dict
    """
    with open(conf_file, 'r') as f:
        config = f.read()

    return parse_config(config, mode=mode)
