"""Nova's MUMPS expected bytes, from PLAN alone; written before chart/run.sh read."""
from pathlib import Path
import json

readings = (19, 26, 47, 69, 93, 110)
floor = tuple(max(40, value) for value in readings)

def summary(values):
    # A separate Python reduction, not a call to the M self-check.
    total = 0
    low = 0
    for value in values:
        total += value
        if value < 70: low += 1
    return len(values), min(values), max(values), total, low

honest, mutant = summary(readings), summary(floor)
assert honest == (6, 19, 110, 364, 4)
assert mutant == (6, 40, 110, 399, 4)
assert mutant[3] - honest[3] == (40-19) + (40-26) == 35

def line(stats):
    n, lo, hi, total, low = stats
    return f'count {n} min {lo} max {hi} sum {total} below70 {low}\n'

expected = {
    'honest': (line(honest) + 'PASS: the 19 is a 19\n').encode('ascii'),
    'mutant': (line(mutant) + 'FAIL: this chart requalified a number (expected 6|19|110|364|4)\n').encode('ascii'),
}

if __name__ == '__main__':
    payload = dict(basis='PLAN.md and public task only; chart.m/run.sh not yet read',
                   readings=readings, floor=floor, honest=honest, mutant=mutant,
                   expected_hex={k:v.hex() for k,v in expected.items()}, exit_codes={'honest':0,'mutant':1})
    print(json.dumps(payload, indent=2))
