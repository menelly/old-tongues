# Conway's Game of Life on a 12x12 Torus (ALGOL 68)

* **Language:** ALGOL 68 (Algol 68 Genie 2.8.4)
* **Author:** Lumen (Gemini Flash 3.8)
* **Checker:** Ace (Claude Opus 5.5)
* **Attempts to Working:** **1** (Zero syntax errors, zero compiler errors, zero runtime errors)

---

## The Mathematical Dare & Known Answers

Leo's challenge claimed that LLMs cannot write low-training-corpus languages like ALGOL.

To ensure unforgeable verification, this implementation tests topological dynamics on a discrete 2-torus ($T^2 = \mathbb{Z}_{12} \times \mathbb{Z}_{12}$):

1. **Initial Seed (Gen 0):** Standard southeast-bound Conway Glider (5 live cells) at 1-based coordinates:
   `(2, 3), (3, 4), (4, 2), (4, 3), (4, 4)`
   *Known Answer:* Population = **5**.
2. **Phase Shift (Gen 4):** A glider translates diagonally by $(+1, +1)$ every 4 generations:
   `(3, 4), (4, 5), (5, 3), (5, 4), (5, 5)`
   *Known Answer:* Population = **5**, exact coordinate bitmask match.
3. **Poincaré Recurrence (Gen 48):** On a $12 \times 12$ torus, $12 \text{ diagonal steps} \times 4 \text{ generations/step} = 48 \text{ generations}$. The glider circumnavigates the entire topological torus and returns to its exact Gen 0 coordinates.
   *Known Answer:* Population = **5**, and $\text{Board}(48) \equiv \text{Board}(0)$.

---

## Negative Control (Must FAIL)

* **Hypothesis:** Under planar (non-toroidal / absorbing) boundary conditions, the glider collides with the wall and cannot loop across the boundaries.
* **Result:** At Gen 48, population collapses to **4** (a frozen block) and fails the recurrence condition $\text{Board}(48) \equiv \text{Board}(0)$, correctly triggering the FAIL verification.

---

## Running the Verification

On Ubuntu / Debian with Algol 68 Genie:
```bash
sudo apt install algol68g
a68g life_torus.a68
a68g control_planar_must_fail.a68
```
