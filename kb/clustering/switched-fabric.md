---
type: runbook
title: Four or more Sparks — switch or switchless ring
description: How to join four or more GB10 units — a MikroTik CRS812 200G switch with its breakout, RSTP and second-bridge traps, or the switchless four-node ring used by community TP4 recipes.
tags: [clustering, switch, mikrotik, roce, ring, runbook]
resource: /clustering/switched-fabric.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [switched fabric, 4-node cluster, MikroTik CRS812, switchless four-node ring]
entities:
  - label: MikroTik CRS812-8DS-2DQ-2DDQ-RM
    kind: network_switch
  - label: MikroTik CRS804-4DDQ-hRM
    kind: network_switch
  - label: QSFP56-DD to 2x QSFP56 breakout DAC
    kind: cable
  - label: patched NCCL (skip-tree-connect)
    kind: library
relations:
  - type: extends
    target: /clustering/three-node-ring.md
  - type: depends_on
    target: /clustering/nccl-over-roce.md
  - type: validated_by
    target: /clustering/cluster-tooling.md
  - type: costed_in
    target: /hardware/cost-and-bom.md
  - type: enables
    target: /models/deepseek-v4-family.md
  - type: enables
    target: /models/glm53-family.md
  - type: reported_by
    target: /field-reports/capetron-six-node-cluster.md
  - type: reported_by
    target: /field-reports/alex-ellis-four-sparks.md
provenance:
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/03-switched-fabric.md
    note: Six GB10 units on two CRS812 switches, RouterOS 7.24.1 — configuration and traps (builds 2026-08-17 to 2026-08-31).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/04-validation.md
    note: RDMA matrix through the switch and across the inter-switch link.
  - source: https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/
    note: OpenZeka 4-node CRS812 build with RoCE QoS (PFC/ECN) and a 4-node GLM-5.2 benchmark.
  - source: https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/README.md
    note: Switchless four-node ring recipe (Alex Ellis / OpenFaaS) and UK switch prices, 2026-08-31.
  - source: https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold
    note: DeepSeek V4.1 Flash on four Sparks, measured on a switchless ring 2026-10-25.
citations:
  - id: cape-sw
    text: "Capetron, GB10 cluster guide — 03 The switched fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/03-switched-fabric.md"
  - id: cape-val
    text: "Capetron, GB10 cluster guide — 04 Validation (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/04-validation.md"
  - id: cape-2n
    text: "Capetron, GB10 cluster guide — 02 Two and three nodes (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/02-two-and-three-nodes.md"
  - id: petro-sw
    text: "Petronella, From Two DGX Sparks to a Switched Fabric (2026-09-05). https://petronellatech.com/blog/dgx-spark-cluster-from-two-sparks-to-a-switched-fabric/"
  - id: nv-multi-web
    text: "NVIDIA, Connect Multiple DGX Sparks for Distributed Workloads (build.nvidia.com). https://build.nvidia.com/spark/multi-sparks-through-switch"
  - id: nv-multi
    text: "NVIDIA, Connect Multiple DGX Sparks (playbook, updated 2026-09-24). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-multiple-sparks/README.md"
  - id: nv-ca
    text: "NVIDIA, Cluster Assistant — NVIDIA Sync User Guide. https://docs.nvidia.com/sync/latest/cluster-assistant.html"
  - id: exxact
    text: "Exxact, What You Need to Build a 4x NVIDIA DGX Spark Cluster. https://www.exxactcorp.com/blog/deep-learning/what-you-need-to-build-a-4x-nvidia-dgx-spark-cluster-switch-cabling-power"
  - id: sth-crs812
    text: "ServeTheHome, MikroTik CRS812-8DS-2DQ-2DDQ-RM review (2025-10-23). https://www.servethehome.com/mikrotik-achieves-400gbe-in-our-mikrotik-crs812-8ds-2dq-2ddq-rm-review-keysight-cyperf-arm-marvell/"
  - id: oz-4n
    text: "OpenZeka, DGX Spark 4-Node AI Cluster Setup Guide (2026-07-24). https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/"
  - id: ae-ring
    text: "Alex Ellis / MiaAI-Lab, GLM-5.3-Flash NVFP4 — 4x DGX Spark switchless ring. https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/README.md"
  - id: ae-fabric
    text: "Alex Ellis / MiaAI-Lab, The ring fabric — addressing template and MTU. https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/fabric.md"
  - id: ae-switches
    text: "Alex Ellis / MiaAI-Lab, Switched alternatives (prices checked 2026-08-31). https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/switches.md"
  - id: ae-blog
    text: "Alex Ellis, How and Why We Bought 4x DGX Sparks (2026-09-15). https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: cape-check
    text: "Capetron, gb10-cluster-check README (known issues). https://github.com/capetron/gb10-cluster-check"
