"""Results ledger: the only source of numbers allowed in a manuscript.

Every measured value is appended to a JSONL file with enough context to trace it
back to a run. Paper text may only quote numbers found here; anything else is
[RESULT REQUIRED].

In a notebook:
    from utils.ledger import log_result
    log_result("results/ledger.jsonl", experiment="xlmr_base", metric="macro_f1",
               value=0.8123, split="test", seed=42, notebook="03_baselines",
               config={"lr": 2e-5, "epochs": 4})

CLI:
    python ledger.py summary results/ledger.jsonl
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone


def log_result(path, experiment, metric, value, split="test", seed=None,
               notebook=None, config=None, note=None) -> dict:
    """Append one measurement. Returns the stored record."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a number")
    rec = {
        "id": None,
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "experiment": experiment,
        "metric": metric,
        "value": float(value),
        "split": split,
        "seed": seed,
        "notebook": notebook,
        "config": config,
        "note": note,
    }
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    rec["id"] = len(load(path)) + 1
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def load(path) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def summary(path) -> str:
    rows = load(path)
    if not rows:
        return "Ledger is empty."
    groups = defaultdict(list)
    for r in rows:
        groups[(r["experiment"], r["metric"], r["split"])].append(r["value"])
    lines = [f"{'experiment':<28}{'metric':<14}{'split':<8}{'n':>3}  {'mean':>8}  {'min':>8}  {'max':>8}"]
    for (exp, met, split), vals in sorted(groups.items()):
        mean = sum(vals) / len(vals)
        lines.append(f"{exp:<28}{met:<14}{split:<8}{len(vals):>3}  {mean:>8.4f}  {min(vals):>8.4f}  {max(vals):>8.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "summary":
        print(summary(sys.argv[2]))
    else:
        print(__doc__)
