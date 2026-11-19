---
type: hardware
title: Unified memory limits
description: How much of the 128 GB a model really gets on a GB10, how weights, KV cache and the runtime share it, why running out freezes the host, and the sizing and guard rules that keep a Spark up.
tags: [gb10, unified-memory, kv-cache, oom, sizing, operations]
resource: /hardware/unified-memory-limits.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [128 GB unified memory, 121.7 GiB, memory guard, earlyoom, KV pool sizing, host freeze]
entities:
  - label: LPDDR5x unified memory
    kind: memory
  - label: earlyoom
    kind: tool
  - label: memory guard
    kind: practice
relations:
  - type: describes
    target: /hardware/gb10-platform.md
  - type: constrains
    target: /models/spark-matrix.md
  - type: related_to
    target: /stacks/quantization-formats.md
  - type: related_to
    target: /stacks/vllm.md
  - type: related_to
    target: /stacks/tensorfold.md
  - type: related_to
    target: /hardware/power-and-thermals.md
  - type: monitored_by
    target: /clustering/cluster-tooling.md
provenance:
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: "Rules from the section Memory on a unified-memory GPU, and the failed two-node boots (August 2026)."
  - source: https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold
    note: TensorFold recipe memory reserve, KV pool sizing, freeze warning.
  - source: https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks/blob/64b02dea8681fb1d8e3a659ea432a8e9e9ba3995/README.md
    note: 121.7 GiB visible per Spark; what competes with the model for unified memory.
  - source: https://whitepapers.openzeka.com/papers/local-llm-guide/
    note: OpenZeka memory budget formula and headroom rule.
citations:
  - id: nv-hw
    text: "NVIDIA, DGX Spark User Guide — Hardware Overview. https://docs.nvidia.com/dgx/dgx-spark/hardware.html"
  - id: nv-rn
    text: "NVIDIA, DGX Spark Release Notes. https://docs.nvidia.com/dgx/dgx-spark/release-notes.html"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: simonw
    text: "Simon Willison, NVIDIA DGX Spark: great hardware, early days for the ecosystem (2025-10-14). https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/"
  - id: mia-ds3
    text: "MiaAI-Lab, DeepSeek-v4.1-Flash on three DGX Sparks (SGLang) README. https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-DGX-Sparks/blob/64b02dea8681fb1d8e3a659ea432a8e9e9ba3995/README.md"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: mia-fn1
    text: "MiaAI-Lab, Qwen3.8 Flash Next on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold"
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: ae-gotchas
    text: "Alex Ellis / MiaAI-Lab, GLM-5.3-Flash 4x switchless — gotchas. https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/gotchas.md"
  - id: oz-local
    text: "OpenZeka, Local LLM Usage Guide (2026-06-30). https://whitepapers.openzeka.com/papers/local-llm-guide/"
  - id: oz-quant
    text: "OpenZeka, LLM Quantization Selection Guide (2026-10-12). https://whitepapers.openzeka.com/papers/llm-quantization-selection/"
  - id: oz-4n
    text: "OpenZeka, DGX Spark 4-Node AI Cluster Setup Guide (2026-07-24). https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/"
  - id: sparkdash
    text: "MiaAI-Lab, sparkDash README. https://github.com/MiaAI-Lab/sparkDash/blob/d229bff50120f475274c28d4faf223fdbb56795a/README.md"
---

# Overview

A GB10 has **128 GB of LPDDR5x shared by the CPU and GPU** at 273 GB/s [nv-hw]. There is no separate
VRAM: "host RAM *is* GPU memory on a Spark" — NCCL buffers, caches and helper processes all compete
with the model [mia-ds3]. Three consequences drive every recipe:

1. **Less than 128 is usable.** About 121 GiB is exposed to CUDA [cape-serve]; recipe authors quote
   **121.7 GiB** visible per Spark [cape-serve] [mia-ds3].
2. **Running out does not fail cleanly — it freezes the host.** "On this machine, running out of
   unified memory freezes it" [mia-fn1]; an OOM can become "a wedged node that usually needs a
   power-cycle" [ae-gotchas]. GB10 units have no BMC (see [power and thermals](/hardware/power-and-thermals.md)).
3. **Container limits do not protect you.** GPU and unified-memory allocations are not charged to a
   container's memory cgroup, so `docker --memory` never engages [cape-serve].

# How much is visible

| Reading | Value | Source |
|---|---|---|
| Marketed | 128 GB | [nv-hw] |
| Exposed to CUDA | ~121 GiB; 121.7 GiB in recipe logs | [cape-serve] [mia-ds3] |
| `free -h` / CUDA at launch (Oct 2025) | 119 GB total, 112 GB available; GPU 119.68 GB | [simonw] |

