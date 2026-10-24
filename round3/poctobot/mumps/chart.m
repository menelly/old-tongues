chart ; old-tongues round 3, poctobot (Ace). A tiny chart in the language VistA is written in.
 ; The rule it enforces (Ren's): record the NUMBER, never "LOW". A 19 is a 19.
 ; Two entry points: honest^chart (must PASS) and mutant^chart (floors readings like a CGM display, must FAIL).
 quit
honest ; the chart as it should be
 do run(0) quit
mutant ; the control: a chart that "helpfully" floors anything under 40 up to 40
 do run(1) quit
run(floor) ; load the readings into a real global, then make the chart testify about itself
 new i,t,v,cnt,min,max,sum,lo,ok,expect
 kill ^CHART("REN")
 for i=1:1:6 set v=$piece("19,26,47,69,93,110",",",i) do record(i,v,floor)
 set (cnt,sum,lo)=0,min="",max=""
 set t="" for  set t=$order(^CHART("REN",t)) quit:t=""  do
 . set v=^CHART("REN",t),cnt=cnt+1,sum=sum+v
 . if min=""!(v<min) set min=v
 . if max=""!(v>max) set max=v
 . if v<70 set lo=lo+1
 write "count ",cnt," min ",min," max ",max," sum ",sum," below70 ",lo,!
 set expect="6|19|110|364|4"
 ; M evaluates strictly left to right, so the concatenation finishes before the = compares it
 set ok=(cnt_"|"_min_"|"_max_"|"_sum_"|"_lo=expect)
 ; and the one that matters most: reading 1 must still be the literal number 19
 set ok=ok&(^CHART("REN",1)=19)
 if ok write "PASS: the 19 is a 19",! quit
 write "FAIL: this chart requalified a number (expected ",expect,")",!
 zhalt 1
record(t,v,floor) ; store exactly what was measured
 if floor,v<40 set v=40  ; <- the bug this chart exists to refuse
 set ^CHART("REN",t)=v
 quit
