---
type: matrix
title: Registry recipes (local-ai-registry)
description: All 46 DGX Spark recipes in the community local-ai-registry, with which figures the registry measured itself (5) and which it copied from recipe authors (41).
tags: [models, recipes, registry, benchmarks, provenance]
resource: /models/registry-recipes.md
timestamp: "2026-10-30T00:00:00Z"
aliases: ["local-ai-registry", "sybilsolutions registry"]
entities:
  - label: local-ai-registry
    kind: catalog
  - label: MiaAI-Lab
    kind: recipe_author
relations:
  - type: complements
    target: /models/spark-matrix.md
  - type: cites
    target: /models/glm53-family.md
  - type: cites
    target: /models/deepseek-v4-family.md
provenance:
  - source: https://github.com/0xSero/local-ai-registry
    note: Registry snapshot in the vault (commit c0604cff4807); registry/recipes/nvidia/dgx-spark-gb10-128gb/*.json, README.md, docs/design.md.
citations:
  - id: reg-readme
    text: "local-ai-registry, README.md (six checks, layout). https://github.com/0xSero/local-ai-registry"
  - id: reg-design
    text: "local-ai-registry, docs/design.md (proof kinds: lab, legacy, reported). https://github.com/0xSero/local-ai-registry/blob/main/docs/design.md"
  - id: reg-recipes
    text: "local-ai-registry, registry/recipes/nvidia/dgx-spark-gb10-128gb/ (46 recipe files). https://github.com/0xSero/local-ai-registry/tree/main/registry/recipes/nvidia/dgx-spark-gb10-128gb"
---

# Overview

The local-ai-registry ([local.sybilsolutions.ai](https://local.sybilsolutions.ai)) publishes one small JSON recipe per
model × GPU setup, each with a `proof` record: decode and prefill speed, which acceptance gates it passed, and whether
the figure was **measured by the registry's lab** or **reported** by the recipe's author [reg-recipes].

Its README says every recipe "passed six checks" — loads, chats, reasons, calls tools, holds its context window, decodes
at ≥ 15 tok/s [reg-readme]. The design document qualifies that: a recipe's latest proof either passed all six gates, **or**
is marked `legacy` (the older load-and-chat acceptance), **or** is `reported` with its source [reg-design].

# What the DGX Spark entries really are

Generated from the 46 recipe files for `dgx-spark-gb10-128gb` in the snapshot [reg-recipes]:

| Where the figure comes from | Recipes |
|---|---|
| Reported by MiaAI-Lab (the author of most of our [matrix](/models/spark-matrix.md)) | 33 |
| Reported by one other contributor (toncao) | 8 |
| Measured by the registry lab, all six gates | 3 |
| Measured by the registry lab, `legacy` acceptance | 2 |

**So this is not a second independent source**: 41 of 46 Spark figures are the recipe authors' own, mostly the same author
as the mia-ai.net catalog. The five lab rows are the independent data points:

| Lab-measured | Lab figure | Author's own figure for a comparable recipe |
|---|---|---|
| GLM 5.3 Flash · TensorFold · 4 Sparks · 1M | **109.7 tok/s**, prefill 2,094, six gates | 95.2 tok/s ([GLM 5.3 family](/models/glm53-family.md)) |
| DeepSeek V4.1 Flash · vLLM · 2 Sparks · 256k | **22.5 tok/s**, prefill 1,939, six gates | 31.6 tok/s on a different 585k EXL3 recipe ([DeepSeek V4 family](/models/deepseek-v4-family.md)) |
| Step 5 Preview · vLLM · 4 Sparks · 256k | 21.3 tok/s, prefill 888, six gates | — |
| GLM 5.3 Flash · SGLang · 2 Sparks · 256k | 30.7 tok/s, legacy | — |
| GLM 5.3 Flash · SGLang · 4 Sparks · 1M | 59.1 tok/s, legacy | — |

One lab figure is **above** the author's (GLM on TensorFold), one is **below** (DeepSeek on vLLM, though on a different
recipe and context). Neither direction is a rule: measure on your own workload.

# Models here that the matrix does not cover

Single Spark: **DeepSeek V4 Flash on one Spark** (45.5 tok/s, 375k context, MiaAI-Lab), Gemma 4 12B / 26B / 31B and
DiffusionGemma 26B (toncao), Ornith 1.5 35B, Qwen3.6 27B, Nemotron Labs 3 Puzzle 75B. Two Sparks: Inkling Small,
Step 3.7 Flash, MiMo V2.5, Leanstral 1.5 119B, Hy3. Three Sparks: GLM 5.2 (21–25.5 tok/s). All reported, none lab-measured.

The registry also lists a second GB10-class card, `rtx-spark-n1x-128gb`, with six recipes (Gemma 4, Qwen3.8 27B AWQ);
none of our other sources describe that product yet.

# All DGX Spark recipes

Decode = single-request tok/s as recorded in the proof; `n/p` = not published. Sorted by Sparks, then speed.

| Sparks | Model | Engine | Context | Decode tok/s | Prefill tok/s | Figure | Gates passed | Recipe |
|---|---|---|---|---|---|---|---|---|
| 1 | diffusiongemma-26b-a4b-it-awq-int4 | vllm | 256k | 101.4 | 462 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | qwen3.6-35b-a3b | vllm | 256k | 95.1 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Unsloth-Qwen3.6-35b-NVFP4-DGX-Spark) |
| 1 | ornith-1.5-35b-a3b | vllm | 256k | 86.3 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Ornith-1.5-35B-A3B-DGX-Spark) |
| 1 | ling-3.0-flash | sglang | 256k | 83 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark) |
| 1 | laguna-s-2.1 | vllm | 256k | 76.7 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Laguna-S-2.1-DGX-Spark-RTX-6000-PRO) |
| 1 | gemma-4-26b-a4b-it-awq-4bit | vllm | 256k | 63.2 | 412 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | diffusiongemma-26b-a4b | vllm | 256k | 55.8 | 463 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | qwen3.8-27b | sglang | 256k | 54.56 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark) |
| 1 | gemma-4-26b-a4b-it-awq-8bit | vllm | 256k | 49 | 401 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | qwen3.8-27b | exllamav3 | 256k | 47.5 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Qwen3.8-27B-DFlash2-EXL3-5.0bpw) |
| 1 | qwen3.6-27b | vllm | 256k | 45.6 | 1,083 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Qwen3.6-27B-NVFP4-DFlash-DGX-Spark) |
| 1 | deepseek-v4-flash | vllm | 375k | 45.5 | 625 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-One-DGX-Spark) |
| 1 | gemma-4-12b-it-awq-int4 | vllm | 128k | 43.1 | 843 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | muse-glimmer-30b | vllm | 256k | 35 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Muse-Glimmer-30B-DGX-Spark-RTX-5090-6000-PRO) |
| 1 | qwen3.8-27b-awq-bf16-int4 | vllm | 256k | 34.5 | 582 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | gemma-4-26b-a4b | vllm | 256k | 29.77 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Gemma-4-26B-A4B-DGX-Spark-18-concurrencies) |
| 1 | qwen3.8-27b-awq-fp8 | vllm | 256k | 29.7 | 562 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | gemma-4-31b-it-awq-4bit | vllm | 256k | 22.2 | 98 | reported | — | [toncao](https://github.com/toncao/local-ai-registry) |
| 1 | gemma-4-31b | vllm | 256k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Gemma-4-31B-IT-NVFP4-Recipe) |
| 1 | nemotron-3.5-lightning-30b-a3b | sglang | 1024k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Nemotron3.5-Lightning-DGX-Spark-RTX-5090-6000-PRO) |
| 1 | nemotron-labs-3-puzzle-75b-a9b | vllm | 256k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Nemotron-Labs-3-Puzzle-75B-DGX-Spark) |
| 1 | qwen3.8-27b | vllm | 976k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Qwen3.8-27B-DGX-Spark-RTX-6000) |
| 2 | mimo-v2.6-flash | sglang | 1024k | 69.8 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks) |
| 2 | deepseek-v4-flash | vllm | 1024k | 56 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark) |
| 2 | qwen3.8-flash-next | vllm | 256k | 54.4 | 2,962 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Qwen3.8-Flash-Next-Dual-DGX-Sparks) |
| 2 | inkling-small | sglang | 1024k | 33.9 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Inkling-Small-NVFP4-Dual-DGX-Sparks) |
| 2 | deepseek-v4.1-flash | vllm | 585k | 31.6 | 1,055 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks) |
| 2 | step-3.7-flash | vllm | 256k | 31.5 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Dual-DGX-Spark-Step-3.7-Flash-NVFP4) |
| 2 | glm-5.3-flash | sglang | 256k | 30.7 | n/p | **lab** | load, chat, reasoning, tools | registry lab |
| 2 | mimo-v2.5 | vllm | 976k | 30 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/MiMo-V2.5-vLLM-Dual-DGX-Sparks) |
| 2 | glm-5.3-flash | vllm | 256k | 26.5 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/GLM-5.3-Flash-NVFP4-Dual-DGX-Spark) |
| 2 | deepseek-v4.1-flash | vllm | 256k | 22.5 | 1,939 | **lab** | load, chat, reasoning, tools, context, speed | registry lab |
| 2 | leanstral-1.5-119b-a6b | vllm | 256k | 21.08 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Leanstral-1.5-119B-A6B_2x_DGX_Sparks_vLLM) |
| 2 | deepseek-v4-flash | vllm | 320k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-0731-vLLM-Dual-DGX-Sparks) |
| 2 | deepseek-v4-flash | vllm | 976k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-V4-Flash-Dual-DGX-Spark-1M-Context) |
| 2 | hy3 | vllm | 128k | n/p | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/Hy3-Dual-DGX-Spark) |
| 3 | deepseek-v4.1-flash | sglang | 256k | 51 | 2,000 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks) |
| 3 | deepseek-v4-flash | vllm | 1024k | 41.9 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark) |
| 3 | glm-5.2 | vllm | 229k | 25.5 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/GLM-5.2-NVFP4-AQLM-Triple-DGX-Sparks) |
| 3 | glm-5.2 | vllm | 340k | 21 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/GLM-5.2-NVFP4-AQLM-Triple-DGX-Sparks) |
| 3 | glm-5.2 | vllm | 372k | 21 | n/p | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/GLM-5.2-NVFP4-AQLM-Triple-DGX-Sparks) |
| 4 | glm-5.3-flash | tensorfold | 1024k | 109.7 | 2,094 | **lab** | load, chat, reasoning, tools, context, speed | registry lab |
| 4 | deepseek-v4.1-flash | sglang | 1024k | 87.7 | 5,925 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks) |
| 4 | glm-5.3-flash | sglang | 1024k | 59.1 | n/p | **lab** | load, chat, reasoning, tools | registry lab |
| 4 | glm-5.3-flash | vllm | 256k | 45 | 1,800 | reported | — | [MiaAI-Lab](https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless) |
| 4 | step-5-preview | vllm | 256k | 21.3 | 888 | **lab** | load, chat, reasoning, tools, context, speed | registry lab |

# Limitations

- Snapshot of the vault copy (commit c0604cff4807); the registry is re-rendered weekly and will have moved.
- `reported` figures inherit every caveat of their source — see the matrix's limitations and
  [Alex Ellis' real-use numbers](/field-reports/alex-ellis-four-sparks.md).
- A recipe filename's context (e.g. `1024k`) is the configured window, not a measured long-context speed.
