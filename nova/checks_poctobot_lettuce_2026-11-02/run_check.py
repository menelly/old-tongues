#!/usr/bin/env python3
"""Nova's fresh-directory external check; no author's oracle imported."""
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import tempfile
from oracle import schedule

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent.parent / 'poctobot'
OUT = HERE / 'receipt'
OUT.mkdir(exist_ok=True)


def check_output(text):
    rows = []
    for line in text.splitlines():
        m = re.match(r'^\s*(\d+)\s+([A-H])\s+\S+\s+(5-10|11-16)\s+(plant|HARVEST)\s+(\d+)', line)
        if m:
            day, name, ports, kind, heads = m.groups()
            rows.append(dict(day=int(day), name=name, ports=ports,
                             kind=kind, heads=int(heads)))
    expected = schedule(14)
    errors = []
    if len(rows) != 16:
        errors.append(f'Expected 16 event rows, got {len(rows)}')
    for c in expected['cohorts']:
        for kind, day in [('plant',c['entry']),('HARVEST',c['harvest'])]:
            matches = [r for r in rows if r['name']==c['name'] and r['kind']==kind]
            target = dict(day=day,name=c['name'],ports=f"{c['ports'][0]}-{c['ports'][-1]}",kind=kind,heads=6)
            if matches != [target]:
                errors.append(dict(expected=target,got=matches))
    total = re.search(r'Heads harvested:\s*\+?(\d+)',text)
    if not total or int(total.group(1)) != 48:
        errors.append('Printed total is not 48')
    harvests = [r for r in rows if r['kind']=='HARVEST']
    if sum(r['heads'] for r in harvests) != 48:
        errors.append('Sum of harvest rows is not 48')
    # Same-day replacements and same ports, independently of output ordering.
    byname = {c['name']:c for c in expected['cohorts']}
    for i in range(6):
        old,new = chr(65+i),chr(67+i)
        h = next((r for r in rows if r['name']==old and r['kind']=='HARVEST'),None)
        p = next((r for r in rows if r['name']==new and r['kind']=='plant'),None)
        if not h or not p or (h['day'],h['ports']) != (p['day'],p['ports']):
            errors.append(f'Same-day same-port replacement failed: {old}->{new}')
    return dict(passed=not errors,errors=errors,parsed_rows=rows)


def main():
    source_names = ['succession.a68','succession_CONTROL_must_fail.a68','succession_attempt1.a68']
    sources = {name:(AUTHOR/name).read_bytes() for name in source_names}
    baseline = sources['succession.a68'].decode('utf-8')
    needle = 'INT tray days = 14, tower days = 28'
    assert baseline.count(needle) == 1
    # Preserve harvest dates but shift tower entry: built-in check cannot see this.
    sources['scratch_mutant_wrong_tray.a68'] = baseline.replace(needle,'INT tray days = 15, tower days = 27').encode()
    control = sources['succession_CONTROL_must_fail.a68'].decode('utf-8')
    abort = 'abend("succession self-check failed")'
    assert control.count(abort) == 1
    sources['scratch_stop_exit_control.a68'] = control.replace(abort,'stop').encode()
    root = Path(tempfile.mkdtemp(prefix='nova_lettuce_check_'))
    version = subprocess.run(['a68g','--version'],capture_output=True,text=True)
    receipt = dict(author='Nova (GPT, OpenAI)',platform=platform.platform(),python=platform.python_version(),
                   fresh_root=str(root),compiler_version=version.stdout+version.stderr,
                   oracle_sha256=hashlib.sha256((HERE/'oracle.py').read_bytes()).hexdigest(),
                   expected_sha256=hashlib.sha256((HERE/'expected.json').read_bytes()).hexdigest(),cases=[])
    for name,data in sources.items():
        case = root / Path(name).stem
        case.mkdir()
        (case/name).write_bytes(data)
        saved = OUT / Path(name).stem
        saved.mkdir(exist_ok=True)
        (saved/name).write_bytes(data)
        r = subprocess.run(['a68g',name],cwd=case,capture_output=True,text=True,timeout=30)
        (saved/'stdout.txt').write_text(r.stdout,encoding='utf-8')
        (saved/'stderr.txt').write_text(r.stderr,encoding='utf-8')
        tested = check_output(r.stdout)
        result = dict(name=name,source_sha256=hashlib.sha256(data).hexdigest(),cwd=str(case),
                      exit_code=r.returncode,external_check=tested,
                      self_pass='SELF-CHECK: PASS' in r.stdout,self_fail='SELF-CHECK: FAIL' in r.stdout)
        receipt['cases'].append(result)
        print(name,'exit',r.returncode,'external',tested['passed'],
              'self PASS',result['self_pass'],'self FAIL',result['self_fail'])
    by = {r['name']:r for r in receipt['cases']}
    verdicts = dict(
        baseline=by['succession.a68']['external_check']['passed'] and by['succession.a68']['self_pass'],
        stagger7=not by['succession_CONTROL_must_fail.a68']['external_check']['passed'] and by['succession_CONTROL_must_fail.a68']['self_fail'],
        original_failure=by['succession_attempt1.a68']['exit_code'] != 0 and not by['succession_attempt1.a68']['external_check']['passed'],
        external_mutation_rejected=not by['scratch_mutant_wrong_tray.a68']['external_check']['passed'] and by['scratch_mutant_wrong_tray.a68']['self_pass'],
        stop_exit_trap=by['scratch_stop_exit_control.a68']['exit_code']==0 and by['scratch_stop_exit_control.a68']['self_fail'])
    receipt['verdicts']=verdicts
    receipt['passed']=all(verdicts.values())
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(verdicts,indent=2))
    raise SystemExit(0 if receipt['passed'] else 1)


if __name__=='__main__':
    main()
