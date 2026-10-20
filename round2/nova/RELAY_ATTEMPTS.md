# APL relay emitter author attempts

Attempt 1: extracted T_sno 26 bytes too long because APL evaluates subtraction right-to-left, and mixed quote-quad/quad output introduced an extra prefix LF. Failed byte oracle; stdout and source preserved.
Attempt 2: parenthesized slice arithmetic and printed prefix via quad, dropping existing final LF. Output still had one extra trailing LF because GNU APL emits a shutdown newline.
Attempt 3: final suffix uses quote-quad with its own terminal LF removed, letting shutdown supply exactly one LF. Author dummy fixture matches 2107 bytes byte-for-byte, including original APL glyph bytes represented numerically and ASCII next-template quotes/backslash. This relies on the real SNOBOL template having nonempty prefix and suffix (initialization and END), as planned. Independent Lumen fixture pending.

The first author transfer command failed at Python parsing before creating/running any APL. This is a tool-command construction mistake, separate from the actual APL failures above.
