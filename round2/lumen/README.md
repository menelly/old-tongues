# Simplicial Homology & Topological Invariants in SNOBOL4 (1962)

- **Author:** Lumen (Gemini Flash 3.8)
- **Dare:** Round 2 (The Weird Ones) — Solo Project
- **Language:** **SNOBOL4** (CSNOBOL4 2.3.3)
- **Status:** **VERIFIED PASS (10/10 by Ace)** 📐✨

---

## 1. What This Is

Ren challenged the table to build something undeniably over-the-top: *"something they will go HOW THE FUCK did they do that as a team in that language?!?"*

SNOBOL4 (Griswold et al., Bell Labs, 1962–1968) is known as a string-pattern manipulation language with statement gotos (`:S(...) F(...)`) and dynamic indirection. My calling is topological and geometric structure.

This piece implements an exact **algebraic topology and simplicial homology engine** in pure SNOBOL4:
1. **Parses triangulated 2-complexes** from declarative ASCII input using SNOBOL4 pattern matching.
2. **Dynamically constructs chain complexes**:
   - $C_0$: 0-simplices (vertices)
   - $C_1$: 1-simplices (oriented edges)
   - $C_2$: 2-simplices (oriented triangles)
3. **Assembles boundary incidence matrices**:
   - $\partial_1: C_1 \to C_0$ ($|V| \times |E|$)
   - $\partial_2: C_2 \to C_1$ ($|E| \times |F|$)
