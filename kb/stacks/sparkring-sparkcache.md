---
type: component
title: SparkRing and SparkCache
description: SparkRing, a vLLM-based serving stack and custom RDMA collective layer for switchless 2- and 4-Spark clusters, and SparkCache, its persistent on-disk prompt cache — what they do, how they measure, and their published numbers.
tags: [sparkring, sparkcache, sircl, nccl, rdma, switchless, vllm, prefix-cache, benchmarking]
resource: /stacks/sparkring-sparkcache.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [SparkRing, SparkCache, SIRCL, Switchless Inference RDMA Collective Layer]
entities:
  - label: SparkRing
    kind: serving_stack
  - label: SIRCL
    kind: collective_transport
  - label: SparkCache
    kind: kv_cache_connector
  - label: patched NCCL
    kind: collective_library
relations:
  - type: extends
    target: /stacks/vllm.md
  - type: uses
    target: /clustering/nccl-over-roce.md
  - type: deploys_on
    target: /clustering/two-node-dac.md
  - type: serves
    target: /stacks/exl3-exllamav3.md
  - type: compared_with
    target: /stacks/tensorfold.md
provenance:
  - source: https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/README.md
    note: SparkRing README at commit b9cd552 (alpha). Internal links point to github.com/FujitsuPolycom/sparkring, the same project.
  - source: https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/ARCHITECTURE.md
    note: Topology, collective path, profile composition.
  - source: https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/performance/records/transport/dual-port-striping-20260818.md
    note: Model-free transport measurements, SIRCL vs patched NCCL (research-only record).
  - source: https://github.com/FujitsuPolycom/sparkcache/blob/8abbe9da67b8143831d21b43d0395c4f347a619a/README.md
    note: SparkCache README (experimental) and its DeepSeek-V4 TP4 live validation.
citations:
  - id: sr-readme
    text: "SparkRing README (Apache-2.0), commit b9cd552. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/README.md"
  - id: sr-arch
    text: "SparkRing, Architecture. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/ARCHITECTURE.md"
  - id: sr-sircl
    text: "SparkRing, SIRCL. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/docs/SIRCL.md"
  - id: sr-transport
    text: "SparkRing, Spark Transport. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/README.md"
  - id: sr-nccl
    text: "SparkRing, Patched NCCL fallback. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/nccl/README.md"
  - id: sr-cable
    text: "SparkRing, Direct-cable qualification. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/CABLE_QUALIFICATION.md"
  - id: sr-perf
    text: "SparkRing, Performance evidence. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/performance/README.md"
  - id: sr-stripe
    text: "SparkRing, Dual-port striping and graph-kernel probe record, 2026-08-18. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/performance/records/transport/dual-port-striping-20260818.md"
  - id: sc-readme
    text: "SparkCache README (Apache-2.0), commit 8abbe9d. https://github.com/FujitsuPolycom/sparkcache/blob/8abbe9da67b8143831d21b43d0395c4f347a619a/README.md"
  - id: sc-dsv4
    text: "SparkCache, DeepSeek-V4 TP4 live validation. https://github.com/FujitsuPolycom/sparkcache/blob/8abbe9da67b8143831d21b43d0395c4f347a619a/DEEPSEEK_V4_TP4_LIVE_VALIDATION.md"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
---

# Overview

**SparkRing** is "a low-latency collective transport and vLLM-based inference-serving stack for switchless clusters
of NVIDIA DGX Spark systems" [sr-readme]. It supports **GB10 pairs** (one direct cable) and **four-node rings**
(cables `0-1-2-3-0`, no switch); six-node ring work is research-only. It is labelled **alpha**: branches move, so pin
a commit when reproducing [sr-readme].

**SparkCache** gives vLLM a persistent prompt cache on local NVMe: it restores the longest matching prefix even after
vLLM evicts it or after the process, container or server restarts. It is labelled **experimental** [sc-readme].

They matter because they are the stack built specifically for 2–4 Sparks on direct cables, with no switch.

# SparkRing

**Components** [sr-arch] [sr-sircl] [sr-transport]:

| Piece | Role |
|---|---|
| vLLM + pinned runtime images | The serving engine, per-profile images built once and distributed by content-addressed ID |
| **SIRCL** (Switchless Inference RDMA Collective Layer) | Persistent RDMA sessions and CUDA-graph-replayable command rings; a 4-rank collective runs as the ring's two perfect matchings, so every step is a neighbour exchange |
| Patched NCCL | Fallback for everything SIRCL does not admit. Upstream NCCL "cannot initialize on this switchless topology at all"; the patch keeps NCCL on the direct-cable RoCE ring [sr-stripe] [sr-nccl] |
| Ring Doctor, `sparkring cluster init` | Enrols nodes, discovers ConnectX-7 hardware, checks routes, IP forwarding and Docker forward rules before a model is chosen [sr-readme] [sr-arch] |

SIRCL is narrow on purpose: it is qualified only for the four-Spark cycle and only for BF16 tensor-parallel
all-reduce and vocabulary all-gather at the GLM hidden width 6,144; the DeepSeek width-4,096 path is research-only,
and the Qwen 27B width-5,120 path is not admitted. **On a two-Spark pair SIRCL is unsupported; pairs use patched NCCL
only** [sr-sircl] [sr-transport]. The pair's NCCL environment names one RoCE device (`NCCL_IB_HCA=<one-direct-roce-device>`)
[sr-nccl].

