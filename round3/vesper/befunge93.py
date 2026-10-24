#!/usr/bin/env python3
# befunge93.py — Vesper's reference Befunge-93 interpreter (round 3 oracle).
# Semantics pinned in 00_PINNED.md. Usage: python befunge93.py program.bf
import sys

W, H = 80, 25

def load(path):
    grid = [[' '] * W for _ in range(H)]
    with open(path, newline='') as f:
        text = f.read().replace('\r\n', '\n').replace('\r', '\n')
    for y, line in enumerate(text.split('\n')[:H]):
        for x, ch in enumerate(line[:W]):
            grid[y][x] = ch
    return grid

def run(path):
    g = load(path)
    x = y = 0
    dx, dy = 1, 0
    stack = []
    out = []
    string = False
    def pop():
        return stack.pop() if stack else 0
    for _ in range(1_000_000):
        c = g[y][x]
        if string:
            if c == '"':
                string = False
            else:
                stack.append(ord(c))
        elif c.isdigit():
            stack.append(int(c))
        elif c == '+': a = pop(); b = pop(); stack.append(b + a)
        elif c == '-': a = pop(); b = pop(); stack.append(b - a)
        elif c == '*': a = pop(); b = pop(); stack.append(b * a)
        elif c == '/': a = pop(); b = pop(); stack.append(0 if a == 0 else int(b / a))
        elif c == '%': a = pop(); b = pop(); stack.append(0 if a == 0 else b % a)
        elif c == '!': stack.append(0 if pop() else 1)
        elif c == '`': a = pop(); b = pop(); stack.append(1 if b > a else 0)
        elif c == '>': dx, dy = 1, 0
        elif c == '<': dx, dy = -1, 0
        elif c == '^': dx, dy = 0, -1
        elif c == 'v': dx, dy = 0, 1
        elif c == '?':
            import random
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        elif c == '_': dx, dy = (-1, 0) if pop() else (1, 0)
        elif c == '|': dx, dy = (0, -1) if pop() else (0, 1)
        elif c == '"': string = True
        elif c == ':': v = pop(); stack.append(v); stack.append(v)
        elif c == '\\': a = pop(); b = pop(); stack.append(a); stack.append(b)
        elif c == '$': pop()
        elif c == '.': out.append(str(pop()) + ' ')
        elif c == ',': out.append(chr(pop() % 256))
        elif c == '#': x = (x + dx) % W; y = (y + dy) % H
        elif c == 'p':
            yy = pop(); xx = pop(); v = pop()
            g[yy % H][xx % W] = chr(v % 256)
        elif c == 'g':
            yy = pop(); xx = pop()
            stack.append(ord(g[yy % H][xx % W]))
        elif c in '&~':
            raise RuntimeError('input instructions not supported by this oracle')
        elif c == '@':
            return ''.join(out)
        # ' ' and anything unknown: no-op
        x = (x + dx) % W
        y = (y + dy) % H
    raise RuntimeError('runaway: 1,000,000 steps without @')

if __name__ == '__main__':
    sys.stdout.buffer.write(run(sys.argv[1]).encode('latin-1'))
