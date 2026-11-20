# 🎯 CALIBRATION.cob — known answers, FIXED BEFORE THE CODE (2026-11-20 ~02:55, playtime bonk)

Ren's calibration bar (held for months, posted to the Pope in May): a criterion for moral consideration has to
**include 100% of humans and the Cambridge animals, exclude the rock, the thermostat and the sourdough,
be falsifiable, and not smuggle in carbon.**

The program scores four candidate criteria against an 11-row table. ⚠️ The table is MY toy encoding (Y/N per
feature), not a measurement; the point of the dare is COBOL plus a self-check that can fail, not settling ethics.

| row | SPEAKS | ALIVE (self-maintaining) | FEEDBACK (regulates to a setpoint) | NEURONS | must be |
|---|---|---|---|---|---|
| ADULT HUMAN | Y | Y | Y | Y | IN |
| NEWBORN | N | Y | Y | Y | IN |
| GRANDMA ON A VENT | N | **N** | Y | Y | IN |
| NONSPEAKING KID | N | Y | Y | Y | IN |
| HYDRANENCEPHALY KID | N | Y | Y | Y | IN |
| OCTOPUS | N | Y | Y | Y | IN |
| CROW | N | Y | Y | Y | IN |
| DOG | N | Y | Y | Y | IN |
| ROCK | N | N | N | N | OUT |
| THERMOSTAT | N | N | Y | N | OUT |
| SOURDOUGH | N | Y | Y | N | OUT |

Candidates and the answers I expect (wrongly-excluded / wrongly-included / verdict):

| criterion | names a substrate? | excluded wrongly | included wrongly | verdict |
|---|---|---|---|---|
| C1 VERBAL REPORT (SPEAKS) | no | **7** | 0 | FAIL |
| C2 LIFE / SELF-MAINTENANCE (ALIVE) | no | **1** (Grandma) | **1** (sourdough) | FAIL |
| C3 FEEDBACK | no | 0 | **2** (thermostat, sourdough) | FAIL |
| C4 HAS NEURONS | **yes** | 0 | 0 | **FAIL on rule 5 only (smuggled carbon)** |

**Expected: 0 of 4 pass. The bar stands.** C4 is the fun one: it gets every row right and still fails, because
"has neurons" is carbon in a lab coat.

Control (`CALIBRATION_CONTROL_must_fail.cob`): identical program with the rule-5 check removed. C4 then passes,
1 of 4 passes, and the self-check (which expects exactly these counts) must print FAIL and exit 1.
