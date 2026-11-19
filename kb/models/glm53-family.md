---
type: model
title: GLM 5.3 family on DGX Spark
description: Every published DGX Spark recipe for Z.ai's GLM 5.3 Flash and full GLM 5.3 (plus GLM 5.2 on Sparkring) — one to four Sparks, EXL3 quants, measured speed, KL quality numbers and licences.
tags: [models, glm, moe, tensorfold, vllm, sglang, exl3, multi-node, quantization]
resource: /models/glm53-family.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [GLM-5.3-Flash, GLM 5.3 Flash, GLM-5.3, GLM-5.2, Z.ai GLM]
entities:
  - label: GLM-5.3-Flash
    kind: model
  - label: GLM-5.3
    kind: model
  - label: GLM-5.2
    kind: model
  - label: DFlash2
    kind: speculative_decoder
  - label: TensorFold
    kind: inference_engine
  - label: vLLM
    kind: inference_engine
  - label: EXL3
    kind: quantization_format
relations:
  - type: part_of
    target: /models/spark-matrix.md
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /clustering/two-node-dac.md
  - type: depends_on
    target: /clustering/three-node-ring.md
  - type: depends_on
    target: /clustering/switched-fabric.md
  - type: uses
    target: /stacks/tensorfold.md
  - type: uses
    target: /stacks/vllm.md
  - type: uses
    target: /stacks/sglang.md
  - type: uses
    target: /stacks/exl3-exllamav3.md
  - type: uses
    target: /stacks/speculative-decoding.md
  - type: uses
    target: /stacks/quantization-formats.md
  - type: uses
    target: /stacks/sparkring-sparkcache.md
  - type: related_to
    target: /field-reports/alex-ellis-four-sparks.md
  - type: related_to
    target: /field-reports/capetron-six-node-cluster.md
  - type: related_to
    target: /models/deepseek-v4-family.md
provenance:
  - source: https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold
    note: MiaAI-Lab recipe page, GLM 5.3 Flash on 2–4 Sparks with TensorFold (v1.10), with the KL comparison of the quants.
  - source: https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold
    note: MiaAI-Lab recipe page, full GLM 5.3 on three Sparks (release build 2026-10-04).
  - source: https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks
    note: Earlier vLLM recipe (superseded by the TensorFold one), 2–4 Sparks, README and REFERENCE at a8cc40d.
  - source: https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless
    note: Alex Ellis / OpenFaaS 4-Spark switchless vLLM NVFP4 recipe with production traffic numbers.
  - source: https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark
    note: Single-Spark vLLM recipe on a 2.0 bpw EXL3 quant with native MTP.
  - source: https://github.com/0xSero/GLM-5.3-Flash-DGX-Spark
    note: Single-Spark quant experiments (2.05 bpw mul1 SGLang, K2/TR3 2 bpw vLLM) with KL against BF16.
  - source: https://github.com/MiaAI-Lab/sparkring
    note: GLM 5.2 EXL3 3.5 bpw on four Sparks, normalized benchmark; GLM 5.3 TP4 quickstarts.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/05-serving-models.md
    note: Independent measurements of GLM-5.3-Flash NVFP4 with stock vLLM patches on 2 and 4 Sparks (August 2026).
