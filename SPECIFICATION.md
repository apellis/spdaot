# Overview

## Modules

The core classes of `spdaot` are implemented in the modules `variable` (representing named variables and monomials in these variables), `relation` (representing an algebraic relation among known variables), `element` (representing linear combinations of monomials), and `op` (representing operators, i.e., elements of an algebraic object acting in some representation).  The former two of these are internal, and the latter two are user facing.  The modules `tools` and `odd` contain user-facing code as well.

There are also three internal utility modules: `exceptions` (custom exceptions), `frosting` (mostly functional programming tools and decorators), and `tests` (a testing suite for all of `spdaot`).

The module `config` contains configuration options, some of which are user facing.

##### Module dependencies

* `variable`: `config`, `exceptions`, `frosting`
* `op`: `frosting`
* `element`: `config`, `variable`, `relation`
* `relation`: `config`, `variable`
* `odd`: `variable`, `element`, `op`
* `tests`: (all)
* `tools`: `element`, `op`


# User facing components

### Classes

TODO: describe all classes, where they appear, whether or not they're exported to the root package, class interfaces and internals, dependencies

TODO: all direct dependencies: `Element` (`Relation`, `VariableWord`)

### Functions

TODO


# Internal components

### Classes

TODO

TODO: all direct dependencies: `Relation` (`VariableWord`, `Variable`); `VariableWord` (`Variable`)

### Functions

TODO


# Examples

TODO