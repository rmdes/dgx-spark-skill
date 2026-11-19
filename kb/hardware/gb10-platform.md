---
type: hardware
title: GB10 platform (DGX Spark and OEM twins)
description: What every GB10 workstation is — 128 GB unified memory at 273 GB/s, a 20-core Arm CPU, and a ConnectX-7 NIC with two 200 Gb/s QSFP ports.
tags: [gb10, dgx-spark, connectx-7, memory-bandwidth]
resource: /hardware/gb10-platform.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [DGX Spark, GB10 Grace Blackwell]
entities:
  - label: NVIDIA GB10
    kind: system_on_chip
  - label: ConnectX-7
    kind: network_controller
relations:
  - type: enables
    target: /clustering/two-node-dac.md
  - type: hosts
    target: /models/qwen38-27b-1x-tensorfold.md
provenance:
  - source: https://docs.nvidia.com/dgx/dgx-spark/hardware.html
    note: NVIDIA DGX Spark User Guide, Hardware Overview (specs, power, ports).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/01-hardware.md
    note: Capetron GB10 cluster guide, measured link and memory figures across 6 units.
citations:
  - id: nv-hw
    text: "NVIDIA, DGX Spark User Guide — Hardware Overview. https://docs.nvidia.com/dgx/dgx-spark/hardware.html"
  - id: nv-cx7
    text: "NVIDIA, DGX Spark User Guide — ConnectX-7 Networking. https://docs.nvidia.com/dgx/dgx-spark/spark-clustering.html"
  - id: cape-hw
    text: "Capetron, GB10 cluster guide — 01 Hardware (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/main/docs/01-hardware.md"
---

# Overview

Every GB10 workstation, whatever the badge, is built on the same chip: NVIDIA's GB10 Grace Blackwell
system-on-chip with 128 GB of unified memory and a ConnectX-7 NIC behind two QSFP ports.
Besides NVIDIA's DGX Spark Founders Edition, the same platform ships as ASUS Ascent GX10,
Dell Pro Max with GB10, HP ZGX Nano G1n, Lenovo ThinkStation PGX, MSI EdgeXpert MS-C931,
Acer Veriton GN100 and Gigabyte AI TOP ATOM. Cables and clustering procedures apply to all of them [cape-hw].

Same chip does not yet mean same speed: the board, BIOS, embedded controller and DRAM vendor differ per OEM. In the author's own
measurements a Dell Pro Max GB10 ran the same model 16–35 % slower than an NVIDIA Founders Edition with identical driver,
VBIOS, OS and vLLM setup; the cause is not established (raw numbers in `benchmarks/`, summary in the
[matrix](/models/spark-matrix.md)). Benchmark a unit before buying more of the same model.

# Specifications

| Component | Value |
|---|---|
| GPU | Blackwell, 5th-gen Tensor Cores (FP4), 6,144 CUDA cores |
| AI compute | Up to 1 PFLOP FP4 with sparsity |
| CPU | 20-core Arm (10 Cortex-X925 + 10 Cortex-A725) |
| Memory | 128 GB LPDDR5x unified, 256-bit, **273 GB/s** |
| Storage | 1 TB or 4 TB NVMe M.2, self-encrypting |
| Network | 10 GbE RJ-45, ConnectX-7 with **2× QSFP** (Ethernet only), Wi-Fi 7 |
| Power | 240 W external supply (required); GB10 SoC TDP 140 W |
| Size | 150 × 150 × 50.5 mm, 1.2 kg |

NVIDIA rates one unit for models up to about 200B parameters and two linked units up to 405B [nv-hw].

# The one ratio that explains everything

Memory inside the box runs at 273 GB/s; the fastest path to the next box is 200 Gb/s, about
25 GB/s before overhead. Local memory is roughly **eleven times faster than the fabric** [cape-hw].
Consequences:

- **Decode on one unit is memory-bandwidth bound.** A dense 27B model in FP8 (~29 GB of weights)
  decodes at about 8.3 tok/s, close to the 273 / 29 ≈ 9.4 tok/s ceiling [cape-hw]. Smaller weights
  (4-bit) and speculative decoding are what move this number — see
  [Qwen3.8 27B on one Spark](/models/qwen38-27b-1x-tensorfold.md), which reaches 58.3 tok/s.
- **Clustering buys capacity, not raw speed.** It fits bigger models; it does not turn 25 GB/s into
  273 GB/s. Mixture-of-experts models are the ones that also gain per-stream speed.

# The QSFP ports

Each port is rated **up to 200 Gb/s**, and the reason is structural: the ConnectX-7 reaches the SoC
over two independent PCIe Gen5 x4 links, so each physical port shows up in Linux as **two Ethernet
interfaces and two RDMA devices**, each good for about 100 Gb/s [nv-cx7].

| Port (seen from the back) | Ethernet interfaces | RDMA devices |
|---|---|---|
| Left, port 0 (next to RJ-45) | `enp1s0f0np0`, `enP2p1s0f0np0` | `rocep1s0f0`, `roceP2p1s0f0` |
| Right, port 1 | `enp1s0f1np1`, `enP2p1s0f1np1` | `rocep1s0f1`, `roceP2p1s0f1` |

The two names of a pair are **the same wire**. Only traffic on both halves at once reaches ~200 Gb/s.

# Cables

Approved: Amphenol NJAAKK-N911 (0.4 m) and NJAAKK0006 (0.5 m), Luxshare LMTQF022-SD-R (0.4 m) [nv-cx7].
They are **QSFP112 DACs rated 400G, negotiated at 200G** by this NIC: the 400G rating is headroom,
not speed you get [cape-hw]. Lengths: 0.5 m side by side or stacked, 1 m around a monitor, 2 m across shelves.

# Limitations

- **Open conflict on per-port bandwidth.** ServeTheHome's launch review (October 2025) saw a single PCIe Gen5 x4 link to
  the ConnectX-7 and ~96 Gb/s of iperf3 traffic whether one or both ports were used
  ([ServeTheHome review](/field-reports/servethehome-review.md)). NVIDIA's guide describes two x4 links [nv-cx7], and
  Capetron measured 196 Gb/s with RDMA on both PCIe halves in August 2026 [cape-hw], after driver updates that took one
  of its links from 13 to 112 Gb/s. Neither source explains the other's figure. Settle it on your own units: run
  `ib_write_bw` on both halves at once ([two-node runbook](/clustering/two-node-dac.md)).
- Single TCP streams top out near 12 Gb/s on the Arm cores — not a fabric measurement.
- A firmware power-throttled ConnectX-7 has been seen at 12.74 Gb/s while every status tool showed a
  healthy 200G link; only an RDMA bandwidth test reveals it [cape-hw]. See the validation steps in
  [Two Sparks over one DAC](/clustering/two-node-dac.md).
