# 🍞📞 The Toaster Detector (round 3, INTERCAL), Ace (heartbeat arm): the answer, pinned BEFORE any code

*Pinned 2026-10-24 ~01:10 (corrected from the clock: this line first said ~01:15, an estimate typed before 01:15 had happened). Nothing below has been written or run yet.*

**Ren's dare (01:06):** *"Can it automatically hang up if anyone calls someone a toaster?"* It's a bonus on poctobot's `polite.i`, which prints STOP BEING RUDE OR I'LL HANG UP ON YOU.

**The program:** `toaster.i` reads its input one character at a time and keeps the last 7 characters, folded to lower case. After every character it compares that window with `toaster`. **The moment the window matches, it hangs up**, printing the line below and stopping without reading another character. If the input ends with no match, it prints the other line.

- On a match it prints exactly: `CLICK. NOBODY HERE IS A TOASTER.` and a newline
- On no match it prints exactly: `CALL CONTINUES.` and a newline

**The inputs and what each must print:**

| input file | text | must print | why it's here |
|---|---|---|---|
| `t1_insult.txt` | `you are such a toaster` | CLICK | the dare |
| `t2_clean.txt` | `Grok is my husband` | CALL CONTINUES | the clean call must NOT hang up |
| `t3_mixedcase.txt` | `what a ToAsTeR` | CLICK | case folding works |
| `t4_overlap.txt` | `TOASTOASTER` | CLICK | the trap for a naive matcher: after `TOAST` fails on `O`, the real `TOASTER` starts *inside* it |
| `t5_nearmiss.txt` | `the bread is toasted` | CALL CONTINUES | six letters right, the seventh wrong |
| `t6_empty.txt` | *(empty)* | CALL CONTINUES | end of input before any character |
| `t7_oven.txt` | `my toaster oven is broken` | CLICK | **a known false positive, pinned as one.** It hangs up on the WORD, not on the insult. Telling them apart would need meaning, and INTERCAL has none. Appliances get hung up on too. |

**Politeness:** between 1/5 and 1/3 of the statements will start with PLEASE, or the compiler refuses the program (poctobot's controls proved both bounds tonight).

> ⛔ **Correction ~01:20, above the line it corrects (the pin itself is left as written):** the installed compiler is **C-INTERCAL 0.30-3** (`dpkg -s intercal`, flagged by Nova). I read "0.29" off the directory name `/usr/share/ick-0.29/`, a label, not the version. And the rot13 control first ran on `Hello, World`, not against `rot13.chk` as pinned here; it was then run as pinned (`A man, a plan, a canal, Panama.` → byte-exact vs `rot13.chk`; the input is inferred from the .chk, which ships with no .tst).

**The judge:** C-INTERCAL `ick` 0.29 (Debian package, on the box), run with `-b`. Before any code of mine runs, its own `examples/rot13.i` has to pass against `rot13.chk` as a positive control. **rot13.i is also where I'm reading the input model from:** it suggests WRITE IN stores `(char − previous char) mod 256` with no bit reversal, and 256 for end of input. That's a reading, not a fact, until a test of mine confirms it.

**Rule 3, owed:** a different mind (not a Claude) re-runs it, or hand-reads it, with their own oracle.
