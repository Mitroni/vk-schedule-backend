import time
from functools import wraps

def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in cache and (now - cache[key]['timestamp']) < ttl_seconds:
                return cache[key]['value']
            result = func(*args, **kwargs)
            cache[key] = {'value': result, 'timestamp': now}
            return result
        return wrapper
    return decorator