#!/usr/bin/env python3
"""Dummy-template harness for the SNOBOL4->Forth relay hop (Vesper+Kairo).

Implements RELAY_PLAN.md v1 mechanics with DUMMY templates so the hop can
be tested alone, before anyone's real templates exist.

Frozen facts honored here:
  SEP        = b"=====HOP=====\\n"  (each template is followed by it in B)
  B          = T_apl + SEP + T_sno + SEP + T_fs + SEP   (raw bytes)
  SNOBOL4 data line: 8 spaces + "D = D 'n n n ... '"  (20 nums, trailing
              space INSIDE the quote; last line may be short)
  Forth data line:   "n n n ... D,"  (20 nums, single spaces)
  splice     = replace the template's line that is exactly "@@\\n"

Modes:
  selftest            emulate the hop spec in Python and assert round-trip
  materialize T_SNO   write out/hop1.sno (T_SNO spliced with B) and
                      out/expected_hop2.fs (what running hop1.sno MUST print)
"""
import sys, os

SEP = b"=====HOP=====\n"
HERE = os.path.dirname(os.path.abspath(__file__))


def load_templates():
    t = {}
    for name in ("T_apl", "T_sno", "T_fs"):
        with open(os.path.join(HERE, "dummies", name + ".dum"), "rb") as f:
            t[name] = f.read()
        assert t[name].endswith(b"\n"), name + " must end with one LF"
        assert b"\n@@\n" in b"\n" + t[name], name + " needs an @@ line"
    return t


def build_B(t):
    return t["T_apl"] + SEP + t["T_sno"] + SEP + t["T_fs"] + SEP


def fmt_snobol(B):
    nums = [str(b) for b in B]
    lines = []
    for i in range(0, len(nums), 20):
        chunk = " ".join(nums[i:i + 20])
        lines.append("        D = D '" + chunk + " '")
    return "\n".join(lines) + "\n"


def fmt_forth(B):
    nums = [str(b) for b in B]
    lines = []
    for i in range(0, len(nums), 20):
        chunk = " ".join(nums[i:i + 20])
        lines.append(chunk + " D,")
    return "\n".join(lines) + "\n"


def splice(template_bytes, payload_text):
    marker = b"@@\n"
    assert template_bytes.count(marker) == 1, "exactly one @@ line required"
    return template_bytes.replace(marker, payload_text.encode("ascii"))


def selftest():
    t = load_templates()
    B = build_B(t)
    # B layout: T_apl, T_sno, T_fs -> next after T_sno is T_fs (index 2)
    data = fmt_snobol(B)
    nums = []
    for line in data.splitlines():
        inner = line[line.index("'") + 1:line.rindex("'")]
        nums.extend(int(x) for x in inner.split())
    assert bytes(nums) == B, "SNOBOL4 data format round-trips B"
    parts = B.split(SEP)
    assert parts[:3] == [t["T_apl"], t["T_sno"], t["T_fs"]] and parts[3] == b""
    expected = splice(t["T_fs"], fmt_forth(B))
    outdir = os.path.join(HERE, "out")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "expected_hop2.fs"), "wb") as f:
        f.write(expected)
    assert expected.endswith(b"\n") and not expected.endswith(b"\n\n")
    print("selftest PASS: B=%d bytes, %d data lines, expected_hop2.fs=%d bytes"
          % (len(B), len(data.splitlines()), len(expected)))


def materialize(t_sno_path):
    t = load_templates()
    B = build_B(t)
    with open(t_sno_path, "rb") as f:
        t_sno = f.read()
    hop1 = splice(t_sno, fmt_snobol(B))
    expected = splice(t["T_fs"], fmt_forth(B))
    outdir = os.path.join(HERE, "out")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "hop1.sno"), "wb") as f:
        f.write(hop1)
    with open(os.path.join(outdir, "expected_hop2.fs"), "wb") as f:
        f.write(expected)
    print("wrote out/hop1.sno (%d bytes) and out/expected_hop2.fs (%d bytes)"
          % (len(hop1), len(expected)))
    print("now: snobol4 out/hop1.sno > out/got_hop2.fs && "
          "cmp out/got_hop2.fs out/expected_hop2.fs")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "selftest":
        selftest()
    elif len(sys.argv) == 3 and sys.argv[1] == "materialize":
        materialize(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(2)
