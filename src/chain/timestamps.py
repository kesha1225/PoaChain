import time


def get_current_accurate_timestamp() -> int:
    return int(time.time() * 1000000)
