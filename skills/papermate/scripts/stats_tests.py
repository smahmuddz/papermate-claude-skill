"""Statistical helpers for NLP/ML experiments (numpy + scipy only).

Functions
---------
macro_f1, accuracy           simple metrics so no sklearn is needed
bootstrap_ci                 CI for one system's metric over test items
paired_bootstrap             difference between two systems on the same test items
mcnemar                      exact McNemar test on correctness of two classifiers
summarize_seeds              mean, std, t-based CI across seeds
compare_seeds                paired comparison across seeds (t-test, Wilcoxon, effect sizes)
holm                         Holm-Bonferroni correction
Run `python stats_tests.py` for a self-test.
"""
from __future__ import annotations

import numpy as np
from scipy import stats


# ---------------------------------------------------------------- metrics
def accuracy(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    return float((y_true == y_pred).mean())


def macro_f1(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    scores = []
    for c in np.unique(y_true):
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        denom = 2 * tp + fp + fn
        scores.append(0.0 if denom == 0 else 2 * tp / denom)
    return float(np.mean(scores))


# ---------------------------------------------------------------- bootstrap
def bootstrap_ci(y_true, y_pred, metric=macro_f1, n_boot=2000, alpha=0.05, seed=0) -> dict:
    """Percentile bootstrap CI for a metric, resampling test items."""
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    rng = np.random.default_rng(seed)
    n = len(y_true)
    vals = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        vals[b] = metric(y_true[idx], y_pred[idx])
    lo, hi = np.percentile(vals, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"estimate": float(metric(y_true, y_pred)), "ci_low": float(lo), "ci_high": float(hi)}


def paired_bootstrap(y_true, pred_a, pred_b, metric=macro_f1, n_boot=10000, alpha=0.05, seed=0) -> dict:
    """Paired bootstrap of metric(A) - metric(B) over the same test items.

    p_one_sided is the share of resamples where A does not beat B
    (H1: A > B). Double it for a rough two-sided value.
    """
    y_true, pred_a, pred_b = map(np.asarray, (y_true, pred_a, pred_b))
    rng = np.random.default_rng(seed)
    n = len(y_true)
    diffs = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        diffs[b] = metric(y_true[idx], pred_a[idx]) - metric(y_true[idx], pred_b[idx])
    lo, hi = np.percentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    observed = metric(y_true, pred_a) - metric(y_true, pred_b)
    return {
        "diff": float(observed),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "p_one_sided": float((np.sum(diffs <= 0) + 1) / (n_boot + 1)),
        "n_boot": n_boot,
    }


# ---------------------------------------------------------------- McNemar
def mcnemar(y_true, pred_a, pred_b) -> dict:
    """Exact McNemar test (two-sided) on per-item correctness."""
    y_true, pred_a, pred_b = map(np.asarray, (y_true, pred_a, pred_b))
    a_ok, b_ok = pred_a == y_true, pred_b == y_true
    b = int(np.sum(a_ok & ~b_ok))  # A right, B wrong
    c = int(np.sum(~a_ok & b_ok))  # A wrong, B right
    n = b + c
    p = 1.0 if n == 0 else float(stats.binomtest(min(b, c), n, 0.5).pvalue)
    return {"a_only_correct": b, "b_only_correct": c, "p_two_sided": min(p, 1.0)}


# ---------------------------------------------------------------- seeds
def summarize_seeds(scores, alpha=0.05) -> dict:
    s = np.asarray(scores, dtype=float)
    n = len(s)
    mean = float(s.mean())
    std = float(s.std(ddof=1)) if n > 1 else 0.0
    if n > 1:
        half = float(stats.t.ppf(1 - alpha / 2, n - 1) * std / np.sqrt(n))
    else:
        half = float("nan")
    return {"n": n, "mean": mean, "std": std, "ci_low": mean - half, "ci_high": mean + half}


def compare_seeds(scores_a, scores_b) -> dict:
    """Paired comparison of per-seed scores (same seeds/splits for A and B)."""
    a, b = np.asarray(scores_a, float), np.asarray(scores_b, float)
    if len(a) != len(b) or len(a) < 2:
        raise ValueError("Need equal-length score lists with at least 2 seeds.")
    d = a - b
    out = {"n": len(d), "mean_diff": float(d.mean())}
    sd = d.std(ddof=1)
    out["cohens_d_paired"] = float(d.mean() / sd) if sd > 0 else float("nan")
    t = stats.ttest_rel(a, b)
    out["t_p_two_sided"] = float(t.pvalue)
    try:
        w = stats.wilcoxon(a, b)
        out["wilcoxon_p_two_sided"] = float(w.pvalue)
    except ValueError:  # all differences zero
        out["wilcoxon_p_two_sided"] = 1.0
    # Cliff's delta
    gt = sum(x > y for x in a for y in b)
    lt = sum(x < y for x in a for y in b)
    out["cliffs_delta"] = float((gt - lt) / (len(a) * len(b)))
    out["note"] = "With n<6 seeds the Wilcoxon p-value has a floor; lean on effect size and CI."
    return out


# ---------------------------------------------------------------- multiple comparisons
def holm(pvals, alpha=0.05) -> list[dict]:
    """Holm-Bonferroni step-down. Returns adjusted p and reject flag in input order."""
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * p[i]
        running = max(running, val)
        adj[i] = min(running, 1.0)
    return [{"p": float(p[i]), "p_adj": float(adj[i]), "reject": bool(adj[i] < alpha)} for i in range(m)]


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    rng = np.random.default_rng(1)
    y = rng.integers(0, 3, 400)
    a = np.where(rng.random(400) < 0.85, y, rng.integers(0, 3, 400))
    b = np.where(rng.random(400) < 0.78, y, rng.integers(0, 3, 400))
    print("macro_f1 A:", round(macro_f1(y, a), 4), "B:", round(macro_f1(y, b), 4))
    print("bootstrap_ci A:", bootstrap_ci(y, a, n_boot=500))
    print("paired_bootstrap:", paired_bootstrap(y, a, b, n_boot=2000))
    print("mcnemar:", mcnemar(y, a, b))
    print("summarize_seeds:", summarize_seeds([0.81, 0.83, 0.82, 0.80, 0.84]))
    print("compare_seeds:", compare_seeds([0.83, 0.84, 0.82, 0.85, 0.83], [0.80, 0.81, 0.80, 0.82, 0.79]))
    print("holm:", holm([0.001, 0.02, 0.04, 0.3]))
    print("self-test ok")
