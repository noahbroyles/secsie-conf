# secsie-conf
SecsieConf is a configuration language made for speed and beauty. Instead of writing config files in JSON (don't get me wrong, this *FAR* better than a lot of other crap), you can save time writing your config files in secsie.  
### Advantages over JSON:
- easier to read
- faster to write
- automatically parses datatypes such as ints, floats, strings, bools, and null values with no special syntax required


## Language Contructs
These are the rules of the language:
1. Comment lines begin with `#` or `;`, but inline comments can only begin with the octothorpe (`#`).
2. Whitespace is ignored everywhere except in key names and section tag names.
3. A config file consists of sections and attributes(keys and values).
4. A section ends where the next section begins. Attributes declared before sections are valid.
5. To begin a section use the following syntax:
```markdown
[section1]
```
6. The syntax for an attribute line is:
```conf
key = value
```
7. Spaces are not allowed in key names or section tags. Only `a-z`, `A-Z` and `0-9` are allowed in section tag names, while special characters are allowed in key names.
8. Values can consist of any character except `#`. Leading and trailing spaces are removed, however.
