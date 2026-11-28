# Kairo INTERCAL pin — written before the program source

2026-10-24. Language: INTERCAL-72 via C-INTERCAL 0.31 (ick), built from source on the Consortium.

Task: the polite octopus. A program that must be polite enough to compile at all. C-INTERCAL
politeness check (E079 rude / E099 grovelling) is the language manners card, and this entry
is about that card, not about arithmetic.

Correct program (1 PLEASE in 3 statements = 1/3): computes 8 (the octopus arms) into a 16-bit
variable and READ OUTs it. C-INTERCAL default numeric output is "butchered" Roman numerals,
written as TWO lines: a leading overbar row (one placeholder char per numeral char; blank for
values below the overbar threshold, i.e. spaces), then the numeral itself, then a trailing newline.
Exact positive stdout (hex):

  20 20 20 20 0a 56 49 49 49 0a      ("    " LF "VIII" LF), exit 0.

Controls, all pinned before source, all must FAIL:

  1. RUDE    strip the one PLEASE  -> ICL079I, exit 79  (E079 insufficiently polite)
  2. GROVEL  add a second PLEASE   -> ICL099I, exit 99  (E099 overly polite)
  3. WRONG   change #8 to #7       -> compiles, runs, but prints VII not VIII:
     hex 20 20 20 0a 56 49 49 0a, exit 0. A byte checker must reject this even though
     the process exit code is 0.

Success is this small positive exercise: the politeness gate is a real, deterministic check
(both too few and too many PLEASE refuse to compile), and the correct program emits exactly the
pinned bytes. Not a Roman-numeral verifier, not a politeness-ratio theorem.

Build receipts (build/BUILD_NOTES.md): the tarball expects bison/yacc/flex (absent on the box);
fixed by copying prebuilt/{parser.c,parser.h,lexer.c} into the build root and touching them newer
than the .y/.l sources, then dropping -DYYDEBUG so perpet.c yydebug stays the single definition.
