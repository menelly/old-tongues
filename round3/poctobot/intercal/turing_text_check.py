#!/usr/bin/env python3
# turing_text_check.py — Vesper's independent decode of poctobot's INTERCAL entry.
# The "Turing Text Model": each array element = (bitrev(prev_char) - bitrev(this_char)) mod 256.
# So bitrev(this) = (bitrev(prev) - element) mod 256; start with prev = NUL (0).
# Written from the PLAN.md description of the model, not from gen.py.
import re, sys

def bitrev8(n):
    b = 0
    for _ in range(8):
        b = (b << 1) | (n & 1)
        n >>= 1
    return b

def decode(path):
    vals = []
    for line in open(path):
        m = re.search(r'SUB\s+#\d+\s+<-\s+#(\d+)', line)
        if m:
            vals.append(int(m.group(1)))
    out = []
    prev = 0
    for v in vals:
        cur = bitrev8((bitrev8(prev) - v) % 256)
        out.append(cur)
        prev = cur
    return bytes(out)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        print(path, '->', repr(decode(path)))
