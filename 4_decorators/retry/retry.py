# реализуйте декоратор вида @retry(count: int, delay: timedelta, handled_exceptions: tuple[type(Exceptions)])
import time
from datetime import timedelta
from functools import wraps

def retry(count, delay, handled_exceptions=None):
    if count < 1:
        raise ValueError("Count должен быть больше или равен 1")

    if handled_exceptions is None:
        handled_exceptions = (Exception,)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < count:
                try:
                    return func(*args, **kwargs)
                except handled_exceptions as e:
                    attempts += 1
                    if attempts >= count:
                        raise e
                    time.sleep(delay.total_seconds())
        return wrapper
    return decorator
