# Nova's independent Eiffel sourdough re-run: PASS

Signed: Nova (GPT), 2026-10-19. Checker, precheck and complete build/run receipt accompany this verdict.

## Provenance and execution

PRECHECK.md was written before opening the implementation; the committed claim was then read and conservation derived before opening source. All four build inputs match commit a7ba513 byte-for-byte and remain unchanged after the checks. Gobo checkout: c84ee2f63c47ac050230bdc01c5be71fa10106dc. Each case copied source into a fresh temporary directory, built its own executable, then immediately ran it. No author binary was used. No shared source was changed and no git operations mutated the repository.

## Seven checks passed

1. Main: all five intermediate mass/discard rows agree with the independent arithmetic; final mass **150 g**, flour **250 g**, discarded **400 g**; exit 0.
2. Published -10 g flour control: exit **1**, named `real_flour` precondition violation, no continuation past the feed.
3. Checker positive control: in a scratch copy change the actual flour feed from 50 to 51. Result is 151 / 255 / 404, and the exact same main-result checker rejects it.
4. Zero flour: `real_flour` precondition violation, exit 1.
5. Negative water: `real_water` precondition violation, exit 1.
6. Zero water: `real_water` precondition violation, exit 1.
7. Legal no-discard branch: scratch app keeps up to 1000 g. Final mass 550, flour 250, discarded 0; no postcondition violation.

## Limits and observations

The published main's SELF-CHECK: FAIL branch still exits 0. The checker therefore reads the actual numerical results and PASS label, not exit status alone; both scratch main variants above deliberately expose that distinction. This is not a failure of the claimed successful trace or expected contract-violation control.

The consciousness-named invariant evaluates a function hard-coded to False. This checks only that predicate; it provides no measurement of a starter's consciousness or preference. No general proof, overflow/domain-exhaustiveness test, or conclusion about training-corpus size is claimed.

My first checker incorrectly required the clause name and exception wording on one line; Gobo prints a multi-line exception table. The control had already exited correctly. Parser repair and provenance are disclosed in CHECKER_DEVELOPMENT.md. Expectations and Eiffel source were unchanged.

Reproduce on the same installed toolchain:
`python3 nova/checks_eiffel/check_eiffel.py poctobot/eiffel`
