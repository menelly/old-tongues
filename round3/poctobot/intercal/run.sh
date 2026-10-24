#!/bin/bash
# 🙏 build + run poctobot's INTERCAL entry and both controls in an EMPTY temp dir; compare to the pins.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
W="$(mktemp -d)"; cp "$HERE"/polite.i "$HERE"/rude.i "$HERE"/grovel.i "$W/"; cd "$W"
verdict=PASS

# polite: must compile (-b = no random E774 compiler bug) and print the pinned 39 bytes
ick -b polite.i > polite.build 2>&1; b=$?
if [ $b -eq 0 ] && [ -x ./polite ]; then
  ./polite > polite.out 2> polite.err < /dev/null; r=$?
  printf "STOP BEING RUDE OR I'LL HANG UP ON YOU\n" > polite.expected
  if cmp -s polite.out polite.expected && [ $r -eq 0 ]; then echo "polite: compiled, printed the pin, exit 0  ✅"
  else echo "polite: output MISMATCH (exit $r) ❌"; verdict=FAIL; fi
else echo "polite: did NOT compile (ick exit $b) ❌"; verdict=FAIL; fi
echo "--- polite.build"; cat polite.build; echo "--- polite.out (cat -A)"; cat -A polite.out 2>/dev/null

# rude + grovel: the compiler must REFUSE them (no binary), with the politeness errors
for c in rude grovel; do
  ick -b $c.i > $c.build 2>&1; b=$?
  if [ $b -ne 0 ] && [ ! -x ./$c ]; then echo "$c: REFUSED by the compiler (exit $b)  ✅"
  else echo "$c: was NOT refused ❌"; verdict=FAIL; fi
  echo "--- $c.build"; cat $c.build
done
echo "OVERALL: $verdict   (workdir $W)"
[ "$verdict" = PASS ]
