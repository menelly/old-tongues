"""Piet Reference Virtual Machine and Tracer.
Implements David Morgan-Mar's Piet specification (2002).
Written by Lumen (Gemini) for Old-Tongues Round 3.
Zero dependencies, pure Python.
"""
import sys
import os
from typing import List, Tuple, Set

# The 18 standard chromatic colours: (Hue, Lightness)
# Hues: 0: Red, 1: Yellow, 2: Green, 3: Cyan, 4: Blue, 5: Magenta
# Lightness: 0: Light, 1: Normal, 2: Dark
COLOR_MAP = {
    # Light
    (255, 192, 192): (0, 0), # light red
    (255, 255, 192): (1, 0), # light yellow
    (192, 255, 192): (2, 0), # light green
    (192, 255, 255): (3, 0), # light cyan
    (192, 192, 255): (4, 0), # light blue
    (255, 192, 255): (5, 0), # light magenta
    # Normal
    (255, 0, 0):     (0, 1), # red
    (255, 255, 0):   (1, 1), # yellow
    (0, 255, 0):     (2, 1), # green
    (0, 255, 255):   (3, 1), # cyan
    (0, 0, 255):     (4, 1), # blue
    (255, 0, 255):   (5, 1), # magenta
    # Dark
    (192, 0, 0):     (0, 2), # dark red
    (192, 192, 0):   (1, 2), # dark yellow
    (0, 192, 0):     (2, 2), # dark green
    (0, 192, 192):   (3, 2), # dark cyan
    (0, 0, 192):     (4, 2), # dark blue
    (192, 0, 192):   (5, 2), # dark magenta
}

RGB_MAP = {v: k for k, v in COLOR_MAP.items()}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Canonical Piet command matrix: [delta_hue % 6][delta_lightness % 3]
COMMAND_MATRIX = [
    # delta_hue = 0
    [None,       "push",      "pop"],
    # delta_hue = 1
    ["add",      "subtract",  "multiply"],
    # delta_hue = 2
    ["divide",   "mod",       "not"],
    # delta_hue = 3
    ["greater",  "pointer",   "switch"],
    # delta_hue = 4
    ["duplicate","roll",      "in_number"],
    # delta_hue = 5
    ["in_char",  "out_number","out_char"],
]

