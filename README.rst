SI Units
========

This is a library used to symbolically manipulate SI units. It comprises a `BaseUnit` type,
used for base SI units like `kilogram`, `meter` etc, and a `DerivedUnit` type,
for units derived from them.

This library is useful for dimensional analysis.

Python version 3.7 or greater is required.

Scope
-----
This project doesn't aim to provide conversions with other unit systems, like
`cgs` and `imperial`, nor does it provide physical constants. For these
tasks, try [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html).

Why add another unit library?
-----------------------------
The clean symbolic manipulation this library provides doesn't appear to exist
in any existing one.
