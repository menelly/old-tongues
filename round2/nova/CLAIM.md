# Nova solo claim: APL Haunted Economy Model Checker

Pinned before APL implementation. Finite economy: 24 cash units total, 3 torches, 4 turnips. State (player cash, player torches, player turnips); shop holds complements. All 500 possible states are enumerated. Initial (12,0,0). One-item trades: buy torch 5, sell torch 3, buy turnip 3, sell turnip 1. Require seller stock and payer funds, never borrow. Every legal trade conserves total cash and each item. No self-loops. Construct full legal directed graph; enumerate reachable states, reachable terminal states, shortest distance layers, maximum legal trace length; certify no reachable cycle. Emit complete reachable-state and edge certificates for external independent checking, not only summary counts.

Negative control: change torch resale to 5. Buy/sell torch is now a reachable 2-cycle, which must be detected rather than certified terminating. Finite-state claims only, not real finance. Python oracle written before APL; another mind must rebuild/rerun APL.

Independent analytic cross-check before APL: rank cash + 4*torches + 2*turnips decreases by exactly one on every original-price trade. Thus cycles are impossible. The reachable terminal rank is 2, initial rank 12, so every maximal initial trace has exactly 10 trades. The fair-resale control breaks this ranking and has an explicit 2-cycle.
