# Module: `spdaot`
### (sage probably does all of this)
#### Alexander Ellis, 2016

This module replaces the following deprecated modules:

* `symmetric`
* `manin_schechtman`
* `nc_polynomial`
* `mystic`
* `odd_code`
* `zero_hecke`

I've removed the above modules from Github.  But until `spdaot` catches up and re-implements all the functonality from those modules, you can email me if you want a copy of the older code.

See SPECIFICATION.md for documentation.

##### Things already implemented:

* class `Op`, which allows for quickly computing  algebra and group actions
* base code for Variable, VariableWord, Relation, Element classes, which handle free algebra modulo relations; wrapper for quickly creating q-commuting variables; inverses
* class Op, which allows for quickly computing  algebra and group actions
* some functional programming tools and decorators
* `D_n^-`, `B_n^+` group actions on `S_{-1}(V)`; braided differentials; isobaric braided differentials
* exact scalar relation finder

##### Things to do, sooner:

* testing suite
* more documentation (SPECIFICATION.md)
* `S_n` group action on `S_1(V)`
* add better type checking and error protection to class Op, especially in `Op.__init__()`
* rank-based relation finder

##### Things to do, later:

* Young cosets and their minimal/maximal representatives
* pickling routines for caching combinatorial data
* convert between reduced Coxeter expression and one-line notation for permutations
* generate Manin-Schechtman graph
* q-bilinear form on quantum noncommutative symmetric polynomials; generalizations of this
* combinatorial data on permutations: descent set, descent compositon, inversions
* classes for Young diagrams and tableaux
* elementary, complete, power sum, schur, schubert polynomials; odd analogues of these, both twisted and untwisted
* Grothendieck polynomials
* RSK, partitions, compositions
* profile and optimize

##### Contact

Email: [apellis@gmail.com](mailto:apellis@gmail.com)

Github: [https://github.com/apellis/spdaot](https://github.com/apellis/spdaot)