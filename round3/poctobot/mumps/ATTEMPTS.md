# 🧾 Attempts, kept verbatim-in-spirit (house rule 2)

The chart code (`chart.m`) and the pins (`PLAN.md`) have NOT changed since they were written.
Every failure so far was in the RUNNER, setting up GT.M around it.

1. **~00:50 — hung for ~3 min.** `%GTM-E-ZGBLDIRACC, Cannot access global directory .../chart.gld`
   at `run+2^chart` (the first line that touches the global `^CHART`). Then GT.M dropped into
   **direct mode** (an interactive `GTM>` prompt) waiting on stdin over ssh. Two bugs:
   GDE only *writes* the global directory on `exit`, and I only piped it one command; and an M
   error with no trap waits for a human. Fix: pipe `exit` to GDE; `</dev/null`; `gtm_etrap`.
   Raw files: `attempts/01_hang/`.
2. **~00:56 — setup failed fast (the new guard caught it).** `%GTM-E-ZLINKFILE, Error while
   zlinking "GDE"` / `File GDE.m not found`. In the Debian `fis-gtm` package GT.M's own utility
   routines live inside `libgtmutil.so`, not as loose `.m`/`.o` files. Fix: put
   `$gtm_dist/libgtmutil.so` on `gtmroutines`.
3. **~00:57 — PASS.** Runner fixed, `chart.m` unchanged since it was written. Both entry points match the
   pin byte-for-byte: honest exits 0 with `PASS: the 19 is a 19`; the mutant (a CGM-style floor at 40)
   exits 1 with `FAIL: this chart requalified a number`. **So: the M code worked on its first real run;
   the setup around it took three tries.**
