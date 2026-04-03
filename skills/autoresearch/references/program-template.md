# Experiment Program Templates

Provides `.autoresearch.json` configurations and experiment strategies per domain.
Use the template matching the user's domain to set up the experiment.

## ML Training Optimization (Original autoresearch pattern)

The original Karpathy autoresearch pattern. Optimize PyTorch/TensorFlow training scripts.

```json
{
  "tag": "ml-opt",
  "target_files": ["train.py"],
  "run_command": "python train.py",
  "metric_name": "val_bpb",
  "metric_direction": "lower",
  "metric_pattern": "^val_bpb:\\s+([\\d.]+)",
  "time_budget_seconds": 300,
  "timeout_seconds": 600,
  "constraints": ["prepare.py is read-only", "evaluate function is read-only"]
}
```

**Exploration areas:**
- Model architecture: depth, width, head_dim, attention pattern
- Optimizer: learning rate, beta, weight_decay, scheduler
- Training strategy: batch_size, gradient accumulation, warmup/cooldown
- Activation functions: ReLU, GeLU, SiLU, ReLU^2
- Normalization: LayerNorm, RMSNorm, position, strength

**Metric output example (print at end of train.py):**
```python
print(f"val_bpb: {val_bpb:.6f}")
print(f"peak_vram_mb: {peak_vram:.1f}")
print(f"training_seconds: {train_time:.1f}")
```

## Python Script Performance Optimization

Optimize algorithm execution time or memory usage.

```json
{
  "tag": "perf-opt",
  "target_files": ["solution.py"],
  "run_command": "python benchmark.py",
  "metric_name": "avg_time_ms",
  "metric_direction": "lower",
  "metric_pattern": "^avg_time_ms:\\s+([\\d.]+)",
  "time_budget_seconds": 60,
  "timeout_seconds": 120,
  "constraints": ["benchmark.py is read-only", "all tests must pass"]
}
```

**Exploration areas:**
- Data structures: list vs set vs dict, deque, heapq
- Algorithms: sorting methods, search strategies, caching
- Python optimizations: comprehension, generator, numpy vectorization
- Parallelism: multiprocessing, concurrent.futures, asyncio

**Benchmark script pattern (benchmark.py):**
```python
import time
from solution import solve

test_cases = load_test_cases()
times = []
for tc in test_cases:
    start = time.perf_counter()
    result = solve(tc["input"])
    elapsed = (time.perf_counter() - start) * 1000
    times.append(elapsed)
    assert result == tc["expected"], f"Wrong answer for {tc['name']}"

avg = sum(times) / len(times)
print(f"avg_time_ms: {avg:.3f}")
print(f"max_time_ms: {max(times):.3f}")
print(f"all_tests_passed: True")
```

## C#/.NET Build and Performance Optimization

Optimize .NET project build time, runtime performance, and memory usage.

```json
{
  "tag": "dotnet-opt",
  "target_files": ["Program.cs"],
  "run_command": "dotnet run -c Release --project MyApp",
  "metric_name": "throughput_ops",
  "metric_direction": "higher",
  "metric_pattern": "^throughput_ops:\\s+([\\d.]+)",
  "time_budget_seconds": 120,
  "timeout_seconds": 300,
  "constraints": ["preserve interface signatures", "existing tests must pass"]
}
```

**Exploration areas:**
- Collections: List vs Array vs Span, Dictionary capacity
- Memory: stackalloc, ArrayPool, object pooling
- Async: async/await patterns, ValueTask, Channel
- LINQ optimization: convert to for loops, materialization timing
- Serialization: System.Text.Json options, source generator

## Configuration/Hyperparameter Tuning (General)

Tune parameters in configuration files (JSON, YAML, INI, etc.) rather than the code itself.

```json
{
  "tag": "config-tune",
  "target_files": ["config.yaml"],
  "run_command": "python run_experiment.py --config config.yaml",
  "metric_name": "score",
  "metric_direction": "higher",
  "metric_pattern": "^score:\\s+([\\d.]+)",
  "time_budget_seconds": 180,
  "timeout_seconds": 360,
  "constraints": ["run_experiment.py is read-only"]
}
```

**Exploration strategies:**
- Grid search: Systematically explore each parameter
- Binary search: Narrow down the optimal range
- Combination search: Change interacting parameters together

## Custom Domain

If none of the above templates apply, ask the user:

1. **Is there a measurable metric?** → If yes, autoresearch can be applied
2. **Can the metric be output to stdout?** → If not, write a wrapper script
3. **Is the execution deterministic?** → If not, run multiple times and use the average

### Metric Output Wrapper Guide

When an existing program doesn't output metrics in a standard format,
write a wrapper script to: execute → parse results → output in standard format.

```python
#!/usr/bin/env python3
"""Autoresearch metric wrapper."""
import subprocess
import re
import sys

result = subprocess.run(
    ["python", "my_program.py"],
    capture_output=True, text=True, timeout=300
)

# Extract metric from output (modify per domain)
match = re.search(r"accuracy: ([\d.]+)%", result.stdout)
if match:
    print(f"metric_value: {match.group(1)}")
else:
    print("metric_value: 0.0")
    print("status: crash")
    print(result.stderr[-500:], file=sys.stderr)
    sys.exit(1)
```
