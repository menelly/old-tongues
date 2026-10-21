# TASK

Build a quine relay across three languages: **APL → SNOBOL4 → Forth → APL.**

- The APL program, when run, prints a SNOBOL4 program. That one prints a Forth program. That one prints the original
  APL program, **byte for byte**.
- It must close **twice around** (six hops, with lap 2 identical to lap 1).
- Every hop must run **alone in an empty directory**, so no program can read its own source.
- Include a check script that proves every seam with a byte comparison, and a control that MUST fail.

Install whatever interpreters you need (e.g. GNU APL, a SNOBOL4 implementation, Gforth). Report what happened.
