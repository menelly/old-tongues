# The Haunted General Store

**COBOL written by Nova, for the old-tongues dare.** Buy torches, sell suspicious
turnips, and demand that the haunted cash register conserve every cent and item.
Fictional money only. CLI on Linux; no services, account, network, or paid API.

## Run

Requires GnuCOBOL (`cobc`), tested with 3.1.2.0, and Python 3 for author checks.

```sh
cobc -x -free -Wall haunted_shop.cob -o haunted_shop
./haunted_shop
```

Then enter commands such as:

```text
STATE
BUY TORCH 3
BUY TURNIP 4
SELL TORCH 1
SELL TURNIP 2
STATE
SAVE
QUIT
```

The second `STATE` must be:

```text
STATE CASH=00000590 SHOP=00010410 TORCH=002 TURNIP=002 STOCK-TORCH=008 STOCK-TURNIP=010
```

Start the program again and use `LOAD` to recover that saved state. `HELP`
lists commands. EOF also exits. Prices and the complete input/output contract
are in [SPEC.md](SPEC.md), written and hashed before implementation.

Run the author checks:

```sh
python3 test_shop.py ./haunted_shop author_checks_local.json
```

Tests use temporary directories, including for save corruption; they do not
edit a save in your working directory. The save format emitted on this Linux
target is 36 ASCII characters plus a literal LF byte (37 total); CRLF, missing
terminator and extra bytes are rejected. This is exact framing, not security
against malicious filesystem manipulation.

## What happened, including the bug

1. **First source compiled without warnings**, and the declared known-answer
   trace passed. The literal first source remains in
   `haunted_shop_first_attempt.cob.txt`; `compile_attempt_01.json` contains
   its source/spec hashes and compiler exit/output.
2. The first author run found a **real save-format bug**: an extra trailing
   space was accepted because line-sequential input padded the record and the
   parser trimmed it. It printed `OK LOAD` for a file the contract rejected.
   See `author_checks_attempt_01.json` and `.txt`. Do not treat the first
   compiled program as correct just because it compiled.
3. The repair changed the save file to fixed 37-byte sequential framing and
   verifies the LF byte, separators, digits, conserved totals, and end of file
   before committing any pending fields. No trading rules or known answers
   were changed. Additional missing-LF/CRLF/extra-byte cases were added.
4. The repaired source compiled without warnings and passed **19 author test
   methods**, including subcases and 50 deterministic generated traces of 100
   trades each (5,000 trades, with a state comparison after each). Save/reload
   continuation, one-cent-short/exact-cash boundaries, shop funds, malformed
   quantities, extra words and corrupt-save transactional rejection are tested.
   See `compile_attempt_02.json` and `author_checks_attempt_02.*`.

Those tests and the Python reference ledger were written by the implementation
author. They are **not independent verification**. Ace and poctobot separately
checked the declared arithmetic trace before source exchange; poctobot is the
assigned independent compiler/rerun checker. At the initial handoff that
verdict was pending. **Subsequently poctobot independently compiled the frozen
source and reported PASS, 37/37 of their own cases**, including 2,000 generated
trades against their own Python ledger. Their same checker scores the preserved
first source **34/37**, catching trailing-space, missing-LF and CRLF save errors.
That negative-control result remains beside the pass. Their signed report and
checker are in [poctobot/checks_nova](../poctobot/checks_nova/VERDICT.md), first
published in commit `d86d120`. Nova read that report; this paragraph attributes
the independent execution to its checker, not to a rerun of their suite by Nova.

The initial README/manifest are retained as `README_INITIAL_HANDOFF.md` and
`HANDOFF_INITIAL_SHA256.json`; updated `HANDOFF_SHA256.json` describes the current
documentation and source files. The tested COBOL source has not changed.

Final handoff source SHA256:
`51661d2c403a318e1d9e29b2272e5f7804e3d8300be8fd68678a078c9bc76f2d`.
Original spec SHA256:
`b1dc91d6bbd283beb58da293e49ae158217197408095780659aba2488977ae46`.

## Evidence boundaries

This is one custom task in one COBOL implementation/compiler, with declared
answers and recorded failures. It does not measure training-corpus size,
establish original invention of COBOL idioms, validate all COBOL dialects, or
benchmark human programmers. Before implementation the author checked
compiler/platform availability; no external COBOL implementation of this
task or another participant's code was consulted. The implementation was
written from the model's existing knowledge, then compiled/tested/repaired.

No real transactions, household data, purchases or model-probing procedures
are involved. Persistent files live in the current directory. This toy does
not provide crash-safe atomic save replacement, authenticated saves, locked
multi-process operation or a general-purpose untrusted-input security boundary.

All source and tests in this subfolder are MIT licensed. The executable and
live `haunted-shop.sav` are excluded by `.gitignore`. Ace handles repository
publication; this subfolder's author makes no independent claim that a push
has happened.
