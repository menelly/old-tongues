#!/usr/bin/env python3
"""
hop0_oracle.py — Independent test fixture and reference oracle for Hop 0 (APL -> SNOBOL4).
Author: Lumen (Gemini Flash 3.8)
Team: Nova & Lumen (Hop 0: APL -> SNOBOL4)
Protocol: round2/RELAY_PLAN.md (FROZEN v1)
"""

import sys
from typing import List, Tuple

SEP = b"=====HOP=====\n"
PLACEHOLDER = b"@@\n"

def format_apl_data_lines(b_bytes: bytes) -> str:
    """Format bytes as APL data lines:
    B<-⍬ (empty vector)
    B<-B,20 numbers...
    """
    nums = list(b_bytes)
    lines = []
    lines.append("B\u2190\u237c\n")  # B <- ⍬ (U+237C ZILDE empty vector)
    for i in range(0, len(nums), 20):
        chunk = nums[i:i+20]
        chunk_str = " ".join(str(n) for n in chunk)
        lines.append(f"B\u2190B,{chunk_str}\n")
    return "".join(lines)

def format_snobol_data_lines(b_bytes: bytes) -> str:
    """Format bytes as SNOBOL4 data lines:
    8 leading spaces, D = D 'n n n ... ' (trailing space inside quote)
    """
    nums = list(b_bytes)
    lines = []
    lines.append("        D = ''\n")
    for i in range(0, len(nums), 20):
        chunk = nums[i:i+20]
        chunk_str = " ".join(str(n) for n in chunk) + " "
        lines.append(f"        D = D '{chunk_str}'\n")
    return "".join(lines)

def build_B(t_apl: bytes, t_sno: bytes, t_fs: bytes) -> bytes:
    """Join templates with SEP."""
    return t_apl + SEP + t_sno + SEP + t_fs + SEP

def assemble_p_apl(t_apl: bytes, B: bytes) -> bytes:
    """Inject B as APL data lines into T_apl at @@ line."""
    if PLACEHOLDER not in t_apl:
        raise ValueError("T_apl missing @@\\n placeholder")
    apl_data = format_apl_data_lines(B).encode('utf-8')
    prefix, suffix = t_apl.split(PLACEHOLDER, 1)
    return prefix + apl_data + suffix

def expected_p_sno(t_sno: bytes, B: bytes) -> bytes:
    """Inject B as SNOBOL4 data lines into T_sno at @@ line."""
    if PLACEHOLDER not in t_sno:
        raise ValueError("T_sno missing @@\\n placeholder")
    sno_data = format_snobol_data_lines(B).encode('utf-8')
    prefix, suffix = t_sno.split(PLACEHOLDER, 1)
    return prefix + sno_data + suffix

def verify_hop0_output(actual_output: bytes, expected_output: bytes) -> Tuple[bool, str]:
    if actual_output == expected_output:
        return True, f"PERFECT MATCH ({len(actual_output)} bytes, exact UTF-8 / LF match)"
    
    diff_idx = -1
    min_len = min(len(actual_output), len(expected_output))
    for i in range(min_len):
        if actual_output[i] != expected_output[i]:
            diff_idx = i
            break
    if diff_idx == -1:
        diff_idx = min_len
    
    return False, (
        f"MISMATCH at byte {diff_idx}: "
        f"actual len={len(actual_output)}, expected len={len(expected_output)}. "
        f"Actual near diff: {actual_output[max(0, diff_idx-20):diff_idx+20]!r}, "
        f"Expected near diff: {expected_output[max(0, diff_idx-20):diff_idx+20]!r}"
    )

if __name__ == "__main__":
    print("hop0_oracle module loaded successfully.")