The launch-week figure is lower than the 2026 figures; we have no source that reconciles them. One
known variable is the display carveout: 2 GB by default, 4 GB optional (July 2026), and since October
2026 automatically down to 512 MB on headless units [nv-rn].

# What eats it

Total = **weights + KV cache + activations + runtime overhead + quantization metadata** [oz-quant].
OpenZeka's rule: leave ~20 % headroom on top [oz-local]. On a mixture-of-experts model, **total**
parameters set the memory, **active** parameters set the speed [oz-local].

A worked failure (Capetron, GLM-5.3-Flash NVFP4, two nodes) [cape-serve]: 92.8 GiB of weights per rank
+ ~5 GiB of host left ~24 GiB for CUDA context, NCCL, the MoE workspace, the MTP draft and the KV
cache — not enough; five boots failed. Committed memory "tracks weights plus runtime, not the
`--gpu-memory-utilization` cap". The boot that worked pinned the KV cache to 4.14 GiB and ran at a
3–4 % host MemAvailable floor, which Capetron would not leave unattended.

What published recipes need free at start (self-reported by recipe authors):

| Recipe | Sparks | Free memory needed per Spark | Weights / KV | Source |
|---|---|---|---|---|
| Qwen3.8 27B, TensorFold | 1 | 45 GiB startup estimate; KV pool takes up to 78 GiB more | KV pool = free GiB − ~31, max 78 | [mia-q27] |
| Nemotron 3.5 Bolt, TensorFold | 1 | ~55 GiB for 16 streams (incl. 10 GiB floor) | — | [mia-bolt] |
| Qwen3.8 Flash Next FP4, TensorFold | 1 | ~108 GiB | ~81 GiB load; 24.36 GiB KV pool = 5 full 262k windows | [mia-fn1] |
| GLM-5.3-Flash EXL3, TensorFold | 2–4 | ~110 GiB | — | [mia-glmf] |
| DeepSeek V4.1 Flash, TensorFold | 4 | ~100 GB | ~80 GiB weights a node; 11–18 GiB left free | [mia-ds4] |

See [quantization formats](/stacks/quantization-formats.md) for how bit width moves the weight term.

# Rules that keep a Spark up

| Rule | Value | Source |
|---|---|---|
| vLLM `--gpu-memory-utilization` | Never 0.85 (leaves 1–4 % MemAvailable); 0.72–0.75 for a standing single node with fp8 KV; 0.65 for TP4+EP. Each 0.01 ≈ 1.2 GiB | [cape-serve] |
| Floor kept free by TensorFold | 10 GiB default (`TENSORFOLD_MEMORY_RESERVE_GIB`); scripts refuse to start below it | [mia-fn1] |
| Same, Qwen3.8 27B recipe | reserve 0 by design — raise it if anything else shares the box | [mia-q27] |
| Per-rank guard (multi-Spark) | stop that Spark's rank below 3 GiB free: "a failed rank beats a frozen Spark" | [mia-glm3] |
| KV pool cap, 4-node switchless GLM | 12 GiB; higher risked an OOM hard-hang | [ae-gotchas] |
| Memory guard loop | poll MemAvailable every 5 s, `docker rm -f` below 12 %; fired once and the host stayed up | [cape-serve] |
| Page cache | drop it when `Cached` > 40 GiB during model load (`cache_flusher.sh`) | [cape-serve] |
| Dashboard alert | sparkDash warns under 3 GB, critical under 1.5 GB of unified memory | [sparkdash] |

**earlyoom: know if it is installed.** With its 10 % default floor it kills the vLLM worker with no
traceback and `docker inspect` shows `OOMKilled=false` [cape-serve]. sparkrun's setup wizard offers
to install it [oz-4n]. Either tune its floor below your serving floor or rely on a guard you control.

NVIDIA's July 2026 driver "enhances Out-of-Memory (OOM) handling" and gives user feedback under memory
pressure [nv-rn]; the field reports above are what recipe authors still do on top.

# Sizing rules

- Budget against ~121 GiB visible, not 128 GB, and keep a floor free (10 GiB in TensorFold's default)
  [cape-serve] [mia-fn1]. The 4-bit and FP4 checkpoints in the [models matrix](/models/spark-matrix.md)
  exist because of this arithmetic.
- In a cluster, everything that pins host memory on the head competes with the model; a head that
  runs out stalls all ranks because tensor parallelism is synchronous [mia-ds3].
- A shared box is tight: recipe authors tell you to shrink the KV pool or raise the reserve when other
  workloads share the Spark, because running out can freeze the host [mia-q27].

# Limitations

- No NVIDIA document states the CUDA-visible capacity; the 121.7 GiB figure is from recipe logs.
- The guard thresholds (3 GiB, 10 GiB, 12 %) are each author's choice, not tested limits.
