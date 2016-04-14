"""
spdaot.tools

Overview:
    Useful tools, mostly for working with objects of classes Element and Op.

Functions:
    div_geometric(): TODO
    relation_finder(): TODO
"""

from math import ceil
from . import Element, Op


def finite_set_exponential(base, exponent):
    """
    Find all functions between two finite sets and yield them (generator).

    Arguments:
        base, exponent (list or tuple): both with finitely many elements

    Assumptions:
        1. each element of base is hashable
        2. the elements of base are pairwise distinct
        3. the elements of exponent are pairwise distinct

    Return value:
        Yields dicts.  Each dict d represents the function which sends x to
        d[x].  Functions are from exponent to base.
    """
    if len(base) == 0:
        # there are no functions to an empty set
        raise ValueError
    elif len(exponent) == 0:
        # there is exactly one function from an empty set
        yield {}
    else:
        for val in base:
            # find all functions which sense exponent[0] to val
            for func in finite_set_exponential(base, exponent[1:]):
                func[exponent[0]] = val
                yield func


def div_geometric(func1, func2, degree):
    """
    Compute a quotient func1 / (1 - func2), where func1 and func2 commute with
    each other, under certain hypotheses.

    Arguments:
        func1, func2 (class Element): the elements such that our goal is to
            compute func1 / (1 - func2)
        degree (function): degree must accept a single argument of class
            VariableWord and return a Number type.  See assumptions below on
            which choices of degree are appropriate.

    Assumptions:
        1. degree is a grading function making objects of class VariableWord
            into a graded monoid.  Explicitly, this means:
                degree(vw1 * vw2) = degree(vw1) + degree(vw2)
            for any VariableWord objects vw1 and vw2.
        2. func2 is central: that is, func2 * g = g * func2 for any Element g.
        3. degree(vw) > 0 for every VariableWord vw with a nonzero coefficient
            in func2.

    Return value:
        an object ret of class Element such that func1 = (1 - func2) * ret
    """
    # find min_deg and max_deg, the min/max term degrees in func1
    #   hence the highest degree term in ret will have degree max_deg, the
    #   lowest
    func1_degrees = [degree(vw) for vw in func1]
    min_deg = min(func1_degrees)
    max_deg = max(func1_degrees)

    # find the smallest positive integer max_exponent such that
    #   max_deg <= min_deg + degree(func2) * max_exponent .
    #   no term func1 * func2 ** e contributes with e > max_exponent
    max_exponent = int(ceil((max_deg - min_deg) /
                            min(degree(vw) for vw in func2)))

    # compute func1 * (1 + func2 + func2**2 + ... + func2**max_exponent)
    ret = Element(0)
    running_power = Element(1)
    for exponent in xrange(max_exponent + 1):
        ret += func1 * running_power
        running_power *= func2

    # truncate: kill off any terms vw with degree(vw) > max_deg
    adjustment = Element(0)
    for vw in ret:
        if degree(vw) > max_deg:
            adjustment -= ret[vw] * Element(vw)
    ret += adjustment

    return ret


def relation_finder(terms, eltlist=None, scalarset=[0, 1], normalize=False,
                    verbose=False):
    """
    Look for a relation among terms and report all found.  This function
    can be called on an iterable whose entries are either all of class
    Element or all of class Op.  In the latter case, eltlist must be set
    to an iterable of objects of class eltlist on which to test equality
    (since equality of Op objects is always in some representation).

    Relations sought are of the form
    \sum_i c_i x_i = 0
    where c_i \in scalarset, x_i \in terms.

    In the Op case, values of Op objects on entries of eltlist are cached in
    advance.

    Arguments:
        terms (iterable): Entries are either all of type Element or all of
            type Op
        eltlist (iterable): If terms are of class Element, then this should
            be None.  If terms are of class Op, then entries should be of
            class Element (or castable to class Element, such as Variable
            or Number).
        scalarset (iterable): The scalars to allow as coefficients in the
            relation.
        normalize (bool): If True, only consider relations in which the
            first coefficient equals 1.

    Return value:
        list of all relations found, where a relation is encoded as a list
        of pairs (term, coeff), with term of the same type as entries in terms,
        and coeff from scalarset.
    """
    ret = []
    zero = Element(0)
    num_funcs = len(scalarset) ** len(terms)

    if all(isinstance(term, Op) for term in terms):
        if eltlist is not None and all(isinstance(elt, Element)
                                       for elt in eltlist):
            # input is OK.  do a relation search using class Element
            found_count, total_count = 0, 1
            # cache values
            if verbose:
                print "caching operator values on test elements ({} total \
                       computations)...".format(len(terms) * len(eltlist))
            value_cache = [[term(elt) for elt in eltlist] for term in terms]
            for scalardict in finite_set_exponential(scalarset,
                                                     range(len(terms))):
                if verbose:
                    print "trying potential relation {} of {}, found {} so \
                           far...".format(total_count, num_funcs, found_count)
                    total_count += 1
                if not all(scalardict[key] == 0 for key in scalardict):
                    if all(sum(scalardict[i] * value_cache[i][j]
                               for i in xrange(len(terms))) == zero
                            for j in xrange(len(eltlist))):
                        ret.append([(terms[key], scalardict[key])
                                    for key in scalardict
                                    if scalardict[key] != 0])
                        found_count += 1
            return ret
        else:
            raise Exception("To call relation_finder() with Op terms, you \
                             must specify an eltlist.")

    elif all(isinstance(term, Element) for term in terms):
        if eltlist is None:
            # input is OK.  do a relation search using class Op
            found_count, total_count = 0, 1
            for scalardict in finite_set_exponential(scalarset,
                                                     range(len(terms))):
                if verbose:
                    print "trying potential relation {} of {}, found {} so \
                           far...".format(total_count, num_funcs, found_count)
                    total_count += 1
                if sum(scalardict[key] * terms[key] for key in scalardict) == \
                        zero and not all(scalardict[key] == 0
                                         for key in scalardict):
                    ret.append([(terms[key], scalardict[key])
                               for key in scalardict if scalardict[key] != 0])
                    found_count += 1
            return ret
        else:
            raise Exception("When calling relation_finder() with Element \
                             terms, eltlist should not be set.")

    else:
        raise TypeError
