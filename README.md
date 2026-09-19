# Project Status Report Agent

An AI agent that synthesizes scattered team updates into a single, clean status report — built with the [Claude API](https://docs.claude.com).

## The problem

Anyone who's coordinated a project knows this cycle: chase down updates from several people (usually in different formats — a Slack message here, a half-finished email there, a verbal update you jotted notes on), figure out what's actually on track vs. at risk, reconcile anything that doesn't quite line up, and turn it all into something a stakeholder can read in 30 seconds. It's necessary work, but it's also repetitive synthesis, not judgment about the project itself.

## What this agent does

Given raw, informal updates from multiple team members, it produces a structured report with:

1. **Overall status** — On Track / At Risk / Blocked, with a clear justification
2. **Highlights** — what's going well
3. **Risks & blockers** — called out explicitly, not softened or buried
4. **Next steps** — what's happening next and who owns it, when stated

Two things it's deliberately built *not* to do: invent details that weren't in the raw updates, and silently resolve contradictions between team members. If two people's updates disagree, it says so rather than picking one — that's a judgment call that belongs to the human reviewing the report, not the agent.

## Example output

Given three raw, informal updates from an engineering, design, and QA lead about the same project, the agent produces something like:

```
**Overall status: At Risk**
Frontend completion is dependent on design assets that are not yet
finalized, and full QA cannot begin until frontend is complete —
creating a bottleneck in the final days before the target date.

**Highlights**
- Backend API is complete and in QA
- Design assets are in final polish, expected to Dana's team tomorrow
- Frontend is ~80% complete

**Risks & blockers**
- Final screens are blocked pending design assets
- Full QA pass cannot start until frontend is complete, compressing
  the QA timeline

**Next steps**
- Marcus (Design) to deliver final assets to Dana's team (~tomorrow)
- Dana's team to complete remaining frontend work post-handoff
- Priya's team to begin full QA once frontend is complete
```

(Full sample saved to `sample_status_report.md` when you run the script.)

## How it works

- Single Claude API call — the "workflow" here is the structuring and synthesis logic embedded in the system prompt, not a multi-step tool chain
- Explicitly instructed not to fabricate details or silently resolve conflicting updates — a design choice aimed at keeping the report trustworthy for actual stakeholder use
- Output is plain markdown, easy to paste into Slack, email, or a project doc

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python agent.py
```

## Tech

- Python
- [Anthropic Claude API](https://docs.claude.com) (Claude Sonnet)
- Structured summarization
