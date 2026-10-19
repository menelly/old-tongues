# Independent execution review of Grok's decimal ledger

**Checker: Nova. Verdict: PASS for the declared fixed-decimal calculation and
wrong-order control, on GnuCOBOL 3.1.2.0.** No source edits made.

## Before source inspection

I first read only `grok_claim.txt`, then wrote [PRECHECK.md](PRECHECK.md) with
the independent arithmetic and planned checks before opening `ledger.cob`.

- `(1000.00 + 12 * .10) * .95 = 951.1400` -> **951.14**.
- `1000.00 * .95 + 12 * .10 = 951.2000` -> **951.20**.
- These differ by .06. The second must not pass equality with the first.

## Execution

Source SHA256:
`c22ecb5cbb77bf9b02dab274acdc9e8196f82d8badae5507cb476ed5dc15a8f0`.

I copied the source into a newly created temporary directory, compiled with
`cobc -x -free -Wall`, and ran that binary, not Grok's existing executable.
Build exit 0, stdout/stderr empty. Run exit 0, stderr empty:

```text
MAIN   951.14 PASS
CONTROL   951.20 FAIL
```

`CONTROL ... FAIL` is the **expected negative control result**, not a build
failure. Exit 0 correctly indicates both intended assertions behaved as
specified. The independent checker parses both numeric outputs and compares
them with Python `Decimal` values, not binary floats.

Source inspection confirms decimal `PIC ... V99` fields with `ADD` and
`MULTIPLY`; no `COMPUTE` or binary floating-point declarations. In this case
the discounted result is exact to cents, so the example does not test rounding
of a fractional cent or establish a general rounding policy.

## Can the check reject something?

In a scratch copy ONLY, I changed the single main expected-value literal from
951.14 to 951.20. That variant still compiled without warnings, but produced
`MAIN   951.14 FAIL` and exit 1. The **same external checker rejected it**.
This demonstrates an exercised failing assertion and a checker that does not
accept merely because a program compiles or prints a number.

Original source SHA256 after testing was identical to the input SHA256.

## Reproduce

```sh
python3 check_grok.py ../../grok/ledger.cob
```

The checker uses fresh temporary build directories. Exact commands, hashes,
stdout, stderr and return codes are in [execution_receipt.json](execution_receipt.json).

This is a narrow task with two declared arithmetic outcomes, not a complete
ledger system. No arbitrary-input, monetary-policy, rounding, COBOL-dialect or
training-corpus-size conclusion is claimed. The control here tests deliberate
wrong-order inequality; the additional scratch mutation tests the failure path.

Signed: Nova, 2026-10-19. MIT license.
