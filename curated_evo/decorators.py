from gspread.exceptions import APIError
from time import sleep

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

def connection_retry(error=(ConnectionError,ConnectionResetError,ConnectionAbortedError,ConnectionResetError,APIError),wait_time=90):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except error as e:
                    print(f"Error: {e}")
                    for x in range(0,wait_time):
                        sleep(1)
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

def selenium_spider_exception(exc=Exception):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc as e:
                args[0].exception_handler(e,args[1].request.meta['driver'])
        return wrapper
    return decorator_func