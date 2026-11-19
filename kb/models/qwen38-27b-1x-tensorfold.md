---
type: recipe
title: Qwen3.8 27B on one Spark (TensorFold)
description: One DGX Spark serves Qwen3.8-27B over an OpenAI API at 58.3 tok/s single-stream, 220.6 tok/s for 8 concurrent requests, 262k context (1M with YaRN).
tags: [qwen, tensorfold, single-node, speculative-decoding, coding]
resource: /models/qwen38-27b-1x-tensorfold.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [Qwen3.8-27B-DGX-Spark-TensorFold]
sparks_needed: 1
entities:
  - label: Qwen3.8-27B
    kind: model
  - label: TensorFold
    kind: inference_engine
  - label: DFlash2
    kind: speculative_decoder
relations:
  - type: runs_on
    target: /hardware/gb10-platform.md
provenance:
  - source: https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold
    note: MiaAI-Lab recipe page; numbers measured with sparkDash on one DGX Spark.
citations:
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: tf
    text: "Ash Hart, TensorFold (Apache-2.0). https://github.com/ashhart/TensorFold"
---

# Overview

| | |
|---|---|
| **Sparks needed** | **1** |
| Engine | TensorFold v0.6.0 + 5 recipe patches [tf] |
| Weights | MLX 4-bit checkpoint + DFlash2 drafter (speculative decoding, exact: output equals serial decoding) |
| API | OpenAI-compatible, port 8888, model `Qwen3.8-27B` |
| Context | 262,144 tokens; 1,048,576 with `YARN_FACTOR=4` |
| Input | Text, up to 50 images, up to 2 videos per request |
| Licences | Recipe Apache-2.0; weights Qwen Community License 1.0; image built on NVIDIA's PyTorch container |

All figures below are from [mia-q27], measured with sparkDash on one DGX Spark.

# Measured speed

| Concurrent requests | Prose, aggregate | Prose, per request | Code, aggregate | First token |
|---|---|---|---|---|
| 1 | 58.3 tok/s | 58.3 tok/s | 136.9 tok/s | 100 ms |
| 2 | 108.5 tok/s | 55.4 tok/s | 223.9 tok/s | ~200 ms |
| 4 | 135.1 tok/s | 40.3 tok/s | 292.0 tok/s | ~420 ms |
| 8 | 220.6 tok/s | 32.7 tok/s | 323.2 tok/s | ~870 ms |

Prefill: 1,793 tok/s at 8k tokens, 1,118 tok/s at 131k. Long prompts are slow: 205 s for 195k tokens,
44 minutes for 884k with YaRN — set client timeouts accordingly.

**Why this matters:** the same class of model, dense 27B in FP8 on stock settings, decodes at
about 8.3 tok/s on the same hardware (see [GB10 platform](/hardware/gb10-platform.md)). 4-bit weights plus
speculative decoding make it ~7× faster per stream. The recipe matters as much as the box.

# Examples

```bash
git clone https://github.com/MiaAI-Lab/Qwen3.8-27B-DGX-Spark-TensorFold.git
cd Qwen3.8-27B-DGX-Spark-TensorFold
./start.sh            # pulls/builds the image, downloads ~19 GB, smoke-tests, prints the endpoint

curl -s http://<spark-address>:8888/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "Qwen3.8-27B",
  "messages": [{"role": "user", "content": "Write a Python fibonacci function."}],
  "max_tokens": 1000
}'
```

Day to day: `./start.sh restart`, `./stop.sh`, `docker logs -f qwen38-27b-tf`.

# Memory

The server pins up to 78 GiB of KV cache at startup (FP8 cache, 32 KiB per token: ~2.5M tokens) and holds
about 97 GiB from the first second — enough for 8 full 262k windows. On a shared Spark, lower `KV_POOL_GB`
and raise `TENSORFOLD_MEMORY_RESERVE_GIB`: running out of unified memory can freeze the host [mia-q27].

# Limitations

- Quality cost of the defaults (FP8 cache + FP8 prompts): perplexity 3.387 vs 3.316 all-bf16, top-1 token
  agreement 94 %. `PREFILL_FP8=0` recovers most of it at lower prefill speed [mia-q27].
- YaRN long-context quality was checked with needle tests only (195k, 491k, 884k).
- Requirements: Docker with the NVIDIA runtime, ~60 GB free disk.
