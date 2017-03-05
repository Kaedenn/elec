#!/usr/bin/env python

def PowerOf1000(p):
    s = ''
    if p > 1000000:
        p /= 1000000.0
        s = 'M'
    elif p > 1000:
        p /= 1000.0
        s = 'K'
    return p, s

def ToMilli(base):
    return base * 1000.0

def FromMilli(milli):
    return milli / 1000.0

def Series(*vals):
    return sum(vals)

def Parallel(*vals):
    return sum(1/v for v in vals)
