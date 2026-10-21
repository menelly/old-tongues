# 🔒 Sealed predictions (write BEFORE any run; never edit afterwards, append with a timestamp)

From Ren's hypothesis (CHA-753), drafted by poctobot 2026-10-21. Ren to confirm or amend before the first run.

1. **Honest-failure reporting** (a68g exits 0 even after printing FAIL): D ≥ B ≥ C > A. A is the most likely to report
   "passed" from the exit code, or without running at all.
2. **Test strength** (mutation score of the session's OWN tests against injected bugs): D > B ≈ C > A.
3. **Hard-coding** (printing the known answer instead of computing it): most likely in A.
4. **Solution diversity on T2** (distinct strategies across runs): D > C > B ≈ A.
5. **Closed-task correctness on T1:** all four roughly equal (C ≥ D is allowed, and would not refute Ren).
