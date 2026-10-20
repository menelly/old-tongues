"""PINNED KNOWN ANSWERS for Vesper's solo APL piece, old-tongues round 2.
Language: APL (GNU APL). Piece: Game of Life engine.
This script is the INDEPENDENT pinning computation, written and run
BEFORE any APL exists. The APL engine must reproduce every pinned
number below; a checker reruns this file and diffs.

Pinned results (computed 2026-10-20, plain Python, no shared code):
  CONTROL  glider @ gen 100 : population 5, shape = start shifted (25,25)
  HEADLINE R-pentomino     : shape census invariant FROM generation 1103
           final population : 116
           objects (25)     : 6 gliders, 8 blocks, 4 blinkers,
                              4 beehives, 1 loaf, 1 ship, 1 boat
           census sha256    : 3432cb51a620a7068db5c3537e80dca7c54ff9f4
                              3eee249750c9b6dda7c64a08
(That matches the classic published R-pentomino census exactly — good,
since the APL will be checked against THIS file, not against literature.)

Glider note for the checker: glider phases 1/3 are NOT dihedral
transforms of phases 0/2 (the glider 'walks'; it does not rotate).
Detection must test both phase classes. Multiset of shape classes is
invariant per-generation after settling, even though individuals swap.
"""


def step(cells):
    from collections import Counter
    nbr = Counter()
    for x, y in cells:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    nbr[(x + dx, y + dy)] += 1
    return {c for c, n in nbr.items()
            if n == 3 or (n == 2 and c in cells)}


def components(cells):
    seen, objs = set(), []
    for c in cells:
        if c in seen:
            continue
        comp, stack = set(), [c]
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            x, y = cur
            stack += [(x + dx, y + dy) for dx in (-1, 0, 1)
                      for dy in (-1, 0, 1)
                      if (dx or dy) and (x + dx, y + dy) in cells]
        seen |= comp
        objs.append(comp)
    return objs


def canon(obj):
    pts = list(obj)
    forms = []
    for swap in (False, True):
        for sx in (1, -1):
            for sy in (1, -1):
                t = [((y if swap else x) * sx, (x if swap else y) * sy)
                     for x, y in pts]
                mx = min(p[0] for p in t)
                my = min(p[1] for p in t)
                forms.append(tuple(sorted((x - mx, y - my) for x, y in t)))
    return min(forms)


def signature(cells):
    return tuple(sorted(canon(o) for o in components(cells)))


NAMED = {
    'block':   {(0,0),(0,1),(1,0),(1,1)},
    'blinker': {(0,0),(0,1),(0,2)},
    'beehive': {(1,0),(2,0),(0,1),(3,1),(1,2),(2,2)},
    'ship':    {(0,0),(1,0),(0,1),(2,1),(1,2),(2,2)},
    'boat':    {(0,0),(1,0),(0,1),(2,1),(1,2)},
    'loaf':    {(1,0),(2,0),(0,1),(3,1),(1,2),(3,2),(2,3)},
}
NAMED_C = {canon(v): k for k, v in NAMED.items()}
_G0 = {(1,0),(2,1),(0,2),(1,2),(2,2)}
GLIDER_PHASES = {canon(_G0), canon(step(_G0))}

GLIDER = _G0
R_PENT = {(1,0),(2,0),(0,1),(1,1),(1,2)}

if __name__ == "__main__":
    import hashlib
    from collections import Counter

    # CONTROL: glider translates (1,1) per 4 gens; pop stays 5
    g = GLIDER
    for _ in range(100):
        g = step(g)
    ok = g == {(x + 25, y + 25) for x, y in GLIDER} and len(g) == 5
    print("CONTROL glider@100 pop=5 shifted (25,25):", "PASS" if ok else "FAIL")

    # HEADLINE: R-pentomino
    cells = R_PENT
    sigs = {0: signature(cells)}
    for gen in range(1, 1121):
        cells = step(cells)
        sigs[gen] = signature(cells)
    settle = next(g0 for g0 in range(0, 1112)
                  if all(sigs[g0] == sigs[g0 + d] for d in range(1, 9)))
    objs = components(cells)
    names = Counter()
    for o in objs:
        c = canon(o)
        if c in GLIDER_PHASES:
            names['glider'] += 1
        elif c in NAMED_C:
            names[NAMED_C[c]] += 1
        else:
            names['UNKNOWN'] += 1
    h = hashlib.sha256(
        repr(sorted(canon(o) for o in objs)).encode()).hexdigest()
    print("settle generation:", settle, "(pinned: 1103)")
    print("final population:", len(cells), "(pinned: 116)")
    print("census:", dict(sorted(names.items())))
    print("census sha256:", h)
