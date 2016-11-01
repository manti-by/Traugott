from random import randrange
from datetime import datetime, timedelta


def random_date():
    start = datetime.strptime('9/9/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('10/10/2016 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)