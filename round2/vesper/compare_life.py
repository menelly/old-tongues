#!/usr/bin/env python3
"""compare_life.py — checker for Vesper's APL Game of Life engine.
Recomputes everything from pin_life.py primitives (no shared code with
the APL) and compares against the APL stdout byte stream.

Usage: python3 compare_life.py life_out.txt expected_gen1103.txt
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pin_life import step, R_PENT


def main():
    raw = open(sys.argv[1], "rb").read()
    expected = set()
    for line in open(sys.argv[2]):
        x, y = line.split()
        expected.add((int(x), int(y)))

    fails = []

    # byte discipline: exactly one trailing LF, no CR, no NUL
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        fails.append("trailing-newline discipline")
    if b"\r" in raw or b"\x00" in raw:
        fails.append("CR/NUL byte present")

    lines = raw.decode("ascii").split("\n")[:-1]
    gen_lines = [l for l in lines if l.startswith("GEN")]
    grid_start = lines.index("FINAL") + 1
    grid = lines[grid_start:]

    # GEN trajectory: 0..1103, populations recomputed independently
    if len(gen_lines) != 1104:
        fails.append(f"GEN line count {len(gen_lines)} != 1104")
    cells = R_PENT
    for g, l in enumerate(gen_lines[:1104]):
        p = l.split()
        num, pop = int(p[1]), int(p[3])
        if num != g:
            fails.append(f"GEN numbering at line {g}")
            break
        if pop != len(cells):
            fails.append(f"POP mismatch at gen {g}: apl={pop} python={len(cells)}")
            break
        cells = step(cells)

    # final grid: 700 rows of 700 chars, 0/1 only
    if len(grid) != 700 or any(len(r) != 700 for r in grid):
        fails.append("grid shape != 700x700")
    if any(c not in "01" for r in grid for c in r):
        fails.append("grid has non-01 chars")

    got = set()
    for row, r in enumerate(grid):
        for col, c in enumerate(r):
            if c == "1":
                got.add((col - 350, row - 350))

    if got != expected:
        fails.append(f"final cell set: only_apl={len(got - expected)} "
                     f"only_expected={len(expected - got)}")

    # border assertion: no live cell in the outer ring of the FINAL grid
    if any(x in (-350, 349) or y in (-350, 349) for x, y in got):
        fails.append("live cell on final border")

    if fails:
        print("COMPARE: FAIL")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("COMPARE: PASS — 1104/1104 generations' populations match the "
          "independent Python, final grid reproduces the pinned 116-cell "
          "set exactly, byte discipline clean.")


if __name__ == "__main__":
    main()
