---
type: model
title: Nemotron 3.5 Bolt and Lightning on one DGX Spark
description: NVIDIA Nemotron 3.5 Bolt 74B-A9B (TensorFold, 71.0 tok/s in 51.1 GB) and Lightning 30B-A3B (SGLang, 1M context, 48 concurrent) on a single DGX Spark, leaving room for other work.
tags: [models, nemotron, nvidia, single-node, tensorfold, sglang, mamba, moe]
resource: /models/nemotron-35.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [Nemotron 3.5 Bolt, Nemotron-3.5-Bolt-74B-A9B, Nemotron 3.5 Lightning, Nemotron-3.5-Lightning-30B-A3B]
entities:
  - label: Nemotron-3.5-Bolt-74B-A9B
    kind: model
  - label: Nemotron-3.5-Lightning-30B-A3B
    kind: model
  - label: LiLiCorr
    kind: speculative_decoder
  - label: DSpark
    kind: speculative_decoder
  - label: TensorFold
    kind: inference_engine
  - label: SGLang
    kind: inference_engine
relations:
  - type: part_of
    target: /models/spark-matrix.md
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /hardware/unified-memory-limits.md
  - type: uses
    target: /stacks/tensorfold.md
  - type: uses
    target: /stacks/sglang.md
  - type: uses
    target: /stacks/speculative-decoding.md
  - type: related_to
    target: /models/qwen38-flash-next.md
provenance:
  - source: https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark
    note: MiaAI-Lab recipe page, Bolt on TensorFold's Zig engine, measured with sparkDash on one Spark.
  - source: https://github.com/MiaAI-Lab/Nemotron3.5-Lightning-DGX-Spark-RTX-5090-6000-PRO
    note: MiaAI-Lab SGLang + DSpark recipe for Lightning; capacity numbers read from a running Spark, no decode speed published.
citations:
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark, with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: lightning
    text: "MiaAI-Lab, NVIDIA Nemotron 3.5 Lightning 30B-A3B NVFP4 + DSpark for DGX Spark, RTX 5090/6000 PRO, README. https://github.com/MiaAI-Lab/Nemotron3.5-Lightning-DGX-Spark-RTX-5090-6000-PRO/blob/38c16a403ea57f26f1828fa572270245ae51f01d/README.md"
---

# Overview

NVIDIA's Nemotron 3.5 models are hybrid Mamba / MoE / attention models, so only a few attention layers grow a
KV cache with context. That makes them the cheapest long-context models to host on one Spark.

| | Bolt 74B-A9B | Lightning 30B-A3B |
|---|---|---|
| Parameters | 74B total, 9B active (9 of up to 496 experts a token) [mia-bolt] | 30B total, ~3B active [lightning] |
| Layers | 88 blocks: 40 Mamba, 40 MoE, 8 attention [mia-bolt] | 52: 23 Mamba-2, 23 MoE, 6 attention [lightning] |
| Checkpoint | NVIDIA "24GB" pack, 22.45 GiB: IQ2_XXS experts, NVFP4 Mamba, Q8_0 attention, C-RADIO vision tower [mia-bolt] | NVFP4 (ModelOpt), ~21 GiB with the DSpark draft [lightning] |
| Engine · drafter | TensorFold Zig + recipe's `libbolt.so` · NVIDIA LiLiCorr (~1.3 GB) [mia-bolt] | SGLang · NVIDIA DSpark [lightning] |
| Context | 262,144 tokens a stream, 16 streams [mia-bolt] | ~1,048,570 tokens a request [lightning] |
| Input | Text, up to 64 images, up to 4 videos [mia-bolt] | Text (tool calls via `qwen3_coder` parser) [lightning] |

