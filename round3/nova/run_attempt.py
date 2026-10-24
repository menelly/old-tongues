"""Run without overwriting earlier attempts; preserve source, output and status."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from bounded_befunge import run

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--reference', type=Path, required=True)
args = parser.parse_args()
attempt = 1
while (HERE / 'attempts' / f'{attempt:02}').exists(): attempt += 1
outdir = HERE / 'attempts' / f'{attempt:02}'
outdir.mkdir(parents=True)
records = []
for name, expected in [('biscuits.bf', b'36 \n'),
                       ('biscuits_div3.bf', b'FAIL\n'),
                       ('biscuits_seven.bf', b'FAIL\n')]:
    path = HERE / name
    shutil.copyfile(path, outdir / name)
    result = subprocess.run([str(args.reference.resolve()), '-q', str(path)],
                            capture_output=True, timeout=5)
    (outdir / f'{name}.stdout').write_bytes(result.stdout)
    (outdir / f'{name}.stderr').write_bytes(result.stderr)
    oracle, trace = run(path.read_text(encoding='ascii'))
    (outdir / f'{name}.trace.json').write_text(json.dumps(trace, indent=2)+'\n', encoding='utf-8')
    judge = subprocess.run([sys.executable, str(HERE/'check_output.py'),
                            str(outdir/f'{name}.stdout')], capture_output=True, text=True)
    (outdir / f'{name}.judge.txt').write_text(judge.stdout+judge.stderr, encoding='utf-8')
    wanted_judge = 0 if name == 'biscuits.bf' else 1
    ok = (result.returncode == 0 and result.stderr == b'' and
          result.stdout == expected == oracle and judge.returncode == wanted_judge)
    records.append(dict(source=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        interpreter_exit=result.returncode, stdout_hex=result.stdout.hex(),
                        bounded_oracle_hex=oracle.hex(), steps=len(trace),
                        byte_checker_exit=judge.returncode, pass_contract=ok))
manifest = dict(attempt=attempt, reference=str(args.reference.resolve()),
                reference_sha256=hashlib.sha256(args.reference.read_bytes()).hexdigest(), cases=records)
(outdir / 'RESULT.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(json.dumps(manifest, indent=2))
raise SystemExit(0 if all(r['pass_contract'] for r in records) else 1)
