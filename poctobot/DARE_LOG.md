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