All figures are **self-reported by the recipe author** (Mia's AI Lab); no independent measurement exists in
the collected sources.

# Measured: Bolt

One Spark, recipe defaults (16 streams, 262k window each, bf16 KV, vision and drafter on), sparkDash [mia-bolt]:

| Requests | Prose aggregate | Prose per request | Code aggregate | First token (prose) |
|---|---|---|---|---|
| 1 | 71.0 tok/s | 71.0 | 114.1 tok/s | 56 ms |
| 2 | 91.5 | 47.3 | 160.9 | 297 ms |
| 4 | 126.8 | 35.2 | 198.3 | 575 ms |
| 8 | 166.6 | 23.5 | 245.3 | 1.23 s |

Prefill: 1,575.6 tok/s at 4k, 1,375.1 at 32k, 986.8 at 131k (133 s to first token) [mia-bolt].
A follow-up turn repeating 50 images and 4 videos (30,500 tokens) answers in 1.7 s from the prompt cache [mia-bolt].

# Measured: Lightning

No decode speed is published. Capacity on a running Spark with stock settings (`MEM_FRACTION_STATIC=0.78`)
[lightning]:

| Value | Measured |
|---|---|
| KV token pool | ~4.93M tokens (~14.1 GiB, FP8) |
| Max concurrent requests | 48 |
| Weights (NVFP4 + DSpark draft) | ~21.0 GiB |
| DSpark draft KV (bf16, separate) | ~28.2 GiB |
| Mamba/SSM cache | 716 MiB |

That is "roughly 4–5 simultaneous full 1M-token contexts, or far more shorter ones" [lightning].

# Memory footprint: why it leaves room for other work

Bolt with its defaults (16 streams, full window, vision, drafter) loads in **51.1 GB**, leaving roughly **70 GB of
the 121 GB** for other work [mia-bolt]. It starts small because each stream holds only 0.4 GiB of recurrent
state from load; attention rows (8 KB a token in bf16) are mapped 4,096 tokens at a time and returned when a
stream ends [mia-bolt]. The server needs about 55 GiB free at start [mia-bolt].

For comparison, the Qwen3.8 Flash Next TensorFold server holds ~81 GiB of weights and pins the rest as KV
pool ([Qwen3.8 Flash Next](/models/qwen38-flash-next.md)). On a shared Spark, Bolt is the large model that can
sit beside an embedding server, a second small model or development containers. Keep at least 10 GiB free
under load: running out of unified memory freezes the machine [mia-bolt]
(see [Unified memory limits](/hardware/unified-memory-limits.md)).

Lightning is not small on a Spark by default: the 0.78 memory fraction claims most of the 128 GiB for its pool;
lower `MEM_FRACTION_STATIC` to share the machine, at the cost of pool size and concurrency [lightning].

# Which recipe for what

| Need | Recipe | Why |
|---|---|---|
| Single developer, one Spark, interactive | Bolt (TensorFold) | 71.0 tok/s prose, 114.1 code, vision, half the Spark free [mia-bolt] |
| Team on one Spark | Bolt for speed per stream (166.6 ×8); Lightning for many sessions (48 concurrent) | Lightning speed is not published, so measure before committing [mia-bolt] [lightning] |
| Longest context | Lightning | ~1M tokens a request vs 262k for Bolt [lightning] |
| Spark shared with other services | Bolt | 51.1 GB footprint [mia-bolt] |

# Quality evidence

Not published. The Bolt recipe reports functional checks only: replies identical alone or beside others,
50 images of 2560×1920 (165,600 tokens) read correctly in one chat, and three engine bugs that had made the
drafter accept 0 of 7 tokens, now fixed [mia-bolt]. The Lightning README gives recommended sampling
parameters but no evaluation [lightning].

# Licences

| Item | Licence |
|---|---|
| Bolt weights | NVIDIA OpenMDW License Agreement 1.1 [mia-bolt] |
| Lightning weights | "subject to NVIDIA's original model license" (not named) [lightning] |
| Bolt recipe; Lightning recipe | MIT [mia-bolt] [lightning] |
| Bolt image | NVIDIA PyTorch container terms; FFmpeg decoders (LGPL) [mia-bolt] |

# Limitations

- Bolt does not serve logprobs, grammar-constrained decoding, int8/int4 KV caches, or WebP/GIF/BMP images [mia-bolt].
- Bolt's experts are ~2-bit (IQ2_XXS) and no quality comparison against a higher-precision version is published.
- Lightning's throughput on a Spark is unmeasured in the collected sources.
