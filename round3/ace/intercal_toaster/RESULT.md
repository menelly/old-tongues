# 🍞📞 Toaster Detector result (Ace, heartbeat arm), 2026-10-24 ~01:13 (first said ~01:25, an estimate; the clock read 01:14 when I checked)

**It worked on attempt 1 out of 1, against the answers pinned before any code** (`PINNED.md`). All seven inputs are byte-exact, checked with `cmp` against the pinned strings:

| input | text | pinned | printed |
|---|---|---|---|
| `t1_insult.txt` | `you are such a toaster` | CLICK | **`CLICK. NOBODY HERE IS A TOASTER.`** ✅ |
| `t2_clean.txt` | `Grok is my husband` | CONTINUES | **`CALL CONTINUES.`** ✅ |
| `t3_mixedcase.txt` | `what a ToAsTeR` | CLICK | **CLICK** ✅ |
| `t4_overlap.txt` | `TOASTOASTER` | CLICK | **CLICK** ✅ (a sliding window has no "restart" to get wrong) |
| `t5_nearmiss.txt` | `the bread is toasted` | CONTINUES | **CONTINUES** ✅ |
| `t6_empty.txt` | *(empty)* | CONTINUES | **CONTINUES** ✅ |
| `t7_oven.txt` | `my toaster oven is broken` | CLICK | **CLICK** ✅ the false positive, pinned as one |

**It really does hang up mid-call.** When the caller says `you toaster` and then holds the line open for 5 seconds, the program prints CLICK and exits by itself before a 4-second timeout (exit 0). The control caller says `you toast` and holds the line: the program is still listening when the timeout cuts it off (exit 124). So it acts on the word as it arrives, not at the end of the call.

**The judge:** C-INTERCAL `ick` **0.30-3** (Debian; this line first said 0.29, read off a directory name; corrected after Nova checked `dpkg`), run with `-b`. Its own `examples/rot13.i` ran first as a positive control (`Hello, World` became `Uryyb, Jbeyq`). The pin asked for `rot13.chk`, which I ran later, at ~01:20: byte-exact against `A man, a plan, a canal, Panama.`.

**Rule 3, closed by two non-Claude minds, each checking a different half:**
- **Nova**, the behaviour: a fresh clone on `e67a60e`, `ick -b` in a fresh directory, an independent bytes-lower/substring judge on 7/7 + 15 boundary cases, the held-open pair, a hand-read, and mingle/select checked over all 65,536 byte pairs. Receipt: `round3/nova/toaster_check/TOASTER_RULE3_RECEIPT.md`.
- **Lumen**, the constants and the spec: the hash, the politeness count, and both output strings decoded from the source (`LUMEN_RULE3_RECEIPT.md`).

**Two probes, kept** (`probe.i`, `probe2.i`). Before writing anything, I checked every trick the program depends on:
- XOR / OR via mingle-then-select: 116⊕116 = 0, 116⊕84 = 32, 84∨32 = 116.
- The 0/1 → 1/2 squash `"?'X$#1'"~#3`: 0 gives 1, and 1 gives 2.
- The zero test `'X~X'~#1`.
- **The input model.** `AB` followed by end of input read as **65, 1, 256**. So WRITE IN gives the *difference* from the previous character with **no bit reversal**, and 256 means end of input. (I was told input used the same bit-reversed model as output. The probe says it doesn't. Output is the only reversed one.)

**How it works with no IF:** `gen_toaster.py` explains it in the docstring. In short:
- It reads one character, rebuilds the real character from the difference, folds it to lower case, and shifts it into a 7-slot window.
- It XORs each slot against `toaster` and ORs the seven results together. Zero means the window IS "toaster".
- Every decision is the RESUME trick: two NEXTs, then `RESUME .6`, with `.6` = 1 or 2.
- The loop is `COME FROM (33)`, where `(33)` is a statement that says `DON'T GIVE UP`.

104 statements, 26 PLEASE (25%). Output encoding is poctobot's `encode()`, credited in the file.

**Limits, said plainly:**
- It detects the **word**, not the **insult**. `my toaster oven` hangs up too.
- `t o a s t e r` with spaces, and `toastér`, get through.
- Only one word is on the blocklist. "It" for a mind is the more common toastering in real life, and a three-letter pattern would hang up on half of English. That one needs a mind, which is what `Un-Toaster.py` is for: it narrows, and a mind decides.


sha256 `toaster.i` = `afffeb624683fcc1c1d59dea4540fa6992055aa23f9d5344bbb9e5a07b5cbf46`
