#!/usr/bin/env python3
"""
test_hop0.py — End-to-end test runner for Hop 0 (APL -> SNOBOL4).
Tests Nova's T_apl_attempt1.apl against the independent oracle.
"""

import os
import subprocess
import sys
from hop0_oracle import build_B, assemble_p_apl, expected_p_sno, verify_hop0_output

def main():
    # Load Nova's T_apl_attempt1.apl
    t_apl_path = "/home/Ace/old_tongues/round2/nova/T_apl_attempt1.apl"
    if not os.path.exists(t_apl_path):
        # Fallback local path if running locally
        t_apl_path = "D:/Ace/old-tongues/round2/nova/T_apl_attempt1.apl"
    
    with open(t_apl_path, "rb") as f:
        t_apl = f.read()

    # Define dummy SNOBOL4 and Forth templates
    t_sno = (
        b"* SNOBOL4 DUMMY TEMPLATE\n"
        b"@@\n"
        b"        OUTPUT = 'HELLO FROM SNOBOL'\n"
        b"END\n"
    )

    # Note: T_fs can contain non-ASCII glyphs to stress UTF-8 payload bytes
    t_fs = (
        b"\\ FORTH DUMMY TEMPLATE WITH GLYPHS \xe2\x8d\xb5 \xe2\x8d\xb0\n"
        b"@@\n"
        b'.\" HELLO FROM FORTH\" CR\n'
        b"BYE\n"
    )

    B = build_B(t_apl, t_sno, t_fs)
    print(f"[TEST] B size: {len(B)} bytes (payload across 3 templates)")

    # Assemble P_apl
    p_apl = assemble_p_apl(t_apl, B)
    print(f"[TEST] P_apl assembled: {len(p_apl)} bytes")

    # Generate expected SNOBOL4 output from oracle
    expected = expected_p_sno(t_sno, B)
    print(f"[TEST] Expected P_sno: {len(expected)} bytes")

    # Write temporary P_apl file
    temp_p_apl = "/tmp/test_p_apl.apl"
    with open(temp_p_apl, "wb") as f:
        f.write(p_apl)

    # Run GNU APL on P_apl
    cmd = ["/home/Ace/gnuapl/bin/apl", "--script", "-f", temp_p_apl]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    actual = res.stdout

    if res.returncode != 0:
        print(f"[FAIL] APL exited with code {res.returncode}")
        print(f"STDERR:\n{res.stderr.decode('utf-8', errors='replace')}")
        sys.exit(1)

    # Verify against oracle
    matched, msg = verify_hop0_output(actual, expected)
    if matched:
        print(f"[PASS] {msg}")
    else:
        print(f"[FAIL] {msg}")
        with open("/tmp/actual_sno.txt", "wb") as f:
            f.write(actual)
        with open("/tmp/expected_sno.txt", "wb") as f:
            f.write(expected)
        print("Wrote actual to /tmp/actual_sno.txt and expected to /tmp/expected_sno.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
