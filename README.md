# secsie-conf
```console
pip3 install secsie-conf
```
Secsie is a configuration language parser for Python, made for speed and beauty. Instead of writing config files in JSON (don't get me wrong, JSON is *FAR* better than a lot of other things you could use (cough cough XML)), you can save time writing your config files in `secsie`.  
The `secsie` language format is very similar to `ini`, except just a little better. You can use `secsie-conf` to read `.ini` files into Python `dict`s. `secsie-conf` will NOT write `.ini` files however, at least at this stage.  

I also wrote a version for Java, which is available at [github.com/noahbroyles/secsie-java](https://github.com/noahbroyles/secsie-java). You can use it to parse `.properties` files. Minecraft will probably adopt this in the next few months for thier `server.properties` ;)  

### Advantages over JSON:
- easier to read
- faster to write
- no special syntax required for strings vs ints, floats, bools, etc.
- file size usually smaller than readable JSON


## Secsie Language Contructs
These are the rules of the secsie config language:
1. Comment lines begin with `#` or `;`, but inline comments can only begin with the octothorpe (`#`) and _must_ have a space preceeding them.
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
7. Spaces are not allowed in key names or section tags. Only `a-z`(case insensitive), `0-9`, `_`, and `-` are allowed in section tag names, while other special characters *are* allowed in key names.
8. Values can consist of any character except `#`. Leading and trailing whitespace is removed.

## INI
`secsie-conf` can be used to read `.ini` files, as long as the mode `ini` is specifed to the parser. The rules of interpretation for `.ini` files vary slightly.
### Differences:
- Section names are allowed to contain spaces and dashes
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
[special_values]
    int = 42
    float = 269.887
    truth = yes
    falsehood = no
    true = true
    ; I don't encourage this but it's valid ;)
    false = FaLSe

    # Null value
    nah = Null

[anotherSection]
    # The indent here is optional, included for readability
    sections = are amazing

```
Parse result:
```python
{'before_section': 'totally okay', 'special_values': {'int': 42, 'float': 269.887, 'truth': True, 'falsehood': False, 'true': True, 'false': False, 'nah': None}, 'anotherSection': {'sections': 'are amazing'}}
```

## Module Usage
### Read a `secsie` config file as a `dict`:
```python
import json
import secsie

# To get a dict from a config file
config = secsie.parse_config_file('examples/valid.secsie.conf')
print(json.dumps(config, indent=2))  # For prettyness
```
Result:
```json
{
  "before_section": "totally okay",
  "special_values": {
    "int": 42,
    "float": 269.887,
    "truth": true,
    "falsehood": false,
    "true": true,
    "false": false,
    "nah": null
  },
  "anotherSection": {
    "sections": "are amazing"
  }
}
```
### Read an `.ini` file:
```python
import json
import secsie

# This might not work...
config = secsie.parse_config_file('examples/php.ini')
```
Result:
```python
...Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/nbroyles/PycharmProjects/secsie-conf/secsie/__init__.py", line 109, in parse_config_file
    conf = _write_to_conf_(conf, line, line_number=lineno, section=c_section, mode=mode)
  File "/home/nbroyles/PycharmProjects/secsie-conf/secsie/__init__.py", line 63, in _write_to_conf_
    raise InvalidSyntax(f'Syntax Error on line {line_number}: "{line}" bad section descriptor or value assignment')
secsie.InvalidSyntax: Syntax Error on line 955: "[CLI Server]" bad section descriptor or value assignment
```
We can see that this up and broke. Dub tee eff?! Actually, its okay. Spaces aren't allowed in `secsie` section names, remember? When reading an `.ini` file, we need to pass the argument `mode='ini'` to the `parse_config_file` function, like this:  
```python
config = secsie.parse_config_file('examples/php.ini', mode='ini')
print(json.dumps(config, indent=2))
```
```json
{
  "PHP": {
    "engine": "On",
    "short_open_tag": "Off",
    "precision": 14,
    "output_buffering": 4096,
    "zlib.output_compression": "Off",
    "implicit_flush": "Off",
    "unserialize_callback_func": "",
    "serialize_precision": -1,
    "disable_functions": "pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,pcntl_unshare,",
    "disable_classes": "",
    "zend.enable_gc": "On",
    "zend.exception_ignore_args": "On",
    "expose_php": "Off",
    "max_execution_time": 30,
    "max_input_time": 60,
    "memory_limit": "128M",
    "error_reporting": "E_ALL & ~E_DEPRECATED & ~E_STRICT",
    "display_errors": "Off",
    "display_startup_errors": "Off",
    "log_errors": "On",
    "log_errors_max_len": 1024,
    "ignore_repeated_errors": "Off",
    "ignore_repeated_source": "Off",
    "report_memleaks": "On",
    "variables_order": "GPCS",
    "request_order": "GP",
    "register_argc_argv": "Off",
    "auto_globals_jit": "On",
    "post_max_size": "8M",
    "auto_prepend_file": "",
    "auto_append_file": "",
    "default_mimetype": "text/html",
    "default_charset": "UTF-8",
    "doc_root": "",
    "user_dir": "",
    "enable_dl": "Off",
    "file_uploads": "On",
    "upload_max_filesize": "2M",
    "max_file_uploads": 20,
    "allow_url_fopen": "On",
    "allow_url_include": "Off",
    "default_socket_timeout": 60
  },
  "CLI Server": {
    "cli_server.color": "On"
  },
  "Pdo_mysql": {
    "pdo_mysql.default_socket": ""
  },
  "mail function": {
    "SMTP": "localhost",
    "smtp_port": 25,
    "mail.add_x_header": "Off"
  },
  "ODBC": {
    "odbc.allow_persistent": "On",
    "odbc.check_persistent": "On",
    "odbc.max_persistent": -1,
    "odbc.max_links": -1,
    "odbc.defaultlrl": 4096,
    "odbc.defaultbinmode": 1
  },
  "MySQLi": {
    "mysqli.max_persistent": -1,
    "mysqli.allow_persistent": "On",
    "mysqli.max_links": -1,
    "mysqli.default_port": 3306,
    "mysqli.default_socket": "",
    "mysqli.default_host": "",
    "mysqli.default_user": "",
    "mysqli.default_pw": "",
    "mysqli.reconnect": "Off"
  },
  "mysqlnd": {
    "mysqlnd.collect_statistics": "On",
    "mysqlnd.collect_memory_statistics": "Off"
  },
  "PostgreSQL": {
    "pgsql.allow_persistent": "On",
    "pgsql.auto_reset_persistent": "Off",
    "pgsql.max_persistent": -1,
    "pgsql.max_links": -1,
    "pgsql.ignore_notice": 0,
    "pgsql.log_notice": 0
  },
  "bcmath": {
    "bcmath.scale": 0
  },
  "Session": {
    "session.save_handler": "files",
    "session.use_strict_mode": 0,
    "session.use_cookies": 1,
    "session.use_only_cookies": 1,
    "session.name": "PHPSESSID",
    "session.auto_start": 0,
    "session.cookie_lifetime": 0,
    "session.cookie_path": "/",
    "session.cookie_domain": "",
    "session.cookie_httponly": "",
    "session.cookie_samesite": "",
    "session.serialize_handler": "php",
    "session.gc_probability": 0,
    "session.gc_divisor": 1000,
    "session.gc_maxlifetime": 1440,
    "session.referer_check": "",
    "session.cache_limiter": false,
    "session.cache_expire": 180,
    "session.use_trans_sid": 0,
    "session.sid_length": 26,
    "session.trans_sid_tags": "a=href,area=href,frame=src,form=",
    "session.sid_bits_per_character": 5
  },
  "Assertion": {
    "zend.assertions": -1
  },
  "Tidy": {
    "tidy.clean_output": "Off"
  },
  "soap": {
    "soap.wsdl_cache_enabled": 1,
    "soap.wsdl_cache_dir": "/tmp",
    "soap.wsdl_cache_ttl": 86400,
    "soap.wsdl_cache_limit": 5
  },
  "ldap": {
    "ldap.max_links": -1
  }
}
```
That **^**'s a whole PHP configuration file converted to some <s>sexy</s> secsie JSON!  
### Write a `secsie` file:
Now that we have the `php.ini` contents stored in `config`, let's output it in `secsie`!
```python
secsie.generate_config_file(config, output_file='examples/php_ini.secsie.conf')
```
Output (`examples/php_ini.secsie.conf`):
```ini
# php_ini.secsie.conf auto-generated by secsie


[PHP]
	engine = On
	short_open_tag = Off
	precision = 14
	output_buffering = 4096
	zlib.output_compression = Off
	implicit_flush = Off
;	unserialize_callback_func = 
	serialize_precision = -1
	disable_functions = pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,pcntl_unshare,
;	disable_classes = 
	zend.enable_gc = On
	zend.exception_ignore_args = On
	expose_php = Off
	max_execution_time = 30
	max_input_time = 60
	memory_limit = 128M
	error_reporting = E_ALL & ~E_DEPRECATED & ~E_STRICT
	display_errors = Off
	display_startup_errors = Off
	log_errors = On
	log_errors_max_len = 1024
	ignore_repeated_errors = Off
	ignore_repeated_source = Off
	report_memleaks = On
	variables_order = GPCS
	request_order = GP
	register_argc_argv = Off
	auto_globals_jit = On
	post_max_size = 8M
;	auto_prepend_file = 
;	auto_append_file = 
	default_mimetype = text/html
	default_charset = UTF-8
;	doc_root = 
;	user_dir = 
	enable_dl = Off
	file_uploads = On
	upload_max_filesize = 2M
	max_file_uploads = 20
	allow_url_fopen = On
	allow_url_include = Off
	default_socket_timeout = 60


[CLIServer]
	cli_server.color = On


[Pdo_mysql]
;	pdo_mysql.default_socket = 


[mailfunction]
	SMTP = localhost
	smtp_port = 25
	mail.add_x_header = Off


[ODBC]
	odbc.allow_persistent = On
	odbc.check_persistent = On
	odbc.max_persistent = -1
	odbc.max_links = -1
	odbc.defaultlrl = 4096
	odbc.defaultbinmode = 1


[MySQLi]
	mysqli.max_persistent = -1
	mysqli.allow_persistent = On
	mysqli.max_links = -1
	mysqli.default_port = 3306
;	mysqli.default_socket = 
;	mysqli.default_host = 
;	mysqli.default_user = 
;	mysqli.default_pw = 
	mysqli.reconnect = Off


[mysqlnd]
	mysqlnd.collect_statistics = On
	mysqlnd.collect_memory_statistics = Off


[PostgreSQL]
	pgsql.allow_persistent = On
	pgsql.auto_reset_persistent = Off
	pgsql.max_persistent = -1
	pgsql.max_links = -1
	pgsql.ignore_notice = 0
	pgsql.log_notice = 0


[bcmath]
	bcmath.scale = 0


[Session]
	session.save_handler = files
	session.use_strict_mode = 0
	session.use_cookies = 1
	session.use_only_cookies = 1
	session.name = PHPSESSID
	session.auto_start = 0
	session.cookie_lifetime = 0
	session.cookie_path = /
;	session.cookie_domain = 
;	session.cookie_httponly = 
;	session.cookie_samesite = 
	session.serialize_handler = php
	session.gc_probability = 0
	session.gc_divisor = 1000
	session.gc_maxlifetime = 1440
;	session.referer_check = 
	session.cache_limiter = False
	session.cache_expire = 180
	session.use_trans_sid = 0
	session.sid_length = 26
	session.trans_sid_tags = a=href,area=href,frame=src,form=
	session.sid_bits_per_character = 5


[Assertion]
	zend.assertions = -1


[Tidy]
	tidy.clean_output = Off


[soap]
	soap.wsdl_cache_enabled = 1
	soap.wsdl_cache_dir = /tmp
	soap.wsdl_cache_ttl = 86400
	soap.wsdl_cache_limit = 5


[ldap]
	ldap.max_links = -1


```
You should notice 2 things: 
1. Keys and value assignments are separated by an equals sign with a space ON BOTH SIDES! `key = value`, **NOT** `key=value`. That is ugly and lazy. This ain't minified JS, son. [They make things for that...](https://www.amazon.com/dp/B089C3TZL9)
2. Blank values were commented out. If you disagree with that, *MAKE 'EM NULL*! `key = ` doesn't say anything.