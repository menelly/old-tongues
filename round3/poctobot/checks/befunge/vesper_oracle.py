#!/usr/bin/env python3
"""🌙 poctobot's oracle for Vesper's Befunge Fibonacci. Written ~01:08 BEFORE opening any of Vesper's files.
Input: only Vesper's table message ("01 01 02 03 05 08 13 21 PASS"; a one-digit mutant ends '...29 FAIL')."""
fib = [1, 1]
while len(fib) < 8:
    fib.append(fib[-1] + fib[-2])
assert fib == [1, 1, 2, 3, 5, 8, 13, 21]
honest_core = " ".join(f"{n:02d}" for n in fib) + " PASS"
print("honest stdout must START with:", repr(honest_core))
# The mutant's exact bytes can't be derived from the message alone (which digit changed is not stated).
# What CAN be pinned: its last number is 29 (not 21) and it ends in FAIL, never PASS.
print("mutant stdout must contain '29' and 'FAIL', and must NOT contain 'PASS'")
