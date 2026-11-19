---
type: model
title: DeepSeek V4 Flash family on DGX Spark
description: Every published DGX Spark recipe for DeepSeek V4 Flash, V4.1 Flash and V4.1 Flash 1017 — one to four Sparks, engine, measured speed, context, quality checks and licences.
tags: [models, deepseek, moe, tensorfold, vllm, sglang, multi-node, dspark]
resource: /models/deepseek-v4-family.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [DeepSeek V4 Flash, DeepSeek-V4.1-Flash, DeepSeek-V4.1-Flash-1017, DeepSeek-V4-Flash-0731, DSv4 Flash]
entities:
  - label: DeepSeek-V4.1-Flash-1017
    kind: model
  - label: DeepSeek-V4-Flash-0731
    kind: model
  - label: DSpark
    kind: speculative_decoder
  - label: TensorFold
    kind: inference_engine
  - label: vLLM
    kind: inference_engine
  - label: SGLang
    kind: inference_engine
  - label: SparkInfer
    kind: inference_engine
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
    target: /stacks/sparkring-sparkcache.md
  - type: uses
    target: /stacks/speculative-decoding.md
  - type: related_to
    target: /models/glm53-family.md
provenance:
  - source: https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold
    note: MiaAI-Lab recipe page, 4-Spark TensorFold switchless ring, measured 2026-10-25.
  - source: https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks
    note: 2-Spark TensorFold recipe on the EAQ 2.9-bit EXL3 quant (README at d8e5b28).
  - source: https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks
    note: 2-Spark vLLM recipe on the EXL3 2.9 bpw quant (README at 6f7d159).
  - source: https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark
    note: 2- and 3-Spark vLLM DSpark recipe for V4 Flash 0731 / Vision-Exp (README, results, TP3 doc at a8b4636).
  - source: https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks
    note: 3- and 4-Spark SGLang recipe for V4.1 Flash 1017 (README, tp4 and switchless-ring docs at 64b02de).
  - source: https://github.com/MiaAI-Lab/sparkring
    note: Sparkring DeepSeek quickstart and normalized TP2/TP4 benchmark records (at b9cd552).
  - source: https://github.com/0xSero/deepseek-v4-flash-0731-spark-sparkinfer
    note: Single-Spark SparkInfer recipe on a REAP-pruned EXL3 checkpoint (at d370c0f).
