# Research gap framework

## Contents
1. Gap types
2. Real gap vs "nobody combined X + Y"
3. Gap statement template
4. Turning a base paper into a research question
5. Contribution types reviewers accept

## 1. Gap types

| Type | Example (NLP) | Strength |
|---|---|---|
| Empirical | Claim shown on English only; untested in other languages/domains | Medium; stronger if you explain *why* it might not transfer |
| Methodological | Existing methods fail on a known failure mode (long text, code-mixing, negation) | High if you diagnose the failure first |
| Resource/data | No benchmark for task T in language L, or existing one is flawed (leakage, label noise) | High if the resource is validated and used to test models |
| Evaluation | Metrics don't capture what matters; no robustness/fairness/calibration testing | High, often underexploited |
| Theoretical/explanatory | Effect observed but unexplained | High; needs controlled experiments |
| Application | Method not yet applied to a real setting with real constraints | Medium; needs real stakes |
| Replication/negative | Published claim fails under fair baselines or other seeds | High when done rigorously |

## 2. Real gap vs "nobody combined X + Y"

"Nobody has combined X and Y" is a **hypothesis about a gap**, not a gap. There are four reasons it can be true; classify yours:

1. **Genuinely unexplored**: no one tried, and there is a mechanism suggesting it could matter.
2. **Tried and failed quietly**: it doesn't work; negative results rarely get published. (Search for it. A rigorous negative result may itself be the contribution.)
3. **Trivial**: any practitioner would predict the outcome. Reviewers call this incremental.
4. **Nobody cares**: works, but no downstream consumer.

Test for a real gap. Answer all four in writing:
- **Mechanism:** Why should X+Y behave differently from X alone and Y alone? What would the result tell us that we could not have predicted?
- **Prediction:** What specific outcome would *refute* the idea? (If nothing can, it is not a research question.)
- **Search:** What did you search to confirm nobody did it? (Cite the search log.)
- **Consumer:** Who would use or change behavior because of the finding?

If the mechanism or prediction is missing, rate Novelty at most 5.

## 3. Gap statement template

> Prior work [cite 2-4 closest] has shown <established finding>. However, <specific limitation, with evidence it matters>. This leaves open the question of <research question>. We address this by <approach>, and test whether <falsifiable hypothesis>.

Each sentence must be traceable to a source or an explicit `[HYPOTHESIS]` tag.

## 4. Base paper to research question

Walk the chain and write one line for each: Method -> Dataset -> Reported results -> Weaknesses (check: baselines weak? single seed? no significance? test-set tuning? narrow domain? no error analysis? unfair compute comparison?) -> Unanswered questions (from the paper's own limitations/future work, plus yours) -> Candidate improvements -> One research question -> Experimental design -> Expected contribution.

Rank candidate extensions by novelty, difficulty, risk, and Colab fit. The best Master's extension is usually **moderate novelty, low-to-medium difficulty, low risk, with a mechanism you can test via ablation**, not the most ambitious one.

## 5. Contribution types reviewers accept

A new method that beats strong, fairly tuned baselines; a diagnostic study that explains a failure; a validated resource plus benchmarking; a rigorous replication or negative result; a robustness/efficiency study with practical impact. "We applied model M to dataset D" is not a contribution unless the finding is surprising or the setting is under-resourced and the analysis is deep.
