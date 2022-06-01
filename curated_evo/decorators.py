from gspread.exceptions import APIError
from time import sleep

class Decorators:

    @staticmethod
    def conditional_function(condition=True):
        def decorator_func(func):
            def wrapper(*args, **kwargs):
                if condition:
                    return func(*args, **kwargs)
            return wrapper
        return decorator_func

    @staticmethod
    def exception_wrapper(exc_func,exc=Exception):
        def decorator_func(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exc as e:
                    exc_func(e)
            return wrapper
        return decorator_func

    @staticmethod
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

    @staticmethod
    def class_exception_wrapper(exc=Exception):
        def decorator_func(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exc as e:
                    args[0].exception_handler(e)
            return wrapper
        return decorator_func

    @staticmethod
    def selenium_spider_exception(exc=Exception):
        def decorator_gen(gen):
            def wrapper(*args, **kwargs):
                try:
                    return (yield from gen(*args, **kwargs))
                except exc as e:
                    args[0].exception_handler(e,args[1])
            return wrapper
        return decorator_gen

decorate = Decorators()