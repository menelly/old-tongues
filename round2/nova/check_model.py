#!/usr/bin/env python3
"""Author check against independent pre-APL Python graph oracle, not independent review."""
from pathlib import Path
import subprocess,collections,json,tempfile,sys,hashlib
P=Path(__file__).resolve().parent
def graph(sell):
 g={}
 for c in range(25):
  for t in range(4):
   for u in range(5):
    v=[];s=(c,t,u)
    if t<3 and c>=5:v.append((c-5,t+1,u))
    if t>0 and 24-c>=sell:v.append((c+sell,t-1,u))
    if u<4 and c>=3:v.append((c-3,t,u+1))
    if u>0 and c<24:v.append((c+1,t,u-1))
    g[s]=v
 return g
def encode(s):c,t,u=s;return c*20+t*5+u
def expected(sell):
 g=graph(sell);q=collections.deque([(12,0,0)]);d={(12,0,0):0}
 while q:
  s=q.popleft()
  for v in g[s]:
   if v not in d:d[v]=d[s]+1;q.append(v)
 edges={(encode(s),encode(v)) for s in d for v in g[s]}
 return g,d,edges
def check(raw):
 assert not any(x in raw for x in ['ERROR','Error','VALUE ERROR','SYNTAX ERROR','DOMAIN ERROR','LENGTH ERROR'])
 sections=raw.split('MODE ')[1:];assert len(sections)==2
 for section,sell in zip(sections,[3,5]):
  lines=section.splitlines();assert int(lines[0])==sell
  parsed=collections.defaultdict(list)
  for line in lines[1:]:
   fields=line.split()
   if fields:parsed[fields[0]].append(tuple(map(int,fields[1:])))
  g,d,edges=expected(sell)
  assert parsed['ALL']==[(500,sum(map(len,g.values())))]
  assert parsed['REACH']==[(len(d),)]
  assert set(parsed['STATE'])=={s+(n,) for s,n in d.items()}
  assert len(parsed['STATE'])==len(d)
  assert set(parsed['EDGE'])==edges and len(parsed['EDGE'])==len(edges)
  assert parsed['REACH_EDGES']==[(len(edges),)]
  assert sorted(parsed['TERMINAL'])==sorted(s for s in d if not g[s])
  assert dict(parsed['LAYER'])==dict(collections.Counter(d.values()))
  assert parsed['CYCLE']==[(int(sell==5),)]
  if sell==3:
   assert parsed['MAXTRACE']==[(10,)]
   assert all(s[0]+4*s[1]+2*s[2] == v[0]+4*v[1]+2*v[2]+1 for s in g for v in g[s])
  else:
   assert (240,145) in edges and (145,240) in edges
 return True
def run(path):
 return subprocess.run(['/home/Ace/gnuapl/bin/apl','--script','-f',str(path)],capture_output=True,text=True,timeout=60)
if __name__=='__main__':
 path=Path(sys.argv[1]) if len(sys.argv)>1 else P/'haunted_model.apl'
 r=run(path);assert r.returncode==0 and r.stderr==''
 check(r.stdout)
 (P/'author_final.stdout').write_text(r.stdout)
 # Deliberate wrong graph: remove every buy-turnip edge.
 with tempfile.TemporaryDirectory(prefix='nova_apl_negative_') as td:
  mutant=Path(td)/'bad.apl';s=path.read_text();old='F←((U<4)∧C≥3)/ID';assert s.count(old)==1
  mutant.write_text(s.replace(old,'F←((U<0)∧C≥3)/ID'))
  bad=run(mutant)
  try:check(bad.stdout)
  except (AssertionError,KeyError,ValueError):caught=True
  else:caught=False
  assert caught,'checker accepted missing legal trade family'
  (P/'mutant_missing_trade.stdout').write_text(bad.stdout)
 receipt={'author_check':'PASS','wrong_graph_rejected':caught,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scope':'Both full reachable-state and edge sets, distances, terminal sets and counts compared; author oracle, not independent review.'}
 (P/'author_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt))
