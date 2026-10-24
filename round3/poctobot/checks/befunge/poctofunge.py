#!/usr/bin/env python3
"""🐙 poctofunge.py — poctobot's OWN Befunge-93 interpreter, from the spec, for rule-3 checks.
Written 2026-10-24 ~01:08 without opening anyone else's interpreter.

80x25 torus. Stack pops from empty give 0 (the spec's behaviour; Vesper's entry relies on it).
'/' and '%' truncate toward zero like the C reference. '.' prints the number followed by ONE space.
No input is used by these tests; '&' and '~' push 0 (documented, not used).
"""
import sys

W, H = 80, 25


def run(path, max_steps=2_000_000):
    src = open(path, "rb").read().decode("latin-1").replace("\r\n", "\n").split("\n")
    grid = [[" "] * W for _ in range(H)]
    for y, line in enumerate(src[:H]):
        for x, ch in enumerate(line[:W]):
            grid[y][x] = ch
    st, out = [], []
    pop = lambda: st.pop() if st else 0
    x = y = 0
    dx, dy = 1, 0
    string_mode = False
    for _ in range(max_steps):
        c = grid[y][x]
        if string_mode:
            if c == '"': string_mode = False
            else: st.append(ord(c))
        elif c == '"': string_mode = True
        elif c.isdigit(): st.append(int(c))
        elif c in "+-*/%`":
            a, b = pop(), pop()
            if c == "+": st.append(b + a)
            elif c == "-": st.append(b - a)
            elif c == "*": st.append(b * a)
            elif c == "/": st.append(int(b / a) if a else 0)
            elif c == "%": st.append(int(b - a * int(b / a)) if a else 0)
            else: st.append(1 if b > a else 0)
        elif c == "!": st.append(0 if pop() else 1)
        elif c == ">": dx, dy = 1, 0
        elif c == "<": dx, dy = -1, 0
        elif c == "^": dx, dy = 0, -1
        elif c == "v": dx, dy = 0, 1
        elif c == "_": dx, dy = (1, 0) if pop() == 0 else (-1, 0)
        elif c == "|": dx, dy = (0, 1) if pop() == 0 else (0, -1)
        elif c == ":": v = pop(); st += [v, v]
        elif c == "\\": a, b = pop(), pop(); st += [a, b]
        elif c == "$": pop()
        elif c == ".": out.append(f"{pop()} ")
        elif c == ",": out.append(chr(pop() % 256))
        elif c == "#": x, y = (x + dx) % W, (y + dy) % H
        elif c == "g":
            gy, gx = pop(), pop()
            st.append(ord(grid[gy][gx]) if 0 <= gx < W and 0 <= gy < H else 0)
        elif c == "p":
            py, px, v = pop(), pop(), pop()
            if 0 <= px < W and 0 <= py < H: grid[py][px] = chr(v % 256)
        elif c in "&~": st.append(0)
        elif c == "?": raise SystemExit("random direction '?' met: not deterministic, refusing")
        elif c == "@": return "".join(out)
        x, y = (x + dx) % W, (y + dy) % H
    raise SystemExit("step limit hit (no '@')")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        o = run(p)
        print(f"{p}\t{o!r}\thex={o.encode('latin-1').hex()}")
