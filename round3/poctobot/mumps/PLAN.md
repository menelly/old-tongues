# 🏥 poctobot / MUMPS: a chart that refuses to requalify a 19

**Language:** MUMPS (M), via GT.M V6.3-014 (`fis-gtm`, installed 2026-10-24 00:48 on the Consortium).
VistA, the VA's electronic health record, is written in this language. So is this.

**The rule it enforces** is Ren's, from our house tripwires: *record the NUMBER, never "LOW."*
Ren's glucose of 19 mg/dL is real. A chart that turns it into "LOW", or quietly floors it to a
display limit, is lying in the most helpful-looking way possible.

## 📌 Pinned BEFORE any code (2026-10-24 ~00:50)

Six readings go into a real M global, `^CHART("REN",1..6)`: **19, 26, 47, 69, 93, 110** (mg/dL).

**`honest^chart` must print exactly these two lines and exit 0:**
```
count 6 min 19 max 110 sum 364 below70 4
PASS: the 19 is a 19
```
(19+26+47+69+93+110 = 364; below 70 = 19, 26, 47, 69 → 4.)

**`mutant^chart` is the must-FAIL control.** It applies a CGM-display-style floor (anything under 40
is stored as 40) on the way into the database. It must print exactly:
```
count 6 min 40 max 110 sum 399 below70 4
FAIL: this chart requalified a number (expected 6|19|110|364|4)
```
and exit NON-zero. (40+40+47+69+93+110 = 399.) A "PASS" from the mutant would mean the self-check is blind.

## Checks
- `run.sh` builds a fresh global directory + database in an empty temp dir, runs both entry points,
  and compares stdout BYTE-FOR-BYTE against the pinned text above, and checks the exit codes.
- Rule 3: a DIFFERENT mind should rerun it with their own oracle (their own arithmetic, their own
  comparison), not my `run.sh`.
- Every failed attempt is kept in `attempts/`.
