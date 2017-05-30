#!/usr/bin/env python

"""
Name    Symbol: SI Unit   Symbol    Definition  Expressed as Base Units
-----------------------------------------------------------------------
Current      I: Amperes   A         SI Base     A
Charge       Q: Coulombs  C         A s         A s
Voltage      V: Volts     V         J/C         kg m^2 s^-3 A^-1
Resistance   R: Ohms      \Ohm, R   V/A         kg m^2 s^-3 A^-2
Power        P: Watt      W         V A         kg m^2 s^-3
Capacitance  C: Farads    F         C/V         kg^-1 m^-2 A^2 s^4
Inductance   L, M: Henry  H         V s/A       kg m^2 s^-2 A^-2

Energy       E: Joules    J         N m         kg m^2 s^-2
Force        F: Newtons   N         kg m/s      kg m/s

Units, as equations:
C = A s (Coulombs = Ampere-seconds)
V = J/C (Volts = Joules per Coulomb)
R = V/A (Ohms = Volts per Ampere)
W = V A (Watts = Volt-Amperes)
F = C/V (Farads = Coulombs per Volt)
H = V s/A (Henrys = Volt-seconds per Ampere)

Laws:
V = I R (Ohm's Law)
P = I V (Watt's Law)

"""

def Ohms(v=None, i=None, r=None):
    if v is None:
        return i*r
    if i is None:
        return v/r
    if r is None:
        return v/i
    return v == i*r

def Watts(p=None, i=None, v=None):
    if p is None:
        return i*v
    if i is None:
        return p/v
    if v is None:
        return p/i
    return p == i*v

