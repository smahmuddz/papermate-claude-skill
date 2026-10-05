# Experiment plan: <project>

## Hypotheses
| ID | Hypothesis | Refuted if | Primary metric |
|---|---|---|---|
| H1 | | | |

## Data
- Source / license / version:
- Split (train/val/test), seed, hash:
- Dedup and leakage checks:

## Systems
| ID | System | Type (baseline/proposed) | Config source | Notebook |
|---|---|---|---|---|
| B0 | Majority class | baseline | - | 03 |
| B1 | TF-IDF + SVM | baseline | | 03 |
| B2 | BiLSTM | baseline | | 03 |
| B3 | mBERT | baseline | | 03 |
| B4 | XLM-R | baseline | | 03 |
| P1 | Proposed | proposed | | 04 |

## Protocol
- Seeds: (>= 3, preferably 5)
- Tuning: search space, trial budget (same for all systems), tuned on validation only
- Metrics: primary / secondary
- Statistical tests: (pre-registered primary comparison; correction family)
- Compute: GPU, est. runtime per run x runs = total

## Analyses
- Ablations: see ablation_plan.md
- Error analysis: sampling, taxonomy
- Robustness / efficiency:

## Decision rules
- If H1 is supported: ...
- If not: what we report and conclude

## Run checklist
- [ ] Smoke test (50 steps) passed, VRAM recorded
- [ ] Every reported number logged via ledger.log_result
- [ ] Checkpoints on Drive, resumable
