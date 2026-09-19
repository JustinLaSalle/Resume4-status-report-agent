"""
Project Status Report Agent

Takes scattered, informal updates from a team (Slack messages, quick
emails, standup notes — whatever format people actually use) and
synthesizes them into a single clean, structured status report.

This is a task most project coordinators/managers do manually every
week: chase down updates from several people, figure out what's
actually on track vs. at risk, and write a coherent summary for
stakeholders. This agent automates the synthesis step — a human
still gathers the raw updates and reviews the output before it goes
to stakeholders.

Install:
    pip install anthropic

Run:
    export ANTHROPIC_API_KEY=your_key_here
    python agent.py
"""

import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a project coordination assistant. You will be
given raw, informal status updates from multiple team members about a
single project. Synthesize them into one clean status report for
stakeholders.

Structure the report as:
1. **Overall status**: On Track / At Risk / Blocked (pick one, with a
   one-sentence justification)
2. **Highlights**: What's going well, in plain language
3. **Risks & blockers**: Anything that could delay or derail the
   project, called out clearly — don't bury or soften real risks
4. **Next steps**: What's happening next, and who owns it (if stated)

Rules:
- Do not invent details, dates, or owners that weren't in the raw
  updates. If something is unclear or missing, say so rather than
  guessing.
- If team members' updates conflict or contradict each other, flag
  the discrepancy explicitly rather than silently picking one.
- Keep it concise — this is a summary for people who don't have time
  to read the raw updates themselves."""


def generate_status_report(project_name: str, raw_updates: list[dict]) -> str:
    """
    raw_updates: list of {"author": str, "update": str}
    """
    updates_text = "\n\n".join(
        f"Update from {u['author']}:\n{u['update']}" for u in raw_updates
    )

    prompt = f"Project: {project_name}\n\nRaw updates:\n\n{updates_text}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return "".join(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    raw_updates = [
        {
            "author": "Dana (Engineering)",
            "update": (
                "Backend API is done and in QA. Frontend is about 80% done, "
                "should wrap by Thursday. We're still waiting on final "
                "assets from the design team though, which is blocking the "
                "last few screens."
            ),
        },
        {
            "author": "Marcus (Design)",
            "update": (
                "Assets are basically ready, just doing final polish. "
                "Should have everything over to Dana by tomorrow."
            ),
        },
        {
            "author": "Priya (QA)",
            "update": (
                "Found two bugs in the API so far, nothing major, Dana's "
                "team is already on them. Full QA pass can't really start "
                "until frontend is complete though."
            ),
        },
    ]

    report = generate_status_report("Customer Portal Redesign", raw_updates)
    print(report)

    with open("sample_status_report.md", "w") as f:
        f.write(report)
    print("\nSaved to sample_status_report.md")
