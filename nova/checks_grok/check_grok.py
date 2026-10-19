#!/usr/bin/env python3
"""Nova's independent execution check of Grok's declared fixed-decimal task.
SPDX-License-Identifier: MIT. Does not alter the input source or its binary.
Usage: python3 check_grok.py /path/to/grok/ledger.cob
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1]).resolve()


def oracle():
    principal, dime, keep = Decimal("1000.00"), Decimal("0.10"), Decimal("0.95")
    return (principal+12*dime)*keep, principal*keep+12*dime


def build_and_run(text, root, name):
    source = root / f"{name}.cob"
    binary = root / name
    source.write_text(text, encoding="utf-8")
    command = ["cobc", "-x", "-free", "-Wall", source.name, "-o", binary.name]
    build = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=20)
    result = {"build_command": command, "build_rc": build.returncode,
              "build_stdout": build.stdout, "build_stderr": build.stderr,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
    if build.returncode == 0:
        run = subprocess.run([str(binary)], cwd=root, capture_output=True, text=True, timeout=5)
        result.update(run_rc=run.returncode, stdout=run.stdout, stderr=run.stderr)
    return result


def accepts(result, expected_main, expected_control):
    if result["build_rc"] != 0 or result.get("run_rc") != 0 or result.get("stderr"):
        return False
    lines = result["stdout"].splitlines()
    if len(lines) != 2:
        return False
    main = re.fullmatch(r"MAIN\s+(\d+\.\d{2}) PASS", lines[0])
    control = re.fullmatch(r"CONTROL\s+(\d+\.\d{2}) FAIL", lines[1])
    return bool(main and control and Decimal(main[1]) == expected_main
                and Decimal(control[1]) == expected_control and expected_main != expected_control)


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    expected_main, expected_control = oracle()
    assert expected_main == Decimal("951.14")
    assert expected_control == Decimal("951.20")
    # Narrow static source requirements of the declared task, not a general COBOL proof.
    assert re.search(r"\bCOMPUTE\b", text, re.I) is None
    assert re.search(r"\b(?:COMP-1|COMP-2|FLOAT-SHORT|FLOAT-LONG)\b", text, re.I) is None
    marker = "VALUE 951.14."
    assert text.count(marker) == 1
    mutation = text.replace(marker, "VALUE 951.20.", 1)
    with tempfile.TemporaryDirectory(prefix="nova-check-grok-") as tmp:
        root = Path(tmp)
        original = build_and_run(text, root, "grok_original")
        mutant = build_and_run(mutation, root, "grok_wrong_expected")
    passed = accepts(original, expected_main, expected_control)
    mutation_rejected = not accepts(mutant, expected_main, expected_control)
    report = {"checker": "Nova", "input_source_sha256": hashlib.sha256(raw).hexdigest(),
              "oracle_main": str(expected_main), "oracle_control": str(expected_control),
              "original": original, "original_pass": passed,
              "wrong_expected_mutation": mutant, "mutation_rejected": mutation_rejected,
              "mutation_compiles": mutant["build_rc"] == 0,
              "source_after_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    assert report["source_after_sha256"] == report["input_source_sha256"]
    (HERE/"execution_receipt.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert passed and mutation_rejected and mutant["build_rc"] == 0


if __name__ == "__main__":
    main()
