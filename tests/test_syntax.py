import secsie


def test_no_value_assigned():
    no_value_assigned = False
    try:
        conf = secsie.parse_config_file('tests/data/no value assigned.secsie')
    except secsie.InvalidSyntax as error:
        assert error.lineno == 1
        assert error.msg == 'Invalid syntax on line 1: "this" - bad section descriptor or value assignment'
        no_value_assigned = True

    assert no_value_assigned

def test_section_with_spaces():
    section_with_spaces = False
    try:
        conf = secsie.parse_config_file('tests/data/section with spaces.secsie')
    except secsie.InvalidSyntax as error:
        assert error.lineno == 3
        assert error.msg == 'Invalid syntax on line 3: "[this is a section]" - bad section descriptor or value assignment'
        section_with_spaces = True

    assert section_with_spaces


def test_value_with_equals_sign():
    config = secsie.parse_config("""
    val = this=not okay
    """)

    assert config['val'] == 'this=not okay'



def test_blank_value_syntax():
    # While this syntax is valid, please don't do it. Its just wrong.
    config = secsie.parse_config("""
    key =
    """)

    assert config['key'] == ''
