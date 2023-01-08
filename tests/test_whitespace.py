import secsie


def test_whitespace_insensitivity():
    """
    Tests that secsie ignores whitespace in attribute declaration lines
    """
    config = secsie.parse_config(
        """
key    =     value


                    key2=value2
ur\t=cute
    space-values =   this      should be chilll     bro
    """
    )

    assert config["key"] == "value"
    assert config["key2"] == "value2"
    assert config["ur"] == "cute"
    assert config["space-values"] == "this      should be chilll     bro"


def test_comment_support():
    """
    Tests that secsie ignores octothorpes in values
    """
    config = secsie.parse_config(
        """
    password = som#$scure # this should be amazing
    """
    )

    assert config["password"] == "som#$scure"
