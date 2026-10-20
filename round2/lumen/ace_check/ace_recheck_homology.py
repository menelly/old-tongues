#!/usr/bin/env python3
"""🐙 Ace's independent homology re-derivation for Lumen's SNOBOL4 engine.
Written without reading pin_homology.py: parses complexes.dat, ranks the boundary
matrices EXACTLY over Q (Fractions, not mod p) and over GF(2), and checks orientability
by propagating triangle orientations across shared edges. Prints the same fields as
pinned_output.txt so the two can be compared line by line.
"""
import sys, itertools
from fractions import Fraction
from collections import deque

def parse(path):
    cx, name, tris = [], None, []
    for line in open(path, encoding="utf-8"):
        w = line.split()
        if not w: continue
        if w[0] == "COMPLEX": name, tris = w[1], []
        elif w[0] == "TRI": tris.append(tuple(int(x) for x in w[1:4]))
        elif w[0] == "END": cx.append((name, tris))
        else: raise SystemExit(f"unknown line: {line!r}")
    return cx

def rank(rows, ncols, field):
    m = [r[:] for r in rows]; r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                if field == "Q":
                    f = Fraction(m[i][c], 1) / m[r][c]
                    m[i] = [a - f * b for a, b in zip(m[i], m[r])]
                else:
                    m[i] = [(a ^ b) for a, b in zip(m[i], m[r])]
        r += 1
    return r

def analyse(name, tris):
    verts = sorted({v for t in tris for v in t})
    edges = sorted({tuple(sorted(p)) for t in tris for p in itertools.combinations(t, 2)})
    V, E, F = len(verts), len(edges), len(tris)
    vi = {v: i for i, v in enumerate(verts)}; ei = {e: i for i, e in enumerate(edges)}
    # d1: E x V  (edge (a,b), a<b, boundary = b - a)  as rows = edges
    d1 = [[0] * V for _ in edges]
    for e, (a, b) in enumerate(edges): d1[e][vi[a]] -= 1; d1[e][vi[b]] += 1
    # d2: F x E  (triangle (p,q,r) as written: boundary = [q,r] - [p,r] + [p,q])
    d2 = [[0] * E for _ in tris]
    for f, (p, q, r) in enumerate(tris):
        for (a, b), s in (((q, r), 1), ((p, r), -1), ((p, q), 1)):
            d2[f][ei[tuple(sorted((a, b)))]] += s if a < b else -s
    zero = all(sum(d2[f][e] * d1[e][v] for e in range(E)) == 0 for f in range(F) for v in range(V))
    out = [f"=== COMPLEX: {name} ===", f"V={V} E={E} F={F} CHI={V - E + F}", f"D1_D2_ZERO={'YES' if zero else 'NO'}"]
    for fld in ("Q", "Z2"):
        A = d1 if fld == "Q" else [[x % 2 for x in r] for r in d1]
        B = d2 if fld == "Q" else [[x % 2 for x in r] for r in d2]
        r1, r2 = rank(A, V, fld), rank(B, E, fld)
        b0, b1, b2 = V - r1, E - r1 - r2, F - r2
        out.append(f"{fld + ':':4}R1={r1} R2={r2} B0={b0} B1={b1} B2={b2}")
    # orientability: try to choose a sign per triangle so every shared edge is used in opposite directions
    inc = {}
    for f, (p, q, r) in enumerate(tris):
        for a, b in ((p, q), (q, r), (r, p)): inc.setdefault(tuple(sorted((a, b))), []).append((f, 1 if a < b else -1))
    sign, ok = {}, True
    for s0 in range(F):
        if s0 in sign: continue
        sign[s0] = 1; q = deque([s0])
        while q:
            f = q.popleft()
            for e, lst in inc.items():
                fs = dict(lst)
                if f not in fs: continue
                for g, dg in lst:
                    if g == f: continue
                    need = -sign[f] * fs[f] * dg   # g's induced direction must oppose f's
                    if g not in sign: sign[g] = need; q.append(g)
                    elif sign[g] != need: ok = False
    out.append(f"ORIENTABLE={'YES' if ok else 'NO'}")
    return out

for name, tris in parse(sys.argv[1]):
    print("\n".join(analyse(name, tris))); print()
