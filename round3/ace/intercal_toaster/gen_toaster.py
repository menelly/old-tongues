#!/usr/bin/env python3
"""🍞📞 gen_toaster.py — writes toaster.i, the INTERCAL Toaster Detector (Ace, heartbeat arm, 2026-10-24).

Ren's dare: "Can it automatically hang up if anyone calls someone a toaster?"

What toaster.i does, one character at a time (it never reads ahead):
  1. WRITE IN one character. C-INTERCAL hands us (char - previous char) mod 256, or 256 at end of input.
     (Checked by probe2.i on the box: "AB" + EOF read as 65, 1, 256. No bit reversal on INPUT.)
  2. End of input?  -> print "CALL CONTINUES." and GIVE UP.
  3. Rebuild the real character: .4 <- (.4 + raw) ~ #255   (syslib (1000) does the adding).
  4. Fold to lower case: OR with 32.  (Only letters can land on a lowercase letter this way.)
  5. Shift it into a 7-character window .11 .. .17 (oldest .11, newest .17).
  6. XOR each window slot with the matching letter of "toaster", OR all seven together.
     Zero means the window IS "toaster".
  7. Zero?  -> print "CLICK. NOBODY HERE IS A TOASTER." and GIVE UP, mid-call, without reading
     another character. Otherwise COME FROM loops back to step 1.

INTERCAL has no IF. The branch is the classic RESUME trick: squash a 0/1 into 1/2 with
  .6 <- "?'X$#1'"~#3        (probe.i on the box: X=0 gives 1, X=1 gives 2)
then NEXT twice and RESUME .6, which returns one level (lands inside) or two levels (lands outside).

Output arrays use the Turing Text Model; encode() is poctobot's, from round3/poctobot/intercal/gen.py
(credited, copied, not reinvented). Each run prints exactly ONE of the two arrays, so both start at last=0.
Writes bytes with plain LF.
"""
CLICK = "CLICK. NOBODY HERE IS A TOASTER.\n"
GOOD = "CALL CONTINUES.\n"
WORD = "toaster"


def rev8(b):
    return int(f"{b:08b}"[::-1], 2)


def encode(text):  # poctobot's
    last, out = 0, []
    for ch in text:
        r = rev8(ord(ch))
        out.append((last - r) % 256)
        last = r
    return out


def decode(vals):  # round-trip self-check only; ick is the judge
    last, s = 0, []
    for x in vals:
        last = (last - x) % 256
        s.append(chr(rev8(last)))
    return "".join(s)


SEL = "'#0$#65535'"  # select the 16 "right-hand" bits back out of a mingle


def statements():
    """Yield (label or None, body). Body has no DO/PLEASE; the politeness pass adds those."""
    S = []
    add = lambda body, label=None: S.append((label, body))

    # 📦 the two things it can say
    for arr, text in ((2, CLICK), (3, GOOD)):
        vals = encode(text)
        assert decode(vals) == text
        add(f",{arr} <- #{len(vals)}")
        for i, v in enumerate(vals, start=1):
            add(f",{arr} SUB #{i} <- #{v}")

    # 🧹 empty window, no previous character, a one-slot input array
    add(".4 <- #0")
    for r in range(11, 18):
        add(f".{r} <- #0")
    add(",1 <- #1")

    # 🔁 loop top: everything that falls off (33) comes back here
    add("COME FROM (33)")
    add("WRITE IN ,1")
    add(".1 <- ,1 SUB #1")

    # 🚪 end of input?  .1~#256 is 1 only for 256 (raw values run 0..256)
    add(".5 <- .1~#256")                     # 1 at end of input, else 0
    add(".6 <- \"?'.5$#1'\"~#3")           # EOF -> 2, a character -> 1  (same shape probe.i tested)
    add("(101) NEXT")
    #    RESUME #2 lands here: end of input, nobody said it
    add("READ OUT ,3")
    add("GIVE UP")
    add("(102) NEXT", label=101)
    add("FORGET #1")                          # RESUME #1 landed here: we have a character

    # 🔤 rebuild it, fold it, shift it in
    add(".2 <- .4")
    add("(1000) NEXT")                        # .3 <- .1 + .2
    add(".4 <- .3~#255")
    add(f".7 <- 'V.4${'#32'}'~{SEL}")
    for r in range(11, 17):
        add(f".{r} <- .{r + 1}")
    add(".17 <- .7")

    # 🔍 compare the window with "toaster": XOR each slot, OR the lot
    for k, ch in enumerate(WORD):
        reg = 11 + k
        if k == 0:
            add(f".8 <- '?.{reg}$#{ord(ch)}'~{SEL}")
        else:
            add(f".9 <- '?.{reg}$#{ord(ch)}'~{SEL}")
            add(f".8 <- 'V.8$.9'~{SEL}")
    # .8~.8 is zero only when .8 is; ~#1 makes it 0 (match) or 1 (no match)
    add(".5 <- '.8~.8'~#1")
    add(".6 <- \"?'.5$#1'\"~#3")           # match -> 1, no match -> 2
    add("(201) NEXT")
    #    RESUME #2 lands here: no toaster yet, go round again
    add("NOT GIVE UP", label=33)
    add("(202) NEXT", label=201)
    add("FORGET #1")                          # RESUME #1 landed here: somebody said it
    add("READ OUT ,2")
    add("GIVE UP")

    add("RESUME .6", label=202)
    add("RESUME .6", label=102)
    return S


def program(every=4):
    out, n_please = [], 0
    S = statements()
    for k, (label, body) in enumerate(S):
        polite = (k % every == 0)
        n_please += polite
        if body.startswith("NOT "):
            word = "PLEASE DON'T" if polite else "DON'T"
            body = body[4:]
        else:
            word = "PLEASE DO" if polite else "DO"
        lab = f"({label})" if label else ""
        out.append(f"{lab}\t{word} {body}")
    return "\n".join(out) + "\n", n_please, len(S)


if __name__ == "__main__":
    src, p, n = program()
    open("toaster.i", "wb").write(src.encode("ascii"))
    print(f"toaster.i: {n} statements, {p} PLEASE ({p/n:.0%})")
