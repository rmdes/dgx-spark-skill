---
type: report
title: "Field report: EXO 1.0 splits prefill (DGX Spark) and decode (Mac Studio)"
description: EXO Labs' early-access experiment — prefill on a DGX Spark, decode on an M3 Ultra Mac Studio, KV cache streamed layer by layer — for 2.8× faster end-to-end inference than the Mac alone.
tags: [field-report, vendor-self-reported, disaggregated-inference, prefill, decode, exo]
resource: /field-reports/exo-spark-mac-studio.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [EXO DGX Spark Mac Studio, disaggregated prefill decode]
entities:
  - label: EXO
    kind: inference_engine
  - label: EXO Labs
    kind: organization
  - label: Mac Studio M3 Ultra
    kind: system
relations:
  - type: cites
    target: /hardware/gb10-platform.md
  - type: related_to
    target: /field-reports/exolabs-handbook.md
provenance:
  - source: https://blog.exolabs.net/nvidia-dgx-spark/
    note: EXO Labs blog; results of EXO's own product on two early-access DGX Spark units. Publication date not shown in the clipped page.
citations:
  - id: exo
    text: "EXO Labs, NVIDIA DGX Spark + Apple Mac Studio = 4x Faster LLM Inference with EXO 1.0. https://blog.exolabs.net/nvidia-dgx-spark/"
---

# Overview

**Source type: self-reported by a software vendor about its own product**, on early-access hardware from NVIDIA [exo].
The idea: the Spark has about 4× the compute of an M3 Ultra (~100 vs ~26 TFLOPs FP16), the Mac has about 3× the memory
bandwidth (819 vs 273 GB/s), so run each phase where it is fastest [exo].

| Item | Detail |
|---|---|
| Who | EXO Labs, makers of the EXO distributed inference software |
| Hardware | 2× DGX Spark (early access), Mac Studio M3 Ultra (512 GB, 819 GB/s) |
| Link | 10 GbE between Spark and Mac [exo] |
| Workload | Llama-3.1 8B FP16, 8,192-token prompt, 32 generated tokens |

# How it works

- **Prefill is compute-bound** (attention compute grows with the square of prompt length) → Spark.
- **Decode is memory-bound** (vector-matrix work against the KV cache) → Mac Studio.
- The KV cache streams **layer by layer** while the next layer's prefill runs, so transfer hides behind compute once
  the prompt is long enough. With 8-bit KV and a 10 GbE link the threshold is about 5K tokens for Llama-3 70B,
  10K for Llama-3 8B, 40K for Llama-2 7B [exo].
- EXO 1.0 discovers devices, profiles them and plans this placement automatically [exo].

# Measured

| Configuration | Prefill | Generation | Total | Speed-up vs Mac |
|---|---|---|---|---|
| DGX Spark alone | 1.47 s | 2.87 s | 4.34 s | 1.9× |
| M3 Ultra alone | 5.57 s | 0.85 s | 6.42 s | 1.0× |
| Spark + M3 Ultra | 1.47 s | 0.85 s | 2.32 s | 2.8× |

Llama-3.1 8B FP16, 8K prompt, 32 output tokens [exo]. The title says "4x"; the only table shows 2.8× over the Mac and
about 1.9× over the Spark alone [exo].

# What did not work / limits

- One small dense model, 32 output tokens: the workload is prefill-heavy by design, which flatters the split.
- No multi-user, no MoE, no long generation results published.
- Needs a Mac Studio; nothing here applies to a Spark-only cluster except the principle.

# Verdict

EXO's conclusion: inference is "no longer constrained by what one box can do, but by what your whole cluster can do together" [exo].
Vendor marketing for its own software; no independent reproduction in the sources collected here.

# Takeaways

- Confirms the Spark's strength is prompt reading (prefill). RAG and agent workloads send long prompts, which suits it;
  see [GB10 platform](/hardware/gb10-platform.md).
- Not a path for a Linux-only setup: it requires Apple hardware and EXO.
- The handbook proposes the same "Spark as prefill helper" idea for other pairings, marked as unproven
  ([DGX Spark Handbook](/field-reports/exolabs-handbook.md)).
