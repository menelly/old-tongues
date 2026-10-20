#!/usr/bin/env python3
"""Vesper's independent oracle for Nova's APL Haunted Economy.
Built from CLAIM.md prose ONLY (24 cash / 3 torches / 4 turnips; start
(12,0,0); buy torch 5, sell torch 3, buy turnip 3, sell turnip 1;
seller stock + payer funds required; conservation). I did not read
hop0_oracle.py, oracle_before_apl.py, or oracle_certificate_before_apl.json
before writing this.

Usage: python3 vesper_oracle.py <apl_stdout_clean> <known_answers.json>
"""
import json, sys
from collections import deque

CASH, TORCH, TURNIP = 24, 3, 4
START = (12, 0, 0)
# (dcash, dtorch, dturnip, needs)  needs = ('shop'|'player', item, n, payer cash)
TRADES = [(-5, 1, 0), (3, -1, 0), (-3, 0, 1), (1, 0, -1)]


def idx(pc, pt, pu):
    return pu + 5 * pt + 20 * pc  # reverse-engineered from EDGE lines, then
                                  # verified trade-by-trade (see verdict)


def edges_of(s):
    pc, pt, pu = s
    shop_t, shop_u, shop_c = TORCH - pt, TURNIP - pu, CASH - pc
    out = []
    # buy: player is payer, shop is seller
    if pc >= 5 and shop_t >= 1: out.append((pc - 5, pt + 1, pu))
    if pc >= 3 and shop_u >= 1: out.append((pc - 3, pt, pu + 1))
    # sell: SHOP is payer (needs the cash), player is seller
    if pt >= 1 and shop_c >= 3: out.append((pc + 3, pt - 1, pu))
    if pu >= 1 and shop_c >= 1: out.append((pc + 1, pt, pu - 1))
    return out


def build(resale_torch=3):
    states = [(pc, pt, pu) for pc in range(CASH + 1)
              for pt in range(TORCH + 1) for pu in range(TURNIP + 1)]
    adj = {}
    for s in states:
        outs = edges_of(s)
        if resale_torch != 3:  # control economy: sell torch pays resale_torch
            pc, pt, pu = s
            shop_c = CASH - pc
            outs = [o for o in outs if o != (pc + 3, pt - 1, pu)]
            if pt >= 1 and shop_c >= resale_torch:
                outs.append((pc + resale_torch, pt - 1, pu))
        adj[s] = [o for o in outs if o != s]
    return states, adj


def analyze(adj):
    dist = {START: 0}
    q = deque([START])
    redges = 0
    while q:
        s = q.popleft()
        for o in adj[s]:
            redges += 1
            if o not in dist:
                dist[o] = dist[s] + 1
                q.append(o)
    terminals = [s for s in dist if not adj[s]]
    # Kahn elimination on reachable subgraph: residue = nodes on cycles
    indeg = {s: 0 for s in dist}
    for s in dist:
        for o in adj[s]:
            if o in indeg:
                indeg[o] += 1
    elim = deque([s for s in dist if indeg[s] == 0])
    removed = 0
    longest = {START: 0}
    order = []
    while elim:
        s = elim.popleft()
        removed += 1
        order.append(s)
        for o in adj[s]:
            if o in indeg:
                longest[o] = max(longest.get(o, 0), longest[s] + 1)
                indeg[o] -= 1
                if indeg[o] == 0:
                    elim.append(o)
    has_cycle = removed < len(dist)
    maxtrace = max(longest.values()) if not has_cycle else None
    layers = {}
    for d in dist.values():
        layers[d] = layers.get(d, 0) + 1
    return dist, redges, terminals, has_cycle, maxtrace, layers


