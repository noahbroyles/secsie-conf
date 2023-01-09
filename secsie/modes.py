"""
modes.py

Contains a dictionary of regular expressions used to match special types, such as numbers, booleans, and nulls.
"""
import re


MODES = {
    "secsie": dict(
        SECTION_EX=re.compile(r"^\[([a-zA-Z\d_-]+)]$"),
        FLOAT_EX=re.compile(r"^(-?\d+[.]\d*)$"),
        FALSE_EX=re.compile(r"^(false|no)$", re.IGNORECASE),
        NULL_EX=re.compile(r"^null$", re.IGNORECASE),
        TRUE_EX=re.compile(r"^(true|yes)$", re.IGNORECASE),
        INT_EX=re.compile(r"^-?\d+$"),
    ),
    "ini": dict(
        SECTION_EX=re.compile(r"^\[([a-zA-Z\d _-]+)]$"),
        FLOAT_EX=re.compile(r"^(-?\d+[.]\d*)$"),
        FALSE_EX=re.compile(r"^(false|no)$", re.IGNORECASE),
        NULL_EX=re.compile(r"^null$", re.IGNORECASE),
        TRUE_EX=re.compile(r"^(true|yes)$", re.IGNORECASE),
        INT_EX=re.compile(r"^-?\d+$"),
    ),
}
