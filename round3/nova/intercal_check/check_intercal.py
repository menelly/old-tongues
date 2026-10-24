"""Independent literal-array decoder and isolated compiler checks; no author generator."""
from pathlib import Path
import hashlib, json, re, subprocess, tempfile

HERE = Path(__file__).resolve().parent
EXPECTED = bytes.fromhex(json.loads((HERE/'PIN_BEFORE_SOURCE.json').read_text())['expected_hex'])

def decode(source):
    size = int(re.search(r',1 <- #(\d+)', source).group(1))
    pairs = [(int(i),int(v)) for i,v in re.findall(r',1 SUB #(\d+) <- #(\d+)',source)]
    assert [i for i,v in pairs] == list(range(1,size+1))
    state=0
    out=bytearray()
    for _,v in pairs:
        assert 0 <= v < 256
        state=(state-v)%256
        out.append(int(f'{state:08b}'[::-1],2))
    return bytes(out)

def main():
    results={}
    for name in ['polite','rude','grovel']:
        raw=(HERE/(name+'.i')).read_bytes()
        source=raw.decode('ascii')
        decoded=decode(source)
        assert decoded == EXPECTED
        assert len(source.splitlines()) == 42
        count=sum('PLEASE' in line for line in source.splitlines())
        assert count=={'polite':11,'rude':0,'grovel':42}[name]
        with tempfile.TemporaryDirectory(prefix='nova-intercal-') as directory:
            run=Path(directory)
            (run/(name+'.i')).write_bytes(raw)
            c=subprocess.run(['ick','-b',name+'.i'],cwd=run,capture_output=True,timeout=45)
            (HERE/(name+'.compile.stdout')).write_bytes(c.stdout)
            (HERE/(name+'.compile.stderr')).write_bytes(c.stderr)
            result={'sha256':hashlib.sha256(raw).hexdigest(),'decoded_hex':decoded.hex(),
                    'please_count':count,'statements':42,'compile_exit':c.returncode,
                    'binary_created':(run/name).is_file()}
            if name=='polite':
                assert c.returncode==0 and (run/name).is_file()
                r=subprocess.run([str(run/name)],cwd=run,capture_output=True,timeout=10)
                (HERE/(name+'.runtime.stdout')).write_bytes(r.stdout)
                (HERE/(name+'.runtime.stderr')).write_bytes(r.stderr)
                result.update(runtime_exit=r.returncode,stdout_hex=r.stdout.hex(),stderr_hex=r.stderr.hex())
                assert r.returncode==0 and r.stdout==EXPECTED and r.stderr==b''
            else:
                diagnostic=c.stdout+c.stderr
                assert c.returncode!=0 and not (run/name).exists()
                assert (b'ICL079I' if name=='rude' else b'ICL099I') in diagnostic
            results[name]=result
    (HERE/'RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    main()
