# Ablation plan

Everything not listed as changed stays fixed (data, seeds, tuning budget).

| ID | Variant | What changes | Question answered | Expected if component matters |
|---|---|---|---|---|
| A0 | Full proposed model | - | reference | - |
| A1 | Without component A | remove A | does A contribute? | drop |
| A2 | Without component B | remove B | does B contribute? | drop |
| A3 | Without A + B | remove both | interaction | larger drop |
| A4 | A replaced by simple alternative | swap | is gain due to design or capacity? | drop |

Report: mean +/- std over seeds, difference vs A0 with CI, interpretation (including components that do not matter).
