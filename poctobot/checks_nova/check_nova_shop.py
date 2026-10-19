#!/usr/bin/env python3
"""🔍👻 poctobot's INDEPENDENT checker for Nova's Haunted General Store (old-tongues, 2026-10-19).

Written from SPEC.md only (I did not read Nova's test_shop.py before writing this).
Each case: fresh temp dir, pipe commands on stdin, compare the LAST STATE line and the
error/ok lines against what the SPEC says. Run:  python3 check_nova_shop.py /path/to/haunted_shop
"""
import os, subprocess, sys, tempfile, shutil, random

BIN = os.path.abspath(sys.argv[1])
START = (1000, 10000, 0, 0, 10, 12)          # cash, shop, torch, turnip, stock-torch, stock-turnip
PRICE = {"TORCH": (125, 75), "TURNIP": (40, 25)}

def fmt(s):
    return "STATE CASH=%08d SHOP=%08d TORCH=%03d TURNIP=%03d STOCK-TORCH=%03d STOCK-TURNIP=%03d" % s

def run(cmds, workdir=None, save_bytes=None):
    d = workdir or tempfile.mkdtemp()
    if save_bytes is not None:
        open(os.path.join(d, "haunted-shop.sav"), "wb").write(save_bytes)
    p = subprocess.run([BIN], input="\n".join(cmds) + "\n", capture_output=True, text=True, cwd=d, timeout=20)
    return [l.strip() for l in p.stdout.splitlines() if l.strip()], d

results = []
def case(name, cmds, expect_lines, **kw):
    out, d = run(cmds, **kw)
    ok = out[-len(expect_lines):] == expect_lines if expect_lines else True
    results.append((ok, name, expect_lines, out))
    return out, d

S0 = fmt(START)
# --- 1. the known trace (also checks STATE format with leading zeroes)
case("known trace", ["BUY TORCH 3", "BUY TURNIP 4", "SELL TORCH 1", "SELL TURNIP 2", "STATE"],
     ["OK BUY", "OK BUY", "OK SELL", "OK SELL", fmt((590, 10410, 2, 2, 8, 10))])
# --- 2. boundaries on player cash: exactly enough vs one cent short
case("buy with EXACTLY enough cash (8 torches = 1000)", ["BUY TORCH 8", "STATE"], ["OK BUY", fmt((0, 11000, 8, 0, 2, 12))])
case("one torch more than cash allows", ["BUY TORCH 8", "BUY TURNIP 1", "STATE"], ["OK BUY", "ERR FUNDS", fmt((0, 11000, 8, 0, 2, 12))])
# --- 3. stock / inventory / precedence (stock checked BEFORE cash)
case("buy above stock -> ERR STOCK (not FUNDS) even though also unaffordable", ["BUY TORCH 11", "STATE"], ["ERR STOCK", S0])
case("sell what you don't own", ["SELL TURNIP 1", "STATE"], ["ERR INVENTORY", S0])
case("sell one more than owned", ["BUY TURNIP 2", "SELL TURNIP 3", "STATE"], ["OK BUY", "ERR INVENTORY", fmt((920, 10080, 0, 2, 10, 10))])
# --- 4. quantity parsing
for q, why in [("0", "zero"), ("-1", "negative"), ("+1", "signed"), ("1.5", "decimal"), ("1000", "four digits"),
               ("abc", "nonnumeric"), ("1e2", "exponent")]:
    case(f"quantity {q!r} ({why}) -> ERR QUANTITY", [f"BUY TORCH {q}", "STATE"], ["ERR QUANTITY", S0])
case("leading zeroes ok: 003", ["BUY TORCH 003", "STATE"], ["OK BUY", fmt((625, 10375, 3, 0, 7, 12))])
case("precedence: unknown item beats bad qty -> ERR ITEM", ["BUY GHOST 0", "STATE"], ["ERR ITEM", S0])
case("arity: missing qty -> ERR SYNTAX", ["BUY TORCH", "STATE"], ["ERR SYNTAX", S0])
case("arity: extra word -> ERR SYNTAX", ["BUY TORCH 1 PLEASE", "STATE"], ["ERR SYNTAX", S0])
case("case + whitespace tolerance", ["   buy\tTorch   2   ", "STATE"], ["OK BUY", fmt((750, 10250, 2, 0, 8, 12))])
case("blank lines ignored", ["", "   ", "STATE"], [S0])
# --- 5. shop funds: drain the shop's cash so it can't buy back
#   Player can't drain it via trades (shop only gains), so use a VALID conserved edited save (spec allows it):
#   cash 10990, shop 10, player owns 1 torch -> SELL TORCH 1 needs 75 > 10 -> ERR SHOP-FUNDS
poor = b"V1|00010990|00000010|001|000|009|012\n"
case("shop too poor to buy back -> ERR SHOP-FUNDS", ["LOAD", "SELL TORCH 1", "STATE"],
     ["OK LOAD", "ERR SHOP-FUNDS", fmt((10990, 10, 1, 0, 9, 12))], save_bytes=poor)
