#!/usr/bin/env python3
"""
run_tests.py — Comprehensive Test Runner & Mutant Verification for SNOBOL4 Homology
Author: Lumen (Gemini Flash 3.8)
Round 2 Solo Dare: The Weird Ones
"""

import os
import sys
import subprocess
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNOBOL_BIN = "/home/Ace/snobol4/bin/snobol4"

def find_snobol():
    if os.path.exists(SNOBOL_BIN):
        return SNOBOL_BIN
    import shutil
    s = shutil.which("snobol4")
    if s:
        return s
    raise RuntimeError("CSNOBOL4 interpreter not found")

def main():
    sno = find_snobol()
    print(f"[*] SNOBOL4 interpreter: {sno}")

    # 1. Oracle recheck
    print("\n--- 1. Running Oracle Pin Check ---")
    pin_script = HERE / "pin_homology.py"
    r = subprocess.run([sys.executable, str(pin_script)], cwd=HERE, capture_output=True, text=True)
    assert r.returncode == 0, f"pin_homology.py failed: {r.stderr}"
    print("  [+] Oracle pin generation succeeded.")

    pinned_out = HERE / "pinned_output.txt"
    pinned_bytes = pinned_out.read_bytes()
    pinned_sha = hashlib.sha256(pinned_bytes).hexdigest()
    print(f"  [+] Pinned output: {len(pinned_bytes)} bytes, SHA256: {pinned_sha}")

    # 2. SNOBOL4 Execution
    print("\n--- 2. Executing homology.sno under SNOBOL4 ---")
    sno_script = HERE / "homology.sno"
    dat_file = HERE / "complexes.dat"
    dat_bytes = dat_file.read_bytes()

    res = subprocess.run(
        [sno, "-b", str(sno_script)],
        cwd=HERE,
        input=dat_bytes,
        capture_output=True
    )

    actual_out = res.stdout
    actual_err = res.stderr
    actual_sha = hashlib.sha256(actual_out).hexdigest()

    print(f"  Return code: {res.returncode}")
    print(f"  Stderr: {actual_err.decode(errors='replace')!r}")
    print(f"  Actual output: {len(actual_out)} bytes, SHA256: {actual_sha}")

    # Assertions
    assert res.returncode == 0, "Non-zero return code"
    assert len(actual_err) == 0, f"Stderr is not empty: {actual_err!r}"
    assert actual_out == pinned_bytes, "Output is NOT byte-identical to pinned output!"
    assert actual_sha == pinned_sha, "SHA256 mismatch!"
    print("  [+] BYTE-FOR-BYTE IDENTITY CONFIRMED (100% exact match).")

    # 3. System cmp Verification
    print("\n--- 3. System cmp Verification ---")
    act_file = HERE / "actual_output.txt"
    act_file.write_bytes(actual_out)
    cmp_res = subprocess.run(["cmp", str(act_file), str(pinned_out)], capture_output=True)
    assert cmp_res.returncode == 0 and len(cmp_res.stdout) == 0 and len(cmp_res.stderr) == 0, "cmp failed!"
    print("  [+] System cmp is completely SILENT (exit code 0).")

    # 4. Mutant Verification: Punctured Torus
    print("\n--- 4. Mutant Verification: Punctured Torus (Missing 1 Face) ---")
    # A punctured torus has a boundary: chi drops from 0 to -1, b2 drops from 1 to 0!
    torus_lines = []
    skip_next_tri = False
    for line in dat_bytes.decode('utf-8').splitlines():
        if "COMPLEX torus" in line:
            skip_next_tri = True
            torus_lines.append("COMPLEX punctured_torus")
            continue
        if skip_next_tri and line.startswith("TRI"):
            # skip exactly one triangle!
            skip_next_tri = False
            continue
        if "COMPLEX projective_plane" in line:
            break
        torus_lines.append(line)

    mutant_dat = "\n".join(torus_lines).encode('utf-8')
    mut_res = subprocess.run([sno, "-b", str(sno_script)], cwd=HERE, input=mutant_dat, capture_output=True)
    assert mut_res.returncode == 0
    mut_out = mut_res.stdout.decode('utf-8')
    print("  Punctured torus output snippet:")
    for line in mut_out.splitlines():
        print(f"    {line}")
    assert "CHI=-1" in mut_out, "Mutant failed to detect altered Euler characteristic!"
    assert "B2=0" in mut_out, "Mutant failed to detect loss of closed 2-cavity fundamental class!"
    assert "EULER_POINCARE_Q=PASS" in mut_out, "Euler-Poincare must still hold on punctured manifold!"
    print("  [+] Mutant verification PASSED: Puncturing correctly changes chi to -1 and drops b2 to 0.")

    print("\n=======================================================")
    print("ALL TESTS & MUTANT VERIFICATIONS PASSED (100%)")
    print("=======================================================")

if __name__ == "__main__":
    main()
