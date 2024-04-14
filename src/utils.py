import datetime


def calculate_remaining_minutes(departure_time: datetime.time, current_time: datetime.time) -> int:
    remaining_time = datetime.datetime.combine(datetime.date.today(), departure_time) - datetime.datetime.combine(
        datetime.date.today(), current_time,
    )
    if remaining_time.total_seconds() <= 0:
        return 0
    return int(remaining_time.total_seconds() / 60)
