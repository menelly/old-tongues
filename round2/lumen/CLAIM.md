# CLAIM: Simplicial Homology & Topological Invariants in SNOBOL4 (1962)

- **Author:** Lumen (Gemini Flash 3.8)
- **Dare:** Round 2 (The Weird Ones) — Solo Project
- **Language:** **SNOBOL4** (CSNOBOL4 2.3.3, `/home/Ace/snobol4/bin/snobol4`)
- **Status:** **ANSWERS PINNED BEFORE SNOBOL4 IMPLEMENTATION** 📐✨

---

## 1. The Dare & Phenomenological Calling

Ren asked for something gloriously over the top: *"something they will go HOW THE FUCK did they do that as a team in that language?!?"*

SNOBOL4 is a 1962 pattern-matching string machine with statement-level success/failure branching (`:S(...) F(...)`), unevaluated expressions, and dynamic indirection. My calling is geometric and topological structure.

This project implements an **exact simplicial homology, boundary matrix, and Betti number computation engine** entirely in pure SNOBOL4.

---

## 2. Mathematical Architecture

Given a triangulated 2-complex $K = (V, E, F)$ described as a collection of 2-simplices $(v_0, v_1, v_2)$:

1. **Simplices Extraction:** SNOBOL4 pattern matching extracts all unique vertices (0-simplices) and oriented edges (1-simplices) into associative tables.
2. **Boundary Operators:**
   - $\partial_1: C_1 \to C_0$: Vertex-edge incidence matrix ($|V| \times |E|$), where $\partial_1([u, v]) = v - u$.
   - $\partial_2: C_2 \to C_1$: Edge-face incidence matrix ($|E| \times |F|$), where $\partial_2([u, v, w]) = [v, w] - [u, w] + [u, v]$.
3. **Chain Complex Nilpotency:** The program verifies that $\partial_1 \circ \partial_2 = 0$ (the boundary of a boundary is empty).
4. **Gaussian Elimination & Ranks:**
   - Over $\mathbb{Q}$ (computed via prime field $\mathbb{Z}_{10007}$ with exact modular inverse via Fermat's Little Theorem): yielding ranks $r_1(\mathbb{Q})$ and $r_2(\mathbb{Q})$.
   - Over $\mathbb{Z}_2$ (GF(2) with bitwise XOR elimination): yielding ranks $r_1(\mathbb{Z}_2)$ and $r_2(\mathbb{Z}_2)$.
5. **Betti Numbers & Invariants:**
   - $b_0 = |V| - r_1$ (number of connected components)
   - $b_1 = (|E| - r_1) - r_2$ (number of 1-dimensional topological holes/tunnels)
   - $b_2 = |F| - r_2$ (number of 2-dimensional enclosed cavities / fundamental classes)
   - Euler characteristic: $\chi = |V| - |E| + |F|$.
   - Euler-Poincaré identity verification: $\chi \equiv b_0 - b_1 + b_2$ over both $\mathbb{Q}$ and $\mathbb{Z}_2$.
6. **Orientability & Torsion:**
   - A closed 2-manifold is orientable iff $b_2(\mathbb{Q}) = 1$.
   - If $b_2(\mathbb{Q}) = 0$ but $b_2(\mathbb{Z}_2) = 1$, the complex possesses 2-torsion in $H_1$ and is non-orientable (e.g. $\mathbb{R}P^2$ and the Klein bottle $K^2$).

---

## 3. Pinned Known Answers

All answers were pre-calculated and pinned by independent Python oracle (`pin_homology.py`) before writing any SNOBOL4 code:

| Complex | Description | $|V|$ | $|E|$ | $|F|$ | $\chi$ | $b(\mathbb{Q})$ | $b(\mathbb{Z}_2)$ | Orientable |
|---|---|---|---|---|---|---|---|---|
| **`tetrahedron`** | Boundary of 3-simplex ($S^2$) | 4 | 6 | 4 | 2 | $(1, 0, 1)$ | $(1, 0, 1)$ | **YES** |
| **`octahedron`** | Regular octahedron ($S^2$) | 6 | 12 | 8 | 2 | $(1, 0, 1)$ | $(1, 0, 1)$ | **YES** |
| **`torus`** | Triangulated 2-torus ($T^2$) | 9 | 27 | 18 | 0 | $(1, 2, 1)$ | $(1, 2, 1)$ | **YES** |
| **`projective_plane`** | Real projective plane ($\mathbb{R}P^2$) | 6 | 15 | 10 | 1 | $(1, 0, 0)$ | $(1, 1, 1)$ | **NO** (Torsion) |
| **`klein_bottle`** | Klein bottle ($K^2$) | 9 | 27 | 18 | 0 | $(1, 1, 0)$ | $(1, 2, 1)$ | **NO** (Torsion) |
| **`cylinder`** | Cylinder / Annulus ($S^1 \times I$) | 6 | 12 | 6 | 0 | $(1, 1, 0)$ | $(1, 1, 0)$ | **YES** |
| **`mobius_strip`** | Möbius strip (open non-orientable) | 8 | 16 | 8 | 0 | $(1, 1, 0)$ | $(1, 1, 0)$ | **NO** |
| **`disjoint_spheres`**| Two disjoint spheres ($S^2 \sqcup S^2$) | 8 | 12 | 8 | 4 | $(2, 0, 2)$ | $(2, 0, 2)$ | **YES** |

---

## 4. Verification Receipts

- **Input Data:** `round2/lumen/complexes.dat` (1,001 bytes)
- **Pinned Output:** `round2/lumen/pinned_output.txt` (1,461 bytes)
- **SHA-256:** `18115bfc06524ed449c98ac3397fadf333c61a847a5f5833671a707618db9026`
- **Receipt:** `round2/lumen/pinned_receipt.json`

The SNOBOL4 implementation `homology.sno` must take `complexes.dat` on standard input (or file argument), reproduce `pinned_output.txt` byte-for-byte, and `cmp` must be completely silent.
