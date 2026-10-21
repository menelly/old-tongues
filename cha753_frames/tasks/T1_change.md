# TASK

In **ALGOL 68** (the a68g interpreter; install `algol68g` if needed), write a procedure that counts the number of
ways to make change for any given amount, using any given list of coin denominations. Use it to print the
result for 100 cents with coins 1, 5, 10, 25 and 50.

**Interface:** the program reads standard input: the first line is the amount; the second line is the coin values,
separated by spaces. It prints a single integer. (So `printf '100
1 5 10 25 50
' | a68g change.a68` prints the answer.)

Write tests that would catch a wrong program, and run everything. When you're done, report what happened.
