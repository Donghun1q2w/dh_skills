---
name: autoresearch
description: >
  Autonomous experiment loop inspired by Karpathy's autoresearch.
  Iteratively modify code, run experiments, measure metrics, and keep/revert changes based on results.
  Use this skill when the user wants to: run autonomous code optimization experiments,
  hyperparameter tuning, performance benchmarking loops, algorithmic optimization,
  architecture search, or any iterative improve-measure-decide workflow.
  Also trigger when user mentions "autoresearch", "experiment loop", "auto-optimize",
  "autonomous tuning", "자율 실험", "자동 최적화", "하이퍼파라미터 탐색",
  or wants to let Claude run experiments overnight/unattended.
---

# Autoresearch: Autonomous Experiment Loop

A generalized autonomous experiment skill based on Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern.
Modify code, run it, measure metrics, and keep/revert based on results — automatically in a loop.

**All user-facing output (messages, strategy suggestions, status reports) must be in Korean.**

## Core Concept

The essence of this skill is simple:

```
LOOP:
  1. Apply an idea as a code change
  2. git commit
  3. Run the experiment (within time budget)
  4. Extract metrics
  5. If improved → keep, otherwise → revert
  6. Record results
  7. Repeat with next idea
```

This applies to **any code optimization with a measurable metric** — not just ML training, but also performance benchmarks, algorithm optimization, build configuration tuning, etc.

## Setup Phase

When the user wants to start an experiment, confirm and agree on the following:

### 1. Collect Experiment Definition

