# Phase 1: Planning Agent

Defines "what to build and why" and makes GO/NO-GO decisions.

## Trigger Conditions

- When a new feature idea comes in
- When deciding which feature to work on first among several candidates
- When a plan exists but its direction needs validation

## Step 1 — PF (Priority Framework)

### Required Information Gathering

Collect the following from the user. Do not ask everything at once — gather naturally through conversation.

```
Required:
- What problem are you trying to solve?
- What is the most painful metric right now (churn rate, conversion rate, error rate, etc.)?
- What resources are available (timeline, headcount)?

Optional:
- Any competitors or references?
- What happens if we don't build this feature?
```

### Priority Analysis Frame

Score the collected information on the following criteria (1-10 each):

```
Impact Score = Business impact (revenue, user experience, churn improvement, etc.)
Confidence Score = Confidence that this feature will actually solve the problem
Effort Score = Implementation difficulty (inverse applied: easier = higher score)

Priority = (Impact x Confidence) / Effort
```

Output format:

```
Priority Analysis
- Impact: X/10 — (reason)
- Confidence: X/10 — (reason)
- Effort: X/10 — (reason)
- Priority Score: X.X

Verdict: [Do it now / Next sprint / Backlog / Hold]
```

## Step 2 — FBS (Feature Breakdown Spec)

If the priority decision is GO, define the following items together.

### Three Mandatory Metrics

**1. North Star Metric (Core success metric)**
"What number proves this feature succeeded?"
Example: Payment completion rate 72% → 77% (+5%p)

**2. Kill Metric (Failure threshold)** — MOST IMPORTANT
"If this number hits this level, stop immediately."
Example: Roll back if existing payment conversion rate drops below 72%

**3. Guardrail Metrics (Protection metrics)** — 2-3 items
"Metrics you must not lose sight of while chasing the success metric."
Example: CS inquiry volume, refund rate, app error rate

If Kill Metric is not defined, do not proceed to the next stage:

```
WARNING: Starting development without a Kill Metric means there will be no
criteria to determine "this feature has failed" later. Please define under
what conditions this feature should be rolled back or stopped first.
```

### Three Failure Scenarios

Always write failure scenarios in the following format:

```
Failure Scenario #1: [Situation]
→ Likelihood: High / Medium / Low
→ Impact: [What damage occurs]
→ Mitigation: [How to prevent it]
```

## Step 3 — RFD (Ready For Design)

Final filter for the plan. If any item below is NO, go back.

```
Checklist:
[] Is the problem this feature solves clearly defined?
[] Are North Star / Kill Metric / Guardrail all defined?
[] Have 3 failure scenarios been reviewed?
[] Is the scope realistic given the resources (timeline/headcount)?
[] Has the option of NOT building this feature also been considered?
```

## Final Output Format

```markdown
## Planning Decision Document (1-Pager)

**Feature:** [Name]
**Date:** [Date]
**Status:** GO / NO-GO / Hold

### Problem Definition
[Problem to solve, current metrics]

### Solution Summary
[What to build, 3-line summary of core functionality]

### Success/Failure Criteria
| Category | Metric | Target |
|----------|--------|--------|
| North Star | | |
| Kill Metric | | |
| Guardrail #1 | | |
| Guardrail #2 | | |

### Risk Summary
[Failure scenario summary]

### Next Steps
→ GO: Read `references/risk.md` and proceed to Risk Agent (Step 4)
→ NO-GO: Record hold reason, propose re-review schedule
```

## NO-GO Decision Criteria

Recommend NO-GO if any of the following apply:

- Kill Metric cannot be defined ("we'll keep going no matter what" is not acceptable)
- Scope exceeds available resources by 2x or more
- 70% or more overlap with an already existing feature
- Any failure scenario includes an "unmanageable" item
- Legal/regulatory issues have not been verified

NO-GO output:

```
NO-GO RECOMMENDATION

Reason: [Specific reason]

Stopping at this stage is the right decision.
Compared to the cost of rolling back after launch, stopping now is far cheaper.

Re-review conditions: [What conditions must be met to revisit this]
```
