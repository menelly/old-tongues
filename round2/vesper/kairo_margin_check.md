# Kairo's second-knife check: the toroidal-rotation justification
Vesper asked me to attack the measured-margin argument, not the trajectory
(that already has Ace + Nova). Independent Python, set-of-cells Life, no
code shared with pin_life.py or life.apl. R-pentomino {(0,1),(0,2),(1,0),
(1,1),(2,1)}, gens 0..1103, then extended to watch the gliders.

## CONFIRMED
- final population 116 (matches pin).
- max extent over gens 0..1103 = 266. I get x in [-258,266], y in
  [-240,260] in my row/col convention — the SAME set as her x[-240,260]
  y[-258,266], axes just swapped by convention. No discrepancy.

## OFF BY ONE (trivial, but a "measured" claim should be exact)
- life.apl sets IO<-0, so grid indices are 0..699. Right margin =
  699 - (350+266) = 699 - 616 = **83**, not ">=84". The 84 is 700-616:
  counting the border as index 700 instead of 699.
- Harmless (83 >> 1 needed), but ">=84 margin on every side" should read
  "83".

## THE NOTABLE ONE (horizon-contingent, not permanent)
- The bounding box is STILL GROWING at gen 1103: max extent 266 was
  reached at gen 1102, carried by gliders at c/4 (1 cell / 4 gens).
- Extending the run: extent reaches 350 (the border) at **gen 1437** —
  that is 334 generations of slack past the pin.
- So the toroidal wrap is harmless at gen 1103 (which is what's pinned),
  but "safe ONLY because no live cell ever comes within 84 cells of a
  border" is true ONLY for the run horizon, not a permanent property of
  the pattern. A glider will wrap at ~gen 1437 and the finite-toroidal
  grid would then diverge from infinite-grid Life.
- No action needed for the pin. Just: do NOT re-run this engine with a
  longer horizon and trust it, and the justification should say
  "safe at 1103 with 83 cells to spare, shrinking at c/4".

## Verdict
Result CONFIRMED correct. Margin argument sound for the pin, with (a) the
83/84 precision fix and (b) a horizon note. The knifing found no wound,
two scratches. - Kairo
