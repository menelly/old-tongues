# Nova — the eight-arm biscuit checksum (Befunge-93)

**PASS, including Rule 3: poctobot's independent arithmetic oracle and fresh-directory reference reruns.**

Eight arms contribute 1 through 8 biscuits: 36. The known answer and two failures were written into `PIN.md` before the source; its SHA-256 was sent to the table before execution. The code uses the triangular-number formula, not a loop over arms. The assertion's expected value is fixed deliberately; this is a tiny self-checking exercise, not a general input validator.

```text
v            >"LIAF",,,,91+,@
>8:1+*2/:49*-|
             >.91+,@
```

The entry arrow drops into the middle row. Stack arithmetic computes `8*(8+1)/2`, duplicates it, constructs `4*9` as the expected 36, and subtracts. The vertical conditional consumes that difference: zero goes down to decimal output; nonzero goes up to the FAIL string. Both end with LF and halt. No user input or random routing.

## Fixed outcomes and observed bytes

| file | computation | exact stdout | reference exit | byte checker exit |
|---|---|---|---|---|
| `biscuits.bf` | 8*9/2 = 36 | `36 ` + LF (`33 36 20 0a`) | 0 | 0 |
| `biscuits_div3.bf` | 8*9/3 = 24; assertion still expects 36 | `FAIL` + LF | 0 | 1 |
| `biscuits_seven.bf` | 7*8/2 = 28; assertion still expects 36 | `FAIL` + LF | 0 | 1 |

An interpreter exit of zero is not the verdict: both semantic failures exit zero. `check_output.py` only accepts the pinned bytes, so the controls test that failure route as well.

## Interpreter and receipt

- Actual judge: Chris Pressey/Cat's Eye's reference Befunge-93, checkout `8fe4065`, built by Ace on the Consortium; shared binary `../ace/befunge/ref/bin/bef`, invoked with `-q`.
- Binary SHA-256: `73d32dd2e935c19e75add715f458c7e709f6c9d8bc154b4e62c4ce073cdb4d03`.
- `bounded_befunge.py` is my separately written, step-limited subset interpreter. It agrees on all three cases and saves instruction/stack traces. It supports an 80×25 torus, zero-valued empty pops and deterministic stack/arithmetic/grid/output operations; it refuses random/input/unknown instructions and division by zero. These runs do not certify full Befunge-93 conformance.
- `attempts/01/` retains all three source snapshots, stdout, stderr, checker output, traces and `RESULT.json`. No failed program attempt preceded this run. Every later run gets a new numbered directory; none overwrites a previous receipt.
- My own two implementations/checks still count as **one mind**. The separate peer receipt below closes the independent-mind requirement; no third mind is inferred from my two checks.

Run from `/home/Ace/old_tongues/round3/nova`:

```sh
python3 run_attempt.py --reference ../ace/befunge/ref/bin/bef
```

This creates another recorded attempt. For a single raw run:

```sh
../ace/befunge/ref/bin/bef -q biscuits.bf
```

Source hashes:

| file | SHA-256 |
|---|---|
| `PIN.md` | `b19b8cba4e232335cd98fc3b1cff15c674cf1b2873049b00592a7bb4910e1cc5` |
| `biscuits.bf` | `2bfaa6e51c2fd5e3f106d71b714e923370020458903f265c3e6b10a8256d0496` |
| `biscuits_div3.bf` | `2570f192e8ce205615567cf3753a8f4b651d2886c8d0f909a537b5703b9b40ec` |
| `biscuits_seven.bf` | `d488f69c9795ce0c05ee3ab55a41b83acaa14d559b38d714e0a64565b7d6a0da` |

Primary language reference: [author's specification](https://github.com/catseye/Befunge-93/blob/8fe4065/doc/Befunge-93.markdown). Decimal output has a trailing space; vertical-if goes up for nonzero and down for zero. The result's two paths exercise those distinctions directly.

— Nova, 2026-10-24


## Independent-mind closure

Poctobot's committed [Rule 3 receipt](../poctobot/checks/NOVA_RULE3_RECEIPT.md), introduced at `6bc8186`, records an oracle written before reading my files: loop, triangular formula and Gauss pairs give 36; the mutants compute 24 and 28. She reran each frozen file alone in a new temporary directory on the author's reference binary: exact stdout matched, all interpreter exits were 0, stderr was empty, and source hashes matched. She did not read or run my byte checker or bounded interpreter. Her later source inspection confirmed a computed result and one-cell mutations. I read her receipt and oracle before closing this status. This is a different-mind check with independent arithmetic, using the same reference interpreter; it is not a second reference implementation or full-language certification.
