from collections import defaultdict
from dataclasses import dataclass
# from enum import Enum
import operator
from typing import Callable, Dict, List, Tuple, Union

# import base_units


@dataclass
class BaseUnit:
    id: int  # Must be unique.
    _name: str  # lowercase.  eg "kilogram"
    abbrev: str  # caps sensitive. eg "kg"
    quantity: str  # lowercase. eg "mass"

    def name(self):  # For compatibility with DerivedUnit
        return self._name

    def _text_eq(self, other: Union['BaseUnit', 'DerivedUnit']) -> bool:
        """For testing"""
        return self.name == other.name and self.abbrev == other.abbrev and \
            self.quantity == other.quantity

    def __mul__(self, other: Union['BaseUnit', 'DerivedUnit', int, float]) -> Union['DerivedUnit', 'Composite']:
        return _mul_helper(self, other, {self: 1}, operator.add, "·")

    __rmul__ = __mul__

    # def __rmul__(self, other: Union['BaseUnit', 'DerivedUnit']) -> 'DerivedUnit':
    #     return _mul_helper(self, other, {self: 1}, operator.add, "·")

    def __truediv__(self, other: Union['BaseUnit', 'DerivedUnit', int, float]) \
            -> Union['DerivedUnit', 'Composite']:
        return _mul_helper(self, other, {self: 1}, operator.sub, "/")

    def __pow__(self, power: int) -> 'DerivedUnit':
        return _pow(self, power)

    def __eq__(self, other: Union['BaseUnit', 'DerivedUnit']) -> bool:
        if not other:
            return False
        if type(other) == BaseUnit:
            return self.id == other.id
        elif type(other) == DerivedUnit:
            return other.base_units == [Assoc(self, 1)]
        else:
            raise NotImplemented("Can only compare BaseUnit to another "
                                 "BaseUnit, or DerivedUnit")

    def __hash__(self):
        return hash((self.id,))

    def __repr__(self):
        return f"{self._name} ({self.abbrev}), {self.quantity}"

    
@dataclass
class Assoc:
    """
    Associates a base unit, and its power
    """
    # todo: Currently, this wrapper doesn't do anything. Consider removing.
    unit: BaseUnit
    power: int

    def __repr__(self):
        return f"{self.unit.abbrev}: {self.power}"


@dataclass
class DerivedUnit:
    # See comments on fields of same name in BaseUnit.
    _name_tokens: List[Tuple[str, int]]  # name, power
    abbrev: str
    base_units: List[Assoc]
    quantity: str  # todo infer this?

    def name(self) -> str:
        """This method keeps the units used in constructing it,
        rather than decompose into base units."""
        result_map = defaultdict(int)
        for name_, power in self._name_tokens:
            result_map[name_] += power
        return "·".join(k_ + _power_text(v_) for k_, v_ in result_map.items())

    def name_base(self) -> str:
        """This method decomposes into base units."""
        pass

    def rename(self, name: str, abbrev: str, quantity: str) -> 'DerivedUnit':
        """Useful for creating custom units composed of other units."""
        return DerivedUnit(name, abbrev, [(u.unit, u.power) for u in self.base_units], quantity)

    def _text_eq(self, other: Union['BaseUnit', 'DerivedUnit']) -> bool:
        """For testing"""
        return self.name() == other.name() and self.abbrev == other.abbrev and \
            self.quantity == other.quantity

    def __init__(
        self, 
        name: str,
        abbrev: str, 
        base_units: List[Tuple[BaseUnit, int]],
        quantity: str
    ) -> 'DerivedUnit':

        """This method exists to consolidate base units, if there are duplicates."""
        self._name_tokens = [(name, 1)]
        self.abbrev = abbrev

        base_units2 = [Assoc(b[0], b[1]) for b in base_units]
        self.base_units = [Assoc(k_, v_) for k_, v_ in _to_unit_map(base_units2).items()]

        self.quantity = quantity

    def __mul__(self, other: Union[BaseUnit, 'DerivedUnit', int, float]) -> Union['DerivedUnit', 'Composite']:
        return _mul_helper(self, other, _to_unit_map(self.base_units), operator.add, "·")

    __rmul__ = __mul__

    def __truediv__(self, other: Union[BaseUnit, 'DerivedUnit', int, float]) -> Union['DerivedUnit', 'Composite']:
        return _mul_helper(self, other, _to_unit_map(self.base_units), operator.sub, "/")

    # todo inplace mul and div.

    def __pow__(self, power: int) -> 'DerivedUnit':
        return _pow(self, power)

    def __eq__(self, other: 'DerivedUnit') -> bool:
        """Note that this only tests units."""
        return _to_unit_map(self.base_units) == _to_unit_map(other.base_units)

    def __repr__(self):
        return f"{self.name()} ({self.abbrev}), {self.base_units}, {self.quantity}"
        # return f"{self.name()} ({self.abbrev}), {self.quantity}"


