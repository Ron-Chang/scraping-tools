from functools import wraps
from datetime import timedelta

class CommonUtils:
    def snap_interval(**kwargs):
        def decorator(method):
            seconds = timedelta(**kwargs).total_seconds()
            if isinstance(seconds, float) or isinstance(seconds, int):
                snap_interval = seconds
            else:
                snap_interval = 60 * 60 * 24 * 7
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs, snap_interval=snap_interval)
            return wrapper
        return decorator
