[![image](https://img.shields.io/pypi/v/siunits.svg)](https://pypi.org/project/siunits/)
[![image](https://img.shields.io/pypi/l/siunits.svg)](https://pypi.org/project/siunits/)
[![image](https://img.shields.io/pypi/pyversions/siunits.svg)](https://pypi.org/project/siunits/)

# SI Units

This is a library used to symbolically manipulate SI units. It comprises a `BaseUnit` type,
used for base SI units like `kilogram`, `meter` etc, a `DerivedUnit` type,
for units derived from them, and a `Composite` type, for when numerical coefficients
are included.

This library is useful for dimensional analysis. Python version 3.7 or greater is required. There are no dependencies.

You can perform normal multiplication, division, and power operations on units
provided by this lib, and between them and `int`s and `floats`, and check equality,
based on the resulting combination of base units.

## Examples

A base unit:
```python
import siunits as u

u.kg
>>> kilogram (kg), mass
```

A derived unit:
```python
u.v
>>> volt (V), [kg: 1, m: 2, s: -3, A: -1]
```

Multiplication:
```python
u.kg * u.s
>>> kilogram·second (kg·s), [kg: 1, s: 1]
```

Division:
```python
u.j / u.m**2
>>> joule / meter² (kg·s⁻²), [kg: 1, s: -2]

u.s**2 / u.kg**3
>>> second²·kilogram⁻³ (s²·kg⁻³), [s: 2, kg: -3]

```

With numerical coefficients:
```python
2*u.a**2 * 3*u.v**2
>>> 6kg²·m⁴·s⁻⁶
```

Equality testing is based on composition of base units:
```python
u.w == u.v * u.a == u.kg * u.m**2 / u.s**3
>>> True
```

## Todo

- Infer composite types that match a given custom (eg multiplied) unit
- Apply arithmetic to quantities as well (eg `energy`, `work` etc), and display them


## Scope

This project doesn't aim to provide conversions with other unit systems, like
`cgs` and `imperial`, nor does it provide physical constants. For these
tasks, try [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html).

## Why add another unit library?

The clean symbolic manipulation this library provides doesn't appear to exist
in any existing one.