citations:
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks, with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm-full
    text: "MiaAI-Lab, The full GLM 5.3, on three DGX Sparks. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
  - id: glm-vllm
    text: "MiaAI-Lab, GLM-5.3 Flash EXL3 on DGX Spark (vLLM), README. https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks/blob/a8cc40ddef876f033e0f1b4d8f178b0fee2a5351/README.md"
  - id: glm-vllm-ref
    text: "MiaAI-Lab, GLM-5.3 Flash EXL3 full reference (3x and 4x Spark sections). https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks/blob/a8cc40ddef876f033e0f1b4d8f178b0fee2a5351/docs/REFERENCE.md"
  - id: ellis-4x
    text: "Alex Ellis / OpenFaaS Ltd, GLM-5.3-Flash NVFP4 — 4x DGX Spark, switchless-ring TP4 + DFlash2 (MIT). https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/README.md"
  - id: sero-glm1x
    text: "0xSero, GLM-5.3 Flash EXL3 on 1x DGX Spark — native MTP serving, README. https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark/blob/6ff8595aa271f2eac49579fbf5e90cde9e90674e/README.md"
  - id: sero-glm-mul1
    text: "0xSero, MEASURED — turboderp-2.05bpw mul1 stack (2026-09-13). https://github.com/0xSero/GLM-5.3-Flash-DGX-Spark/blob/f8311c5f01b314ce083383ca1a40ab130ac9d94f/recipes/turboderp-2p05-sglang-mul1/MEASURED.md"
  - id: sero-glm-k2
    text: "0xSero, K2/TR3 2 bpw vLLM — Benchmark evidence. https://github.com/0xSero/GLM-5.3-Flash-DGX-Spark/blob/f8311c5f01b314ce083383ca1a40ab130ac9d94f/recipes/k2-tr3-2bpw-vllm/BENCHMARKS.md"
  - id: sr-results
    text: "Sparkring, benchmark results (GLM-5.2 EXL3 3.5 bpw, four Sparks). https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/RESULTS.md"
  - id: sr-glm53
    text: "Sparkring, GLM-5.3-Flash DFlash2 BF16 TP4 quickstart. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/GLM53_FLASH_DFLASH2_BF16_TP4_QUICKSTART.md"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
---

# Overview

Two Z.ai models and their predecessor have DGX Spark recipes:

| Model | Shape | Weights licence |
|---|---|---|
| GLM-5.3-Flash | 320B total, 18B active MoE, 45 layers, 288 routed experts [sero-glm1x] | MIT (Z.ai) [mia-glmf] |
| GLM-5.3 (full) | 78 layers of MLA with DeepSeek sparse attention, 256 routed experts, MTP head [mia-glm-full] | GLM-5.3 License [mia-glm-full] |
| GLM-5.2 | Served at EXL3 3.5 bpw on Sparkring only [sr-results] | n/p in the sources read |

GLM-5.3-Flash at 4 bits (~176 GB) does not fit one Spark, so the useful recipes start at two. The one-Spark
recipes run 2-bit quants at 9–19 tok/s. Figures are **self-reported by the recipe authors** unless the row
says Capetron, which measured independently with stock vLLM [cape-serve].

# Recipes: GLM 5.3 Flash

| Sparks | Recipe | Engine · weights · drafter | 1-stream decode | Peak aggregate | Prefill | Context |
|---|---|---|---|---|---|---|
| 1 | 0xSero 1x [sero-glm1x] | vLLM · EXL3 K2 2.0 bpw · native MTP depth 2 | 18.94 tok/s (sampled, thinking on) | n/p | 570.5 tok/s at 4k | 262k |
| 1 | 0xSero 2.05 bpw mul1 [sero-glm-mul1] | SGLang · EXL3 2.05 bpw (85.23 GB) · none | n/p ("speed cells pending") | n/p | ≈425 tok/s at 262k | 262k |
| 2 | TensorFold 2x [mia-glmf] | TensorFold · Mia EXL3 4 bpw · DFlash2 + copy drafts | 60.4 prose / 114.7 structured | 108.8 ×4 (130.8 ×8 with `PARALLEL=8`) | 1,978.9 tok/s at 32k | 1M |
| 2 | vLLM EXL3 (superseded) [glm-vllm] | vLLM · EXL3 4 bpw · DFlash2 | 36.1 prose / 54.6 code | 53.6 ×2 (short code) | 1,511 tok/s at 32k | 850k |
| 2 | **Capetron, independent** [cape-serve] | stock vLLM patch chain · NVFP4 · MTP-4 | 16.0 prose / 21.4 code / 31.1 math | 52.1 ×6 | 1,495 tok/s warm | 507k-token KV |
| 3 | TensorFold 3x [mia-glmf] | as 2x, `./start-tp3.sh` | 77.6 prose / 104.3 code | 146.2 ×4; 166.0 ×8 (separate boot) | 2,064 tok/s at 32k | 1M |
| 3 | vLLM EXL3 TP3 [glm-vllm-ref] | vLLM · EXL3 4 bpw · DFlash2 | 40.1 prose | 88.4 ×4 | n/p | n/p |
| 4 | TensorFold 4x, ring [mia-glmf] | as 2x, `tp4` branch, switchless ring | 95.2 prose / 138.6 code | 222.4 ×8 | 2,583 tok/s at 32k | 1M |
| 4 | Alex Ellis switchless [ellis-4x] | vLLM TP4 · NVFP4 · DFlash2 | ~45 tok/s typical on real traffic, up to ~100 warm | n/p | ~1,800 tok/s at 32–64k | 262k |
| 4 | **Capetron, independent** [cape-serve] | stock vLLM patch chain TP4 · NVFP4 · MTP-4 | 26.5 prose / 38.1 code / 46.7 math | 91.2 ×6 | 3,840 tok/s warm, 725 cold | 2.25M-token KV |

