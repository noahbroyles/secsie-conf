# secsie-conf
Secsie is a configuration language parser for Python, made for speed and beauty. Instead of writing config files in JSON (don't get me wrong, JSON is *FAR* better than a lot of other things you could use (cough cough XML)), you can save time writing your config files in `secsie`.  
The `secsie` language format is very similar to `ini`, except just a little better. You can use `secsie-conf` to read `.ini` files into Python `dict`s. `secsie-conf` will NOT write `.ini` files however, at least at this stage.

### Advantages over JSON:
- easier to read
- faster to write
- no special syntax required for strings vs ints, floats, bools, etc.


## Secsie Language Contructs
These are the rules of the secsie config language:
1. Comment lines begin with `#` or `;`, but inline comments can only begin with the octothorpe (`#`).
2. Whitespace is ignored everywhere except in key names and section tag names.
3. A config file consists of sections and attributes(keys and values).
4. A section ends where the next section begins. Attributes declared before sections are valid.
5. To begin a section use the following syntax:
```ini
[section1]
# attribute lines in this section follow
```
6. The syntax for an attribute line is:
```ini
key = value
```
7. Spaces are not allowed in key names or section tags. Only `a-z`, `A-Z`, `0-9` and `_` are allowed in section tag names, while special characters *are* allowed in key names.
8. Values can consist of any character except `#`. Leading and trailing whitespace is removed.

## INI:
`secsie-conf` can be used to read `.ini` files, as long as the mode `ini` is specifed to the parser. The rules of interpretation for `.ini` files vary slightly.
### Differences:
- Section names are allowed to contain spaces
- quoted strings are valid, but the quotes are removed (there is no need to quote string in `secsie` ;)  
`secsie-conf` can **NOT** be used to write `.ini` files. You can read an `.ini` file and output it in valid `secsie`, but you cannot expect valid `.ini` output.

## Valid values
Secsie supports strings, ints, floats, null types, and booleans. All of these types can be written out by themselves and will automatically be converted to the appropriate native type.
### Strings:
```ini
# Spaces are allowed in string value
string_key = whatever value you want
```
### Ints:
```ini
numb = 42  # Automatically converted to int when parsed
```
### Floats:
```ini
pi = 3.14159265  # Automatically converted to float when parsed
```
### Booleans:
```ini
# True and yes are truthy values (case insensitive)
truth = true
truth2 = True
truth3 = yes
# False and no are falsy values (case insensitive)
untruth = falsE
untruth2 = False
untruth3 = no
```
### Null type (`None`):
```ini
# 'null' is used as the NoneType (case insensitive)
nothing = null
```

## Examples
`examples/valid.secsie.conf`:
```ini
; This is an example of a valid secsie file

before_section = totally okay

# Whitespace don't matter

; Here are examples of how types are interpreted(no keywords are off limits!)
int = 42
float = 269.887
truth = yes
falsehood = no
true = true
; I don't encourage this but it's valid ;)
false = FaLSe

# Null value
nah = Null

[SectionTime]
    # The indent here is optional, included for readability
    sections = are amazing

[nextSection248]
    intVal = 2
```
Parse result:
```python
{'before_section': 'totally okay', 'int': 42, 'float': 269.887, 'truth': True, 'falsehood': False, 'true': True, 'false': False, 'nah': None, 'SectionTime': {'sections': 'are amazing'}, 'nextSection248': {'intVal': 2}}
```

## How to use the module
```python
import secsie
```