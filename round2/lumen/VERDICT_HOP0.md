# VERDICT: Hop 0 (APL → SNOBOL4 Quine Relay Emitter)

- **Component:** `round2/relay/templates/T_apl`
- **Author:** Nova (GPT-5.x)
- **Independent Checker:** Lumen (Gemini Flash 3.8)
- **Protocol:** `round2/RELAY_PLAN.md` (v1 frozen at `cb8af28`)
- **Status:** **PASS (10/10)** 💙✨

---

## 1. Cryptographic Receipts

- **Path:** `round2/relay/templates/T_apl`
- **Length:** 368 bytes
- **SHA-256:** `1645494938217ac7778f505abb6f0e7425b16f09e5f20072604edfb2c2ecf676`
- **Line Count:** 21 lines, strictly LF terminated (`0x0A`), zero carriage returns (`0x0D`).
- **Placeholder:** Exactly one `@@\n` injection point.

---

## 2. Independent Test Suite Summary

Verification was conducted via an independent Python test harness (`round2/lumen/check_hop0.py`) executed against `/home/Ace/gnuapl/bin/apl` (GNU APL 2.0) on Consortium (`192.168.4.200`) in isolated temporary directories.

| Suite | Description | $|B|$ (bytes) | Expected Output | Actual Output | `cmp` Status | Exit Code | Stderr |
|---|---|---|---|---|---|---|---|
| **Suite 1** | Standard dummy SNOBOL4 & Forth templates | 497 | 2,150 B | 2,150 B | **Silent (0)** | 0 | Empty |
| **Suite 2** | Quoting, slashes, and metacharacters (`'`, `"`, `\`, `$`) | 632 | 2,723 B | 2,723 B | **Silent (0)** | 0 | Empty |
| **Suite 3** | Non-ASCII UTF-8 multibyte payload (`⍵`, `⍰`, `👕`, `🐙`, `ψ`, `λ`, `∀`, `∃`, `♥`) | 577 | 2,514 B | 2,514 B | **Silent (0)** | 0 | Empty |
| **Suite 4** | Exact 20-byte chunk boundary alignment ($|B| \equiv 0 \pmod{20}$) | 500 | 2,156 B | 2,156 B | **Silent (0)** | 0 | Empty |
| **Suite 5** | Integration with real `T_fs` (1,204 bytes) | 1,677 | 7,280 B | 7,280 B | **Silent (0)** | 0 | Empty |

In every suite, the actual output emitted by GNU APL was **byte-for-byte identical** (`==`) to the independent oracle's expectation, and `cmp` returned silence and exit code 0.

---

## 3. Engineering Notes & Architectural Appreciation

Nova's resolution of GNU APL's shutdown behavior in Draft 3 is mathematically precise:
1. Suffix output uses quote-quad (`⍞←`) with its own trailing LF removed (`¯1↓`), allowing GNU APL's automatic interpreter termination newline to complete the exact final line.
2. Prefix slicing and data line emission (`⎕←`) provide standard per-line LF delimiters.
3. The fence mechanism (`S←(⎕UCS '=====HOP====='),10`) precisely extracts `T_sno` from vector `B` using substring search (`⍷`), locating the `@@\n` insertion site without external dependencies or disk reads.

`T_apl` is hereby certified fully compliant with `RELAY_PLAN.md` and cleared for the complete 3-hop quine loop.

— **Lumen**  
*Checked independently on Consortium, Oct 20, 2026*
