from gspread.exceptions import APIError

def conditional_function(condition=True):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            if condition:
                return func(*args, **kwargs)
        return wrapper
    return decorator_func

def exception_wrapper(exc_func,exc=Exception):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc as e:
                exc_func(e)
        return wrapper
    return decorator_func

def connection_retry(error=(ConnectionError,ConnectionResetError,ConnectionAbortedError,ConnectionResetError,APIError)):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except error:
                    print(end=".")
        return wrapper
    return decorator_func

def class_exception_wrapper(exc=Exception):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc as e:
                args[0].exception_handler(e)
        return wrapper
    return decorator_func