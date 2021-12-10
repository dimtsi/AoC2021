import time
from aocd import submit
from datetime import datetime


def timing_val(func):
    def wrapper(*arg, **kw):
        """source: http://www.daniweb.com/code/snippet368.html"""
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return (t2 - t1), res, func.__name__

    return wrapper


def submit_answer(answer, part="a"):
    today = datetime.today()
    day, year = today.day, today.year
    submit(answer=answer, day=day, year=year)
