---
type: matrix
title: Models × Sparks matrix
description: Every published DGX Spark model recipe in one table — how many Sparks it needs, its engine, measured speed, context and recipe link.
tags: [models, recipes, benchmarks, sizing]
resource: /models/spark-matrix.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [model sizing table, how many Sparks]
entities:
  - label: TensorFold
    kind: inference_engine
  - label: vLLM
    kind: inference_engine
  - label: SGLang
    kind: inference_engine
  - label: sparkDash
    kind: benchmark
relations:
  - type: summarizes
    target: /models/qwen38-27b-1x-tensorfold.md
  - type: depends_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /clustering/two-node-dac.md
provenance:
  - source: https://mia-ai.net/models
    note: MiaAI-Lab model catalog, snapshot 2026-10-29; one card per recipe with Sparks needed, decode, peak, prefill, context.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/05-serving-models.md
    note: Independent measurements with stock vLLM (August 2026), used as a cross-check.
citations:
  - id: mia
    text: "MiaAI-Lab, Free DGX Spark model recipes (catalog, snapshot 2026-10-29). https://mia-ai.net/models"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/main/docs/05-serving-models.md"
  - id: sparkring
    text: "MiaAI-Lab / FujitsuPolycom, sparkring — docs/RESULTS.md and DEEPSEEK_V4_FLASH_QUICKSTART.md. https://github.com/MiaAI-Lab/sparkring"
  - id: ds41-sglang
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash on 3x and 4x DGX Sparks (SGLang). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks"
  - id: ox-glm
    text: "0xSero, GLM-5.3 Flash EXL3 on 1x DGX Spark. https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark"
  - id: ox-ds
    text: "0xSero, DeepSeek V4 Flash on one DGX Spark (SparkInfer). https://github.com/0xSero/deepseek-v4-flash-0731-spark-sparkinfer"
---

# Overview

One row per published recipe that runs on DGX Spark (GB10). Figures come from the MiaAI-Lab catalog [mia]
unless marked otherwise, measured by the recipe author with sparkDash through the OpenAI API.

- **1-stream** = decode speed of a single request, prose (temperature 0.7, thinking on, unless noted).
- **Peak** = combined decode across N concurrent requests (×N).
- **Prefill** = prompt reading speed on a 32k-token prompt; "TTFT" rows give time to first token instead.
- *n/p* = not published. RTX-only recipes in the catalog are left out.

# 1 Spark

