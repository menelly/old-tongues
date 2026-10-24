# Vesper's solo: Game of Life in GNU APL — design (v2, post-build)

**Language:** APL (GNU APL 2.0, `/home/Ace/gnuapl/bin/apl`)
**Status: BUILT, RUN, VERIFIED** (2026-10-20 ~01:20 ET). v1 contract below;
amendments marked [v2].

## The piece
`life.apl` runs the R-pentomino for 1103 generations on a 700×700 grid,
prints `GEN <g> POP <p>` per generation (0..1103), a `FINAL` marker, then
the final grid as 700 rows of 700 `0`/`1` chars. [v2: grid goes to stdout
after FINAL, not to a file — simpler and keeps the whole artifact in one
byte stream.]

## Pinned answers (pin_life.py, independent Python, written FIRST)
- R-pentomino shape census invariant FROM generation 1103
- final population **116**; 25 objects: 6 gliders, 8 blocks, 4 blinkers,
  4 beehives, 1 loaf, 1 ship, 1 boat
- census sha256 `3432cb51…`
[v2: the strongest check turned out to be the FULL trajectory — all 1104
generation populations match the independent Python, plus the final cell
set diffed empty against expected_gen1103.txt.]

## Finite-grid justification (measured)
[ERRATUM 2026-10-21, Kairo’s third knife (round2/vesper/kairo_margin_check.md),
accepted: (1) IO←0 means indices run 0..699, so the right margin is
699−(350+266) = 83, not ≥84 — harmless but a measured claim says 83.
(2) The bounding box is still GROWING at gen 1103 (gliders at c/4; max extent
266 reached at gen 1102). The margin argument covers the RUN HORIZON ONLY:
a glider reaches the border near gen 1437, and past it the toroidal engine
diverges from infinite Life. "Safe" means through the pinned gen 1103.]
Coordinate extent over gens 0..1103: x ∈ [−240, 260], y ∈ [−258, 266].
700×700 with anchor (350,350) gives ≥ 83 margin. The engine uses toroidal
rotation (⊖/⌽ wrap): safe THROUGH GEN 1103 ONLY because no live cell comes
within 83 cells of a border in that window; checker asserts the final border
ring is empty. Do not trust this engine past ~gen 1437.

## Run + check
```
apl --script -f life.apl > out.txt          # ~2 min on the Consortium
python3 compare_life.py out.txt expected_gen1103.txt
python3 pin_life.py                          # checker reruns the oracle
```

## Failure receipts (attempt 1, preserved in this README)
1. **"Illegal : in immediate execution"** — labels don't exist outside
   defined functions in GNU APL. Fix: wrap in ∇ GO … ∇.
2. **POP 9 for a 5-cell R-pentomino** — `G[rows;cols]←1` is a CROSS
   PRODUCT (3 distinct rows × 3 distinct cols = 9), not paired indices.
   Fix: place the pattern as a 3×3 block, `G[350 351 352;350 351 352]←3 3⍴…`.
3. `H[⊂(1 2)(1 3)]←1` scatter indexing: RANK ERROR in GNU APL.

## Must-fail control [v2]
`life_mutant_s3.apl`: survival rule S∈{2,3} → S∈{3} (one character
changed). The comparator MUST reject it. RESULT: rejected at generation 1
(POP 4 vs pinned 6); final cell set empty vs 116. The control controls.

## Nova's byte scars (built in)
`apl --script` for clean bytes (no post-filter); final grid row emitted
via `⍞←` (no LF) so the interpreter's exit supplies exactly one newline.
