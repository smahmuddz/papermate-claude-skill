# Contributing to PaperMate

Thanks for helping improve PaperMate.

## Ground rules
- Keep the anti-fabrication rules intact: no invented citations, DOIs, datasets, results, or journal data in any file, example, or test.
- Examples must use placeholders (`<Paper A>`), never fake references.
- Explain *why* an instruction exists; avoid bare "MUST" rules.
- Keep `SKILL.md` under ~500 lines; put detail in `references/`.

## Ways to contribute
- New reference files for other domains (vision, speech, tabular ML, RL).
- Better scoring anchors or reviewer checklists.
- More templates and example prompts.
- Bug fixes for `scripts/` (run `python skills/papermate/scripts/stats_tests.py` for the self-test).
- Test prompts with expected behaviors (add under `examples/`).

## Workflow
1. Fork and create a branch.
2. Make changes under `skills/papermate/`.
3. Rebuild `dist/papermate.skill` if the skill changed (zip the `papermate` folder, or use the skill-creator packaging script).
4. Open a pull request describing what changed and why.
