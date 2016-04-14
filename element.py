"""spdaot.element

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

    Keyword arguments:
        commute: a number or a callable which returns a number when called
            with two arugments, each one of the elements of args.
        inverses (bool): if True, also creates inverses for each variable.
            'f' inverse will have the name 'fi'.  inverses are given
            commutation relations so as to match: if x2 x1 = c x1 x2, then
            x2i x1i = c x1i x2i

    When commute is a function, commute(v1, v2) is the scalar c such that
    v2 * v1 = c * v1 * v2, where v1 precedes v2 in args.  If commute is a
    callable and inverses = True, the commutation relation for inverses is
    inferred from that of the original variables; the argument to commute,
    does not have to know about inverses.

    Return value:
        a tuple of Elements representing 1*v for v in args, in order
    """
    variables = tuple(Variable(x) for x in args)
    inverse_variables = tuple(
        Variable(x, make_inverse=True) for x in args) \
        if kwargs['inverses'] is True else tuple()

    # make com a callable with two arguments
    if 'commute' not in kwargs:
        def com(x, y): return 1
    elif isinstance(kwargs['commute'], Number):
        def com(x, y): return kwargs['commute']
    else:
        com = kwargs['commute']

    # relations of the form x * xi = 1 take precedence
    if kwargs['inverses']:
        for i in xrange(len(args)):
            x = variables[i]
            xi = inverse_variables[i]
            config.relations[x*xi] = Relation(x*xi, (1, VariableWord()))
            config.relations[xi*x] = Relation(xi*x, (1, VariableWord()))

    # commutation relations
    for i in xrange(len(args)):
        for j in xrange(i+1, len(args)):
            x, y = variables[i], variables[j]
            config.relations[y*x] = Relation(y*x, (com(x, y), x*y))
            if kwargs['inverses']:
                xi, yi = inverse_variables[i], inverse_variables[j]
                config.relations[yi*xi] = Relation(yi*xi, (com(x, y), xi*yi))
                cinv = 1./com(x, y)
                cinv = int(cinv) if cinv.is_integer() else cinv
                config.relations[y*xi] = Relation(y*xi, (cinv, xi*y))
                config.relations[yi*x] = Relation(yi*x, (cinv, x*yi))

    return tuple(Element(v) for v in variables) + tuple(
        Element(v) for v in inverse_variables)


def add_central_variable(newvar):
    """Register a new central variable.

    The new variable is given name newvar, and relations are registered making
    this new variable commute with all known variables.  Variables added
    subsequently will not automatically commute with newvar

    Arguments:
        If newvar is a string, create a Variable object with that string as
        initializer.  If the argument is a Variable object, no new Variable
        object is created.

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
            Relation(VariableWord(varname, newvar),
                     (1, VariableWord(newvar, varname)))
    return Element(newvar)


class Element:
    """TODO"""

    def __init__(self, terms={}, coeff_initializer=int):
        """
        Initialize self to be an element with terms given by terms.

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

        if isinstance(terms, list) or isinstance(terms, tuple):
            terms = {x: 1 for x in terms}

        if isinstance(terms, dict) or isinstance(terms, defaultdict):
            for x in terms:
                if isinstance(x, VariableWord):
                    self.terms[x] = terms[x]
                elif isinstance(x, Variable) or isinstance(x, str):
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
        """Return the sum of self and other."""
        if isinstance(other, Element):
            return Element({vw: self[vw] + other[vw]
                           for vw in set(self.terms).union(other.terms)})
        elif isinstance(other, VariableWord) or isinstance(other, Variable):
            return self + Element(other)
        elif isinstance(other, Number):
            return self + Element(other)
        else:
            return NotImplemented

    def __radd__(self, other):
        """Return the sum of other and self."""
        # the case where other is an Element will never happen, because
        # in that case, other.__add__ is called instead
        if isinstance(other, VariableWord) or isinstance(other, Variable):
            return self + Element(other)
        elif isinstance(other, Number):
            return self + Element(other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """Return self - other."""
        return self + -1 * other

    def __rsub__(self, other):
        """Return other - self."""
        return other + -1 * self

    def __mul__(self, other):
        """Return the product of self and other."""
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
            return NotImplemented

    def __rmul__(self, other):
        """Return the product of other and self."""
        # the case whereother is an Element will never happen, since
        # other.__mul__ will be called instead
        if isinstance(other, VariableWord) or isinstance(other, Variable):
            return Element(other) * self
        elif isinstance(other, Number):
            return Element(other) * self
        else:
            return NotImplemented

    def __pow__(self, n):
        """Returns the n-fold product of self, n a positive integer."""
        if isinstance(n, int):
            if n > 0:
                return self * self**(n-1)
            elif n == 0:
                return Element(VariableWord())
            else:
                return NotImplemented
        else:
            return NotImplemented

    def __eq__(self, other):
        """Return True or False according to equality."""
        if isinstance(other, Element):
            rhs = other
        elif isinstance(other, VariableWord) or isinstance(other, Variable):
            rhs = Element(other)
        elif isinstance(other, Number):
            rhs = Element(other)
        else:
            return NotImplemented
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
            # be very generous: we'll allow this if index is an Element
            # of the form 1 * vw for some VariableWord vw
            index_vw = index.as_vw()
            if index_vw:
                return self[index_vw]
            else:
                return NotImplemented

    def __str__(self):
        """Stringifies self."""
        one = VariableWord()
        if len(self.terms.keys()) > 0:
            return config.print_options['addsep'].join(
                [str(self[key]) + config.print_options['mulsep'] +
                 (str(key) if key != one else '') for key in self.terms])
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

    def __iter__(self):
        """Iterate over VariableWord objects that are terms of self."""
        for vw in self.terms:
            yield vw

    def __neg__(self):
        """Return -1 * self."""
        return self * -1

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

    def transform(self, old, new, scale_func=lambda x: 1, swap=False):
        """Change all occurrences of variable old to scalar*new."""
        newterms = defaultdict(self._coeff_initializer)
        for key in self.terms:
            scale_factor = key.scale_by_factors(scale_func)
            newkey = key.copy()
            newkey.transform(old, new, swap=swap)
            newterms[newkey] = self.terms[key] * scale_factor
        self.terms = newterms
        self._simplify()

    def as_vw(self):
        """
        If self is 1*vw for some VariableWord, return a copy of that
        VariableWord.  Otherwise, return False.
        """
        nonzero_terms = [key for key in self.terms if self.terms[key] != 0]
        if len(nonzero_terms) != 1:
            return False
        elif self.terms[nonzero_terms[0]] != 1:
            return False
        else:
            return nonzero_terms[0]

    def copy(self):
        """Returns a copy of self."""
        from copy import deepcopy
        return Element(deepcopy(self.terms),
                       coeff_initializer=self._coeff_initializer)

    def _simplify(self):
        """Apply relations from config.relations to self while possible."""
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
                        changes[before_vw*varword*after_vw] += \
                            coeff * self.terms[term_vw]
                    made_simplification = True
                    break
                else:
                    continue

            # if we have changes make, then make them
            if made_simplification:
                self._add_terms(*list(changes.iteritems()))

            # remove any terms with zeroes
            self.terms = defaultdict(self._coeff_initializer,
                                     {key: val for key, val in
                                      self.terms.iteritems() if val != 0})
