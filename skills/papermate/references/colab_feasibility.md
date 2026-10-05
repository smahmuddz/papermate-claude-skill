# Feasibility and reproducibility check (Colab-first)

Fill this before calling any project feasible. Mark each line verified/unverified.

```
Dataset publicly available?            Y/N   <link you opened>
License permits research use?          Y/N   <license text/name>
Size, splits, label quality known?     Y/N   <numbers, IAA if reported>
Official code available?               Y/N   <repo, last commit, stars, open issues>
Pretrained weights available?          Y/N   <hub link, license, gated?>
GPU requirement                        <T4 / L4 / A100 / API>
Peak VRAM estimate                     <GB, with method>
Expected runtime per run               <hours>  x runs = <total>
Model size on disk                     <GB>
Training/inference cost                <free / paid compute units / API $>
Colab feasible?                        Y / Y with QLoRA / paid tier / N
Ethics/data-use constraints            <PII, social media ToS, sensitive content>
```

## Verify live limits
Colab GPU types, session length, RAM, and free-tier policies change. Check the current Colab FAQ/pricing page before stating limits. If you cannot, say "typical free-tier limits as I remember them, unverified".

## Back-of-envelope VRAM (state as estimates, `[INFERENCE]`)
- Weights: params x bytes/param (fp32 4, fp16/bf16 2, int8 1, 4-bit ~0.5).
- Full fine-tuning with Adam in mixed precision: roughly 16 bytes/param before activations. So ~1B params already strains 16 GB; 7B is out of reach without PEFT.
- LoRA/QLoRA: frozen base weights + small adapters + optimizer states for adapters + activations. A 7B model in 4-bit is feasible on a 16 GB GPU with short sequences, small batch, gradient checkpointing, but slow.
- Encoder models (mBERT, XLM-R base/large, BanglaBERT-style) fine-tune comfortably on a T4 with fp16 and modest batch/seq length.
- Activations scale with batch x sequence length; cut sequence length first.
- Always confirm with a 50-step smoke test and record the measured peak memory.

## Session survival
- Checkpoint to Google Drive each epoch or N steps; make notebooks resumable.
- Fix seeds; log the environment (GPU, library versions) in notebook 01.
- Keep runs under the free-tier session length; split long jobs into resumable chunks.
- Cache tokenized datasets and downloaded weights on Drive.

## LLM/API-based experiments
- Record exact model identifier and access date (hosted models change).
- Estimate cost = items x (input + output tokens) x price x prompts x runs; present before running.
- Plan for rate limits, parse failures, and non-determinism (temperature 0 reduces but does not remove variance).
- Check benchmark contamination risk for popular public datasets.

## Verdicts
- **Feasible**: all lines resolved, runtime fits.
- **Feasible with descoping**: say exactly what is cut (smaller model, subset, fewer seeds) and what claims that still supports.
- **Not feasible**: say which line blocks, and propose the nearest feasible variant.
