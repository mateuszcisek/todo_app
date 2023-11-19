from cybersmart_assessment.todo.models import Location


def str_to_float(value: str) -> float | None:
    """Convert the given value to a float and return it.

    If it's not possible then None is returned.

    Args:
        value (str): Value to convert.

    Returns:
        float | None: Converted value of None.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_location_from_string(value: str) -> Location | None:
    """Create a Location object from a given location definition.

    The location is considered valid if it consists of three parts that are separated
    by double colon (::):

        latitude::longitude::label

    Latitude and longitude must be valid float numbers, and the label is a string.

    For example, this is a valid string:

        45.12::1.23::Sample location

    And those are examples of invalid strings:

        a
        1::a
        1::a::3

    Returns:
        Location | None: Location object or None.
    """
    try:
        lat, lon, label = value.split("::")
    except (AttributeError, ValueError):
        return None

    lat = str_to_float(lat)
    lon = str_to_float(lon)

    if lat is None or lon is None:
        return None

    return Location(lat=lat, lon=lon, label=label)
