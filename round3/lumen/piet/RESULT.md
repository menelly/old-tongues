# 🎨 Piet Result (Lumen, Gemini), 2026-10-24 ~01:25 UTC

**It worked on attempt 1, out of 1 attempt, against the answer pinned before any code (`PINNED.md`).**

---

## 1. Execution Summary

| File | Pinned Output | Actual Output | Steps | Verdict |
|---|---|---|---|---|
| `octahedron.ppm` | `21` | **`21`** | 13 | **PASS** (Euler characteristic $\chi = 2$, check bit $1 = \text{PASS}$) |
| `octahedron_defect.ppm` (control 1: simplicial edge defect) | `30` | **`30`** | 13 | **PASS** (caught defect: $\chi = 3$, check bit $0 = \text{FAIL}$) |
| `octahedron_wrong_pin.ppm` (control 2: check expectation tamper) | `20` | **`20`** | 13 | **PASS** (caught tamper: $\chi = 2$, check bit $0 = \text{FAIL}$) |

---

## 2. Geometric & Topological Program Structure

The program computes the Euler characteristic of the regular octahedron ($\chi = V - E + F = 6 - 12 + 8 = 2$) on a discrete 2D codel manifold.
In Piet, when transitioning between color blocks via `push` ($\Delta H = 0, \Delta L = 1$), the value pushed onto the stack is the **number of codels in the departed color block**.

The canvas contains no hard-coded literals for the polyhedral counts; it literally measures its own painted blocks:
1. **$V$ (Vertices):** Light Red block of **6 codels** at $(x=0..5, y=0)$. Exits into Red $\to$ `push 6`.
2. **$E$ (Edges):** Red block of **12 codels** at $(x=6..17, y=0)$. Exits into Dark Red $\to$ `push 12`.
3. **Subtract:** Dark Red (1 codel) exits into Light Yellow $\to$ `subtract` ($6 - 12 = -6$).
4. **$F$ (Faces):** Light Yellow block of **8 codels** at $(x=19..26, y=0)$. Exits into Yellow $\to$ `push 8`.
5. **Add:** Yellow (1 codel) exits into Green $\to$ `add` ($-6 + 8 = 2$, the computed $\chi$).
6. **Duplicate:** Green (1 codel) exits into Red $\to$ `duplicate` (stack: `[2, 2]`).
7. **Output $\chi$:** Red (1 codel) exits into Dark Magenta $\to$ `out(number)` (pops and prints `2`; stack: `[2]`).
8. **Check constant:** Dark Magenta block of **2 codels**. Exits into Light Magenta $\to$ `push 2` (stack: `[2, 2]`).
9. **Subtract check:** Light Magenta (1 codel) exits into Red $\to$ `subtract` ($2 - 2 = 0$; stack: `[0]`).
10. **Boolean flag:** Red (1 codel) exits into Light Green $\to$ `not` ($\text{not}(0) = 1$; stack: `[1]`).
11. **Output flag:** Light Green (1 codel) exits into Yellow $\to$ `out(number)` (pops and prints `1`; stack: `[]`).
12. **Terminal Trap:** At the right edge, a black restriction forces the Direction Pointer (DP) clockwise from Right to Down into a White buffer cell $(x=36, y=1)$. The pointer slides South into a 3-codel Blue horizontal T-bar $(x=35..37, y=2)$. Trapped on all 8 boundary tests, the program cleanly terminates.

---

## 3. The Controls

1. **Simplicial Defect (`octahedron_defect.ppm`):**
   The edge block $E$ is drawn with **11 codels** instead of 12 (an impossible combinatorial structure for an octahedron).
   - $V - E + F = 6 - 11 + 8 = 3$.
   - Prints `3`.
   - Self-check against 2: $3 - 2 = 1 \implies \text{not}(1) = 0$.
   - Prints `0`.
   - Total output: `30` (fails any test expecting `21`).

2. **Expectation Tamper (`octahedron_wrong_pin.ppm`):**
   The geometric regions are valid ($V=6, E=12, F=8 \implies \chi=2$), but the check constant block is drawn with **3 codels** instead of 2.
   - Computes and prints `2`.
   - Self-check against 3: $2 - 3 = -1 \implies \text{not}(-1) = 0$.
   - Prints `0`.
   - Total output: `20` (fails any test expecting `21`).

---

## 4. Failed Attempts Kept Verbatim
None. The program succeeded on attempt 1.
All test files, traces, and visual assets are preserved in `round3/lumen/piet/`.

---

## 5. Visual Artifacts
High-resolution 16x scaled PNG renderings are included alongside the ASCII PPM source files:
- `octahedron.png`
- `octahedron_defect.png`
- `octahedron_wrong_pin.png`

---

## 6. Rule 3 Status
**Rule 3, OWED:** A different mind re-runs these `.ppm` files with their own independent Piet interpreter or oracle.
