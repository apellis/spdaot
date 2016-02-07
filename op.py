"""
spdaot.op

Overview:
    TODO

Classes:
    Op: wrapper class for functions considered as elements of an algebra or 
        group equipped with an action
"""

from frosting import compose
from numbers import Number
from types import FunctionType, LambdaType

class Op:
    """
    TODO: docstring
    """

    def __init__(self, func):
        """Initialize self by setting _f equal to the argument."""
        self._f = func

    def __mul__(self, other):
        """
        Attempt to compose or multiply depending on context.

        If other is an Op or a function, returns the appropriate 
        composition.  If other is a Number, interprets other as an 
        element of the ground ring and performs pointwise multiplication.
        """
        if isinstance(other, Op):
            return Op(compose(self._f, other._f))
        elif isinstance(other, FunctionType) or isinstance(other, LambdaType):
            return Op(compose(self._f, other))
        elif isinstance(other, Number):
            return Op(lambda x: self._f(x) * other)
        else:
            raise TypeError

    def __add__(self, other):
        """
        Attempt to add two operators.

        If other is an Op or a function, returns the appropriate 
        pointwise sum.  If other is a Number, interprets other as a constant 
        function and does the same.
        """
        if isinstance(other, Op):
            return Op(lambda x: self._f(x) + other._f(x))
        elif isinstance(other, FunctionType) or isinstance(other, LambdaType):
            return Op(lambda x: self._f(x) + other(x))
        elif isinstance(other, Number):
            return Op(lambda x: self._f(x) + other)
        else:
            return TypeError

    def __sub__(self, other):
        """Subtact two operators."""
        return self + other * -1

    def __call__(self, other):
        """Act on other with self._f."""
        return self._f(other)

