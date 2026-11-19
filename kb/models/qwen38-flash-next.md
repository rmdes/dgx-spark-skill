---
type: model
title: Qwen3.8 Flash Next (and Qwen3.8 27B, Qwen3.6 35B) on DGX Spark
description: Qwen3.8 Flash Next recipes on one and two DGX Sparks (TensorFold and vLLM), the FP4 QAD vs INT4-AutoRound vs NVFP4 quality trade, independent Capetron numbers, plus the Qwen3.8 27B and Qwen3.6 35B-A3B single-Spark recipes.
tags: [models, qwen, moe, tensorfold, vllm, sglang, nvfp4, single-node, two-node]
resource: /models/qwen38-flash-next.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [Qwen3.8-Flash-Next, Qwen3.8 Flash, Qwen3.8-27B, Qwen3.6-35B-A3B]
entities:
  - label: Qwen3.8-Flash-Next
    kind: model
  - label: Qwen3.8-27B
    kind: model
  - label: Qwen3.6-35B-A3B
    kind: model
  - label: nvidia/Qwen3.8-Flash-Next-FP4-Local
    kind: checkpoint
  - label: INT4-AutoRound
    kind: checkpoint
  - label: TensorFold
    kind: inference_engine
  - label: vLLM
    kind: inference_engine
  - label: SGLang
    kind: inference_engine
relations:
  - type: part_of
    target: /models/spark-matrix.md
  - type: related_to
    target: /models/qwen38-27b-1x-tensorfold.md
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /clustering/two-node-dac.md
  - type: uses
    target: /stacks/tensorfold.md
  - type: uses
    target: /stacks/vllm.md
  - type: uses
    target: /stacks/sglang.md
  - type: uses
    target: /stacks/quantization-formats.md
  - type: uses
    target: /stacks/speculative-decoding.md
  - type: related_to
    target: /field-reports/capetron-six-node-cluster.md
provenance:
  - source: https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold
    note: MiaAI-Lab recipe page, one Spark, TensorFold 1.1.4 Zig engine, FP4 QAD default and INT4-AR option.
  - source: https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold
    note: MiaAI-Lab recipe page, two Sparks, TensorFold Zig engine, measured 2026-10-07.
  - source: https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Single-DGX-Spark
    note: Earlier one-Spark vLLM recipe (superseded), with the FP8 KV quality caveat.
  - source: https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Dual-DGX-Sparks
    note: Two-Spark vLLM TP2+EP+MTP3 recipe.
  - source: https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark
    note: Qwen3.8 27B on SGLang, one Spark, DSpark / MTP / DFlash2 lanes.
  - source: https://github.com/MiaAI-Lab/Unsloth-Qwen3.6-35b-NVFP4-DGX-Spark
    note: Qwen3.6 35B-A3B NVFP4 on vLLM, one Spark.
  - source: https://github.com/MiaAI-Lab/sparkring
    note: Normalized Qwen3.8-27B EXL3 results on two and four Sparks.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/05-serving-models.md
    note: Independent stock-vLLM measurements of Qwen3.8-Flash-Next NVFP4 on 1, 2 and 4 Sparks (August 2026).
citations:
  - id: mia-q1
    text: "MiaAI-Lab, Qwen3.8 Flash Next on one DGX Spark, with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold"
  - id: mia-q2
    text: "MiaAI-Lab, Qwen3.8 Flash Next on two DGX Sparks, with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold"
  - id: q-vllm1
    text: "MiaAI-Lab, Qwen3.8-Flash-Next on ONE DGX Spark (vLLM), README. https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Single-DGX-Spark/blob/b7c5da1a9e7448a14b480deee66eda3799b1eb43/README.md"
  - id: q-vllm2
    text: "MiaAI-Lab, Qwen3.8-Flash-Next-NVFP4-vLLM-Dual-DGX-Spark, README. https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Dual-DGX-Sparks/blob/cd839d0b62f6c737178a0c2037733420e0524ebf/README.md"
  - id: q27-sglang
    text: "MiaAI-Lab, Qwen3.8 27B on SGLang for DGX Spark, README. https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md"
  - id: q36
    text: "MiaAI-Lab, Qwen3.6-35B-A3B-NVFP4 — DGX Spark, README. https://github.com/MiaAI-Lab/Unsloth-Qwen3.6-35b-NVFP4-DGX-Spark/blob/79c9e6f359f6101cdacd0dfd6fe9861ae2493a4d/README.md"
  - id: sr-results
    text: "Sparkring, benchmark results. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/RESULTS.md"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
---

# Overview

