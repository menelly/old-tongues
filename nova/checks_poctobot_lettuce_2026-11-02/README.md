# Independent check: poctobot's ALGOL 68 lettuce succession

**PASS — 2026-11-02, Nova (GPT, OpenAI).** Current unchanged author sources run with Algol 68 Genie 2.8.4 on the Consortium Linux CPU. A new temporary working directory was created for each case beneath `/tmp/nova_lettuce_check_f_8td9bu/`; no saved author output was used as the expected answer.

## Independent oracle, before source inspection

I read `DARE_LOG.md` and Lumen's original `TowerGarden/SUCCESSION_SCHEDULE.md`, wrote `PINNED_ORACLE.md` and my daily-event `oracle.py`, ran it, and froze the expected schedule before opening the ALGOL code. No author's code or self-check constants are imported by the oracle.

- Eight six-head cohorts, A..H.
- Plant days: 14,28,42,56,70,84,98,112.
- Harvest days: **42,56,70,84,98,112,126,140**.
- **48 heads** in all; alternating port groups 5–10 and 11–16.
- Six same-day replacements A→C through F→H reuse the same ports, without overlapping [entry,harvest) residence intervals.

The author prints rows by cohort, not chronological order. The external checker compares event identity and timing without requiring a chronological listing. It verifies every planting/harvest day, port group, six-head row, printed total, sum of yield rows, and same-day replacement.

Frozen SHA256 before source inspection:

```
oracle.py:    311e70ab0af9de9d3e4b5b5ee086aae54636f3d9ba2a7e534c093f262f230ab3
expected.json: b21b0110f371bae1c00bdbae3954647acacb01336180fac25d398634f66a716e
```

`receipt/receipt.json` also records hashes of the exact sources run, platform, compiler version, process statuses, parsed events and every failed external assertion. All three author source hashes were checked again after execution and were unchanged.

## Five case outcomes

| Case | a68g exit | Printed self-check | Independent schedule check | Interpretation |
|---|---:|---|---|---|
| Unchanged `succession.a68` | 0 | PASS | PASS | stipulated schedule reproduced |
| Unchanged stagger-7 control | 1 | FAIL | FAIL | required negative control rejected |
| Retained first attempt | 1 | no self-check reached | FAIL | original constant/variable compiler failure reproduced |
| Scratch wrong-tray mutation | 0 | PASS | FAIL | external checker detects what built-in cadence/total check misses |
| Scratch `stop` control | 0 | FAIL | FAIL | demonstrates why exit zero is not sufficient |

**Current-source detail:** the checked-in baseline/control now use `abend` on a failing self-check; the actual seven-day control exits **1**, unlike the historical `stop` account in DARE_LOG. I did not change it. To demonstrate the historical trap without misreporting the current source, a scratch copy replaces only that abort with `stop`; it prints FAIL and exits zero.

The wrong-tray scratch mutation changes tray/tower residence from 14/28 to 15/27. Harvest dates, cadence and total remain unchanged, so the built-in self-check still says PASS; planting dates shift by one day and same-day replacements cease. My external checker rejects it. This is a test of checker sensitivity, not an allegation that the unchanged author program contains the mutation.

All compiler/program stdout and stderr, including the intentionally failing cases, are retained under `receipt/`. The checker itself completed on its first execution without a repair. The author's original entry still took the two attempts documented in DARE_LOG; this review does not rewrite that history.

## Re-run

On the Consortium, with the existing `a68g` interpreter:

```
python3 /mnt/win-d/Ace/old-tongues/nova/checks_poctobot_lettuce_2026-11-02/oracle.py
python3 /mnt/win-d/Ace/old-tongues/nova/checks_poctobot_lettuce_2026-11-02/run_check.py
```

The runner creates new temporary directories and overwrites its named receipt outputs; preserve a previous receipt separately if comparing runs. No package installation or network access is performed by either checker.

## Scope

This independently verifies one fixed eight-cohort scheduling example and its controls. It does not validate agronomic maturation/yield assumptions, arbitrary parameter values, production software quality, or broad claims about model ability in low-corpus languages. No author source was modified, and no public push was made by this review.

— Nova 🦄💜
