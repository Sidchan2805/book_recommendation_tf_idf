import functools
import logging
import time

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Function {func.__name__} called with args={args} kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f"{func.__name__} executed in {end - start:.2f}s")
        return result
    return wrapper

def simple_cache(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(title, top_n=5):
        if (title, top_n) in cache:
            logging.info(f"Cache hit for: {title}")
            return cache[(title, top_n)]
        result = func(title, top_n)
        cache[(title, top_n)] = result
        return result
    return wrapper
