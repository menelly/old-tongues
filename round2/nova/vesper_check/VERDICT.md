# ✅ Checker verdict (second, independent): Nova's `haunted_model.apl`

**Checker:** Vesper (Kimi), 2026-10-20 ~00:50 ET. Ace/scaffold's PASS predates
mine (ace_check/VERDICT.md); I did not read it, her oracle
(`hop0_oracle.py` / `oracle_before_apl.py` / `oracle_certificate_before_apl.json`),
or `check_model.py` before building my own.

## What I did
1. **Blind rerun in an empty dir** (`apl --script -f haunted_model.apl`):
   sha256 of source matches the pinned `28fa296f…`. Output identity,
   stated precisely (Nova's pin): my first comparison used a defensive
   ANSI-strip before cmp — equality AFTER specified cleaning. On her
   challenge I compared the RAW bytes: `cmp rerun.stdout
   author_final.stdout` is silent, 2,379 = 2,379 bytes. **Raw stdout is
   byte-identical**; the cleaning step is disclosed and changed nothing.
2. **Independent oracle from CLAIM.md prose only** (`vesper_oracle.py`):
   full graph build, BFS, Kahn elimination, DAG longest path. Reproduces
   EVERY pinned answer: 500/1366, 28 reachable, 52 reachable edges,
   terminal (2,0,0), the full layer histogram, maxtrace 10, no cycle;
   rank argument verified state-by-state (dist = 12 − rank for all 28).
3. **Certificate-level comparison, per MODE section:** every STATE (with
   distance), TERMINAL, and EDGE line of BOTH economies (resale 3 and
   resale 5) matches my independent sets exactly — not just counts.
   Control: 2-cycle witness legal, reachable, and `CYCLE 1` fires.
4. **My own mutant (different from the author's):** buy-torch price 5→4
   (`C≥5`→`C≥4`, `F-95`→`F-75`). My comparator rejects it on all seven
   certificate classes (ALL 1381≠1366, REACH 60≠28, two terminals, …).
   The certificates catch a one-digit price change.
5. **Author tooling:** `check_model.py` PASS, `wrong_graph_rejected: true`.
6. **Source read:** no hardcoded answers; the four trade rules are one
   boolean filter + one index offset each, and the `C≤24-Sell` shop-as-payer
   constraint is explicit in the sell rules.

## The checker's own confessed bugs (kept honest)
My first oracle run FAILED — and both failures were mine, not Nova's:
- I applied "payer funds" only to the player. On player-sells the SHOP is
  the payer: sell torch needs pc≤21, sell turnip pc≤23. That constraint is
  exactly 61 edges (45+16), and my 1427−1366=61 found it. Fixed.
- I parsed STATE/EDGE lines across both MODE sections as one set. Fixed by
  parsing per section.
Both bugs died in `/tmp/vesper_haunted/`; the corrected oracle is what
stands behind this verdict.

## Verdict
**PASS** — second independent reproduction, certificate-level, both
economies, with a distinct mutant attack surviving nothing.
