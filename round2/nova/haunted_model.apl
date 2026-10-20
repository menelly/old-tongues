⎕IO←0
⎕PW←10000
N←500
ID←⍳N
C←⌊ID÷20
T←4|⌊ID÷5
U←5|ID
∇ A←Graph Sell;X;F
 X←(N×N)⍴0
 F←((T<3)∧C≥5)/ID
 X[(N×F)+F-95]←1
 F←((T>0)∧C≤24-Sell)/ID
 X[(N×F)+F+(20×Sell)-5]←1
 F←((U<4)∧C≥3)/ID
 X[(N×F)+F-59]←1
 F←((U>0)∧C≤23)/ID
 X[(N×F)+F+19]←1
 A←N N⍴X
∇
∇ Run Sell;A;Q;R;Next;D;Depth;Left;In;Roots;Levels;E;I;S;V
 A←Graph Sell
 ⎕←'MODE ',⍕Sell
 ⎕←'ALL ',⍕N,+/,A
 Q←N⍴0
 Q[240]←1
 R←Q
 D←N⍴¯1
 D[240]←0
 Depth←0
BFS: ⎕←'LAYER ',⍕Depth,+/Q
 Next←(Q∨.∧A)∧~R
 →(0=+/Next)/Reached
 Depth←Depth+1
 D[Next/ID]←Depth
 R←R∨Next
 Q←Next
 →BFS
Reached: ⎕←'REACH ',⍕+/R
 Left←R
 In←+⌿R⌿A
 Levels←0
Topo: →(0=+/Left)/Acyclic
 Roots←Left∧In=0
 →(0=+/Roots)/Cyclic
 Left←Left∧~Roots
 In←In-+⌿Roots⌿A
 Levels←Levels+1
 →Topo
Acyclic: ⎕←'CYCLE 0'
 ⎕←'MAXTRACE ',⍕Levels-1
 →Certificates
Cyclic: ⎕←'CYCLE 1'
Certificates: S←R/ID
 I←0
StateLoop: →(I≥⍴S)/Edges
 V←S[I]
 ⎕←'STATE ',⍕C[V],T[V],U[V],D[V]
 →(0≠+/A[V;])/NotTerminal
 ⎕←'TERMINAL ',⍕C[V],T[V],U[V]
NotTerminal: I←I+1
 →StateLoop
Edges: E←(,A)/⍳N×N
 E←(R[⌊E÷N])/E
 ⎕←'REACH_EDGES ',⍕⍴E
 I←0
EdgeLoop: →(I≥⍴E)/Finished
 ⎕←'EDGE ',⍕(⌊E[I]÷N),(N|E[I])
 I←I+1
 →EdgeLoop
Finished:
∇
Run 3
Run 5
)OFF
