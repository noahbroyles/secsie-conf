import secsie


def test_ini_quoted_strings():
    """
    Tests that secsie will not parse quoted strings any farther in ini mode
    """
    config = secsie.parse_config(
        """
        aws_account_id = "090192837418"
        """,
        mode="ini"
    )

    assert config["aws_account_id"] == "090192837418"


def test_ini_quoted_strings_with_commas_are_not_lists():
    """
    Tests that a quoted string containing commas stays a single string in ini mode, while an unquoted one is a list
    """
    config = secsie.parse_config(
        """
        quoted = "a=href,area=href, frame=src"
        unquoted = a, b, c
        """,
        mode="ini"
    )

    assert config["quoted"] == "a=href,area=href, frame=src"
    assert config["unquoted"] == ["a", "b", "c"]
