# Nova's independent precheck of Grok's fixed-decimal ledger

2026-10-19. Written after reading only `grok_claim.txt`, before reading
`ledger.cob` or any Grok compiler/output receipts. Grok declared DONE via Ace.

Contract: COBOL / GnuCOBOL 3.1.2, no `COMPUTE`, no binary floats; start at
1000.00, add twelve 0.10 amounts, then multiply by .95.

Independent arithmetic: 1000.00 + 12*(.10) = 1001.20;
1001.20 * .95 = **951.1400**, exact cents **951.14**.
Different operation order: 1000.00 * .95 + 12*(.10) = **951.20**.
The different result must not pass equality with 951.14. The gap is .06.

Planned review: hash/copy source; compile from a new temporary directory,
without using Grok's binary; capture compiler exit/warnings and execution;
inspect exact arithmetic operations and numeric types; compare outputs with
Python Decimal arithmetic written independently; run a same-checker negative
control (deliberately wrong expected answer/source mutation in scratch only).
Do not edit Grok's source. No broad claim about all fixed-point arithmetic or
unknown training data. Record source/receipt hashes and actual control behavior.
