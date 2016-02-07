Module: spdaot
(sage probably does all of this)

Alexander Ellis, 2016

This module replaces the following deprecated modules:
symmetric
manin_schechtman
nc_polynomial
mystic
odd_code
zero_hecke

TODO: documentation

Here's a quick summary, before I get around to writing proper documentation.

Things already implemented:
* base code for Variable, VariableWord, Relation, Element classes, which 
    handle free algebra modulo relations; wrapper for quickly creating
    q-commuting variables
* class Op, which allows for quickly computing  algebra and group actions
* some functional programming tools and decorators

Things to do, sooner:
* testing suite
* fill out documentation
* implement particular group actions of interest: S_n, S_n^-, D_n^-, B_n^+ 
    on S(V), S_{-1}(V)
* braided differential operators and their variants, S(V) and S_{-1}(V) cases
* 