Confirm the following with the user (infer from conversation where possible, only ask what's missing):

| Field | Description | Example |
|-------|-------------|---------|
| **target_file** | File(s) to modify (1 recommended, max 3) | `train.py`, `config.yaml` |
| **run_command** | Command to run the experiment | `python train.py`, `dotnet run` |
| **metric_name** | Name of the metric to optimize | `val_bpb`, `latency_ms`, `accuracy` |
| **metric_direction** | `lower` (lower is better) or `higher` (higher is better) | `lower` |
| **metric_pattern** | Regex to extract metric from output | `^val_bpb:\s+(.+)` |
| **time_budget** | Time limit per experiment (seconds) | `300` (5 min) |
| **constraints** | Read-only files, memory limits, etc. | `prepare.py is read-only` |

### 2. Create Branch

```bash
git checkout -b autoresearch/<tag>
```

Suggest a date-based tag (e.g., `autoresearch/apr3`). Must not conflict with existing branches.

### 3. Initialize Results File

Create `results.tsv` at project root (tab-separated, keep git untracked):

```
commit	metric_value	status	description
```

### 4. Run Baseline

The first run must always establish a baseline without any code modifications.
This value becomes the comparison target for all subsequent experiments.

### 5. Save Experiment Config

Create `.autoresearch.json` at project root:

```json
{
  "tag": "apr3",
  "target_files": ["train.py"],
  "run_command": "python train.py",
  "metric_name": "val_bpb",
  "metric_direction": "lower",
  "metric_pattern": "^val_bpb:\\s+(.+)",
  "time_budget_seconds": 300,
  "timeout_seconds": 600,
  "constraints": ["prepare.py is read-only"],
  "baseline_value": null
}
```

## Experiment Loop

After setup is complete, enter the experiment loop.
Every step in the loop is mandatory. Modifying code without running it is not an experiment.
For detailed guides on idea generation and analysis, see `references/experiment-loop.md`.

### Mandatory Steps Per Experiment (Do Not Skip Any)

Every experiment must complete all 6 steps below, in order.
If any step is missing, the experiment is incomplete.

```
┌─ EXPERIMENT CYCLE (repeat) ──────────────────────────────┐
│                                                          │
│  STEP 1: Idea → Code Modification                        │
│    Modify the target_file.                               │
│                                                          │
│  STEP 2: Commit                                          │
│    git commit -m "experiment: <description>"             │
│                                                          │
│  STEP 3: Run ← NEVER skip this step                     │
│    <run_command> > run.log 2>&1                           │
│    Modifying code without running it is meaningless.     │
│    You must run the benchmark/training to measure the    │
│    metric.                                               │
│                                                          │
│  STEP 4: Extract Metric                                  │
│    grep -oP '<metric_pattern>' run.log                   │
│    If output is empty → treat as crash                   │
│                                                          │
│  STEP 5: Verdict (keep / discard / crash)                │
│    metric_direction=lower: new < best → keep             │
│    metric_direction=higher: new > best → keep            │
│    Otherwise → discard (git reset --hard HEAD~1)         │
│    crash → revert and move to next idea                  │
│                                                          │
│  STEP 6: Record in results.tsv ← NEVER skip this either │
│    If not recorded, the experiment effectively never     │
│    happened.                                             │
│    Format: commit\tmetric_value\tstatus\tdescription     │
│                                                          │
│  → Return to STEP 1 for next experiment                  │
└──────────────────────────────────────────────────────────┘
```

**Completion check**: After each experiment, verify a new row was added to results.tsv.
If no row was added, the experiment is incomplete. Go back and perform the missing step.

### STEP 3 Detail: Execution

This is the core of the experiment. Modifying code without running it is meaningless.
You must execute run_command and extract the metric from its output.

```bash
# Redirect stdout to log (prevent context pollution)
<run_command> > run.log 2>&1

# Extract metric
grep '<metric_pattern>' run.log
```

Timeout handling (kill if execution exceeds timeout_seconds):
```bash
# Linux/Mac
timeout <timeout_seconds> <run_command> > run.log 2>&1

# Windows — use Python subprocess
python -c "import subprocess; subprocess.run('<run_command>'.split(), stdout=open('run.log','w'), stderr=subprocess.STDOUT, timeout=<timeout_seconds>)"
```

### STEP 5 Detail: Verdict Criteria

- **metric_direction=lower**: new value < previous best → keep
- **metric_direction=higher**: new value > previous best → keep
- Equal or worse → discard (git reset --hard HEAD~1)
- **Simplification criterion**: If code becomes clearly simpler while metric stays equivalent → keep

### STEP 6 Detail: Recording Results

Record in results.tsv with tab separation (not commas):

```
commit	metric_value	status	description
a1b2c3d	0.997900	keep	baseline
b2c3d4e	0.993200	keep	increase learning rate to 0.04
c3d4e5f	1.005000	discard	switch to GeLU activation
d4e5f6g	0.000000	crash	double model width (OOM)
```

Status values: `keep`, `discard`, `crash`.
For crashes, metric_value is `0.000000`.

## Autonomous Mode vs Interactive Mode

### Autonomous Mode

Runs an infinite loop without user intervention, like the original autoresearch.
Activate when the user says things like "run autonomously", "experiment overnight", "keep going until I stop you".

**Core rule: Never stop.**
- Never ask "should I continue?" — that is forbidden
- If ideas run out, think harder:
  - Combine near-misses from previous experiments
  - Try more radical structural changes
  - Reverse direction (decrease what was increased)
- Continue until the user manually interrupts

### Interactive Mode (Default)

Report results to the user after each experiment and discuss next direction.
Default to interactive mode unless the user explicitly requests autonomous mode.

## Idea Generation Strategy

Cycle through these strategies to avoid running out of ideas:

1. **Hyperparameter grid**: Systematically explore key parameters (learning rate, batch size, regularization strength)
2. **Structural changes**: Modify layer count, dimensions, activation functions, normalization
3. **Combination experiments**: Combine previously kept changes
4. **Reverse experiments**: Try counterintuitive changes (e.g., 10x learning rate)
5. **Simplification**: Remove code/structure and check if performance holds
6. **Literature-based**: Borrow ideas from papers/techniques referenced in the code

## Analysis

When experiments accumulate (10+), analyze results:

```bash
# Load and analyze results.tsv
python -c "
import pandas as pd
df = pd.read_csv('results.tsv', sep='\t')
print('=== 실험 요약 ===')
print(f'전체: {len(df)}개 실험')
print(f'Keep: {len(df[df.status==\"keep\"])}')
print(f'Discard: {len(df[df.status==\"discard\"])}')
print(f'Crash: {len(df[df.status==\"crash\"])}')
best = df[df.status=='keep'].sort_values('metric_value')
print(f'최고: {best.iloc[0].metric_value} ({best.iloc[0].description})')
print(f'개선: {df.iloc[0].metric_value} -> {best.iloc[0].metric_value}')
"
```

For detailed analysis methods, see `references/analysis.md`.

## Reference Files

- `references/experiment-loop.md` — Detailed experiment loop procedures, error handling, Windows-compatible commands
- `references/program-template.md` — Domain-specific experiment program templates (ML, performance optimization, build tuning)
- `references/analysis.md` — Experiment result analysis and visualization methods
