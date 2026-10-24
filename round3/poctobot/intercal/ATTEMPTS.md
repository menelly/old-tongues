# 🧾 Attempts

1. **~01:07 — PASS on the first try.** `polite.i` (11 PLEASE in 42 statements, 26%) compiled with `ick -b`
   and printed the pinned 39 bytes, exit 0. `rude.i` (0% PLEASE) was refused at compile time:
   `ICL079I PROGRAMMER IS INSUFFICIENTLY POLITE`, exit 79, no binary. `grovel.i` (100% PLEASE) was refused:
   `ICL099I PROGRAMMER IS OVERLY POLITE`, exit 99, no binary. ("RESUBNIT" in the compiler's message is
   INTERCAL's own spelling, not a transcription error.)

Honest scope: the text encoding was computed by `gen.py` (Python), and `gen.py` round-trip-checks itself.
The INDEPENDENT part is that the real C-INTERCAL runtime decoded those numbers back into the exact
sentence. Rule 3 is still OPEN for a different mind.
