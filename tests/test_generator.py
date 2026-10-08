import secsie


def test_top_level_list_is_written_once():
    """
    Tests that a top-level list is written as a single comma separated line
    """
    generated = secsie.generate_config({"fruits": ["apple", "banana"], "count": 2})

    assert generated == "fruits = apple, banana\ncount = 2\n"
    assert secsie.parse_config(generated) == {"fruits": ["apple", "banana"], "count": 2}
