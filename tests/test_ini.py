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
