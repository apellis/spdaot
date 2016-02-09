"""
TODO
"""

from collections import defaultdict
from numbers import Number
from .op import Op
from .variable import Variable, VariableWord
from .element import Element

def minus_s(x, i, j=None, sign=1, varletter='x'):
    """Simple generator of -D_n"""
    if j is None:
        j = i + 1
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(j), scalar=sign*-1, swap=True, no_swap_scalar=-1)
    return y

def sig(x, i, j=None, sign=1, varletter='x'):
    """Simple generator of B_n^+"""
    if j is None:
        j = i + 1
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(j), scalar=sign, swap=True, revscalar=sign*-1)
    return y

def minus_Dn_generators(n, varletter='x'):
    """
    Return functions for the simple generators of -D_n in the order
    -s_1^+, ..., -s_{n-1}^+, -s_1^-, ... -s_{n-1}^-

    Argument:
        n, a positive integer
    Return value:
        A tuple of 2(n-1) functions
    """
    def generator_factory(i, s):
        if s == 1:
            return lambda f: minus_s(f, i, sign=1, varletter=varletter)
        elif s == -1:
            return lambda f: minus_s(f, i, sign=-1, varletter=varletter)
    return tuple(Op(generator_factory(i, 1)) for i in xrange(1, n)) + tuple(Op(generator_factory(i, -1)) for i in xrange(1, n))

def Bn_plus_generators(n, varletter='x'):
    """
    Return functions for the simple generators of B_n^+ in the order
    \sigma_1^+, ..., \sigma_{n-1}^+, \sigma_1^-, ..., \sigma_{n-1}^-

    Argument:
        n, a positive integer
    Return value:
        A tuple of 2(n-1) functions
    """
    def generator_factory(i, s):
        if s == 1:
            return lambda f: sig(f, i, sign=1, varletter=varletter)
        elif s == -1:
            return lambda f: sig(f, i, sign=-1, varletter=varletter)
    return tuple(
        Op(generator_factory(i, 1)) for i in xrange(1, n)) + tuple(
        Op(generator_factory(i, -1)) for i in xrange(1, n))

def _braided_differential_variable(var, x_values):
    """Compute a braided differential on a single Variable, return result."""
    if isinstance(var, VariableWord):
        if len(var) == 0:
            return 0
        elif len(var) == 1:
            var = Variable(var[0])
        else:
            raise TypeError
    elif isinstance(var, Variable):
        if var in x_values:
            return x_values[var]
        elif var.name in x_values:
            return x_values[var.name]
        else:
            return 0
    elif isinstance(var, str):
        if var in x_values:
            return x_values[var]
        elif Variable(var) in x_values:
            return x_values[Variable(var)]
        else:
            return 0
    else:
        raise TypeError

def _braided_differential_vw(vw, x_values, braiding):
    """Compute a braided differential on a VariableWord, return result."""
    if not isinstance(vw, VariableWord):
        raise TypeError
    ret_terms = []
    for i in xrange(len(vw)):
        left = braiding(Element(VariableWord(*vw[:i]))) if i > 0 else Element(1)
        middle = x_values[vw[i]]
        right = Element(VariableWord(*vw[i+1:])) if i < len(vw) - 1 else Element(1)
        ret_terms.append(left * middle * right)
    return sum(ret_terms)

def braided_differential(elt, x_values, braiding):
    """
    Compute the braided differential d defined by the rule
    d(xy) = d(x) y + w(x) y
    for some group element w acting on an algebra containing x, y.  Return 
    the value d(elt).

    Arguments:
        elt (Element): the element on which we are evaluating the differential
        x_values (dict): for a Variable or string s, x_values[s] is 
            the value of d on the corresponding variable.  all values of 
            x_values should be of type Number.  If x_values is a defaultdict, 
            its default value should be 0.
        braiding (callable): braiding(x) should be the Element representing d(x)

    Return value:
        an Element representing d(elt)
    """
    if isinstance(x_values, dict):
        x_values = defaultdict(int, x_values)
    if isinstance(elt, Variable) or isinstance(elt, VariableWord):
        return _braided_differential_variable(elt, x_values)
    elif isinstance(elt, str):
        return _braided_differential_variable(Variable(var), x_values)
    elif isinstance(elt, Element):
        return sum(
            _braided_differential_vw(
                vw, x_values, braiding) * elt.terms[vw] for vw in elt.terms)
    else:
        raise TypeError

def minus_Dn_braided_differentials(n, varletter='x'):
    """
    Return Op objects for each braided differential for -D_n acting 
    on S_{-1}(V) in the order d_1^+, ..., d_1^-, ...
    """
    def differential_factory(i, s):
        x_values = defaultdict(int, {varletter+str(i): 1,
            varletter+str(i+1): s})
        braiding = lambda x: minus_s(x, i, sign=s, varletter=varletter)
        return lambda x: braided_differential(x, x_values, braiding)
    return tuple(
        Op(differential_factory(i, 1)) for i in xrange(1, n)) + tuple(
        Op(differential_factory(i, -1)) for i in xrange(1, n))

