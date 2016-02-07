"""
spdaot.element

Overview:
    TODO

Classes:
    Element: TODO
"""

from collections import defaultdict
from numbers import Number
from itertools import product
from .variable import Variable, VariableWord
from .relation import Relation
from . import config

def make_poly_family(*args, **kwargs):
    """
    Creates a family of q-commuting variables, one for each non-keyword 
    argument.  By default, q = 1 for all pairs of variables.

    Arguments:
        args: a list of strings or Variable objects
        commute: a number or a callable which returns a number when called 
            with two arugments, each one of the elements of args

    When commute is a function, commute(v1, v2) is the scalar c such that
    v2 * v1 = c * v1 * v2, where v1 precedes v2 in args.

    Return value:
        a tuple of Elements representing 1*v for v in args, in order
    """
    variables = tuple(Variable(x) for x in args)
    if 'commute' not in kwargs:
        com = lambda x, y: 1
    elif isinstance(kwargs['commute'], Number):
        com = lambda x, y: kwargs['commute']
    else:
        com = kwargs['commute']
    for i in xrange(len(args)):
        for j in xrange(i+1, len(args)):
            x, y = variables[i], variables[j]
            config.relations[y*x] = Relation(y*x, (com(x, y), x*y))
    return tuple(Element(v) for v in variables)

def add_central_variable(newvar):
    """
    Return a Element representing 1*newvar and add relations making newvar 
    commute with all known variables.  If the argument is a string, it 
    creates a Variable object with that string as initializer.  If the 
    argument is a Variable object, no new Variable object is created.

    Return value:
        an Element representing 1*newvar
    """
    if isinstance(newvar, str):
        newvar = Variable(newvar)
    elif isinstance(newvar, Variable):
        pass
    else:
        raise TypeError
    for varname in config.variables:
        if newvar.name != varname:
            Relation(VariableWord(varname, newvar), (1, VariableWord(newvar, varname)))
    return Element(newvar)

