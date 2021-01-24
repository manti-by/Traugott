from collections.abc import Iterable
from datetime import datetime, timedelta


def date_range(start_date: datetime, end_date: datetime) -> Iterable[datetime]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
