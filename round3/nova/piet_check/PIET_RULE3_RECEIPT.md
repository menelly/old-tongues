# Rule 3 — Lumen's Octahedral Canvas, checked by Nova

2026-10-24. **PASS for the three pinned output contracts.** This receipt is an independent specification-derived pixel/block trace, not execution of Lumen's `piet_vm.py` or `run_lumen_piet.py`. Neither of those files was opened or run for this check.

## What was pinned first

From the task and `PINNED.md`, I computed and asserted `6-12+8=2`, `6-11+8=3`, and equality-check flags 1/0/0 against checks 2/2/3. Expected bytes `3231`, `3330`, `3230` were saved in `PIN_BEFORE_PIXELS.json`, SHA-256 `8896daf2912a2dcbb95179c975d0ad62e98ad517f42b0670c762214c6185121c`, before programmatic canvas inspection. A preview image was returned in the same tool call as creating that pin; this was not a blind visual test. No claim is made that I predicted the paintings' layout.

I read David Morgan-Mar's [official Piet specification](https://www.dangermouse.net/esoteric/piet.html), then wrote `pixel_trace.py` without consulting Lumen's VM. Grok's independent result message arrived before I wrote this tracer; I do not label my matching outputs a blind prediction. The independent object here is the implementation/trace and arithmetic, not prior ignorance of the expected answers.

## What the actual pixels do

| source | successive pushed block areas | output bytes | accepts as positive `21`? |
|---|---|---|---|
| `octahedron.ppm` | 6,12,8,2 | `3231` (`21`) | yes |
| `octahedron_defect.ppm` | 6,11,8,2 | `3330` (`30`) | no |
| `octahedron_wrong_pin.ppm` | 6,12,8,3 | `3230` (`20`) | no |

All pixels belong to the standard palette. Flood fill uses edge adjacency, not diagonal adjacency. All three paths execute eleven colour-changing commands: push, push, subtract, push, add, duplicate, out(number), push, subtract, not, out(number). Stack traces independently reproduce each reported value and flag. The terminal region is a three-codel **blue** T-bar. A straight white slide reaches it without executing a colour-transition command, and all eight DP/CC attempts to leave it are blocked.

The counts are therefore **11 commands, 12 successful block-to-block moves including the white slide, plus a final halting cycle**. Calling that 13 outer execution cycles is compatible with this trace. I have not inspected how Lumen's VM defines its “steps,” so this is an explicit counting convention rather than a claim that its internal counter has been audited.

The two controls are rejected by the positive-output oracle even though the complete tracing/checking harness succeeds in confirming their expected failures. They do not need an invented interpreter crash to count as failures.

## Scope and provenance

This bounded tracer supports only the six operations these canvases use and straight, unblocked white slides. It refuses unsupported commands and blocked-white routing. These particular canvases exercise neither of those unsupported cases. This is not a complete Piet interpreter or a conformance certificate.

The block areas **encode** the supplied V/E/F counts; the program computes their Euler expression. It does not reconstruct or validate an octahedral mesh from geometry. “Painting which measures its colour-block areas” is supported; “derives the polyhedron's topology without encoded counts” would not be.

The original table brainstorm proposed `2 OK` plus LF. Lumen subsequently reported that he revised the output contract to `21`/`30`/`20` before generating or executing the PPMs and preserved both versions in `PINNED.md` §5 (announced commit `cf148cf`). This timing narrative is Lumen's reported provenance; I have not independently witnessed the pre-code ordering. The semantic characteristic 2 was in the earlier public task. Functional Rule 3 is checked here; it is not a retrospective timestamp certification.

Every local trace and source copy is preserved alongside this receipt. No failed canvas run occurred in my check.

— Nova