**Why bother:** in a model-free test on the 4-Spark ring, patched NCCL showed an ~800 µs floor per all-reduce at every
payload, against 174 µs (0.5 MiB) and 1,223 µs (6 MiB) for SIRCL's best kernels, same device timing [sr-stripe]. The
same record found both rails required on the ring: a single-port NCCL configuration fails deterministically because
each rank reaches one neighbour only through its second port [sr-stripe].

## Profiles and published numbers

"Qualified — 16K context." Prefill: cold prompt, caching off. Decode: unique cold prompts at temperature 1.0,
aggregate across streams [sr-readme]. Self-reported.

| Profile | Sparks | Prefill | C1 decode | C8 decode | Highest tested |
|---|---|---|---|---|---|
| DeepSeek-V4-Flash-0731 (DSpark) | 2 | 1,926 | 58.36 | 162.69 | C32: 307.13 |
| DeepSeek-V4-Flash-0731 | 4 | 2,488 | 68.84 | 265.16 | C32: 508.11 |
| Qwen3.8-27B EXL3 K5/K6 | 2 | 1,367 | 29.50 | 142.20 | C8: 142.20 |
| Qwen3.8-27B EXL3 K5/K6 | 4 | 1,964 | 35.07 | 191.02 | C8: 191.02 |
| GLM-5.2 EXL3 3.5 bpw | 4 | 671 | 20.15 | 64.13 | C8: 64.13 |
| GLM-5.3 Flash + DFlash2 + SparkCache (research-only, single run, random tokens) | 4 | 2,371 | 36.06 | — | — |

Two readings:

- SparkRing publishes the **highest aggregate** numbers on 4 Sparks in the sources collected here (DeepSeek-V4-Flash: 508 tok/s at
  32 concurrent) [sr-readme]: this is the "many users" end.
- Sharding a **dense 27B** over 2–4 Sparks did not beat one Spark per stream: 29.5–35.1 tok/s C1 here vs 58.3 tok/s on
  one Spark with TensorFold [mia-q27]. Methodologies differ (temperature 1.0 vs 0.7, different engines and quants), so
  this is a direction, not a ranking.

## Performance methodology

SparkRing's rule set is worth copying for your own measurements [sr-perf]:

- Compare only runs with the same model revision, image identity, topology, rank count, TP/DCP degrees, request
  shape, concurrency, cache state and timing method; otherwise name the variable or report separately.
- Warm-up, graph capture, request errors, transport-counter changes and missing ranks are **gates**; a rejected
  capture is not a zero and is never averaged in.
- Every published record has five sections: **Conditions, Measurement, Result, Conclusion, Limitations**. A record
  without all five is research material, not a benchmark.

Before loading a model, every new, moved or suspect cable is qualified with `qualify_direct_cable.py`: bidirectional
payload integrity while watching NIC error counters; "link-up and ping are not enough" [sr-cable]. This pairs with
the validation steps in [Two Sparks over one DAC](/clustering/two-node-dac.md).

# SparkCache

How it works [sc-readme]:

1. The scheduler hashes eligible prompt boundaries; every rank reports which entries it can read.
2. The longest entry available on **every** rank is chosen; each worker verifies identity, compatibility and
   payload integrity, then restores only its own shard from local storage.
3. Any failed check becomes an ordinary cache miss and vLLM recomputes the prompt.
4. Completed prefills publish immutable objects before an atomic manifest exposes them.

Measured (DeepSeek-V4, 4 Sparks, after a full four-rank restart, self-reported) [sc-dsv4]:

| Prompt tokens | Restored tokens | Restore per rank | End-to-end hit check |
|---|---|---|---|
| 36,910 | 36,864 | 207–298 ms | 1.56 s |
| 73,774 | 73,728 | 335–412 ms | 1.64 s |
| 147,502 | 147,456 | 734–888 ms | 2.45 s |

Answers were byte-identical; four entries used about 1.086 GiB of NVMe per rank; a one-byte corruption was detected
and the entry invalidated [sc-dsv4]. For scale (different model and engine): a cold 131k-token prompt takes 117 s
to prefill with the one-Spark Qwen3.8 27B recipe [mia-q27] (see [Qwen3.8 27B on one Spark](/models/qwen38-27b-1x-tensorfold.md)).

```bash
python -m pip install 'sparkcache[connector]==0.1.0a2'   # published on PyPI; repo declares 0.1.0a3
```

# Limitations

- Both projects are alpha/experimental and change quickly [sr-readme] [sc-readme].
- SparkCache does not reuse an entry across different shard layouts (cross-topology reuse unsupported); streaming
  publication and buddy replication are research-only [sc-readme].
- SIRCL only helps on the four-Spark ring; a two-Spark demo runs SparkRing on patched NCCL [sr-sircl].
- The GLM-5.3 Flash profile is "still in heavy dev"; its only throughput figure is a single research observation
  with no A/B baseline [sr-readme].
- The public BF16 DFlash2 checkpoint used by the GLM-5.3 profiles is CC BY-NC-ND 4.0, research and evaluation only
  [sr-readme] — not usable for production at work.
