from .main import BaseUnit, DerivedUnit


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


# Physical constants, defined by their units
hbar = a**2 * s**4 / m**3 / kg
ħ = hbar

epsilon_0 = a**2 * s**4 / m**3 / kg
ϵ_0 = epsilon_0

mu_0 = m * kg / s**2 / a**2
μ_0 = mu_0


base_units = [kg, s, k, a, mol,cd, m]

derived_units = [rad, sr, hz, celsius, c, v, ohm, siem, f, h, wb, t, lm, lx,
                 dipotry, bq, gy, sv, kat]

constants = [hbar, epsilon_0, mu_0]

units = base_units + derived_units + constants


