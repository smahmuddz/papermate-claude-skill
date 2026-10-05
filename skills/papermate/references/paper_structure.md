# Paper writing (results-grounded)

Write only from the results ledger and outputs the user has pasted. Anything not measured is `[RESULT REQUIRED]`. Anything not verified in a source is `[UNVERIFIED]` or omitted.

## Contents
1. Workflow
2. Section guide
3. Claim-evidence map
4. Elsevier-oriented extras
5. Final checks

## 1. Workflow
1. Read `PROJECT.md` and the ledger (`python scripts/ledger.py summary results/ledger.jsonl`).
2. Build the claim-evidence map (section 3) before drafting prose.
3. Draft section by section. Results first, then methods that explain them, then introduction/related work/discussion.
4. Lint: `python scripts/lint_manuscript.py draft.md --ledger results/ledger.jsonl`.
5. Run reviewer simulation (`reviewer_checklist.md`) before the user submits.

## 2. Section guide

```
Title, Abstract, Keywords, Highlights
1. Introduction
2. Related Work
3. Research Gap
4. Methodology
5. Experimental Setup
6. Results
7. Ablation Study
8. Error Analysis
9. Discussion
10. Limitations
11. Conclusion
Declarations, Data/Code availability, References
```

| Section | What it must do |
|---|---|
| Abstract | Problem, gap, method, main quantitative result (from ledger), implication. One clear claim, no hype. |
| Introduction | Why the problem matters, what is missing, your question, contributions (specific, testable bullets), roadmap. |
| Related Work | Organized by theme, ends by positioning against the closest papers from recon. Compare, do not list. |
| Research Gap | Gap statement with citations (template in `research_gap_framework.md`). |
| Methodology | Enough detail to reproduce: architecture, objective, prompts, hyperparameters, algorithm. |
| Experimental Setup | Datasets (source, license, split sizes), preprocessing, baselines, metrics, seeds, hardware, tuning budget. |
| Results | Main table with mean +/- std, significance tests, CIs; text states what the table shows without overclaiming. |
| Ablation | One component per row; interpret what each contributes. |
| Error Analysis | Taxonomy, counts, examples, comparison against baseline errors. |
| Discussion | Why the results look this way (label `[HYPOTHESIS]` unless tested), implications, surprising findings. |
| Limitations | Honest: data scope, language/domain, compute, single dataset, evaluation gaps, ethical risks. |
| Conclusion | Restate findings supported by results; future work that follows from limitations. |

## 3. Claim-evidence map

| Claim in paper | Evidence (ledger id / table / figure) | Status |
|---|---|---|
| "Method X improves macro-F1 over XLM-R" | ledger: exp-12 vs exp-07, paired bootstrap | supported / [RESULT REQUIRED] |

Delete or soften any claim without evidence. Avoid "state-of-the-art" unless compared against current SOTA under comparable conditions.

## 4. Elsevier-oriented extras (verify against the target journal's current guide for authors)
- Highlights (often 3-5 bullets, short) and sometimes a graphical abstract.
- Structured declarations: funding, competing interests, author contributions (CRediT), data availability, code availability.
- Generative-AI disclosure: Elsevier journals have a policy on declaring AI use in writing; check the current wording and follow it. The user should disclose any AI assistance in preparing the manuscript.
- Reference style per journal; verify every reference exists and the details match.
- Reproducibility: public repo/Zenodo release with config, seeds, and instructions; model/dataset cards.

## 5. Final checks
- Every number traces to the ledger; lint passes.
- Every cited paper was actually opened, and its DOI matches.
- No fabricated or placeholder citations remain.
- Contributions listed in the introduction match what the experiments support.
- Limitations section is real, not boilerplate.
- Remaining `[RESULT REQUIRED]` markers are listed to the user.
