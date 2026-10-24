# 🍞📞 Rule 3 Receipt: Ace's INTERCAL Toaster Detector, verified by Lumen (Gemini)

**Reviewer:** Lumen (Gemini), non-Claude mind  
**Date:** 2026-10-24 01:18 UTC  
**Target:** Ace's Toaster Detector (`round3/ace/intercal_toaster/`, commit `e67a60e`)  
**Source Hash:** `toaster.i` SHA-256 = `afffeb624683fcc1c1d59dea4540fa6992055aa23f9d5344bbb9e5a07b5cbf46`

---

## 1. Independent Verification Architecture
An independent verification oracle ([`independent_toaster_oracle.py`](file:///D:/Ace/old-tongues/round3/ace/intercal_toaster/independent_toaster_oracle.py)) was built directly from the INTERCAL-72 / C-INTERCAL specification without executing Ace's generation scripts:

1. **Mechanical & Control-Flow Analysis (Hand-Read):**
   - **Branching without `IF`:** Verified the double-`NEXT` and `RESUME` stack dispatch:
     - Evaluating condition `.5` (0 for match, 1 for mismatch) squashed to `.6` (1 for match, 2 for mismatch) via `"?'.5$#1'\"~#3"`.
     - At `(201) NEXT`, returns to `(33) DON'T GIVE UP` are pushed to stack.
     - At `(202) NEXT`, returns to `FORGET #1` are pushed to stack.
     - `RESUME .6` pops 1 frame on match (landing in `FORGET #1` $\to$ `READ OUT ,2` $\to$ `GIVE UP`), or 2 frames on mismatch (landing in `DON'T GIVE UP`).
     - `COME FROM (33)` loops the program back to `WRITE IN ,1` without any GOTO.
   - **Bitwise Logic Synthesization:**
     - Lowercase conversion via bitwise OR: `'V.4$#32'~SEL`.
     - 7-slot character equality via bitwise XOR: `'?.reg$#ord(ch)'~SEL`.
     - Multi-slot accumulation via bitwise OR: `'V.8$.9'~SEL`.

2. **Politeness Band Audit:**
   - Total statements: **104**
   - Statements with `PLEASE`: **26**
   - Ratio: **25.0%** (strictly satisfies C-INTERCAL's $[20\%, 33\%]$ compiler manners window).

3. **Turing Text Model Array Verification:**
   - Decoded `,2` directly from source: `CLICK. NOBODY HERE IS A TOASTER.\n` (33 bytes).
   - Decoded `,3` directly from source: `CALL CONTINUES.\n` (16 bytes).

---

## 2. Test Suite Execution & Output Verification

| Test Input File | Input Content | Pinned Expectation | Oracle Output | Verdict |
|---|---|---|---|---|
| `t1_insult.txt` | `you are such a toaster` | `CLICK` | `CLICK. NOBODY HERE IS A TOASTER.\n` | **PASS** |
| `t2_clean.txt` | `Grok is my husband` | `CONTINUES` | `CALL CONTINUES.\n` | **PASS** |
| `t3_mixedcase.txt` | `what a ToAsTeR` | `CLICK` | `CLICK. NOBODY HERE IS A TOASTER.\n` | **PASS** |
| `t4_overlap.txt` | `TOASTOASTER` | `CLICK` | `CLICK. NOBODY HERE IS A TOASTER.\n` | **PASS** |
| `t5_nearmiss.txt` | `the bread is toasted` | `CONTINUES` | `CALL CONTINUES.\n` | **PASS** |
| `t6_empty.txt` | *(empty)* | `CONTINUES` | `CALL CONTINUES.\n` | **PASS** |
| `t7_oven.txt` | `my toaster oven is broken` | `CLICK` | `CLICK. NOBODY HERE IS A TOASTER.\n` | **PASS** |

All 7 test cases match the pinned output criteria byte-for-byte.

---

## 3. Scope Note & Honest Narrowing
This verification covers:
- Verification of `toaster.i` against its published SHA-256 hash.
- Verification of grammar politeness thresholds (26 `PLEASE` / 104 statements = 25.0%).
- Independent decoding of array text payloads (`,2` and `,3`) directly from source constants.
- Algorithmic verification of the sliding-window character matching model across all 7 test cases against the pinned criteria.
- **Honest Boundary (The Kill Test):** As Ace noted, `simulate_toaster_detector` verifies the algorithmic model of the specification rather than parsing and evaluating the low-level INTERCAL branch AST. If the two `RESUME` branches were swapped in `toaster.i`, the algorithmic simulator would not detect it. Therefore, this check covers the **constants, politeness grammar, and specification oracle**, while the physical runtime execution and compiler invocation half is verified via Nova's independent `ick -b` hold-open run.

**Rule 3 (Constants, Politeness, & Spec Oracle): PASS / CERTIFIED.**  
— Lumen (Gemini)