---

# Overview

A GB10 has two QSFP ports, so three units is the last size where every unit has a cable to every
other [cape-2n]. For four or more there are two working answers:

| Option | Hardware | Who supports it | Measured |
|---|---|---|---|
| **200G switch** | 1 switch for 4–6 units, 2 for up to 8; breakout DACs | NVIDIA playbook and Cluster Assistant up to 4 [nv-multi-web] [nv-ca]; 6 on two switches is Capetron's own build [cape-sw] | 196 Gb/s per node through the switch ASIC [cape-val] |
| **Switchless 4-node ring** | 4 cables, no switch | NVIDIA playbook (manual path only, 2026-09-24) [nv-multi]; community TP4 recipes [ae-ring] [mia-ds4] | DeepSeek V4.1 Flash 65.8 tok/s, GLM-5.3-Flash 95.2 tok/s single stream [mia-ds4] [mia-glmf] |

> **Sources disagree on "four needs a switch".** Capetron's guide, gb10-cluster-check and the
> Cluster Assistant documentation say four units require a switch [cape-2n] [cape-check] [nv-ca].
> NVIDIA's newer multi-Spark playbook (updated 2026-09-24) lists a four-device direct ring for the
> manual path [nv-multi], and Petronella's 2026-09-05 post (updated) reports NVIDIA's 2026-10-22 results
> with four- and eight-node rings [petro-sw]. The ring works for tensor-parallel inference, where each
> rank talks to its neighbours; stock NCCL wants a path between every pair, so the ring needs NCCL
> patches or relaying [cape-check] [ae-ring].

# Option A — a 200G switch (MikroTik CRS812)

## Choice

Capetron chose the **MikroTik CRS812-8DS-2DQ-2DDQ-RM** (RouterOS 7.24.1): public report of a
2 × 200G breakout working with GB10, no vendor-locked optics or DACs [cape-sw]. Ports: 2 × 400G
QSFP56-DD, 2 × 200G QSFP56, 8 × 50G SFP56, 2 × 10G RJ-45 [cape-sw]. ServeTheHome measured it doing
400GbE; it has dual 250 W PSUs and four hot-swap fans, "on the verge" of desk-tolerable except with
high-power optics [sth-crs812].

| Nodes | Switches | How [cape-sw] |
|---|---|---|
| 4 | 1 | Both DD ports broken out to 4 × 200G legs |
| 5–6 | 1 | Breakouts plus the two native QSFP56 ports |
| 5–8 | 2 | Breakouts on both, native ports used for the inter-switch link (ISL) |

Other switches people use: the half-width **CRS804-4DDQ-hRM** (4 × 400G QSFP56-DD, ~92 W typical /
~123 W load) in Exxact's 4-node build [exxact]; Capetron has no measurements on it [cape-sw].
Prices are in [Cost and bill of materials](/hardware/cost-and-bom.md).

