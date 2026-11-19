---
type: report
title: "Field report (vendor): NVIDIA on scaling agents and workloads across DGX Sparks"
description: NVIDIA's own benchmarks for agent-style long-context inference, concurrency, and one-to-four-node scaling of inference and fine-tuning on DGX Spark.
tags: [field-report, vendor, nvidia, scaling, concurrency, agents, fine-tuning]
resource: /field-reports/nvidia-agents-on-spark.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [Scaling Autonomous AI Agents and Workloads with NVIDIA DGX Spark, NVIDIA scaling blog]
entities:
  - label: NVIDIA
    kind: organization
  - label: TensorRT LLM
    kind: inference_engine
  - label: vLLM
    kind: inference_engine
  - label: NemoClaw
    kind: tool
relations:
  - type: cites
    target: /clustering/switched-fabric.md
  - type: cites
    target: /clustering/three-node-ring.md
  - type: cites
    target: /stacks/vllm.md
  - type: cited_by
    target: /field-reports/exolabs-handbook.md
provenance:
  - source: https://developer.nvidia.com/blog/scaling-autonomous-ai-agents-and-workloads-with-nvidia-dgx-spark/
    note: NVIDIA Technical Blog, Allen Bourgoyne, 2026-03-16. Vendor source; numbers measured by NVIDIA.
citations:
  - id: nv-agents
    text: "NVIDIA Technical Blog, Scaling Autonomous AI Agents and Workloads with NVIDIA DGX Spark (2026-03-16). https://developer.nvidia.com/blog/scaling-autonomous-ai-agents-and-workloads-with-nvidia-dgx-spark/"
---

# Overview

**Source type: VENDOR.** NVIDIA wrote and measured everything here, to promote DGX Spark for agent workloads
(OpenClaw, NemoClaw). The numbers are useful because few others publish concurrency and 1→4-node scaling, but they are
not independently reproduced in the collected sources [nv-agents]. The [DGX Spark Handbook](/field-reports/exolabs-handbook.md)
relies on tables 3 and 5 below.

# Measured: long-context agent requests (one Spark)

128K-token prompt, 1K-token answer, batch size 1 [nv-agents].

| Model, engine | End-to-end (s) | Prompt processing (s) | Prefill (tok/s) | Decode (tok/s) |
|---|---|---|---|---|
| Nemotron 3 Super 120B NVFP4, TensorRT LLM | 99 | 44 | 2,855 | 18 |
| Qwen3.5 35B A3B FP8, vLLM | 73 | 41 | 3,080 | 35.75 |
| Qwen3 Coder Next 80B FP8, vLLM | 89 | 54 | 2,390 | 28.95 |

# Measured: concurrency (one Spark)

Qwen3 Coder Next FP8 on vLLM, 32K-token prompt, 1K-token answer [nv-agents].

| Simultaneous tasks | End-to-end (s) | Median TTFT (s) | Prefill (tok/s) | Decode (tok/s) |
|---|---|---|---|---|
| 1 | 35 | 9 | 3,261 | 38 |
| 2 | 54 | 12 | 5,363 | 47 |
| 4 | 91 | 15 | 9,616 | 53 |

NVIDIA's reading: four times the tasks take 2.6× the time [nv-agents]. The decode column is aggregate; per task it falls
from 38 to about 13 tok/s at four tasks (53 / 4).

# Measured: one, two and four nodes

Llama 3.3 70B Instruct NVFP4, TensorRT LLM, 32K input, 1K output, batch 1 [nv-agents].

| | 1 node TP1 | 2 nodes TP2 | 4 nodes TP4 |
|---|---|---|---|
| TTFT (ms) | 33,415 | 21,384 | 15,552 |
| TPOT (ms) | 269 | 133 | 72 |

Decode (TPOT) scales ~2× and ~3.7×; prefill (TTFT) only ~1.6× and ~2.1× [nv-agents]. Training scales better because nodes
sync once per step:

| Workload | 1 node | 2 nodes | 3 nodes | 4 nodes |
|---|---|---|---|---|
| Isaac Lab RL, FPS | 630 | 1,241 | — | 2,520 |
| Nanochat fine-tuning, tok/s | ~18,400 | ~35,900 | — | ~74,600 |
| Qwen3 4B DDP, samples/s | 2.03 | — | 6.12 | — |

# Supported topologies (NVIDIA's positioning)

| Topology | NVIDIA's stated use |
|---|---|
| 1 node | Low-latency large-context inference, fine-tuning up to 120B, local agents |
| 2 nodes | Inference up to 400B parameters, faster fine-tuning |
| 3 nodes in a ring | Fine-tuning larger models, small training jobs |
| 4 nodes with a 200 GbE RoCE switch | Inference up to 700B parameters |

[nv-agents]. See [three-node ring](/clustering/three-node-ring.md) and [switched fabric](/clustering/switched-fabric.md).

# What does not work well (NVIDIA's own words)

"Inference scaling is less than linear when the workload requires frequent, fine-grained communication between nodes… As
additional nodes are added, this overhead becomes increasingly dominant" [nv-agents]. A roofline comparison shows Spark
kernels further from their roofline than B200's, i.e. optimisation headroom remains on Spark [nv-agents].

# Takeaways

- The concurrency table is the best published model for "several developers on one Spark": four parallel 32K-context agent
  tasks finish in 91 s versus 35 s for one, with TTFT rising from 9 to 15 s. Usable, but per-user speed drops sharply.
- Long agent contexts (128K) cost 40–55 s of prompt processing per cold request on one Spark; prefix caching in a
  [vLLM](/stacks/vllm.md) setup matters more than raw decode speed.
- Two Sparks roughly halve per-token latency on a dense 70B; that is a vendor best case on TensorRT LLM, not what community
  vLLM recipes show (see [capetron six-node cluster](/field-reports/capetron-six-node-cluster.md)).
- Label every number from this page "NVIDIA-measured" when quoting it.
