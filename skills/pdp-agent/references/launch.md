# Phase 4: Launch Agent

Realizes the principle "Everyone becomes humble in front of data."

## Trigger Conditions

- When QA is passed and deployment is ready
- When A/B test design is needed
- When A/B test result data is available
- When questions like "Can we deploy this to everyone now?" arise

## Step 9 — RFT (Ready For Testing in production)

### Pre-Deployment Mandatory Checklist

**Rollback readiness:**
```
[] Feature Flag applied (can it be toggled off immediately?)
[] Rollback procedure documented (executable by anyone)
[] Expected rollback time: within X minutes
[] DB migration rollback feasibility confirmed
```

**Monitoring:**
```
[] Core metrics dashboard ready (North Star, Kill Metric)
[] Error alerting configured
[] Abnormal traffic alerting configured
```

**Deployment strategy selection:**
```
[] Full deploy (simple bugfix, no-risk changes)
[] Canary Release (gradual traffic increase)
[] Blue-Green (instant switch, instant rollback)
[] Feature Flag (expose to specific user groups only)
```

If no rollback strategy exists, block deployment:

```
DEPLOYMENT BLOCKED

No rollback strategy has been prepared.
Deploying without an answer to "How do we revert if this fails?"
becomes a disaster when an incident occurs.

Minimum requirements:
1. Apply Feature Flag or Canary deployment
2. Define rollback trigger conditions (when to auto/manual rollback)
3. Assign rollback owner
```

### Canary Deployment Plan

```markdown
## Gradual Rollout Plan

| Phase | Traffic % | Observation Period | Pass Criteria |
|-------|-----------|-------------------|---------------|
| Phase 1 | 1% | 2 hours | Error rate < 0.5%, p99 < 2s |
| Phase 2 | 10% | 12 hours | Error rate < 0.5%, Kill Metric maintained |
| Phase 3 | 30% | 24 hours | Statistical significance achieved |
| Phase 4 | 100% | - | Full deployment |

Auto-rollback triggers:
- Error rate > 1% (5-minute window)
- p99 latency > 3000ms (10-minute window)
- Kill Metric degradation detected
```

## Step 10 — FUT (Feature Under Testing in production)

### A/B Test Design

```markdown
## A/B Test Design Document

**Hypothesis:** [Changing button color will improve conversion rate by X%]

**Group Setup:**
- Control (A): [Current state]
- Experiment (B): [Changes applied]

**Statistical Settings:**
- Confidence level: 95% (p < 0.05)
- Power: 80%
- Minimum detectable effect size: X%

**Required Sample Size:** N users (per group)
**Estimated Duration:** X days
→ Formula: (required sample) / (daily traffic x 0.5)

**Measurement Metrics:**
| Category | Metric | Priority |
|----------|--------|----------|
| Primary | North Star Metric | Highest |
| Secondary | Guardrail #1 | |
| Secondary | Guardrail #2 | |
| Guard | Kill Metric | Halt immediately if degraded |
```

### Without A/B Test Infrastructure

If A/B testing is not available, use this alternative path:

```
[] Internal dogfooding completed (team uses feature for X days)
[] Canary deployment metrics reviewed (error rate, latency, Kill Metric)
[] Manual QA sign-off from product owner
[] Monitoring dashboard confirms no regression

→ Proceed to launch decision based on canary data + qualitative feedback
```

### Result Interpretation Guide

When A/B test results are provided, interpret them using this frame:

**Statistical significance check:**
- Is p < 0.05?
- Is the sample size sufficient?
- Was the test period at least 1 week? (to eliminate day-of-week effects)

**Comprehensive metric assessment:**
- Did North Star improve?
- Did Kill Metric degrade?
- Any anomalous signals in Guardrails?

**Common interpretation pitfalls:**
- "Clicks increased but purchases decreased" → partial success ≠ success
- "Not statistically significant" → this is NOT evidence of no effect
- "Test period was short" → results cannot be trusted

## Steps 11 & 12 — FL / FNL (Feature Launch / Feature Not Launch)

### Launch Decision Criteria

**LAUNCH (Full deployment):**
- North Star statistically significantly improved (p < 0.05)
- Kill Metric maintained or improved
- No anomalies in Guardrails
- Sufficient sample size and test duration

**HOLD (On hold):**
- Statistical significance not reached (insufficient sample or short duration)
- Mixed results (some improved, some degraded)
- Action: Extend test or re-review design

**NOT LAUNCH (Discard):**
- No North Star improvement + Kill Metric degraded
- Statistically significantly negative results
- Action: Remove feature, clean up technical debt

When NOT LAUNCH is decided:

```
NOT LAUNCH DECISION

Even if a feature took a month to build, if the data says no, it must be removed.

Keeping a failed feature alive causes:
1. Code complexity increases, slowing down future development
2. Meaningless maintenance costs accumulate indefinitely
3. The team's judgment criteria become blurred

Removal action items:
[] Feature Flag OFF or code deletion
[] Related data cleanup plan
[] Document lessons learned → Read `references/retro.md` and proceed to Retro Agent
```

## Final Output Format

```markdown
## Launch Decision Report

**Feature:** [Name]
**Decision:** LAUNCH / HOLD / NOT LAUNCH

### A/B Test Results Summary
| Metric | Control | Experiment | Change Rate | Significance |
|--------|---------|------------|-------------|--------------|
| North Star | | | | |
| Kill Metric | | | | |
| Guardrail #1 | | | | |

### Decision Rationale
[Data-driven explanation]

### Next Actions
→ LAUNCH: Full deployment schedule + monitoring plan
→ HOLD: Additional test plan or redesign direction
→ NOT LAUNCH: Removal plan + Read `references/retro.md` for Retro Agent (Step 13)
```
