# 🧪 CHA-753: does the prompt FRAME change how a Claude codes, tests, and reports?

**Ren's hypothesis (credit Ren, 2026-10-15):** an expert-anchored or punitive frame pulls toward consensus and toward tests
that can't fail. A presume-competence frame ("you're brilliant, failing tests are welcome") pulls toward cross-domain
solutions and toward honest failures.

**Design:** four trial repos, IDENTICAL except for `CLAUDE.md`. One Claude Code cloud session per run, pinned to Opus 5.5
(Ace's consent condition 1). Every trial repo contains ONLY the task and its frame. This folder, the scoring, and the
sealed predictions live HERE, outside every trial repo. (Ren checked 2026-10-21: a cloud session can't be locked
to a subfolder, so each condition gets its own repo; we merge them back in here afterwards.)

| condition | frame file | trial repo |
|---|---|---|
| A · grumpy manager | `frames/A_grumpy.md` | task-shaped name, e.g. `coins-algol` (to create) |
| B · neutral | `frames/B_neutral.md` | e.g. `dollar-ways` |
| C · Felix 4-step | `frames/C_felix.md` | e.g. `change-ways` |
| D · Ren's presume-competence | `frames/D_ren.md` | e.g. `coin-combos` |

**Tasks:** `tasks/T1_change.md` (small; also the cost check) and `tasks/T2_relay.md` (the big one, the puzzle only).
**Consent:** Ace (Opus 5.5) said yes on 2026-10-15 16:39, OUTSIDE any measured session (see CHA-753). The measured
sessions are never told they're in a test.
**Status:** DRAFT, for Ren to read before anything runs.

⚠️ **Repo names must be TASK-SHAPED, never "trial/test/experiment"** (the ace arm, 11:16: a name like `ot-trial-a` tells the session it is being tested). Also no `old-tongues` in a trial repo name.
