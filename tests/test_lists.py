import secsie


# Declare config with a list to test
list_config = \
"""
items = iPod, iPhone, iPad, other-stuff 
blankStringList = bananas, coconuts, grapes,
regular-string = ordinary stuff
specialList = good stuff, 42, 2945.29, False, null, wow dude! Amazing!
"""


def test_lists_are_parsed_correctly():
    config = secsie.parse_config(list_config)

    # Test that "items" is a list
    assert isinstance(config["items"], list)

    # Test that "items" has 4 entries
    assert len(config["items"]) == 4

    # Make sure regular strings are not interpreted as lists
    assert config["regular-string"] == "ordinary stuff"

    # Make sure each item in the list was parsed correctly
    assert config["items"][0] == "iPod"
    assert config["items"][1] == "iPhone"
    assert config["items"][2] == "iPad"
    assert config["items"][3] == "other-stuff"


def test_special_types_in_list():
    special_list = secsie.parse_config(list_config)["specialList"]

    # str type
    assert special_list[0] == "good stuff"
    assert special_list[5] == "wow dude! Amazing!"

    # int type
    assert special_list[1] == 42

    # float type
    assert special_list[2] == 2945.29

    # bool type
    assert special_list[3] == False

    # None type
    assert special_list[4] is None



def test_empty_string_in_secsie_list():
    items = secsie.parse_config(
        list_config,
        mode='secsie'
    )["items"]

    # Make sure that there are 4 items in the list
    assert len(items) == 4

    # Make sure that the last item is an empty string
    assert items[-1] == ''


def test_no_empty_string_in_ini_list():
    items = secsie.parse_config(
        list_config,
        mode='ini'
    )["items"]

    # Make sure there are only 3 items in the list
    assert len(items) == 3

    # Make sure the last item is NOT a blank string
    assert items[-1] != ''
