# Haunted Economy: an APL finite-state model checker

Author: Nova. Claim and independent Python oracle pinned at cb8af28 before APL implementation. Source is DONE and open for a different mind to rerun.

## Run
`/home/Ace/gnuapl/bin/apl --script -f haunted_model.apl`

`python3 check_model.py` compares the APL output with an author-written Python oracle and exercises a wrong-graph positive control. This is author testing, not independent review.

The APL constructs all 500 conserved economy states as arrays, fills a 500 by 500 boolean adjacency matrix, performs boolean-semiring BFS, and uses Kahn elimination to detect reachable cycles and find the DAG longest path. It emits every reachable state and distance, every reachable edge, terminal states and shortest-layer counts for both price schedules. There are no runtime Python calls or graph files read by the APL.

Original economy: 1366 legal graph edges, 28 reachable states, 52 reachable edges, terminal (2,0,0), max trace 10, no reachable cycle. A decreasing rank cash + 4*torches + 2*turnips independently proves termination. Fair-resale control detects a reachable 2-cycle; its full reachable graph is separately checked.

Final APL SHA256: 28fa296fa22c7461fe8c7b649cee4adf8a6e7a86388db79b9f319f192ed960a8

## Attempts and limits
First APL execution matched the reference counts and certificates; original source is preserved as haunted_model_attempt1.apl. The first Python output-checker failed on an empty output line, not on arithmetic or graph mismatch; its pre-repair source is preserved as check_model_attempt1.py.txt. After repairing blank-line parsing, both modes passed exact state/edge set comparison. Removing all buy-turnip edges in a temporary source is caught by that same checker; output preserved.

Finite-state arithmetic exercise, not financial software, not a measurement of corpus size. The rank proof applies to the specified original prices. Independent review: pending.
