# For use with [pytest](https://docs.pytest.org/)

import siunits as u
import pytest

# Note that the equality checks here included text descriptions,
# but equality for DerivedUnit only checks the units.
# todo test the text too?


def test_compose_identity():
    assert u.kg / u.kg == u.I  # Base
    assert u.m**0 == u.I
    assert u.j / u.j == u.I  # Derived
    assert u.n**0 == u.I


# Tests for '+'
def test_add_base():
    assert u.kg + u.kg == u.Composite(2, u.kg)


def test_add_base_number():
    assert u.kg + 1 == u.Composite(2, u.kg)
    assert 1 + u.kg == u.Composite(2, u.kg)


def test_add_base_incompatible():
    with pytest.raises(TypeError):
        test = u.kg + u.m


def test_add_derived():
    assert u.m/u.s + u.m/u.s == u.Composite(
        2, u.m/u.s
    )


def test_add_derived_number():
    assert u.m/u.s + 2.5 == u.Composite(
        3.5, u.m/u.s
    )
    assert 2.5 + u.m/u.s == u.Composite(
        3.5, u.m/u.s
    )


def test_add_derived_incompatible():
    with pytest.raises(TypeError):
        test = u.m/u.s + u.kg/u.s


def test_add_composite():
    assert 2*u.m/u.s + 2*u.m/u.s == u.Composite(4, u.m/u.s)


def test_add_composite_incompatible():
    with pytest.raises(TypeError):
        2*u.m/u.s + 2*u.kg/u.s


# Tests for '+='
def test_iadd_base():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test += u.kg
    assert isinstance(test, u.Composite)
    assert test == u.Composite(2, u.kg)


def test_iadd_base_number():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test += 1
    assert isinstance(test, u.Composite)
    assert test == u.Composite(2, u.kg)


def test_iadd_base_incompatible():
    test = u.kg
    with pytest.raises(TypeError):
        test += u.m


def test_iadd_derived():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived += u.m/u.s
    assert isinstance(derived, u.Composite)
    assert derived == u.Composite(2, u.m/u.s)


def test_iadd_derived_number():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived += 2.5
    assert derived == u.Composite(
        3.5, u.m/u.s
    )
    number = 2.5
    number += u.m/u.s
    assert isinstance(number, u.Composite)
    assert number == u.Composite(
        3.5, u.m/u.s
    )


def test_iadd_derived_incompatible():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    with pytest.raises(TypeError):
        derived += u.kg/u.s


def test_iadd_composite():
    composite = 2*u.m/u.s
    composite += 3*u.m/u.s
    assert composite == u.Composite(5, u.m/u.s)


def test_iadd_composite_incompatible():
    composite = 2*u.m/u.s
    with pytest.raises(TypeError):
        composite += 2*u.kg/u.s


# Tests for '-'
def test_sub_base():
    assert u.kg - u.kg == 0


def test_sub_base_number():
    assert u.kg - 1 == 0
    assert 1 - u.kg == 0


def test_sub_base_incompatible():
    with pytest.raises(TypeError):
        test = u.kg - u.m


def test_sub_derived():
    assert u.m/u.s - u.m/u.s == 0


def test_sub_derived_number():
    assert u.m/u.s - 2.5 == u.Composite(
        -1.5, u.m/u.s
    )
    assert 2.5 - u.m/u.s == u.Composite(
        -1.5, u.m/u.s
    )


def test_sub_derived_incompatible():
    with pytest.raises(TypeError):
        test = u.m/u.s - u.kg/u.s


def test_sub_composite():
    assert 2*u.m/u.s - 3*u.m/u.s == u.Composite(-1, u.m/u.s)


def test_sub_composite_incompatible():
    with pytest.raises(TypeError):
        2*u.m/u.s - 2*u.kg/u.s


# Tests for '-='
def test_isub_base():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test -= u.kg
    assert isinstance(test, u.Composite)
    assert test == 0


def test_isub_base_number():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test -= 1
    assert isinstance(test, u.Composite)
    assert test == 0


def test_isub_base_incompatible():
    test = u.kg
    with pytest.raises(TypeError):
        test -= u.m


def test_isub_derived():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived -= u.m/u.s
    assert isinstance(derived, u.Composite)
    assert derived == 0


def test_isub_derived_number():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived -= 2.5
    assert derived == u.Composite(
        -1.5, u.m/u.s
    )
    number = 2.5
    number -= u.m/u.s
    assert isinstance(number, u.Composite)
    assert number == u.Composite(
        -1.5, u.m/u.s
    )


def test_isub_derived_incompatible():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    with pytest.raises(TypeError):
        derived -= u.kg/u.s


def test_isub_composite():
    composite = 2*u.m/u.s
    composite -= 3*u.m/u.s
    assert composite == u.Composite(-1, u.m/u.s)


def test_isub_composite_incompatible():
    composite = 2*u.m/u.s
    with pytest.raises(TypeError):
        composite -= 2*u.kg/u.s


# tests for '*'
def test_mul_base():
    assert u.kg * u.s == u.DerivedUnit(
        "kilogram · meter",
        "kg·m",
        [(u.kg, 1), (u.s, 1)],
        "mass · distance"
    )


def test_mul_derived():
    assert u.ohm * u.f == u.DerivedUnit(
        "ohm · farad",
        "s",
        [(u.s, 1)],
        "resistance · capacitance"
    )


def test_mul_derived_base():
    assert u.pa * u.m**2 == u.n  # the second one here is actually derived due to power...


