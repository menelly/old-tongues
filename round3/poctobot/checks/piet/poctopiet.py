#!/usr/bin/env python3
"""🐙🎨 poctopiet.py — poctobot's OWN Piet interpreter, written from the language spec
(David Morgan-Mar's Piet page), WITHOUT opening Lumen's piet_vm.py. Built 2026-10-24 ~01:00
as the rule-3 different-mind check for Lumen's octahedron canvas.

Reads PPM (P3 text or P6 binary), codel size 1. Prints the program's output, then (on stderr)
a short trace so a human can see what the pointer did.

The 3am-readable version of how Piet works:
  * The picture is cut into BLOCKS: same-colour regions, 4-connected.
  * A direction pointer (DP: right/down/left/up) and a codel chooser (CC: left/right) pick which
    edge of the current block to leave from, and which corner of that edge.
  * Moving from one coloured block to the next RUNS A COMMAND chosen by how far the HUE moved
    around the colour wheel and how much DARKER it got. "push" pushes the AREA of the block you left.
  * Black or the image edge = blocked: toggle CC, then rotate DP, alternating, 8 tries, then stop.
  * White is free space you slide through; no command runs across white.
"""
import sys

# 🌈 the 18 colours: (hue 0..5 = red,yellow,green,cyan,blue,magenta ; lightness 0..2 = light,normal,dark)
PALETTE = {}
_light = ["FFC0C0", "FFFFC0", "C0FFC0", "C0FFFF", "C0C0FF", "FFC0FF"]
_norm = ["FF0000", "FFFF00", "00FF00", "00FFFF", "0000FF", "FF00FF"]
_dark = ["C00000", "C0C000", "00C000", "00C0C0", "0000C0", "C000C0"]
for li, row in enumerate([_light, _norm, _dark]):
    for hue, hx in enumerate(row):
        PALETTE[tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))] = (hue, li)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# the command wheel: [hue steps][darkness steps]
COMMANDS = [
    ["none", "push", "pop"],
    ["add", "subtract", "multiply"],
    ["divide", "mod", "not"],
    ["greater", "pointer", "switch"],
    ["duplicate", "roll", "in_number"],
    ["in_char", "out_number", "out_char"],
]
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # DP 0=right 1=down 2=left 3=up, as (dx, dy)


def read_ppm(path):
    data = open(path, "rb").read()
    magic = data[:2]
    if magic == b"P3":
        toks = [t for line in data.decode().splitlines() for t in line.split("#")[0].split()]
        w, h, _mx = int(toks[1]), int(toks[2]), int(toks[3])
        vals = list(map(int, toks[4:4 + w * h * 3]))
    elif magic == b"P6":
        # header: P6 w h max, single whitespace, then raw bytes
        parts, i = [], 2
        while len(parts) < 3:
            while data[i:i + 1].isspace():
                i += 1
            j = i
            while not data[j:j + 1].isspace():
                j += 1
            parts.append(int(data[i:j]))
            i = j
        w, h, _mx = parts
        raw = data[i + 1:i + 1 + w * h * 3]
        vals = list(raw)
    else:
        raise SystemExit(f"not a PPM I know: {magic!r}")
    grid = [[tuple(vals[(y * w + x) * 3:(y * w + x) * 3 + 3]) for x in range(w)] for y in range(h)]
    return grid, w, h


