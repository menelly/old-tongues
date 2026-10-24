# Checker attempts

Attempt 1: both-byte comparison and final-state check reached successfully for
the positive program, but my direction assertion failed. I incorrectly demanded
that all four direction *glyphs* execute. Conditional `|` also changes direction;
an upward walk need not execute `^`. Source program was not changed.

Failure: AssertionError at `assert directions==sorted('><^v')`.
Attempt 2 instead measures direction from adjacent instruction-pointer positions.

Attempt 2: the inherited no-empty-stack assertion failed. The positive trace
reached `:` at (68,4), tick 830, with an empty stack after printing PASS. This
is the verdict-string sentinel, not a Fibonacci calculation error. Grok's
no-empty-pop report had become an assertion in my checker; my trace did not
support it. Attempt 3 records and checks the empty duplicate in each program
instead of presupposing its absence. Program and walker remained unchanged.
