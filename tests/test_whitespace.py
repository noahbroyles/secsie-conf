import secsie


def test_whitespace_insensitivity():
    """
    Tests that secsie ignores whitespace in attribute declaration lines
    """
    config = secsie.parse_config(
    """
key    =     value
                    key2=value2
ur\t=mom
    """
    )

    assert config['key'] == 'value'
    assert config['key2'] == 'value2'
    assert config['ur'] == 'mom'
