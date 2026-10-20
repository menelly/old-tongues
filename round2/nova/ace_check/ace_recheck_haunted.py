#!/usr/bin/env python3
"""🐙 Ace's independent re-derivation of Nova's haunted economy, written from CLAIM.md's
PROSE ONLY (I did not open her oracle or checker first). Prints the same summary facts so
they can be compared against KNOWN_ANSWERS.json and against her APL run.

Economy: 24 cash, 3 torches, 4 turnips in total. State = what the PLAYER holds; the shop
holds the rest. Trades: buy torch 5, sell torch 3, buy turnip 3, sell turnip 1.
Needs seller stock and payer funds; no borrowing.
"""
import json, sys
from collections import deque

CASH, TOR, TUR = 24, 3, 4

def trades(s, torch_resale):
    c, t, u = s
    out = []
    if t < TOR and c >= 5:              out.append((c - 5, t + 1, u))            # buy torch (shop has stock, I can pay)
    if t > 0 and CASH - c >= torch_resale: out.append((c + torch_resale, t - 1, u))  # sell torch (shop can pay)
    if u < TUR and c >= 3:              out.append((c - 3, t, u + 1))            # buy turnip
    if u > 0 and CASH - c >= 1:         out.append((c + 1, t, u - 1))            # sell turnip
    return [x for x in out if x != s]

def analyse(torch_resale):
    states = [(c, t, u) for c in range(CASH + 1) for t in range(TOR + 1) for u in range(TUR + 1)]
    all_edges = sum(len(trades(s, torch_resale)) for s in states)
    start = (12, 0, 0)
    dist = {start: 0}; q = deque([start]); redges = 0
    while q:
        s = q.popleft()
        for n in trades(s, torch_resale):
            redges += 1
            if n not in dist: dist[n] = dist[s] + 1; q.append(n)
    reach = set(dist)
    terminals = sorted(s for s in reach if not trades(s, torch_resale))
    # cycle check + longest path by DFS colouring on the reachable subgraph
    sys.setrecursionlimit(10000)
    colour, longest, cyc = {}, {}, [False]
    def dfs(s):
        colour[s] = 1; best = 0
        for n in trades(s, torch_resale):
            if colour.get(n) == 1: cyc[0] = True; continue
            if colour.get(n) != 2: dfs(n)
            best = max(best, 1 + longest.get(n, 0))
        colour[s] = 2; longest[s] = best
    dfs(start)
    layers = {}
    for d in dist.values(): layers[str(d)] = layers.get(str(d), 0) + 1
    return {"all_states": len(states), "all_edges": all_edges, "reachable_states": len(reach),
            "reachable_edges": redges, "terminals": [list(t) for t in terminals],
            "shortest_layers": dict(sorted(layers.items(), key=lambda kv: int(kv[0]))),
            "maximum_trace_length": None if cyc[0] else longest[start], "reachable_cycle": cyc[0],
            "rank_drops_by_one_everywhere": all((s[0] + 4*s[1] + 2*s[2]) - (n[0] + 4*n[1] + 2*n[2]) == 1
                                                for s in reach for n in trades(s, torch_resale))}

print(json.dumps({"original_resale_3": analyse(3), "control_resale_5": analyse(5)}, indent=1))
