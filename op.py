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

    def __init__(self, func, name=None):
        """Initialize self by setting _f equal to the argument."""
        self._f = func
        try:
            self.name = str(name)
        except:
            self.name = None

    def __mul__(self, other):
        """
        Attempt to compose or multiply depending on context.

        If other is an Op or a function, returns the appropriate 
        composition.  Otherwise, tries to pointwise multiply if 
        possible.
        """
        if isinstance(other, Op):
            return Op(compose(self._f, other._f))
        elif isinstance(other, FunctionType) or isinstance(other, LambdaType):
            return Op(compose(self._f, other))
        else:
            try: 
                return Op(lambda x: self._f(x) * other)
            except:
                return NotImplemented

    def __rmul__(self, other):
        """
        Attempt to compose or multiply depending on context.

        If other is an Op or a function, returns the appropriate 
        composition.  Otherwise, tries to pointwise multiply if 
        possible.
        """
        # the case isinstance(other, Op) will never happen, since in that 
        # case, other.__mul__() will be called instead
        if isinstance(other, FunctionType) or isinstance(other, LambdaType):
            return Op(compose(other, self._f))
        else:
            try: 
                return Op(lambda x: other * self._f(x))
            except:
                return NotImplemented

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
        else:
            try:
                return Op(lambda x: self._f(x) + other)
            except:
                return NotImplemented

    def __radd__(self, other):
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
        else:
            try:
                return Op(lambda x: self._f(x) + other)
            except:
                return NotImplemented

    def __sub__(self, other):
        """Return self - other."""
        return self + -1 * other

    def __rsub__(self, other):
        """Return other - self."""
        return other + -1 * self

    def __sub__(self, other):
        """Subtact two operators."""
        return self + other * -1

    def __call__(self, other):
        """Act on other with self._f."""
        return self._f(other)

    def __str__(self):
        """Print self.name"""
        return self.name

    def __repr__(self):
        """Print self.name"""
        return self.name    

identity = Op(lambda x: x, name='id')
"""Op object for the identity operator."""