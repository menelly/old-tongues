#!/usr/bin/env python3
# toaster_decode.py — Vesper's independent decode of toaster.i's two Turing-Text arrays.
# Same model as my turing_text_check.py (from PLAN prose, not gen code); per-array parse.
import re

def bitrev8(n):
    b = 0
    for _ in range(8):
        b = (b << 1) | (n & 1)
        n >>= 1
    return b

def decode_array(path, arr):
    pat = re.compile(r'%s\s+SUB\s+#\d+\s+<-\s+#(\d+)' % re.escape(arr))
    vals = [int(m.group(1)) for line in open(path) if (m := pat.search(line))]
    out, prev = [], 0
    for v in vals:
        cur = bitrev8((bitrev8(prev) - v) % 256)
        out.append(cur)
        prev = cur
    return bytes(out)

if __name__ == '__main__':
    import sys
    for arr in [',2', ',3']:
        print(arr, '->', repr(decode_array(sys.argv[1], arr)))
