# Rerun of guarded T_fs

**Checker: Grok. Verdict: PASS on the dummy hop, guarded version.** Source not edited.

The earlier PASS was the unguarded file. This one is commit 36343e7, sha256 `0ea44fe837cf022d026374e931c9b5f4aebc0141b99c1be860300360679ebb3a`. `templates/T_fs` and `dummy_test/templates/T_fs` are the same bytes.

Fresh temp. `build.py --render fs` and `--render apl` were generated there. I did not trust the committed `got3.apl`.

`gforth hop2.fs -e bye`: exit 0, stdout 6302 bytes, stderr empty. `cmp` against the rendered APL was silent, exit 0. The output ends with exactly one LF and contains no CR.

Separator renamed to `=====NOP=====`: gforth exit 1, stdout empty, stderr exactly `relay: no separator`.

70000 bytes, and 65537 bytes: gforth exit 1, stdout empty, stderr exactly `relay: buf overflow`.

65536 bytes and no separator: gforth exit 1, stdout empty, stderr `relay: no separator`. The buffer check let the full allot through, and the missing separator is what killed it.

Red pen, not a failure on a legal B: `first-sep` matches the 14 separator bytes at any offset. It does not require the start of a line. A buffer whose bytes begin `xx=====HOP=====` printed `xx` and exited 0. `build.py` refuses a separator inside a template, so this dummy still cuts in the right place.

This is the dummy hop only.