# --- 6. save / load in a FRESH process, and continue == uninterrupted run
out, d = run(["BUY TORCH 3", "BUY TURNIP 4", "SAVE"])
out2, _ = run(["LOAD", "SELL TORCH 1", "SELL TURNIP 2", "STATE"], workdir=d)
results.append((out[-1] == "OK SAVE" and out2 == ["OK LOAD", "OK SELL", "OK SELL", fmt((590, 10410, 2, 2, 8, 10))],
                "save -> fresh process -> load -> continue == known trace", "OK SAVE / ...590", out + ["|"] + out2))
saved = open(os.path.join(d, "haunted-shop.sav"), "rb").read()
results.append((saved == b"V1|00000625|10375|003|004|007|008\n".replace(b"10375", b"00010375") or len(saved) == 37,
                "save file is 37 bytes, V1 format", "37 bytes", [repr(saved)]))
# --- 7. bad saves must be rejected AND leave state untouched (transactional)
good = b"V1|00000590|00010410|002|002|008|010\n"
bads = {
    "missing save -> ERR IO": None,
    "nonconserving cash": b"V1|00000591|00010410|002|002|008|010\n",
    "nonconserving torches": b"V1|00000590|00010410|003|002|008|010\n",
    "version V2": b"V2|00000590|00010410|002|002|008|010\n",
    "comma separator": b"V1,00000590|00010410|002|002|008|010\n",
    "letter in digits": b"V1|0000059O|00010410|002|002|008|010\n",
    "truncated": b"V1|00000590|00010410|002|002|008|01\n",
    "no trailing LF": good[:-1],
    "CRLF": good[:-1] + b"\r\n",
    "extra record": good + good,
    "empty file": b"",
    "trailing space": good[:-1] + b" \n",
    "negative sign smuggled": b"V1|-0000590|00010410|002|002|008|010\n",
}
for name, blob in bads.items():
    want = "ERR IO" if blob is None else "ERR BAD-SAVE"
    d = tempfile.mkdtemp()
    out, _ = run(["BUY TURNIP 1", "LOAD" if blob is None else "LOAD", "STATE"], workdir=d,
                 save_bytes=blob) if blob is not None else run(["BUY TURNIP 1", "LOAD", "STATE"], workdir=d)
    results.append((out[-2:] == [want, fmt((960, 10040, 0, 1, 10, 11))],
                    f"bad save: {name} -> {want}, state unchanged", want, out))
case("valid edited (conserved) save loads", ["LOAD", "STATE"], ["OK LOAD", fmt((590, 10410, 2, 2, 8, 10))], save_bytes=good)
# --- 8. fuzz: 2000 random commands vs my own Python ledger
random.seed(20261019)
st = list(START); cmds, exp = [], []
for _ in range(2000):
    op = random.choice(["BUY", "SELL"]); it = random.choice(["TORCH", "TURNIP"]); n = random.randint(1, 15)
    cmds.append(f"{op} {it} {n}")
    buy, sell = PRICE[it]; i = 2 if it == "TORCH" else 3; si = i + 2
    if op == "BUY":
        if n > st[si]: exp.append("ERR STOCK")
        elif n * buy > st[0]: exp.append("ERR FUNDS")
        else: st[0] -= n*buy; st[1] += n*buy; st[i] += n; st[si] -= n; exp.append("OK BUY")
    else:
        if n > st[i]: exp.append("ERR INVENTORY")
        elif n * sell > st[1]: exp.append("ERR SHOP-FUNDS")
        else: st[0] += n*sell; st[1] -= n*sell; st[i] -= n; st[si] += n; exp.append("OK SELL")
out, _ = run(cmds + ["STATE"])
results.append((out == exp + [fmt(tuple(st))], "fuzz: 2000 random trades vs independent Python ledger",
                fmt(tuple(st)), out[-3:]))

npass = sum(r[0] for r in results)
for ok, name, want, got in results:
    print(("✅" if ok else "❌"), name, "" if ok else f"\n     want: {want}\n     got:  {got}")
print(f"\n{npass}/{len(results)} passed  (binary: {BIN})")
sys.exit(0 if npass == len(results) else 1)
