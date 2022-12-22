r"""
---------------------------------------
   _____                    _      
  / ___/ ___   _____ _____ (_)___   
  \__ \ / _ \ / ___// ___// // _ \  
 ___/ //  __// /__ (__  )/ //  __/  
/____/ \___/ \___//____//_/ \___/  
---------------------------------------
A small library for parsing configuration files.
Supports secsie and ini formats. Not suitable for writing .ini files, but reads them just fine.
"""

__version__ = '2.1.3'
__author__ = 'Noah Broyles'
__all__ = [
    'InvalidSyntax',
    'parse_config',
    'parse_config_file',
    'generate_config',
    'generate_config_file'
]

import re
from pathlib import Path

MODES = {
    "secsie": dict(
        SECTION_EX=re.compile(r'^\[([a-zA-Z\d_-]+)]$'),
        FLOAT_EX=re.compile(r'^(-?\d+[.]\d*)$'),
        FALSE_EX=re.compile(r'^(false|no)$', re.IGNORECASE),
        NULL_EX=re.compile(r'^null$', re.IGNORECASE),
        TRUE_EX=re.compile(r'^(true|yes)$', re.IGNORECASE),
        INT_EX=re.compile(r'^-?\d+$')
    ),
    "ini": dict(
        SECTION_EX=re.compile(r'^\[([a-zA-Z\d _-]+)]$'),
        FLOAT_EX=re.compile(r'^(-?\d+[.]\d*)$'),
        FALSE_EX=re.compile(r'^(false|no)$', re.IGNORECASE),
        NULL_EX=re.compile(r'^null$', re.IGNORECASE),
        TRUE_EX=re.compile(r'^(true|yes)$', re.IGNORECASE),
        INT_EX=re.compile(r'^-?\d+$')
    )
}


class InvalidSyntax(SyntaxError):
    """This happens when the config you're trying to parse is invalid."""

    def __init__(self, error_message: str, line_number: int):
        super().__init__(f"Invalid syntax on line {line_number}: {error_message}")
        self.lineno = line_number


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

    if MODES[mode]["FLOAT_EX"].match(value):
        value = float(value)
    elif MODES[mode]["INT_EX"].match(value):
        value = int(value)
    elif MODES[mode]["NULL_EX"].match(value):
        value = None
    elif MODES[mode]["TRUE_EX"].match(value):
        value = True
    elif MODES[mode]["FALSE_EX"].match(value):
        value = False

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
    lines = config.split('\n')
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


def parse_config_file(conf_file: str, mode: str = 'secsie') -> dict:
    """
    Read a config file and return a dictionary of the values inside.

    :param conf_file: A file path to a configuration file
    :param mode: The language of the config file, 'secsie' or 'ini' are supported
    :return: The config as a dict
    """
    with open(conf_file, 'r') as f:
        config = f.read()

    return parse_config(config, mode=mode)


def generate_config(conf_obj: dict) -> str:
    """Generate and return a valid config from an object.
    Will save the config if an output file is passed.
    
    This WILL NOT currently write valid .ini files, so don't even try. The only output format is secsie.

    :param conf_obj: The dictionary to parse into a configuration language string
    :return: a string of configuration code
    """

    conf = ''
    for key, value in conf_obj.items():
        if isinstance(value, dict):
            conf += f"\n[{key.replace(' ', '')}]\n"
            for k, v in value.items():
                conf += f"{';' if v == '' else ''}\t{k} = {v}\n"
            conf += "\n"
            continue
        conf += f"{key} = {value}\n"

    return conf


def generate_config_file(conf_obj: dict, output_file: str):
    """
    Generate and write a config file from a dictionary of keys and values

    :param conf_obj: The dictionary to render into the secsie config language
    :param output_file: The file to write to
    """
    output_file = Path(output_file)
    conf = generate_config(conf_obj)

    with open(output_file, 'w') as f:
        f.write(f"# {output_file.name} auto-generated by secsie\n{conf}")
