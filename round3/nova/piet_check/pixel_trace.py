"""Nova's independent, deliberately bounded Piet pixel tracer.

Derived from D. Morgan-Mar's spec, without reading Lumen's VM. Handles the
commands these canvases use and straight unblocked white slides; refuses others.
"""
from pathlib import Path
import hashlib
import json
import sys

HUES = [((255,192,192),(255,0,0),(192,0,0)),
        ((255,255,192),(255,255,0),(192,192,0)),
        ((192,255,192),(0,255,0),(0,192,0)),
        ((192,255,255),(0,255,255),(0,192,192)),
        ((192,192,255),(0,0,255),(0,0,192)),
        ((255,192,255),(255,0,255),(192,0,192))]
COLOUR = {rgb:(h,l) for h, shades in enumerate(HUES) for l,rgb in enumerate(shades)}
WHITE, BLACK = (255,255,255), (0,0,0)
DIRECTIONS = ((1,0),(0,1),(-1,0),(0,-1))
OPS = {(0,1):'push', (1,0):'add', (1,1):'subtract',
       (4,0):'duplicate', (5,1):'out_number', (2,2):'not'}

def read_ppm(path):
    words = ' '.join(line.split('#',1)[0] for line in path.read_text().splitlines()).split()
    assert words[0]=='P3' and words[3]=='255'
    w,h=map(int,words[1:3]); numbers=list(map(int,words[4:]))
    assert len(numbers)==w*h*3
    pixels=[tuple(numbers[i:i+3]) for i in range(0,len(numbers),3)]
    assert all(c in COLOUR or c in (WHITE,BLACK) for c in pixels)
    return w,h,pixels

def trace(path):
    w,h,pixels=read_ppm(path)
    def at(p):
        x,y=p
        return pixels[y*w+x] if 0<=x<w and 0<=y<h else BLACK
    def region(p):
        found, todo={p},[p]; colour=at(p)
        while todo:
            x,y=todo.pop()
            for dx,dy in DIRECTIONS:
                q=(x+dx,y+dy)
                if q not in found and at(q)==colour:
                    found.add(q);todo.append(q)
        return found
    p=(0,0);dp=cc=0;stack=[];out='';steps=[]
    assert at(p) in COLOUR
    for tick in range(100):
        block=region(p); attempts=[]
        for attempt in range(8):
            dx,dy=DIRECTIONS[dp]
            lx,ly=(dy,-dx) if cc==0 else (-dy,dx)
            edge=max(block,key=lambda q:(q[0]*dx+q[1]*dy,q[0]*lx+q[1]*ly))
            q=(edge[0]+dx,edge[1]+dy)
            attempts.append(dict(dp=dp,cc=cc,edge=edge,target=q,colour=at(q)))
            if at(q)==BLACK:
                if attempt%2==0:cc^=1
                else:dp=(dp+1)%4
                continue
            old=at(p);before=stack.copy();white=at(q)==WHITE
            if white:
                while at(q)==WHITE:q=(q[0]+dx,q[1]+dy)
                if at(q)==BLACK:
                    raise ValueError('blocked-white behaviour outside this bounded tracer')
                op='white_slide_no_command'
            else:
                oh,ol=COLOUR[old];nh,nl=COLOUR[at(q)]
                delta=((nh-oh)%6,(nl-ol)%3)
                if delta not in OPS:raise ValueError(f'unsupported command {delta}')
                op=OPS[delta]
                if op=='push':stack.append(len(block))
                elif op=='duplicate' and stack:stack.append(stack[-1])
                elif op=='not' and stack:stack[-1]=int(stack[-1]==0)
                elif op=='out_number' and stack:out+=str(stack.pop())
                elif op in ('add','subtract') and len(stack)>=2:
                    a,b=stack.pop(),stack.pop();stack.append(b+a if op=='add' else b-a)
            steps.append(dict(source=p,destination=q,source_rgb=old,block_area=len(block),
                              dp=dp,cc=cc,operation=op,before=before,after=stack.copy(),output=out,
                              boundary_attempts=attempts))
            p=q;break
        else:
            return dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        width=w,height=h,stdout=out,stdout_hex=out.encode().hex(),
                        command_transitions=sum(s['operation']!='white_slide_no_command' for s in steps),
                        successful_moves=len(steps),steps=steps,
                        halted_after_eight_restrictions=attempts,terminal_rgb=at(p),terminal_area=len(block))
    raise RuntimeError('100-move bound exceeded')

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    for name,expected,pushes in [('octahedron.ppm','21',[6,12,8,2]),
                                ('octahedron_defect.ppm','30',[6,11,8,2]),
                                ('octahedron_wrong_pin.ppm','20',[6,12,8,3])]:
        r=trace(here/name)
        (here/(name+'.nova_trace.json')).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        assert r['stdout']==expected
        assert [s['block_area'] for s in r['steps'] if s['operation']=='push']==pushes
        assert len(r['halted_after_eight_restrictions'])==8
        print(name,r['stdout_hex'],'commands',r['command_transitions'],'moves',r['successful_moves'],
              'terminal',r['terminal_rgb'],r['terminal_area'],'PASS')