def test_mul_base_derived():
    assert u.a * u.v == u.DerivedUnit(
        "ampere·volt",
        "kg·m²·s⁻³",
        [(u.kg, 1), (u.m, 2), (u.s, -3)],
        "potential · current"
    )


# Tests for '*='
def test_imul_base():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test *= u.kg
    assert isinstance(test, u.DerivedUnit)
    assert test == u.kg ** 2


def test_imul_base_number():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test *= 2
    assert isinstance(test, u.Composite)
    assert test == 2*u.kg


def test_imul_derived():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived *= u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    assert derived == u.m ** 2 / u.s ** 2


def test_imul_derived_number():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived *= 2.5
    assert derived == u.Composite(
        2.5, u.m/u.s
    )
    number = 2.5
    number *= u.m/u.s
    assert isinstance(number, u.Composite)
    assert number == u.Composite(
        2.5, u.m/u.s
    )


def test_imul_composite():
    composite = 2*u.m/u.s
    composite *= 3*u.m/u.s
    assert composite == u.Composite(6, u.m ** 2 / u.s ** 2)


# tests for '/'
def test_div_base():
    assert u.a / u.cd**2 == u.DerivedUnit(
        "ampere / candela²",
        "A·cd⁻²",
        [(u.a, 1), (u.cd, -2)],
        "current / luminosity"
    )


def test_div_derived():
    assert u.ohm / u.f == u.DerivedUnit(
        "ohm / farad",
        "kg²·m⁴·s⁻⁷·A⁻⁴",
        [(u.kg, 2), (u.m, 4), (u.s, -7), (u.a, -4)],
        "resistance / capacitance"
    )


def test_div_derived_base():
    assert u.pa * u.m ** 2 == u.n
    assert u.kg * u.m / u.s ** 2 == u.n
    derived = u.n
    base = u.s
    res = derived / base
    assert isinstance(res, u.DerivedUnit)
    assert res == u.kg * u.m / u.s ** 3


def test_div_derived_composite():
    # Derived / Composite
    derived = u.n
    composite = 2 * derived
    # check for the right type
    assert isinstance(derived, u.DerivedUnit)
    assert isinstance(composite, u.Composite)
    res = derived / composite
    assert res == 1/2
    # Composite / Derived
    res = composite / derived
    assert res == 2


def test_div_base_composite():
    # Base / Composite
    base = u.s
    composite = 2 * base
    # check for the right type
    assert isinstance(base, u.BaseUnit)
    assert isinstance(composite, u.Composite)
    res = base / composite
    assert res == 1/2
    # Composite / Base
    res = composite / base
    assert res == 2


def test_div_base_derived():
    assert u.v / u.a == u.DerivedUnit(
        "volt / ampere",
        "kg·m²·s⁻³·A⁻²",
        [(u.kg, 1), (u.m, 2), (u.s, -3), (u.a, -2)],
        "potential / current"
    )


# division by and with a number for BaseUnit
def test_div_base_number():
    # __truediv__
    assert u.v / 2 == u.Composite(1/2, u.v)
    # __rtruediv__
    assert 2 / u.s == u.Composite(2, u.s**-1)


# division by and with a number for Derived
def test_div_derived_number():
    derived_unit = u.m / u.s
    # __truediv__
    assert derived_unit / 2 == u.Composite(1/2, derived_unit)
    # __rtruediv__
    assert 2 / derived_unit == u.Composite(2, derived_unit ** -1)


# division by and with a number for Composite
def test_div_composite_number():
    composite_unit = 4 * u.m / u.s
    temp = composite_unit / 2
    # __truediv__
    assert temp == u.Composite(2, u.m / u.s)
    # __rtruediv__
    temp = 2 / composite_unit
    assert temp == u.Composite(1/2, u.s / u.m)


# Tests for '/='
def test_idiv_base():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test /= u.kg
    assert isinstance(test, u.DerivedUnit)
    assert test == 1


def test_idiv_base_number():
    test = u.kg
    assert isinstance(test, u.BaseUnit)
    test /= 2
    assert isinstance(test, u.Composite)
    assert test == 1/2*u.kg


def test_idiv_derived():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived /= u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    assert derived == 1


def test_idiv_derived_number():
    derived = u.m/u.s
    assert isinstance(derived, u.DerivedUnit)
    derived /= 2.5
    assert derived == u.Composite(
        1/2.5, u.m/u.s
    )
    number = 2.5
    number /= u.m/u.s
    assert isinstance(number, u.Composite)
    assert number == u.Composite(
        2.5, u.s/u.m
    )


def test_idiv_composite():
    composite = 4*u.kg/u.s
    composite /= 2*u.m/u.s
    assert composite == u.Composite(2, u.kg / u.m)


# test '__eq__'
def test_eq_base_derived():
    assert u.kg == u.n * u.s**2 / u.m


def test_equality():
    assert u.kg * (u.m / u.s)**2 == u.j
    assert u.v * u.a == u.w
    assert u.a * u.ohm == u.v
    assert u.v / u.m == u.n / u.c


def test_equality_mixed():
    assert 3 * u.w == 6 * u.v * 0.5 * u.a == 3 * u.kg * u.m**2 / u.s**3


def test_composite_base():
    assert (u.kg * 2) * (3 * u.s) == u.Composite(6, u.kg * u.s)


def test_composite_derived():
    assert (u.v * 2) * (3 * u.j) == u.Composite(
        6, u.kg**2 * u.m**4 * u.s**-5 / u.a
    )


def test_composite_derived_base():
    assert (u.v * -4) * (2.0 * u.a) == u.Composite(
        -8., u.kg * u.m**2 * u.s**-3
    )


