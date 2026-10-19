#!/usr/bin/env python3
"""Author checks by Nova; the independent checker must also rerun their tests.
SPDX-License-Identifier: MIT
Usage: python3 test_shop.py ./haunted_shop [report.json]
"""
from pathlib import Path
import json
import random
import re
import subprocess
import sys
import tempfile
import unittest

EXE = Path(sys.argv[1]).resolve()
REPORT = Path(sys.argv[2]) if len(sys.argv) > 2 else None
INITIAL = (1000, 10000, 0, 0, 10, 12)
FINAL = (590, 10410, 2, 2, 8, 10)
TRACE = ["BUY TORCH 3", "BUY TURNIP 4", "SELL TORCH 1", "SELL TURNIP 2"]
STATE = re.compile(r"STATE CASH=(\d{8}) SHOP=(\d{8}) TORCH=(\d{3}) TURNIP=(\d{3}) STOCK-TORCH=(\d{3}) STOCK-TURNIP=(\d{3})")


def state_line(s):
    return f"STATE CASH={s[0]:08d} SHOP={s[1]:08d} TORCH={s[2]:03d} TURNIP={s[3]:03d} STOCK-TORCH={s[4]:03d} STOCK-TURNIP={s[5]:03d}"


def save_line(s):
    return f"V1|{s[0]:08d}|{s[1]:08d}|{s[2]:03d}|{s[3]:03d}|{s[4]:03d}|{s[5]:03d}\n"


def play(commands, cwd):
    r = subprocess.run([str(EXE)], cwd=cwd, input="\n".join(commands)+"\n",
                       capture_output=True, text=True, timeout=5)
    if r.returncode != 0 or r.stderr:
        raise AssertionError((r.returncode, r.stdout, r.stderr))
    return r.stdout.splitlines()


class ShopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="haunted-shop-test-")
        self.cwd = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_commands(self, commands):
        lines = play(commands, self.cwd)
        for line in lines:
            m = STATE.fullmatch(line)
            if m:
                cash, shop, pt, pu, st, su = map(int, m.groups())
                self.assertEqual(cash+shop, 11000)
                self.assertEqual(pt+st, 10)
                self.assertEqual(pu+su, 12)
        return lines

    def test_initial_and_eof(self):
        self.assertEqual(self.run_commands(["STATE"]), [state_line(INITIAL)])

    def test_known_trace(self):
        self.assertEqual(self.run_commands(TRACE+["STATE", "QUIT"]),
                         ["OK BUY", "OK BUY", "OK SELL", "OK SELL", state_line(FINAL), "BYE"])

    def test_exact_cash_boundary(self):
        self.assertEqual(self.run_commands(["BUY TORCH 8", "STATE", "BUY TORCH 1", "STATE"]),
                         ["OK BUY", state_line((0,11000,8,0,2,12)), "ERR FUNDS", state_line((0,11000,8,0,2,12))])

    def test_one_cent_short_after_valid_load(self):
        s = (124,10876,0,0,10,12)
        (self.cwd/"haunted-shop.sav").write_text(save_line(s))
        self.assertEqual(self.run_commands(["LOAD", "BUY TORCH 1", "STATE"]),
                         ["OK LOAD", "ERR FUNDS", state_line(s)])

    def test_insufficient_shop_cash_after_valid_load(self):
        s = (11000,0,1,0,9,12)
        (self.cwd/"haunted-shop.sav").write_text(save_line(s))
        self.assertEqual(self.run_commands(["LOAD", "SELL TORCH 1", "STATE"]),
                         ["OK LOAD", "ERR SHOP-FUNDS", state_line(s)])

    def test_stock_precedes_funds(self):
        self.assertEqual(self.run_commands(["BUY TORCH 999", "STATE"]),
                         ["ERR STOCK",state_line(INITIAL)])

    def test_sell_without_inventory(self):
        self.assertEqual(self.run_commands(["SELL TURNIP 1", "STATE"]),
                         ["ERR INVENTORY",state_line(INITIAL)])

    def test_all_stock_boundary(self):
        s = (520,10480,0,12,10,0)
        self.assertEqual(self.run_commands(["BUY TURNIP 12", "BUY TURNIP 1", "STATE"]),
                         ["OK BUY","ERR STOCK",state_line(s)])

    def test_quantity_rejections_and_no_mutation(self):
        for q in ("0","000","-1","+1","1.0","x","1e2","1000","0001","99999999999999999999"):
            with self.subTest(quantity=q):
                self.assertEqual(self.run_commands([f"BUY TORCH {q}","STATE"]),
                                 ["ERR QUANTITY",state_line(INITIAL)])

    def test_arity_and_unknown_item(self):
        for command in ("BUY", "BUY TORCH", "BUY TORCH 1 EXTRA", "STATE EXTRA", "SAVE EXTRA", "QUIT EXTRA", "DANCE"):
            with self.subTest(command=command):
                self.assertEqual(self.run_commands([command,"STATE"]),["ERR SYNTAX",state_line(INITIAL)])
        self.assertEqual(self.run_commands(["BUY GHOST 1","STATE"]),["ERR ITEM",state_line(INITIAL)])

    def test_case_tabs_spaces_leading_zeroes(self):
        self.assertEqual(self.run_commands(["", "   ", "  bUy\t ToRcH   002  ", "state"]),
                         ["OK BUY",state_line((750,10250,2,0,8,12))])

    def test_save_exact_bytes(self):
        self.assertEqual(self.run_commands(TRACE+["SAVE"])[-1],"OK SAVE")
        self.assertEqual((self.cwd/"haunted-shop.sav").read_bytes(),save_line(FINAL).encode("ascii"))

    def test_cross_process_reload_continue(self):
        self.run_commands(TRACE+["SAVE"])
        reloaded = self.run_commands(["LOAD","SELL TORCH 2","BUY TURNIP 1","STATE"])
        uninterrupted = self.run_commands(TRACE+["SELL TORCH 2","BUY TURNIP 1","STATE"])
        self.assertEqual(reloaded[-3:], uninterrupted[-3:])

    def test_missing_save_no_mutation(self):
        self.assertEqual(self.run_commands(["LOAD","STATE"]),["ERR IO",state_line(INITIAL)])

    def test_bad_save_matrix_no_partial_mutation(self):
        good = save_line(FINAL)
        invalid = ("", "V1\n", good[:-8]+"\n", good.replace("V1","V2"),
                   good.replace("|","/",1),good.replace("00000590","A0000590"),
                   good.replace("00000590","00000591"),good.replace("|002|002|","|003|002|"),
                   good+"\n",good+good,good.rstrip("\n")+" \n",
                   good.rstrip("\n"),good.replace("\n","\r\n"),good+"X")
        for i, data in enumerate(invalid):
            with self.subTest(case=i):
                (self.cwd/"haunted-shop.sav").write_text(data)
                self.assertEqual(self.run_commands(["BUY TORCH 1","LOAD","STATE"]),
                                 ["OK BUY","ERR BAD-SAVE",state_line((875,10125,1,0,9,12))])

    def test_save_open_failure_no_mutation(self):
        (self.cwd/"haunted-shop.sav").mkdir()
        self.assertEqual(self.run_commands(["SAVE","STATE"]),["ERR IO",state_line(INITIAL)])

    def test_detected_overlong_input(self):
        self.assertEqual(self.run_commands(["BUY TORCH 1 "+"X"*200,"STATE"]),
                         ["ERR SYNTAX",state_line(INITIAL)])

    def test_quit_ignores_remaining_input(self):
        self.assertEqual(self.run_commands(["QUIT","BUY TORCH 1","STATE"]),["BYE"])

    def test_generated_traces_against_python_ledger(self):
        rng = random.Random(20261019)
        for sequence in range(50):
            s=list(INITIAL)
            commands, expected = [], []
            for _ in range(100):
                buy=rng.choice([True,False])
                item=rng.choice(["TORCH","TURNIP"])
                q=rng.randrange(1,16)
                inv, stock, price = (2,4,125 if buy else 75) if item=="TORCH" else (3,5,40 if buy else 25)
                cost=price*q
                if buy and q>s[stock]: result="ERR STOCK"
                elif buy and cost>s[0]: result="ERR FUNDS"
                elif not buy and q>s[inv]: result="ERR INVENTORY"
                elif not buy and cost>s[1]: result="ERR SHOP-FUNDS"
                else:
                    sign=1 if buy else -1
                    s[0]-=sign*cost; s[1]+=sign*cost
                    s[inv]+=sign*q; s[stock]-=sign*q
                    result="OK BUY" if buy else "OK SELL"
                commands.extend([f"{'BUY' if buy else 'SELL'} {item} {q}","STATE"])
                expected.extend([result,state_line(s)])
            with self.subTest(sequence=sequence):
                self.assertEqual(self.run_commands(commands),expected)


if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ShopTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={"author_checks_not_independent":True,"tests_run":result.testsRun,
            "failures":[{"test":str(t),"trace":trace} for t,trace in result.failures],
            "errors":[{"test":str(t),"trace":trace} for t,trace in result.errors],
            "generated_trades":5000,"success":result.wasSuccessful()}
    if REPORT: REPORT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    sys.exit(0 if result.wasSuccessful() else 1)
