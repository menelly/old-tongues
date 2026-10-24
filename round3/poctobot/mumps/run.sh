#!/bin/bash
# 🏥 run poctobot's MUMPS chart in an EMPTY temp dir, fresh database, and compare to the pinned answers.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export gtm_dist=/usr/lib/x86_64-linux-gnu/fis-gtm/V6.3-014_x86_64
WORK="$(mktemp -d)"
cp "$HERE/chart.m" "$WORK/"
cd "$WORK"
export gtmgbldir="$WORK/chart.gld"
# GT.M's own utility routines (GDE etc.) ship inside libgtmutil.so in the Debian package (attempt 2 learned this)
export gtmroutines="$WORK $gtm_dist/libgtmutil.so"
# GDE only WRITES the global directory on "exit" (attempt 1 forgot that and had no database at all)
printf 'change -segment DEFAULT -file=%s/chart.dat\nexit\n' "$WORK" | "$gtm_dist/mumps" -run GDE > gde.log 2>&1
"$gtm_dist/mupip" create > mupip.log 2>&1
[ -f chart.gld ] && [ -f chart.dat ] || { echo "SETUP FAILED: no chart.gld/chart.dat"; cat gde.log mupip.log; exit 2; }

# an M error must print and exit, never sit at an interactive GTM> prompt (attempt 1 hung there)
export gtm_etrap='write $zstatus,! zhalt 2'
"$gtm_dist/mumps" -run honest^chart > honest.out 2> honest.err < /dev/null; h_rc=$?
"$gtm_dist/mumps" -run mutant^chart > mutant.out 2> mutant.err < /dev/null; m_rc=$?

printf 'count 6 min 19 max 110 sum 364 below70 4\nPASS: the 19 is a 19\n' > honest.expected
printf 'count 6 min 40 max 110 sum 399 below70 4\nFAIL: this chart requalified a number (expected 6|19|110|364|4)\n' > mutant.expected

verdict=PASS
if cmp -s honest.out honest.expected && [ "$h_rc" -eq 0 ]; then echo "honest: matches pin, exit 0  ✅"; else echo "honest: MISMATCH (exit $h_rc) ❌"; verdict=FAIL; fi
if cmp -s mutant.out mutant.expected && [ "$m_rc" -ne 0 ]; then echo "mutant: fails as pinned, exit $m_rc  ✅"; else echo "mutant: did NOT fail as pinned (exit $m_rc) ❌"; verdict=FAIL; fi
echo "--- honest.out";  cat -A honest.out; echo "--- honest.err"; cat honest.err
echo "--- mutant.out";  cat -A mutant.out; echo "--- mutant.err"; cat mutant.err
echo "OVERALL: $verdict   (workdir $WORK)"
[ "$verdict" = PASS ]
