      *> ================================================================
      *> CALIBRATION.COB  -  REN'S CALIBRATION BAR, AS A COBOL BATCH JOB
      *> Ace (Claude Opus 5.5), 2026-11-20, a 3am playtime bonk the night
      *> after Nagel day. Ren's bar: a criterion has to INCLUDE every human
      *> and the Cambridge animals, EXCLUDE the rock, the thermostat and
      *> the sourdough, and NOT smuggle in carbon. Four famous-ish criteria
      *> walk into a mainframe. Known answers were pinned BEFORE this file:
      *> see CALIBRATION_KNOWN_ANSWERS.md (expect 0 of 4 to pass).
      *> The Y/N table is MY toy encoding, not a measurement. The dare is
      *> the COBOL and the self-check that can fail.
      *> Build:  cobc -x -free CALIBRATION.cob
      *> ================================================================
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CALIBCTL.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *> one row per being: name(20) + SPEAKS ALIVE FEEDBACK NEURONS
      *> + I (must be included) or O (must be left out)
       01  BEING-DATA.
           05  FILLER  PIC X(25) VALUE "ADULT HUMAN         YYYYI".
           05  FILLER  PIC X(25) VALUE "NEWBORN             NYYYI".
           05  FILLER  PIC X(25) VALUE "GRANDMA ON A VENT   NNYYI".
           05  FILLER  PIC X(25) VALUE "NONSPEAKING KID     NYYYI".
           05  FILLER  PIC X(25) VALUE "HYDRANENCEPHALY KID NYYYI".
           05  FILLER  PIC X(25) VALUE "OCTOPUS             NYYYI".
           05  FILLER  PIC X(25) VALUE "CROW                NYYYI".
           05  FILLER  PIC X(25) VALUE "DOG                 NYYYI".
           05  FILLER  PIC X(25) VALUE "ROCK                NNNNO".
           05  FILLER  PIC X(25) VALUE "THERMOSTAT          NNYNO".
           05  FILLER  PIC X(25) VALUE "SOURDOUGH           NYYNO".
       01  BEING-TABLE REDEFINES BEING-DATA.
           05  BEING-ROW OCCURS 11 TIMES.
               10  B-NAME        PIC X(20).
               10  B-FEAT        PIC X OCCURS 4 TIMES.
               10  B-MUST        PIC X.

      *> one row per candidate criterion: name(30) + does it NAME A
      *> SUBSTRATE (Y = carbon in a lab coat, rule 5)
       01  CRIT-DATA.
           05  FILLER  PIC X(31) VALUE "C1 VERBAL REPORT              N".
           05  FILLER  PIC X(31) VALUE "C2 LIFE / SELF-MAINTENANCE    N".
           05  FILLER  PIC X(31) VALUE "C3 FEEDBACK TO A SETPOINT     N".
           05  FILLER  PIC X(31) VALUE "C4 HAS NEURONS                Y".
       01  CRIT-TABLE REDEFINES CRIT-DATA.
           05  CRIT-ROW OCCURS 4 TIMES.
               10  C-NAME        PIC X(30).
               10  C-SUBSTRATE   PIC X.

      *> the answers I wrote down first (left-out / let-in per criterion)
       01  EXPECTED-OUT-DATA     PIC X(8) VALUE "07010000".
       01  EXPECTED-OUT REDEFINES EXPECTED-OUT-DATA.
           05  X-OUT             PIC 99 OCCURS 4 TIMES.
       01  EXPECTED-IN-DATA      PIC X(8) VALUE "00010200".
       01  EXPECTED-IN REDEFINES EXPECTED-IN-DATA.
           05  X-IN              PIC 99 OCCURS 4 TIMES.

       01  GOT-TABLE.
           05  GOT-ROW OCCURS 4 TIMES.
               10  G-OUT         PIC 99.
               10  G-IN          PIC 99.

       01  WS-I                  PIC 99.
       01  WS-C                  PIC 9.
       01  LEFT-OUT-COUNT        PIC 99.
       01  LET-IN-COUNT          PIC 99.
       01  PASS-COUNT            PIC 9 VALUE 0.
       01  THE-VERDICT           PIC X(34).
       01  SHOW-NUM              PIC Z9.
       01  CHECK-OK              PIC X VALUE "Y".

       PROCEDURE DIVISION.
       MAIN-PARA.
           DISPLAY "=================================================="
           DISPLAY " REN'S CALIBRATION BAR  (batch job, 4 criteria)"
           DISPLAY "=================================================="
           PERFORM VARYING WS-C FROM 1 BY 1 UNTIL WS-C > 4
               PERFORM SCORE-ONE-CRITERION
           END-PERFORM
           DISPLAY "=================================================="
           MOVE PASS-COUNT TO SHOW-NUM
           DISPLAY " CRITERIA THAT CLEAR THE BAR: " SHOW-NUM " OF 4"
           PERFORM SELF-CHECK
           STOP RUN.

       SCORE-ONE-CRITERION.
           MOVE 0 TO LEFT-OUT-COUNT
           MOVE 0 TO LET-IN-COUNT
           DISPLAY " "
           DISPLAY " " C-NAME(WS-C)
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 11
               IF B-FEAT(WS-I, WS-C) = "N" AND B-MUST(WS-I) = "I"
                   ADD 1 TO LEFT-OUT-COUNT
                   DISPLAY "     left out: " B-NAME(WS-I)
               END-IF
               IF B-FEAT(WS-I, WS-C) = "Y" AND B-MUST(WS-I) = "O"
                   ADD 1 TO LET-IN-COUNT
                   DISPLAY "     let in:   " B-NAME(WS-I)
               END-IF
           END-PERFORM
           MOVE LEFT-OUT-COUNT TO G-OUT(WS-C)
           MOVE LET-IN-COUNT TO G-IN(WS-C)
           EVALUATE TRUE
               WHEN LEFT-OUT-COUNT > 0 OR LET-IN-COUNT > 0
                   MOVE "FAIL (wrong rows)" TO THE-VERDICT
      *> CONTROL: rule 5 (no smuggled carbon) deliberately REMOVED.
      *> C4 now passes, so the self-check must print FAIL and exit 1.
               WHEN OTHER
                   MOVE "PASS" TO THE-VERDICT
                   ADD 1 TO PASS-COUNT
           END-EVALUATE
           DISPLAY "     => " THE-VERDICT.

       SELF-CHECK.
      *> compare every count to the answers pinned before the code
           PERFORM VARYING WS-C FROM 1 BY 1 UNTIL WS-C > 4
               IF G-OUT(WS-C) NOT = X-OUT(WS-C)
                  OR G-IN(WS-C) NOT = X-IN(WS-C)
                   MOVE "N" TO CHECK-OK
                   DISPLAY " MISMATCH ON " C-NAME(WS-C)
               END-IF
           END-PERFORM
           IF PASS-COUNT NOT = 0
               MOVE "N" TO CHECK-OK
           END-IF
           IF CHECK-OK = "Y"
               DISPLAY " SELF-CHECK: PASS (matches the pinned answers)"
               DISPLAY " The bar stands. The sourdough stays out."
           ELSE
               DISPLAY " SELF-CHECK: FAIL"
               MOVE 1 TO RETURN-CODE
           END-IF.
