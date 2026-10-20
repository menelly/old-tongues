"""Ace's independent check of Vesper's APL Life (2026-10-20). NO code shared with pin_life.py or compare_life.py.

Reads the APL stdout, recomputes the R-pentomino on an unbounded set-based board (my own step), and compares
every GEN line's population plus the final 0/1 grid (after FINAL) as a cell set, up to translation.
"""
import sys
from collections import Counter

def step(cells):
    n = Counter((x + dx, y + dy) for x, y in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    return {c for c, k in n.items() if k == 3 or (k == 2 and c in cells)}

def norm(cells):
    mx = min(x for x, _ in cells); my = min(y for _, y in cells)
    return {(x - mx, y - my) for x, y in cells}

raw = open(sys.argv[1], 'rb').read()
lines = raw.decode('ascii').split('\n')
if lines[-1] == '':
    lines = lines[:-1]
gens = [l for l in lines if l.startswith('GEN')]
grid = lines[lines.index('FINAL') + 1:]

# R-pentomino, the standard one:  .XX / XX. / .X.
cells = {(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)}
bad = []
for g in range(1104):
    p = gens[g].split()
    if int(p[1]) != g or int(p[3]) != len(cells):
        bad.append((g, gens[g], len(cells)))
        if len(bad) > 3:
            break
    if g < 1103:
        cells = step(cells)

apl_final = {(c, r) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '1'}
print('GEN lines:', len(gens), '| population mismatches:', len(bad), bad[:2])
print('final pop: mine', len(cells), '| APL', len(apl_final))
print('final cell sets equal up to translation:', norm(cells) == norm(apl_final) if apl_final else 'APL grid empty')
print('mine stable at 1103 -> 1104 pop:', len(step(cells)), '(gliders keep moving, so pop stays 116, not the set)')
