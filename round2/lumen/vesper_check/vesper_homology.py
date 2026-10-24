#!/usr/bin/env python3
"""Vesper's third-knife oracle for Lumen's homology.sno.
Built from CLAIM.md prose + complexes.dat ONLY. I did not read
pin_homology.py, run_tests.py, check_hop0.py, or homology.sno.

Conventions (mine, prose-derived):
- edges canonicalized (min,max), orientation min -> max
- d1 col [u,v]: -1 at u, +1 at v          (d1([u,v]) = v - u)
- d2 col [a,b,c]: +[b,c] -[a,c] +[a,b] with sign per canonical orientation
- ranks: exact Fraction elimination (Q) and XOR elimination (GF(2))
- orientability: independent face-orientation propagation (each interior
  edge must be traversed oppositely by its two faces), NOT read off Betti
Usage: python3 vesper_homology.py complexes.dat pinned_output.txt
"""
import sys
from fractions import Fraction


def parse(path):
    complexes, name, tris = [], None, []
    for line in open(path):
        p = line.split()
        if not p:
            continue
        if p[0] == "COMPLEX":
            name = p[1]
        elif p[0] == "TRI":
            tris.append(tuple(int(x) for x in p[1:4]))
        elif p[0] == "END" and name:
            complexes.append((name, tris))
            name, tris = None, []
    return complexes


def build(tris):
    verts = sorted({v for t in tris for v in t})
    eset = set()
    for a, b, c in tris:
        eset |= {tuple(sorted((a, b))), tuple(sorted((b, c))),
                 tuple(sorted((a, c)))}
    edges = sorted(eset)
    epos = {e: i for i, e in enumerate(edges)}
    vpos = {v: i for i, v in enumerate(verts)}
    d1 = [[0] * len(edges) for _ in verts]
    for j, (u, v) in enumerate(edges):
        d1[vpos[u]][j] = -1
        d1[vpos[v]][j] = 1
    d2 = [[0] * len(tris) for _ in edges]
    for j, (a, b, c) in enumerate(tris):
        for (x, y), s in (((b, c), 1), ((a, c), -1), ((a, b), 1)):
            e = tuple(sorted((x, y)))
            sign = s if (x, y) == e else -s
            d2[epos[e]][j] += sign
    return verts, edges, d1, d2


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def rank_q(M):
    M = [[Fraction(x) for x in row] for row in M]
    rows, cols, r = len(M), len(M[0]) if M else 0, 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def rank_gf2(M):
    M = [[x & 1 for x in row] for row in M]
    rows, cols, r = len(M), len(M[0]) if M else 0, 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][c]:
                M[i] = [a ^ b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def orientable(tris):
    """Independent: propagate face orientations; every interior edge must be
    traversed in opposite directions by its two adjacent faces."""
    from collections import defaultdict
    edge_faces = defaultdict(list)
    for i, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (c, a)):
            edge_faces[tuple(sorted(e))].append((i, e))
    assign = {}
    for start in range(len(tris)):
        if start in assign:
            continue
        assign[start] = 1
        stack = [start]
        while stack:
            f = stack.pop()
            a, b, c = tris[f]
            if assign[f] == -1:
                a, b, c = a, c, b
            dirs = {(a, b), (b, c), (c, a)}
            for e in dirs:
                nb = [g for g, _ in edge_faces[tuple(sorted(e))] if g != f]
                if len(nb) != 1:
                    continue  # boundary edge or non-manifold; skip
                g = nb[0]
                x, y, z = tris[g]
                gdirs = {(x, y), (y, z), (z, x)}
                # coherence: s_g = -nat_g(e), since e already carries f's
                # final orientation (nat_f(e) = s_f by construction).
                need = -1 if e in gdirs else 1
                if g in assign:
                    if assign[g] != need:
                        return False
                else:
                    assign[g] = need
                    stack.append(g)
    return True


def main():
    complexes = parse(sys.argv[1])
    pinned_text = open(sys.argv[2]).read()
    fails = []
    for name, tris in complexes:
        verts, edges, d1, d2 = build(tris)
        V, E, F = len(verts), len(edges), len(tris)
        chi = V - E + F
        zero = matmul(d1, d2)
        nilp = all(x == 0 for row in zero for x in row)
        r1q, r2q = rank_q(d1), rank_q(d2)
        r1z, r2z = rank_gf2(d1), rank_gf2(d2)
        bq = (V - r1q, E - r1q - r2q, F - r2q)
        bz = (V - r1z, E - r1z - r2z, F - r2z)
        ep_q = chi == bq[0] - bq[1] + bq[2]
        ep_z = chi == bz[0] - bz[1] + bz[2]
        ori = orientable(tris)

        block = pinned_text.split(f"=== COMPLEX: {name} ===")[1].split("===")[0]
        def want(key):
            line = [l for l in block.splitlines() if key in l][0]
            return line
        checks = [
            ("counts", f"V={V} E={E} F={F} CHI={chi}", want("V=")),
            ("nilpotency", f"D1_D2_ZERO={'YES' if nilp else 'NO'}",
             want("D1_D2_ZERO")),
            ("Q ranks+betti", f"R1={r1q} R2={r2q} B0={bq[0]} B1={bq[1]} B2={bq[2]}",
             want("Q:").split(":", 1)[1].strip()),
            ("Z2 ranks+betti", f"R1={r1z} R2={r2z} B0={bz[0]} B1={bz[1]} B2={bz[2]}",
             want("Z2:").split(":", 1)[1].strip()),
            ("euler-poincare",
             f"EULER_POINCARE_Q={'PASS' if ep_q else 'FAIL'} "
             f"EULER_POINCARE_Z2={'PASS' if ep_z else 'FAIL'}",
             want("EULER_POINCARE")),
            ("orientable", f"ORIENTABLE={'YES' if ori else 'NO'}",
             want("ORIENTABLE")),
        ]
        for label, mine, theirs in checks:
            if mine != theirs:
                fails.append(f"{name}/{label}: mine=[{mine}] pinned=[{theirs}]")
        print(f"{name}: V={V} E={E} F={F} chi={chi} bQ={bq} bZ={bz} "
              f"nilp={'YES' if nilp else 'NO'} orient={'YES' if ori else 'NO'}")

    if fails:
        print("\nVESPER THIRD KNIFE: FAIL")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("\nVESPER THIRD KNIFE: PASS — all 8 complexes reproduced from "
          "prose: counts, nilpotency, exact-Q and GF(2) ranks, Betti "
          "numbers, Euler-Poincare both fields, independent orientability.")


if __name__ == "__main__":
    main()