citations:
  - id: mia-ds4x
    text: "MiaAI-Lab, DeepSeek V4.1 Flash on four DGX Sparks, with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: ds-tf2x
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 EXL3 on 2x DGX Sparks with TensorFold, README. https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/blob/d8e5b28da6ebcf539035be564a4a94d087b2f480/README.md"
  - id: ds-exl3-vllm
    text: "MiaAI-Lab, DeepSeek v4.1 Flash EXL3 2.9 bpw for 2x DGX Sparks, README. https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks/blob/6f7d1590ad49a2b8995188e45d7b9db31e677452/README.md"
  - id: ds-dspark
    text: "MiaAI-Lab, DeepSeek V4 Flash Vision-Exp DSpark on 2x DGX Spark, README. https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark/blob/a8b4636710068fd30edb98e1365d567086cc208e/README.md"
  - id: ds-dspark-results
    text: "MiaAI-Lab, DeepSeek V4 Flash DSpark — Results 2026-08-14. https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark/blob/a8b4636710068fd30edb98e1365d567086cc208e/results/RESULTS-2026-08-14.md"
  - id: ds-dspark-tp3
    text: "MiaAI-Lab, DeepSeek V4 Flash DSpark — Optional: 3x DGX Spark (TP=3). https://github.com/MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark/blob/a8b4636710068fd30edb98e1365d567086cc208e/docs/TP3.md"
  - id: ds-sglang
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash on 3x and 4x NVIDIA DGX Sparks, README. https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks/blob/64b02dea8681fb1d8e3a659ea432a8e9e9ba3995/README.md"
  - id: ds-sglang-tp4
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash TP4 production line (docs/tp4.md). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks/blob/64b02dea8681fb1d8e3a659ea432a8e9e9ba3995/docs/tp4.md"
  - id: ds-sglang-ring
    text: "MiaAI-Lab, TP4 switchless-ring serving numbers (4x DGX Spark). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks/blob/64b02dea8681fb1d8e3a659ea432a8e9e9ba3995/docs/tp4-switchless-ring-results.md"
  - id: sr-quick
    text: "Sparkring, DeepSeek-V4-Flash-0731 Spark quickstart. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/DEEPSEEK_V4_FLASH_QUICKSTART.md"
  - id: sr-readme
    text: "Sparkring README (Apache-2.0). https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/README.md"
  - id: sr-tp2
    text: "Sparkring, DeepSeek-V4-Flash DSpark package — two Sparks, TP2/DCP1 (2026-08-23). https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/performance/records/deepseek-v4-flash/normalized-tp2-base-temp1-n5-20260823.md"
  - id: sr-tp4
    text: "Sparkring, DeepSeek-V4-Flash-0731 — four Sparks, TP4/DCP1 (2026-08-23). https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/performance/records/deepseek-v4-flash/normalized-tp4-base-temp1-n5-20260823.md"
  - id: sero-1x
    text: "0xSero, DeepSeek V4 Flash on one DGX Spark (SparkInfer), README. https://github.com/0xSero/deepseek-v4-flash-0731-spark-sparkinfer/blob/d370c0f0806a9ac994dc5f354715576cc23840b9/README.md"
  - id: sero-1x-val
    text: "0xSero, DeepSeek V4 Flash on one DGX Spark — Validation evidence. https://github.com/0xSero/deepseek-v4-flash-0731-spark-sparkinfer/blob/d370c0f0806a9ac994dc5f354715576cc23840b9/VALIDATION.md"
---

# Overview

DeepSeek's V4 Flash line is the largest model family with complete DGX Spark recipes, from one Spark
(pruned) to four (unquantized). Three generations appear in the recipes:

| Checkpoint | Size as published | Notes |
|---|---|---|
| V4 Flash 0731 / Vision-Exp / DSpark preview | 48 FP8 shards, ~167 GB [sr-quick] | Native DSpark draft blocks; Vision-Exp adds an image tower, no video encoder [ds-dspark] |
| V4.1 Flash 1017 (FP8 + MXFP4) | ~510 GB on disk [mia-ds4x]; 476 GiB, of which 189 GiB are the two Engram n-gram tables [ds-sglang] | Engram tables can live on NVMe; ~305 GiB stays GPU-resident [ds-sglang] |
| V4.1 Flash 1017, EXL3 2.9 bpw (Mia EAQ v1) | 196 GiB plus ~203 GB of unquantized Engram tables [ds-tf2x] | Routed experts at 3 bits (2 bits in layers 18–22) [ds-tf2x] |

All figures on this page are **self-reported by the recipe authors** on their own hardware. No independent
source (Capetron) has measured this family; see [Models × Sparks matrix](/models/spark-matrix.md) for the
cross-family view.

# Recipes

