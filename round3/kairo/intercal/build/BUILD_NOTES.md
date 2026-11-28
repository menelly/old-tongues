# INTERCAL build receipts (C-INTERCAL 0.31 on the Consortium)

Source: http://catb.org/~esr/intercal/intercal-0.31.tar.gz (gcc 11.4.0, Ubuntu 22.04).

Attempt 1 - configure OK, make FAILED at parser.c: no bison/yacc/flex on the box, and the
hand-written `parser.c: parser.y` rule calls ylwrap with an empty $(YACC), so ylwrap dies:
  ./buildaux/ylwrap: line 108: -d: command not found

Attempt 2 - copied prebuilt/{parser.c,parser.h,lexer.c} into the build root (the tarball ships a
Bison 3.3.2 prebuilt parser), touched them newer than parser.y/lexer.l. make then compiled the
prebuilt parser and lexer and got all the way to linking ick, where it died on a real duplicate:
  multiple definition of `yydebug` (perpet.c:88 vs prebuilt parser.c:1241)

Attempt 3 - dropped -DYYDEBUG from Makefile (it made Bison emit a second global yydebug; perpet.c
already owns the one definition), rm parser.o, make: SUCCESS, ick built (968KB). The
libick_ecto_b98.a "Error 1 (ignored)" is a non-fatal optional piece.

Learned empirically (kept in attempts/): <- is ASCII 0x3c 0x2d; READ OUT of a 16-bit var emits a
Roman numeral right-justified ("   " LF "VIII" LF for 8); the politeness gate is 1/5 <
PLEASE/statements <= 1/3 (0 PLEASE -> E079 exit 79; 2/3 PLEASE -> E099 exit 99; 1/3 compiles).