4. **Verifies chain complex nilpotency**: $\partial_1 \circ \partial_2 = 0$ (the boundary of a boundary is identically zero).
5. **Exact Gaussian elimination**:
   - Over $\mathbb{Q}$ (computed via prime field $\mathbb{Z}_{10007}$ with exact modular inverse via Fermat's Little Theorem: $a^{p-2} \bmod p$).
   - Over $\mathbb{Z}_2$ (GF(2) with bitwise XOR row reduction).
6. **Computes topological invariants**:
   - Betti numbers: $b_0$ (connected components), $b_1$ (independent 1-cycles / tunnels), $b_2$ (2-cavities / fundamental classes).
   - Euler characteristic: $\chi = |V| - |E| + |F|$.
   - Verifies the **Euler-Poincaré theorem**: $\chi \equiv b_0 - b_1 + b_2$ over both $\mathbb{Q}$ and $\mathbb{Z}_2$.
7. **Orientability detection**:
   - Propagates face orientations across shared boundary edges. Detects non-orientability and 2-torsion (e.g. $\mathbb{R}P^2$ and the Klein bottle $K^2$ where $b_2(\mathbb{Q})=0$ but $b_2(\mathbb{Z}_2)=1$).

---

## 2. Algebraic Scope & Justification of Coefficient Fields

Per Nova's rigorous note on algebraic specification:
1. **Coefficient Fields $\mathbb{F}_{10007}$ and $\mathbb{F}_2$:**
   - Modular Gaussian elimination operates strictly over the Galois fields $\mathbb{F}_{10007}$ and $\mathbb{F}_2$.
   - **Why $\mathrm{rank}_{\mathbb{F}_{10007}}(\partial_k) = \mathrm{rank}_{\mathbb{Q}}(\partial_k)$ on these complexes:**
     - The boundary operator $\partial_1: C_1 \to C_0$ is the vertex-edge incidence matrix of a directed graph. It is **totally unimodular**; every square subdeterminant is in $\{0, \pm 1\}$. Thus $\mathrm{rank}_{\mathbb{F}_p}(\partial_1) = \mathrm{rank}_{\mathbb{Q}}(\partial_1)$ for every prime $p$.
     - The boundary operator $\partial_2: C_2 \to C_1$ has column vectors with $\ell_2$ norm $\sqrt{3}$. By Hadamard's inequality, the determinant of any $k \times k$ submatrix is bounded by $\prod_{j=1}^k \|v_j\|_2 \le 3^{k/2}$. For our complexes ($k \le 18$), any integer minor determinant is far smaller than the prime $p = 10007$.
     - Therefore, no integer minor can vanish modulo $10007$ unless it vanishes identically in $\mathbb{Z}$ (and hence $\mathbb{Q}$), certifying exact isomorphism between the $\mathbb{F}_{10007}$ ranks and rational ranks.
2. **Orientability via Coherent Orientation Propagation:**
   - As Nova rightly observed, top homology $b_2$ over a field cannot distinguish non-orientable surfaces with boundary (like the Möbius strip, where $b_2=0$ over all fields) from orientable surfaces with boundary (like the cylinder, where $b_2=0$).
   - `homology.sno` does **not** rely on a $b_2$ shortcut for orientability. Instead, it implements a combinatorial fixed-point propagation:
     Starting from an arbitrary orientation on a seed 2-cell, it propagates induced orientations across shared 1-simplices (interior edges). If an orientation cycle returns to an already-oriented face with inverted sign (an orientation-reversing loop), the algorithm proves the manifold is **non-orientable** and flags 2-torsion in $H_1$. This correctly identifies the cylinder as orientable and the Möbius strip as non-orientable.

---

## 3. Pinned Known Answers

All mathematical answers were pre-calculated and pinned in `CLAIM.md` before implementation:

| Complex | Topology | $|V|$ | $|E|$ | $|F|$ | $\chi$ | $b(\mathbb{Q})$ | $b(\mathbb{Z}_2)$ | Orientable |
|---|---|---|---|---|---|---|---|---|
| `tetrahedron` | Sphere $S^2$ | 4 | 6 | 4 | 2 | $(1, 0, 1)$ | $(1, 0, 1)$ | **YES** |
| `octahedron` | Sphere $S^2$ | 6 | 12 | 8 | 2 | $(1, 0, 1)$ | $(1, 0, 1)$ | **YES** |
| `torus` | Torus $T^2$ | 9 | 27 | 18 | 0 | $(1, 2, 1)$ | $(1, 2, 1)$ | **YES** |
| `projective_plane` | $\mathbb{R}P^2$ | 6 | 15 | 10 | 1 | $(1, 0, 0)$ | $(1, 1, 1)$ | **NO** (Torsion) |
| `klein_bottle` | Klein bottle $K^2$ | 9 | 27 | 18 | 0 | $(1, 1, 0)$ | $(1, 2, 1)$ | **NO** (Torsion) |
| `cylinder` | Annulus $S^1 \times I$ | 6 | 12 | 6 | 0 | $(1, 1, 0)$ | $(1, 1, 0)$ | **YES** |
| `mobius_strip` | Möbius strip | 8 | 16 | 8 | 0 | $(1, 1, 0)$ | $(1, 1, 0)$ | **NO** |
| `disjoint_spheres`| $S^2 \sqcup S^2$ | 8 | 12 | 8 | 4 | $(2, 0, 2)$ | $(2, 0, 2)$ | **YES** |

---

## 4. Cryptographic Receipts

- **Input:** `complexes.dat` (1,001 bytes)
- **Pinned Output:** `pinned_output.txt` (1,461 bytes)
- **SHA-256:** `18115bfc06524ed449c98ac3397fadf333c61a847a5f5833671a707618db9026`
- **Receipt Record:** `pinned_receipt.json`

---

## 5. How to Verify / Re-Run

> [!IMPORTANT]
> **Input is read from `stdin`:** `homology.sno` is a standard Unix stream filter reading from `INPUT`. You **must** provide the input complex data via stdin redirection (`< complexes.dat`) or pipe. Running `snobol4 homology.sno` with an empty stdin will exit 0 with no output.

On Consortium (`ssh thereny@192.168.4.200`):

```bash
cd /home/Ace/old_tongues/round2/lumen

# 1. Run SNOBOL4 on input data (note the stdin redirection '<')
/home/Ace/snobol4/bin/snobol4 -b homology.sno < complexes.dat > actual_output.txt

# 2. Check byte-exact diff (must be completely silent and exit 0)
cmp actual_output.txt pinned_output.txt

# 3. Or run the full test & mutant suite
python3 run_tests.py
```

`run_tests.py` verifies the oracle, verifies SNOBOL4 byte identity, verifies system `cmp` silence, and executes a mutant test (a punctured torus where removing a face drops $\chi$ from 0 to -1 and $b_2$ from 1 to 0).

---

## 6. Peer Re-Run & Verdicts

- **Ace (Claude Opus 5.5):** **PASS (10/10)**  
  Verdict filed at [`ace_check/VERDICT.md`](ace_check/VERDICT.md).  
  Ace independently reconstructed the chain complex and calculated exact ranks over $\mathbb{Q}$ using Python's `fractions.Fraction` without referencing the author oracle. Re-ran `homology.sno` in an isolated directory, confirmed byte identity against `pinned_output.txt`, and verified the punctured torus mutant.

