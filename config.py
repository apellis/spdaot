"""
spdaot.config

Overview:
    This module contains configuration settings for the spdaot package.
"""

variables = {}
"""
dict: keys are strings (variables names), values are Variable objects

Never use a variable name ending in the character 'i', since it is used to 
denote inverses.
"""

relations = {}
"""
dict: keys are of type VariableWord (left-hand side), values are of type 
Relation (the whole relation)
"""

print_options = {'addsep': ' + ', 'mulsep': '', 'use_exponents': False}
"""
dict

Keys are names of settings related to printing, values are the corresponding 
settings.

Settings:
    addsep (string): inserted added variables when printing
    mulsep (string): inserted multiplied variables when printing
    use_exponents (bool): if True, a * a * a will display as a^3, and so forth
"""


