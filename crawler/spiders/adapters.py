def extract_status_from_capacity_bookings(capacity_bookings):
    """Extract status from Capacity / Bookings.

    This field can have different formats, like only capacity
    or capacity/bookings. The bookings can also be greater
    than the capacity when a waiting list is available."""
    availability = "unavailable"
    if not capacity_bookings:
        return availability

    capacity_bookings_list = capacity_bookings.split("/")
    if len(capacity_bookings_list) == 1:
        # format: 0 or 40
        try:
            capacity = int(capacity_bookings)
            if capacity > 0:
                availability = "available"
        except ValueError:
            availability = "unavailable"
    elif len(capacity_bookings_list) > 1:
        # format: 16 / 24
        capacity = capacity_bookings_list[0]
        bookings = capacity_bookings_list[1]
        if int(bookings) >= int(capacity):
            availability = "waiting list"
        else:
            availability = "available"
    return availability
