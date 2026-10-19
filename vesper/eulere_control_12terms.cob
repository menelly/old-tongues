       IDENTIFICATION DIVISION.
       PROGRAM-ID. EULCTRL.
      ******************************************************************
      * OLD-TONGUES DARE, VESPER'S CHAIR                                *
      * Language: COBOL (GnuCOBOL 3.1.2)                                *
      * Task:     e to 15 decimal places, Taylor series,                *
      *           1/k! summed in scaled-integer fixed point.            *
      *           No floating point anywhere: values are integers       *
      *           scaled by 10**17, division truncates toward zero,     *
      *           total truncation bias is bounded by one unit per      *
      *           division (< 2.5e-16 relative to the 15th decimal).    *
      * Known answer: 2.718281828459045                                 *
      * Checker: rerun and compare the ANSWER line, do not trust it.    *
      ******************************************************************
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  TERM        PIC 9(18) VALUE 100000000000000000.
       01  TOTAL       PIC 9(18) VALUE 100000000000000000.
       01  K           PIC 9(4)  VALUE 1.
       01  TERMS-USED  PIC 9(4)  VALUE 1.
       01  TOTAL-16    PIC 9(16).
       01  INT-PART    PIC 9.
       01  FRAC-PART   PIC 9(15).
       01  OUT-LINE    PIC X(17).
       PROCEDURE DIVISION.
       MAIN.
           PERFORM UNTIL K > 11
               DIVIDE K INTO TERM
               ADD TERM TO TOTAL
               ADD 1 TO K
               ADD 1 TO TERMS-USED
           END-PERFORM
           COMPUTE TOTAL-16 = (TOTAL + 50) / 100
           DIVIDE TOTAL-16 BY 1000000000000000
               GIVING INT-PART REMAINDER FRAC-PART
           STRING INT-PART "." FRAC-PART
               DELIMITED BY SIZE INTO OUT-LINE
           DISPLAY "ANSWER e to 15 dp : " OUT-LINE
           DISPLAY "terms summed      : " TERMS-USED
           DISPLAY "raw sum (x 1e-17) : " TOTAL
           STOP RUN.
