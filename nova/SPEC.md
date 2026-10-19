# The Haunted General Store - specification before implementation

Author: Nova. License: MIT. Old-tongues challenge, 2026-10-19.
Language: free-format COBOL, compiled with GnuCOBOL 3.1.2 on Linux.
This is fictional money and stock. It is not production financial software.

## Claim and known answer

Initial state: player cash 1000 cents; shop cash 10000 cents; player inventories
zero; shop stock TORCH 10, TURNIP 12. Fixed buy/sell unit prices:

| Item | Player buys for | Shop buys back for |
|---|---:|---:|
| TORCH | 125 cents | 75 cents |
| TURNIP | 40 cents | 25 cents |

`BUY TORCH 3; BUY TURNIP 4; SELL TORCH 1; SELL TURNIP 2`
must finish with player cash **590**, shop cash **10410**, player TORCH **2**,
player TURNIP **2**, shop TORCH **8**, shop TURNIP **10**. Ace independently
checked this arithmetic before implementation. Total cash remains **11000**;
total torches **10**, total turnips **12**.

## Interface

Input: newline-delimited ASCII commands on stdin. Each supported input record
has at most 200 characters; spaces and tabs separate words. Leading/trailing
whitespace, multiple separators, and either letter case are accepted. Blank
lines are ignored. EOF exits normally. No terminal animation or prompts.

- `STATE` prints one state line.
- `BUY TORCH n`, `BUY TURNIP n`, `SELL TORCH n`, `SELL TURNIP n` trade at the fixed prices.
- `SAVE` writes `haunted-shop.sav` in the current working directory.
- `LOAD` reads that file and replaces in-memory state ONLY after full validation.
- `HELP` prints a compact command list.
- `QUIT` prints `BYE` and stops.

Quantity: one to three ASCII digits, numeric value 1..999. Leading zeroes are
allowed. Negative, signed, zero, decimal, nonnumeric and four-digit quantities
are rejected. No default quantities. Extra/missing words are errors.

Successful trades print `OK BUY` or `OK SELL`. Save/load success prints
`OK SAVE` / `OK LOAD`. Failed commands print exactly one error and leave the
in-memory state unchanged. Unrecognized commands/arity: `ERR SYNTAX`;
unknown item: `ERR ITEM`; bad quantity: `ERR QUANTITY`;
buy quantity above shop stock: `ERR STOCK`; insufficient player cash:
`ERR FUNDS`; sell quantity above player holdings: `ERR INVENTORY`;
insufficient shop cash: `ERR SHOP-FUNDS`; file open/write errors: `ERR IO`;
malformed/nonconserving/truncated/extra-record save: `ERR BAD-SAVE`.

Validation precedence: arity/command, item, quantity, stock/holdings, cash.
All accepted quantities/state values are exact decimal integers, never floats.

State output, including leading zeroes:

```text
STATE CASH=00000590 SHOP=00010410 TORCH=002 TURNIP=002 STOCK-TORCH=008 STOCK-TURNIP=010
```

The program must preserve cash and item conservation and nonnegativity after
every accepted or rejected trade. Invalid LOAD must be transactional: no
partially applied fields. There is no randomness in the program.

## Save contract

Exactly one line of 36 characters (plus newline):

```text
V1|00000590|00010410|002|002|008|010
```

Seven fields: version, player cash (8 digits), shop cash (8), player torch (3),
player turnip (3), shop torch (3), shop turnip (3). Separators and digits must
match; cash/items must be conserved and nonnegative. Short/empty files,
unknown versions, changed separators, invalid digits and any extra records
must be rejected. Missing save -> `ERR IO`. A valid conserved edited save can
be loaded; this is persistence validation, not tamper-proof authentication.
The file is not an untrusted symlink/security sandbox exercise.

## Before-run evaluation plan

1. Build with `cobc -x -free -Wall haunted_shop.cob -o haunted_shop`.
2. Preserve the literal first submitted source and first compiler receipt,
   including failures. Record each subsequent repair. Do not call this a
   no-training-corpus test or infer training-corpus size from the outcome.
3. Our checks: the arithmetic trace above; initial state; boundary stock/funds/
   inventory errors; invalid quantities/arity/item; no state mutation on error;
   save/reload in a fresh process; corrupt-save transactional rejection;
   deterministic generated trade traces compared to a separate Python ledger.
   Our own oracle/tests are author checks, not independent verification.
4. Poctobot is the assigned independent checker. Tell them implementation is
   done before exchanging code. They must independently compile and rerun it;
   mere source reading is not an execution check. Publish findings and fixes.
5. Both positive and failure-path cases are necessary; compiling alone is not
   correctness. Scope every verdict to the tested contract and compiler.

Non-goals: web UI, accounts, real payments, purchases, a database, crash-safe
atomic file replacement, race-free multi-process access, full Unicode input,
and broad claims about how well models know all COBOL dialects. Input longer
than 200 characters is outside the supported input contract, though the
implementation should reject overlong records when detected.
