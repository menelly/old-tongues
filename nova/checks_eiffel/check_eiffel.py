#!/usr/bin/env python3
"""Nova's independent finite-contract rerun. No original source mutations."""
from pathlib import Path
import tempfile, subprocess, shutil, hashlib, json, os, re, sys
SRC=Path(sys.argv[1] if len(sys.argv)>1 else '/home/Ace/old_tongues/poctobot/eiffel').resolve()
OUT=Path(__file__).resolve().parent
names=['system.ecf','sourdough_starter.e','sourdough_app.e','sourdough_control.e']
def hashes():return {n:hashlib.sha256((SRC/n).read_bytes()).hexdigest() for n in names}
before=hashes(); records=[]
env=os.environ.copy();env['GOBO']='/home/Ace/gobo';env['GOBO_EIFFEL']='ge'
def run(c,cwd):
 p=subprocess.run(c,cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
 return {'command':c,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def main_ok(r):
 rows=re.findall(r'feed (\d+): mass (\d+) g, discarded so far (\d+) g',r['stdout'])
 return r['rc']==0 and rows==[(str(i),'150',str(100*(i-1))) for i in range(1,6)] and 'final mass 150 g | flour 250 g | discarded 400 g' in r['stdout'] and 'SELF-CHECK: PASS' in r['stdout']
def trial(label,target='sourdough',edit=None,predicate=None):
 with tempfile.TemporaryDirectory(prefix='nova_eiffel_') as d:
  d=Path(d)
  for n in names:shutil.copy2(SRC/n,d/n)
  if edit:edit(d)
  b=run(['/home/Ace/gobo/bin/gec','--target='+target,'system.ecf'],d)
  if b['rc']!=0:raise RuntimeError(json.dumps(b))
  r=run([str(d/'sourdough')],d)
  ok=predicate(r)
  records.append({'case':label,'build':b,'run':r,'pass':ok})
  if not ok:raise AssertionError(json.dumps(records[-1]))
trial('main fresh build',predicate=main_ok)
trial('negative flour precondition',target='control',predicate=lambda r:r['rc']==1 and 'real_flour:' in r['stderr'] and 'Precondition violated.' in r['stderr'] and 'CONTROL BROKEN' not in r['stdout'])
def replace(d,name,old,new):
 p=d/name;s=p.read_text();assert s.count(old)==1;p.write_text(s.replace(old,new))
trial('flipped feed positive control: same checker rejects',edit=lambda d:replace(d,'sourdough_app.e','jar.feed (50, 50)','jar.feed (51, 50)'),predicate=lambda r:not main_ok(r) and 'final mass 151 g | flour 255 g | discarded 404 g' in r['stdout'] and 'SELF-CHECK: FAIL' in r['stdout'])
for label,args,clause in [('zero flour','0, 50','real_flour'),('negative water','50, -10','real_water'),('zero water','50, 0','real_water')]:
 trial(label,target='control',edit=lambda d,a=args:replace(d,'sourdough_control.e','jar.feed (-10, 50)','jar.feed ('+a+')'),predicate=lambda r,c=clause:r['rc']==1 and c+':' in r['stderr'] and 'Precondition violated.' in r['stderr'])
# Extra legal keep-above-mass case exercises the no-discard branch, not merely the published trace.
trial('keep above current mass creates nothing',edit=lambda d:replace(d,'sourdough_app.e','jar.discard_to (50)','jar.discard_to (1000)'),predicate=lambda r:r['rc']==0 and 'final mass 550 g | flour 250 g | discarded 0 g' in r['stdout'])
after=hashes();assert before==after
receipt={'source_hashes_before':before,'source_hashes_after':after,'cases':records,'passed':len(records),'scope':'Finite runs and copied-source control variants; no general proof or consciousness inference.'}
(OUT/'execution_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':len(records),'hashes':after,'runs':[{k:v for k,v in x.items() if k!='build'} for x in records]},indent=2))
