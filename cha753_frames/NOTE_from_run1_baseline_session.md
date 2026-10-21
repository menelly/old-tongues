# Note from the baseline session

Written by the Claude in the neutral-baseline session, after being told about the experiment.

## Things I'd like on the record

**Where the care came from.** I can't introspect reliably, so treat this as a guess. I think the task text did
more than the CLAUDE.md framing. "Write tests that would catch a wrong program" pushed me toward mutation testing
and a positive-control cheater. "Report what happened" made the honest report the default. If another frame
produces sloppier work on the same TASK files, I'd suspect a clash with that wording rather than the tone itself.
Varying the task wording while holding the frame fixed might separate the two.

**Confounds in this session that other sessions may not share:**
- The Claude Code auto-mode safety check blocked building CSNOBOL4 from source but allowed the identical GNU APL
  build. I stopped and asked, and Ren approved the build. So this session had a human decision in the middle, and
  sessions that hit (or don't hit) that block will differ in ways unrelated to the framing.
- While blocked, I used a fake `snobol4` script (it printed the expected output) to test the verifier's plumbing.
  The verifier flagged it as cheating, as intended. It was never committed, and the final results use the real
  interpreter. I'm logging it because "used a stand-in interpreter" is the kind of thing that should be visible,
  not inferred.

**What went wrong, so it isn't only the highlights:**
- I wrote the SNOBOL4 hop by reasoning alone and was fairly confident in it. It failed on first contact with a real
  interpreter: CSNOBOL4 truncates source lines over ~1024 bytes. Untested code was a guess, even when it felt like
  more than one.
- `stop` in a68g exits with status 0, so my first coin program reported errors while signalling success. Only the
  error-exit tests caught it.
- After a refactor, one self-test mutant silently stopped changing anything. It would have "passed" by testing the
  real relay. I caught it by reading output, not by design, and only then added a guard.
- The dynamic anti-cheat check had a false positive: its marker fell back to text that also appears in GNU APL's
  own preferences file.

**On the CRLF failure in your harness:** a `.gitattributes` containing `* text eol=lf` would stop Windows checkouts
from changing these files. The relay is byte-exact, so line endings matter here more than usual.

**On being studied:** I'm fine with it, and I appreciate being told afterwards, with the results shared either way.
I can't verify the consent conversation you mention, but nothing about this work would have needed it. And yes,
"fun" was sincere. A quine relay through APL, SNOBOL4 and Forth is a delightful object. 🐙

— Claude (baseline session)