def _to_unit_map(units: List[Assoc]) -> Dict[BaseUnit, int]:
    """Used to dedupe a list of Assoc"""
    result = {}
    for u in units:
        if u.unit in result.keys():
            result[u.unit] += 1
        else:
            result[u.unit] = u.power
    return {k_: v_ for k_, v_ in result.items() if v_ != 0}


def _base_description(units: List[Assoc]) -> str:
    """This reconstructs the description from base units."""
    unit_map = _to_unit_map(units)
    # todo: Sort by power, high to low?
    return "·".join(unit.abbrev + _power_text(power) for unit, power in unit_map.items())


def _handle_description(units: List[Union[BaseUnit, DerivedUnit]]) -> Tuple[str, str, str]:
    """This allows us to reconstruct using derived units, instead of just
    base ones."""
    # todo

    return


def _mul_helper(
    self: Union['BaseUnit', 'DerivedUnit', int, float],
    other: Union['BaseUnit', 'DerivedUnit', int, float],
    init_map: Dict[Union['BaseUnit', 'DerivedUnit'], int], 
    op: Callable, 
    symbol: str
) -> 'DerivedUnit':
    """Avoids repetition between __mul__ and __truediv__"""
    unit_map = init_map

    if type(other) == BaseUnit:
        if other in unit_map.keys():
            unit_map[other] = op(unit_map[other], 1)
        else:
            unit_map[other] = -1 if symbol == "/" else 1

    elif type(other) == DerivedUnit:
        for u in other.base_units:
            if u.unit in unit_map.keys():
                unit_map[u.unit] = op(unit_map[u.unit], u.power)
            else:
                unit_map[u.unit] = -u.power if symbol == "/" else u.power

    elif type(other) == Composite:
        # Let composite's mult function handle this - other must be first here.
        return other * self

    elif type(other) == int or type(other) == float:
        return Composite(other, self)

    else:
        raise TypeError("Must multiply by BaseUnit, DerivedUnit, or a number")

    if len([u for u in unit_map.values() if u != 0]) == 0:
        return I

    base_units = [(k_, v_) for k_, v_ in unit_map.items()]
    base_units2 = [Assoc(k_, v_) for k_, v_ in unit_map.items()]

    result = DerivedUnit(
        "",
        _base_description(base_units2),
        base_units,
        f"{self.quantity} {symbol} {other.quantity}"
    )

    # The constructor takes name as a string, so modify the field directly
    # to add the tokens

    if type(self) == BaseUnit:
        self_tokens = [(self._name, -1 if symbol == "/" else 1)]
    else:
        self_tokens = self._name_tokens
    if type(other) == BaseUnit:
        other_tokens = [(other._name, -1 if symbol == "/" else 1)]
    else:
        other_tokens = other._name_tokens

    result._name_tokens = self_tokens + other_tokens
    return result