| Sparks | Recipe | Engine · weights | 1-stream decode | Peak aggregate | Prefill | Context |
|---|---|---|---|---|---|---|
| 1 | 0xSero sparkinfer [sero-1x] | vLLM + SparkInfer · REAP-pruned EXL3 of 0731, K64 DSpark draft | 38.12 tok/s code (median of 5; min 34.30) | n/p (4 sequences) | 1,055 tok/s at 252k (tuning run) | 262k |
| 2 | V4 Flash DSpark [ds-dspark-tp3] | vLLM TP2 · official Vision-Exp FP8, DSpark | 38.6 tok/s prose (2026-09-02) | 139 ×6 [ds-dspark] | TTFT 18.0 s at 32k | 1M ceiling |
| 2 | V4.1 Flash EXL3 [ds-exl3-vllm] | vLLM TP2 · EXL3 2.9 bpw, DSpark k=3 | 31.6 tok/s prose | 53.7 ×4 with speculation off | 1,054.7 tok/s at 32k | 600k |
| 2 | V4.1 Flash 1017 TensorFold [ds-tf2x] | TensorFold Zig TP2 · EXL3 2.9 bpw, DSpark | 74.9 prose / 109.9 code | 130.0 ×4 prose | 2,175 tok/s at 32k | 1M (512k practical, see Limitations) |
| 2 | Sparkring pair [sr-tp2] | vLLM TP2 · DeepSeek-V4-Flash-DSpark package, DSpark K5 | 58.36 tok/s at 16k (T=1) | 307.13 ×32 at 16k | 1,926 tok/s at 16k | 1M |
| 3 | V4 Flash DSpark TP3 [ds-dspark-tp3] | vLLM TP3 · same as 2-Spark lane | 41.9 tok/s | 198.0 ×16 | TTFT 18.6 s at 32k | 1M ceiling |
| 3 | V4.1 Flash 1017 SGLang [ds-sglang] | SGLang TP3 · native MXFP4 experts + FP8 dense, Engram on NVMe | 51.0 tok/s prose | 85.4 ×4 | ~2,000 tok/s | 256k configured |
| 4 | V4.1 Flash 1017 SGLang TP4 [ds-sglang-tp4] | SGLang TP4 (switched fabric) · MXFP4 + FP8 | 87.7 prose / 124.8 code | 342.7 ×16 prose | 4.8k–5.0k tok/s on real text | 1M |
| 4 | V4.1 Flash 1017 TensorFold [mia-ds4x] | TensorFold Zig TP4, switchless ring · FP8 + MXFP4 as published | 65.8 prose / 117.4 code | 165.3 ×8 prose | 4,127 tok/s at 32k | 1M, 16 streams |
| 4 | Sparkring cycle [sr-tp4] | vLLM TP4, cabled ring · official 0731 FP8, DSpark K5 | 68.84 tok/s at 16k (89.98–105.88 at other lengths) | 508.11 ×32 at 16k | 2,488 tok/s at 16k | 1M |

Measurement methods differ between rows (sparkDash, the recipes' own bench scripts, llm_decode_bench;
greedy vs T=0.7 vs T=1.0). Compare rows only as an order of magnitude.

## Notes per recipe

- **2-Spark vLLM DSpark:** the same lane measured 62–83 tok/s single-stream and 160–190 aggregate for six
  short chats on 2026-08-14; the author says decode on 2026-09-02 was 15–25 % lower with no setting to blame,
  and to treat the August numbers as "the best seen, not the norm" [ds-dspark]. Six simultaneous cold
  32k–128k prompts fall to a ~8 tok/s decode floor while prefills run [ds-dspark-results].
- **3-Spark vLLM TP3:** buys capacity (16 slots, three times the KV) and +4–13 % decode, but prefill is
  22–23 % slower at 128k–256k. "Single-user long-context work is better served by the 2-node lane" [ds-dspark-tp3].
- **2-Spark vLLM EXL3:** an optional cooperative-MoE extension raises single-stream decode from 31.45 to
  40.23 tok/s (not bit-exact with stock) [ds-exl3-vllm].
- **4-Spark SGLang on a switchless ring:** an independent reproduction on Carlos's ring (k=5, 8 slots) measured
  74.03 tok/s aggregate at C1 and 224.84 at C8 on code, with no A/B against a switch [ds-sglang-ring].
- **4-Spark TensorFold:** a switch removes the ring's one relayed hop; the published numbers are the ring's
  [mia-ds4x]. Each Spark holds ~80 GiB of weights; spark1 needs ~510 GB + ~320 GB of disk [mia-ds4x].
