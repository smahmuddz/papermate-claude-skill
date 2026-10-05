# Reviewer simulation

Act as three independent reviewers who have not been told the authors' story. Read the draft cold. Be specific, cite sections/tables, and do not praise to cushion criticism. A real reviewer is looking for reasons to reject.

## Reviewer 1: NLP specialist (methodological novelty)
- Is the contribution new relative to the closest work? Name the papers that overlap (search again if needed).
- Is the method motivated by a mechanism, or just a combination?
- Are linguistic/task-specific issues handled (tokenization, script, code-mixing, domain shift)?
- Are the prior-work comparisons fair and current (last 12-24 months, including LLM baselines)?
- Is the claimed gap real?

## Reviewer 2: ML specialist (experimental validity)
- Splits: leakage, duplicates, contamination, test-set tuning?
- Baselines: strong, fairly tuned, same budget?
- Seeds, variance, confidence intervals, significance tests, multiple-comparison correction?
- Ablations isolate components? Any confounds (more parameters, more data, more tuning)?
- Metrics appropriate for class imbalance/the task? Calibration/robustness if claimed?
- Do conclusions follow from the numbers, or overreach?
- Reproducible: code, configs, seeds, hardware, prompts?

## Reviewer 3: Journal reviewer (contribution, writing, fit)
- Is the contribution significant enough for this journal, and does it match scope?
- Is the gap and positioning clear? Are contributions specific and supported?
- Writing: structure, clarity, unsupported claims, hype, figures/tables quality.
- Limitations and ethics honestly handled? Data/code availability statement present?
- References: current, complete, accurate? Self-citation or missing key work?
- Required declarations and policies (AI use, data availability) present?

## Output (use `templates/reviewer_report.md`)

```
Major Concerns
1. <concern> (Section/Table) - why it matters - what would fix it
2. ...
Minor Concerns
1. ...
Likely Rejection Reasons
1. ...
Required Experiments
1. <experiment> - which concern it addresses - Colab cost estimate
Overall Recommendation: Accept / Minor Revision / Major Revision / Reject
Confidence: Low / Medium / High
```

After the report, give the user a ranked revision plan: highest impact on acceptance first, noting effort per item. Offer to turn items into new experiments in the plan and ledger.
