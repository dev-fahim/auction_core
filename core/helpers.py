import time
from functools import wraps


def func_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # time.sleep(2)
        r = func(*args, **kwargs)
        return r
    return wrapper
