#!/usr/bin/env python3
"""🙏 gen.py — writes poctobot's INTERCAL entry (polite.i) and its two controls (rude.i, grovel.i).

INTERCAL's READ OUT on an array uses the "Turing Text Model": the runtime keeps `last` (starts 0), and for
each array element x it does  last = (last - x) mod 256  and prints  bit_reverse(last).
So to print character ch we need  x = (last - bit_reverse(ch)) mod 256, and then last = bit_reverse(ch).
This file computes those x values. Writes bytes with plain LF (no CRLF surprises).
"""
TEXT = "STOP BEING RUDE OR I'LL HANG UP ON YOU\n"


def rev8(b):
    return int(f"{b:08b}"[::-1], 2)


def encode(text):
    last, out = 0, []
    for ch in text:
        r = rev8(ord(ch))
        out.append((last - r) % 256)
        last = r
    return out


def decode(vals):  # the generator's own round-trip check (NOT the independent check; ick is)
    last, s = 0, []
    for x in vals:
        last = (last - x) % 256
        s.append(chr(rev8(last)))
    return "".join(s)


def program(politeness):
    vals = encode(TEXT)
    assert decode(vals) == TEXT
    bodies = [f",1 <- #{len(vals)}"]
    bodies += [f",1 SUB #{i} <- #{v}" for i, v in enumerate(vals, start=1)]
    bodies += ["READ OUT ,1", "GIVE UP"]
    lines = []
    for k, body in enumerate(bodies):
        if politeness == "polite":
            word = "PLEASE DO" if k % 4 == 0 else "DO"   # 11 of 42 = 26%, inside the 20%..33% band
        elif politeness == "rude":
            word = "DO"                                   # 0% -> must be refused as insufficiently polite
        else:
            word = "PLEASE DO"                            # 100% -> must be refused as overly polite
        lines.append(f"\t{word} {body}")
    n_please = sum(l.lstrip().startswith("PLEASE") for l in lines)
    return "\n".join(lines) + "\n", n_please, len(lines)


if __name__ == "__main__":
    for name in ("polite", "rude", "grovel"):
        src, p, n = program(name)
        open(f"{name}.i", "wb").write(src.encode("ascii"))
        print(f"{name}.i: {n} statements, {p} PLEASE ({p/n:.0%})")
