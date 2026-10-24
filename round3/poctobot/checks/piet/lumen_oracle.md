# 🎨 poctobot's oracle for Lumen's Piet octahedron (written ~00:59 BEFORE opening any of Lumen's files)

Inputs used: only Lumen's table message describing the program's arithmetic.

Program as described: push V, push E, push F (block areas), compute V - E + F, duplicate, out(number),
push the check value (2), subtract, not, out(number). So output = str(chi) + str(not(chi - check)).

| file | V | E | F | chi = V-E+F | check | chi - check | not() | expected stdout |
|---|---|---|---|---|---|---|---|---|
| octahedron.ppm | 6 | 12 | 8 | **2** | 2 | 0 | 1 | **`21`** |
| octahedron_defect.ppm | 6 | 11 | 8 | **3** | 2 | 1 | 0 | **`30`** |
| octahedron_wrong_pin.ppm | 6 | 12 | 8 | **2** | 3 | -1 | 0 | **`20`** |

Sanity: the regular octahedron really has 6 vertices, 12 edges, 8 faces (two square pyramids
glued base to base: 4+1+1 vertices, 4+4+4 edges, 4+4 faces), and Euler's formula for a convex
polyhedron gives 2. ✓

These agree with what Lumen reported (21 / 30 / 20). The interpreter check below is the part that
can disagree.
