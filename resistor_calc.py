#!/usr/bin/env python

RESISTORS = [
  '1', '2.2', '4.7', '5.6', '7.5', '8.2', '10', '15', '22', '27', '33', '39',
  '47', '56', '68', '75', '82', '100', '120', '150', '180', '220', '270',
  '330', '390', '470', '510', '680', '820', '1k', '1.5k', '2.2k', '3k',
  '3.9k', '4.7k', '5.6k', '6.8k', '7.5k', '8.2k', '10k', '15k', '22k', '33k',
  '39k', '47k', '56k', '68k', '75k', '82k', '1M', '1.5M', '2M', '3.3M',
  '4.7M', '5.6M', '10M'
]

def to_absolute(r):
  if r.endswith('k'):
    return float(r[:-1]) * 1000
  if r.endswith('M'):
    return float(r[:-1]) * 1000 * 1000
  return float(r)

ABS_RESISTORS = [to_absolute(r) for r in RESISTORS]

def series(*r):
  return sum(r)

def parallel(*r):
  return 1.0/sum(1.0/v for v in r)

def LM317_cc(mA):
  return 1.25/(mA / 1000.0)

ALL_PARALLEL = dict(
  ((r1, r2), parallel(r1, r2))
  for r1 in ABS_RESISTORS
    for r2 in ABS_RESISTORS
      if r1 >= r2)

"""
rcc = [LM317_cc(i) for i in (1, 5, 10, 15, 20, 25, 30, 50, 100, 200)]
for i in rcc:
  (r1, r2), real = best_parallel(i)
  print('%-5d -> %-5d %-5d\t%-8.6g' % (i, r1, r2, real))
"""

def best_parallel(value):
  'v(ohms) -> (r1, r2)'
  avg = lambda n1, n2: (n1+n2)/2.0
  seq = [
    (abs(v-value), abs(k[0]-k[1]), avg(k[0], k[1]), k, v)
    for k,v in ALL_PARALLEL.items()]
  eps, diff, mean, (r1, r2), real = min(seq)
  print(eps, diff, mean, r1, r2, real)
  return (r1, r2), real


