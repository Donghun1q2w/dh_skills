# Phase 2: Risk Agent

Relentlessly asks "Will this blow up if we proceed as-is?"

## Trigger Conditions

- When planning is finalized and before design/development begins
- When a pre-kickoff review is needed
- When questions like "Can we just start building this right away?" arise

## Step 4 — FBD (Feature-Based Design review)

### UX Risk Checklist

Review each item below and assess the risk level for each.

```
[] Are there points where users could get confused on this screen?
   → Catalog UI elements that could trigger "What is this button?" moments

[] Have error state UIs been designed?
   → Check for loading / failure / empty state screens

[] Are there mobile/PC responsive edge cases?

[] Are there accessibility (a11y) requirements?
   → Screen reader, color contrast, keyboard navigation

[] Is this safe to ship without usability testing?
   → If MAU exceeds 100K or involves payment, testing is strongly recommended
```

## Step 5 — RFE (Ready For Engineering)

### Technical Risk Checklist

**Network / Stability:**
```
[] Is the handling for network disconnection defined?
[] Are there external API calls that need timeout configuration?
[] Is there a plan for traffic spikes (sudden concurrent access surge)?
[] Data consistency — can duplicate requests/payments occur?
```

**Performance:**
```
[] Will this feature affect app initial load time?
[] Are additional DB queries needed? Any N+1 problem potential?
[] Is there data that requires cache invalidation?
```

**Data:**
```
[] Is existing data migration required?
[] Is a schema change needed? → What happens on rollback?
[] Is there a data backup/recovery plan?
```

### Business / Legal Risk Checklist

**Privacy / Security:**
```
[] Does this involve new personal data collection?
[] Does the privacy policy need updating?
[] Does this handle sensitive data (payment info, auth tokens, etc.)?
[] Are there vulnerabilities from an OWASP Top 10 perspective?
```

**Business:**
```
[] Are refund/cancellation cases reflected in the plan?
[] Are there scenarios that could increase CS inquiries?
[] Does this feature conflict with existing policies/terms?
[] If integrating with partners/external services, has the SLA been verified?
```

### Rollback Strategy Check

```
[] Can this feature be immediately reverted after deployment?
[] Is Feature Flag or gradual rollout applicable?
[] If DB migration was done, what about data consistency on rollback?
```

If no rollback strategy exists → classify as CRITICAL risk.

## Risk Level Criteria

| Level | Description |
|-------|-------------|
| **LOW** | A few edge cases, quickly fixable after launch |
| **MEDIUM** | Additional design needed, must be resolved before kickoff |
| **HIGH** | Structural issue requiring return to the planning stage |
| **CRITICAL** | Cannot start development. Legal/security/no-rollback issues exist |

If even one CRITICAL risk is found:

```
CRITICAL RISK DETECTED

[Risk description]

If development starts in this state, the cost of fixing after launch
is at least 50x the current cost.
You must resolve this before proceeding to kickoff.

Starting development is not recommended until this is resolved.
```

## Kickoff Must-Ask Questions

Based on the risk check results, generate a list of questions that developers/QA must verify at the kickoff meeting.

Output format:

```markdown
## Kickoff Checklist (Must confirm before developers say "yes")

### Required (Cannot start development without answers)
1. [Question] — [Reason]
2. [Question] — [Reason]

### Recommended (Knowing these upfront saves time later)
3. [Question]
4. [Question]

### Can be decided during development
5. [Question]
```

## Final Output Format

```markdown
## Risk Analysis Report

**Feature:** [Name]
**Overall Risk Level:** LOW / MEDIUM / HIGH / CRITICAL

### UX Risks
| Item | Level | Details |
|------|-------|---------|

### Technical Risks
| Item | Level | Details |
|------|-------|---------|

### Business / Legal Risks
| Item | Level | Details |
|------|-------|---------|

### Rollback Strategy
[Ready / Incomplete / Not possible]

### Kickoff Checklist
[As formatted above]

### Next Steps
→ LOW/MEDIUM: Read `references/build.md` and proceed to Build Agent (Step 6)
→ HIGH: Re-review after [items to resolve]
→ CRITICAL: Cannot start development. Return to planning stage (`references/planning.md`)
```
