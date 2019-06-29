from dataclasses import dataclass
from enum import Enum
import operator
from typing import Callable, Dict, List, Tuple, Union

# import base_units

# class Quantity(Enum):
#     FORCE = 1
#     PRESSURE = 2
#     ENERGY = 3

#     def __str__(self):
#         return 'my custom str! {0}'.format(self.value)

@dataclass
class BaseUnit:
    id: int  # Must be unique.
    name: str  # lowercase.  eg "kilogram"
    abbrev: str  # caps sensitive. eg "kg"
    # todo enum?
    quantity: str  # lowercase. eg "mass"

    # todo: Dry with this method in DerivedUnit
    def _mul_helper(self, other: Union['BaseUnit', 'DerivedUnit'], 
        op: Callable, symbol: str) -> 'DerivedUnit':
        """Avoids repetition between __mul__ and __truediv__"""
        unit_map = {self: 1}

        if type(other) == BaseUnit:
            if other in unit_map.keys():
                unit_map[other] = op(unit_map[other], 1)
            else:
                unit_map[other] = 1
        else:
            for u in other.base_units:
                if u.unit in unit_map.keys():
                    unit_map[u.unit] = op(unit_map[u.unit], u.power)
                else:
                    unit_map[u.unit] = u.power

        base_units = [Assoc(k, v) for k, v in unit_map.items()]
        return DerivedUnit(
            f"{self.name} + {other.name}", 
            f"{self.abbrev} {symbol} {other.abbrev}", 
            base_units, 
            f"{self.quantity} {symbol} {other.quantity}"
        )

    def __mul__(self, other: Union['BaseUnit', 'DerivedUnit']) -> 'DerivedUnit':
        return self._mul_helper(other, operator.add, "·")

    def __truediv__(self, other: Union['BaseUnit', 'DerivedUnit']) -> 'DerivedUnit':
        return self._mul_helper(other, operator.sub, "/")

    # todo DRY with __pow__ in DerivedUnit
    def __pow__(self, power: int) -> 'DerivedUnit':
        result = self
        for _ in range(power - 1):
            result = result * self
        return result

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash((self.id,))

    def __repr__(self):
        return f"{self.name}({self.abbrev}) - {self.quantity}"

    
@dataclass
class Assoc:
    """
    Associates a base unit, and its power
    """
    unit: BaseUnit
    power: int

    def __repr__(self):
        return f"{self.unit.name}: {self.power}"

def _to_unit_map(units: List[Assoc]) -> Dict[BaseUnit, int]:
    """Used to dedupe a list of Assoc"""
    result = {}
    for u in units:
        if u.unit in result.keys():
            result[u.unit] += 1
        else:
            result[u.unit] = u.power
    return result

@dataclass
class DerivedUnit:
    # See comments on fields of same name in BaseUnit.
    name: str
    abbrev: str
    base_units: List[Assoc]
    quantity: str  # lowercase. eg "mass"

    def __init__(
        self, 
        name: str, 
        abbrev: str, 
        base_units: List[Assoc], 
        quantity: str
        ) -> 'DerivedUnit':

        """This method exists to consolidate base units, if there are duplicates."""
        self.name = name
        self.abbrev = abbrev
        self.base_units = [Assoc(k, v) for k, v in _to_unit_map(base_units).items()]
        self.quantity = quantity 

    # def id(self) -> str:
    #     """A unique id, generated only from base units."""
    #     pass

    def _mul_helper(self, other: Union[BaseUnit, 'DerivedUnit'], 
            op: Callable, symbol: str) -> 'DerivedUnit':
        """Avoids repetition between __mul__ and __div__"""
        unit_map = _to_unit_map(self.base_units)

        if type(other) == BaseUnit:
            if other in unit_map.keys():
                unit_map[other] = op(unit_map[other], 1)
            else:
                unit_map[other] = 1
        else:
            for u in other.base_units:
                if u.unit in unit_map.keys():
                    unit_map[u.unit] = op(unit_map[u.unit], u.power)
                else:
                    unit_map[u.unit] = u.power

        base_units = [Assoc(k, v) for k, v in unit_map.items()]
        return DerivedUnit(
            f"{self.name} + {other.name}", 
            f"{self.abbrev} {symbol} {other.abbrev}", 
            base_units, 
            f"{self.quantity} {symbol} {other.quantity}"
        )
    
    def __mul__(self, other: Union[BaseUnit, 'DerivedUnit']) -> 'DerivedUnit':
        return self._mul_helper(other, operator.add, "·")

    def __truediv__(self, other: Union[BaseUnit, 'DerivedUnit']) -> 'DerivedUnit':
        return self._mul_helper(other, operator.sub, "/")

    def __pow__(self, power: int) -> 'DerivedUnit':
        result = self
        for _ in range(power - 1):
            result = result * self
        return result

    def __repr__(self):
        return f"{self.name}({self.abbrev}), {self.base_units} - {self.quantity}"

def compose(units: List[Tuple]) -> List[Assoc]:
    """
    Combine assitions from units
    """
    for unit, power in units:
        if type(unit) == BaseUnit:
            pass
        elif type(unit) == DerivedUnit:
            pass
        elif type(unit) == Assoc:
            pass
        else:
            raise TypeError("Incorrect type passed to compose")


# http://www.ebyte.it/library/educards/siunits/TablesOfSiUnitsAndPrefixes.html

# Base units
kg = BaseUnit(0, "kilogram", "kg", "mass")
s = BaseUnit(1, "second", "s", "time")
k = BaseUnit(2, "kelvin", "K", "temperature")
a = BaseUnit(3, "ampere", "A", "current")
mol = BaseUnit(4, "mole", "mol", "quantity of substance")
cd = BaseUnit(5, "candela", "cd", "luminosity")
m = BaseUnit(6, "meter", "m", "distance")

# Unitless
rad = BaseUnit(7, "radian", "rad", "")  # todo count this?

# Derived
hz = DerivedUnit("hertz", "Hz", [Assoc(s, -1)], "frequency")

n = DerivedUnit("newton", "N", [Assoc(kg, 1), Assoc(m, 1), Assoc(s, -2)], "force")
pa = DerivedUnit("pascal", "Pa", n.base_units + [Assoc(m, -2)], "pressure")
j = DerivedUnit("joule", "J", n.base_units + [Assoc(m, 1)], "energy")
w = DerivedUnit("watt", "W", j.base_units + [Assoc(s, -1)], "power")

# Celsius ?

c = DerivedUnit("coulomb", "C", [Assoc(a, 1), Assoc(s, 1)], "charge")
v = DerivedUnit("volt", "V", w.base_units + [Assoc(s, 1)], "potential")
ohm = DerivedUnit("ohm", "Ω", v.base_units + [Assoc(a, -1)], "resistance")
# s = DerivedUnit("siemens", "S", [Assoc(a, 1) + [Assoc(a, -1)], "conductance")
# f = DerivedUnit("farad", "F", [Assoc()], "capacitance")