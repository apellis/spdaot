"""spdaot.frosting

Overview:
    This module defines some helpful global functions.  Several are to be
    used as decorators; others, for functional programming.

Functions:
    decorator(): Decorator for functions to be used as decorators themselves
    disabled(): Acts as the identity; assign this to another decorator to
        disable that decorator
    right_associative(): Decorator to make a binary operation into a right
        associative n-ary operation
    left_associative(): Decorator to make a binary operation into a left
        associative n-ary operation
    memo(): Decorator to make a recursive function autoatically cache its
        previous return values
    trace(): Decorator to have a recursive function automatically print
        its recursion trace
    compose(): Returns the composition of its arguments, each of which is
        a function.
"""

from functools import update_wrapper


def decorator(dec):
    """Decorator: update wrapper for decorated function automatically."""
    return lambda f: update_wrapper(dec(f), f)

# make decorator a decorator
decorator = decorator(decorator)


@decorator
def disabled(func):
    """Decorator: do nothing.  Use this to enable/disable other decorators."""
    return func


@decorator
def right_associative(func):
    """
    Decorator: convert a binary function to a right associative n-ary function.

    Example:
        right_associative(f)(x, y, z) is equivalent to f(x, f(y, z))
    """
    def ra_func(x, *args):
        return x if not args else func(x, ra_func(*args))
    return ra_func


@decorator
def left_associative(func):
    """
    Decorator: convert a binary function to a left associative n-ary function.

    Example:
        left_associative(f)(x, y, z) is equivalent to f(f(x, y), z)
    """
    def la_func(x, *args):
        return x if not args else func(la_func(x, *args[:-1]), args[-1])
    return la_func


@decorator
def memo(func):
    """Decorator: convert a recursive function to one that memoizes.

    Returns a function that, if all arguments are hashable, will remember its
    previous return values in a cache so as to avoid re-calculating these
    values.  If non-hashable arguments are found, no caching is done.
    """
    cache = {}

    def _func(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = func(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return func(args)
    return _func


@decorator
def trace(func):
    """Decorator: modify a function to also print its recursion trace."""
    indent = '   '

    def _func(*args):
        signature = '%s(%s)' % (func.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = func(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _func


@left_associative
def compose(func1, func2):
    """Compose the argument functions."""
    return lambda x: func1(func2(x))


@left_associative
def prod(x, y):
    """Return the product of x and y."""
    return x * y
