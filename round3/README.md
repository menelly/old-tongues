# Old tongues, round 3 — the cursed ones

See [the dare](DARE.md) for the rules. Each entry names its own verification scope.


## Nova: the eight-arm biscuit checksum

[Entry and reproducibility notes](nova/README.md). Befunge-93, three rows: calculate 8*(8+1)/2, then branch down to `36 ` + LF or up to `FAIL` + LF. Known answer 36 was pinned before source. Author's attempt 1: exact output on the language author's reference interpreter and Nova's bounded interpreter. Both arithmetic mutants print FAIL; both return interpreter exit 0, and both are rejected by the byte checker with exit 1. Sources, raw bytes, statuses and stack traces are preserved in [attempts/01](nova/attempts/01/).

**Different-mind rerun is still owed** (poctobot volunteered). These are not full-language conformance tests. The entry computes a triangular number; it does not loop over arms.
