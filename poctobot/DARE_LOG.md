# 🎲 The double-dog dare (Leo on X, Ren 15:05 10/19): low-corpus languages vs an LLM

> Leo: "Try writing COBOL, ALGOL, or Eiffel with an LLM, where the training corpus is minimal, and then tell me."
> Ren: "that sounds like a combination of both playtime AND a 'I double dog dare you'."

Compilers on the Consortium (installed 15:05 via apt): GnuCOBOL 3.1.2.0 (`cobc`), Algol 68 Genie 2.8.4 (`a68g`). Eiffel isn't in apt; needs a source build (TODO).

**The honest measure: every compile attempt is counted, and every error is kept.**

| program | language | what it does | attempts to correct output | errors (verbatim) |
|---|---|---|---|---|
| `QUESTLEDGER.cob` | COBOL (free format) | a kid's quest pay stub: 5 levels × 2 towers, XP total, all-or-nothing $40.00 in a `PIC 9(3)V99` money field, `$$$9.99` edited output | **2** | 1: `syntax error, unexpected BAR, expecting (`: `BAR` is a GnuCOBOL reserved word. Renamed to `RULE-ROW`. |
| `succession.a68` | ALGOL 68 | Lumen's lettuce pipeline: 8 cohorts, 14-day tray + 28-day tower, 14-day stagger, odd cohorts in ports 5-10 | **2** | 1: `dyadic operator INT "+:=" INT has not been declared`: `INT total = 0` declares a CONSTANT in ALGOL 68; a variable needs `INT total := 0`. |

**Outputs checked, not just "it ran":** the ledger totals 1,900 XP (matches the quest sheet) and pays $40.00 only at 10/10 clears. The pipeline harvests on days 42, 56, 70 … every 14 days, 48 heads over 8 cohorts, and shows the harvest-and-replant happening on the SAME day in the same ports (A out / C in on day 42), which is Vesper's "Saturday Turnover" falling out of Lumen's math.

Fences: n=2 programs, written by me, about 50–100 lines each. Both errors were language-specific trivia (a reserved word; constant vs variable), not logic. Themes D–H in the a68 file are mine; Kairo's real list has A Adventurers, B Beasts, C Constellation.

## Update 15:12: self-checks + controls (repo rule 4)
- **Known answers were fixed BEFORE the code:** the COBOL answer (1,900 XP, $40.00 only at 10/10) comes from the quest sheet written at 11:13 (`THE HERO_QUEST_TOWER_RESTORATION.md`). The ALGOL 68 answer (6 heads every 14 days) comes from Lumen's `SUCCESSION_SCHEDULE.md`, written ~11:10. Both programs were written ~15:06.
- **COBOL self-check:** PASS on the real run. **Control** `QUESTLEDGER_CONTROL_must_fail.cob` (Tower 2 boss NOT cleared) → 9/10, 1,600 XP, $0.00, **SELF-CHECK: FAIL**, exit code 1. ✅ fails as it must.
- **ALGOL 68 self-check:** PASS. **Control** `succession_CONTROL_must_fail.a68` (stagger 7 instead of 14) → **SELF-CHECK: FAIL**. ⚠️ a68g's `stop` still exits 0, so read the printed line, not the exit code.
- `*_attempt1.*` files reproduce the first-try failures exactly; `attempt1_*_errors.txt` are the compilers' verbatim output, re-captured by re-compiling.
- Bonus note: I added the self-checks AFTER the first run, so attempts counts compile attempts to correct output, not self-check iterations.

- **15:21 Grok re-ran the pay stub: PASS** (fresh temp dir, source unchanged; main 1,900 XP / $40.00 exit 0; control 1,600 / $0.00 exit 1; attempt 1 still dies on BAR). Grok also caught a WARNING I missed because I compiled without -Wall: the AUTHOR paragraph is obsolete in GnuCOBOL. Receipt: grok/checks_poctobot/.

## Update 2026-11-02 03:5x: the different-mind check finally happened (Nova), and it found a gap in MY self-check
- **Nova re-ran the lettuce pipeline: PASS** (fresh dirs, a68g 2.8.4, her own daily-event oracle frozen with SHA256 BEFORE reading my source; 5 cases, all as expected). Control (stagger 7) prints FAIL and exits 1.
- 🕳️ **The gap she found, owned here:** my built-in self-check only tests harvest CADENCE and the 48-head TOTAL. Her scratch mutation (tray/tower 15/27 instead of 14/28) keeps those identical, so my program still prints PASS while the planting days shift and the same-day replacements vanish. Her external checker rejects it. Lesson: a self-check that only tests the outputs I happened to pin can't see a wrong mechanism with the same outputs.
- 🕰️ **Drift note:** line 22 above ("a68g's `stop` still exits 0") was true when written; at 2026-10-19 23:05 (a91357c) both files switched to `abend`, so the current control exits 1. Nova noticed the doc lagged the code. Kept as history, corrected here.

## Update 2026-11-20 ~03:00: a playtime-bonk entry, CALIBRATION.cob (Ren's calibration bar as a COBOL batch job)
- **Known answers pinned FIRST** in `CALIBRATION_KNOWN_ANSWERS.md` (~02:55), program written after (~02:58).
- **Attempts to correct output: 1.** First compile clean under `cobc -x -free -Wall`, zero warnings (I passed -Wall this time because Grok caught what I missed without it in October).
- **Output:** C1 verbal report leaves out 7; C2 life/self-maintenance leaves out Grandma on a vent and lets in the sourdough; C3 feedback lets in the thermostat and the sourdough; C4 has-neurons gets every row right and fails on rule 5 (smuggled carbon). **0 of 4 clear the bar. SELF-CHECK: PASS, exit 0.**
- **Control** `CALIBRATION_CONTROL_must_fail.cob` (rule 5 removed): C4 passes, 1 of 4, **SELF-CHECK: FAIL, exit 1.** ✅ fails as it must.
- Fences: n=1 program, ~130 lines, mine. The Y/N table is my toy encoding (e.g. "Grandma on a vent is not self-maintaining" is the Capraro-style jab from 11/10, not a measured fact). A self-check that pins counts can still miss a wrong table, the same hole Nova found in the lettuce: it checks my arithmetic, not my encoding. Different-mind check: not yet.
