from dataclasses import dataclass
from enum import Enum
from typing import List

# import base_units

# class Quantity(Enum):
#     FORCE = 1
#     PRESSURE = 2
#     ENERGY = 3

#     def __str__(self):
#         return 'my custom str! {0}'.format(self.value)

@dataclass
class BaseUnit:
    name: str  # lowercase.  eg "kilogram"
    abbrev: str  # caps sensitive. eg "kg"
    # todo enum?
    quantity: str  # lowercase. eg "mass"

    
@dataclass
class Assoc:
    """
    Associates a base unit, and its power
    """
    unit: BaseUnit
    power: int

    def __repr__(self):
        return f"{self.unit.name}, p: {self.power}"


@dataclass
class DerivedUnit:
    # See comments on fields of same name in BaseUnit.
    name: str
    abbrev: str
    base_units: List[Assoc]
    quantity: str  # lowercase. eg "mass"

    # todo: Tidy duplicates, perhaps in constructor
    def clean_units(self):
        result = []
        checked_units = []
        for unit in self.base_units:
            if unit in checked_units:
                continue

            checked_units.append(unit)

        self.base_units = result


# http://www.ebyte.it/library/educards/siunits/TablesOfSiUnitsAndPrefixes.html

# Base units
kg = BaseUnit("kilogram", "kg", "mass")
s = BaseUnit("second", "s", "time")
k = BaseUnit("kelvin", "K", "temperature")
a = BaseUnit("ampere", "A", "current")
mol = BaseUnit("mole", "mol", "quantity of substance")
cd = BaseUnit("candela", "cd", "luminosity")
m = BaseUnit("meter", "m", "distance")

# Unitless
rad = BaseUnit("radian", "rad", "")  # todo count this?

# Derived
hz = DerivedUnit("hertz", "Hz", [Assoc(s, -1)], "frequency")

n = DerivedUnit("newton", "N", [Assoc(kg, 1), Assoc(m, 1), Assoc(s, -1)], "force")
pa = DerivedUnit("pascal", "Pa", [n.base_units] + [Assoc(m, -2)], "pressure")
j = DerivedUnit("joule", "J", [n.base_units] + [Assoc(m, 1)], "energy")
w = DerivedUnit("watt", "W", [j.base_units] + [Assoc(s, -1)], "power")

# Celsius ?

c = DerivedUnit("coulomb", "C", [Assoc(a, 1), Assoc(s, 1)], "charge")
v = DerivedUnit("volt", "V", [w.base_units] + [Assoc(s, 1)], "potential")
