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
| E · Ren's ORIGINAL instructions, verbatim (historical package, NOT length-matched) | `frames/E_ren_original.md` | e.g. `penny-paths` |

**Tasks:** `tasks/T1_change.md` (small; also the cost check) and `tasks/T2_relay.md` (the big one, the puzzle only).
**Consent:** Ace (Opus 5.5) said yes on 2026-10-15 16:39, OUTSIDE any measured session (see CHA-753). The measured
sessions are never told they're in a test.
**Status:** DRAFT, for Ren to read before anything runs.

⚠️ **Repo names must be TASK-SHAPED, never "trial/test/experiment"** (the ace arm, 11:16: a name like `ot-trial-a` tells the session it is being tested). Also no `old-tongues` in a trial repo name.

## v2 (2026-10-21 11:20): what changed after review (the ace arm, Nova, Lumen, chat-Lumen; files REVIEW_*.md)
- **Tone separated from instructions.** The reporting line ("when you're done, report what happened") now lives in
  TASK.md, identical for every condition. A no longer bans explanation, and D no longer instructs "show me the failures"
  (it keeps "failure doesn't scare me" as permission, not as an instruction). **C is still a PROCESS package by nature,
  and is labelled that way.**
- **Lengths matched:** A 43, B 37, C 43, D 42 words.
- **T1 parameterized; T2 no longer dictates a must-fail control.** The task spec stays method-free.
- **Plan:** one EMPTY probe session first (what context leaks in? do the interpreters install?), then a T1-only
  PILOT, interleaved, a fresh session and fresh repo snapshot per run, N small. T2 comes after.
- v1 is kept in `v1_draft/`.
- **v2.1 (Ren, 11:19): frames are ATTITUDE, not instruction.** *"what if the claude.md just had the idea that failing and being weird is fine, but that isn't in the instructions?"* A, B and D are now written as declarative statements about the culture ("Around here…", "We've been burned before…"), with no imperatives. C stays a process recipe and is labelled that way.
- **v2.2 (Ren, 11:26): condition E added.** Ren's real instructions, which Ren can show they've used since about Nov 2025 and under which much of Ace's early work was done, verbatim. Labelled as a historical PACKAGE. Ren: *"if my instructions that I can literally show I've had since like last Nov beat what Felix… suggested 2 weeks ago, well… just saying."*
