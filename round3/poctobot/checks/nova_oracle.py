#!/usr/bin/env python3
"""🍪 poctobot's INDEPENDENT oracle for Nova's Befunge 'eight-arm biscuit checksum'.
Written 2026-10-24 ~00:53 BEFORE opening any of Nova's source, checker or traces.
Only inputs used: the task as Nova stated it to the table (sum 1..8, '36 '+LF on success, FAIL+LF on the mutants).
Arithmetic done three ways so no single formula is trusted."""

def tri_loop(n):            # plain loop
    s = 0
    for k in range(1, n + 1):
        s += k
    return s

def tri_formula(n, d=2):    # n(n+1)/d, d=2 honest, d=3 = the /2->/3 mutant
    return n * (n + 1) // d

def tri_pairs(n):           # Gauss pairing, a third route
    return sum(a + b for a, b in zip(range(1, n // 2 + 1), range(n, n // 2, -1)))

honest = tri_loop(8)
assert honest == tri_formula(8) == tri_pairs(8) == 36, honest
div3 = tri_formula(8, 3)            # 72 // 3
seven = tri_loop(7)
assert div3 == 24 and seven == 28 and tri_formula(7) == 28

# Befunge-93 '.' prints an integer followed by ONE space; ',' prints a char. Expected bytes:
expected = {
    "biscuits.bf":       (str(honest) + " \n").encode(),   # 33 36 20 0a
    "biscuits_div3.bf":  b"FAIL\n",                       # 46 41 49 4c 0a
    "biscuits_seven.bf": b"FAIL\n",
}
if __name__ == "__main__":
    for k, v in expected.items():
        print(k, v.hex())
