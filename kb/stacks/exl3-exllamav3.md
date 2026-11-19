---
type: component
title: EXL3 and ExLlamaV3 on Spark
description: ExLlamaV3's EXL3 trellis quantization (fractional bits per weight, mcg/mul1 codebooks) and the three ways it is served on DGX Spark — vLLM overlays, SparkRing's exl3-r7 runtime, and TensorFold.
tags: [exl3, exllamav3, quantization, bpw, vllm, tensorfold, glm, deepseek]
resource: /stacks/exl3-exllamav3.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [EXL3, ExLlamaV3, trellis quantization, exl3-r7]
entities:
  - label: EXL3
    kind: quantization_format
  - label: ExLlamaV3
    kind: library
  - label: exl3-r7
    kind: runtime_image
relations:
  - type: is_a
    target: /stacks/quantization-formats.md
  - type: served_by
    target: /stacks/vllm.md
  - type: served_by
    target: /stacks/tensorfold.md
  - type: served_by
    target: /stacks/sparkring-sparkcache.md
  - type: runs_on
    target: /hardware/gb10-platform.md
provenance:
  - source: https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/recipes/exl3.md
    note: Format description (tiles, codebooks, per-tensor widths) and TensorFold support status.
  - source: https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/runtime/exl3-r7/README.md
    note: SparkRing's ARM64/SM121 builder combining vLLM, B12X, ExLlamaV3, InstantTensor and SIRCL.
  - source: https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark/blob/6ff8595aa271f2eac49579fbf5e90cde9e90674e/README.md
    note: GLM-5.3-Flash at 2.0 bpw on ONE Spark (vLLM + native MTP), receipted measurements.
  - source: https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold
    note: MiaAI-Lab's own 4 bpw EXL3 quant with KL measured against Z.AI's FP8 release.
citations:
  - id: tf-exl3
    text: "Ash Hart, TensorFold docs — EXL3 weights. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/recipes/exl3.md"
  - id: tf-readme
    text: "Ash Hart, TensorFold README, commit d33dcfc. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/README.md"
  - id: sr-exl3r7
    text: "SparkRing, GLM-5.2 EXL3 3.5-bpw ARM64 builder (runtime/exl3-r7). https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/runtime/exl3-r7/README.md"
  - id: sr-readme
    text: "SparkRing README, commit b9cd552. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/README.md"
  - id: glm1x
    text: "0xSero, GLM-5.3 Flash EXL3 on 1× DGX Spark — native MTP serving (README). https://github.com/0xSero/GLM-5.3-Flash-EXL3-1x-DGX-Spark/blob/6ff8595aa271f2eac49579fbf5e90cde9e90674e/README.md"
  - id: glm-vllm2
    text: "MiaAI-Lab, GLM-5.3 Flash EXL3 on DGX Spark (vLLM, README). https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks/blob/a8cc40ddef876f033e0f1b4d8f178b0fee2a5351/README.md"
  - id: ds-vllm2
    text: "MiaAI-Lab, DeepSeek v4.1 Flash EXL3 2.9 bpw for 2x DGX Sparks (vLLM, README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks/blob/6f7d1590ad49a2b8995188e45d7b9db31e677452/README.md"
  - id: ds-tf2
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 EXL3 on 2x DGX Sparks with TensorFold (README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/blob/d8e5b28da6ebcf539035be564a4a94d087b2f480/README.md"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
---

# Overview

EXL3 is ExLlamaV3's **trellis quantization**, and it is what "many of the community's best low-bit NVIDIA
checkpoints ship as" [tf-exl3]. For DGX Spark it matters because it reaches **fractional and mixed bit widths**
(2.0, 2.75, 2.9, 3.5, 4 bpw), which is how 300B-class and larger MoE models (GLM-5.3-Flash is 320B-A18B [glm1x])
are squeezed onto one to four 128 GB boxes.

How it works, in short [tf-exl3]:

- A quantized linear layer is a `trellis` int16 tensor plus sign/scale vectors (`suh`, `svh`), stored in tiles of
  256 values read as a circular bitstream; a **codebook** maps each 16-bit state to an fp16 value.
- Codebook markers: `mcg` (used at 4 bits for GLM-5.3-Flash) and `mul1` (2–6 bits for MiMo-V2.6-Flash, Qwen3.8-27B,
  Flash Next); no marker means the original `3inst`.
- Widths are **per tensor**: one checkpoint mixes widths across layers, projections and the experts of one MoE layer.
  `config.json`'s `bits` is only the average. Example, DeepSeek V4.1 Flash at 2.9 bpw: routed experts 3 bits (2 on
  layers 18–22), shared experts 4–5, attention 5, `lm_head` 6, indexer 8 [ds-vllm2].

Codebook matters operationally: a `mul1` checkpoint cannot run on runtimes that only accept `mcg` [glm1x].

# Three serving paths on Spark

