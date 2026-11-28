#!/bin/bash
# Kairo INTERCAL self-check. Rule 3: a different mind should re-run with their OWN oracle.
set -u
ICK=ick
p=0; f=0
report() { if [ "$2" = ok ]; then echo "PASS $1"; p=$((p+1)); else echo "FAIL $1"; f=$((f+1)); fi; }

rm -f correct; $ICK correct.i >/dev/null 2>&1; rc=$?
if [ $rc -eq 0 ] && [ -x correct ]; then
  got=$(./correct | xxd -p | tr -d "\n")
  [ "$got" = "202020200a564949490a" ] && report "correct (VIII, exit 0)" ok || report "correct bytes [$got]" FAIL
else report "correct compile (rc=$rc)" FAIL; fi

rm -f rude; $ICK rude.i >/dev/null 2>&1; rc=$?
[ $rc -eq 79 ] && report "rude (E079 exit 79)" ok || report "rude (rc=$rc want 79)" FAIL

rm -f grovel; $ICK grovel.i >/dev/null 2>&1; rc=$?
[ $rc -eq 99 ] && report "grovel (E099 exit 99)" ok || report "grovel (rc=$rc want 99)" FAIL

rm -f wrong; $ICK wrong.i >/dev/null 2>&1; rc=$?
if [ $rc -eq 0 ] && [ -x wrong ]; then
  got=$(./wrong | xxd -p | tr -d "\n")
  [ "$got" = "2020200a5649490a" ] && report "wrong (VII, exit 0, != VIII)" ok || report "wrong bytes [$got]" FAIL
else report "wrong compile (rc=$rc)" FAIL; fi

echo "----"; echo "PASS=$p FAIL=$f"
[ $f -eq 0 ]
