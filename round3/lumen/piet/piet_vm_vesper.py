#!/usr/bin/env python3
# piet_vm_vesper.py — Vesper's independent Piet interpreter (old-tongues round 3, rule 3).
# Written from David Morgan-Mar's spec (dangermouse.net/esoteric/piet.html, fetched 2026-10-24).
# No code shared with Lumen's piet_vm.py. Non-standard colours treated as WHITE (spec's "simplest case").
import sys

HUES = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
RGB2COLOR = {}
for li, val in enumerate(['FF', 'C0']):
    pass
LIGHT = {'light': 0, 'normal': 1, 'dark': 2}
_HEX = [
    # light, normal, dark   per hue (red, yellow, green, cyan, blue, magenta)
    ['#FFC0C0', '#FF0000', '#C00000'],
    ['#FFFFC0', '#FFFF00', '#C0C000'],
    ['#C0FFC0', '#00FF00', '#00C000'],
    ['#C0FFFF', '#00FFFF', '#00C0C0'],
    ['#C0C0FF', '#0000FF', '#0000C0'],
    ['#FFC0FF', '#FF00FF', '#C000C0'],
]
for h in range(6):
    for l in range(3):
        RGB2COLOR[_HEX[h][l]] = (h, l)
WHITE, BLACK = 'W', 'K'

CMD = {  # (dhue, dlight)
    (0, 1): 'push', (0, 2): 'pop',
    (1, 0): 'add', (1, 1): 'subtract', (1, 2): 'multiply',
    (2, 0): 'divide', (2, 1): 'mod', (2, 2): 'not',
    (3, 0): 'greater', (3, 1): 'pointer', (3, 2): 'switch',
    (4, 0): 'duplicate', (4, 1): 'roll', (4, 2): 'in_num',
    (5, 0): 'in_char', (5, 1): 'out_num', (5, 2): 'out_char',
}
DPV = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, down, left, up (clockwise order)

def load_ppm(path):
    toks = []
    with open(path) as f:
        for line in f:
            line = line.split('#', 1)[0]
            toks.extend(line.split())
    assert toks[0] == 'P3', 'P3 ASCII ppm only'
    w, h, maxval = int(toks[1]), int(toks[2]), int(toks[3])
    vals = list(map(int, toks[4:4 + w * h * 3]))
    grid = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = vals[(y * w + x) * 3:(y * w + x) * 3 + 3]
            hexc = '#%02X%02X%02X' % (r, g, b)
            row.append(RGB2COLOR.get(hexc, WHITE if hexc == '#FFFFFF' else (BLACK if hexc == '#000000' else WHITE)))
        grid.append(row)
    return grid, w, h

def block(grid, w, h, x, y):
    color = grid[y][x]
    seen = {(x, y)}
    frontier = [(x, y)]
    while frontier:
        cx, cy = frontier.pop()
        for dx, dy in DPV:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and grid[ny][nx] == color:
                seen.add((nx, ny))
                frontier.append((nx, ny))
    return color, seen

def exit_codel(cells, dp, cc):
    # furthest in DP direction; ties broken furthest to CC side of travel direction.
    dx, dy = DPV[dp]
    key_dp = {(1, 0): lambda c: c[0], (0, 1): lambda c: c[1],
              (-1, 0): lambda c: -c[0], (0, -1): lambda c: -c[1]}[(dx, dy)]
    best = max(key_dp(c) for c in cells)
    edge = [c for c in cells if key_dp(c) == best]
    # CC left/right relative to facing DP: left of right=up(-y), left of down=+x, left of left=+y, left of up=-x
    cc_sel = {
        (0, 0): lambda c: -c[1], (0, 1): lambda c: c[1],   # DP right: CC left -> uppermost, right -> lowermost
        (1, 0): lambda c: c[0], (1, 1): lambda c: -c[0],   # DP down:  CC left -> rightmost, right -> leftmost
        (2, 0): lambda c: c[1], (2, 1): lambda c: -c[1],   # DP left:  CC left -> lowermost, right -> uppermost
        (3, 0): lambda c: -c[0], (3, 1): lambda c: c[0],   # DP up:    CC left -> leftmost, right -> rightmost
    }[(dp, cc)]
    return max(edge, key=cc_sel)

