# Claim 1 — source/protocol audit

## Exact live claim

A3's low-rank approximated LLaMA 3.1-70B achieves WikiText-2 perplexity 4.69 at 10% compression versus SVD-LLM 7.87 (Table 1).

## Pinned evidence

- arXiv `2505.12942`, source archive and PDF: `evidence/source/SHA256SUMS`.
- Retained source table: `tables/tab-main-ppl-full.tex` in the pinned archive.
- Method source: `sections/03_method.tex` in the pinned archive.

## Protocol availability finding

The pinned paper source supplies tables and method TeX but no LLaMA-3.1-70B weights, WikiText-2 preprocessing/evaluation launcher, SVD-LLM pin, compression configuration, calibration activations, seed list, or benchmark outputs. A claimed 70B perplexity number cannot be independently rerun source-faithfully from the archive.

## Outcome

**Inconclusive.** This is a source/protocol audit, not a numerical reproduction, toy, verification, or falsification. The direct local next step targets the separately live mathematical A3-QK/OV/MLP claim with finite matrix conformance tests.