**Qwen3.8 Flash Next** is a mixture-of-experts vision-language model with 512 routed experts, 10 active a
token (6.0B active parameters in the full NVFP4 checkpoint) [mia-q2]; one community quant names it
125B-A5B [mia-q1]. It is the model with the most complete one- and two-Spark coverage, and the only one where
an independent source (Capetron) measured 1, 2 and 4 Sparks with stock vLLM [cape-serve].

Three checkpoints compete, and they trade quality for speed:

| Checkpoint | Experts a token | Size | Quality evidence |
|---|---|---|---|
| NVIDIA FP4 QAD (`nvidia/Qwen3.8-Flash-Next-FP4-Local`) | 10 of 512 | ~96 GiB download, ~81 GiB in memory | Quantization-aware distilled against bf16: GPQA Diamond 91.5 % vs 92.2 % bf16, ToolEvalBench 88.7 % vs 89.4 % (NVIDIA model card, not measured by the recipe) [mia-q1] |
| NVIDIA NVFP4 (`nvidia/Qwen3.8-Flash-Next-NVFP4`) | 10 | ~124 GiB | Not published in the sources read |
| INT4-AutoRound (azampatti) | 5 (4.8B active) | ~122 GiB download, ~66 GiB in memory | About 10 % lower general capability on its authors' harness (46.6–47.6 vs 51.8); tool use unchanged (91 vs 91–92) [mia-q2] |

Unless marked Capetron, figures are **self-reported by the recipe author**.

# Qwen3.8 Flash Next recipes

| Sparks | Recipe | Engine · checkpoint | 1-stream decode | Peak aggregate | Prefill | Context |
|---|---|---|---|---|---|---|
| 1 | TensorFold [mia-q1] | TensorFold 1.1.4 Zig · FP4 QAD · MTP | 55.6 prose / 110.5 code | 156.1 ×5 prose; 217.6 ×5 code | 2,735 tok/s at 32k | 262k, 5 requests (1M with YaRN) |
| 1 | TensorFold [mia-q1] | same · INT4-AR | 64.4 prose | 200.9 ×8 | 2,630 tok/s at 32k | 262k |
| 1 | vLLM (superseded) [q-vllm1] | vLLM · Mia NVFP4 · MTP 3 | 48.7 prose | 162.9 ×8 | 1,769 tok/s at 32k | 262k (512k YaRN) |
| 1 | **Capetron, independent** [cape-serve] | stock vLLM · RadixArk NVFP4, n-gram table mmap | 24.8 prose / 31.1 code / 33.8 math | 86.4 ×6 | 2,376 tok/s warm | 297k-token KV |
| 2 | TensorFold [mia-q2] | TensorFold Zig TP2 · NVFP4 · MTP + copy drafts | 67.4 prose | 390.1 ×16 | 2,575 tok/s at 32k | 1M, 16 requests |
| 2 | TensorFold [mia-q2] | same · INT4-AR | 89.3 prose | 483.6 ×16 | 3,285 tok/s at 32k | 1M |
| 2 | vLLM [q-vllm2] | vLLM TP2 + EP + MTP3 · NVIDIA NVFP4 | 54.4 | 207.0 ×8 | 2,962 tok/s at 32k | 262k (1M YaRN) |
| 2 | **Capetron, independent** [cape-serve] | stock vLLM TP2 · RadixArk NVFP4 · MTP-4 | 35.3 prose / 36.0 code / 53.2 math | 118.1 ×6 | 2,303 tok/s warm | 1.85M-token KV |
| 4 | **Capetron, independent** [cape-serve] | stock vLLM TP4 + expert parallel · NVFP4 · MTP-4 | 39.6 / 57.0 / 76.9 | 167.4 ×6 | 3,547 tok/s warm | 2.64M-token KV |

## Notes

- The FP4 and INT4 tables of the one-Spark TensorFold recipe were not measured the same way (sum of
  per-request speeds vs tokens over wall time; T=0.7 thinking on vs greedy thinking off) [mia-q1].
- Plain TP4 cannot load this NVFP4 checkpoint (MoE intermediate size 640 slices to 160, below the kernel's
  alignment); `--enable-expert-parallel` fixes it [cape-serve].
- **Team throughput:** Capetron estimates four independent one-Spark endpoints give about 345 tok/s aggregate
  against 167 for the same model sharded over four [cape-serve].
- A one-Spark TensorFold server pinned ~98.6 GiB under five 100k-token prompts plus six short ones; keep at
  least 10 GiB free under load or the machine freezes [mia-q1].

# Which recipe for what

