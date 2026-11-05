# Running a deck workshop (teacher's notes)

This folder is a reusable workshop for building projector slide decks for any lesson of the Chemistry Case Files site, with Claude Fable 5.1 as orchestrator in your account (A) and Claude Opus 5.5 as implementer in a school account (B). The reference implementation is the newest accepted Unit 4 decks on `main` (or the branch that carries the reference decks, the kit and this folder; today that is claude/unit-4-chemistry-slides-j62190 until it is merged) (at least `unit4/slides-4-1.html` and `unit4/slides-4-2.html`); older decks are archived under `unit4/old-slides/` and are not used; every new deck copies their engine, templates, chrome, register and audits; when the accepted 4.3, 4.4 and 4.5 decks are on the base they are reference too.

## Same-account workshop (school account: Fable 5.1 orchestrates, Opus 5.5 implements as its in-session agent)
Paste one message in the school account:
```
Open jivishov/texaschemistry, read workshop/ORCHESTRATOR.md, and run a workshop.
Assignment: unit 5, lessons 5.1 and 5.2. Mode: in-session, lean. Base: main. Priority: 5.1 first.
```
Fable creates the workshop branch from the base, writes the lesson sheets and the plan, sends you the plan to confirm, then builds one lesson at a time with Opus as its agent (extra-high effort for builds, high for fixes), commits each accepted step to the workshop branch, and sends you each deck as soon as it is accepted. `lean` keeps the token use within a weekly limit (PROTOCOL.md, Lean mode): one step per lesson, one light-theme suite per step, the dark theme and the zoom matrix once at the end. Work can stop at any gate and resume next week with the same message plus "resume". Nothing reaches `main` until you merge the pull request.

## Once
1. The reference decks, the kit `tools/slides-kit/` and this `workshop/` folder are on the branch `claude/unit-4-chemistry-slides-j62190`; merge it into `main` or name that branch as the base in the start message.
2. Give account B the repository through its own GitHub connector with write access (collaborator on the repo, Claude GitHub App installed for it).

## Per workshop, your three moments
1. **Start.** In account A, paste one message (template below). Fable creates the workshop branch and the draft pull request, writes the assignment, the lesson sheets and the plan, and replies with the exact one-line start message for account B.
   ```
   Open jivishov/texaschemistry, read workshop/ORCHESTRATOR.md, and run a workshop.
   Assignment: unit 4, lessons 4.5 and 4.6. Mode: cross-account. Base: main. Priority: 4.5 first.
   ```
   You may add wishes in plain words ("hook with the Texas freeze", "urgent, one deck is enough this week").
2. **Confirm the plan** when Fable sends it; then start account B with the line Fable gave you (set extra-high effort for build steps; when Fable asks for a fix round, restart B at high effort). The same line resumes either side at any time; `workshop/status.md` tells each side what to do.
3. **Review each deck** when Fable sends it with its sheets; send screenshots and remarks back to Fable. At the end say "merge" (or "commit and push"); Fable writes FINAL.md, the implementer strips the sheets, and you merge the pull request.

Wake-ups: each side subscribes its session to the pull request, so a comment from the other side wakes it. If a side does not wake, paste its start line again.

Optional in-session mode (one account): say `Mode: in-session` and Fable spawns Opus itself as an in-session agent; the rest is unchanged.
