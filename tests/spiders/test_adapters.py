import pytest

from crawler.spiders.adapters import extract_status_from_capacity_bookings


@pytest.mark.parametrize("capacity_bookings,expected_status", [
    ("40", "available"),
    ("20 / 13", "available"),
    ("14 / 23", "waiting list"),
    ("0", "unavailable"),
    ("", "unavailable"),
    ("ERROR", "unavailable"),
    (None, "unavailable"),
])
def test_extract_status_from_capacity_bookings(capacity_bookings, expected_status):
    assert extract_status_from_capacity_bookings(capacity_bookings) == expected_status
