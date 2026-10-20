⍝ life.apl — Vesper's old-tongues round 2 solo: Game of Life in GNU APL.
⍝ Pins in pin_life.py (written FIRST, independent Python):
⍝   R-pentomino census invariant FROM gen 1103, final population 116,
⍝   25 objects: 6 gliders 8 blocks 4 blinkers 4 beehives 1 loaf 1 ship 1 boat.
⍝ Grid 700x700, anchor (350,350) 0-indexed = pin origin. Extent over the
⍝ run measured x[-240,260] y[-258,266]: >=84 margin on every side, so the
⍝ toroidal rotation below can never create a spurious birth.
⍝ Receipts from attempt 1: labels need a defined function in GNU APL, and
⍝ G[rows;cols] is a CROSS PRODUCT, not paired indices (POP 9 taught me).
⎕IO←0
⎕PW←10000
∇ GO;G;GEN;S;I
G←700 700⍴0
⍝ R-pentomino as a 3x3 pattern (avoids the cross-product trap):
⍝   .XX / XX. / .X.
G[350 351 352;350 351 352]←3 3⍴0 1 1 1 1 0 0 1 0
GEN←0
⎕←'GEN ',(⍕GEN),' POP ',⍕+/,G
LP:
→(GEN≥1103)/FIN
S←(¯1⊖G)+(1⊖G)+(¯1⌽G)+(1⌽G)+(¯1⊖¯1⌽G)+(¯1⊖1⌽G)+(1⊖¯1⌽G)+(1⊖1⌽G)
G←(S=3)∨G∧S=3
GEN←GEN+1
⎕←'GEN ',(⍕GEN),' POP ',⍕+/,G
→LP
FIN:
⎕←'FINAL'
I←0
ROWLP:
→(I≥699)/LASTROW
⎕←'01'[G[I;]]
I←I+1
→ROWLP
LASTROW:
⍝ Nova's shutdown trick: quote-quad adds no LF; the interpreter's exit LF
⍝ terminates the last row, so stdout ends with exactly one newline.
⍞←'01'[G[699;]]
∇
GO
)OFF
