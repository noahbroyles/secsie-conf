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
from secsie.exceptions import InvalidSyntax
from secsie.parser import parse_config, parse_config_file
from secsie.generator import generate_config, generate_config_file


__version__ = '3.0.2'
__author__ = 'Noah Broyles'
__all__ = [
    'InvalidSyntax',
    'parse_config',
    'parse_config_file',
    'generate_config',
    'generate_config_file'
]
