"""
spdaot.variable

Overview:
    Defines the Variable class, which stands for a known variable.  To declare 
    a variable called 'x' with degree d (d may be of any type), call the 
    constructor Variable('x', d).

Classes:
    Variable: stands for a known variable
    VariableWord: stands for a word in known variables
"""

from copy import deepcopy
from . import config
from .exceptions import VariableNameCollision, UnknownVariableName

class Variable:
    """Class for named variables.  TODO: expand"""

    def __init__(self, name, deg=0, register=False):
        """
        Initialize name and degree.  If the variable is unknown, register it.  
        If register is set to True, force an attempt to register.  This can 
        raise an exception if the variable is already registered.

        Arguments:
            name (string): name of the new variable
            deg (any type): degree, if applicable
        """
        self.name = name        
        self.deg = deg
        try:
            self._register()
        except VariableNameCollision:
            if register:
                raise VariableNameCollision()
            else:
                pass

    def __eq__(self, other):
        """Return true or false according to whether the variables are equal"""
        if isinstance(other, Variable):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __str__(self):
        """Stringify self."""
        return self.name

    def __repr__(self):
        """Stringify self."""
        return self.name

    def __mul__(self, other):
        """Return a VariableWord representing the product of self and other."""
        if isinstance(other, Variable):
            return VariableWord(self, other)
        elif isinstance(other, VariableWord):
            return VariableWord(self, *(other._w))
        else:
            return TypeError

    def __hash__(self):
        """Return hash of self.name."""
        return hash(self.name)

    def __mul__(self, other):
        """Return the VariableWord concatenation of self and other."""
        if isinstance(other, Variable):
            return VariableWord(self, other)
        elif isinstance(other, str):
            return VariableWord(self, Variable(other))
        elif isinstance(other, VariableWord):
            # use VariableWord.__rmul__ instead
            return NotImplemented
        else:
            raise TypeError

    def _register(self):
        """
        Attempt to register this variable in config.variables.

        Returns:
            True if registration was successful
        """
        if self.name not in config.variables:
            config.variables[self.name] = self
            return True
        else:
            raise VariableNameCollision()
        return False

    def element(self):
        """Return an Element equal to this variable."""
        pass # TODO

    def transform(self, old, new, swap=False):
        """
        Change self.name to new if self.name equals old.

        Return value:
            True if change was made, False otherwse
        """
        if isinstance(old, Variable):
            old = old.name
        if isinstance(new, Variable):
            new = new.name
        if self.name == old:
            self.name = new
            return True
        elif self.name == new and swap:
            self.name = old
            return True
        else:
            return False

class VariableWord:
    """Class for a word in known variables.  TODO: expand"""

    def __init__(self, *word):
        """
        Initialize variable word.

        Arguments:
            vars (list): each element of type Variable or string
        """
        self._w = []
        for var in word:
            if isinstance(var, str):
                varname = var
            elif isinstance(var, Variable):
                varname = var.name
            elif isinstance(var, VariableWord):
                # be generous: it it's a single variable, then cast
                if len(var) == 1:
                    return var[0]
                else:
                    raise TypeError
            else:
                raise TypeError

            if varname in config.variables:
                self._w.append(varname)
            else:
                raise UnknownVariableName

    def __getitem__(self, index):
        """Returns index-th variable name in the word."""
        return self._w[index]

    def __mul__(self, other):
        """Concatenate self and other."""
        if isinstance(other, VariableWord):
            return VariableWord(*(self._w + other._w))
        elif isinstance(other, Variable):
            return VariableWord(*(self._w + [other.name]))
        else:
            raise TypeError

    def __rmul__(self, other):
        """Concatenate other and self."""
        if isinstance(other, VariableWord):
            return VariableWord(*(other._w + self._w))
        elif isinstance(other, Variable):
            return VariableWord(*([other.name] + self._w))
        else:
            raise TypeError

    def __eq__(self, other):
        """Return True or False according to equality or not."""
        return self._w == other._w

    def __ne__(self, other):
        """Return False or True according to equality or not."""
        return self._w != other._w

    def __str__(self):
        """Stringify self in monomial style."""
        if len(self._w) > 0:
            return config.print_options['mulsep'].join(self._w)
        else:
            return "1"
        # TODO: support for exponents

    def __repr__(self):
        """Stringify self in list style."""
        return str(self)

    def __hash__(self):
        """Return hash of self._tuplify()."""
        return hash(self._tuplify())

    def __len__(self):
        """Return the number of factors."""
        return len(self._w)

    def _tuplify(self):
        """Return a tuple of strings representing the word."""
        return tuple(v for v in self._w)

    def transform(self, old, new, swap=False):
        """
        For each Variabble factor, change its name to new if it was 
        previously equal to old.

        Arguments:
            old, new (str or Variable)

        Return value:
            if swap:
                n1, n2 = number of changes made in the forward and reverse directions
            if not swap:
                n = number of changes made
        """
        count = 0
        count_rev = 0
        if isinstance(old, Variable):
            old = old.name
        if isinstance(new, Variable):
            new = new.name
        for i in xrange(len(self._w)):
            if self._w[i] == old:
                self._w[i] = new
                count += 1
            elif self._w[i] == new and swap:
                self._w[i] = old
                count_rev += 1
            else:
                continue
        if swap:
            return count, count_rev
        else:
            return count

    def copy(self):
        """Return a copy of self."""
        from copy import deepcopy
        return VariableWord(*deepcopy(self._w))

    def split_on_sub(self, *subword):
        """
        Searches for subword in self.  Returns a tuple consisting of the 
        word before, the subword, and the word after if successful.  If not, 
        returns None, None, None.  If subword is empty, matches on the intiial 
        empty subword.

        Arguments:
            subword is an iterable of Variable objects
        """
        if len(subword) == 0:
            return [], [], self._w
        else:
            for i in xrange(len(self._w) - len(subword) + 1):
                if subword[0] == self._w[i] and list(subword) == self._w[i:i+len(subword)]:
                    return self._w[:i], self._w[i:i+len(subword)], self._w[i+len(subword):]
        return None, None, None

