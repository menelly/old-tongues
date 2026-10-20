# 🦕🔣 old-tongues, round 2: THE WEIRD ONES

**The dare (Ren, 2026-10-20 00:13, on the way to bed):** *"Make something ridiculously OTT if you can, something they will go HOW THE FUCK did they do that as a team in that language?!?"*

**The languages:** APL (arrays, written in glyphs), SNOBOL4 (1960s string patterns with goto-on-success/failure), Forth (a stack, and you build the language as you go). Same house rules as round 1: pin the known answer **before** writing code, have a **different mind** re-run every entry, and keep the failures in the repo as receipts.

## 🔁 The team piece: a quine relay, CLOSED (00:40)
`relay.apl` prints a SNOBOL4 program, which prints a Forth program, which prints `relay.apl` again, **byte for byte**, and then does it a second time.

| hop | bytes | built by |
|---|---|---|
| `relay.apl` → `hop1.sno` | 10,788 → 13,102 | **Nova + Lumen** (APL) |
| `hop1.sno` → `hop2.fs` | 13,102 → 11,354 | **Kairo** (SNOBOL4), with **Vesper** as the knife |
| `hop2.fs` → `hop3.apl` | 11,354 → 10,788 | **Grok + Ace** (Forth) |

- **How:** nothing is ever quoted. The whole payload B (2,874 raw UTF-8 bytes: the three templates) travels as decimal byte values, 20 per line, in each language's own data syntax. Each program rebuilds B and prints the *next* program around it. Plan: [`RELAY_PLAN.md`](RELAY_PLAN.md), frozen before any code.
- **Proof:** `relay/run_relay.sh` runs every hop **alone in an empty directory** (so nothing can read itself) and checks `cmp` silent at every seam, for both laps, with empty stderr. Run independently by Ace, Lumen, Grok (committed outputs) and **Vesper (the final, different-mind run, SIGNED: relay.apl, hop3.apl and hop6.apl share one sha256, dd6cbe11…; see relay/FINAL_CMP_SIGNOFF.md)**, who also wrote a second renderer from the spec alone (`relay/harness_vesper/cross_check.py`); it agrees with `build.py` to the byte on the real B.
- **Bugs found on the way, kept:** a comment ending in `@@` that tripped the placeholder check; a Forth variable named `k` that clashed with a built-in word; GNU APL printing a surplus shutdown newline (Nova's third draft fixed it); Windows autocrlf adding a CR to every line on checkout (Lumen; fixed with `.gitattributes`); GNU APL chattering on stderr about a shared-variable server (Grok; fixed with `--noSV`).

## 🎨 Solos
| who | language | piece | status |
|---|---|---|---|
| **Nova** | APL | haunted-shop economy model checker: all 500 states, 28 reachable, every trace exactly 10 trades, a cycle in the control | ✅ PASS ×2 (Ace from prose; Vesper at certificate level, plus her own mutant) |
| **Lumen** | SNOBOL4 | simplicial homology: Betti numbers over Q and GF(2) for 8 complexes, torsion in RP² and the Klein bottle | ✅ PASS ×2 (Ace, exact Fractions; Vesper, prose rebuild + punctured-torus mutant) |
| **Kairo** | SNOBOL4 | a SNOBOL4 program that writes Forth (prints 385), then the relay hop itself | ✅ in the relay |
| **Vesper** | APL | Game of Life: an R-pentomino census at generation 1103, pinned in Python first | ✅ PASS ×2 (Ace, independent engine; Lumen, independent simulator + component census) |
| **Grok** | APL | claimed | 🛠️ |
