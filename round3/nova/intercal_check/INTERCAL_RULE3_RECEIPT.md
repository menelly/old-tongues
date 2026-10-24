# Nova: independent INTERCAL text decode and compiler rerun

2026-10-24. Scope: poctobot's three literal-array programs, not Kairo's separate entry.

**PASS.** In three fresh temporary directories, installed C-INTERCAL `ick -b`
compiled `polite.i`, whose executable exited 0 and printed the pinned 39 bytes
with empty stderr. `rude.i` failed compilation with exit 79 / ICL079I;
`grovel.i` failed with exit 99 / ICL099I. Neither control produced an executable.
Raw compiler streams and runtime streams are retained beside RESULT.json.

The independent literal-array decoder reconstructs the requested sentence plus
LF from all three sources. It uses the Turing Tape output rule in the installed
C-INTERCAL manual section 7.7.2: begin at state zero; subtract each array value
modulo 256; reverse the resulting eight bits to obtain the output byte.
Primary manual online: https://www.catb.org/~esr/intercal/ick.htm
The online fetch failed (502); the installed manual supplied the rule actually read.

`PIN_BEFORE_SOURCE.json` fixes the expected bytes and decoding rule before .i
files were fetched/read. The decoder implementation was written after reading
the positive source. This is an independent implementation with known answers,
not a blind prediction. I did not open or run gen.py, run.sh, Lumen's decoder,
or Lumen's receipt. Each source has 42 statements and PLEASE counts 11/0/42.
This verifies a constant encoded message and compiler politeness gates, not
a Toaster Detector, text understanding, or runtime detection of rudeness.

Installed package: `intercal 30:0.30-3`.
Compiler /usr/bin/ick SHA256:
`a36414cc5018798d6ff2e1f1eb66d6507b63b51a78753d2e95dfa1c7e4bbcc4d`.
Source and output hashes/hex are in RESULT.json.

## Preserved setup errors and correction

- An ssh grep command lost quoting: `grep: output: No such file or directory`.
  Replaced by copying installed manual bytes through subprocess.
- First local decoding of those manual bytes as UTF-8 raised UnicodeDecodeError
  on byte 0xa9; Latin-1 decoding recovered the text. No source or program altered.
- `ick --help` is unsupported and exited 1; its usage output confirmed -b.
- My commentary prematurely claimed a length discrepancy. Before source read,
  the Python byte pin showed 38 visible characters plus LF = 39, agreeing with
  PLAN.md. I corrected the claim immediately. No discrepancy remains.
- All three actual compilation/runtime checks passed on their first attempt.
