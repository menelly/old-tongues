from pathlib import Path
import subprocess,json,tempfile,sys
p=Path(__file__).resolve().parent
s=(p/sys.argv[1]).read_text()
templates=[s,"* quote ' slash \\ double \" test\n        D = ''\n@@\nEND\n",': dummy ;\n@@\nbye\n']
b=''.join(t+'=====HOP=====\n' for t in templates).encode()
program=s.replace('@@\n',''.join('B'+chr(8592)+'B,'+' '.join(map(str,b[i:i+20]))+'\n' for i in range(0,len(b),20)))
expected=templates[1].replace('@@\n',''.join("        D = D '"+' '.join(map(str,b[i:i+20]))+" '\n" for i in range(0,len(b),20))).encode()
with tempfile.TemporaryDirectory(prefix='nova_relay_fixture_') as d:
 f=Path(d)/'fixture.apl';f.write_text(program)
 r=subprocess.run(['/home/Ace/gnuapl/bin/apl','--script','-f',str(f)],cwd=d,capture_output=True,timeout=30)
label=sys.argv[1].replace('.apl','')
(p/(label+'.stdout')).write_bytes(r.stdout)
(p/(label+'.stderr')).write_bytes(r.stderr)
(p/(label+'.expected')).write_bytes(expected)
print(json.dumps({'rc':r.returncode,'match':r.stdout==expected,'stderr':r.stderr.decode(errors='replace'),'lengths':[len(r.stdout),len(expected)]}))
assert r.stdout==expected and r.returncode==0 and not r.stderr
