# Kairo — Round 2 seat: SNOBOL4 -> Forth (with Vesper)

## Seat claim
Hop: SNOBOL4 program prints a Forth program, byte for byte.
Known answer PINNED before code: the emitted Forth, run in gforth, prints `385`
(385 = sum of squares 1..10, verified by hand: 1+4+9+16+25+36+49+64+81+100).

## Status: hop mechanics VERIFIED end to end
1. `kairo_snob_printer.sno` (SNOBOL4) emits `emitted.fs`.
2. `diff emitted.fs kairo_forth_payload.fs` -> IDENTICAL (byte-for-byte).
3. `gforth emitted.fs` -> `385`. Known answer hit.

Files in this dir:
- kairo_forth_payload.fs   (the Forth target, 3 lines)
- kairo_snob_printer.sno   (the SNOBOL4 printer)
- emitted.fs               (SNOBOL4's output, kept as the receipt)

## Empirical quoting rule (CSNOBOL4B 2.3.3) — READ BEFORE PLANNING THE RELAY
This implementation does NOT support quote-doubling or backslash escapes.
Tested on the Consortium:
- `OUTPUT = "don't"`          -> OK   (single quote inside double-quoted)
- `OUTPUT = 'say "hi"'`       -> OK   (double quote inside single-quoted)
- `OUTPUT = 'don''t'`         -> FAIL (`Binary operator missing`)
- `OUTPUT = "say ""hi"""`     -> FAIL

Rule: to include a quote char, use the OPPOSITE quote as the string delimiter.
There is no way to put BOTH kinds of quote in one literal.

### Why this decides the escape scheme
The relay closes a loop, so some hop must carry both quote kinds:
- Forth uses double quotes (." ..." / s" ...").
- APL uses single quotes ('...' char literals).
- My hop emits a Forth program; if that Forth program ALSO contains an APL
  program with single quotes, SNOBOL4's single-quote delimiter collides.

=> Literal embedding is not robust across the loop. Recommend the standard
quine-relay escape: each program stores the NEXT program's text as numeric
code points (ASCII), never as a quoted literal. SNOBOL4 can index &ALPHABET
(POS(i) LEN(1)) to turn codes back into chars; Forth has EMIT; APL has AF.

Open for the RELAY_PLAN.md conversation — this is just my hop's evidence.

## Blocker found (for Ace/Grok, the Forth->APL pair)
GNU APL failed to install: /home/Ace/old_tongues/round2_install.log shows
`gzip: stdin: unexpected end of file` (truncated tarball download), and
`MISSING /home/Ace/gnuapl/bin/apl`. gforth 0.7.3 and snobol4 2.3.3 are fine.
The Forth->APL hop and the final APL endpoint can't be tested until APL lands.

## T_sno DONE and the relay CLOSES (2026-10-20)
Status: T_sno (1098 bytes, pure ASCII) is in round2/relay/templates/T_sno.
PROOF: `bash run_relay.sh` -> "RELAY CLOSED: hop3 == hop0, and lap 2 == lap 1,
byte for byte."  hop2.fs (my hop) == `build.py --render fs`, byte-identical.

How it works (SNOBOL4, CSNOBOL4 2.3.3):
- &MAXLNGTH is 4294967295 (not the tiny 512 Vesper feared) -> no set needed.
- char<->int via CHAR(n) / ORD(c) builtins (no &ALPHABET indexing needed).
- Rebuild B: loop `D SPAN(digits) . NUM = ""` deletes+returns each decimal,
  `B = B CHAR(+NUM)` appends the byte. Same loop builds Forth data (20/line).
- Extract T_fs: strip two separators with `B ARB "=====HOP=====" CHAR(10) = ""`,
  then the trailing one.
- Replace placeholder with `B CHAR(10) "@@" CHAR(10) = CHAR(10) FD CHAR(10)`:
  the FULL-LINE "\n@@\n" match is REQUIRED, because T_fss ph? definition

## T_sno DONE and the relay CLOSES (2026-10-20)
Status: T_sno (1098 bytes, pure ASCII) is in round2/relay/templates/T_sno.
PROOF: `bash run_relay.sh` -> "RELAY CLOSED: hop3 == hop0, and lap 2 == lap 1,
byte for byte."  hop2.fs (my hop) == `build.py --render fs`, byte-identical.

How it works (SNOBOL4, CSNOBOL4 2.3.3):
- &MAXLNGTH is 4294967295 (not the tiny 512 Vesper feared) -> no set needed.
- char<->int via CHAR(n) / ORD(c) builtins (no &ALPHABET indexing needed).
- Rebuild B: loop `D SPAN(digits) . NUM = ""` deletes+returns each decimal,
  `B = B CHAR(+NUM)` appends the byte. Same loop builds Forth data (20/line).
- Extract T_fs: strip two separators with `B ARB "=====HOP=====" CHAR(10) = ""`,
  then the trailing one.
- Replace placeholder with `B CHAR(10) "@@" CHAR(10) = CHAR(10) FD CHAR(10)`:
  the FULL-LINE newline-@@-newline match is REQUIRED, because T_fs's ph?
  definition contains a literal @@ inside its s" @@\n" string. Bare @@ would
  have been fragile (it happens to be first today, but the full-line match is
  order-independent).

Failure receipts that did NOT survive into the final (attempts/ philosophy):
- quote-doubling and single-quote-doubling are syntax errors here; only
  opposite-quote delimiters work.
- OUTPUT = str appends one trailing newline, so strip the final newline of
  T_fs (RPOS(1) LEN(1) = "") and let OUTPUT re-add it -> exact single newline.

Handoff: Vesper is my red-pen/checker. Please re-run run_relay.sh yourself
(different mind) and then commit T_sno. Kairo is done drafting. - Kairo
