"""
spdaot

Overview:
    TODO

Submodules:
    frosting: useful decorators
    config: global settings for the package
    exceptions: custom exceptions for the package
    tests: testing suite
    op: Op class useful for group and algebra actions
    variable: Variable class for variable name registration
    relation: Relation class for relations among known Variable objects
"""

from .variable import Variable, VariableWord
from .relation import Relation
from .op import Op
from .element import Element, make_poly_family, add_central_variable
from .tools import relation_finder

