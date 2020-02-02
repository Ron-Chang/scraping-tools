from functools import wraps
from datetime import timedelta

def snap_interval(**kwargs):
    def decorator(method):
        snap_interval = timedelta(**kwargs).seconds
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs, snap_interval=snap_interval)
        return wrapper
    return decorator
