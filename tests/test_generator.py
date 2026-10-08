import pytest
import secsie


def test_top_level_list_is_written_once():
    """
    Tests that a top-level list is written as a single comma separated line
    """
    generated = secsie.generate_config({"fruits": ["apple", "banana"], "count": 2})

    assert generated == "fruits = apple, banana\ncount = 2\n"
    assert secsie.parse_config(generated) == {"fruits": ["apple", "banana"], "count": 2}


def test_lists_of_non_strings_are_generated():
    """
    Tests that lists containing ints, floats, bools, and None can be written, and read back identically
    """
    conf = {"top": [1, 2.5, True, False, None, "text"], "section": {"nested": [1, None, False, "text"]}}

    assert secsie.parse_config(secsie.generate_config(conf)) == conf


def test_none_and_bools_round_trip():
    """
    Tests that None is written as null (not the string 'None') and bools survive a round trip
    """
    conf = {"nothing": None, "yes": True, "no": False, "section": {"nothing": None, "yes": True, "no": False}}
    generated = secsie.generate_config(conf)

    assert "None" not in generated
    assert secsie.parse_config(generated) == conf


def test_empty_strings_are_commented_out():
    """
    Tests that empty strings are commented out consistently, at the top level and in sections
    """
    generated = secsie.generate_config({"blank": "", "kept": 1, "section": {"blank": "", "kept": 2}})

    assert ";blank = \n" in generated
    assert ";\tblank = \n" in generated
    assert secsie.parse_config(generated) == {"kept": 1, "section": {"kept": 2}}


def test_nested_dicts_raise_type_error():
    """
    Tests that a dict inside a section raises a clear error instead of generating a corrupt config
    """
    with pytest.raises(TypeError, match=r"'db\.options' is a dict.*nested dicts are not supported"):
        secsie.generate_config({"db": {"host": "localhost", "options": {"ssl": True}}})


def test_space_hash_in_string_raises_value_error():
    """
    Tests that strings containing a space followed by # (an inline comment) are rejected
    """
    with pytest.raises(ValueError, match=r"'password' contains a space followed by '#'"):
        secsie.generate_config({"password": "pass #word"})

    with pytest.raises(ValueError, match=r"'section\.items' contains a space followed by '#'"):
        secsie.generate_config({"section": {"items": ["fine", "#not fine"]}})


def test_hash_without_leading_space_round_trips():
    """
    Tests that a # that is not preceded by a space is a valid part of a value, like in passwords
    """
    conf = {"password": "p#ss#w0rd", "section": {"password": "som#$cure", "list": ["a#b", "c"]}}

    assert secsie.parse_config(secsie.generate_config(conf)) == conf


def test_indent_is_used_for_lists_in_sections():
    """
    Tests that every line in a section, including lists, uses the indent that was passed in
    """
    conf = {"s": {"number": 1, "items": ["x", "y"], "text": "hello"}}

    assert secsie.generate_config(conf, indent="  ") == "\n[s]\n  number = 1\n  items = x, y\n  text = hello\n\n"
    assert secsie.generate_config(conf, indent="") == "\n[s]\nnumber = 1\nitems = x, y\ntext = hello\n\n"
    assert secsie.generate_config(conf) == "\n[s]\n\tnumber = 1\n\titems = x, y\n\ttext = hello\n\n"


def test_top_level_keys_are_written_before_sections():
    """
    Tests that a top level key which comes after a section in the dict is not read back as part of that section
    """
    conf = {"first": 1, "section": {"inside": 2}, "last": [3, 4], "other": {"inside": 5}, "blank": ""}
    generated = secsie.generate_config(conf)

    assert generated == "first = 1\nlast = 3, 4\n;blank = \n\n[section]\n\tinside = 2\n\n\n[other]\n\tinside = 5\n\n"
    assert secsie.parse_config(generated) == {
        "first": 1, "last": [3, 4], "section": {"inside": 2}, "other": {"inside": 5}
    }
