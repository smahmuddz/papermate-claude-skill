"""Scaffold a Colab-ready research project.

    python scaffold_project.py my-project --out ./projects [--task "Bangla sentiment"]

Creates:
    <out>/<name>/
      PROJECT.md
      notebooks/01_setup.ipynb ... 08_results.ipynb
      utils/ledger.py, utils/stats_tests.py
      data/  results/  paper/

Each notebook opens with a markdown cell listing objectives, libraries, expected
outputs, checkpoints, and debugging guidance, followed by code cells with TODOs
for Claude (or the user) to fill in for the specific task.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"

SETUP_CELL = '''# --- Colab setup: Drive, paths, seeds, utils ---
import os, sys, random
import numpy as np
try:
    from google.colab import drive
    drive.mount("/content/drive")
    ROOT = "/content/drive/MyDrive/{name}"
except ImportError:          # running locally
    ROOT = os.path.abspath("..")
for sub in ("data", "results", "checkpoints", "utils"):
    os.makedirs(f"{{ROOT}}/{{sub}}", exist_ok=True)
sys.path.insert(0, f"{{ROOT}}/utils")
LEDGER = f"{{ROOT}}/results/ledger.jsonl"
SEED = 42
random.seed(SEED); np.random.seed(SEED)
try:
    import torch; torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
except ImportError:
    pass
from ledger import log_result            # every reported number goes through this
'''

NOTEBOOKS = [
    {
        "file": "01_setup.ipynb",
        "title": "01 Setup and environment",
        "objectives": ["Pin the environment and seeds", "Record GPU and library versions", "Smoke-test that the GPU is visible"],
        "libs": ["transformers", "datasets", "accelerate", "peft (if LoRA)", "scikit-learn", "scipy"],
        "outputs": ["Printed GPU name and VRAM", "environment.txt saved to results/"],
        "checkpoints": ["Re-running the notebook after a runtime reset restores everything from Drive"],
        "debug": ["No GPU: Runtime > Change runtime type", "Version conflicts: restart runtime after pip install"],
        "code": [
            "!pip -q install transformers datasets accelerate scikit-learn scipy  # add peft/bitsandbytes if needed",
            "import subprocess\nprint(subprocess.run(['nvidia-smi'], capture_output=True, text=True).stdout)\n"
            "!pip freeze > {ROOT}/results/environment.txt  # TODO: record exact versions for the paper",
        ],
    },
    {
        "file": "02_data_preparation.ipynb",
        "title": "02 Data preparation",
        "objectives": ["Load the dataset from its official source", "Clean, deduplicate, and check leakage", "Create fixed train/val/test splits and hash them"],
        "libs": ["datasets", "pandas", "hashlib"],
        "outputs": ["Split sizes and class distribution table", "Duplicate/leakage counts", "Split files + SHA-256 hashes in data/"],
        "checkpoints": ["Test split never used for tuning", "Split hashes logged in PROJECT.md"],
        "debug": ["Label mismatch: print a few raw rows per class", "Encoding errors: set encoding='utf-8' explicitly"],
        "code": [
            "# TODO: load dataset (record source URL, version, license)",
            "# TODO: dedup exact and near-duplicates across splits; count removed",
            "# TODO: save splits to {ROOT}/data and print SHA-256 of each file",
        ],
    },
    {
        "file": "03_baselines.ipynb",
        "title": "03 Baselines",
        "objectives": ["Train/evaluate every baseline with the same tuning budget", "Run >= 3 seeds", "Save per-item predictions for significance tests"],
        "libs": ["scikit-learn", "torch", "transformers"],
        "outputs": ["Per-baseline mean +/- std over seeds", "predictions_<system>_<seed>.npy in results/"],
        "checkpoints": ["Majority-class and TF-IDF baselines finish before any neural run", "Each run logged via log_result"],
        "debug": ["OOM: lower batch size / max_length, enable fp16 and gradient checkpointing", "Disconnect: resume from last checkpoint in Drive"],
        "code": [
            "# TODO: majority-class + TF-IDF/SVM baseline",
            "# TODO: pretrained encoder baselines (mBERT / XLM-R / language-specific)",
            "# for each seed and system:\n#   log_result(LEDGER, experiment=name, metric='macro_f1', value=score, split='test', seed=seed, notebook='03_baselines', config=cfg)",
        ],
    },
    {
        "file": "04_proposed_method.ipynb",
        "title": "04 Proposed method",
        "objectives": ["Implement the proposed method exactly as specified in the experiment plan", "Use the same data, seeds, and tuning budget as baselines", "Save per-item predictions"],
        "libs": ["torch", "transformers", "peft (if used)"],
        "outputs": ["Test metrics per seed", "Trainable parameter count, runtime, peak VRAM"],
        "checkpoints": ["50-step smoke test passes before full training", "Hyperparameters tuned on validation only"],
        "debug": ["Loss NaN: lower LR, check fp16 overflow, inspect a batch", "No improvement: verify labels/tokenization before blaming the method"],
        "code": [
            "# TODO: implement proposed method",
            "# TODO: smoke test (50 steps), print torch.cuda.max_memory_allocated()",
            "# TODO: full run over seeds; log_result for every metric",
        ],
    },
    {
        "file": "05_ablation.ipynb",
        "title": "05 Ablation study",
        "objectives": ["Run every variant in ablation_plan.md", "Change exactly one component per variant", "Compare against the full model on identical seeds"],
        "libs": ["same as 04"],
        "outputs": ["Ablation table: variant, mean +/- std, diff vs full with CI"],
        "checkpoints": ["Variant list matches ablation_plan.md", "Each variant logged with experiment name 'abl_<id>'"],
        "debug": ["Variants look identical: check the component is truly disabled", "Unexpected gain: check for leakage or extra capacity"],
        "code": [
            "# TODO: loop over variants A1..An",
            "# TODO: log_result(LEDGER, experiment=f'abl_{vid}', ...)",
        ],
    },
    {
        "file": "06_error_analysis.ipynb",
        "title": "06 Error analysis",
        "objectives": ["Sample errors stratified by class/length/domain", "Apply the written error taxonomy", "Compare proposed vs strongest baseline errors"],
        "libs": ["pandas", "numpy"],
        "outputs": ["Confusion matrices", "Error taxonomy counts", "Example table for the paper"],
        "checkpoints": ["Taxonomy defined before labeling", "Second annotator on a subset, kappa computed"],
        "debug": ["Too few errors: increase sample or analyze per-class", "Ambiguous labels: document and report"],
        "code": [
            "# TODO: load saved predictions from results/",
            "# TODO: sample errors, label with taxonomy, count categories",
        ],
    },
    {
        "file": "07_statistics.ipynb",
        "title": "07 Statistical testing",
        "objectives": ["Run the pre-registered primary comparison", "Report CI and effect sizes", "Correct for multiple comparisons (Holm)"],
        "libs": ["numpy", "scipy", "utils/stats_tests.py"],
        "outputs": ["Table of differences with 95% CI and p-values", "Seed-level summaries"],
        "checkpoints": ["Tests and family of comparisons fixed in experiment_plan.md before looking at results"],
        "debug": ["Mismatched lengths: ensure predictions align with the same test items", "Wilcoxon floor with few seeds: report effect size"],
        "code": [
            "from stats_tests import paired_bootstrap, mcnemar, summarize_seeds, compare_seeds, holm, macro_f1",
            "# TODO: res = paired_bootstrap(y_true, pred_proposed, pred_baseline, metric=macro_f1)\n# log_result(LEDGER, 'proposed_vs_xlmr', 'macro_f1_diff', res['diff'], note=str(res))",
        ],
    },
    {
        "file": "08_results.ipynb",
        "title": "08 Results and figures",
        "objectives": ["Build final tables and figures from the ledger only", "Export LaTeX/markdown tables", "Print ledger summary for the paper"],
        "libs": ["pandas", "matplotlib"],
        "outputs": ["results_table.md / .tex", "figures/*.png", "ledger summary"],
        "checkpoints": ["Every number in a table exists in ledger.jsonl", "Run lint_manuscript.py on the draft"],
        "debug": ["Missing numbers: rerun the relevant notebook and log_result, never type values by hand"],
        "code": [
            "from ledger import summary\nprint(summary(LEDGER))",
            "# TODO: build tables/figures from ledger records",
        ],
    },
]


def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_cell(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(keepends=True)}


def bullets(items):
    return "\n".join(f"- {i}" for i in items)


def build(nb, name, task):
    header = (
        f"# {nb['title']}\n\n"
        f"**Project:** {name}" + (f" | **Task:** {task}" if task else "") + "\n\n"
        f"## Objectives\n{bullets(nb['objectives'])}\n\n"
        f"## Required libraries\n{bullets(nb['libs'])}\n\n"
        f"## Expected outputs\n{bullets(nb['outputs'])}\n\n"
        f"## Checkpoints\n{bullets(nb['checkpoints'])}\n\n"
        f"## Debugging guidance\n{bullets(nb['debug'])}\n"
    )
    cells = [md_cell(header), code_cell(SETUP_CELL.format(name=name))]
    cells += [code_cell(c) for c in nb["code"]]
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "accelerator": "GPU",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--out", default=".")
    ap.add_argument("--task", default="")
    args = ap.parse_args()

    root = Path(args.out) / args.name
    for sub in ("notebooks", "utils", "data", "results", "paper"):
        (root / sub).mkdir(parents=True, exist_ok=True)

    for nb in NOTEBOOKS:
        (root / "notebooks" / nb["file"]).write_text(json.dumps(build(nb, args.name, args.task), indent=1), encoding="utf-8")

    for script in ("ledger.py", "stats_tests.py"):
        shutil.copy(HERE / script, root / "utils" / script)

    state = TEMPLATES / "project_state.md"
    if state.exists() and not (root / "PROJECT.md").exists():
        shutil.copy(state, root / "PROJECT.md")

    print(f"Scaffolded {root}")
    for nb in NOTEBOOKS:
        print("  notebooks/" + nb["file"])
    print("Upload the folder to Drive at MyDrive/" + args.name + " so the setup cell paths resolve.")


if __name__ == "__main__":
    main()
