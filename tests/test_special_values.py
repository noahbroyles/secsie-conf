import secsie


def test_null():
    """
    Tests that secsie recognizes 'null' values in config and parses to None in Python.
    """
    config = secsie.parse_config(
        """
    not-null = none  # none is not converted to None in Python, 'null' is.
    nowl = null
    NOWL = NULL
    """)

    assert config['not-null'] == 'none'
    assert config['nowl'] is None
    assert config['NOWL'] is None


def test_true():
    """
    Tests that secsie recognizes and parses 'truthy' values
    """
    config = secsie.parse_config(
        """
    true = true
    true4u = True
    true2 = yes
    not-true = yes but like also no
    """)

    assert config['true'] is True
    assert config['true4u'] is True
    assert config['true2'] is True
    assert config['not-true'] == 'yes but like also no'


def test_false():
    """
    Tests that secsie recognizes and parses 'falsey' values
    """
    config = secsie.parse_config(
        """
    false = false
    false4u = False
    false2 = no
    not-false = no but like also maybe
    wow_okay = no no NO
    """)

    assert config['false'] is False
    assert config['false4u'] is False
    assert config['false2'] is False
    assert config['not-false'] == 'no but like also maybe'
    assert config['wow_okay'] == 'no no NO'


def test_numerics():
    config = secsie.parse_config(
        """
    int = 42
    negative-int = -42
    float = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
    negative-float = -0.987654321
    zero = 0
    float-test = 53.61.51.231
    """)

    assert config['int'] == 42
    assert config['negative-int'] == -42
    assert config['float'] == 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
    assert config['negative-float'] == -0.987654321
    assert config['zero'] == 0
    assert config['float-test'] == '53.61.51.231'
