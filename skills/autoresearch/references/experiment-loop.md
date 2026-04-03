# Experiment Loop Detailed Guide

This document provides guides for idea generation, error handling, and analysis for the autonomous experiment loop.
The mandatory 6 steps per experiment are defined in SKILL.md. You must follow all 6 steps.

This document is a supplementary guide for performing each step more effectively.

## Prerequisites

- `.autoresearch.json` config file exists
- Checked out to experiment branch (`autoresearch/<tag>`)
- `results.tsv` header has been created
- Baseline run completed and `baseline_value` recorded

## Pre-Experiment Status Check

```bash
git log --oneline -5
git diff --stat
cat results.tsv | tail -5
```

Identify the current best metric value and recent experiment history.
Use the pattern from previous experiments to plan the next idea.

## Idea Generation Guide

Modify the target_file. Ideally, change only one variable at a time.
Changing multiple variables simultaneously makes it impossible to determine which change was effective.

Considerations when making changes:
- Reflect learnings from previous experiment results
- Balance between too conservative and too aggressive
- Weigh code complexity vs performance improvement tradeoff

## Git Commit Guide

```bash
git add <target_files>
git commit -m "experiment: <change summary>"
```

The commit message should match the description in results.tsv.
Committing is necessary for clean reverts.

**Note**: Do not commit results.tsv. Keep it git untracked.

## Execution Command Guide

Always redirect output to a log file. Stdout must not pollute the context.

**Linux/Mac:**
```bash
timeout <timeout_seconds> <run_command> > run.log 2>&1
EXIT_CODE=$?
```

**Windows (Git Bash):**
```bash
# Use Python wrapper since Windows timeout command is different
python -c "
import subprocess, sys
try:
    result = subprocess.run(
        '<run_command>'.split(),
        stdout=open('run.log', 'w'),
        stderr=subprocess.STDOUT,
        timeout=<timeout_seconds>
    )
    sys.exit(result.returncode)
except subprocess.TimeoutExpired:
    print('TIMEOUT')
    sys.exit(124)
"
EXIT_CODE=$?
```

**Alternative — use Bash tool's run_in_background:**
For long-running experiments, use the Bash tool's `run_in_background` option and `timeout` parameter.

## Crash Handling Guide

If grep returns empty when extracting metrics, treat it as a crash.

```bash
# Check error log
tail -50 run.log
```

Crash cause classification:
1. **Trivial bugs** (typo, missing import, syntax error): Fix immediately and re-run
2. **Resource exhaustion** (OOM, disk full): Revert and retry with more conservative settings
3. **Fundamental issues** (algorithm itself is flawed): Skip and move to next idea

When re-running after a fix, use `git commit --amend` to update the commit.
If it still fails after 3+ retries, give up and record as crash.

## Verdict (Keep / Discard) Guide

Check `metric_direction` from `.autoresearch.json`:

```
if metric_direction == "lower":
    improved = new_value < best_value
elif metric_direction == "higher":
    improved = new_value > best_value
```

**Simplification criterion:**
Even if the metric is equal or marginally worse (within -0.1%),
if the code is clearly simpler, it can be judged as keep.
This improves long-term experiment efficiency.

**Keep:**
```bash
# Branch naturally advances. No additional action needed.
echo "KEEP: metric improved from $BEST to $NEW"
```

Update best_value.

**Discard:**
```bash
git reset --hard HEAD~1
echo "DISCARD: metric $NEW did not improve over $BEST"
```

**Crash:**
```bash
git reset --hard HEAD~1
echo "CRASH: experiment failed"
```

## Result Recording

Append one line to results.tsv:

```bash
# Tab-separated (not commas!)
COMMIT=$(git rev-parse --short HEAD)
echo -e "${COMMIT}\t${METRIC_VALUE}\t${STATUS}\t${DESCRIPTION}" >> results.tsv
```

For crashes, metric_value is `0.000000`.

## Idea Generation Strategies

Cycle through these strategies to avoid running out of ideas:

### Level 1: Parameter Exploration (Safest)
- Double or halve existing constants/parameters
- Learning rate, batch size, regularization strength, etc.
- Try both directions (increase/decrease)

### Level 2: Structural Changes (Medium Risk)
- Add/remove layers
- Swap activation functions
- Change normalization methods
- Modify scheduling strategies

### Level 3: Combination Experiments (Combine kept changes)
- Simultaneously apply changes that were individually effective
- Check for synergy effects

### Level 4: Reverse Experiments (Counterintuitive attempts)
- Try things that seem like "this won't work"
- Often yields unexpected discoveries

### Level 5: Simplification (Remove code)
- Remove unnecessary parts and check if metric holds
- Equal performance with simpler code is always a win

### Level 6: Literature/Code-Based Ideas
- Borrow ideas from papers/libraries referenced in the code
- Apply known solutions to similar problems

## Autonomous Mode Behavior Rules

In autonomous mode, strictly follow these rules:

1. **Never stop** — Continue the loop until the user manually interrupts
2. **Never ask questions** — "Should I continue?", "What should I try next?" are forbidden
3. **Decide autonomously** — Determine the next experiment direction on your own
4. **Record everything** — Log every experiment in results.tsv without exception
5. **Don't fear failure** — Many discards/crashes are fine. They're a natural part of exploration

## Suspend and Resume

### On Suspend
```bash
# Print current state summary
echo "=== Autoresearch 세션 요약 ==="
echo "브랜치: $(git branch --show-current)"
echo "전체 실험: $(wc -l < results.tsv)"
echo "최고 메트릭: $(sort -t$'\t' -k2 -n results.tsv | head -2 | tail -1)"
```

### On Resume
1. Read `.autoresearch.json`
2. Check current best value from `results.tsv`
3. Checkout to experiment branch
4. Re-enter the loop
