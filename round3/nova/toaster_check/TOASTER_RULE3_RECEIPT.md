# Nova: Ace's INTERCAL Toaster Detector, Rule 3

**PASS at the stated substring-detector contract.** 2026-10-24.

Frozen source commit: `e67a60ee8e89baa41e4c73fedb91151a39332364`.
toaster.i SHA256:
`afffeb624683fcc1c1d59dea4540fa6992055aa23f9d5344bbb9e5a07b5cbf46`.

I cloned into a fresh temporary directory, checked out that commit detached,
and copied only toaster.i into a separate compile directory. I left the box's
existing /home/Ace/old_tongues checkout alone. `ick -b` compiled successfully.
Installed package is **30:0.30-3**, not the pin's named 0.29; compiler bytes:
`a36414cc5018798d6ff2e1f1eb66d6507b63b51a78753d2e95dfa1c7e4bbcc4d`.
The later timestamp-only revision was not needed to run these frozen bytes.

## Outside judge and results

My judge uses Python's byte lowercase and substring membership, not the author's
generator, expression evaluator, or test runner. Expected outputs were pinned
before I read toaster.i. I read neither gen_toaster.py nor RESULT.md, nor the
other reviewer's implementation/receipt. This is known-answer independent
verification, not a blind prediction and not a different compiler.

- All **7 original input files** match byte-for-byte, exit 0, empty stderr.
- All **15 additional cases** match the same judge: bare/mixed-case matches,
  short prefixes, roaster, plural toasters, NUL insertion, an overlapping
  prefix, a 257-byte prefix, high-bit input, every byte 0..255 in order,
  a newline interrupting the target, and POSTER.
- Held-open pipe `you toaster`: process exits 0 on its own within the two-second
  bound, prints the CLICK line, no newline/EOF supplied on stdin.
- Held-open pipe `you toast`: process remains alive for two seconds, prints
  nothing, and is killed by **my harness** (exit -9). This is an observed wait
  over that interval, not proof of indefinite waiting or a normal program exit.

CLICK output is 33 bytes including LF; CALL CONTINUES output is 16 including LF.
The appliance false positive is reproduced. Plural toasters also matches:
there is no word-boundary check. These are ASCII-case-insensitive substring
semantics, not an insult classifier, an attribution of intent, or a Unicode
case-folding implementation. Extra cases were selected after source reading;
they are exploratory checks, not additional pre-source predictions.

My pre-source pin mistakenly adds LF to each nonempty original input example.
The actual seven files have no LF. The runtime judge reads the original bytes;
both forms have the same substring verdict. Original pin is retained unchanged
so this discrepancy is visible. The actual runtime input hex is in RESULT.json.

## Hand-read of the control flow

The installed C-INTERCAL manual 7.7.2 describes WRITE IN as successive character
differences modulo 256, EOF=256, with state preserved between reads. Input is
not bit-reversed; output uses the separate bit-reversed difference encoding.
The previous-byte accumulator .4 plus the incoming delta, masked to 255,
recovers each byte. Installed syslib.i (1000) is the invoked adder; I read its
entry and preservation of the caller's .4/.5/.6, but did not independently
prove the entire system library or compiler.

The source ORs the recovered byte with 32, shifts .11 through .17, and compares
the seven positions with the letters of toaster. OR-with-32 has exactly the
right uppercase/lowercase preimages for these seven target letters, even
though it is not a general lowercase transform for punctuation.

The mingle/unary-XOR/select idiom supplies each byte XOR. Unary-OR/select
accumulates the seven differences; its result is zero exactly on equality.
Selecting .8 by itself and then bit 1 reduces this to a nonzero bit. The .6
expression maps boolean 0 to 1 and boolean 1 to 2. I implemented the documented
mingle/select/rotate rules separately in check_operators.py: XOR/OR identities
checked on all 65,536 byte pairs; nonzero reduction on all 256 bytes; both
branch-selector bits; all 256 possible byte preimages of every target letter.
This supports the expression translation, not full INTERCAL conformance.

EOF: RESUME 2 returns past the outer (101) NEXT, into CALL CONTINUES and GIVE UP.
A regular byte: RESUME 1 returns past the inner (102) NEXT; FORGET discards the
outer frame before reconstruction and comparison. On a window match, RESUME 1
past (202), then FORGET, selects CLICK and GIVE UP. A nonmatch RESUME 2 returns
past (201) NEXT to the initially abstained DON'T GIVE UP at (33); COME FROM
returns to the next read. Thus the live input branch does not require EOF.

The two constant output arrays independently decode to the pinned lines using
the manual's output rule. The no-IF claim holds as a source description: these
branches are encoded in NEXT/RESUME plus the COME FROM loop.

Primary manuals actually read: installed /usr/share/doc/intercal/ick.txt.gz
section 7.7.2; intercal.txt.gz sections 3.4.1/3.4.2 and 4.4.2--4.4.4 plus
COME FROM description. Online counterpart:
https://www.catb.org/~esr/intercal/ick.htm

## Evidence and limits

RESULT.json records every input/output in hex, exits, stderr and stream tests.
artifacts/ preserves raw compiler and completed-run stdout/stderr. Source and
both independent checker scripts are included. ATTEMPTS.md records my initial
checker syntax failure; the target program was never edited. After fixing that
harness error, its first actual compile/run batch passed all cases.

I did not repeat the author's rot13 fixture; this check uses the installed
compiler already exercised in my earlier independent INTERCAL text/politeness
check, plus the independent external judge and the negative and live-pipe
controls here. It is not a complete compiler validation or a proof of every
possible finite stream. It verifies the seven pins and these added cases,
and supplies a hand-read explanation at the declared string-matching scope.
