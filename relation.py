"""
spdaot.relation

Overview:
    The only types of relations currently supported are of the form
    x = \sum_i c_i y_i
    x and each y_i are of type VariableWord and each c_i is a numeric type.  
    Relations are stored in an ordered fashion, and they are applied accoridng 
    to this order.  The user is expected to load relations in the order (s)he 
    wants, and there is no check performed to make sure the 
    relation-application loop terminates.

    In particular, declaring both relations
    a * b = b * a
    and
    a * b = b * a
    will lead to an infinite loop whenever the sub-expression x * y is found.

Classes:
    Relation: class for representing relations among known variables
"""

from numbers import Number
from .variable import Variable, VariableWord
from . import config

class Relation:
    """
    TODO
    """

    def __init__(self, lhs, *rhs):
        """
        Initialize the relation and store it in config.relations.

        Arguments:
            lhs (VariableWord): the left-hand side
            rhs (list): the right-hand side.  Each element of the list is a 
                tuple (coeff, varword) with coeff of a numeric type and 
                varword of type VariableWord

        Example:
            Relation(x, (1, y), (-2, z)) adds the relation x = y - 2z, where 
            x, y, and z are all of type VariableWord (and therefore represent 
            monomials in known variables).
        """
        if isinstance(lhs, VariableWord):
            self.lhs = lhs
        elif isinstance(lhs, Variable):
            self.lhs = VariableWord(lhs)
        else:
            raise TypeError

        self.rhs = []
        for coeff, varword in rhs:
            if not isinstance(coeff, Number):
                raise TypeError
            if isinstance(varword, VariableWord):
                self.rhs.append((coeff, varword))
            elif isinstance(varword, Variable):
                self.rhs.append((coeff, VariableWord(varword)))
            else:
                raise TypeError

        self._register()

    def _register(self):
        """Register this relation in config.relations."""
        config.relations[self.lhs] = self

    def __str__(self):
        """Stringify self."""
        return str(self.lhs) + ' = ' + config.print_options['addsep'].join(str(x) for x in self.rhs)

    def __repr__(self):
        """Stringify self."""
        return repr(self.lhs) + ' = ' + config.print_options['addsep'].join(repr(x) for x in self.rhs)

