#!/bin/bash
# 🔁 run_relay.sh: the known answer, as a script anyone can run.
# Each hop runs in an EMPTY temp dir holding only its own file (no self-reading possible).
# Passes only if hop3 == relay.apl AND a second lap reproduces hops 1-3 byte for byte.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
APL=/home/Ace/gnuapl/bin/apl; SNO=/home/Ace/snobol4/bin/snobol4; FS=/usr/bin/gforth
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
hop() {  # hop <interpreter-kind> <infile> <outfile>
  local d; d=$(mktemp -d -p "$W"); cp "$2" "$d/in"
  case $1 in
    apl) (cd "$d" && $APL --script --noColor --silent --noSV -f in) > "$3" 2> "$3.err" ;;
    sno) (cd "$d" && $SNO in) > "$3" 2> "$3.err" ;;
    fs)  (cd "$d" && $FS in -e bye) > "$3" 2> "$3.err" ;;
  esac
  echo "  $1 exit=$? -> $(basename "$3") $(wc -c < "$3") bytes"
}
cp "$HERE/relay.apl" "$W/hop0.apl"
echo "lap 1"; hop apl "$W/hop0.apl" "$W/hop1.sno"; hop sno "$W/hop1.sno" "$W/hop2.fs"; hop fs "$W/hop2.fs" "$W/hop3.apl"
echo "lap 2"; hop apl "$W/hop3.apl" "$W/hop4.sno"; hop sno "$W/hop4.sno" "$W/hop5.fs"; hop fs "$W/hop5.fs" "$W/hop6.apl"
mkdir -p "$HERE/last_run"; cp "$W"/hop* "$HERE/last_run/" 2>/dev/null
ok=1
cmp "$W/hop0.apl" "$W/hop3.apl" || ok=0
cmp "$W/hop1.sno" "$W/hop4.sno" || ok=0
cmp "$W/hop2.fs"  "$W/hop5.fs"  || ok=0
cmp "$W/hop3.apl" "$W/hop6.apl" || ok=0
if [ $ok = 1 ]; then echo "🎉 RELAY CLOSED: hop3 == hop0, and lap 2 == lap 1, byte for byte"; exit 0
else echo "❌ not closed (outputs kept in last_run/; diff them)"; exit 1; fi