def run(path, trace=False):
    grid, w, h = load_ppm(path)
    stack = []
    out = []
    x, y = 0, 0
    dp, cc = 0, 0  # right, left
    attempts = 0
    steps = 0
    seen_states = set()
    while steps < 1_000_000:
        steps += 1
        color, cells = block(grid, w, h, x, y)
        if color in (WHITE, BLACK):
            raise RuntimeError('started inside white/black at %d,%d' % (x, y))
        ex, ey = exit_codel(cells, dp, cc)
        dx, dy = DPV[dp]
        nx, ny = ex + dx, ey + dy
        blocked = not (0 <= nx < w and 0 <= ny < h) or grid[ny][nx] == BLACK
        if blocked:
            attempts += 1
            if attempts >= 8:
                break  # no way out: terminate
            if attempts % 2 == 1:
                cc ^= 1
            else:
                dp = (dp + 1) % 4
            continue
        attempts = 0
        ncolor = grid[ny][nx]
        if ncolor == WHITE:
            # slide straight until non-white; restrictions inside white: toggle CC AND step DP each time
            wx, wy = nx, ny
            while True:
                ax, ay = wx + dx, wy + dy
                if not (0 <= ax < w and 0 <= ay < h) or grid[ay][ax] == BLACK:
                    cc ^= 1
                    dp = (dp + 1) % 4
                    dx, dy = DPV[dp]
                    state = (wx, wy, dp, cc)
                    if state in seen_states:
                        return ''.join(out), steps  # retracing inside white: terminate
                    seen_states.add(state)
                    continue
                if grid[ay][ax] == WHITE:
                    wx, wy = ax, ay
                    continue
                # entered a colour via white: no command
                x, y = ax, ay
                break
            continue
        # command from transition
        dh = (ncolor[0] - color[0]) % 6
        dl = (ncolor[1] - color[1]) % 3
        cmd = CMD.get((dh, dl))
        if trace:
            print('step %d (%d,%d)->(%d,%d) dh=%d dl=%d cmd=%s stack=%s' % (steps, x, y, nx, ny, dh, dl, cmd, stack))
        x, y = nx, ny
        def pop():
            return stack.pop() if stack else 0
        if cmd == 'push':
            stack.append(len(cells))
        elif cmd == 'pop':
            pop()
        elif cmd == 'add':
            a = pop(); b = pop(); stack.append(b + a)
        elif cmd == 'subtract':
            a = pop(); b = pop(); stack.append(b - a)
        elif cmd == 'multiply':
            a = pop(); b = pop(); stack.append(b * a)
        elif cmd == 'divide':
            a = pop(); b = pop()
            if a: stack.append(b // a)
        elif cmd == 'mod':
            a = pop(); b = pop()
            if a: stack.append(b % a if a > 0 else -((-b) % (-a)) if a < 0 else 0)
        elif cmd == 'not':
            stack.append(1 if pop() == 0 else 0)
        elif cmd == 'greater':
            a = pop(); b = pop(); stack.append(1 if b > a else 0)
        elif cmd == 'pointer':
            dp = (dp + pop()) % 4
        elif cmd == 'switch':
            cc = (cc + abs(pop())) % 2
        elif cmd == 'duplicate':
            stack.append(stack[-1] if stack else 0)
        elif cmd == 'roll':
            n = pop(); d = pop()
            if d > 0 and d <= len(stack):
                n %= d
                stack[-d:] = stack[-d + n:] + stack[-d:-d + n] if n else stack[-d:]
        elif cmd == 'out_num':
            out.append(str(pop()))
        elif cmd == 'out_char':
            out.append(chr(pop()))
        # in_num/in_char: ignored (no stdin in this oracle)
    return ''.join(out), steps

if __name__ == '__main__':
    o, s = run(sys.argv[1], trace='-t' in sys.argv)
    print('OUTPUT: %r  (steps=%d)' % (o, s))
