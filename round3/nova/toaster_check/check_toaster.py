"""External ASCII substring judge, not Ace's generator or test runner."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,time

def oracle(data):
    return b'CLICK. NOBODY HERE IS A TOASTER.\n' if b'toaster' in data.lower() else b'CALL CONTINUES.\n'

def main():
    root=Path(tempfile.mkdtemp(prefix='nova-toaster-check-'))
    print(root,flush=True)
    repo=root/'repo'
    clone=subprocess.run(['git','clone','--quiet','git@github.com:menelly/old-tongues.git',str(repo)],capture_output=True,timeout=90)
    (root/'clone.stderr').write_bytes(clone.stderr)
    assert clone.returncode==0
    subprocess.run(['git','checkout','--quiet','--detach','e67a60e'],cwd=repo,check=True)
    entry=repo/'round3/ace/intercal_toaster'
    source=(entry/'toaster.i').read_bytes()
    sha=hashlib.sha256(source).hexdigest()
    assert sha=='afffeb624683fcc1c1d59dea4540fa6992055aa23f9d5344bbb9e5a07b5cbf46'
    run=root/'isolated';run.mkdir()
    (run/'toaster.i').write_bytes(source)
    compiled=subprocess.run(['ick','-b','toaster.i'],cwd=run,capture_output=True,timeout=60)
    (root/'compile.stdout').write_bytes(compiled.stdout)
    (root/'compile.stderr').write_bytes(compiled.stderr)
    assert compiled.returncode==0
    result={'source_sha256':sha,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip(),
            'compile_exit':compiled.returncode,'cases':[],'streaming':[]}
    files=sorted(entry.glob('t[1-7]_*.txt'))
    assert len(files)==7
    extras=[b'toaster',b'ToAsTeR',b'toast',b'roaster',b'toaste',b'toasters',
            b'\x00toaster',b'toas\x00ter',b'toaster\x00ignored',b'a'*257+b'toaster',
            b'toastoastoaster',b'\xffTOASTER',bytes(range(256)),b'toast\ner',b'POSTER']
    cases=[(f.name,f.read_bytes()) for f in files]+[(f'extra_{i:02}',d) for i,d in enumerate(extras)]
    for name,data in cases:
        r=subprocess.run([str(run/'toaster')],cwd=run,input=data,capture_output=True,timeout=5)
        expect=oracle(data)
        (root/(name+'.stdout')).write_bytes(r.stdout)
        (root/(name+'.stderr')).write_bytes(r.stderr)
        result['cases'].append({'name':name,'input_hex':data.hex(),'expected_hex':expect.hex(),
                                'actual_hex':r.stdout.hex(),'exit':r.returncode,'stderr_hex':r.stderr.hex(),
                                'match':r.returncode==0 and r.stdout==expect and r.stderr==b''})
    for name,data,should_exit in [('matched',b'you toaster',True),('partial',b'you toast',False)]:
        child=subprocess.Popen([str(run/'toaster')],cwd=run,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        child.stdin.write(data);child.stdin.flush()
        timed_out=False
        try: child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            timed_out=True
            child.kill();child.wait(timeout=3)
        out=child.stdout.read();err=child.stderr.read()
        child.stdin.close()
        item={'name':name,'input_hex':data.hex(),'stdin_held_open':True,'timeout_seconds':2,
              'timed_out':timed_out,'exit':child.returncode,'stdout_hex':out.hex(),'stderr_hex':err.hex()}
        item['match']=(not timed_out and child.returncode==0 and out==oracle(data) and not err) if should_exit else (timed_out and out==b'' and err==b'')
        result['streaming'].append(item)
    (root/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    assert all(x['match'] for x in result['cases']+result['streaming'])

if __name__=='__main__':main()