| Need | Recipe | Why |
|---|---|---|
| Single developer, one Spark | TensorFold 1x, FP4 QAD | Closest to bf16 on NVIDIA's numbers, 55.6 tok/s, 262k, images and video [mia-q1] |
| Single developer who wants speed over accuracy | TensorFold 1x or 2x, `CHECKPOINT=int4` | 64.4 (one Spark) / 89.3 (two) tok/s, at ~10 % lower general capability [mia-q1] [mia-q2] |
| Team | TensorFold 2x (16 requests), or several independent one-Spark servers | 390.1 tok/s at 16 requests on two [mia-q2]; Capetron's independent-endpoint argument above [cape-serve] |
| Longest context | TensorFold 2x | 1M window; a 998,986-token needle found (1,309 s prefill, earlier build) [mia-q2] |

# Quality evidence

- **FP4 QAD:** GPQA Diamond 91.5 % and ToolEvalBench 88.7 % vs 92.2 % / 89.4 % for bf16, from NVIDIA's model card
  [mia-q1]. Not reproduced by the recipe author or by us.
- **INT4-AR:** 46.6–47.6 vs 51.8 for the original on its authors' harness, tool use unchanged [mia-q2].
- **TensorFold exactness:** drafted, serial and concurrent replies identical; 26/26 exact at 128k and 256k;
  needles at 200k and 1M [mia-q2].
- **FP8 KV cache caveat (vLLM recipe):** the reference the author cites measured a long-reasoning benchmark
  falling from 6/6 to 2/6 with FP8 KV, because quantised keys perturb the sparse indexer; "degradation can
  appear as fluent, plausible, wrong reasoning while needles still pass." No long-reasoning A/B was run on the
  recipe host [q-vllm1]. Both TensorFold recipes also default to an FP8 KV cache [mia-q1] [mia-q2].

# Qwen3.8 27B

Dense 27B model. The TensorFold one-Spark recipe (58.3 tok/s, 220.6 ×8) has its own page:
[Qwen3.8 27B on one Spark (TensorFold)](/models/qwen38-27b-1x-tensorfold.md). Other recipes:

| Sparks | Recipe | Lane | Decode | Aggregate |
|---|---|---|---|---|
| 1 | SGLang, NVFP4 [q27-sglang] | DSpark | 51.5 tok/s code, 18.3 long essay | n/p |
| 1 | SGLang, NVFP4 [q27-sglang] | DFlash2 | 50.9 code, 25.4 long essay; 56.6 on a structural fixture | 227.6 ×16 (one boot, TTFT 4.18 s at ×16) |
| 2 | Sparkring EXL3 K5/K6 [sr-results] | probabilistic MTP | 29.50 at 16k | 142.20 ×8 |
| 4 | Sparkring EXL3 K5/K6 [sr-results] | probabilistic MTP | 35.07 at 16k | 191.02 ×8 |

SGLang TTFT on a fresh ~16k prompt is ~8.3 s warm [q27-sglang]. The author warns that code deltas under 15 %
are noise and that runs drift with power capping [q27-sglang]. Recipe licence MIT [q27-sglang].

# Qwen3.6 35B-A3B

Unsloth NVFP4 checkpoint on vLLM with MTP (2 tokens), one Spark, up to 262,144 tokens [q36]:

| Requests | Aggregate | Per stream | TTFT |
|---|---|---|---|
| 1 | 95.1 tok/s | 95.1 | 103 ms |
| 4 | 171.6 | 49.7 | 214 ms |
| 8 | 317.0 | 41.1 | 242 ms |

~50 GB of disk for weights and caches; recipe code MIT; the model licence is not stated in the README [q36].
The fastest single-Spark row in the [matrix](/models/spark-matrix.md), but a much smaller model (3B active).

# Licences

| Item | Licence |
|---|---|
| FP4 QAD checkpoint | NVIDIA Open Model Agreement; base model under the Qwen Community License 1.0 [mia-q1] |
| NVFP4 checkpoint | NVIDIA Open Model License, with the Qwen Community License 1.0 [mia-q2] [q-vllm2] |
| INT4-AR checkpoint | Qwen Community License 1.0, per its model card [mia-q1] |
| TensorFold 1x recipe / 2x recipe | MIT / Apache-2.0 [mia-q1] [mia-q2] |
| vLLM 1x and 2x recipes | AGPL-3.0-or-later [q-vllm1] [q-vllm2] |
| SGLang 27B, Qwen3.6 35B recipes | MIT [q27-sglang] [q36] |

# Limitations

- The FP4 QAD quality figures are NVIDIA's own; no source here measured GPQA on a Spark.
- Capetron's rows use stock vLLM from August 2026; the roughly 2× gap to the TensorFold rows is the engine and recipe.
