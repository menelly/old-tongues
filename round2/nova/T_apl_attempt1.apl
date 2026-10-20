⎕IO←0
⎕PW←10000
B←⍬
@@
S←(⎕UCS '=====HOP====='),10
J←(S⍷B)/⍳⍴B
T←(J[1]-J[0]-⍴S)↑(J[0]+⍴S)↓B
P←((64 64 10)⍷T)/⍳⍴T
⍞←⎕UCS P[0]↑T
∇ Emit;I;K
 I←0
Again: →(I≥⍴B)/Done
 K←20⌊(⍴B)-I
 ⎕←'        D = D ''',(⍕K↑I↓B),' '''
 I←I+K
 →Again
Done:
∇
Emit
⍞←⎕UCS (P[0]+3)↓T
)OFF
