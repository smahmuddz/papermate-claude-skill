# Scoring rubric

Use integers 1-10. Every score gets a one-line evidence note (a paper, a dataset card, a measured number, a Colab limit you verified). A score without evidence is a guess; say so or omit it.

## Dimensions

| Dimension | Direction | Anchors |
|---|---|---|
| **Novelty** | higher = better | 1-3: done already / trivial recombination. 4-6: incremental (new data or setting, same method, expected result). 7-8: new question, setting, or finding that a reviewer would not call obvious. 9-10: new problem formulation or method with a clear mechanism and strong evidence. Rarely above 8 for a Master's project. |
| **Scientific contribution** | higher = better | Would the result change what a practitioner or researcher does or believes? 1-3: no. 4-6: useful resource or confirmation. 7-10: changes a conclusion, fixes a flawed benchmark, or reveals a robust, explained effect. |
| **Technical difficulty** | higher = harder | 1-3: standard fine-tuning/prompting. 4-6: custom training objective, adapter design, careful data engineering. 7-10: new architecture, large-scale pretraining. |
| **Implementation difficulty** | higher = harder | Engineering effort given available code. 1-3: runnable repo exists. 7-10: reimplement from paper with missing details. |
| **Dataset availability** | higher = better | 9-10: public, licensed for research, adequate size, reliable labels. 5-6: needs partial collection/annotation. 1-3: must build from scratch or access restricted. |
| **Colab feasibility** | higher = better | 9-10: fits free T4 comfortably. 6-8: fits with QLoRA/short sequences/checkpointing. 3-5: needs paid tier or API budget. 1-2: needs multi-GPU. |
| **Publication potential** | higher = better | Fit to a real venue plus novelty plus experimental depth. Name the venue type you have in mind. |
| **Risk** | Low / Medium / High | Chance the main hypothesis shows no effect, and whether a null result would still be publishable. |

## Gating rule

Do not average into one number. Apply the weakest-link rule:

- **Novelty, Dataset availability, Colab feasibility, Publication potential**: if any is 3 or below, the verdict cannot be GO as scoped. State which dimension blocks and what descoping would lift it.
- High Technical/Implementation difficulty is a cost, not a blocker, unless it blows the timeline.
- A high-risk idea can still be GO if a null result is itself publishable (e.g., a rigorous negative finding on a popular claim).

## Scorecard format

```
Scorecard: <idea name>
Novelty               7   Closest: <paper>; differs in <dimension>
Contribution          6   <why>
Technical difficulty  4   <why>
Implementation diff.  3   <repo exists / not>
Dataset availability  9   <dataset, license>
Colab feasibility     8   <model, VRAM, runtime>
Publication potential 7   <venue type>
Risk                  Medium   <what could fail; is null publishable?>
Gate result: GO / PIVOT / KILL; blocked by: <dimension or none>
```