def run(path, max_steps=10000, trace=sys.stderr):
    grid, w, h = read_ppm(path)

    def colour(x, y):
        return grid[y][x]

    def passable(x, y):
        return 0 <= x < w and 0 <= y < h and colour(x, y) != BLACK

    def block_at(x, y):
        c, seen, todo = colour(x, y), {(x, y)}, [(x, y)]
        while todo:
            cx, cy = todo.pop()
            for dx, dy in DIRS:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and colour(nx, ny) == c:
                    seen.add((nx, ny)); todo.append((nx, ny))
        return seen

    def exit_codel(block, dp, cc):
        dx, dy = DIRS[dp]
        far = max(x * dx + y * dy for x, y in block)              # furthest along DP
        edge = [(x, y) for x, y in block if x * dx + y * dy == far]
        side = (dp + (3 if cc == 0 else 1)) % 4                     # CC left = DP turned counter-clockwise
        sx, sy = DIRS[side]
        return max(edge, key=lambda p: p[0] * sx + p[1] * sy)

    stack, out = [], []
    x, y, dp, cc = 0, 0, 0, 0
    steps = 0
    while steps < max_steps:
        block = block_at(x, y)
        here = colour(x, y)
        moved = False
        for attempt in range(8):
            ex, ey = exit_codel(block, dp, cc)
            nx, ny = ex + DIRS[dp][0], ey + DIRS[dp][1]
            if passable(nx, ny):
                moved = True
                break
            if attempt % 2 == 0:
                cc = 1 - cc
            else:
                dp = (dp + 1) % 4
        if not moved:
            print(f"  halt: blocked 8 ways at block of {here} (size {len(block)}) after {steps} steps", file=trace)
            break
        steps += 1
        if colour(nx, ny) == WHITE:
            # slide straight through white; if blocked inside white, turn and keep sliding (no command runs)
            seen = set()
            while True:
                while passable(nx + DIRS[dp][0], ny + DIRS[dp][1]) and colour(nx, ny) == WHITE:
                    nx, ny = nx + DIRS[dp][0], ny + DIRS[dp][1]
                if colour(nx, ny) != WHITE:
                    break
                if (nx, ny, dp, cc) in seen:
                    print("  halt: trapped in white", file=trace)
                    print("".join(out), end="")
                    return "".join(out), stack
                seen.add((nx, ny, dp, cc))
                cc = 1 - cc
                dp = (dp + 1) % 4
            x, y = nx, ny
            print(f"  step {steps}: slid through white", file=trace)
            continue
        new = colour(nx, ny)
        cmd = "none"
        if here in PALETTE and new in PALETTE:
            (h0, l0), (h1, l1) = PALETTE[here], PALETTE[new]
            cmd = COMMANDS[(h1 - h0) % 6][(l1 - l0) % 3]
        size = len(block)
        execute(cmd, size, stack, out)
        print(f"  step {steps}: {here}->{new} {cmd}{' '+str(size) if cmd=='push' else ''}  stack={stack}", file=trace)
        x, y = nx, ny
        if cmd == "pointer" and getattr(execute, "dp_turn", None) is not None:
            dp = (dp + execute.dp_turn) % 4; execute.dp_turn = None
        if cmd == "switch" and getattr(execute, "cc_flip", None) is not None:
            cc = (cc + execute.cc_flip) % 2; execute.cc_flip = None
    return "".join(out), stack


def execute(cmd, size, s, out):
    """One Piet command. Underflow = the command is ignored (spec)."""
    def need(n):
        return len(s) >= n
    if cmd == "push":
        s.append(size)
    elif cmd == "pop" and need(1):
        s.pop()
    elif cmd in ("add", "subtract", "multiply", "divide", "mod", "greater") and need(2):
        a, b = s.pop(), s.pop()          # a = top, b = second
        if cmd == "add": s.append(b + a)
        elif cmd == "subtract": s.append(b - a)
        elif cmd == "multiply": s.append(b * a)
        elif cmd == "divide":
            if a == 0: s.extend([b, a])  # division by zero: leave the stack alone
            else: s.append(b // a)
        elif cmd == "mod":
            if a == 0: s.extend([b, a])
            else: s.append(b % a)        # Python's % takes the divisor's sign, as the spec asks
        elif cmd == "greater": s.append(1 if b > a else 0)
    elif cmd == "not" and need(1):
        s.append(1 if s.pop() == 0 else 0)
    elif cmd == "pointer" and need(1):
        execute.dp_turn = s.pop()
    elif cmd == "switch" and need(1):
        execute.cc_flip = abs(s.pop())
    elif cmd == "duplicate" and need(1):
        s.append(s[-1])
    elif cmd == "roll" and need(2):
        rolls, depth = s.pop(), s.pop()
        if depth > 0 and depth <= len(s):
            seg = s[-depth:]
            r = rolls % depth
            s[-depth:] = seg[-r:] + seg[:-r] if r else seg
        else:
            s.extend([depth, rolls])
    elif cmd == "out_number" and need(1):
        out.append(str(s.pop()))
    elif cmd == "out_char" and need(1):
        out.append(chr(s.pop()))
    # in_number / in_char: no input in these tests; ignored


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"=== {p}", file=sys.stderr)
        result, stack = run(p)
        print(f"{p}\t{result!r}\tfinal stack={stack}")
