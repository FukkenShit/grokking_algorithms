def print_results(func):
    """Decorator printing args, kwargs and return value of a function before returning actual result."""
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        print(*[obj for obj in (args, kwargs, result) if obj])
        return result
    return wrapped

