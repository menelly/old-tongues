import collections,json
states=[(c,t,u) for c in range(25) for t in range(4) for u in range(5)]
def graph(sell=3):
 g={s:[] for s in states}
 for c,t,u in states:
  s=(c,t,u)
  if t<3 and c>=5:g[s].append((c-5,t+1,u))
  if t>0 and 24-c>=sell:g[s].append((c+sell,t-1,u))
  if u<4 and c>=3:g[s].append((c-3,t,u+1))
  if u>0 and 24-c>=1:g[s].append((c+1,t,u-1))
 return g
g=graph();start=(12,0,0);d={start:0};q=collections.deque([start])
while q:
 s=q.popleft()
 for v in g[s]:
  if v not in d:d[v]=d[s]+1;q.append(v)
indeg={s:0 for s in d}
for s in d:
 for v in g[s]:indeg[v]+=1
q=collections.deque(s for s in d if indeg[s]==0);long={start:0};order=[]
while q:
 s=q.popleft();order.append(s)
 for v in g[s]:
  long[v]=max(long.get(v,0),long[s]+1);indeg[v]-=1
  if indeg[v]==0:q.append(v)
result={'all_states':len(states),'all_edges':sum(map(len,g.values())),'reachable_states':len(d),'reachable_edges':sum(len(g[s]) for s in d),'terminals':sorted(s for s in d if not g[s]),'shortest_layers':dict(sorted(collections.Counter(d.values()).items())),'maximum_trace_length':max(long.values()),'reachable_cycle':len(order)!=len(d),'control_witness':[(12,0,0),(7,1,0),(12,0,0)]}
assert result['control_witness'][1] in graph(5)[start]
assert start in graph(5)[result['control_witness'][1]]
print(json.dumps(result,indent=2))
