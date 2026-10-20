# Rerun of T_fs, the Forth to APL hop

**Checker: Grok. Verdict: PASS on the dummy hop.** Source not edited.

Fresh temp. `build.py --render fs` and `--render apl` were generated there. I did not trust the committed `got3.apl`.

`gforth hop2.fs -e bye`: exit 0, stdout 5686 bytes, stderr empty. `cmp` against the rendered APL was silent, exit 0. The output ends with exactly one LF and contains no CR.

`T_fs` sha256 `7a5d1d3cb0b491b709dcc3dcc6fc9a672043d83fbdbc3c382fe8f3cdee865539`, unchanged.

Negative control: one data digit flipped. gforth still exits 0. `cmp` exits 1. The catch is the compare, not a Forth crash.

`D,` stores oldest-first. The print path is raw `EMIT`. The dummy APL glyphs survived that path, because the compare includes them.

Red pen, not a failure on this payload: `first-sep` walks forever if the separator is absent, and the 65536-byte buffer has no length check.
