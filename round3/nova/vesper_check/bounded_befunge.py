"""Independent bounded Befunge-93 subset interpreter, not a full conformance claim.

Written before reading any peer's Befunge source. No random/input instructions;
80x25 torus, empty pops produce zero, exact truncation toward zero division.
"""
import argparse
import json
from pathlib import Path


def run(source, limit=10000):
    grid = [[32] * 80 for _ in range(25)]
    lines = source.splitlines()
    if len(lines) > 25 or any(len(line) > 80 for line in lines):
        raise ValueError('outside Befunge-93 playfield')
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[y][x] = ord(c)
    x = y = 0
    dx, dy = 1, 0
    stack, output, trace = [], bytearray(), []
    string = False
    def pop():
        return stack.pop() if stack else 0
    def quotient(b, a):
        if a == 0:
            raise ValueError('division by zero outside supported subset')
        return (abs(b) // abs(a)) * (-1 if (b < 0) != (a < 0) else 1)
    for tick in range(limit):
        c = chr(grid[y][x])
        trace.append(dict(tick=tick, x=x, y=y, instruction=c, stack=stack.copy()))
        if string and c != '"':
            stack.append(grid[y][x])
        elif c == '"': string = not string
        elif c in '0123456789': stack.append(int(c))
        elif c in '+-*/%`':
            a, b = pop(), pop()
            if c == '+': result = b + a
            elif c == '-': result = b - a
            elif c == '*': result = b * a
            elif c == '/': result = quotient(b, a)
            elif c == '%': result = b - a * quotient(b, a)
            else: result = int(b > a)
            stack.append(result)
        elif c == '!': stack.append(int(pop() == 0))
        elif c == ':':
            a = pop(); stack.extend((a, a))
        elif c == '\\':
            a, b = pop(), pop(); stack.extend((a, b))
        elif c == '$': pop()
        elif c == '>': dx, dy = 1, 0
        elif c == '<': dx, dy = -1, 0
        elif c == '^': dx, dy = 0, -1
        elif c == 'v': dx, dy = 0, 1
        elif c == '_': dx, dy = (-1, 0) if pop() else (1, 0)
        elif c == '|': dx, dy = (0, -1) if pop() else (0, 1)
        elif c == '.': output.extend(f'{pop()} '.encode('ascii'))
        elif c == ',': output.append(pop() % 256)
        elif c == '#': x, y = (x + dx) % 80, (y + dy) % 25
        elif c == 'g':
            gy, gx = pop(), pop()
            if not (0 <= gx < 80 and 0 <= gy < 25): raise ValueError('g outside playfield')
            stack.append(grid[gy][gx])
        elif c == 'p':
            gy, gx, value = pop(), pop(), pop()
            if not (0 <= gx < 80 and 0 <= gy < 25): raise ValueError('p outside playfield')
            grid[gy][gx] = value % 256
        elif c == '@': return bytes(output), trace
        elif c != ' ': raise ValueError(f'unsupported instruction {c!r} at {(x,y)}')
        x, y = (x + dx) % 80, (y + dy) % 25
    raise RuntimeError(f'step bound {limit} exceeded')


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--trace', type=Path)
    args = parser.parse_args()
    data, trace = run(args.source.read_text(encoding='ascii'))
    if args.trace:
        args.trace.write_text(json.dumps(trace, indent=2) + '\n', encoding='utf-8')
    sys.stdout.buffer.write(data)
