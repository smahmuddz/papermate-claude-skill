# Topic mining (thesis/topic funnel)

Use when the user has no idea yet, or wants "an easy NLP thesis topic". "Easy" means **feasible and defensible**, not trivial: a topic that is too easy is the one reviewers call incremental.

## Intake (one line, no interrogation)
Infer from context or ask once: subject area (default NLP/LLMs), language/domain interests, compute (default free Colab T4), time budget, target venue (default Elsevier journal). State assumptions and go.

## Funnel

```
Generate 10 candidates
  -> Remove already-published ideas        (search each; overlap >= 0.7)
  -> Remove ideas without usable datasets   (public, licensed, adequate size)
  -> Remove ideas needing expensive GPUs    (fails Colab feasibility)
  -> Remove low-novelty ideas               (Novelty <= 4)
  -> Remove ideas with thin experimental depth (cannot support baselines + ablation + error analysis)
  -> 5 survivors
  -> Rank by publication potential
  -> Top 3 thesis candidates
```

## Generating candidates
Draw from gap types in `research_gap_framework.md`. Good sources: limitations/future-work sections of recent surveys and papers, shared-task overviews, under-resourced language benchmarks, robustness/evaluation gaps in popular tasks, efficiency (small models vs LLMs) comparisons. Prefer candidates with a **mechanism** and a **falsifiable hypothesis**. Spread across gap types so the 10 are not variations of one idea.

## Elimination ledger
Keep a table so every elimination is auditable. Do not silently drop ideas.

| # | Candidate | Eliminated at | Evidence |
|---|---|---|---|
| 1 | ... | Already published | <paper, year, overlap 0.8> |
| 2 | ... | No dataset | <what you searched> |
| 3 | ... | survives | |

Run a lightweight autopsy (3-4 queries) on each candidate rather than the full 8+, then the full autopsy on the 5 survivors' top 3.

## Output
For each of the top 3: one-paragraph pitch, research question, falsifiable hypothesis, closest work and how it differs, dataset(s) with license, baseline list, proposed contribution, scorecard (`scoring_rubric.md`), Colab plan, main risk, and a recommended pick with reasons. Offer a first-week plan for the pick. Save to `PROJECT.md`.
