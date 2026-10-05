# Novelty and kill-mode checklist

Goal: try to disprove the idea before the user invests months in it.

## Procedure

1. **Restate the idea** in one sentence along five dimensions: Problem, Data/Language, Method, Evaluation, Claimed finding.
2. **Search hard.** Run at least 8 differently-phrased queries. Vary: task name synonyms, language names/scripts, method names and acronyms, "benchmark", "survey", "shared task", "we propose", "empirical study", "negative results". Search arXiv, ACL Anthology, Semantic Scholar/Google Scholar, ScienceDirect, Papers with Code, Hugging Face, GitHub. Check the last 12 months especially; preprints are prior art. Log every query in `PROJECT.md`.
3. **Collect candidates** (aim for 5-10 closest papers). Fetch the abstract or paper to confirm; do not rate from titles.
4. **Rate overlap** for each candidate, 0 = different, 1 = partial, 2 = same, on the five dimensions. Overlap = sum / 10.

| Overlap | Reading |
|---|---|
| >= 0.7 | Duplicate for practical purposes |
| 0.4 - 0.6 | Incremental; novelty rests on the dimensions that differ |
| < 0.4 | Meaningfully distinct |

   Report as a table with per-dimension marks, not a bare percentage.

5. **Run the reviewer "so what" tests:**
   - Would the result surprise an expert, or would they predict it?
   - Is it a change of data/language only (same method, expected outcome)?
   - Is it a combination with no mechanism?
   - Could a strong baseline already match it? (Check unfair comparisons in prior work.)
   - Is the contribution experimentally testable with the available data?
   - Is the effect big or general enough to matter?
6. **Verdict:**
   - **KILL**: closest work overlaps >= 0.7, or the idea fails the "so what" tests and no salvage exists.
   - **PIVOT**: core idea too incremental, but a variant is distinct (say which dimension to change).
   - **GO**: closest overlap < 0.4 on at least two dimensions, a mechanism exists, hypothesis is falsifiable.
7. **Salvage** (always provide for KILL/PIVOT): change the language/domain *and* add a diagnostic; swap the evaluation (robustness, calibration, fairness, efficiency); add a new resource with validation; reframe as a rigorous replication or negative result; narrow to a failure mode and explain it.

## Output format

```
Idea: <one sentence>
Searches run: <n> (see PROJECT.md log)

Closest existing work
| Paper (year, venue) | Problem | Data | Method | Eval | Finding | Overlap |
| ...                 |  2      |  1   |  2     |  1   |  0      | 0.6     |

Verdict: KILL / PIVOT / GO
Why: <2-4 sentences, evidence-labelled>
Salvageable version: <specific variant, what changes, why it is distinct>
Confidence in this verdict: Low / Medium / High, because <search coverage>
```

## Honesty about search coverage

You cannot prove a negative. Say "I found no work doing X in these sources with these queries" and state limits (paywalled venues, non-English venues, very recent preprints). Never say "this has never been done."
