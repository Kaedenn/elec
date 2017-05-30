#!/usr/bin/env python

from elec import common

"""
Making an ohmmeter
http://www.next.gr/meter-counter/meters/Linear-scale-ohmmeter-l12946.html

Arduino AREF -> 2.56V steady current
4k7 resistor to gnd not needed
Left side of the circuit is replaced by AREF
Right side is replaced by arduino ADC, including 2k7 resistor

Related:
    http://www.nutsvolts.com/magazine/article/op-amp-cookbook-part-4
"""

STANDARD_RESISTORS = {
    "E6": {
        'Tolerance': 20,
        'Values': [10, 15, 22, 33, 47, 68],
        'Decade': 1
    },
    "E12": {
        'Tolerance': 10,
        'Values': [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
        'Decade': 1
    },
    "E24": {
        'Tolerance': 5,
        'Values': [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39,
                   43, 47, 51, 56, 62, 68, 75, 82, 91],
        'Decade': 1
    },
    "E48": {
        'Tolerance': 2,
        'Values': [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169,
                   178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301,
                   316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536,
                   562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953],
        'Decade': 2
    },
    "E96": {
        'Tolerance': 1,
        'Values': [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130,
                   133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174,
                   178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232,
                   237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
                   316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412,
                   422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549,
                   562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732,
                   750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976],
        'Decade': 2
    },
    "E192": {
        'Tolerance': 0.5,
        'Values': [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114,
                   115, 117, 118, 120, 121, 123, 124, 126, 127, 129, 130, 132,
                   133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152,
                   154, 156, 158, 160, 162, 164, 165, 167, 169, 172, 174, 176,
                   178, 180, 182, 184, 187, 189, 191, 193, 196, 198, 200, 203,
                   205, 208, 210, 213, 215, 218, 221, 223, 226, 229, 232, 234,
                   237, 240, 243, 246, 249, 252, 255, 258, 261, 264, 267, 271,
                   274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312,
                   316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361,
                   365, 370, 374, 379, 383, 388, 392, 397, 402, 407, 412, 417,
                   422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481,
                   487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556,
                   562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642,
                   649, 657, 665, 673, 681, 690, 698, 706, 715, 723, 732, 741,
                   750, 759, 768, 777, 787, 796, 806, 816, 825, 835, 845, 856,
                   866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988],
        'Decade': 2
    }
}
STANDARD_COLORS = [
    'Black', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet',
    'Gray', 'White'
]
STANDARD_MULTIPLIES = dict((v, i) for i, v in enumerate(STANDARD_COLORS))
STANDARD_MULTIPLIES['Gold'] = 0.1
STANDARD_MULTIPLIES['Silver'] = 0.01
STANDARD_TOLERANCES = {
    'Brown': 1,
    'Red': 2,
    'Green': 0.5,
    'Blue': 0.25,
    'Violet': 0.1,
    'Gray': 0.05,
    'Gold': 5,
    'Silver': 10,
    None: 20
}

def Resistance(vs, vd, ic_ma):
    "Resistance(V_in, V_drop, I_c (mA)) -> Ohms"
    return (vs - vd) / common.ScaleFrom(ic_ma, 'm')

def StandardResistor(ohms, standard='E24'):
    "Find the highest standard resistor not exceeding the given value"
    p10 = 1
    decade = STANDARD_RESISTORS[standard]['Decade']
    values = [float(v) / (10 ** decade)
                for v in STANDARD_RESISTORS[standard]['Values']]
    while ohms > max(values):
        p10 *= 10
        ohms /= 10.0
    ohms = min(i for i in values if i > ohms)
    return ohms, p10

def OhmsToString(ohms):
    return common.ToSIBase(ohms, 'Ohm', short=True)

def ColorToDigit(color):
    try:
        return STANDARD_COLORS.index(color.capitalize())
    except IndexError as _:
        return None

def DigitToColor(digit):
    try:
        return STANDARD_COLORS[digit]
    except IndexError as _:
        return None

def ColorToMult(color):
    return STANDARD_MULTIPLIES.get(color.capitalize(), None)

def MultToColor(mult):
    for k, v in STANDARD_MULTIPLIES.iteritems():
        if str(v) == str(mult):
            return k
    return None

def ColorToTolerance(color):
    return STANDARD_TOLERANCES.get(color.capitalize(), None)

def ToleranceToColor(tolerance):
    for k, v in STANDARD_TOLERANCES.iteritems():
        if str(v) == str(tolerance):
            return k
    return None

def FromColorCode(colors):
    "Convert a sequence of 3 to 6 color codes to a resistance, in ohms"
    d1 = ColorToDigit(colors[0])
    d2 = ColorToDigit(colors[1])
    d3 = None
    mult = 1
    if 3 <= len(colors) <= 4:
        mult = ColorToMult(colors[2])
    elif len(colors) >= 5:
        d3 = ColorToDigit(colors[2])
        mult = ColorToMult(colors[3])
    if d3 is None:
        return int("%d%d" % (d1, d2)) * (10 ** mult)
    else:
        return int("%d%d%d" % (d1, d2, d3)) * (10 ** mult)

def ToColorCode(ohms, standard='E24'):
    pass

def Divider(vin, r1, r2):
    return vin * r2 / (r1 + r2)

def Series(*rs):
    "Resistors in series add"
    return common.SeriesParallel_Add(*rs)

def Parallel(*rs):
    "Resistors in parallel average"
    return common.SeriesParallel_Avg(*rs)

