#!/usr/bin/env python

SI_PREFIXES = [
    # Letter, Name, Scale
    ['f', 'Femto', -15],
    ['p', 'Pico', -12],
    ['n', 'Nano', -9],
    ['u', 'Micro', -6],
    ['m', 'Milli', -3],
    ['', '', 0],
    ['k', 'Kilo', 3],
    ['K', 'Kilo', 3],
    ['M', 'Mega', 6],
    ['G', 'Giga', 9],
    ['T', 'Tera', 12],
    ['P', 'Peta', 15]
]
STANDARD_PREFIXES = dict((l, (n, s)) for (l, n, s) in SI_PREFIXES)
def _check_base(b):
    if b not in STANDARD_PREFIXES:
        msg = 'Base "%s" not known; use one of %s'
        bases = [p[0] for p in SI_PREFIXES]
        raise ValueError(msg % (b, bases))

def ToSIBase(num, unit='', short=False):
    "Convert number to a standard prefix notation, optionally using short notation"
    for letter, name, scale in reversed(SI_PREFIXES):
        prefix = letter if short else name
        if num >= 10**scale:
            return '%g %s%s' % (ScaleTo(num, letter), prefix, unit)
    # Reachable if number is too small
    return ('%g %s' % (num, unit)).strip()

def Scale(number, frombase, tobase):
    "Scale from a specific base to another specific base ('' is 10^0)"
    _check_base(frombase)
    _check_base(tobase)
    fromexp = STANDARD_PREFIXES[frombase][1]
    toexp = STANDARD_PREFIXES[tobase][1]
    return float(number) * (10**(toexp-fromexp))

def ScaleFrom(number, frombase):
    "Scale from a specific base to exp 10^0"
    # FIXME: Why does this have to be backwards?
    return Scale(number, '', frombase)

def ScaleTo(number, tobase):
    "Scale from exp 10^0 to a specific base"
    # FIXME: Why does this have to be backwards?
    return Scale(number, tobase, '')

def SeriesParallel_Add(*vs):
    return sum(vs)

def SeriesParallel_Avg(*vs):
    return 1.0/sum(1.0/v for v in vs)
