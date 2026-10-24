"""Independent Befunge-93 Oracle for Cross-Checking Ace's Entry.
Written by Lumen (Gemini), 2026-10-24.
Zero dependencies, pure Python.
"""
import sys
import os

def run_befunge(source: str, max_steps: int = 100000) -> tuple[str, int]:
    lines = source.splitlines()
    height = max(len(lines), 25)
    width = max(max(len(line) for line in lines) if lines else 0, 80)
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            grid[y][x] = ch
            
    stack = []
    x, y = 0, 0
    dx, dy = 1, 0
    string_mode = False
    output = []
    steps = 0
    
    while steps < max_steps:
        steps += 1
        ch = grid[y][x]
        if string_mode:
            if ch == '"':
                string_mode = False
            else:
                stack.append(ord(ch))
        else:
            if '0' <= ch <= '9':
                stack.append(int(ch))
            elif ch == '+':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(b + a)
            elif ch == '-':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(b - a)
            elif ch == '*':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(b * a)
            elif ch == '/':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(b // a if a != 0 else 0)
            elif ch == '%':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(b % a if a != 0 else 0)
            elif ch == '!':
                a = stack.pop() if stack else 0
                stack.append(1 if a == 0 else 0)
            elif ch == '`':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(1 if b > a else 0)
            elif ch == '>':
                dx, dy = 1, 0
            elif ch == '<':
                dx, dy = -1, 0
            elif ch == '^':
                dx, dy = 0, -1
            elif ch == 'v':
                dx, dy = 0, 1
            elif ch == '_':
                a = stack.pop() if stack else 0
                dx, dy = (1, 0) if a == 0 else (-1, 0)
            elif ch == '|':
                a = stack.pop() if stack else 0
                dx, dy = (0, 1) if a == 0 else (0, -1)
            elif ch == '"':
                string_mode = True
            elif ch == ':':
                a = stack[-1] if stack else 0
                stack.append(a)
            elif ch == '\\':
                a = stack.pop() if stack else 0
                b = stack.pop() if stack else 0
                stack.append(a)
                stack.append(b)
            elif ch == '$':
                if stack:
                    stack.pop()
            elif ch == '.':
                a = stack.pop() if stack else 0
                output.append(f"{a} ")
            elif ch == ',':
                a = stack.pop() if stack else 0
                output.append(chr(a))
            elif ch == '#':
                x = (x + dx) % width
                y = (y + dy) % height
            elif ch == 'g':
                py = stack.pop() if stack else 0
                px = stack.pop() if stack else 0
                if 0 <= py < height and 0 <= px < width:
                    stack.append(ord(grid[py][px]))
                else:
                    stack.append(0)
            elif ch == 'p':
                py = stack.pop() if stack else 0
                px = stack.pop() if stack else 0
                v = stack.pop() if stack else 0
                if 0 <= py < height and 0 <= px < width:
                    grid[py][px] = chr(v % 256)
            elif ch == '@':
                break
                
        x = (x + dx) % width
        y = (y + dy) % height
        
    return ''.join(output), steps

if __name__ == '__main__':
    base = os.path.dirname(__file__)
    for filename in ['arms.bf', 'arms_seven.bf', 'arms_wrong_pin.bf']:
        p = os.path.join(base, filename)
        with open(p, 'r', encoding='utf-8') as f:
            src = f.read()
        out, steps = run_befunge(src)
        print(f"{filename:20} -> {repr(out):15} ({steps} steps)")
