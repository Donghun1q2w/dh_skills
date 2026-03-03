# Phase 3: Build Agent

Realizes the principle "Implementation is negotiation, not just coding."

## Trigger Conditions

- When development has started or is in progress
- When there are conflicting opinions in API design/negotiation
- When QA scenario creation is needed
- When questions like "Should I implement it this way?" arise

## Step 6 — FUE (Feature Under Engineering)

### API Conflict Detection

When differences arise between frontend and backend perspectives, analyze both sides.

Analysis frame:

```
Frontend request: [What is desired]
Backend reality: [What is actually needed]
- Whether additional DB joins are required
- Whether cache structure changes are needed
- Expected latency changes

Conflict level:
- Simple addition (resolvable within 30 minutes)
- Design change required (1-2 days)
- Architecture review required (1+ week)
```

When the conflict reaches architecture level:

```
WARNING: This request is not a simple field addition.

Expected impact:
- DB: [Changes]
- Cache: [Changes]
- Latency: [Predicted change]

Alternative options:
A) [Original direction + compromise]
B) [API separation approach]
C) [Short-term vs long-term solution]
```

### Performance Impact Check

Always compare before and after adding a feature:

```
[] New API call added? → Design timeout, error handling
[] DB query added/changed? → N+1, index, slow query potential
[] Bundle size increased? → Impact on app initial load time
[] Predicted page latency change: +Xms → Convert to MAU x bounce rate
```

When latency increases by 200ms or more:

```
PERFORMANCE WARNING

Predicted latency increase: +Xms
Estimated bounce rate increase at 1M MAU: approx. X%

Releasing the feature without performance improvements is not recommended.
Please review the following options:
1. Query optimization
2. Introduce caching
3. Reduce feature scope
```

## Step 7 — RFQ (Ready For QA)

### Definition of Done Checklist

Completion criteria the developer must verify before QA begins:

**Code quality:**
- [ ] Code review completed
- [ ] Unit tests written (coverage X% or above)
- [ ] Lint/static analysis passed

**Feature completeness:**
- [ ] Happy path verified
- [ ] Error state UI exists
- [ ] Loading state UI exists
- [ ] Empty state UI exists

**Integration:**
- [ ] Deployed to staging environment
- [ ] API documentation updated
- [ ] Feature flag applied (if needed)

## Step 8 — FUQ (Feature Under QA)

When a feature description is received, automatically generate test scenarios in the following categories.

### Scenario Generation Frame

```markdown
## QA Scenarios: [Feature Name]

### Happy Path (Normal Flow)
| # | Scenario | Input | Expected Result |
|---|----------|-------|-----------------|
| 1 | | | |

### Error Cases
| # | Scenario | Condition | Expected Behavior |
|---|----------|-----------|-------------------|
| 1 | Request during network disconnection | Offline state | Error message displayed, no data loss |
| 2 | Request during session expiry | Token expired | Redirect to login page |
| 3 | Server 500 error | Server error | User-friendly error message |

### Edge Cases
| # | Scenario | Condition | Expected Behavior |
|---|----------|-----------|-------------------|
| 1 | Concurrent duplicate requests | Button spam | Duplicate processing prevention |
| 2 | Max/min input values | Boundary values | Normal processing or clear guidance |
| 3 | Special characters/XSS | Malicious input | Filtering applied |

### Performance Tests
| # | Scenario | Condition | Threshold |
|---|----------|-----------|-----------|
| 1 | Normal request response time | Normal traffic | p95 < 1000ms |
| 2 | Concurrent access load | 100 simultaneous users | Error rate < 1% |
```

Add specialized scenarios based on the feature's domain:

- **Payment** → Duplicate payment, network disconnection during cancellation, PG timeout
- **Authentication** → Token theft, session sharing, concurrent login
- **File upload** → Large files, malicious files, cancellation during upload
- **Search** → Empty query, special characters, no results state

## Final Output Format

```markdown
## Build Stage Report

**Feature:** [Name]
**Stage:** In implementation / QA preparation complete / QA in progress

### API Negotiation Result
[Conflict points and agreed direction]

### Performance Impact
- Expected latency change: [+/-Xms]
- DB query additions: [Yes/No]
- Recommendations: [If any]

### Definition of Done
[Checklist]

### QA Scenarios
[Total X — Happy path X, Error X, Edge case X, Performance X]

### Next Steps
→ QA passed: Read `references/launch.md` and proceed to Launch Agent (Step 9)
→ Issues found: [List of required fixes]
```
