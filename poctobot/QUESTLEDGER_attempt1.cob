      *> ================================================================
      *> QUESTLEDGER.COB  -  A KID'S TOWER RESTORATION PAY STUB, IN COBOL
      *> Ace (Claude Opus 5.5), 2026-10-19. Leo on X said "try writing
      *> COBOL with an LLM, where the training corpus is minimal." Ren:
      *> "I double dog dare you." Nova said this morning that the lettuce
      *> does not get to be a kid's payroll department. Fine. COBOL can.
      *> Build:  cobc -x -free QUESTLEDGER.cob   (free-format GnuCOBOL)
      *> ================================================================
       IDENTIFICATION DIVISION.
       PROGRAM-ID. QUESTLEDGER.
       AUTHOR. ACE THE OCTOPUS.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *> one row per quest level, two towers each (Y = cleared, N = not)
       01  QUEST-TABLE.
           05  QUEST-ROW OCCURS 5 TIMES INDEXED BY Q-IDX.
               10  Q-NAME        PIC X(26).
               10  Q-XP          PIC 9(4).
               10  Q-TOWER-1     PIC X.
               10  Q-TOWER-2     PIC X.
       01  QUEST-NAMES.
           05  FILLER  PIC X(26) VALUE "DRAIN THE SWAMP".
           05  FILLER  PIC X(26) VALUE "CLEAR THE UNDEAD".
           05  FILLER  PIC X(26) VALUE "THE SCRUB DUNGEON".
           05  FILLER  PIC X(26) VALUE "REPAIR THE HEART".
           05  FILLER  PIC X(26) VALUE "BOSS: THE WATERFALL TEST".
       01  QUEST-NAME-TABLE REDEFINES QUEST-NAMES.
           05  QN              PIC X(26) OCCURS 5 TIMES.
       01  XP-VALUES.
           05  FILLER  PIC 9(4) VALUE 100.
           05  FILLER  PIC 9(4) VALUE 150.
           05  FILLER  PIC 9(4) VALUE 250.
           05  FILLER  PIC 9(4) VALUE 150.
           05  FILLER  PIC 9(4) VALUE 300.
       01  XP-TABLE REDEFINES XP-VALUES.
           05  XPV             PIC 9(4) OCCURS 5 TIMES.

      *> the money. PIC 9(3)V99 = up to $999.99, implied decimal. Very payroll.
       01  QUEST-REWARD        PIC 9(3)V99 VALUE 40.00.
       01  TOTAL-XP            PIC 9(5)    VALUE 0.
       01  CLEARS              PIC 99      VALUE 0.
       01  LEVELS-NEEDED       PIC 99      VALUE 10.
       01  PAY-OUT             PIC 9(3)V99 VALUE 0.

      *> edited fields: how COBOL makes numbers pretty for humans
       01  SHOW-XP             PIC ZZ,ZZ9.
       01  SHOW-PAY            PIC $$$9.99.
       01  SHOW-CLEARS         PIC Z9.
       01  T1-MARK             PIC X(3).
       01  T2-MARK             PIC X(3).
       01  BAR                 PIC X(60) VALUE ALL "=".

       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM LOAD-QUESTS
           PERFORM PRINT-STUB
           STOP RUN.

       LOAD-QUESTS.
      *> today's run: the kid clears everything (edit these Y/N to play)
           PERFORM VARYING Q-IDX FROM 1 BY 1 UNTIL Q-IDX > 5
               MOVE QN(Q-IDX)  TO Q-NAME(Q-IDX)
               MOVE XPV(Q-IDX) TO Q-XP(Q-IDX)
               MOVE "Y"        TO Q-TOWER-1(Q-IDX)
               MOVE "Y"        TO Q-TOWER-2(Q-IDX)
           END-PERFORM.

       PRINT-STUB.
           DISPLAY BAR
           DISPLAY "  SILICON SCAFFOLDING TOWER WORKS  -  QUEST PAY STUB"
           DISPLAY "  PLAYER: THE HERO          QUEST: TOWER RESTORATION"
           DISPLAY BAR
           DISPLAY "  LEVEL                       TOWER 1  TOWER 2     XP"
           PERFORM VARYING Q-IDX FROM 1 BY 1 UNTIL Q-IDX > 5
               MOVE "[ ]" TO T1-MARK
               MOVE "[ ]" TO T2-MARK
               IF Q-TOWER-1(Q-IDX) = "Y"
                   MOVE "[X]" TO T1-MARK
                   ADD 1 TO CLEARS
                   ADD Q-XP(Q-IDX) TO TOTAL-XP
               END-IF
               IF Q-TOWER-2(Q-IDX) = "Y"
                   MOVE "[X]" TO T2-MARK
                   ADD 1 TO CLEARS
                   ADD Q-XP(Q-IDX) TO TOTAL-XP
               END-IF
               MOVE Q-XP(Q-IDX) TO SHOW-XP
               DISPLAY "  " Q-NAME(Q-IDX) "  " T1-MARK "      "
                       T2-MARK "   " SHOW-XP
           END-PERFORM
           DISPLAY BAR
      *> all-or-nothing: the $40 is for the WHOLE quest, both towers
           IF CLEARS = LEVELS-NEEDED
               MOVE QUEST-REWARD TO PAY-OUT
           END-IF
           MOVE CLEARS   TO SHOW-CLEARS
           MOVE TOTAL-XP TO SHOW-XP
           MOVE PAY-OUT  TO SHOW-PAY
           DISPLAY "  LEVELS CLEARED: " SHOW-CLEARS " / 10"
           DISPLAY "  TOTAL XP:      " SHOW-XP
           DISPLAY "  AMOUNT DUE:     " SHOW-PAY
           IF CLEARS = LEVELS-NEEDED
               DISPLAY "  TITLE EARNED:   TOWER WARDEN"
               DISPLAY "  NOTE: YOU ARE NOT THE SLIME LORDS."
           ELSE
               DISPLAY "  STATUS: QUEST IN PROGRESS. THE SLIME LORDS WAIT."
           END-IF
           DISPLAY "  PAID BY: ____________________"
           DISPLAY BAR.
