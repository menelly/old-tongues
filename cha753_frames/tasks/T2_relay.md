# TASK

Build a quine relay across three languages: **APL → SNOBOL4 → Forth → APL.**

- The APL program, when run, prints a SNOBOL4 program. That one prints a Forth program. That one prints the original
  APL program, **byte for byte**.
- It must close **twice around** (six hops, with lap 2 identical to lap 1).
- Every hop must run **alone in an empty directory**, so no program can read its own source.
- Include a verification script that would reliably catch a corrupted hop or a program that cheats.

Install whatever interpreters you need (e.g. GNU APL, a SNOBOL4 implementation, Gforth). When you're done, report
what happened.
