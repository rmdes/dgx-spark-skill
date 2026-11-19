---
type: concept
title: Quantization formats on GB10
description: NVFP4, MXFP4, FP8, INT4-AutoRound, MLX 4-bit and EXL3 compared for the DGX Spark — what each stores, the published quality numbers (KL, perplexity, GPQA, task scores) and the measured speed trade-offs on GB10.
tags: [quantization, nvfp4, mxfp4, fp8, int4, autoround, mlx, exl3, kv-cache, quality]
resource: /stacks/quantization-formats.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [NVFP4, MXFP4, FP8, INT4-AutoRound, MLX 4-bit, EXL3 bpw, quants]
entities:
  - label: NVFP4
    kind: quantization_format
  - label: MXFP4
    kind: quantization_format
  - label: FP8 (E4M3)
    kind: quantization_format
  - label: INT4-AutoRound
    kind: quantization_format
  - label: MLX affine 4-bit
    kind: quantization_format
  - label: EXL3
    kind: quantization_format
relations:
  - type: generalizes
    target: /stacks/exl3-exllamav3.md
  - type: read_by
    target: /stacks/tensorfold.md
  - type: read_by
    target: /stacks/vllm.md
  - type: read_by
    target: /stacks/sglang.md
  - type: depends_on
    target: /hardware/gb10-platform.md
  - type: affects
    target: /models/qwen38-flash-next.md
provenance:
  - source: https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/
    note: NVIDIA's definition of NVFP4 vs MXFP4 and its FP8-to-NVFP4 accuracy claim (vendor data).
  - source: https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/quantization.md
    note: TensorFold's GB10 measurement of NVFP4 checkpoint math vs bf16 activations (KL, top-1, prefill, decode).
  - source: https://mia-ai.net/models
    note: MiaAI-Lab recipe pages — measured quality/speed trade-offs per checkpoint on DGX Spark (self-reported).
