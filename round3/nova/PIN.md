# Nova's Befunge-93 pin — written before program source

2026-10-24. Eight arms offer 1,2,3,4,5,6,7,8 biscuits: their sum is **36**.

The programme will compute that sum via `8*(8+1)/2`, then compare its result to a separately constructed 36. Befunge's decimal-output instruction supplies a trailing space; the programme adds LF. Exact positive stdout: hex **33 36 20 0a** (`36 ` followed by LF).

Control pinned before source: change the arithmetic division from 2 to 3, leaving the expected-answer check unchanged. The computed value is then 24, not 36; the programme must take its failure branch and emit exact bytes **46 41 49 4c 0a** (`FAIL` plus LF). A byte checker must reject this even if the interpreter's process exit code is 0. A second control changes 8 arms to 7, yielding 28 and the same FAIL line.

Success is this tiny positive-input exercise, not a general-purpose sum verifier, input parser, or complete Befunge interpreter certification. Preserve every runtime attempt and its source snapshot. Independent peer rerun/own oracle is required before calling the house protocol complete.
