# PaperMate: Claude Skill for Research Gap Finding, Novelty Checking and Thesis Topic Selection

> **An AI research assistant skill for Claude that tries to kill your research idea before you waste months on it.**
> Literature search, research gap detection, novelty check, Google Colab feasibility, experiment and ablation design, statistical testing, results-grounded paper writing, simulated peer review, and journal targeting (Elsevier-first) for NLP, LLM and machine learning research.

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange)
![Domain: NLP / LLM / ML research](https://img.shields.io/badge/domain-NLP%20%7C%20LLM%20%7C%20ML-green)
![Google Colab ready](https://img.shields.io/badge/Google%20Colab-ready-yellow)

**PaperMate** is a [Claude Skill](https://www.anthropic.com/news/skills) that turns Claude into a skeptical senior researcher, a research engineer, and a journal reviewer. It takes a rough idea or a base paper and moves it through a gated pipeline toward a **defensible, reproducible, publication-oriented research project**, without inventing citations, datasets, or results.

---

## Table of contents

- [Why PaperMate](#why-papermate)
- [Who it is for](#who-it-is-for)
- [What it does](#what-it-does)
- [Quick start](#quick-start)
- [Example prompts](#example-prompts)
- [The pipeline](#the-pipeline)
- [Anti-fabrication guarantees](#anti-fabrication-guarantees)
- [Repository layout](#repository-layout)
- [Included tools (Colab-friendly)](#included-tools-colab-friendly)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## Why PaperMate

Most AI research assistants help you *prove your idea is good*. PaperMate does the opposite:

> Your job is not to help the researcher prove their idea is good. Your job is to determine whether the idea deserves to be researched.

Typical failure modes it is built to prevent:

| Problem | How PaperMate handles it |
|---|---|
| "Nobody has combined X + Y" turns out to be already published | **Kill-my-idea mode** runs 8+ differently-phrased searches and rates overlap with the closest papers before recommending anything |
| A "gap" that is really just an incremental combination | A **real-gap test** requires a mechanism, a falsifiable prediction, and a consumer for the finding |
| Months spent on an experiment that does not fit your GPU | **Colab feasibility check** (dataset license, VRAM, runtime, cost) before design |
| Hallucinated references, DOIs, or benchmark numbers | Everything cited must have been opened in the session; otherwise tagged `[UNVERIFIED]` |
| Invented results in the manuscript | A **results ledger** and a **manuscript linter**: unmeasured numbers become `[RESULT REQUIRED]` |
| Rejection for weak baselines, no seeds, no significance tests | **Experiment design**, **statistics helpers**, and a **three-reviewer simulation** |
| Submitting to the wrong journal | **Journal targeting** from where the closest papers were published, verified on live journal pages |

## Who it is for

- Master's and PhD students looking for a **thesis topic** or **research gap** in NLP, LLMs, or machine learning
- Researchers working with **low-resource languages** (for example Bangla) and limited compute
- Anyone who wants to run experiments in **Google Colab** and aim at **Elsevier journals** or similar venues
- Supervisors and reviewers who want a structured second opinion on novelty and experimental validity

## What it does

1. **Research reconnaissance**: recent and foundational papers, competing approaches, datasets, GitHub implementations, benchmarks, surveys, and papers in target journals, summarized as paper cards.
2. **Idea autopsy (kill mode)**: closest-work table with five-dimension overlap rating (problem, data, method, evaluation, finding) and a verdict of **KILL**, **PIVOT**, or **GO**, always with a salvageable version.
3. **Research gap detection**: gap taxonomy and the real-gap vs "X + Y" test.
4. **Base paper to improved paper**: method, dataset, weaknesses, unanswered questions, ranked extensions, research question, experimental design.
5. **Scorecards**: novelty, contribution, difficulty, dataset availability, Colab feasibility, publication potential, and risk, each with evidence and a weakest-link gating rule.
6. **Experiment designer**: splits, baselines, metrics, seeds, tuning budget, ablations, error analysis, human evaluation.
7. **Reproducibility and Colab check**: license, code, weights, VRAM, runtime, cost, ethics.
8. **Notebook scaffold**: eight Colab notebooks from setup to results, each with objectives, libraries, expected outputs, checkpoints, and debugging guidance.
9. **Statistics**: paired bootstrap, McNemar, seed-level comparisons, effect sizes, Holm correction.
10. **Results-grounded paper writing**: section guide, claim-evidence map, Elsevier-oriented extras.
11. **Reviewer simulation**: NLP specialist, ML specialist, and journal reviewer, ending in major/minor concerns, required experiments, and a recommendation.
12. **Journal targeting**: scope match, recent similar papers, open access and APC information (verified live), difficulty, fit, and mismatches.
13. **Topic funnel**: 10 candidate ideas filtered to 5 survivors and the top 3 thesis candidates, with an auditable elimination ledger.

## Quick start

### Option A: Claude (web, desktop, or mobile)

1. Download [`dist/papermate.skill`](dist/papermate.skill) from this repository.
2. In Claude, open the settings page for skills/capabilities and upload the file (menu labels may change over time; see Anthropic's current Skills documentation).
3. Make sure web search is enabled, so novelty claims can be verified.
4. Start a chat with one of the example prompts below.

### Option B: Claude Code

Copy the skill folder into your skills directory:

```bash
# personal skills (all projects)
cp -r skills/papermate ~/.claude/skills/papermate

# or project-level skills
mkdir -p .claude/skills && cp -r skills/papermate .claude/skills/papermate
```

### Option C: Use the helper scripts on their own

```bash
python skills/papermate/scripts/scaffold_project.py my-thesis --out ./projects --task "Bangla sentiment analysis"
```

Upload the generated folder to Google Drive at `MyDrive/my-thesis` and open the notebooks in Colab.

## Example prompts

```text
Find me an easy NLP thesis topic.
```
```text
Is Bangla sentiment analysis with LLMs still a viable Master's thesis? Try to kill the idea first.
```
```text
Here is a paper (PDF attached). Find its weaknesses and propose three extensions ranked by novelty, difficulty, and risk.
```
```text
Design the experiments and ablations for this research question and check that it fits on a free Colab T4.
```
```text
Here are my results from the ledger. Write the Results and Discussion sections, and mark anything unmeasured as [RESULT REQUIRED].
```
```text
Review my draft like three skeptical reviewers and tell me the likely rejection reasons.
```
```text
Which Elsevier journals fit this paper? Verify scope and APC from the journal pages.
```

## The pipeline

```text
Idea -> Recon -> Autopsy -> [GATE 1: KILL / PIVOT / GO]
     -> Gap & novelty -> Feasibility -> [GATE 2: doable on your compute?]
     -> Experiment design -> Colab notebooks -> (you run experiments)
     -> Results ledger -> Statistics -> Paper writing
     -> Reviewer simulation -> Journal targeting
```

PaperMate stops at each gate and shows its verdict instead of rushing to write a proposal.

Illustrative kill-mode output format (placeholders, not real papers):

```text
Idea: <one sentence>
Searches run: <n>

Closest existing work
| Paper (year, venue) | Problem | Data | Method | Eval | Finding | Overlap |
| <Paper A>           |   2     |  1   |   2    |  1   |   0     |  0.6    |
| <Paper B>           |   1     |  1   |   1    |  0   |   0     |  0.3    |

Verdict: PIVOT
Salvageable version: <what to change and why it becomes distinct>
Confidence: Medium, because <search coverage and its limits>
```

## Anti-fabrication guarantees

- **No novelty claim without searching.** If no search tool is available, PaperMate says so and gives you exact search strings to run.
- **No invented** citations, DOIs, datasets, repositories, benchmark numbers, journal metrics, or results.
- **Epistemic labels** on important claims: `[FACT]`, `[LIT]`, `[INFERENCE]`, `[HYPOTHESIS]`, `[SPECULATION]`.
- **Ledger-backed numbers.** Manuscript values must exist in `results/ledger.jsonl`; otherwise `[RESULT REQUIRED]`.
- **Live verification** of anything that changes: APCs, journal scope, impact metrics, Colab limits, model versions, publisher AI-disclosure policies.
- **Honest wording**: "I found no work doing X in these sources", never "this has never been done".

## Repository layout

```text
papermate-claude-skill/
├── README.md
├── LICENSE
├── CITATION.cff
├── CONTRIBUTING.md
├── dist/
│   └── papermate.skill            # ready-to-upload skill package
├── skills/papermate/
│   ├── SKILL.md                   # skill instructions and routing
│   ├── references/                # gap framework, kill checklist, rubric, design, stats, writing, review, journals
│   ├── templates/                 # paper card, proposal, experiment plan, ablation plan, outline, review report
│   └── scripts/                   # scaffold, ledger, stats, manuscript lint
├── examples/
│   └── prompts.md
└── docs/
    └── GITHUB_SETUP.md            # repository description, topics, SEO checklist
```

## Included tools (Colab-friendly)

| Script | Purpose |
|---|---|
| `scaffold_project.py` | Generates the 8-notebook Colab layout, `PROJECT.md`, and utility modules |
| `ledger.py` | Logs every measured result to `ledger.jsonl` with seed, config, and notebook |
| `stats_tests.py` | Bootstrap CIs, paired bootstrap, McNemar, seed comparisons, Holm correction (numpy + scipy only) |
| `lint_manuscript.py` | Flags numbers missing from the ledger, open markers, DOIs to verify, and unsupported superlatives |

Generated notebooks: `01_setup`, `02_data_preparation`, `03_baselines`, `04_proposed_method`, `05_ablation`, `06_error_analysis`, `07_statistics`, `08_results`.

## FAQ

**What is a Claude Skill?**
A packaged set of instructions, reference files, templates, and scripts that Claude loads when a task matches the skill's description. See Anthropic's documentation for the current format and installation steps.

**Does PaperMate write my paper for me?**
It writes only from your measured results and verified sources. Unmeasured claims stay as `[RESULT REQUIRED]`. You are responsible for the work and for following your target journal's policies, including disclosure of AI assistance.

**Can it guarantee my idea is novel?**
No. It reports what it found with the queries and sources it had access to, and states the limits of that search. Absence of evidence in search results is not proof.

**Does it only work for NLP and LLMs?**
The defaults target NLP/LLM research with Google Colab and Elsevier journals, but the pipeline (autopsy, design, statistics, review) applies to most empirical machine learning work. Adjust the context in your first message.

**Can it run my experiments?**
No. It designs them, scaffolds the notebooks, and tells you what to run and paste back.

**Is it limited to Elsevier?**
No. Elsevier is the default target; it will say when no Elsevier journal fits and suggest alternatives.

## Limitations

- Quality of novelty checking depends on the search tools available in your Claude setup.
- Paywalled, non-English, and very recent venues may be under-covered.
- Scores are structured judgments backed by evidence, not objective measurements.
- Journal information changes; always confirm on the publisher's site before submitting.

## Contributing

Issues and pull requests are welcome: new reference files for other domains (vision, speech, tabular ML), better rubrics, more templates, or evaluation prompts. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

If PaperMate helps your research workflow, you can cite it using [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button).

## License

MIT. See [LICENSE](LICENSE).

---

<sub>Keywords: Claude skill, AI research assistant, research gap finder, novelty checker, literature review assistant, thesis topic finder, Master's thesis ideas, NLP research, LLM research, machine learning research, Google Colab experiments, experiment design, ablation study, statistical significance testing, reproducibility, peer review simulator, journal finder, Elsevier, low-resource languages, Bangla NLP, academic writing assistant.</sub>
