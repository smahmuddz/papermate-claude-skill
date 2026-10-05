# Statistical testing

Helpers live in `scripts/stats_tests.py` (copied to `utils/stats_tests.py` by the scaffold). They need only numpy and scipy, both preinstalled on Colab.

## Two sources of variance
1. **Test-set sampling variance**: would the result hold on a different sample of test items? Use paired bootstrap or McNemar on predictions from the same test set.
2. **Training variance**: would it hold with a different random seed? Use multiple seeds and compare per-seed scores.

Report both when you can. A claim of improvement needs the difference to survive the relevant one.

## Choosing a test

| Situation | Test | Notes |
|---|---|---|
| Two classifiers, same test items, accuracy/correctness | McNemar (exact) | Uses only discordant pairs |
| Two systems, same test items, any metric (macro-F1) | Paired bootstrap | Report difference and 95% CI; p = share of resamples where the difference is <= 0 |
| Two methods, scores from n seeds | Paired t-test or Wilcoxon signed-rank | With n = 5, Wilcoxon cannot go below p = 0.0625 (two-sided); report effect size and CI instead and say so |
| Several methods, several datasets | Friedman + post-hoc (Nemenyi) | Needs enough datasets; otherwise skip |
| Many comparisons | Holm-Bonferroni correction | Apply across the whole family of tests in the paper |

## Effect sizes and intervals
- Always give the absolute difference with a 95% CI, not just p.
- For seed-level comparisons add Cohen's d (paired) or Cliff's delta.
- For single-metric results, bootstrap CI over test items.
- Small improvements (< ~1 point) on small test sets are usually within noise; say so.

## Reporting rules
- State the test, the alpha, and what was paired.
- Name the family for multiple-comparison correction.
- Distinguish statistical from practical significance.
- Do not run many tests and report the one that passes (p-hacking). Pre-register the primary comparison in the experiment plan.
- Do not claim "significant" without having run a test.

## Minimal use
```python
from utils.stats_tests import paired_bootstrap, mcnemar, summarize_seeds, holm, macro_f1
res = paired_bootstrap(y_true, pred_proposed, pred_baseline, metric=macro_f1, n_boot=10000)
# res -> {"diff": ..., "ci_low": ..., "ci_high": ..., "p_one_sided": ...}
```
Log each outcome with `ledger.log_result(...)` so the paper's numbers trace back to a run.
