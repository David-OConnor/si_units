# For use with [pytest](https://docs.pytest.org/)

import src as u

# Note that the equality checks here included text descriptions,
# but equality for DerivedUnit only checks the units.
# todo test the text too?


def test_compose_identity():
    assert u.kg / u.kg == u.I  # Base
    assert u.m**0 == u.I
    assert u.j / u.j == u.I  # Derived
    assert u.n**0 == u.I


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


def test_div_base_derived():
    assert u.v / u.a == u.DerivedUnit(
        "volt / ampere",
        "kg·m²·s⁻³·A⁻²",
        [(u.kg, 1), (u.m, 2), (u.s, -3), (u.a, -2)],
        "potential / current"
    )


def test_eq_base_derived():
    assert u.kg == u.n * u.s**2 / u.m


def test_equality():
    assert u.kg * (u.m / u.s)**2 == u.j
    assert u.v * u.a == u.w
    assert u.a * u.ohm == u.v
    u.v / u.m == u.n / u.c


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