## Notes per recipe

- **TensorFold 2x–4x** is the recipe the vLLM one now points to ("an improved version ... Everyone should use
  that") [glm-vllm]. Since v1.9 it also answers Anthropic's `/v1/messages`, so Claude Code talks to it
  directly [mia-glmf]. Three-Spark decode at 590k context went from 66.2 to 184.4 tok/s in v1.9 [mia-glmf].
  The 4-Spark branch is experimental: the full exactness checks run at three Sparks have not been run at four [mia-glmf].
- **Alex Ellis 4x** is the only recipe with production numbers: 476 requests, ~17.5M tokens of real agentic
  coding traffic, deepest prompt 122k. Prompt tokens outweighed completion tokens about **58:1**, so
  "prefill throughput and prefix-cache reuse matter far more than a headline decode rate" [ellis-4x].
- **Capetron 4x with DFlash2 K=7:** single stream rises to 27.5 / 40.5 / 69.2 tok/s, but six-stream aggregate
  falls to 48.5 (−47 %); "use it for a single-user coding or math endpoint, not a shared one" [cape-serve].
- **Capetron 2x vs 4x:** two nodes give 56–67 % of four-node decode and run at a 3–4 % host-memory floor
  [cape-serve].
- **vLLM EXL3 on four Sparks** (contributor kit with a switch): decode 1.45× the 2-node baseline but cold
  prefill only +29 %, and a 96k chunked prefill beside 6–7 speculative streams hung all four ranks [glm-vllm-ref].

# Recipes: full GLM 5.3 (three Sparks)

TensorFold, Mia EXL3 2.75 bpw (~273 GiB, ~86 GiB of weights a Spark), DSpark drafts, one request at a time
in the default long-context mode [mia-glm-full]:

| Mode | Decode | Prefill | Context |
|---|---|---|---|
| `CP=1` (default), greedy | 31.3 prose / 41.7 code tok/s | 591.2 tok/s at 32k; 468 at 314k | 499,712 |
| `CP=1`, sampled (T=1.0) | 22.9–24.0 prose / 25.7–29.4 code | — | 499,712 |
| `CP=0 PARALLEL=4` | 48.2 tok/s total, 12.1–14.0 each | — | 32,768 a request |

A 314,225-token prompt took 671 s to first token and was answered correctly [mia-glm-full].

# Recipes: GLM 5.2 (Sparkring, four Sparks)

EXL3 3.5 bpw at 16k context: prefill 671 tok/s, 20.15 tok/s at C1, 64.13 aggregate at C8 [sr-results].
Sparkring's GLM 5.3 Flash TP4 profiles are documented as quickstarts without published speed numbers [sr-glm53].

# Which recipe for what

| Need | Recipe | Why |
|---|---|---|
| One Spark only | 0xSero 1x (MTP) | ~19 tok/s at 262k; usable for batch or overnight work, slow for interactive coding [sero-glm1x] |
| Single developer, two Sparks (the demo setup) | TensorFold 2x | 60.4 tok/s prose, 1M window, Anthropic API for Claude Code [mia-glmf] |
| Team | TensorFold 3x (8 requests by default) or 4x | 166.0 tok/s for 8 requests on three, 222.4 on four [mia-glmf] |
| Longest context | TensorFold 2x–4x | 1M window; a 981,841-token needle found on two Sparks (967 s to first token) [mia-glmf] |
| Largest model in the family | Full GLM 5.3 on three | ~500k window, one request at a time, ~31 tok/s [mia-glm-full] |

# Quality evidence

**Mia EXL3 4 bpw vs the earlier TR3-4bpw quant**, both served by TensorFold, KL divergence against Z.ai's
official FP8 release (lower is better) [mia-glmf]:

| | TR3-4bpw | Mia 4 bpw |
|---|---|---|
| KL, wiki / workload | 0.0990 / 0.3271 | **0.0903 / 0.3150** |
| GSM8K (250, greedy) | 98.0 % | 98.8 % |
| HumanEval (164, greedy) | 97.6 % | 95.7 % |
| HumanEval+ / MBPP+ (542, thinking on) | 86.3 % | 86.5 % |
| Size | 175.7 GB | 175.7 GB |

The author states the benchmark gaps are "a few problems each and go both ways; none is statistically
significant"; the measured gain is fidelity [mia-glmf].

**One-Spark 2-bit quants**, KL against the BF16 teacher on a frozen 65,504-position panel [sero-glm-mul1]:

| Quant | Size | Top-1 agreement | KL |
|---|---|---|---|
| K2/TR3 (earlier release) | 111.35 GB | 77.385 % | 0.439 |
| 2.05 bpw mul1 | 85.23 GB | 78.902 % | 0.384 |

The 2.05 bpw recipe passed 15 of 20 pre-registered samples, with free-form generation the weak family (1/5)
[sero-glm-mul1]. A "mosaic" quant scores higher (top-1 0.80842, KL −15.3 %) but decodes at ~9–10 tok/s
because it cannot use MTP [sero-glm1x]. The 2 bpw vLLM baseline without drafts measured ~9.3 tok/s [sero-glm-k2].

**Full GLM 5.3:** fp4 vs FP8 KV cache on the recipe's paired suite showed no significant difference
(McNemar p = 1.00 in every category; e.g. 123/150 vs 124/150 short questions, 25/25 Python tasks on both);
recall of 112 of 112 keys at up to ~314k tokens [mia-glm-full].

# Licences

| Item | Licence |
|---|---|
| GLM-5.3-Flash base model | MIT (Z.ai) [mia-glmf] |
| Mia GLM-5.3-Flash EXL3 4 bpw | Apache-2.0 [mia-glmf] |
| TR3-4bpw (older default) | ShapleyMcg License 1.0, attribution required [mia-glmf] |
| **DFlash2 drafter (IncoAI)** | **CC BY-NC-ND 4.0, non-commercial use only**; `DRAFTER=mtp` avoids it, one request at a time [mia-glmf] |
| Full GLM-5.3 EXL3 2.75 bpw and Red Hat DSpark speculator | GLM-5.3 License [mia-glm-full] |
| TensorFold recipes | Apache-2.0 [mia-glmf] [mia-glm-full] |
| vLLM EXL3 recipe | AGPL-3.0 (contributions before 2026-09-07 MIT) [glm-vllm] |
| Alex Ellis 4x recipe; 0xSero 1x code | MIT [ellis-4x] [sero-glm1x] |

The DFlash2 drafter licence matters for a workplace deployment: the TensorFold recipe's default drafter is
non-commercial, and the alternative (MTP) serves one request at a time.

# Limitations

- Each Spark needs about 110 GiB free when the 2x TensorFold server starts; a Spark that runs out of unified
  memory freezes instead of failing [mia-glmf] [mia-glm-full].
- The 4-Spark TensorFold branch was measured on a ring, not a switch, and lags the 2-Spark fixes after v1.10 [mia-glmf].
- Capetron's GLM rows are stock vLLM from August 2026; the gap to the TensorFold rows is the engine and recipe,
  not the hardware [cape-serve].
