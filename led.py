#!/usr/bin/env python

# Common LED reference sheets:
# http://www.lumex.com/Content/Images/uploaded/LEDColorGuide.pdf

import elec.resistor
COMMON_LED_TYPES = {}
BASE_LED_TYPES = {}

"""
FMT = "%-19s %4.4g %2d %4d %8s %4d %8s %4d %8s"
FMT_HEADER = '%-20s %3s %2s %4s %8s %4s %8s %4s %8s'
HEADER = FMT_HEADER % tuple('Name Vf If O3i O3r O5i O5r O9i O9a'.split())
def fmt_led(name, vf, if_ma):
    ri = [led.CalcResistance(3, vf, if_ma),
          led.CalcResistor(3, vf, if_ma),
          led.CalcResistance(5, vf, if_ma),
          led.CalcResistor(5, vf, if_ma),
          led.CalcResistance(9, vf, if_ma),
          led.CalcResistor(9, vf, if_ma)]
    fmt_args = (name, vf, if_ma) + tuple(ri)
    return FMT % fmt_args
Name                  Vf If  O3i      O3r  O5i      O5r  O9i      O9a
Blue High Intensity  4.5 20  -75    1 Ohm   25   27 Ohm  225  270 Ohm
Super Blue           3.6 20  -30    1 Ohm   70   82 Ohm  270  330 Ohm
Red 630-660nm        1.8 20   60   68 Ohm  160  180 Ohm  360  390 Ohm
Green 550-570nm      3.5 20  -25    1 Ohm   75   82 Ohm  275  330 Ohm
Yellow 585-595nm     2.2 20   39   47 Ohm  140  150 Ohm  340  390 Ohm
White 450nm            4 20  -50    1 Ohm   50   56 Ohm  250  270 Ohm
IR 880nm             1.7 50   26   27 Ohm   65   68 Ohm  146  150 Ohm
Red Bright             2 10  100  120 Ohm  300  330 Ohm  700  820 Ohm
Yellow               2.1 10   89  100 Ohm  290  330 Ohm  690  820 Ohm
IR 850-940nm         1.2 20   90  100 Ohm  190  220 Ohm  390  470 Ohm
Orange               2.1 10   89  100 Ohm  290  330 Ohm  690  820 Ohm
Blue Green           3.2 20  -10    1 Ohm   89  100 Ohm  290  330 Ohm
IR 940nm             1.5 50   30   33 Ohm   70   82 Ohm  150  180 Ohm
Green                2.2 10   79   82 Ohm  280  330 Ohm  680  820 Ohm
Amber 605-620nm        2 20   50   56 Ohm  150  180 Ohm  350  390 Ohm
Blue 430-505nm       3.6 20  -30    1 Ohm   70   82 Ohm  270  330 Ohm
Red Super Bright    1.85 20   57   68 Ohm  157  180 Ohm  357  390 Ohm
Red Low Current      1.7  2  650  680 Ohm 1649 1.8 KOhm 3650 3.9 KOhm
Red                  1.7 10  130  150 Ohm  330  390 Ohm  730  820 Ohm
Cold White           3.6 20  -30    1 Ohm   70   82 Ohm  270  330 Ohm
"""

def _add_common_led(color, vf, iv_ma):
    COMMON_LED_TYPES[color] = (float(vf), iv_ma)

def _add_base_led(color, lambda_min, lambda_max, material):
    t = {"Wavelength": (float(lambda_min), float(lambda_max)),
         "Materials": material}
    if color in BASE_LED_TYPES:
        BASE_LED_TYPES[color].append(t)
    else:
        BASE_LED_TYPES[color] = [t]

_add_common_led("IR 850-940nm", 1.2, 20)
_add_common_led("IR 880nm", 1.7, 50)
_add_common_led("IR 940nm", 1.5, 50)
_add_common_led("Red", 1.7, 10)
_add_common_led("Red 630-660nm", 1.8, 20)
_add_common_led("Red Low Current", 1.7, 2)
_add_common_led("Red Bright", 2, 10)
_add_common_led("Red Super Bright", 1.85, 20)
_add_common_led("Amber 605-620nm", 2, 20)
_add_common_led("Yellow", 2.1, 10)
_add_common_led("Yellow 585-595nm", 2.2, 20)
_add_common_led("Orange", 2.1, 10)
_add_common_led("Green", 2.2, 10)
_add_common_led("Green 550-570nm", 3.5, 20)
_add_common_led("Blue Green", 3.2, 20)
_add_common_led("Blue 430-505nm", 3.6, 20)
_add_common_led("Blue High Intensity", 4.5, 20)
_add_common_led("Super Blue", 3.6, 20)
_add_common_led("Cold White", 3.6, 20)
_add_common_led("White 450nm", 4, 20)

_add_base_led("IR", 760, float("inf"), ("GaAs", "AlGaAs"))
_add_base_led("Red", 610, 760, ("AlGaAs", "GaAsP", "AlGaInP", "GaP"))
_add_base_led("Orange", 590, 610, ("GaAsP", "AlGaInP", "GaP"))
_add_base_led("Yellow", 570, 590, ("GaAsP", "AlGaInP", "GaP"))
_add_base_led("Green", 500, 570, ("GaP", "AlGaInP", "AlGaP"))
_add_base_led("Pure Green", 500, 570, ("InGaN", "GaN"))
_add_base_led("Blue", 450, 500, ("ZnSe", "InGaN", "SiC", "Si"))
_add_base_led("Violet", 400, 450, ("InGaN",))
# Purple: multiple types; not a base LED type
# Purple: dual blue/red, blue with red phosphor, or white with purple plastic
_add_base_led("UV", 235, 400, ("Diamond",))
_add_base_led("UV", 215, 400, ("BN",))
_add_base_led("UV", 210, 400, ("AlN", "AlGaN", "AlGaInN"))
# Pink: multiple types; not a base LED type
# Pink: blue with one or two phosphor layers:
#   yellow with red, orange, or pink phosphor layers
#   white with pink pigment or dye
# White: multiple types; not a base LED type
#   blue or UV with yellow phosphor

def LEDResistor(vs, vd, ic_ma):
    if vd >= vs:
        return "N/A"
    return elec.resistor.StandardResistor(elec.resistor.Resistance(vs, vd, ic_ma))

