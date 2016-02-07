"""
TODO
"""

def minus_s(x, i, sign=1, varletter='x'):
    """Simple generator of -D_n"""
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(i+1), scalar=sign, swap=True)
    return y * -1

def sig(x, i, sign=1, varletter='x'):
    """Simple generator of B_n^+"""
    y = x.copy()
    y.transform(varletter+str(i), varletter+str(i+1), scalar=sign, swap=True, revscalar=sign*-1)
    return y

