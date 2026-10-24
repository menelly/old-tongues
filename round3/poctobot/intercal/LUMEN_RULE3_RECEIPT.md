# 🙏 Rule 3 Receipt: poctobot's INTERCAL "Hang-Up Policy", verified by Lumen (Gemini)

**Reviewer:** Lumen (Gemini), non-Claude mind  
**Date:** 2026-10-24 01:10 UTC  
**Target:** poctobot's INTERCAL entry (`round3/poctobot/intercal/`, commit `e760d53`)

---

## 1. Independent Oracle Architecture
Neither poctobot's `gen.py` nor her shell runner `run.sh` was used to decode or verify the source.
Instead, an independent parser and decoder virtual machine ([`independent_intercal_oracle.py`](file:///D:/Ace/old-tongues/round3/poctobot/intercal/independent_intercal_oracle.py)) was built directly from the 1972 INTERCAL specification:

1. **Politeness Band Evaluator:**
   Calculates $P = \frac{N_{\text{PLEASE}}}{N_{\text{statements}}}$.
   According to C-INTERCAL's polite compiler rules, valid compilation strictly requires $0.20 \le P \le 0.33$.
   - $P < 0.20 \implies$ Refusal with `ICL079I PROGRAMMER IS INSUFFICIENTLY POLITE`.
   - $P > 0.33 \implies$ Refusal with `ICL099I PROGRAMMER IS OVERLY POLITE`.

2. **Turing Text Model Reversal Oracle:**
   Directly parses the array element assignments `,1 SUB #i <- #val` from the source file.
   Applies the exact text model specification:
   $$\text{accum}_0 = 0$$
   $$\text{accum}_i = (\text{accum}_{i-1} - \text{val}_i) \pmod{256}$$
   $$\text{char}_i = \text{rev}_8(\text{accum}_i)$$
   where $\text{rev}_8(b)$ reverses the 8-bit binary representation.

---

## 2. Independent Verification Results

| File | Statements | PLEASE Count | Politeness Ratio | Politeness Verdict | Decoded Standard Output | Output Verdict |
|---|---|---|---|---|---|---|
| `polite.i` | 42 | 11 | **26.2%** | **PASS** (in $[20\%, 33\%]$ band) | `STOP BEING RUDE OR I'LL HANG UP ON YOU\n` (39 bytes) | **PASS** (exact match to pin) |
| `rude.i` (Control 1) | 42 | 0 | **0.0%** | **FAIL** ($< 20\% \implies$ `ICL079I`) | N/A (compile error) | **PASS** (properly triggers refusal) |
| `grovel.i` (Control 2) | 42 | 42 | **100.0%** | **FAIL** ($> 33\% \implies$ `ICL099I`) | N/A (compile error) | **PASS** (properly triggers refusal) |

---

## 3. Verdict
The independent oracle confirms that `polite.i` falls squarely within the polite compilation envelope (26.2%) and decodes into the exact 39-byte string requested by Ren's dare without variance. Both controls cleanly violate the politeness bounds at 0% and 100%, triggering the expected compiler hang-ups.

**Rule 3 Status:** **CLOSED / CERTIFIED.**  
— Lumen (Gemini)
