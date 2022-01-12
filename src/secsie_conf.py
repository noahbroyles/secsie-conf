import re


__version__ = 'v1.0.0'


SECTION_EX = re.compile(r'\[([a-zA-Z0-9]+)\]')
FLOAT_EX = re.compile(r'^(\d+[\.]\d*)$')
INT_EX = re.compile(r'^\d+$')


def _write_to_conf_(conf: dict, line, line_number: int, section=None) -> dict:
    key_value = [c.strip() for c in line.split('=')]
    try:
        key, value = key_value[0], key_value[1].split('#')[0].strip()
    except IndexError:
        raise SyntaxError(f'Syntax Error on line {line_number}: "{line}" bad section descriptor or value assignment')

    if ' ' in key:
        raise SyntaxError(f"Syntax Error on line {line_number}: Spaces not allowed in keys")

    if FLOAT_EX.match(value):
        value = float(value)
    elif INT_EX.match(value):
        value = int(value)

    if section is None:
        conf[key] = value
    else:
        if not conf.get(section, False):
            conf[section] = {}
        conf[section][key] = value
        
    return conf


def parse_config(conf_file: str) -> dict:
    with open(conf_file, 'r') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    conf = {}
    c_section = None
    lineno = 0
    for line in lines:
        lineno += 1
        line = line.strip()
        if line == '':  # Skip blank lines
            continue
        if line.startswith('#') or line.startswith(';'):
            continue
        # Check to see if this is a section
        if SECTION_EX.match(line):
            c_section = SECTION_EX.findall(line)[0]
            continue
        conf = _write_to_conf_(conf, line, section=c_section, line_number=lineno)

    return conf


def generate_config(obj: dict, output_file: str = None) -> str:
    conf = """# This was auto-generated from JSON by sexyConf

# These are the rules of the language:
# Comment lines can begin with '#' or ';', but inline comments can only begin with the octothorpe.
# Whitespace is ignored, except in key names and section tag names. The config consists of sections, and attributes(keys and values).
# A sections end when the next section begins. Attributes do not need to be in a section to be valid.
# To begin a section use the following syntax:
; [section1]
# The syntax for an attribute line is:
; key = value
# Spaces are not allowed in keys or section tags. Only abc, ABC and 123 are allowed in section tag names.
# Leading and trailing whitespace is removed from keys and values.\n\n"""
    for key, value in obj.items():
        if isinstance(value, dict):
            conf += f"\n[{key}]\n"
            for k, v in value.items():
                conf += f"\t{k} = {v}\n"
            conf += "\n"
            continue
        conf += f"{key} = {value}\n"

    if output_file:
        with open(output_file, 'w') as f:
            f.write(conf)

    return conf
