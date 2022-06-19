import time
from functools import wraps


def func_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        # time.sleep(2)
        r = func(*args, **kwargs)
        print("Process took", "%.2f" % (time.time() - start), 'seconds')
        return r
    return wrapper
