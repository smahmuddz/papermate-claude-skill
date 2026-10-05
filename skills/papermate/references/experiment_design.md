# Experiment design

## Contents
1. Principles
2. Experiment matrix
3. Splits and leakage
4. Baselines
5. Metrics
6. Seeds, tuning budget, fairness
7. LLM-specific controls
8. Ablations
9. Error analysis and human evaluation
10. Reporting efficiency

## 1. Principles
- Every experiment answers a stated hypothesis that it could falsify. Write the hypothesis first.
- The test set is touched once per final configuration. Tune on validation only.
- Give baselines the same tuning effort and compute as the proposed method; unfair baselines are the most common reason for rejection.
- Plan for a null result: decide in advance what you will conclude if the method does not win.

## 2. Experiment matrix

```
Dataset
 +- Train / Validation / Test (fixed, versioned)
Baselines
 +- Classical (TF-IDF + SVM / LR)
 +- Neural (BiLSTM / CNN)
 +- Pretrained encoders (mBERT, XLM-R, language-specific model)
 +- LLM zero/few-shot (if relevant)
 +- Strongest published prior result (reproduced, not copied)
Proposed
 +- Proposed method (final config)
Ablation
 +- Without component A / without B / without A+B / component swapped
Analysis
 +- Error analysis, robustness, efficiency
```
Adapt rows to the task; add a row for every claim the paper will make.

## 3. Splits and leakage
- Use the official split if one exists; otherwise stratified split with a recorded seed.
- Deduplicate (exact and near-duplicate) across train/val/test; report how many were removed.
- Check temporal, author, or source leakage (same user/thread/article across splits).
- Keep a hash of the split files in the ledger/notebook 02.

## 4. Baselines
Choose to cover a ladder (simple, standard, strong, state of the art). Always include a majority-class/random baseline for context. Reproduce prior SOTA yourself on your split; if you quote their number, state that the setup differs.

## 5. Metrics
- Imbalanced classification: macro-F1 (primary), plus accuracy, per-class P/R/F1, MCC if useful.
- Generation: task-appropriate automatic metrics plus a small human evaluation; automatic metrics alone are weak evidence.
- Calibration/robustness when claims involve reliability (ECE, perturbation accuracy drop).
- Choose the primary metric before running anything and say why.

## 6. Seeds, tuning budget, fairness
- At least 3 seeds, preferably 5, for trained models; report mean +/- std and a CI.
- Fix and document the hyperparameter search space and trial budget; same for every method.
- Record the exact config of each run in the ledger (`config` field).
- Report training time and parameter count so comparisons are not hiding compute differences.

## 7. LLM-specific controls
- Version every prompt; report the final prompt text (appendix) and how it was chosen (on validation only).
- Fixed decoding settings; temperature, max tokens, stop sequences recorded.
- Parse failures counted as errors, reported as a rate, never silently dropped.
- Repeat stochastic runs; report variance across runs.
- Model identifier + access date; open-weight models preferred for reproducibility.
- Contamination check or caveat for public benchmarks.
- For PEFT: report rank, alpha, target modules, trainable parameter count.

## 8. Ablations
Each ablation removes or replaces exactly one component and keeps everything else (data, seeds, budget) fixed. Use `templates/ablation_plan.md`. Include a "component swapped for a simple alternative" row to show the component is not just adding parameters. If an ablation shows a component does nothing, report it; do not hide it.

## 9. Error analysis and human evaluation
- Sample errors (stratified by class/length/domain), categorize with a written taxonomy, and report counts.
- Compare proposed vs strongest baseline errors: what does the method fix, and what does it newly break?
- Human evaluation: at least 2 annotators, written guidelines, report agreement (Cohen's/Fleiss' kappa or Krippendorff's alpha). Say who annotated and how they were recruited and compensated.

## 10. Reporting efficiency
Parameters, trainable parameters, GPU type, wall-clock training time, inference latency/throughput, peak VRAM. Reviewers and practitioners increasingly require this.
