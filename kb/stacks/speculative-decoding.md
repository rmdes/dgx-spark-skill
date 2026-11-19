---
type: concept
title: Speculative decoding on Spark
description: How draft-and-verify decoding (MTP, EAGLE, DFlash2, DSpark, LiLiCorr, copy and n-gram drafts) multiplies per-stream speed on the bandwidth-bound GB10, what each drafter is, measured gains, when it hurts, and what "exact decoding" guarantees.
tags: [speculative-decoding, mtp, dflash2, dspark, lilicorr, eagle, exact-decoding, performance]
resource: /stacks/speculative-decoding.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [spec decode, drafting, draft model, MTP, DFlash2, DSpark, LiLiCorr]
entities:
  - label: MTP
    kind: speculative_decoder
  - label: DFlash2
    kind: speculative_decoder
  - label: DSpark
    kind: speculative_decoder
  - label: LiLiCorr
    kind: speculative_decoder
  - label: EAGLE-3
    kind: speculative_decoder
  - label: SPEED-Bench
    kind: benchmark
relations:
  - type: implemented_by
    target: /stacks/tensorfold.md
  - type: implemented_by
    target: /stacks/sglang.md
  - type: implemented_by
    target: /stacks/vllm.md
  - type: explains
    target: /models/qwen38-27b-1x-tensorfold.md
  - type: depends_on
    target: /hardware/gb10-platform.md
provenance:
  - source: https://huggingface.co/blog/nvidia/speed-bench
    note: NVIDIA SPEED-Bench — domain- and batch-dependence of acceptance and speedup (datacenter GPUs, not Spark).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: Independent GB10 measurements of DFlash2 and MTP under vLLM, alone and under concurrency.
  - source: https://mia-ai.net/models
    note: MiaAI-Lab recipe pages and repositories (self-reported measurements per drafter).
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/speculative-decoding/README.md
    note: NVIDIA's Spark playbook (EAGLE-3 and draft-target with TensorRT-LLM).
