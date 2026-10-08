import random
import pytest
import secsie


def roundtrip(conf: dict, **kwargs) -> dict:
    """
    Write a config in ini and read it back the way a user would
    """
    return secsie.parse_config(secsie.generate_config(conf, mode="ini", **kwargs), mode="ini")


def canonical(value):
    """
    Turn a value into something that is only equal to another value of the same *type*, which a plain == is not
    (True == 1 and 1 == 1.0 in Python, but a bool, an int, and a float are all different things to a config file)
    """
    if isinstance(value, dict):
        return {key: canonical(val) for key, val in value.items()}
    if isinstance(value, list):
        return [canonical(val) for val in value]
    return type(value).__name__, value


def test_generated_ini_layout():
    """
    Tests the shape of the output: top level keys first, a blank line between sections, no indentation
    """
    conf = {"name": "app", "db": {"host": "localhost", "port": 5432}, "debug": False, "cache": {"size": 10}}

    assert secsie.generate_config(conf, mode="ini") == (
        "name = app\n"
        "debug = false\n"
        "\n"
        "[db]\n"
        "host = localhost\n"
        "port = 5432\n"
        "\n"
        "[cache]\n"
        "size = 10\n"
    )


def test_top_level_keys_stay_top_level():
    """
    Tests that a top level key which comes after a section in the dict is not read as part of that section
    """
    conf = {"section": {"inside": 1}, "outside": 2}

    assert roundtrip(conf) == conf


def test_indent():
    """
    Tests that keys in a section are indented when asked to be, and only those
    """
    conf = {"top": 1, "section": {"a": 1, "b": [1, 2]}}

    assert secsie.generate_config(conf, indent="  ", mode="ini") == "top = 1\n\n[section]\n  a = 1\n  b = 1, 2\n"


def test_types_round_trip():
    """
    Tests that every type secsie knows about survives a trip through ini
    """
    conf = {"text": "hello world", "int": -42, "float": 3.14, "yes": True, "no": False, "nothing": None}

    assert canonical(roundtrip(conf)) == canonical(conf)


def test_section_names_with_spaces():
    """
    Tests that section names ini allows are written as they are, unlike secsie mode which has to remove the spaces
    """
    conf = {"CLI Server": {"cli_server.color": "On"}}

    assert roundtrip(conf) == conf


@pytest.mark.parametrize("text", [
    "090192837418",  # digits that must keep their leading zero
    "42", "-1", "3.14",
    "true", "False", "yes", "NO", "null", "Null",
    "a, b, c", "a,b",
    "",
    " padded ", "\tpadded",
    "#starts-with-hash",
    'say "hi", then leave',  # quotes in the middle of a string are fine, even when it needs quoting
])
def test_strings_that_would_change_are_quoted(text):
    """
    Tests that strings which would otherwise be read as another type, split into a list, or trimmed stay strings
    """
    conf = {"value": text, "section": {"value": text}}

    assert canonical(roundtrip(conf)) == canonical(conf)


def test_plain_strings_are_not_quoted():
    """
    Tests that quotes are only added when they have to be
    """
    conf = {"a": "plain", "b": "E_ALL & ~E_DEPRECATED", "c": "p#ss", "d": "a=b"}
    generated = secsie.generate_config(conf, mode="ini")

    assert generated == "a = plain\nb = E_ALL & ~E_DEPRECATED\nc = p#ss\nd = a=b\n"


def test_empty_string_is_kept():
    """
    Tests that, unlike secsie mode which comments them out, empty strings are written as "" and read back
    """
    assert secsie.generate_config({"blank": ""}, mode="ini") == 'blank = ""\n'
    assert roundtrip({"blank": "", "section": {"blank": ""}}) == {"blank": "", "section": {"blank": ""}}


@pytest.mark.parametrize("number", [
    0.0, -0.0, 1.5, 10.0,
    1e-07, 5e-324,  # repr writes these with an exponent
    1e16, 1.2345678901234568e+17, 1.7976931348623157e308,
])
def test_floats_round_trip(number):
    """
    Tests that floats come back as the same float, including the ones repr writes with an exponent
    """
    result = roundtrip({"number": number})["number"]

    assert isinstance(result, float)
    assert result == number


def test_lists():
    """
    Tests lists of mixed types, including the ones that need a trailing comma or a lone comma to be lists at all
    """
    conf = {
        "mixed": ["text", 1, 2.5, True, None],
        "single": ["only"],
        "single_number": [7],
        "none": [],
        "section": {"mixed": ["a", 1], "single": ["only"], "none": []},
    }

    assert canonical(roundtrip(conf)) == canonical(conf)


@pytest.mark.parametrize("bad_item", ["", " padded", "has, comma", "42", "true", "null", "1.5"])
def test_list_items_that_cannot_be_written_raise(bad_item):
    """
    Tests that a list item that would be dropped, trimmed, split, or converted is an error and not a silent change
    """
    with pytest.raises(ValueError, match=r"'items' has a list item"):
        secsie.generate_config({"items": ["fine", bad_item]}, mode="ini")


@pytest.mark.parametrize("text, reason", [
    ('"quoted"', "quote character"),
    ('ends with a quote"', "quote character"),
    ("line one\nline two", "line break"),
    ("carriage\rreturn", "line break"),
    ("not a comment #really", "space followed by '#'"),
    ("a = b", "next to an '='"),
    ("a =b", "next to an '='"),
])
def test_strings_that_cannot_be_written_raise(text, reason):
    """
    Tests that strings ini has no way to write are errors that say why, wherever they are
    """
    with pytest.raises(ValueError, match=reason):
        secsie.generate_config({"top": text}, mode="ini")

    with pytest.raises(ValueError, match=r"'section\.nested'"):
        secsie.generate_config({"section": {"nested": text}}, mode="ini")


