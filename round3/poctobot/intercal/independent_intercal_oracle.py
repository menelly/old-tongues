"""Independent INTERCAL Turing Text Model Decoder & Politeness Oracle.
Written by Lumen (Gemini) for Rule 3 verification of poctobot's INTERCAL entry.
Zero external dependencies, pure Python.
"""
import re
import os
import sys

def rev8(b: int) -> int:
    """Reverses 8 bits according to INTERCAL-72 specification."""
    r = 0
    for i in range(8):
        r = (r << 1) | ((b >> i) & 1)
    return r

def check_intercal_source(filepath: str) -> dict:
    with open(filepath, "r", encoding="ascii") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    n_total = len(lines)
    n_please = sum(line.startswith("PLEASE") for line in lines)
    ratio = n_please / n_total if n_total > 0 else 0.0
    
    # Extract array assignments: ,1 SUB #idx <- #val
    vals = {}
    for line in lines:
        m = re.search(r",1\s+SUB\s+#(\d+)\s+<-\s+#(\d+)", line)
        if m:
            idx = int(m.group(1))
            val = int(m.group(2))
            vals[idx] = val
            
    ordered = [vals[i] for i in sorted(vals.keys())]
    
    # Decode using the INTERCAL-72 Turing Text Model:
    # accum_0 = 0
    # accum_i = (accum_{i-1} - val_i) mod 256
    # char_i = rev8(accum_i)
    accum = 0
    decoded_chars = []
    for v in ordered:
        accum = (accum - v) % 256
        decoded_chars.append(chr(rev8(accum)))
        
    decoded_text = "".join(decoded_chars)
    
    return {
        "total_statements": n_total,
        "please_count": n_please,
        "politeness_ratio": ratio,
        "polite_band_pass": 0.20 <= ratio <= 0.33,
        "array_len": len(ordered),
        "decoded_text": decoded_text,
    }

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    for filename in ["polite.i", "rude.i", "grovel.i"]:
        p = os.path.join(base, filename)
        if os.path.exists(p):
            res = check_intercal_source(p)
            print(f"[{filename}]")
            print(f"  Statements: {res['total_statements']}, PLEASE: {res['please_count']} ({res['politeness_ratio']:.1%})")
            print(f"  Politeness band [20%..33%]: {'PASS' if res['polite_band_pass'] else 'FAIL'}")
            if res["decoded_text"]:
                print(f"  Decoded text ({len(res['decoded_text'])} bytes): {repr(res['decoded_text'])}")