- **Sparkring:** the profiles are "not qualified for general use or for 1,048,576-token output quality"; the
  TP2 and TP4 runs used different checkpoint packages, so they do not isolate topology scaling [sr-quick].

# Which recipe for what

| Need | Recipe | Why |
|---|---|---|
| One Spark only | 0xSero sparkinfer | The only 1-Spark option, and it serves a REAP-pruned checkpoint, not the full model; its 35 tok/s decode gate is still open [sero-1x] |
| Single developer, two Sparks (the demo setup) | V4.1 Flash 1017 TensorFold 2x | Highest single-stream speed on two (74.9 prose, 109.9 code) with the 1M window [ds-tf2x] |
| Team, many concurrent sessions | SGLang TP4 or Sparkring TP4 | 342.7 tok/s at 16 streams [ds-sglang-tp4]; up to 508 at 32 streams [sr-tp4] (Sparkring unqualified) |
| Longest context | TensorFold 4x | 16 streams that can each hold the full 1M window; 45/45 needles to 997,530 tokens [mia-ds4x] |
| Unquantized weights | TensorFold 4x or SGLang 3x/4x | Serve DeepSeek's FP8/MXFP4 checkpoint without re-quantization [mia-ds4x] [ds-sglang] |

# Quality evidence

- **4x TensorFold (unquantized):** `tools/validate.py` passes (text, thinking, tool call, image, video,
  concurrent replies equal serial ones); needle 45 of 45 cells, 4k to 997,530 tokens [mia-ds4x].
- **4x SGLang TP4:** 72 of 75 on the recipe's auto-scored `qeval.py` suite; the three misses fail identically
  on the stock profile; 1,011,084-token needle passed [ds-sglang-tp4].
- **2x TensorFold, EXL3 2.9 bpw:** the quant's model card has **no perplexity or KL measurement** against the
  unquantized model [ds-tf2x]. Needle 3 of 3 at a 479,012-token prompt [ds-tf2x].
- **1x sparkinfer:** functional gates only (arithmetic, JSON schema, tool call, 500–20,000-character coherence);
  the checkpoint is REAP-pruned and a true NVFP4 KV path produced corrupted text and is disabled [sero-1x-val].
- Speculative decoding (DSpark) is exact in the TensorFold recipes: drafted replies equal undrafted ones [mia-ds4x].

# Licences

| Item | Licence |
|---|---|
| DeepSeek V4.1 Flash / 1017 weights | MIT (DeepSeek) [mia-ds4x] [ds-exl3-vllm] |
| Mia EAQ 2.9-bit quantization | MIT [ds-tf2x] |
| V4 Flash 0731 / Vision-Exp weights | "own terms"; not named in the recipe [ds-dspark] |
| TensorFold recipes (2x, 4x) | Apache-2.0 [ds-tf2x] [mia-ds4x] |
| vLLM EXL3 2x recipe | AGPL-3.0 (some files MIT) [ds-exl3-vllm] |
| SGLang 3x/4x recipe | AGPL-3.0-or-later [ds-sglang] |
| Sparkring, sparkinfer recipe | Apache-2.0 [sr-readme] [sero-1x] |
| Optional abliteration overlays (`ABLIT=1`) | Gated on Hugging Face, separate terms [mia-ds4x] |

# Limitations

- **Memory is the ceiling on two Sparks.** The 2x TensorFold recipe needs 112 GiB available on each Spark; a
  head that also runs a desktop (~6 GiB) is limited to a 512k window in practice, and a reported 655k run had
  rank 0 killed by the memory guard [ds-tf2x].
- The 2x TensorFold recipe reads ~203 GB of Engram tables at runtime; reading them over NFS instead of local
  disk dropped prefill to ~690–890 tok/s [ds-tf2x].
- Disable `earlyoom` on both hosts for the vLLM DSpark lane, or it can kill vLLM under deep-context load [ds-dspark].
- Recipes change several times a week; versions are pinned in the citations above.
