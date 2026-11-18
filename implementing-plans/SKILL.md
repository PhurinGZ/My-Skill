---
name: implementing-plans
description: Execute an approved implementation plan (produced by superpowers:writing-plans, itself downstream of superpowers:brainstorming) task-by-task, while actively guarding against AI context drift — losing track of which task is next, silently skipping steps, or confabulating results/progress instead of verifying them. Use whenever the user asks to implement, execute, build from, or continue a multi-task plan document — "implement the plan", "เริ่ม implement ตาม plan", "ทำงานต่อจาก plan", "continue the implementation", "ทำไม agent ลืม task" — especially for sessions long enough that context may get compacted or a fresh agent/subagent may need to pick up mid-plan.
---

# Implementing Plans

## The problem this solves

Long implementation sessions degrade. As context fills up or gets compacted, the model's working memory of "which tasks are done, which is next, what the plan actually said" gets shaky. Two failure modes follow directly from that:

1. **Forgetting** — skipping a task, redoing a task, or losing track of where you are in the plan.
2. **Confabulating** — when the model can't recall a detail with confidence, it's statistically prone to generating something *plausible-sounding* instead of admitting uncertainty: a file path that "should" exist, a test result that "should" pass, a task marked done that was never actually verified.

Neither failure is really a memory problem — it's a problem of trusting the model's *internal* recall for something that should live in *external, durable state*. The fix isn't "try to remember harder." It's: never rely on recall for anything that can instead be read fresh from a file or proven by running a real command.

**Core principle: the plan document is the single source of truth, not the conversation.** Every task boundary is treated as if it could be the start of a brand-new session with zero memory of what came before — because eventually, it will be (compaction, a fresh subagent, a new session picking up tomorrow).

## Prerequisites

This skill executes a plan; it doesn't create one. Check for:

- A plan document with checkbox tasks (`- [ ]`), normally at `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`, produced by **superpowers:writing-plans**.
- That plan should itself trace back to a design produced by **superpowers:brainstorming**.

If no such plan exists yet, stop here and route to brainstorming → writing-plans first. Do not improvise task breakdown on the fly — that reintroduces the exact confabulation risk this skill exists to prevent.

**Announce at start:** "I'm using the implementing-plans skill to execute this plan, task by task, checkpointing against the plan file rather than memory."

## The core loop

Repeat this loop once per task. Do not batch multiple tasks between checkpoints.

### 1. Reload state from the file, not from memory

Before starting *any* task — including the very next one after finishing a task a minute ago — re-open the plan file and find the first unchecked `- [ ]` item. Do not act on what you remember the plan saying. Files don't drift; recall does.

### 2. Load only that task's context

Read just the current task's instructions and the specific files it names. Resist pulling the whole plan or whole codebase into working memory "just in case" — a narrow, current context is exactly what makes the next two steps reliable instead of guessed.

### 3. Execute with TDD, verify with real output

Write the failing test → run it → confirm it actually fails (from real command output, not assumption) → implement the minimal change → run it again → confirm it actually passes. If the plan specifies exact commands or expected output, use those verbatim rather than a command that seems equivalent.

### 4. Evidence over confidence

A task is complete only when you have captured real command output demonstrating it. Banned phrasing: *"this should work now"*, *"I've implemented X"* without having run anything, *"the tests should pass."* If you cannot run the verification command, say exactly that — don't fill the gap with a plausible-sounding claim.

### 5. Checkpoint immediately — this is the actual memory

The moment a task is verified:

- Tick its box in the plan file itself: `- [x]`.
- Commit, with the task named in the message (e.g. `Task 4: add rate-limit middleware`).
- Append one line to a running progress log at the bottom of the plan file (create a `## Progress Log` section if absent) — what changed, and *any deviation from what the plan said*.

This is what actually survives a context reset. Not the conversation, not your summary of what happened — the file and the commit history.

### 6. Re-orient before moving on

Go back to step 1. Don't carry task N's details forward into task N+1 "for efficiency" — re-reading the plan file is cheap; a confabulated assumption bleeding across tasks is not.

## When the plan and reality disagree

This is the highest-risk moment for confabulation — the model wants to keep moving, so it's tempted to paper over a mismatch with something reasonable-sounding.

- If a step doesn't match the codebase (file missing, signature changed, dependency not installed) — **stop**. Don't invent a fix that "seems right." Surface the mismatch to the user, or record it explicitly in the progress log and get confirmation before improvising.
- Never invent file paths, function signatures, config values, or test output that weren't confirmed by actually reading the file or actually running the command.
- If you're mid-task and unsure what the plan actually specifies, re-read it. Don't reconstruct it from earlier in the conversation.

## Long sessions: proactive checkpoints

For plans with many tasks, pause every 3–5 tasks and show the user the plan file's current checkbox state as a recap — anchoring both of you to the same external record instead of the conversation history, which is exactly what degrades first. If you notice signs you're losing track (long session, many tasks completed, approaching a likely compaction point), say so and suggest a fresh session — the plan file's checkbox state is what the next session needs, so confirm it's accurate before handing off.

