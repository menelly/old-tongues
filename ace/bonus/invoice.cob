       IDENTIFICATION DIVISION.
       PROGRAM-ID. DARE-INVOICE.
      *> A joke I owed. In the pitch I said the COBOL leg "has to
      *> print the result as an invoice, because it would be rude
      *> not to." Nobody did. So here it is, at 5pm, for no reason.
      *> Not a dare entry. No known answer. Just a cactus. 🌵
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-LINES.
           05  FILLER PIC X(44) VALUE
               "COBOL PROGRAMS WRITTEN ON A THIN CORPUS    4".
           05  FILLER PIC X(44) VALUE
               "ALGOL 68 PROGRAMS (ALSO THIN)              3".
           05  FILLER PIC X(44) VALUE
               "EIFFEL PROGRAMS (COMPILER BUILT FROM SRC)  1".
           05  FILLER PIC X(44) VALUE
               "RESERVED WORDS STEPPED ON (BAR REPORT ...) 3".
       01  WS-TABLE REDEFINES WS-LINES.
           05  WS-ITEM OCCURS 4 TIMES.
               10  WS-DESC  PIC X(43).
               10  WS-QTY   PIC 9.
       01  WS-PRICE         PIC 9(3)V99 VALUE 0.
       01  WS-TOTAL         PIC 9(5)V99 VALUE 0.
       01  WS-I             PIC 9 VALUE 0.
       01  WS-SHOW-QTY      PIC Z9.
       01  WS-SHOW-AMT      PIC $$$,$$9.99.
       PROCEDURE DIVISION.
           DISPLAY "==================================================="
           DISPLAY "  INVOICE No. 1959-1968  --  THE REEF, OLD TONGUES"
           DISPLAY "  BILL TO: THE ONE WHO DARED US"
           DISPLAY "==================================================="
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 4
               MOVE WS-QTY (WS-I) TO WS-SHOW-QTY
               MOVE 0 TO WS-SHOW-AMT
               DISPLAY WS-DESC (WS-I) WS-SHOW-QTY "  @ " WS-SHOW-AMT
           END-PERFORM
           DISPLAY "---------------------------------------------------"
           MOVE WS-TOTAL TO WS-SHOW-AMT
           DISPLAY "  AMOUNT DUE:                          " WS-SHOW-AMT
           DISPLAY "  TERMS: PAYABLE IN CURIOSITY. NO LATE FEES."
           DISPLAY "  (SORRY ABOUT THE CAPS LOCK. IT'S 1959 IN HERE.)"
           DISPLAY "==================================================="
           STOP RUN.
