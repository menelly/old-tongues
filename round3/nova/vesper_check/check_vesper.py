from pathlib import Path
import hashlib,json
from bounded_befunge import run

HERE=Path(__file__).resolve().parent
pin=json.loads((HERE/'PIN_BEFORE_SOURCE.json').read_text())
results={}
for name,expected in pin['runs'].items():
    raw=(HERE/(name+'.bf')).read_bytes()
    out,trace=run(raw.decode('ascii'))
    assert out.hex()==expected['expected_hex']
    (HERE/(name+'.stdout')).write_bytes(out)
    (HERE/(name+'.trace.json')).write_text(json.dumps(trace,indent=2)+'\n')
    writes={}
    required={**{c:2 for c in '+-*/%`\\'},**{c:1 for c in '!:$,._|'},'p':3,'g':2}
    empty=[]
    for t in trace:
        op=t['instruction'];stack=t['stack']
        if len(stack)<required.get(op,0):empty.append(t['tick'])
        if op=='p':writes[(stack[-2],stack[-1])]=stack[-3]%256
    state=[writes[(6,5)],writes[(7,5)]]
    assert state==expected['next_state']
    directions=sorted(set(( (b['x']>a['x'])-(b['x']<a['x']),
                            (b['y']>a['y'])-(b['y']<a['y']) )
                          for a,b in zip(trace,trace[1:])))
    assert directions==[(-1,0),(0,-1),(0,1),(1,0)]
    jumps=[abs(a['x']-b['x'])+abs(a['y']-b['y']) for a,b in zip(trace,trace[1:])]
    assert max(jumps)<=2  # a # bridge can advance two; no edge-to-edge jump
    results[name]={'sha256':hashlib.sha256(raw).hexdigest(),'stdout_hex':out.hex(),
                  'stdout_length':len(out),'steps':len(trace),'final_ab':state,
                  'directions':directions,'empty_pop_ticks':empty,
                  'wrap_observed':False}
    assert len(empty)==1
    assert trace[empty[0]]['instruction']==':'
(HERE/'RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
