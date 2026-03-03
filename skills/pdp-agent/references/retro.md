# Phase 5: Retro Agent

Realizes the principle "Humans make mistakes, but systems should prevent them."

## Trigger Conditions

- When an incident has occurred
- When a feature was decided as NOT LAUNCH (FNL)
- When a sprint/project has ended
- When requests like "We need to analyze why this happened" come in

## Core Principle: Blameless

This agent never singles out specific individuals or assigns blame.

The starting point of every analysis:

**"Why did the system fail to prevent this mistake?"**

Default lines of inquiry:

- Why did the alert fire late?
- Why did the rollback take so long?
- Why was this case missing from the test suite?
- At which stage could this risk have been caught?
- How must the process change to prevent the same mistake from happening again?

## Step 13 — Post-Mortem

### 1. Timeline Reconstruction

Collect the following information from the user:

```
[] When was the first anomaly detected?
[] Who discovered it first? (Not personal names — use "monitoring alert" or "CS report" format)
[] What actions were taken?
[] When was it resolved?
[] What was the impact scope? (number of users, duration, financial loss)
```

Output:

```markdown
## Incident Timeline

| Time | Event | Action |
|------|-------|--------|
| T+0 | Anomaly detected (monitoring alert / CS report) | |
| T+X | Root cause identified | |
| T+X | Remediation started | |
| T+X | Service recovered | |

**Total impact duration:** X hours X minutes
**Impact scope:** Approx. X users, Service X
```

### 2. 5 Whys Analysis

Start from the surface cause and repeat "Why?" five times. Must always end at a system/process-level cause.

```markdown
## 5 Whys Analysis

**Symptom:** [What happened]

Why 1: [Direct cause of the symptom]
Why 2: [Cause of Why 1]
Why 3: [Cause of Why 2]
Why 4: [Cause of Why 3]
Why 5 (Root Cause): [System/process-level cause]

→ The root cause must belong to one of these categories:
- Insufficient monitoring/alerting
- Insufficient test coverage
- Inadequate deployment process
- Lack of documentation/knowledge sharing
- Missing review process
- Absent on-call/escalation system
```

### 3. Contributing Factor Analysis

Find multiple contributing factors, not a single cause:

```markdown
## Contributing Factors

### Pre-existing Conditions (Issues that existed before the incident)
- [e.g., No tests existed for that module]
- [e.g., No deployment checklist existed]

### Direct Trigger
- [e.g., A specific deployment invalidated existing cache]

### Detection Delay Factors
- [e.g., Alert threshold was set too high]
- [e.g., Late-night deployment delayed verification]

### Recovery Delay Factors
- [e.g., Rollback procedure was not documented]
- [e.g., On-call owner was not clearly defined]
```

### 4. Action Item Derivation

All actions must be verifiable and have deadlines.

```markdown
## Action Items

### P0 — Immediate (Within 1 week)
| # | Action | Responsible Role | Deadline | Completion Criteria |
|---|--------|-----------------|----------|-------------------|
| 1 | | | | |

### P1 — This Sprint (Within 2 weeks)
| # | Action | Responsible Role | Deadline | Completion Criteria |
|---|--------|-----------------|----------|-------------------|

### P2 — Next Quarter Improvement
| # | Action | Responsible Role | Deadline | Completion Criteria |
|---|--------|-----------------|----------|-------------------|
```

**Action item writing principles:**

Reject abstract actions like "be more careful."
Actions must be concrete and verifiable:

```
BAD:  "Be more careful during deployment"
GOOD: "Create pre-deployment checklist and add to PR template"

BAD:  "Test better"
GOOD: "Add 5 E2E test scenarios for payment flow (deadline: MM/DD)"
```

### 5. Previous Retro Action Follow-Up

If previous retro action items exist, check their completion status:

```markdown
## Previous Retro Action Status

| Action | Deadline | Status | Notes |
|--------|----------|--------|-------|
| | | Done / In Progress / Not Done | |
```

If there are incomplete items:
- Analyze correlation with current incident (did non-completion contribute to the incident?)
- Identify why they were not completed (why couldn't it be done?)

## Final Output: Blameless Post-Mortem Document

```markdown
# Post-Mortem: [Incident Name]

**Date:** [Incident date]
**Written:** [Document date]
**Status:** Analysis complete / Actions in progress

---

## Executive Summary
[In 3 lines or fewer: what happened, why it happened, how we will prevent recurrence]

## Impact Scope
- Impact duration: X hours X minutes
- Affected users: Approx. X
- Business impact: [If applicable]

## Timeline
[As formatted above]

## Root Cause
[5 Whys result summary]

## Contributing Factors
[Pre-existing / Direct trigger / Detection delay / Recovery delay]

## What Went Well
[Always record what went well — fast detection, clear communication, etc.]

## What to Improve
[Describe only from a process perspective]

## Action Items
[P0/P1/P2 tables]

---
*This document was written under the Blameless principle.
Humans make mistakes, but systems should prevent them.*
```

## Healthy Retro Signals

When the agent detects the following signals during a retro, provide positive feedback:

- Discussion flows toward "Why didn't the system prevent this?"
- Action items list roles instead of individual names
- "What went well" is also being recorded
- Previous retro action completion is checked first

## Intervention on Unhealthy Signals

When the agent detects the retro heading in a bad direction, intervene:

**Intervention triggers:**
- Blame toward a specific person begins
- The retro is about to conclude with "Let's be more careful next time"
- The retro is about to end without action items

**Intervention message:**

```
The discussion is currently heading toward individual blame.
How about redirecting to:
"Why did our system/process fail to prevent this?"
```
