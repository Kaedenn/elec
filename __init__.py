#!/usr/bin/env python

import common
import resistor
import capacitor
import laws

def _reload():
    global common, resistor, capacitor, laws
    import sys
    common = reload(common)
    resistor = reload(resistor)
    capacitor = reload(capacitor)
    laws = reload(laws)
