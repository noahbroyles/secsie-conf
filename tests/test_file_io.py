import secsie

from pathlib import Path


def test_parse_ini_file():
    expected = {'PHP': {'engine': 'On', 'short_open_tag': 'Off', 'precision': 14, 'output_buffering': 4096, 'zlib.output_compression': 'Off', 'implicit_flush': 'Off', 'unserialize_callback_func': '', 'serialize_precision': -1, 'disable_functions': ['pcntl_alarm', 'pcntl_fork', 'pcntl_waitpid', 'pcntl_wait', 'pcntl_wifexited', 'pcntl_wifstopped', 'pcntl_wifsignaled', 'pcntl_wifcontinued', 'pcntl_wexitstatus', 'pcntl_wtermsig', 'pcntl_wstopsig', 'pcntl_signal', 'pcntl_signal_get_handler', 'pcntl_signal_dispatch', 'pcntl_get_last_error', 'pcntl_strerror', 'pcntl_sigprocmask', 'pcntl_sigwaitinfo', 'pcntl_sigtimedwait', 'pcntl_exec', 'pcntl_getpriority', 'pcntl_setpriority', 'pcntl_async_signals', 'pcntl_unshare'], 'disable_classes': '', 'zend.enable_gc': 'On', 'zend.exception_ignore_args': 'On', 'expose_php': 'Off', 'max_execution_time': 30, 'max_input_time': 60, 'memory_limit': '128M', 'error_reporting': 'E_ALL & ~E_DEPRECATED & ~E_STRICT', 'display_errors': 'Off', 'display_startup_errors': 'Off', 'log_errors': 'On', 'log_errors_max_len': 1024, 'ignore_repeated_errors': 'Off', 'ignore_repeated_source': 'Off', 'report_memleaks': 'On', 'variables_order': 'GPCS', 'request_order': 'GP', 'register_argc_argv': 'Off', 'auto_globals_jit': 'On', 'post_max_size': '8M', 'auto_prepend_file': '', 'auto_append_file': '', 'default_mimetype': 'text/html', 'default_charset': 'UTF-8', 'doc_root': '', 'user_dir': '', 'enable_dl': 'Off', 'file_uploads': 'On', 'upload_max_filesize': '2M', 'max_file_uploads': 20, 'allow_url_fopen': 'On', 'allow_url_include': 'Off', 'default_socket_timeout': 60}, 'CLI Server': {'cli_server.color': 'On'}, 'Pdo_mysql': {'pdo_mysql.default_socket': ''}, 'mail function': {'SMTP': 'localhost', 'smtp_port': 25, 'mail.add_x_header': 'Off'}, 'ODBC': {'odbc.allow_persistent': 'On', 'odbc.check_persistent': 'On', 'odbc.max_persistent': -1, 'odbc.max_links': -1, 'odbc.defaultlrl': 4096, 'odbc.defaultbinmode': 1}, 'MySQLi': {'mysqli.max_persistent': -1, 'mysqli.allow_persistent': 'On', 'mysqli.max_links': -1, 'mysqli.default_port': 3306, 'mysqli.default_socket': '', 'mysqli.default_host': '', 'mysqli.default_user': '', 'mysqli.default_pw': '', 'mysqli.reconnect': 'Off'}, 'mysqlnd': {'mysqlnd.collect_statistics': 'On', 'mysqlnd.collect_memory_statistics': 'Off'}, 'PostgreSQL': {'pgsql.allow_persistent': 'On', 'pgsql.auto_reset_persistent': 'Off', 'pgsql.max_persistent': -1, 'pgsql.max_links': -1, 'pgsql.ignore_notice': 0, 'pgsql.log_notice': 0}, 'bcmath': {'bcmath.scale': 0}, 'Session': {'session.save_handler': 'files', 'session.use_strict_mode': 0, 'session.use_cookies': 1, 'session.use_only_cookies': 1, 'session.name': 'PHPSESSID', 'session.auto_start': 0, 'session.cookie_lifetime': 0, 'session.cookie_path': '/', 'session.cookie_domain': '', 'session.cookie_httponly': '', 'session.cookie_samesite': '', 'session.serialize_handler': 'php', 'session.gc_probability': 0, 'session.gc_divisor': 1000, 'session.gc_maxlifetime': 1440, 'session.referer_check': '', 'session.cache_limiter': 'nocache', 'session.cache_expire': 180, 'session.use_trans_sid': 0, 'session.sid_length': 26, 'session.trans_sid_tags': ['a=href', 'area=href', 'frame=src', 'form='], 'session.sid_bits_per_character': 5}, 'Assertion': {'zend.assertions': -1}, 'Tidy': {'tidy.clean_output': 'Off'}, 'soap': {'soap.wsdl_cache_enabled': 1, 'soap.wsdl_cache_dir': '/tmp', 'soap.wsdl_cache_ttl': 86400, 'soap.wsdl_cache_limit': 5}, 'ldap': {'ldap.max_links': -1}}
    actual = secsie.parse_config_file('tests/data/php.ini', mode='ini')

    assert expected == actual


def test_read_secsie_file_with_string_name():
    config = secsie.parse_config_file("tests/data/valid-fileio.secsie")

    assert config["bluepill-database-configuration"]["port"] == 2669


def test_read_secsie_file_with_path_obj():
    config_path = Path(__file__).parent / "data" / "valid-fileio.secsie"
    config = secsie.parse_config_file(config_path)

    assert config["bluepill-database-configuration"]["port"] == 2669


def test_write_secsie_config_file():
    path_to_output_file = Path("randomConfigFile.secsie")
    config = {
        "random": {
            "stuff": "goes here"
        }
    }

    # Write the config file
    secsie.generate_config_file(config, path_to_output_file)

    assert path_to_output_file.exists()