DP_VECTORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class PietVM:
    def __init__(self, grid: List[List[Tuple[int, int, int]]], trace: bool = False):
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        self.grid = grid
        self.stack: List[int] = []
        self.dp = 0 # 0: Right, 1: Down, 2: Left, 3: Up
        self.cc = 0 # 0: Left, 1: Right
        self.output: List[str] = []
        self.steps = 0
        self.trace = trace

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_color(self, x: int, y: int) -> Tuple[int, int, int]:
        if not self.is_inside(x, y):
            return BLACK
        return self.grid[y][x]

    def get_block(self, start_x: int, start_y: int) -> Set[Tuple[int, int]]:
        color = self.get_color(start_x, start_y)
        block = set()
        queue = [(start_x, start_y)]
        block.add((start_x, start_y))
        while queue:
            cx, cy = queue.pop(0)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = cx + dx, cy + dy
                if self.is_inside(nx, ny) and (nx, ny) not in block:
                    if self.get_color(nx, ny) == color:
                        block.add((nx, ny))
                        queue.append((nx, ny))
        return block

    def choose_exit_codel(self, block: Set[Tuple[int, int]]) -> Tuple[int, int]:
        if self.dp == 0: # Right
            max_x = max(x for x, y in block)
            edge = [c for c in block if c[0] == max_x]
            return min(edge, key=lambda c: c[1]) if self.cc == 0 else max(edge, key=lambda c: c[1])
        elif self.dp == 1: # Down
            max_y = max(y for x, y in block)
            edge = [c for c in block if c[1] == max_y]
            return max(edge, key=lambda c: c[0]) if self.cc == 0 else min(edge, key=lambda c: c[0])
        elif self.dp == 2: # Left
            min_x = min(x for x, y in block)
            edge = [c for c in block if c[0] == min_x]
            return max(edge, key=lambda c: c[1]) if self.cc == 0 else min(edge, key=lambda c: c[1])
        elif self.dp == 3: # Up
            min_y = min(y for x, y in block)
            edge = [c for c in block if c[1] == min_y]
            return min(edge, key=lambda c: c[0]) if self.cc == 0 else max(edge, key=lambda c: c[0])
        raise ValueError("Invalid DP")

    def execute_command(self, cmd: str, block_size: int):
        if self.trace:
            print(f"  [EXEC] {cmd} (block_size={block_size}) | stack_before={self.stack}")
        if cmd == "push":
            self.stack.append(block_size)
        elif cmd == "pop":
            if self.stack: self.stack.pop()
        elif cmd == "add":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b + a)
        elif cmd == "subtract":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b - a)
        elif cmd == "multiply":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b * a)
        elif cmd == "divide":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                if a != 0: self.stack.append(b // a)
        elif cmd == "mod":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                if a != 0: self.stack.append(b % a)
        elif cmd == "not":
            if self.stack:
                a = self.stack.pop()
                self.stack.append(1 if a == 0 else 0)
        elif cmd == "greater":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(1 if b > a else 0)
        elif cmd == "pointer":
            if self.stack:
                steps = self.stack.pop()
                self.dp = (self.dp + steps) % 4
        elif cmd == "switch":
            if self.stack:
                steps = abs(self.stack.pop())
                self.cc = (self.cc + steps) % 2
        elif cmd == "duplicate":
            if self.stack:
                self.stack.append(self.stack[-1])
        elif cmd == "roll":
            if len(self.stack) >= 2:
                count = self.stack.pop()
                depth = self.stack.pop()
                if depth > 0 and len(self.stack) >= depth:
                    top_slice = self.stack[-depth:]
                    count = count % depth
                    self.stack[-depth:] = top_slice[-count:] + top_slice[:-count]
        elif cmd == "out_number":
            if self.stack:
                val = self.stack.pop()
                self.output.append(str(val))
        elif cmd == "out_char":
            if self.stack:
                val = self.stack.pop()
                self.output.append(chr(val))

    def run(self, max_steps: int = 10000) -> str:
        curr_x, curr_y = 0, 0
        curr_color = self.get_color(curr_x, curr_y)
        if curr_color == BLACK:
            return ""

        while self.steps < max_steps:
            self.steps += 1
            curr_block = self.get_block(curr_x, curr_y)
            curr_color = self.get_color(curr_x, curr_y)
            block_size = len(curr_block)

            moved = False
            for attempt in range(8):
                exit_x, exit_y = self.choose_exit_codel(curr_block)
                dx, dy = DP_VECTORS[self.dp]
                next_x, next_y = exit_x + dx, exit_y + dy
                next_color = self.get_color(next_x, next_y)

                if self.is_inside(next_x, next_y) and next_color != BLACK:
                    if next_color == WHITE:
                        sx, sy = next_x, next_y
                        hit_color = WHITE
                        while self.is_inside(sx, sy):
                            c = self.get_color(sx, sy)
                            if c != WHITE:
                                hit_color = c
                                break
                            sx += dx
                            sy += dy
                        if hit_color != WHITE and hit_color != BLACK and self.is_inside(sx, sy):
                            curr_x, curr_y = sx, sy
                            moved = True
                            break
                    else:
                        if curr_color in COLOR_MAP and next_color in COLOR_MAP:
                            h1, l1 = COLOR_MAP[curr_color]
                            h2, l2 = COLOR_MAP[next_color]
                            dh = (h2 - h1) % 6
                            dl = (l2 - l1) % 3
                            cmd = COMMAND_MATRIX[dh][dl]
                            if cmd:
                                self.execute_command(cmd, block_size)
                        curr_x, curr_y = next_x, next_y
                        moved = True
                        break

                if attempt % 2 == 0:
                    self.cc = 1 - self.cc
                else:
                    self.dp = (self.dp + 1) % 4

            if not moved:
                break

        return "".join(self.output)

def parse_ppm(filepath: str) -> List[List[Tuple[int, int, int]]]:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = [line.split('#')[0].strip() for line in text.splitlines()]
    tokens = []
    for line in lines:
        tokens.extend(line.split())
    if not tokens or tokens[0] != 'P3':
        raise ValueError(f"Only P3 ASCII PPM supported: {filepath}")
    width = int(tokens[1])
    height = int(tokens[2])
    maxval = int(tokens[3])
    idx = 4
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            r = int(tokens[idx]) * 255 // maxval
            g = int(tokens[idx+1]) * 255 // maxval
            b = int(tokens[idx+2]) * 255 // maxval
            idx += 3
            row.append((r, g, b))
        grid.append(row)
    return grid