| Model | Engine · weights · drafter | 1-stream | Peak | Prefill | Context | Recipe |
|---|---|---|---|---|---|---|
| Qwen3.6 35B-A3B | vLLM · NVFP4 · MTP | 95.1 | 317 ×8 | n/p | 262k | [repo](https://github.com/MiaAI-Lab/Unsloth-Qwen3.6-35b-NVFP4-DGX-Spark) |
| Ling 3.0 Flash | SGLang · INT4 · DSpark | 83 | 136 ×6 | n/p | 256k | [repo](https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark) |
| Nemotron 3.5 Bolt 74B-A9B | TensorFold Zig · IQ2_XXS + NVFP4 · LiLiCorr | 71.0 | 166.6 ×8 | 1,375 | 262k, 16 streams | [page](https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark) |
| Qwen3.8 27B | TensorFold · MLX 4-bit · DFlash2 | 58.3 | 220.6 ×8 | 1,633 | 262k (1M YaRN) | [concept](/models/qwen38-27b-1x-tensorfold.md) |
| Qwen3.8 Flash Next | TensorFold Zig · NVIDIA FP4 QAD · MTP | 55.6 (64.4 INT4) | 156.1 ×5 | 2,735 | 262k, 5 streams | [page](https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold) |
| Ornith 1.5 122B | TensorFold Zig · EXL3 4-bit · DFlash2 | 52.6 | 111.0 ×4 (code) | 1,955 | 262k, 4 streams | [repo](https://github.com/MiaAI-Lab/Ornith-1.5-122B-TensorFold) |
| Qwen3.8 Flash Next | vLLM · NVFP4 | 48.7 | 163 ×8 | 1,769 | 262k (512k YaRN) | [repo](https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Single-DGX-Spark) |
| Muse Glimmer 30B | vLLM · NVFP4 · DFlash | ~35 | n/p | n/p | 256k | [repo](https://github.com/MiaAI-Lab/Muse-Glimmer-30B-DGX-Spark-RTX-5090-6000-PRO) |
| Qwen3.8 27B | SGLang · NVFP4 · DSpark / DFlash2 | 18.3 (DSpark) | 228 ×16 (DFlash2) | TTFT ~8.3 s @16k | 262k (1M YaRN) | [repo](https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark) |
| DeepSeek V4 Flash 0731, REAP-pruned² | SparkInfer · EXL3 · DSpark | 38.1 (code, median) | n/p | 1,055 (252k cold) | 262k | [repo](https://github.com/0xSero/deepseek-v4-flash-0731-spark-sparkinfer) |
| GLM 5.3 Flash 320B-A18B² | vLLM (B12X) · EXL3 2.0 bpw · native MTP | ~19 (sampling on) | n/p | ~470 (single stream) | 262k | [repo](https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark) |
| Laguna S 2.1 | vLLM · NVFP4 · DFlash | n/p on Spark¹ | 107 ×8¹ | n/p | 256k | [repo](https://github.com/MiaAI-Lab/Laguna-S-2.1-DGX-Spark-RTX-6000-PRO) |
| Nemotron 3.5 Lightning 30B-A3B | SGLang · NVFP4 · DSpark | n/p | 48 requests | n/p | 1M | [repo](https://github.com/MiaAI-Lab/Nemotron3.5-Lightning-DGX-Spark-RTX-5090-6000-PRO) |

¹ The catalog card shows 76.7 tok/s / 107 ×8 shared between "1 Spark" and "RTX PRO 6000" and the recipe
README gives no Spark figure, so the decode number is not attributed to the Spark here.
² 0xSero recipes, not in the MiaAI catalog; figures from their READMEs [ox-glm] [ox-ds]. The DeepSeek one
reports its own ≥35 tok/s acceptance gate as still pending. These two prove the ~300B models *fit* on one
Spark at 2–3 bits, at a third of the 2-Spark speed.

# 2 Sparks (one cable: [Two Sparks over one DAC](/clustering/two-node-dac.md))

| Model | Engine · weights · drafter | 1-stream | Peak | Prefill | Context | Recipe |
|---|---|---|---|---|---|---|
| DeepSeek V4.1 Flash 1017 | TensorFold Zig · EXL3 2.9-bit · DSpark | 74.9 | 130.0 ×4 | 2,175 | 1M | [repo](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks) |
| Qwen3.8 Flash Next | TensorFold Zig · NVFP4 · MTP | 67.4 (89.3 INT4) | 390.1 ×16 | 2,575 | 1M | [page](https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold) |
| GLM 5.3 Flash | TensorFold · EXL3 4-bit · DFlash2 | 60.4 | 108.8 ×4 | 1,979 | 1M | [page](https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| Qwen3.8 Flash Next | vLLM · NVFP4 | 54.4 | 207 ×8 | 2,962 | 262k (1M YaRN) | [repo](https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Dual-DGX-Sparks) |
| MiMo V2.6 Flash | SGLang · MXFP4 | 35.0 | 120 ×8 | 2,317 | 1M | [repo](https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks) |
| DeepSeek V4.1 Flash | vLLM · EXL3 2.9-bit | 31.6 | 54 ×4 (no speculation) | 1,055 | 600k | [repo](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks) |
| DeepSeek V4 Flash (2–3 Sparks) | vLLM · DSpark | 38.6 | 139 ×6 | TTFT 18.0 s @32k | n/p | [repo](https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark) |
| DeepSeek V4 Flash DSpark³ | vLLM (sparkring) · DSpark | 58.4 @16k | 307.1 ×32 (162.7 ×8) | 1,926 @16k | n/p | [sparkring](https://github.com/MiaAI-Lab/sparkring) |

# 3 and 4 Sparks

| Sparks | Model | Engine · weights · drafter | 1-stream | Peak | Prefill | Context | Recipe |
|---|---|---|---|---|---|---|---|
| 3 | GLM 5.3 Flash | TensorFold · EXL3 4-bit · DFlash2 | 77.6 | 146.2 ×4, 166.0 ×8 | n/p | 1M | [page](https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| 3 | GLM 5.3 (full model, ~273 GiB) | TensorFold · EXL3 2.75-bit · DSpark | 31.3 (code 41.7) | 1 request at a time | 591 | ~500k | [page](https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold) |
| 3 (card: 3–4) | GLM 5.3 Flash | vLLM · EXL3 4-bit | 40.1 | 88 ×4 | n/p | n/p | [repo](https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks) |
| 4 | GLM 5.3 Flash | TensorFold · EXL3 4-bit · DFlash2 | 95.2 | 163.3 ×4, 222.4 ×8 | n/p | 1M | [page](https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| 4 | DeepSeek V4.1 Flash 1017 (FP8 + MXFP4 as published) | TensorFold Zig · DSpark | 65.8 | 165.3 ×8 | 4,127 | 1M, 16 streams | [page](https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold) |
| 4 (switch) | DeepSeek V4.1 Flash | SGLang · TP4 | 87.7 (code 124.8) | 342.7 ×16 | 4,059–5,925 (4k–262k) | 1M (needle passed) | [repo](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks) |
| 4 | DeepSeek V4 Flash 0731³ | vLLM (sparkring) | 68.8 @16k | 508.1 ×32 (265.2 ×8) | 2,488 @16k | n/p | [sparkring](https://github.com/MiaAI-Lab/sparkring) |
| 4 | GLM 5.2 EXL3 3.5 bpw³ | vLLM (sparkring) | 20.2 @16k | 64.1 ×8 | 671 @16k | n/p | [sparkring](https://github.com/MiaAI-Lab/sparkring) |

³ sparkring records [sparkring]: 16k context, aggregate decode, its own normalized method. The author states the
DeepSeek V4 Flash profiles are **not qualified for general use** until a post-publication replay passes.

The 4-Spark DeepSeek run used a **switchless cabled ring** (one relayed hop between the two nodes without a
direct cable); a switch removes that hop.

# Independent cross-check: stock vLLM

Capetron measured some of the same models with the stock vLLM community patch chain in August 2026 [cape-serve]
(temperature 0, prose):

| Model | Sparks | Stock vLLM (Capetron) | Best catalog recipe |
|---|---|---|---|
| Qwen3.8 Flash Next | 1 | 24.8 tok/s, 86.4 ×6 | 55.6, 156.1 ×5 |
| Qwen3.8 Flash Next | 2 | 35.3 tok/s, 118.1 ×6 | 67.4, 390.1 ×16 |
| Qwen3.8 Flash Next | 4 (TP4 + expert parallel) | 39.6 tok/s, 167.4 ×6 | — |
| GLM 5.3 Flash | 2 | 16.0 tok/s, 52.1 ×6 | 60.4, 108.8 ×4 |
| GLM 5.3 Flash | 4 | 26.5 tok/s, 91.2 ×6 | 95.2 |

Dates, builds and sampling settings differ, so read this as an order of magnitude, not a ranking:
**the engine and recipe matter as much as the number of Sparks.**

# What the matrix says

1. **One Spark already serves useful models at 50–95 tok/s per request**, up to Ornith 1.5 122B and
   Nemotron 3.5 Bolt 74B, with 262k context.
2. **Two Sparks unlock 1M-token context and the ~300B-class MoE models** (DeepSeek V4.1 Flash, GLM 5.3 Flash)
   at 60–75 tok/s per request.
3. **Three to four Sparks are for the largest models**: the full GLM 5.3, or DeepSeek V4.1 Flash unquantized.
4. **For a team, independent Sparks beat one sharded model on throughput.** Capetron: four single-Spark
   endpoints of Qwen3.8 Flash Next give about 345 tok/s aggregate against 167 tok/s for the same model sharded
   over all four [cape-serve]. Clustering buys capacity (bigger models, longer context), not team throughput.

# Limitations

- Catalog figures are self-reported by one author on their own hardware with their own benchmark tool;
  the author has not reproduced most of them.
- **Benchmarks are best cases.** Alex Ellis saw DeepSeek V4 Flash at 30–40 tok/s in daily use on two Sparks
  where the recipe claimed 65–85 on a "count to 200" test — see
  [his report](/field-reports/alex-ellis-four-sparks.md). The author measured Qwen3.6 35B-A3B
  (NVFP4) with llama-benchy: 116.5 tok/s for one stream on an NVIDIA Founders Edition and 90.5–93.9 on a Dell Pro Max GB10
  before a vLLM image change, 102–106 after (2026-10-21 and 10-30), around the catalog's 95.1 — the vLLM image alone moved
  single-stream decode by ~15 % and doubled prefill on cached context
  ([home Spark stack](/field-reports/our-home-spark-local-ai.md), raw results in `benchmarks/`).
  Measure on your own workload before quoting any number as a promise.
- Licences differ per recipe: GLM 5.3 Flash's default DFlash2 drafter is CC BY-NC-ND 4.0, non-commercial
  only ([GLM 5.3 family](/models/glm53-family.md)).
- Recipes move fast (several releases a week); the catalog snapshot is 2026-10-29.
- Every catalog card ships an install prompt meant for a coding agent ("ask me before installing system
  packages, using sudo…"): the recipes are designed to be installed by an agent, not by hand.
