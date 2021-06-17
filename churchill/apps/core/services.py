from typing import Tuple, List

import pytz


def get_timezone_list() -> List:
    return pytz.common_timezones


def get_timezone_choices() -> Tuple:
    return tuple(zip(pytz.common_timezones, pytz.common_timezones))
