import pytest
from todo_app.todo.models import Location
from todo_app.todo.utils import get_location_from_string, str_to_float


@pytest.mark.parametrize(
    "value, expected_result",
    (
        ("1.0::2.0::sample, label", Location(lat=1.0, lon=2.0, label="sample, label")),
        ("0::-1::sample", Location(lat=0.0, lon=-1.0, label="sample")),
    ),
)
def test_get_location_from_string(value, expected_result):
    """
    Given a correct location definition
    When we create a location using function get_location_from_string
    Then a correct location object is created.
    """
    assert get_location_from_string(value) == expected_result


@pytest.mark.parametrize("value", ("1", "1::2", "a::b", "1::b::c", {}, [], set()))
def test_get_location_from_string_with_incorrect_data(value):
    """
    Given an incorrect location definition
    When we create a location using function get_location_from_string
    Then None is returned as the result.
    """
    assert get_location_from_string(value) is None


@pytest.mark.parametrize(
    "value, expected_result",
    (
        ("1", 1.0),
        ("1.2", 1.2),
        ("0.0000", 0.0),
        ("-123.456", -123.456),
    ),
)
def test_str_to_float(value, expected_result):
    """
    Given a string with a correct float number
    When we convert it to float using function str_to_float
    Then we get a correct float number as the result.
    """
    assert str_to_float(value) == expected_result


@pytest.mark.parametrize("value", ("a", {}, [], set()))
def test_str_to_float_with_incorrect_data(value):
    """
    Given a string with an incorrect float number
    When we convert it to float using function str_to_float
    Then None is returned as the result.
    """
    assert str_to_float(value) is None
