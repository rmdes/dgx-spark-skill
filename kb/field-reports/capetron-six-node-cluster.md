---
type: report
title: "Field report: Petronella's six-node GB10 cluster on two MikroTik switches"
description: Petronella Technology Group's measured build of six GB10 workstations (4 MSI + 2 DGX Spark) on a switched 200G RoCE fabric — what broke, what it measured, and why six units serve as pools rather than one model.
tags: [field-report, self-reported, vendor-adjacent, cluster, switched-fabric, vllm, sm121, measured]
resource: /field-reports/capetron-six-node-cluster.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [gb10-cluster-guide, Petronella six-node cluster, capetron cluster guide]
entities:
  - label: Petronella Technology Group
    kind: organization
  - label: MikroTik CRS812-8DS-2DQ-2DDQ-RM
    kind: switch
  - label: MSI EdgeXpert MS-C931
    kind: system
  - label: gb10-cluster-check
    kind: tool
relations:
  - type: cites
    target: /clustering/switched-fabric.md
  - type: cites
    target: /clustering/nccl-over-roce.md
  - type: cites
    target: /clustering/two-node-dac.md
  - type: cites
    target: /stacks/vllm.md
  - type: cites
    target: /hardware/unified-memory-limits.md
  - type: cites
    target: /hardware/cost-and-bom.md
provenance:
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/README.md
    note: Guide overview and headline numbers (CC BY 4.0).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/03-switched-fabric.md
    note: Switch build and the four traps.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: vLLM on sm_121 patch chain, serving results, memory rules, six-node findings.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/06-bill-of-materials.md
    note: Fabric parts and prices, GB10 unit list prices observed June 2026.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/07-faq.md
    note: Short answers, including the H200 comparison.
citations:
  - id: cape-readme
    text: "Petronella Technology Group, Clustering NVIDIA GB10 workstations — README (CC BY 4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/README.md"
  - id: cape-sw
    text: "Petronella Technology Group, 03 The switched fabric (CC BY 4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/03-switched-fabric.md"
  - id: cape-serve
    text: "Petronella Technology Group, 05 Serving models across the fabric (CC BY 4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: cape-bom
    text: "Petronella Technology Group, 06 Bill of materials (CC BY 4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/06-bill-of-materials.md"
  - id: cape-faq
    text: "Petronella Technology Group, 07 FAQ (CC BY 4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/07-faq.md"
---

# Overview