@pytest.mark.parametrize("number", [float("inf"), float("-inf"), float("nan")])
def test_non_finite_floats_raise(number):
    with pytest.raises(ValueError, match="no way to represent"):
        secsie.generate_config({"number": number}, mode="ini")


def test_list_starting_with_a_quote_raises():
    """
    Tests that a list whose first item is a quote is refused, since the reader would take it for a quoted string
    """
    with pytest.raises(ValueError, match="starts with a quote"):
        secsie.generate_config({"items": ['"', "b"]}, mode="ini")

    # A quote anywhere else in the list is just a character
    conf = {"items": ["a", '"', 'b"c']}
    assert roundtrip(conf) == conf


def test_unsupported_types_raise():
    with pytest.raises(TypeError, match="nested dicts are not supported"):
        secsie.generate_config({"section": {"inner": {"a": 1}}}, mode="ini")

    with pytest.raises(TypeError, match="inside a list"):
        secsie.generate_config({"items": [[1, 2]]}, mode="ini")

    with pytest.raises(TypeError, match="is a tuple"):
        secsie.generate_config({"items": (1, 2)}, mode="ini")


@pytest.mark.parametrize("key", ["has space", "has\ttab", "has=equals", "#comment", ";comment", ""])
def test_bad_keys_raise(key):
    with pytest.raises((ValueError, TypeError), match="key"):
        secsie.generate_config({key: 1}, mode="ini")

    with pytest.raises((ValueError, TypeError), match="key"):
        secsie.generate_config({"section": {key: 1}}, mode="ini")


@pytest.mark.parametrize("name", ["dotted.name", "has]bracket", "", "new\nline"])
def test_bad_section_names_raise(name):
    with pytest.raises(ValueError, match="not a valid section name"):
        secsie.generate_config({name: {"a": 1}}, mode="ini")


def test_unknown_mode_raises():
    with pytest.raises(ValueError, match="Unknown mode 'toml'"):
        secsie.generate_config({"a": 1}, mode="toml")


def test_php_ini_round_trips():
    """
    Tests that a real world ini file can be read, written back out as ini, and read again without any change
    """
    original = secsie.parse_config_file("tests/data/php.ini", mode="ini")

    assert canonical(roundtrip(original)) == canonical(original)


def test_write_ini_config_file(tmp_path):
    """
    Tests that files are written in ini mode with an ini style comment on top, and can be read back
    """
    path = tmp_path / "out.ini"
    conf = {"section": {"key": "value", "number": "42"}}

    secsie.generate_config_file(conf, path, mode="ini")

    assert path.read_text() == '; out.ini auto-generated by secsie\n[section]\nkey = value\nnumber = "42"\n'
    assert secsie.parse_config_file(path, mode="ini") == conf


def test_failed_generation_does_not_touch_the_file(tmp_path):
    """
    Tests that a config which can't be written fails before the output file is created or changed
    """
    missing = tmp_path / "missing.ini"
    existing = tmp_path / "existing.ini"
    existing.write_text("keep me")

    for path in (missing, existing):
        with pytest.raises(ValueError):
            secsie.generate_config_file({"bad": "a = b"}, path, mode="ini")

    assert not missing.exists()
    assert existing.read_text() == "keep me"


def random_text(rng: random.Random) -> str:
    """
    Make a string out of the pieces that ini cares about, so the awkward combinations show up quickly
    """
    pieces = ["a", "b", "Z", "0", "7", ".", "-", " ", "  ", "\t", ",", "#", " #", "=", " = ", '"', "'", "[", "]", ";",
              "true", "no", "null", "yes", "\n", "\r", "é", "٣"]
    return "".join(rng.choice(pieces) for _ in range(rng.randint(0, 6)))


def random_scalar(rng: random.Random):
    kind = rng.randrange(6)
    if kind == 0:
        return random_text(rng)
    if kind == 1:
        return rng.choice([None, True, False])
    if kind == 2:
        return rng.randint(-10**6, 10**6)
    if kind == 3:
        return rng.choice([0.0, -0.0, 0.5, 1e-9, 1e20, 123456.789, rng.uniform(-1e6, 1e6), rng.uniform(-1e-5, 1e-5)])
    if kind == 4:
        return random_text(rng).strip() or "x"
    return [random_scalar(rng) for _ in range(rng.randint(0, 4))] if rng.random() < 0.5 else random_text(rng)


def random_key(rng: random.Random) -> str:
    return "".join(rng.choice("abcXYZ019_.-") for _ in range(rng.randint(1, 5)))


def random_config(rng: random.Random) -> dict:
    conf = {}
    for _ in range(rng.randint(0, 4)):
        if rng.random() < 0.5:
            conf[random_key(rng)] = random_scalar(rng)
        else:
            name = "".join(rng.choice("abc XY_-") for _ in range(rng.randint(1, 4)))
            conf[name] = {random_key(rng): random_scalar(rng) for _ in range(rng.randint(1, 4))}
    return conf


def test_writer_never_writes_something_that_reads_back_differently():
    """
    Throws thousands of awkward configs at the writer. Every one must either be refused with an error, or be read
    back as exactly the data that went in. Writing something that reads back differently is the one thing it must
    never do. (The seed is fixed so a failure is reproducible.)
    """
    rng = random.Random(20260414)
    written = 0

    for _ in range(5000):
        conf = random_config(rng)
        try:
            text = secsie.generate_config(conf, mode="ini")
        except (ValueError, TypeError):
            continue

        # A section with no keys has nothing to read back, but the generator above never makes one
        assert canonical(secsie.parse_config(text, mode="ini")) == canonical(conf), text
        written += 1

    # Make sure the test is really testing something, and not just being refused every time
    assert written > 1000
