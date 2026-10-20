#!/usr/bin/env python3
"""Cross-check: Vesper's harness renderers vs poctobot's build.py --render,
on the REAL templates. Two independent implementations of the frozen spec
must produce byte-identical known answers. Run from relay/ directory."""
import subprocess, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import harness

RELAY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDIR = os.path.join(RELAY, "templates")

t = {}
for name in ("T_apl", "T_sno", "T_fs"):
    with open(os.path.join(TDIR, name), "rb") as f:
        t[name] = f.read()

B = t["T_apl"] + harness.SEP + t["T_sno"] + harness.SEP + t["T_fs"] + harness.SEP
mine = {
    "sno": harness.splice(t["T_sno"], harness.fmt_snobol(B)),
    "fs": harness.splice(t["T_fs"], harness.fmt_forth(B)),
}

ok = True
for lang in ("sno", "fs"):
    theirs = subprocess.run(
        ["python3", os.path.join(RELAY, "build.py"), "--render", lang],
        capture_output=True).stdout
    if theirs == mine[lang]:
        print(f"{lang}: IDENTICAL ({len(theirs)} bytes)")
    else:
        ok = False
        print(f"{lang}: MISMATCH mine={len(mine[lang])} theirs={len(theirs)}")
        for i, (a, b) in enumerate(zip(mine[lang], theirs)):
            if a != b:
                print(f"  first diff at byte {i}: mine={a} theirs={b}")
                print(f"  mine   ...{mine[lang][max(0,i-30):i+30]!r}")
                print(f"  theirs ...{theirs[max(0,i-30):i+30]!r}")
                break

sys.exit(0 if ok else 1)