class Element:
    """
    TODO
    """

    def __init__(self, terms={}, coeff_initializer=int):
        """
        Initializes self to be an element with terms given by terms.

        Arguments:
            terms (dict): keys are of type VariableWord, values of any numeric 
                type; terms[vw] is the coefficient of vw in the element
            coeff_initializer: a function of no arguments which returns 
                the default value for a new term; default is int

        If terms is an object of type VariableWord or Variable, the arument is 
        interpreted as having coefficient 1 (integer).  A number is interpreted 
        as the coefficient of an empty product.
        """
        self.terms = defaultdict(coeff_initializer)
        self._coeff_initializer = coeff_initializer
        if isinstance(terms, dict) or isinstance(terms, defaultdict):
            for x in terms:
                if isinstance(x, VariableWord):
                    self.terms[x] = terms[x]
                elif isinstance(x, Variable):
                    self.terms[VariableWord(x)] = terms[x]
                else:
                    raise TypeError
        elif isinstance(terms, VariableWord):
            self.__init__({terms: 1})
        elif isinstance(terms, Variable) or isinstance(terms, str):
            self.__init__({VariableWord(terms): 1})
        elif isinstance(terms, Number):
            self.__init__({VariableWord(): terms})
        else:
            raise TypeError

        # __init__ is often called as part of a call to __add__ or 
        # to __mul__, so we should simplify here
        self._simplify()

    def __add__(self, other):
        """Returns the sum of two elements."""
        if isinstance(other, Element):
            return Element({vw: self[vw] + other[vw] 
                for vw in set(self.terms).union(other.terms)})
        elif isinstance(other, VariableWord) or isinstance(other, Variable):
            return self + Element(other)
        elif isinstance(other, Number):
            return self + Element(other)
        else:
            return TypeError

    def __sub__(self, other):
        """Returns the difference of two elements."""
        return self + other * -1

    def __mul__(self, other):
        """Returns the product of two elements."""
        if isinstance(other, Element):
            ret = Element()
            for vw1, vw2 in product(self.terms, other.terms):
                ret.terms[vw1 * vw2] += self[vw1] * other[vw2]
            ret._simplify()
            return ret
        elif isinstance(other, VariableWord) or isinstance(other, Variable):
            return self * Element(other)
        elif isinstance(other, Number):
            return self * Element(other)
        else:
            raise TypeError

    def __eq__(self, other):
        """Returns True or False according to equality."""
        if isinstance(other, Element):
            rhs = other
        elif isinstance(other, VariableWord) or isinstance(other, Variable):
            rhs = Element(other)
        elif isinstance(other, Number):
            rhs = Element(other)
        else:
            raise TypeError
        words = set(self.terms).union(rhs.terms)
        return all(self[x] == rhs[x] for x in words)

    def __getitem__(self, index):
        """Returns the coefficient of index in self, is possible."""
        if isinstance(index, VariableWord):
            return self.terms[index]
        elif isinstance(index, Variable):
            return self[VariableWord(index)]
        elif index == 1:
            return self[VariableWord()]
        elif isinstance(index, Element):
            # being very generous, we'll allow this if index is an Element 
            # of the form 1 * vw for some VariableWord vw
            vw = None
            for key, val in index.terms.iteritems():
                if val not in [0, 1]:
                    raise TypeError
                elif val == 1:
                    if vw is not None:
                        raise TypeError
                    else:
                        vw = key
            return self[vw]

    def __str__(self):
        """Stringifies self."""
        one = VariableWord()
        if len(self.terms.keys()) > 0:
            return config.print_options['addsep'].join(
                [str(self[key]) + (str(key) if key != one else '') 
                    for key in self.terms])
        else:
            return '0'

    def __repr__(self):
        """Stringifies self."""
        one = VariableWord()
        if len(self.terms.keys()) > 0:
            return config.print_options['addsep'].join(
                [repr(self[key]) + (repr(key) if key != one else'')
                    for key in self.terms])
        else:
            return '0'

    def _add_terms(self, *args):
        """
        Adds a list of terms to self.

        Arguments:
            All of the form (coeff, varword), where coeff is a Number and 
            varword is a VariableWord.

        Adds coeff*varword to self for each such pair.  No return value.
        """
        for varword, coeff in args:
            if not isinstance(coeff, Number):
                raise TypeError
            if isinstance(varword, VariableWord):
                self.terms[varword] += coeff
            elif isinstance(varword, Variable):
                self.terms[VariableWord(varword)] += coeff
            else:
                raise TypeError

    def transform(self, old, new, scalar=1, swap=False, revscalar=None):
        """Change all occurrences of variable old to scalar*new."""
        if swap and revscalar is None:
            revscalar = scalar
        newterms = defaultdict(self._coeff_initializer)
        for key in self.terms:
            newkey = key.copy()
            if swap:
                ex1, ex2 = newkey.transform(old, new, swap=swap)
                newterms[newkey] = self.terms[key] * scalar**ex1 * revscalar**ex2
            else:
                ex = newkey.transform(old, new, swap=swap)
                newterms[newkey] = self.terms[key] * scalar**ex
        self.terms = newterms
        self._simplify()

    def copy(self):
        """Returns a copy of self."""
        from copy import deepcopy
        return Element(deepcopy(self.terms), coeff_initializer=self._coeff_initializer)

    def _simplify(self):
        """TODO"""
        made_simplification = True
        while made_simplification:
            made_simplification = False

            # try and apply a relation
            for term_vw, rel_vw in product(self.terms, config.relations):
                before, during, after = term_vw.split_on_sub(*rel_vw._w)
                if during:
                    # we found rel_vw inside term_vw, so let's record
                    # the changes we want to make
                    # we don't make them here so as to avoid changing the 
                    # dict self.terms during iteration
                    changes = defaultdict(self._coeff_initializer)
                    before_vw = VariableWord(*before)
                    after_vw = VariableWord(*after)
                    changes[before_vw*rel_vw*after_vw] -= self.terms[term_vw]
                    for coeff, varword in config.relations[rel_vw].rhs:
                        changes[before_vw*varword*after_vw] += coeff * self.terms[term_vw]
                    made_simplification = True
                    break
                else:
                    continue

            # if we have changes make, then make them
            if made_simplification:
                self._add_terms(*list(changes.iteritems()))

            # remove any terms with zeroes
            self.terms = defaultdict(self._coeff_initializer, 
                {key: val for key, val in self.terms.iteritems() if val != 0})


