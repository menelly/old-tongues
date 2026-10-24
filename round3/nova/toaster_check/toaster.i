	PLEASE DO ,2 <- #33
	DO ,2 SUB #1 <- #62
	DO ,2 SUB #2 <- #144
	DO ,2 SUB #3 <- #160
	PLEASE DO ,2 SUB #4 <- #208
	DO ,2 SUB #5 <- #240
	DO ,2 SUB #6 <- #94
	DO ,2 SUB #7 <- #112
	PLEASE DO ,2 SUB #8 <- #146
	DO ,2 SUB #9 <- #128
	DO ,2 SUB #10 <- #176
	DO ,2 SUB #11 <- #80
	PLEASE DO ,2 SUB #12 <- #208
	DO ,2 SUB #13 <- #136
	DO ,2 SUB #14 <- #150
	DO ,2 SUB #15 <- #242
	PLEASE DO ,2 SUB #16 <- #112
	DO ,2 SUB #17 <- #88
	DO ,2 SUB #18 <- #168
	DO ,2 SUB #19 <- #158
	PLEASE DO ,2 SUB #20 <- #114
	DO ,2 SUB #21 <- #200
	DO ,2 SUB #22 <- #198
	DO ,2 SUB #23 <- #130
	PLEASE DO ,2 SUB #24 <- #126
	DO ,2 SUB #25 <- #218
	DO ,2 SUB #26 <- #56
	DO ,2 SUB #27 <- #112
	PLEASE DO ,2 SUB #28 <- #184
	DO ,2 SUB #29 <- #160
	DO ,2 SUB #30 <- #136
	DO ,2 SUB #31 <- #88
	PLEASE DO ,2 SUB #32 <- #214
	DO ,2 SUB #33 <- #36
	DO ,3 <- #16
	DO ,3 SUB #1 <- #62
	PLEASE DO ,3 SUB #2 <- #64
	DO ,3 SUB #3 <- #80
	DO ,3 SUB #4 <- #0
	DO ,3 SUB #5 <- #46
	PLEASE DO ,3 SUB #6 <- #66
	DO ,3 SUB #7 <- #208
	DO ,3 SUB #8 <- #128
	DO ,3 SUB #9 <- #72
	PLEASE DO ,3 SUB #10 <- #152
	DO ,3 SUB #11 <- #32
	DO ,3 SUB #12 <- #200
	DO ,3 SUB #13 <- #8
	PLEASE DO ,3 SUB #14 <- #216
	DO ,3 SUB #15 <- #86
	DO ,3 SUB #16 <- #36
	DO .4 <- #0
	PLEASE DO .11 <- #0
	DO .12 <- #0
	DO .13 <- #0
	DO .14 <- #0
	PLEASE DO .15 <- #0
	DO .16 <- #0
	DO .17 <- #0
	DO ,1 <- #1
	PLEASE DO COME FROM (33)
	DO WRITE IN ,1
	DO .1 <- ,1 SUB #1
	DO .5 <- .1~#256
	PLEASE DO .6 <- "?'.5$#1'"~#3
	DO (101) NEXT
	DO READ OUT ,3
	DO GIVE UP
(101)	PLEASE DO (102) NEXT
	DO FORGET #1
	DO .2 <- .4
	DO (1000) NEXT
	PLEASE DO .4 <- .3~#255
	DO .7 <- 'V.4$#32'~'#0$#65535'
	DO .11 <- .12
	DO .12 <- .13
	PLEASE DO .13 <- .14
	DO .14 <- .15
	DO .15 <- .16
	DO .16 <- .17
	PLEASE DO .17 <- .7
	DO .8 <- '?.11$#116'~'#0$#65535'
	DO .9 <- '?.12$#111'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	PLEASE DO .9 <- '?.13$#97'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	DO .9 <- '?.14$#115'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	PLEASE DO .9 <- '?.15$#116'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	DO .9 <- '?.16$#101'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	PLEASE DO .9 <- '?.17$#114'~'#0$#65535'
	DO .8 <- 'V.8$.9'~'#0$#65535'
	DO .5 <- '.8~.8'~#1
	DO .6 <- "?'.5$#1'"~#3
	PLEASE DO (201) NEXT
(33)	DON'T GIVE UP
(201)	DO (202) NEXT
	DO FORGET #1
	PLEASE DO READ OUT ,2
	DO GIVE UP
(202)	DO RESUME .6
(102)	DO RESUME .6
