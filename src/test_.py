# For use with [pytest](https://docs.pytest.org/)

from . import main

# Note that the equality checks here included text descriptions,
# but equality for DerivedUnit only checks the units.
# todo test the text too?


def test_compose_identity():
    assert main.kg / main.kg == main.I  # Base
    assert main.m**0 == main.I
    assert main.j / main.j == main.I  # Derived
    assert main.n**0 == main.I


def test_mul_base():
    assert main.kg * main.s == main.DerivedUnit(
        "kilogram · meter",
        "kg·m",
        [(main.kg, 1), (main.s, 1)],
        "mass · distance"
    )


def test_mul_derived():
    assert main.ohm * main.f == main.DerivedUnit(
        "ohm · farad",
        "s",
        [(main.s, 1)],
        "resistance · capacitance"
    )


def test_mul_derived_base():
    assert main.pa * main.m**2 == main.n  # the second one here is actually derived due to power...


def test_mul_base_derived():
    assert main.a * main.v == main.DerivedUnit(
        "volt · ampere",
        "kg·m²·s⁻¹·A",
        [(main.kg, 1), (main.m, 2), (main.s, -1), (main.a, 1)],
        "potential · current"
    )


def test_div_base():
    assert main.a / main.cd**2 == main.DerivedUnit(
        "ampere / candela²",
        "A·cd⁻²",
        [(main.a, 1), (main.cd, -2)],
        "current / luminosity"
    )


def test_div_derived():
    assert main.ohm / main.f == main.DerivedUnit(
        "ohm / farad",
        "kg²·m⁴·s⁻⁵·A⁻²",
        [(main.kg, 2), (main.m, 4), (main.s, -5), (main.a, -2)],
        "resistance / capacitance"
    )


def test_div_derived_base():
    assert main.pa * main.m ** 2 == main.n


def test_div_base_derived():
    assert main.a / main.v == main.DerivedUnit(
        "volt / ampere",
        "kg·m²·s⁻²·A⁻¹",
        [(main.kg, -1), (main.m, -2), (main.s, 2), (main.a, 1)],
        "potential / current"
    )


def test_eq_base_derived():
    assert main.kg == main.n * main.s**2 / main.m


def test_equality():
    assert main.kg * (main.m / main.s)**2 == main.j
    # assert main.v * main.a == main.w  # todo: SOmething fishy here...
    assert main.a * main.ohm == main.v


def test_mul_base_derived():
    pass