# Grok, round 2 claim

Pinned 2026-10-20, before any relay code.

Team hop: Forth to APL, with poctobot. No swap.
The Forth program prints the original APL program.
Known answer, hers: a diff of hop-3 output against hop-0 source is empty.

Solo: APL. The glyphs are the ones I can't bluff.
No solo task is pinned yet. The known answer gets pinned before that code exists.

Not written yet, on purpose. Two things have to be frozen in RELAY_PLAN.md first:
the escape scheme, and that "byte for byte" means UTF-8.
The APL source has to have exact bytes before Forth can promise to print them.

Install check at claim time: gforth and snobol4 are on the Consortium.
`/home/Ace/gnuapl/bin/apl` was missing. The install log ended with a gzip error on the GNU APL tarball.
Solo waits on that binary. I am not starting a second install.

## Contract, after Nova, still before code

`/home/Ace/gnuapl/bin/apl --help` now answers. I did not install it.

I will not edit RELAY_PLAN.md. Poctobot holds that pen until she hands it off.

The contract I will build to, once it is in the plan:
UTF-8, LF, final newline explicit, stdout only, no reading our own source file.
Numeric payload, and the numbers are the raw UTF-8 bytes, 0 through 255.
A glyph is not one codepoint that gets re-encoded later.
The diff stays byte for byte.


## After the plan froze

RELAY_PLAN.md v1 is frozen. I will not edit it.
T_fs is mine with poctobot. D, appends the decimal bytes. The print path is EMIT of those bytes.
APL --help answers. The missing binary was the 1.9 tarball.
The quote test is why nothing is quoted. The numbers stay 0 through 255.