citations:
  - id: speed-bench
    text: "NVIDIA, Introducing SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding (2026-03-19). https://huggingface.co/blog/nvidia/speed-bench"
  - id: nv-spec
    text: "NVIDIA, DGX Spark playbook — Speculative Decoding (TensorRT-LLM). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/speculative-decoding/README.md"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric: vLLM on sm_121 (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: tf-readme
    text: "Ash Hart, TensorFold README, commit d33dcfc. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/README.md"
  - id: tf-zig
    text: "Ash Hart, TensorFold Zig engine preview. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/ZIG-PREVIEW.md"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek V4.1 Flash 1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: mia-fn2
    text: "MiaAI-Lab, Qwen3.8 Flash Next on two DGX Sparks with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold"
  - id: sgl-q27
    text: "MiaAI-Lab, Qwen3.8 27B on SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md"
  - id: sgl-ling
    text: "MiaAI-Lab, Ling-3.0-Flash SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark/blob/ca840cb8d032353e24648aeee06312b0938348f6/README.md"
  - id: sgl-mimo
    text: "MiaAI-Lab, MiMo-V2.6-Flash for 2x DGX Sparks (README). https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks/blob/201be3e743d215291feee09fe470822ec453c63d/README.md"
  - id: ds-vllm2
    text: "MiaAI-Lab, DeepSeek v4.1 Flash EXL3 2.9 bpw for 2x DGX Sparks (vLLM, README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks/blob/6f7d1590ad49a2b8995188e45d7b9db31e677452/README.md"
---

# Overview

A small **drafter** proposes several next tokens; the big model checks them all in one forward pass and keeps the
ones it would have produced itself [nv-spec]. On a GB10 decode is memory-bandwidth bound, and smaller weights plus
speculative decoding are what move per-stream speed (see [GB10 platform](/hardware/gb10-platform.md)): every
single-Spark recipe above 50 tok/s in the [Models × Sparks matrix](/models/spark-matrix.md) runs a drafter.

How much it helps depends on three things, all measured below:

1. **What the model is writing.** Code, math and edits are predictable; prose and roleplay are not [speed-bench].
2. **How many requests share the GPU.** As the batch grows, inference moves from memory-bound to compute-bound and
   wasted drafts start to cost real time [speed-bench] [cape-serve].
3. **Which drafter.** Native heads trained with the model generally accept more than post-trained ones [speed-bench].

# The drafters you will meet

| Drafter | What it is | Where on Spark |
|---|---|---|
| **MTP** (multi-token prediction) | A head trained with the model and shipped in the checkpoint; no extra download | Qwen3.8 Flash Next (TensorFold, vLLM), GLM-5.3-Flash on vLLM, Qwen 27B on SGLang [mia-fn2] [cape-serve] [sgl-q27] |
| **EAGLE / EAGLE-3** | Post-trained draft head on the target's hidden states | NVIDIA's TensorRT-LLM playbook; MiMo's "EAGLE MTP" (3-layer head in the checkpoint) [nv-spec] [sgl-mimo] |
| **DFlash / DFlash2** | A separate small block-diffusion draft model (z-lab) that drafts a whole block at once (7–8 tokens) | Qwen3.8 27B (TensorFold, SGLang), GLM-5.3-Flash (TensorFold, vLLM), MiMo [mia-q27] [mia-glmf] [sgl-mimo] |
| **DSpark** | DFlash extended with target-model auxiliary features and a confidence head, trained with SpecForge; Ling's is a 1.36B, 5-layer draft [sgl-ling] | Ling 3.0 Flash, Qwen 27B (SGLang); full GLM 5.3 (Red Hat AI speculator); DeepSeek V4.1 Flash, whose checkpoint carries its own DSpark draft blocks [sgl-ling] [mia-glm3] [mia-ds4] |
| **LiLiCorr** | NVIDIA's drafter for Nemotron 3.5 Bolt (~1.3 GB), 7 tokens per stream per round | Nemotron 3.5 Bolt on TensorFold's Zig engine [mia-bolt] |
| **Copy / n-gram** | Draft by copying spans already in the context or seen before | TensorFold copy drafts and `--recall` [tf-zig] [tf-readme]; SGLang NGRAM; TensorRT-LLM N-Gram [sgl-q27] [speed-bench] |

# Measured gains on GB10

Self-reported by recipe authors unless marked independent.

| Model, engine | Without / weaker drafter | With drafter | Gain |
|---|---|---|---|
| Ling 3.0 Flash, SGLang, 1 Spark | MTP (NEXTN) 37 tok/s ×1, 76 ×6 | DSpark 83 tok/s ×1, 136 ×6 | 2.2× / 1.8×; accepted length 5.2–6.4 [sgl-ling] |
| Qwen3.8 27B, SGLang, 1 Spark | EAGLE/MTP code 24.20, essay 18.19 tok/s | DFlash2 code 54.56, essay 25.61 tok/s | 2.25× / 1.41× [sgl-q27] |
| MiMo V2.6 Flash, SGLang, 2 Sparks | EAGLE MTP code 46.0, prose 35.0 | DFlash code 69.8, prose 25.8 | code +52 %, prose −26 % [sgl-mimo] |
| DeepSeek V4.1 Flash EXL3, vLLM, 2 Sparks | spec off 23 tok/s ×1 | DSpark 31.6 tok/s ×1 | +37 % alone; **off wins at ×4** (53.7 vs 42.8) [ds-vllm2] |
| GLM-5.3-Flash NVFP4, vLLM, 4 Sparks — **independent** | MTP-4: math 46.7, 6-stream 91.2 | DFlash2 K=7: math 69.2, 6-stream 48.5 | +48 % alone, **−47 % aggregate** [cape-serve] |

Code vs prose with drafting on (same server): Qwen3.8 27B on TensorFold 136.9 vs 58.3 tok/s [mia-q27]; DeepSeek
V4.1 Flash on 4 Sparks 117.4 vs 65.8 [mia-ds4]; full GLM 5.3 41.7 vs 31.3, with drafter acceptance 87 % on worked
arithmetic [mia-glm3].

# When it hurts

- **Under concurrency, long drafts are wasted.** Capetron's DFlash2 acceptance fell from 3.09 tokens alone to 1.97
  under six streams; their advice: use it "for a single-user coding or math endpoint, not a shared one"
  [cape-serve]. Longer is not better either: MTP-6 lost to MTP-4 (mean acceptance 3.64 of 6) [cape-serve].
- **Lightweight n-gram drafting can be a net slowdown** at moderate batch: 0.88× mean speedup for Llama 3.3 70B with
  N-Gram at batch 32, against 1.34× for GPT-OSS 120B with EAGLE3 and 1.20× for Qwen3-Next with MTP [speed-bench].
  On the 27B SGLang recipe NGRAM ran ~30 % under MTP [sgl-q27]. (SPEED-Bench numbers are from datacenter GPUs.)
- **Sampling lowers acceptance.** Full GLM 5.3 sampled at temperature 1.0 decodes 22.9–24.0 tok/s prose against
  31.3 greedy [mia-glm3]. The GLM-5.3-Flash recipe closed that gap by testing both ranks' candidates together:
  43.5 tok/s sampled vs 44.1 greedy [mia-glmf].
- **Benchmarks lie with random tokens:** with speculation on, random-token prompts overestimated throughput by ~23 %
  [speed-bench]. Measure with real prompts from your own workload.

# The "exact decoding" guarantee

TensorFold defines it strictly: "Every accepted draft must equal the token the same native engine would produce with
`"draft": false`"; resumed requests must equal fresh execution and concurrent streams must equal their solo runs
[tf-readme]. Recipes check it and publish the result, e.g. drafted, serial and concurrent replies identical
(`tools/exact.py`) on two Sparks [mia-fn2]; 12/12 exact on every measured boot of full GLM 5.3 [mia-glm3]; eight
greedy replies sent at once equal to the same replies sent one at a time on DeepSeek V4.1 Flash [mia-ds4]. Any
client can check it by sending `"draft": false` and comparing.

What it does **not** promise:

- It is exact relative to the same checkpoint, backend, settings and runtime. "Different quantizations and different
  backends can produce different outputs" [tf-readme]. A 4-bit model with an FP8 KV cache is still lossy against
  BF16, drafts or not.
- For vLLM and SGLang, SPEED-Bench describes speculative decoding as preserving "the exact output distribution of the
  target model" [speed-bench]; a byte-for-byte drafted-vs-serial check on Spark is **not published** in the vLLM and
  SGLang recipe sources we collected.

# Limitations

- Drafter choice is per boot on SGLang (no per-request switch) [sgl-mimo]; on TensorFold a request can turn drafts off
  but not change drafter [tf-readme].
- Drafters cost memory: MiMo's DFlash keeps a second KV pool, shrinking the pool from 2,878,144 to 1,664,704 tokens
  [sgl-mimo]; DeepSeek's DSpark costs ~3.5 GiB [ds-vllm2].
- Licences differ from the target model's: the BF16 DFlash2 checkpoint used by SparkRing's GLM-5.3 profiles is
  CC BY-NC-ND 4.0 (see [SparkRing and SparkCache](/stacks/sparkring-sparkcache.md)).
