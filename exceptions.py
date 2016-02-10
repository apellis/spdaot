"""
spdaot.exceptions

Overview:
    This module contains custom exceptions for the spdaot package.

Exceptions:
    VariableNameCollision: raised when trying to create a new variable with 
        a name already use for another variable
    UnknownVariableName: raised when trying to use a variable name which 
        hasn't been registered
"""

class VariableNameCollision(Exception): 
    pass

class UnknownVariableName(Exception):
    pass

class InvalidVariableName(Exception):
    pass