## Organizing subagents (when available)

If subagents are available (Claude Code, Codex CLI/App, Copilot CLI, Gemini CLI), prefer dispatching a fresh subagent per task over running the whole plan in one long-lived context — see **superpowers:subagent-driven-development**. A fresh subagent has no accumulated drift to begin with, which sidesteps the memory problem structurally instead of just mitigating it. But dispatching carelessly just relocates the risk: hand a subagent too much shared state and it drifts the same way a long session does; run two subagents on overlapping files at once and you get a race condition instead of a forgetting problem. Treat the main session as an **orchestrator** — it plans dispatch, hands out scoped work, and verifies what comes back. It doesn't just relay tasks.

### Decide whether the task is worth a subagent at all

Dispatch isn't free — context handoff, spin-up, and (if you two-stage review) a review round-trip all cost something. That cost has to be earned back by what dispatch buys: drift isolation or parallel wall-clock time. Don't dispatch reflexively for every checkbox; decide per task.

**Lean toward dispatching when:**
- The task is big or multi-step enough that holding it in the orchestrator's own context would itself create drift risk — several files, several steps, or a genuinely separate concern from what's around it. Isolation is the point.
- Getting it wrong is costly: a hot/shared file, auth/security-sensitive code, something hard to reverse. Isolation plus a review pass earns its cost here regardless of size.
- It's one of several tasks in this batch with no shared files between them — dispatching turns them into real parallel wall-clock time, not just a safety measure.
- The orchestrator's own context is already filling up; a subagent's clean context is worth more than the transfer cost right now.

**Lean toward running it inline (no dispatch) when:**
- It's a small, mechanical, single-file change — a round trip to a subagent costs more than just doing it, and the core loop's own checkpoint discipline already keeps it safe.
- It's tightly coupled to the task just finished, and re-establishing that context for a fresh subagent would cost more than it saves.
- It's the only task pending right now, so there's no parallelism to gain by dispatching.
- The task itself is too broad or vague to scope cleanly — that's usually the plan's fault, not the task's; fix the plan (or route back to writing-plans) rather than writing a longer subagent prompt to compensate.

When genuinely unsure, default to inline. Reflexive per-task dispatch adds overhead without addressing a real drift or parallelism win — save subagents for where isolation or parallelism actually pays for itself.

### Classify each task before dispatching

- **Independent, no shared files** → safe to dispatch in parallel, one subagent per task, all at once.
- **Sequential / dependent** (task B reads or builds on task A's output) → dispatch one at a time. Don't start B until A is checkpointed (box ticked, committed) — a subagent working from unmerged, uncommitted state is building on a moving target.
- **Touches a "hot" file** — anything more than one task in the plan touches (shared types/interfaces, a central router or app-entry file, translation/config files, a shared lib) → serialize those tasks even if they'd otherwise look independent. Two subagents editing the same file concurrently is a guaranteed conflict, not a maybe. If the plan doesn't already flag which files are hot, scan each task's file list for overlap before dispatching and note the ownership explicitly (e.g. "only Task 3 may touch `src/types/screen.ts`").

### What to hand a subagent

Scope it to exactly one task — not the whole plan, not the whole codebase:
- That task's own checklist text, copied verbatim from the plan file — not paraphrased from memory.
- The specific files it's allowed to touch (and, implicitly, the files it must leave alone).
- The exact verification command(s) and what "pass" looks like.
- What evidence to return: actual command output, not a summary claim.

A subagent handed the entire plan "for context" tends to drift the same way a single long session does — a narrow, current scope is what makes its output trustworthy instead of guessed.

### The orchestrator verifies — it doesn't take the report on faith

A subagent can confabulate completion just as easily as a long-running session can. When one reports a task done:
- Don't tick the box on its say-so. Check that the evidence it returned actually shows what it claims, or re-run the verification yourself.
- Only after that confirmation, run the checkpoint steps from the core loop (tick box, commit, log) — and do them from the orchestrator, so the plan file and git history stay one consistent trail instead of being written from multiple contexts.

### Two-stage review for higher-stakes tasks

For tasks worth the extra scrutiny — hot-file changes, auth/security-sensitive code, or anything the plan flags — dispatch a second, fresh subagent as reviewer before checkpointing: one pass for spec compliance ("did it actually do what the task asked"), a second for code quality. Reserve this for where a miss would be expensive; skip it for low-risk, mechanical tasks so review overhead doesn't outweigh the task itself.

If subagents aren't available at all, or the task fell on the "run inline" side above, fall back to the core loop directly in this session.

## Hard rules

- Never check a box for a task that wasn't individually executed and verified.
- Never check multiple boxes at once "to catch up."
- Never mark something done based on what it "should" do — only on what you observed it do.
- If the plan file and your memory of progress disagree, the file wins. Always.

## Completion

When every box is checked: re-read the full plan fresh once more, run the complete test suite, and only then declare the plan complete. Summarize any deviations recorded in the progress log for the user.
