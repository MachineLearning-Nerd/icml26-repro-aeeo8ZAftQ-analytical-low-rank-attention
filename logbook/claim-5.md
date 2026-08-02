# Claim 5 — analytical A3 components (finite clean-room toy)

**Live claim.** Theorem 2 supplies activation-aware SVD for A3-QK, Theorem 3 gives per-head autocorrelation-weighted A3-OV, and Lemma 4 uses CUR decomposition for nonlinear A3-MLP.

**Verdict: toy.** This is a clean-room five-seed finite matrix conformance fixture, not LLaMA/WikiText reproduction and not verification of universal theorem statements.

## Protocol

Pinned source excerpts: `evidence/claim5_attempt1/a3_qk_ov_excerpt.tex` and `a3_mlp_excerpt.tex` (hashes in `SHA256SUMS`). `src/claim5_a3_conformance.py` generates non-isotropic calibration activations (`d=12`, rank `r=4`) and implements:

- A3-QK: covariance-square-root weighted truncated SVD;
- A3-OV: per-head autocorrelation weighted truncated SVD;
- A3-MLP: diagonal channel-selection/CUR-style finite conformance.

Run: `../icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/.venv/bin/python src/claim5_a3_conformance.py --out outputs/claim5_a3_conformance --seeds 11 23 47 89 131`.

## Result and control

Across five fixed seeds, activation-aware QK relative score error was **0.1033** vs raw-SVD **0.2785**; activation-aware OV error was **0.1361** vs raw-SVD **0.2861**. The retained-energy MLP selection error was **0.2948** vs destructive low-energy selection **0.9580**. Raw CSV/config/log/summary are hash-manifested in `outputs/claim5_a3_conformance/`.

The raw-SVD and low-energy choices are predeclared negative controls and degrade in every fixed fixture. These finite results only demonstrate the stated linear-algebra route on synthetic matrices.