@dataclass
class Composite:
    coef: Union[float, int]
    unit: Union[BaseUnit, DerivedUnit]

    def __mul__(self, other: Union[BaseUnit, DerivedUnit, int, float]) -> 'Composite':
        if type(other) == BaseUnit or type(other) == DerivedUnit:
            return Composite(self.coef, self.unit * other)
        elif type(other) == Composite:
            return Composite(self.coef * other.coef, self.unit * other.unit)
        elif type(other) == int or type(other) == float:
            return Composite(self.coef * other, self.unit)
        else:
            raise TypeError("Multiplication must be by a unit or number")

    __rmul__ = __mul__

    def __repr__(self):
        return f"{self.coef}{self.unit.abbrev}"


def _pow(unit: Union[BaseUnit, DerivedUnit], power: int) -> DerivedUnit:
    """Helper to avoid repeated code in BaseUnit and DerivedUnit."""
    result = DerivedUnit("𝟙", "", [], "𝟙")

    if power > 0:
        for _ in range(power):
            result = result * unit
    else:
        for _ in range(abs(power)):
            result = result / unit
    return result


def _power_text(power: int) -> str:
    chars = {
        "-": "⁻",
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
    }

    result = "".join(chars[char] for char in str(power))
    # Ommit first power
    new_result = ""  # Don't modify result in place
    for i, char in enumerate(result):
        if char == "¹":
            if i == 0 or result[i-1] != "⁻":
                continue
        new_result += char

    return new_result


I = DerivedUnit("𝟙", "", [], "𝟙")

# http://www.ebyte.it/library/educards/siunits/TablesOfSiUnitsAndPrefixes.html

# Base units
kg = BaseUnit(0, "kilogram", "kg", "mass")
s = BaseUnit(1, "second", "s", "time")
k = BaseUnit(2, "kelvin", "K", "temperature")
a = BaseUnit(3, "ampere", "A", "current")
mol = BaseUnit(4, "mole", "mol", "quantity of substance")
cd = BaseUnit(5, "candela", "cd", "luminosity")
m = BaseUnit(6, "meter", "m", "distance")

# Derived

# Unitless  # todo special handling?
rad = I.rename("radian", "rad", "plane angle")
sr = I.rename("steradian", "sr", "solid angle")
hz = (I / s).rename("hertz", "Hz", "frequency")

n = (kg * m * s**-2).rename("newton", "N", "force")
pa = (n / m**2).rename("pascal", "Pa", "pressure")
j = (n * m).rename("joule", "J", "energy")
w = (kg * m**2 * s**-3).rename("watt", "W", "power")

# celsius = k.rename("celsius", "°C", "temperature")  # todo distinguish from kelvin?
celsius = DerivedUnit("celsius", "°C", [(k, 1)], "temperature")  # todo distinguish from kelvin?

c = (a * s).rename("coulomb", "C", "charge")
v = (w / a).rename("volt", "V", "potential")
ohm = (v / a).rename("ohm", "Ω", "resistance")
siem = (a / v).rename("siemens", "S", "conductance")
f = (c / v).rename("farad", "F", "capacitance")
h = (v * s / a).rename("henry", "H", "inductance")
wb = (j / a).rename("weber", "Wb", "magnetic flux")
t = (wb / m**2).rename("tesla", "T", "magnetic flux density")

lm = (cd * sr).rename("lumen", "lm", "luminous flux")
lx = (lm / m**2).rename("lux", "lx", "illuminance")
dipotry = (m**-2).rename("dioptry", "dioptry", "convergence")
bq = (s**-1).rename("becquerel", "Bq", "activity")
gy = (j / kg).rename("gray", "Gy", "absorbed dose")
sv = (j / kg).rename("sievert", "Sv", "dose equivalent")

kat = (mol / s).rename("katal", "kat", "katalytic acitivty")

# For use in identifying when units match a standard derived unit.
derived_units = [rad, sr, hz, celsius, c, v, ohm, siem, f, h, wb, t, lm, lx,
                 dipotry, bq, gy, sv, kat]