**Source type: self-reported measurements by a company that sells the cluster cable** (disclosed: "That is why this guide
exists"). Every figure is backed by a command line and a date, and the authors invite corrections with raw output [cape-readme].
Treat cable recommendations as commercial; treat the measurements as the most detailed public multi-node GB10 data we have.

| Item | Detail |
|---|---|
| Who | Petronella Technology Group, Inc. (Raleigh, NC), cybersecurity/compliance firm running private AI for clients |
| Hardware | 6× GB10: 4× MSI EdgeXpert MS-C931 + 2× DGX Spark Founders Edition |
| Fabric | 2× MikroTik CRS812-8DS-2DQ-2DDQ-RM (RouterOS 7.24.1), QSFP56-DD → 2× QSFP56 breakouts, 200G inter-switch link, RoCE v2, MTU 9000, no PFC/ECN |
| Engine | vLLM with community sm_121 patch chains; NCCL over RoCE |
| Models | GLM-5.3-Flash NVFP4, Qwen3.8-Flash-Next NVFP4 |
| Period | August 2026 [cape-readme] |

# Measured: fabric

| Measurement | Result |
|---|---|
| Direct cable, one PCIe half, `ib_write_bw` | 111.86 Gb/s |
| Direct cable, both halves | 98.04 + 98.04 = 196.08 Gb/s |
| Through the switch ASIC, both halves | 196 Gb/s |
| Cross-switch over the ISL, one flow | 109.08 Gb/s |
| Six nodes, three concurrent pairs | 327.4 Gb/s aggregate |
| Second bridge on the switch (trap) | 196 → 4.85 Gb/s |

[cape-readme]. DGX Spark FE and MSI units measured the same [cape-faq]. See [switched fabric](/clustering/switched-fabric.md)
and [NCCL over RoCE](/clustering/nccl-over-roce.md).

# Measured: serving

All single-stream decode numbers are prose / code / math, temperature 0, 256 tokens, warm pass [cape-serve].

| Configuration | Decode (tok/s) | Prefill warm (tok/s) | Aggregate, 6 streams | KV cache (tokens) |
|---|---|---|---|---|
| GLM-5.3-Flash, 4 nodes TP4 | 26.5 / 38.1 / 46.7 | 3,840 | 91.2 | 2,246,948 |
| GLM-5.3-Flash, 2 nodes TP2, MTP-4 | 16.0 / 21.4 / 31.1 | 1,495 | 52.1 | 507,041 |
| Qwen3.8-Flash-Next, 1 node (n-gram table mmapped) | 24.8 / 31.1 / 33.8 | 2,376 | 86.4 | 296,636 |
| Qwen3.8-Flash-Next, 2 nodes TP2 | 35.3 / 36.0 / 53.2 | 2,303 | 118.1 | 1,850,932 |
| Qwen3.8-Flash-Next, 4 nodes TP4 + EP | 39.6 / 57.0 / 76.9 | 3,547 | 167.4 | 2,643,285 |
| Six nodes as three TP2 pairs (pool) | ~32–35 prose per pair | ~9,450 total | ~386 total (18 streams) | — |

Reference on the same harness: GLM-5.3-Flash FP8 on four H200 decodes at 233–339 tok/s single stream, about ten times four
GB10 [cape-serve]. The authors estimate four independent single-node Qwen endpoints would give ~345 tok/s aggregate against
167 for one TP4 + EP endpoint, trading per-stream speed and context for throughput [cape-serve].
See [Qwen3.8 Flash Next](/models/qwen38-flash-next.md) and [GLM-5.3 family](/models/glm53-family.md).

# What broke

| Problem | Fix / lesson |
|---|---|
| Stock vLLM image died five ways on sm_121 (attention backend gate, FlashInfer NaN at 64–256-row batches, silent NCCL downgrade 2.30.7 → 2.29.7, CUTLASS DSL mismatch, PDL race) | Community patch chain; "assume the image's attention backend selection, kernel library version, and NCCL version are all wrong until a multi-node run has produced a coherent answer" [cape-serve] |
| MikroTik DD breakout no link | Force 200G-baseCR4 on lane masters [cape-sw] |
| RSTP blocked the ISL; traffic detoured over the campus LAN at 4.47 Gb/s | Raise RSTP cost of second switch's uplink → 109.08 Gb/s [cape-sw] |
| Second bridge: 196 → 4.85 Gb/s | Switch chip offloads only one bridge [cape-sw] |
| GLM TP2 failed five boots at memory | Exact recipe KV setting; host memory floor 3–4% [cape-serve] |
| Qwen TP4 could not load (MoE kernel alignment) | `--enable-expert-parallel` [cape-serve] |
| Worker killed silently 7 s after KV allocation | `earlyoom` default 10% floor; check `journalctl -u earlyoom` [cape-serve] |
| One model cannot span six units (TP6 and PP fail) | Run pools of pairs; eight divides cleaner [cape-serve] |
| Firmware-throttled NIC at 12.74 Gb/s while showing 200G | OS/driver update; only RDMA tests reveal it [cape-faq] |

Memory rules from their logs: never `--gpu-memory-utilization 0.85` on a GB10; 0.65 for TP4 + EP, 0.72–0.75 for a
single-node endpoint; a memory guard on every rank; GPU allocations are not cgroup-charged [cape-serve]. See
[unified memory limits](/hardware/unified-memory-limits.md).

# Costs

Fabric only: 2 nodes $159; 3-node ring $435; 4 nodes on one switch $874 plus switch; 6 nodes $1,311–1,470 plus two
switches (Petronella's own cable prices) [cape-bom]. GB10 4 TB unit list prices seen June 2026: Gigabyte AI TOP ATOM $3,999,
ASUS Ascent GX10 ~$4,149, DGX Spark FE $4,699, MSI EdgeXpert ~$4,000; "raw performance is essentially equal" [cape-bom].
They recommend a smart PDU because the units have no BMC [cape-bom]. See [cost and BOM](/hardware/cost-and-bom.md).

# Verdict

"Clustering is a capacity play." Decode is bound by the 273 GB/s memory bus; tensor parallelism helps per-stream speed mainly
on MoE models [cape-faq]. Two nodes for GLM-5.3-Flash is "a 'free the other pair for something else' configuration, not a
faster one" [cape-serve].

# Minor inconsistency in the source

The FAQ says TP6 fails because "16 heads" are not divisible by 6; the serving chapter gives the error as "16 is not divisible
by 6" in the MoE kernels and states the model has 24 attention heads [cape-faq] [cape-serve]. The conclusion (no TP6) is the same.

# Takeaways

- For a team, **pools of independent units beat one giant model on aggregate throughput** (~386 tok/s across three pairs).
  With 3–4 Sparks, consider one pair for a big model plus single units for fast daily models.
- Budget engineer time: every new model on sm_121 needed patches, and the failures look like network or hardware faults.
  Pin vLLM images by digest: floating images changed behaviour and ran out of memory on a home Spark
  ([home Spark stack](/field-reports/our-home-spark-local-ai.md)).
- Stay at ≤3 units to avoid a switch; four or more means a 200G switch and its configuration traps.
- Remote power control (smart PDU) and memory guards are cheap and were learned the hard way; include them in the BOM.
