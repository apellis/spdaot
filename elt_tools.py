"""
spdaot.elt_tools

Overview:
    Useful tools for working with objects of class Element.

Functions:
    div_geometric(): TODO
"""

from math import ceil
from . import Element

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
    max_exponent = int(ceil((max_deg - min_deg) / min(degree(vw) for vw in func2)))

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
