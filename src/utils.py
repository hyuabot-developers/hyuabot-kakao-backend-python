import datetime


def calculate_remaining_minutes(departure_time: datetime.time, current_time: datetime.time) -> int:
    remaining_time = datetime.datetime.combine(datetime.date.today(), departure_time) - datetime.datetime.combine(
        datetime.date.today(), current_time,
    )
    return remaining_time.seconds // 60 if remaining_time.seconds > 0 else 0
