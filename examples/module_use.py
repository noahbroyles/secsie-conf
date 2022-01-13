
import json
import secsie

# To get a dict from a config file
config = secsie.parse_config_file('examples/valid.secsie.conf')
print(json.dumps(config, indent=2))  # For prettyness

# Read .ini file
config = secsie.parse_config_file('examples/php.ini', mode='ini')

# write secsie file from config obj
secsie.generate_config_file(config, output_file='examples/php_ini.secsie.conf')
