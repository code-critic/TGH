import timeit
import functools
import numpy as np


def timefunc(number=10000):
    def _timefunc(func):
        @functools.wraps(func)
        def time_func_wrapper(*args, **kwargs):
            t0 = timeit.default_timer()
            for _ in range(number):
                value = func(*args, **kwargs)
            t1 = timeit.default_timer()
            print("func: {}(args={}, kwargs={}) time: {}".format(func.__name__, str(args), str(kwargs), t1-t0))
            return value
        return time_func_wrapper
    return _timefunc

volumes= [6, 7, 8]
@timefunc(number=100000)
def modify_np(x, i, j):
    y = x.copy()
    free = volumes[j] - x[j]
    spill = min(free, x[i])
    y[i] -= spill
    y[j] += spill
    #y = x
    h = hash(y.tostring())
    return h

x = np.array([1,2,3])
modify_np(x, 1, 2)



@timefunc(number=100000)
def modify_np(x, i, j):
    y = x.copy()
    free = volumes[j] - x[j]
    spill = min(free, x[i])
    y[i] -= spill
    y[j] += spill
    hash(tuple(y))

x = [1,2,3]
modify_np(x, 1, 2)