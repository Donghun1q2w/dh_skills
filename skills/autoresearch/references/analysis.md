# Experiment Result Analysis

When experiments accumulate, analyze results to derive insights and determine next experiment direction.

## Basic Analysis

### results.tsv Summary Statistics

```python
#!/usr/bin/env python3
"""Autoresearch results analyzer."""
import sys

def analyze_results(filepath="results.tsv", direction="lower"):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) >= 4:
            rows.append({
                "commit": parts[0],
                "metric": float(parts[1]) if parts[1] != "0.000000" else None,
                "status": parts[2],
                "description": parts[3]
            })

    total = len(rows)
    kept = [r for r in rows if r["status"] == "keep"]
    discarded = [r for r in rows if r["status"] == "discard"]
    crashed = [r for r in rows if r["status"] == "crash"]

    print(f"=== 실험 요약 ===")
    print(f"전체 실험: {total}개")
    print(f"  Keep:    {len(kept)}개 ({100*len(kept)/total:.0f}%)")
    print(f"  Discard: {len(discarded)}개 ({100*len(discarded)/total:.0f}%)")
    print(f"  Crash:   {len(crashed)}개 ({100*len(crashed)/total:.0f}%)")

    if kept:
        metrics = [r["metric"] for r in kept if r["metric"] is not None]
        if direction == "lower":
            best = min(metrics)
            best_row = [r for r in kept if r["metric"] == best][0]
        else:
            best = max(metrics)
            best_row = [r for r in kept if r["metric"] == best][0]

        baseline = kept[0]["metric"] if kept else None
        print(f"\n=== 성능 ===")
        print(f"베이스라인: {baseline}")
        print(f"최고:       {best} ({best_row['description']})")
        if baseline:
            improvement = abs(best - baseline)
            pct = 100 * improvement / abs(baseline) if baseline != 0 else 0
            print(f"개선:       {improvement:.6f} ({pct:.2f}%)")

    # Recent 10 experiment trend
    print(f"\n=== 최근 실험 (최대 10개) ===")
    for r in rows[-10:]:
        status_icon = {"keep": "+", "discard": "-", "crash": "X"}[r["status"]]
        metric_str = f"{r['metric']:.6f}" if r["metric"] else "CRASH"
        print(f"  [{status_icon}] {r['commit']} {metric_str} {r['description']}")

if __name__ == "__main__":
    direction = sys.argv[1] if len(sys.argv) > 1 else "lower"
    analyze_results(direction=direction)
```

Save this script as `analyze_results.py` and run:
```bash
PYTHONIOENCODING=utf-8 python analyze_results.py <lower|higher>
```

## Advanced Analysis

### Experiment Efficiency Analysis

When 20+ experiments have accumulated, check the following:

1. **Keep rate trend**: It's natural for the keep rate to decline over time (easy improvements are found first)
2. **Consecutive discards**: If 10+ consecutive discards, a strategy change is needed
3. **Crash patterns**: If a specific type of change repeatedly crashes, avoid that direction

### Success Rate by Change Type

Classify descriptions in results.tsv to identify which types of changes are effective:

```python
# Change type classification (keyword-based)
categories = {
    "lr/learning_rate": ["lr", "learning rate"],
    "architecture": ["layer", "depth", "width", "head", "attention"],
    "optimizer": ["adam", "sgd", "momentum", "weight decay"],
    "batch_size": ["batch"],
    "regularization": ["dropout", "norm", "regulariz"],
    "simplification": ["remove", "delete", "simplif"],
}
```

### Progress Visualization

Generate an experiment progress chart with matplotlib:

```python
import matplotlib.pyplot as plt

# Extract from results.tsv
# x: experiment number (all), y: metric_value
# keep = blue dot, discard = gray dot, crash = red X
# running best as green line

fig, ax = plt.subplots(figsize=(12, 5))
for i, row in enumerate(rows):
    if row["status"] == "keep":
        ax.scatter(i, row["metric"], c="blue", s=30, zorder=3)
    elif row["status"] == "discard":
        ax.scatter(i, row["metric"], c="gray", s=15, alpha=0.5)
    elif row["status"] == "crash":
        ax.scatter(i, 0, c="red", marker="x", s=30)

# Running best line
best_so_far = []
current_best = rows[0]["metric"]
for r in rows:
    if r["metric"] and r["status"] == "keep":
        current_best = min(current_best, r["metric"])  # or max for higher
    best_so_far.append(current_best)
ax.plot(range(len(rows)), best_so_far, c="green", linewidth=2, label="Best so far")

ax.set_xlabel("실험 번호")
ax.set_ylabel("메트릭 값")
ax.set_title("Autoresearch 진행 현황")
ax.legend()
plt.tight_layout()
plt.savefig("progress.png", dpi=150)
print("차트 저장 완료: progress.png")
```

## Cross-Session Comparison

To compare experiments across different tags:

```bash
# Compare best per branch
for branch in $(git branch --list 'autoresearch/*'); do
    echo "$branch: $(git log $branch --oneline -1)"
done
```

## Deciding Next Experiment Direction

Checklist for determining next experiment direction based on analysis:

1. **What do recently kept changes have in common?** → Explore that direction further
2. **Which change gave the largest improvement?** → Try changes of similar magnitude
3. **What areas haven't been tried yet?** → Ensure exploration diversity
4. **Which areas have many consecutive discards?** → Temporarily avoid and try other directions
5. **What patterns cause frequent crashes?** → Fix root cause or avoid
