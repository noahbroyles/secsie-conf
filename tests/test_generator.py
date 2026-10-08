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
