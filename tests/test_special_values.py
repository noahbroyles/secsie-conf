import secsie



def test_null():
    """
    Tests that secsie recognizes special values in config.
    """
    config = secsie.parse_config(
    """
    not-null = none  # none is not converted to None in Python, 'null' is.
    """)

    assert config['not-null'] == 'none'
    