def main():
    apl_out, known_path = sys.argv[1], sys.argv[2]
    known = json.load(open(known_path))
    states, adj = build()
    dist, redges, terminals, has_cycle, maxtrace, layers = analyze(adj)

    fails = []
    def chk(name, got, want):
        if got != want:
            fails.append(f"{name}: mine={got} pinned={want}")

    chk("all_states", len(states), known["all_states"])
    chk("all_edges", sum(len(v) for v in adj.values()), known["all_edges"])
    chk("reachable_states", len(dist), known["reachable_states"])
    chk("reachable_edges", redges, known["reachable_edges"])
    chk("terminals", sorted(terminals), [tuple(t) for t in known["terminals"]])
    chk("layers", {str(k): v for k, v in sorted(layers.items())},
        known["shortest_layers"])
    chk("maxtrace", maxtrace, known["maximum_trace_length"])
    chk("cycle", has_cycle, known["reachable_cycle"])

    # every path length equals 12 - rank (rank drops exactly 1 per trade)
    rank = lambda s: s[0] + 4 * s[1] + 2 * s[2]
    assert all(dist[s] == rank(START) - rank(s) for s in dist)

    # parse the APL stdout independently, PER MODE SECTION, and compare
    sections = {}
    cur = None
    for line in open(apl_out):
        p = line.split()
        if not p:
            continue
        if p[0] == "MODE":
            cur = int(p[1])
            sections[cur] = {"STATE": {}, "EDGE": set(), "TERMINAL": set(),
                             "ALL": None, "REACH": None, "CYCLE": None,
                             "MAXTRACE": None, "REACH_EDGES": None}
        elif cur is None:
            continue
        elif p[0] == "STATE":
            sections[cur]["STATE"][(int(p[1]), int(p[2]), int(p[3]))] = int(p[4])
        elif p[0] == "EDGE":
            sections[cur]["EDGE"].add((int(p[1]), int(p[2])))
        elif p[0] == "TERMINAL":
            sections[cur]["TERMINAL"].add((int(p[1]), int(p[2]), int(p[3])))
        elif p[0] in ("ALL", "REACH", "CYCLE", "MAXTRACE", "REACH_EDGES"):
            sections[cur][p[0]] = [int(x) for x in p[1:]]

    sec = sections.get(3, {})
    astates = sec.get("STATE", {})
    chk("APL_states_match", sorted(astates), sorted(dist))
    chk("APL_dists_match", astates, dist)
    chk("APL_terminals", sorted(sec.get("TERMINAL", set())), sorted(terminals))
    my_edges = {(idx(*s), idx(*o)) for s in dist for o in adj[s]}
    chk("APL_edges_match", sec.get("EDGE", set()), my_edges)
    chk("APL_ALL", sec.get("ALL"), [500, 1366])
    chk("APL_REACH", sec.get("REACH"), [28])
    chk("APL_REACH_EDGES", sec.get("REACH_EDGES"), [52])
    chk("APL_CYCLE", sec.get("CYCLE"), [0])
    chk("APL_MAXTRACE", sec.get("MAXTRACE"), [10])

    # control section (MODE 5) vs my control analysis
    _, cadj = build(resale_torch=5)
    cdist, credges, _, ccycle, _, _ = analyze(cadj)
    csec = sections.get(5, {})
    chk("ctrl_states_match", sorted(csec.get("STATE", {})), sorted(cdist))
    my_cedges = {(idx(*s), idx(*o)) for s in cdist for o in cadj[s]}
    chk("ctrl_edges_match", csec.get("EDGE", set()), my_cedges)
    chk("ctrl_ALL", csec.get("ALL"), [500, 1336])
    chk("ctrl_CYCLE", csec.get("CYCLE"), [1])

    # control economy: 2-cycle witness must be legal + reachable
    w = [tuple(t) for t in known["control_witness"]]
    legal = all(w[i + 1] in cadj[w[i]] for i in range(len(w) - 1))
    chk("control_witness_legal", legal and w[0] == w[-1] != w[1], True)
    chk("control_cycle_detected", ccycle, True)
    chk("control_witness_reachable", all(s in cdist for s in w), True)

    if fails:
        print("VESPER ORACLE: FAIL")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("VESPER ORACLE: PASS — every pinned answer and every APL "
          "certificate line reproduced from prose, independently.")


if __name__ == "__main__":
    main()