| Path | What it is | Used by |
|---|---|---|
| **vLLM + ExLlamaV3 overlay** | EXL3 kernels layered onto a vLLM image built for `sm_121a` | GLM-5.3-Flash 1 Spark (0xSero) [glm1x]; GLM-5.3-Flash 2–4 Sparks [glm-vllm2]; DeepSeek V4.1 Flash 2 Sparks [ds-vllm2] |
| **SparkRing `exl3-r7` runtime** | ARM64/SM121 image built from pinned sources: vLLM, B12X, ExLlamaV3, InstantTensor, SIRCL; ExLlamaV3 patched to disable x86-only CPU collectives on ARM64 [sr-exl3r7] | GLM-5.2 EXL3 3.5 bpw and Qwen3.8-27B EXL3 K5/K6 profiles [sr-readme] |
| **TensorFold** | Python engine 0.3.6–0.6.6 served EXL3 on CUDA (every codebook, widths 1–8) [tf-exl3]; native Zig support is partial | GLM 5.3 Flash 4 bpw (v0.6.0 + patches) [mia-glmf]; full GLM 5.3 2.75 bpw [mia-glm3]; DeepSeek V4.1 Flash 1017 2.9 bpw (contributor's Zig fork) [ds-tf2] |

**Source conflict inside TensorFold's docs (same commit):** the EXL3 page says "No model serves an EXL3 checkpoint in
this release" of the native engine [tf-exl3]; the README model table lists GLM-5.3-Flash EXL3/TR3 on two CUDA ranks
as an experimental native path [tf-readme]. The Spark recipes sidestep this by pinning their own TensorFold build.

# Measured

Self-reported by recipe authors; settings differ per row.

| Model, bpw | Sparks | Engine | 1 stream | Prefill | Notes |
|---|---|---|---|---|---|
| GLM-5.3-Flash, 2.0 bpw `mcg` | 1 | vLLM + MTP depth 2 | 18.94 tok/s at 4k, 18.75 at 131k | 570.5 tok/s at 4k | sampling on; 727,449-token KV pool; ~102 GiB engine load [glm1x] |
| GLM-5.3-Flash, 4 bpw | 2 | vLLM + DFlash2 | prose 36.1, code 54.6 tok/s | n/p | temperature 0, thinking off [glm-vllm2] |
| GLM-5.3-Flash, 4 bpw | 2 | TensorFold + DFlash2 | prose 60.4 tok/s | 1,979 tok/s at 32k | [mia-glmf] |
| GLM 5.3 full, 2.75 bpw (~273 GiB) | 3 | TensorFold + DSpark | prose 31.3, code 41.7 tok/s | 591 tok/s at 32k | [mia-glm3] |
| DeepSeek V4.1 Flash, 2.9 bpw `mul1` | 2 | vLLM + DSpark | 31.6 tok/s | ~1,041 tok/s at 10k | [ds-vllm2] |
| DeepSeek V4.1 Flash 1017, 2.9 bpw | 2 | TensorFold Zig + DSpark | 74.9 tok/s | ~2,140–2,180 tok/s, 8k–64k | different checkpoint revision than the row above [ds-tf2] |
| GLM-5.2, 3.5 bpw | 4 | SparkRing (vLLM) | 20.15 tok/s (C1), 64.13 (C8) | 671 tok/s | 16k, temperature 1.0 [sr-readme] |

# Quality numbers published

- **GLM-5.3-Flash 4 bpw (MiaAI calibration) vs the widely used TR3-4bpw**, KL divergence to Z.AI's official FP8
  release as served: 0.0903 vs 0.0990 (wiki), 0.3150 vs 0.3271 (workload). GSM8K 98.8 % vs 98.0 %, HumanEval 95.7 %
  vs 97.6 %, EvalPlus 86.5 % vs 86.3 %; the author states none of the benchmark gaps is statistically significant,
  the gain is fidelity (KL 2–18 % lower) [mia-glmf].
- **GLM-5.3-Flash at 2.0 bpw vs a 3.05 bpw mosaic** (12 of 45 MoE layers at higher width): the mosaic has top-1 0.80842
  vs 0.78902 and KL −15.3 %, but it is `mul1` and so runs without MTP at ~9–10 tok/s instead of 18.7–19.2 [glm1x].
- Full GLM 5.3 at 2.75 bpw: no KL/perplexity against BF16 published; the recipe publishes paired task scores for its
  KV-cache choice only [mia-glm3].

# Runbook

```bash
# GLM-5.3-Flash EXL3 on two Sparks, vLLM path (MiaAI-Lab)
git clone https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks.git
cd GLM-5.3-Flash-EXL3-2x-DGX-Sparks
cp .env.example .env     # HEAD_IP, WORKER_IP, CX7 interface names
./start.sh               # pulls image, downloads ~164 GiB, shares weights, starts both ranks
```

That README itself now points readers to the TensorFold version of the same recipe, which "runs faster"
[glm-vllm2].

# Limitations

- EXL3 is a community format: no NVIDIA support statement, and the Spark runtimes are community-built images
  pinned by digest [sr-exl3r7] [glm-vllm2].
- Memory is tight at these sizes. The DeepSeek 2.9 bpw recipe holds 99.5 GiB of weights per rank and leaves the head
  ~5.9 GiB MemAvailable after a 34k agent replay [ds-vllm2]; the 1-Spark GLM kit refuses to start if any other GPU job
  runs [glm1x]. See [Unified memory limits](/hardware/unified-memory-limits.md).
- Quality of a given EXL3 checkpoint depends on its calibration; two quants at the same bpw and size can differ in KL
  [mia-glmf]. See [Quantization formats](/stacks/quantization-formats.md).
