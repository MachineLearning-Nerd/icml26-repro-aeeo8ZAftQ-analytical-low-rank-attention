# A3: Analytical Low-Rank Approximation Framework for Attention

Independent ICML 2026 reproduction workspace for OpenReview `aeeo8ZAftQ`.

## Scope

This workspace pins the live six-claim contract and arXiv `2505.12942` source. It uses local CPU/GPU only; no HF cpu-upgrade, Jobs, paid compute, or remote GPU service.

## Current milestone

Claim 1 source/protocol audit is complete. The paper-scale LLaMA-3.1-70B WikiText-2 result cannot be reproduced locally without the released model/evaluation protocol; no empirical claim outcome is asserted. The next local route is a direct finite A3-QK algebra/conformance implementation for Claim 5, followed by a separately labelled toy if appropriate.

## Verify source pins

```bash
(cd evidence/source && sha256sum -c SHA256SUMS)
python3 -m pytest -q
```
