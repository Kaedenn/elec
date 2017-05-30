#!/usr/bin/env python

import math
from elec import common
from elec import laws

def Parallel(*cs):
    "Capacitors in parallel add"
    return common.SeriesParallel_Add(*cs)

def Series(*cs):
    "Capacitors in series average"
    return common.SeriesParallel_Avg(*cs)

def Impedance(c, freq=60):
    """
    Calculate the impedance given the specified capacitance
    Z = 1/Cs = 1/(C * Hz * 2PI)
    """
    return 1/(c * freq * 2 * math.pi)

def InvImpedance(impedance, freq=60):
    """
    Calculate the capacitance giving the specified impedance
    C = 1/(Z*Hz*2PI)
    """
    return 1/(impedance * freq * 2 * math.pi)

def GetDropper(vf, current, freq=60):
    """
    Find an adequate dropper capacitor for a given Vf and If
    usage:
        v_f = 5 # 5V
        i_f = elec.common.ScaleFrom(20, 'm') # 20mA
        elec.common.ToSIBase(elec.common.GetDropper(v_f, i_f)
    """
    return InvImpedance(laws.Ohms(v=vf, i=current), freq=freq)