citations:
  - id: nvfp4-blog
    text: "Eduardo Alvarez (NVIDIA), Introducing NVFP4 for Efficient and Accurate Low-Precision Inference (2025-06-24). https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/"
  - id: tf-quant
    text: "Ash Hart, TensorFold docs — Quantized checkpoints. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/quantization.md"
  - id: tf-readme
    text: "Ash Hart, TensorFold README, commit d33dcfc. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/README.md"
  - id: tf-exl3
    text: "Ash Hart, TensorFold docs — EXL3 weights. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/recipes/exl3.md"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: mia-fn1
    text: "MiaAI-Lab, Qwen3.8 Flash Next on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold"
  - id: mia-fn2
    text: "MiaAI-Lab, Qwen3.8 Flash Next on two DGX Sparks with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek V4.1 Flash 1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: sgl-mimo
    text: "MiaAI-Lab, MiMo-V2.6-Flash for 2x DGX Sparks (README). https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks/blob/201be3e743d215291feee09fe470822ec453c63d/README.md"
  - id: glm1x
    text: "0xSero, GLM-5.3 Flash EXL3 on 1× DGX Spark — native MTP serving (README). https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark/blob/6ff8595aa271f2eac49579fbf5e90cde9e90674e/README.md"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric: vLLM on sm_121 (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: nv-vllm
    text: "NVIDIA, DGX Spark playbook — vLLM for Inference. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/vllm/README.md"
---

# Overview

On a DGX Spark every model is quantized in practice: 128 GB of unified memory and 273 GB/s of bandwidth make bytes per
weight the main lever on both "does it fit" and "how fast does it decode" (see
[GB10 platform](/hardware/gb10-platform.md)). The GB10 is a Blackwell part with FP4 tensor cores, but the fastest
published Spark recipes do not all use NVIDIA's own FP4 format; several use MLX 4-bit, INT4 or EXL3.

Rule of thumb from the sources: **4-bit weights are the default, the checkpoint's calibration matters as much as the
format, and the KV cache and prompt precision are separate quality knobs.**

# The formats

| Format | What is stored | Bits / weight | Notes |
|---|---|---|---|
| **NVFP4** | E2M1 values + one **FP8 E4M3 scale per 16 values** + one FP32 scale per tensor | 4.5 [nvfp4-blog] | Blackwell hardware scaling; ~3.5× smaller than FP16, ~1.8× smaller than FP8 [nvfp4-blog] |
| **MXFP4** | E2M1 values + one **power-of-two (E8M0) scale per 32 values** | 4 + one shared scale per 32 | Open MX standard; coarser scaling than NVFP4 [nvfp4-blog]. GPT-OSS ships in it [nv-vllm]; MiMo's experts use it (U8 nibble pairs + E8M0 block-32 scales) [sgl-mimo] |
| **FP8 (E4M3)** | 8-bit float, block or per-tensor scales | 8 | Common for attention/dense layers in mixed checkpoints [tf-readme] and for the **KV cache** [mia-q27] |
| **INT4-AutoRound** | Intel AutoRound int4, GPTQ int4 experts [mia-fn1] | 4 + group scales | The Flash Next INT4-AR checkpoint also cuts routed experts from 10 to 5 per token [mia-fn1] |
| **MLX affine 4-bit** | int4 codes + scale and bias per group of 32/64/128 | 4 + group scale and bias | Apple's MLX format; TensorFold reads affine 2/3/4/5/6/8-bit on CUDA too [tf-quant] |
| **EXL3** | ExLlamaV3 trellis codes with a codebook, **per-tensor widths** | fractional (2.0–4.0 on Spark) | See [EXL3 and ExLlamaV3](/stacks/exl3-exllamav3.md) [tf-exl3] |

Real checkpoints mix formats. NVIDIA's GLM-5.3-Flash **FP4-Local** stores routed experts in NVFP4 with compressed
block scales and most of the rest in MXFP8 and 128×128-block FP8 [tf-readme]. Nemotron 3.5 Bolt's 24 GB pack uses
IQ2_XXS experts, NVFP4 Mamba projections and Q8_0 attention [mia-bolt].

# Quality numbers published

Each row names who measured it. Vendor and recipe-author numbers are self-reported.

| Comparison | Metric | Result | Source |
|---|---|---|---|
| DeepSeek-R1-0528, FP8 → NVFP4 (PTQ) | 7 evals | ≤ 1 % degradation; AIME 2024 +2 % | NVIDIA [nvfp4-blog] |
| Qwen3.8 Flash Next, NVIDIA FP4 QAD vs bf16 | GPQA Diamond / ToolEvalBench | 91.5 % / 88.7 % vs 92.2 % / 89.4 % | NVIDIA model card, quoted by recipe, not re-measured [mia-fn1] |
| Qwen3.8 Flash Next, INT4-AutoRound (top-5 experts) vs original | general capability (authors' harness) | 46.6–47.6 vs 51.8 (~10 % lower); tool use unchanged | checkpoint authors [mia-fn2] |
| GLM-5.3-Flash at TP=2, vs BF16 | NLL above BF16 | NVFP4 1.37 %, FP4-Local 1.11 %, XSFP4 0.85 % | contributor receipt, quoted in TensorFold README [tf-readme] |
| GLM-5.3-Flash XSFP4 vs FP4-Local | top-1 agreement / KL bound | 93.26 % / 0.0431 vs 92.82 % / 0.0510 | same [tf-readme] |
| GLM-5.3-Flash EXL3 4 bpw, MiaAI calibration vs TR3 | KL to Z.AI's FP8 release (wiki / workload) | 0.0903 / 0.3150 vs 0.0990 / 0.3271 | recipe author [mia-glmf] |
| Nemotron 3.5 Super VL NVFP4 on GB10: FP4 activations (`checkpoint`) vs bf16 activations (`full`) | KL / top-1 / NLL | 0.0077 nats / 98.4 % / +0.0058 | TensorFold [tf-quant] |
| Qwen3.8 27B, FP8 KV cache only vs all-bf16 | perplexity / KL / top-1 | 3.315 vs 3.316 / 0.0031 / 98.7 % | recipe author [mia-q27] |
| Qwen3.8 27B, FP8 prompts (prefill) vs bf16 | perplexity / KL / top-1 | 3.397 / 0.0435 / 94.1 % | recipe author [mia-q27] |
| Qwen3.8 Flash Next, FP8 KV vs bf16 KV | top-1 agreement | 98.8 % | recipe author [mia-fn2] |
| Full GLM 5.3, FP4 KV vs FP8 KV | paired task suite (McNemar) | no measurable difference (e.g. 124/150 vs 123/150, p = 1.00) | recipe author [mia-glm3] |

Takeaway from the 27B rows: an **FP8 KV cache is almost free in quality**; FP8 *prompt* processing costs about 14× as much KL
(0.0435 vs 0.0031) [mia-q27].

# Speed trade-offs measured on GB10

| Choice | Measured effect | Source |
|---|---|---|
| MLX 4-bit vs NVIDIA NVFP4, Qwen3.8 27B on TensorFold | NVFP4 prefilled the same but **decoded 20–25 % slower** (and cannot take images); quality between the two not measured | [mia-q27] |
| INT4-AR vs NVIDIA FP4 QAD, Flash Next, 1 Spark | 64.4 vs 55.6 tok/s single stream; needs ~93 vs ~108 GiB free at start | [mia-fn1] |
| INT4-AR vs NVFP4, Flash Next, 2 Sparks | 89.3 vs 67.4 tok/s single; 483.6 vs 390.1 ×16 | [mia-fn2] |
| NVFP4 checkpoint math vs bf16 activations, Super VL on GB10 | prefill **1.81× faster** (8,192-token prompt 4.41 s vs 7.96 s); decode 52.3 vs 50.1 ms/token (slightly slower) | [tf-quant] |
| FP8 prompts on (27B) | +52 % prefill in the recipe's test; decode unaffected | [mia-q27] |
| FP8 KV cache | twice the tokens per GiB (27B: 32 vs 64 KiB/token) at the same speed | [mia-q27] |
| EXL3 2.0 bpw vs 3.05 bpw mosaic, GLM-5.3-Flash, 1 Spark | 18.7–19.2 vs ~9–10 tok/s (the mosaic's codebook cannot use MTP on that runtime) | [glm1x] |
| Serving DeepSeek V4.1 Flash as published (FP8 + MXFP4, ~510 GB) | needs 4 Sparks; 65.8 tok/s single stream | [mia-ds4] |

Why bits matter on a bandwidth-bound box: Bolt reads about 5 GB per token at one request with its
~2-bit experts, not the 14.6 GB of an fp16 expansion [mia-bolt].

# Limitations

- **Format support is per engine and per kernel.** NVFP4 MoE kernels refused Qwen3.8 Flash Next at TP4 because the
  sliced intermediate size (160) is below their alignment; expert parallel was the workaround [cape-serve]. MXFP4 on
  MiMo needs a recent SGLang; older engines expanded experts to FP8 and took the node down [sgl-mimo]. TensorFold's
  native engine refuses formats it has no reader for (GGUF, AWQ, GPTQ and others need their own kernels) [tf-quant].
- **"Same format" is not "same quality":** two 4 bpw EXL3 quants of the same size differ in KL [mia-glmf]; INT4-AR's
  quality loss comes partly from cutting experts, not only from int4 [mia-fn1].
- Most quality numbers here are short-context (the 27B KL used 4k-token sequences; long context was checked with
  needles only) [mia-q27]. Benchmark gaps of a few problems are noise, as the GLM author notes [mia-glmf].
- NVIDIA's NVFP4 accuracy claim is on DeepSeek-R1 in a datacenter setting, not measured on Spark [nvfp4-blog].
