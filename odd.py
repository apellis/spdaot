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
    def scale_func(s):
        if s == varletter + str(i) or s == varletter + str(j):
            return -1 * sign
        elif s[0] == varletter and s[1:].isdigit():
            return -1
        else:
            return 1
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(j), scale_func=scale_func, swap=True)
    return y

def sig(x, i, j=None, sign=1, varletter='x'):
    """Simple generator of B_n^+"""
    if j is None:
        j = i + 1
    def scale_func(s):
        if s == varletter + str(i):
            return sign
        elif s == varletter + str(j):
            return -1 * sign
        else:
            return 1
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(j), scale_func=scale_func, swap=True)
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
    return tuple(Op(generator_factory(i, 1), name='-s_'+str(i)+'^+') for i in xrange(1, n)) + tuple(Op(generator_factory(i, -1), name='-s_'+str(i)+'^-') for i in xrange(1, n))

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
        Op(generator_factory(i, 1), name='sigma_'+str(i)+'^+') for i in xrange(1, n)) + tuple(
        Op(generator_factory(i, -1), name='sigma_'+str(i)+'^-') for i in xrange(1, n))

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
    elif isinstance(elt, Number):
        return 0
    elif isinstance(elt, Element):
        return sum(
            _braided_differential_vw(
                vw, x_values, braiding) * elt.terms[vw] for vw in elt.terms)
    else:
        raise TypeError

def minus_Dn_braided_differentials(n, varletter='x', isobaric=False):
    """
    Return Op objects for each braided differential for -D_n acting 
    on S_{-1}(V) in the order d_1^+, ..., d_1^-, ...

    If isobaric = True, returns \pm x_i * d_i^\pm in place of d_i^\pm.
    """
    if isobaric:
        # i = 0 case is never used, but it makes the formula below look better
        pre_x = [Element(Variable(varletter + str(i+1))) for i in xrange(n)]

    def differential_factory(i, s):
        x_values = defaultdict(int, {varletter+str(i): 1,
            varletter+str(i+1): s})
        braiding = lambda x: minus_s(x, i, sign=s, varletter=varletter)
        if isobaric:
            return lambda x: pre_x[i] * braided_differential(x, x_values, braiding) * s
        else:
            return lambda x: braided_differential(x, x_values, braiding)

    dee = 'D' if isobaric else 'd'

    return tuple(
            Op(differential_factory(i, 1), name=dee+'_'+str(i)+'^+') for i in xrange(1, n)) + tuple(
            Op(differential_factory(i, -1), name=dee+'_'+str(i)+'^-') for i in xrange(1, n))

def minus_Dn_hecke_generators(n, varletter='x', qletter='q'):
    """
    Return Op objects for generators of the Hecke deformation of the isobaric 
    braided differentials for -D_n.
    """
    isobarics = minus_Dn_braided_differentials(
        n, varletter=varletter, isobaric=True)
    sigmas = Bn_plus_generators(n, varletter=varletter)

    ret = []
    for i in xrange(1, n):
        ret.append((Element(1)-Element(qletter))*isobarics[i-1]+sigmas[n-1+i-1])
    for i in xrange(1, n):
        ret.append((Element(1)-Element(qletter))*isobarics[n-1+i-1]+sigmas[i-1])

    return ret