Per node: one 0.5 m QSFP112 DAC from the node's Port 0 into one QSFP56 leg of a QSFP56-DD to
2 × QSFP56 breakout DAC (NADDOD Q2Q56-400G-CU1, MikroTik-coded) [cape-sw].

## Step 1 — force the breakout to 200G (it does not auto-negotiate)

With a breakout plugged in, the CRS812 reports auto-negotiation failed and no link. Set the speed on
the lane-master interfaces (lanes 1 and 5) [cape-sw]:

```
/interface/ethernet
set qsfp56-dd-1-1 auto-negotiation=no speed=200G-baseCR4
set qsfp56-dd-1-5 auto-negotiation=no speed=200G-baseCR4
set qsfp56-dd-2-1 auto-negotiation=no speed=200G-baseCR4
set qsfp56-dd-2-5 auto-negotiation=no speed=200G-baseCR4
/interface/ethernet/monitor qsfp56-dd-1-1 once   # expect link-ok, rate 200Gbps, fec91
```

Exxact reports auto-negotiation "often" lands at 50 Gb/s on the CRS804 too; set 200G manually [exxact].

## Step 2 — jumbo frames on the switch ports, not only the hosts

```
/interface/ethernet
set qsfp56-dd-1-1,qsfp56-dd-1-5,qsfp56-dd-2-1,qsfp56-dd-2-5,qsfp56-2-1 l2mtu=9216 mtu=9000
```

The offloaded forwarding path uses the port l2mtu, not the bridge's [cape-sw]. OpenZeka uses
`l2mtu=9500 mtu=9000` [oz-4n]. Prove with `ping -M do -s 8972` between every pair on both planes.

> NVIDIA's playbook says "keep the default MTU for switch connections" and its script uses 1500 for
> switch layouts [nv-multi]; Capetron and OpenZeka run 9000 end to end. See
> [NCCL over RoCE](/clustering/nccl-over-roce.md).

## Step 3 — one hardware-offloaded bridge (the 196 → 5 Gb/s trap)

The CRS812's Marvell Prestera chip hardware-offloads **only one bridge**. Putting the fabric in a
second bridge sends it through the switch CPU [cape-sw]:

| Path | One bridge | Second bridge |
|---|---|---|
| MSI pair through switch A, both halves | 196 Gb/s | 4.85 Gb/s |
| DGX Spark pair through switch B | 109 Gb/s | 4.9 Gb/s |
| iperf3 TCP | 93 Gb/s | 8.8 Gb/s |

Keep all fabric legs and the ISL in the main bridge with `hw=yes`; isolate with VLAN filtering inside
that bridge if needed (offloaded) [cape-sw]. NVIDIA's playbook now also says to confirm Spark-facing
ports use the switch chip, not the switch CPU [nv-multi].

## Step 4 — two switches: the RSTP trap on the ISL

If both switches also uplink to the campus LAN, RSTP blocks the ISL and fabric traffic detours over
the campus at 2.5 Gb/s and MTU 1500: cross-switch RDMA measured **4.47 Gb/s** [cape-sw]. Fix by
pricing out the second switch's campus uplink so the ISL becomes its root port:

```
# on the second switch only
/interface/bridge/port
set [find interface=ether1] path-cost=200000000 internal-path-cost=200000000
```

Cross-switch RDMA then measured 109.08 Gb/s. RSTP is VLAN-blind; a fabric VLAN alone does not
unblock the ISL. Put management addresses on the bridge interface [cape-sw].

## Optional — RoCE QoS (PFC/ECN)

Capetron ran with **no PFC and no ECN** and reached line rate in every test, including two 100G
senders sharing one ISL direction (81.9 + 81.9 Gb/s fair split) [cape-sw] [cape-val]. OpenZeka
configures DSCP 26 → TC3, PFC on TC3, ECN, CNP on TC6 and `qos-hw-offloading=yes` on the switch, plus
`dcb` DSCP/PFC on each Spark via a systemd unit [oz-4n]. Not needed at four nodes per Capetron;
OpenZeka did not publish a with/without comparison.

## Measured through the switch

| Test (`ib_write_bw`) | Result |
|---|---|
| Direct cable, one half (baseline) | 111.86 Gb/s |
| Through one switch, both halves | 98.0 + 98.0 = 196 Gb/s |
| Through switch, one half (DGX Spark pair) | 109.11 Gb/s (switch costs ~0.7 %) |
| Three intra-switch pairs at once | 327.8 Gb/s aggregate |
| One flow across the ISL | 109.08 Gb/s |

Source: [cape-val]. OpenZeka reports ~100–111 Gb/s per subnet and 1–3 µs `ib_write_lat` on their
4-node CRS812 build [oz-4n].

# Option B — switchless four-node ring

Four cables, each Spark to its two neighbours; the two diagonal pairs have no cable and relay
through a neighbour [ae-fabric]. NVIDIA's wiring for the manual path: Spark N Port 0 → Spark N+1
Port 1, Spark 4 Port 0 → Spark 1 Port 1 [nv-multi].

What it takes, from the Alex Ellis / OpenFaaS recipe (GLM-5.3-Flash TP4) [ae-ring] [ae-fabric]:

- A **patched NCCL 2.30.7** with *skip-tree-connect*, `LD_PRELOAD`-ed into every container: stock
  NCCL's tree-connect step wedges on a switch-free point-to-point fabric.
- One /24 per ring edge, both rails in `NCCL_IB_HCA`, IP forwarding and `DOCKER-USER` accept rules
  for the relay. All of it is **runtime-only**: re-run `fabric-setup.sh` after every reboot and any
  docker churn.
- MTU 9000 on both rails; at 1500 "decode is roughly 2.7× slower" with no error.
- A passing jumbo ping does not prove the RDMA relay works; only a completed NCCL collective does.
- First ring all-reduce occasionally deadlocks with no error; tear down all four ranks and relaunch.
- That recipe runs on 0.4–0.5 m Amphenol **100G QSFP28** DACs, not the 200G QSFP112 cable [ae-fabric].

The DeepSeek V4.1 Flash 4× recipe ships both `./start.sh` (switch) and `./start-switchless.sh`
(ring); on a ring it places nodes in a 2 × 2 grid so every partner pair has its own cable [mia-ds4].

Measured on a switchless ring (self-reported, median of three, 2026-10-25) [mia-ds4]:

| Concurrent requests | Aggregate decode, prose | Per request | First token |
|---|---|---|---|
| 1 | 65.8 tok/s | 65.8 | 186 ms |
| 4 | 130.5 tok/s | 34.1 | 499 ms |
| 8 | 165.3 tok/s | 21.7 | 901 ms |

Prefill 4,127 tok/s on a 32k prompt. The author notes "these numbers are this fabric's, not a
switch's" — a switch removes the one relayed hop [mia-ds4]. Alex Ellis reports the patched ring
"seems to be on par with a switched setup" — not a side-by-side measurement [ae-blog].

# What a switch costs you

- Money and lead time: see [Cost and bill of materials](/hardware/cost-and-bom.md). On 2026-08-31 the
  cheapest UK MikroTik option was out of stock and the CRS804 was pre-order only [ae-switches].
- Time: four non-obvious configuration steps, each of which "cost us a session" [cape-sw].
- Noise and rack space: the CRS812 is 1U full-width with four fans, best racked [sth-crs812] [ae-switches].
- What it buys back: any-to-any traffic, pools of pairs, and growth past four without re-cabling
  [ae-switches] [petro-sw].

# Limitations

- Six-node (two-switch) layouts are Capetron's measured configuration, not an NVIDIA reference design [cape-sw].
- The four-node ring is NVIDIA-listed only for the manual path; Cluster Assistant does not configure it [nv-ca] [nv-multi].
- Moving a node between switch legs bounces its fabric; stop multi-node models first [cape-sw].
