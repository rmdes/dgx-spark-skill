---
type: runbook
title: Three Sparks in a ring
description: Wire, address and validate three GB10 units as a switchless ring of three QSFP cables, and what a third unit buys over two.
tags: [clustering, connectx-7, ring, rdma, nccl, runbook]
resource: /clustering/three-node-ring.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [3-node cluster, Connect Three Sparks, triangle, switchless ring]
entities:
  - label: QSFP112 DAC
    kind: cable
  - label: discover-sparks
    kind: tool
  - label: NVIDIA Sync Cluster Assistant
    kind: tool
relations:
  - type: extends
    target: /clustering/two-node-dac.md
  - type: depends_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /clustering/nccl-over-roce.md
  - type: validated_by
    target: /clustering/cluster-tooling.md
  - type: alternative_to
    target: /clustering/switched-fabric.md
provenance:
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/connect-three-sparks/README.md
    note: NVIDIA ring playbook (first published 2026-03-19) — wiring, netplan per node, discover-sparks, rollback.
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-three-sparks/README.md
    note: Updated ring playbook (2026-08-12) recommending the Sync Cluster Assistant.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/02-two-and-three-nodes.md
    note: Field-tested addressing schemes, persistence traps, link-check order.
  - source: https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold
    note: Measured 2-, 3- and 4-Spark decode for one recipe (what a third unit buys).
citations:
  - id: nv-3s
    text: "NVIDIA, Connect Three DGX Spark in a Ring Topology (playbook, 2026-03-19). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/connect-three-sparks/README.md"
  - id: nv-3s-v2
    text: "NVIDIA, Connect Three DGX Sparks in a Ring Topology (playbook, updated 2026-08-12). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-three-sparks/README.md"
  - id: nv-multi
    text: "NVIDIA, Connect Multiple DGX Sparks (playbook, updated 2026-09-24). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-multiple-sparks/README.md"
  - id: nv-rn
    text: "NVIDIA, DGX Spark Release Notes (June 2026 release). https://docs.nvidia.com/dgx/dgx-spark/release-notes.html"
  - id: nv-nccl
    text: "NVIDIA, NCCL for Multiple Sparks (playbook). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/nccl/README.md"
  - id: cape-2n
    text: "Capetron, GB10 cluster guide — 02 Two and three nodes (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/02-two-and-three-nodes.md"
  - id: cape-check
    text: "Capetron, gb10-cluster-check README (known issues). https://github.com/capetron/gb10-cluster-check"
  - id: exxact
    text: "Exxact, What You Need to Build a 4x NVIDIA DGX Spark Cluster. https://www.exxactcorp.com/blog/deep-learning/what-you-need-to-build-a-4x-nvidia-dgx-spark-cluster-switch-cabling-power"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
---

# Overview

Three GB10 units, three QSFP cables, no switch. Each unit uses **both** QSFP ports, and every
unit has a direct cable to every other unit, so the "ring" of three is also a full mesh [cape-2n].
NVIDIA publishes it as an official playbook: about one hour including validation, medium risk,
reversible by removing the netplan file [nv-3s]. Since the June 2026 release NCCL (2.30u1) has
"updated support" for the three-node ring, and the Sync Cluster Assistant configures it [nv-rn].

It is the step after the [two-Spark DAC demo](/clustering/two-node-dac.md): the demo pair plus one
unit and two more cables.

# What it enables

| Units | Pooled memory | NVFP4 model size (vendor rule of thumb) |
|---|---|---|
| 2 | 256 GB | up to ~400B |
| 3 | 384 GB | up to ~600B |

Source: Exxact, a reseller — treat the size column as a marketing estimate, not a measurement [exxact].

Measured, self-reported by the recipe author, same recipe (GLM-5.3-Flash EXL3 on TensorFold) [mia-glmf]:

| Sparks | 1 request, prose | 1 request, code | 4 requests, prose (combined) | Prefill, 32k prompt |
|---|---|---|---|---|
| 2 | 60.4 tok/s | n/p here | 108.8 tok/s | n/p here |
| 3 | 77.6 tok/s | 104.3 tok/s | 146.2 tok/s | 2,064 tok/s |

Three units also hold models two cannot: the full GLM-5.3 (~273 GiB checkpoint at 2.75 bpw,
~86 GiB of weights per Spark) serves at 31.3 tok/s prose with a 499,712-token window [mia-glm3].
See [GLM-5.3 family](/models/glm53-family.md) and the [models matrix](/models/spark-matrix.md).

# Prerequisites

- Three GB10 systems on the latest OS and firmware, SSH and sudo on all, **the same username on all** [nv-3s].
- Three QSFP112 DACs (see [GB10 platform](/hardware/gb10-platform.md) for approved parts). 0.5 m gives room
  for the longest run of the ring [cape-2n].

# Runbook

## 1. Cable: every cable joins a Port 0 to a Port 1

Port 0 is the cage next to the RJ-45 jack, Port 1 the one further away [nv-3s].

| Cable | From | To |
|---|---|---|
| 1 | Node 1, Port 0 | Node 2, Port 1 |
| 2 | Node 2, Port 0 | Node 3, Port 1 |
| 3 | Node 3, Port 0 | Node 1, Port 1 |

Wire Port 0 to Port 0 and every interface still shows Up, but the two ends of that cable sit in
different subnets of the playbook's addressing and ping fails [cape-2n] [cape-check]. On all nodes:

```bash
ibdev2netdev   # all four interfaces must be (Up): enp1s0f0np0, enP2p1s0f0np0, enp1s0f1np1, enP2p1s0f1np1
```

## 2. Address all four interfaces on every node

In a three-node ring all four interfaces on each node need an address [nv-3s]. Two options:

**a. NVIDIA Sync Cluster Assistant or the `spark_cluster_setup` script** — recommended by NVIDIA;
if Cluster Assistant reports success, skip the manual steps [nv-3s-v2]. See [cluster tooling](/clustering/cluster-tooling.md).

**b. Manual netplan.** NVIDIA's plan gives each cable two /24 subnets (one per PCIe half), so the
Port 0 of one node and the Port 1 it faces share them [nv-3s]:

| Subnet | Node 1 | Node 2 | Node 3 |
|---|---|---|---|
| 192.168.0.0/24 (cable 1, half A) | `enp1s0f0np0` .0.1 | `enp1s0f1np1` .0.2 | — |
| 192.168.1.0/24 (cable 1, half B) | `enP2p1s0f0np0` .1.1 | `enP2p1s0f1np1` .1.2 | — |
| 192.168.2.0/24 (cable 3, half A) | `enp1s0f1np1` .2.1 | — | `enp1s0f0np0` .2.2 |
| 192.168.3.0/24 (cable 3, half B) | `enP2p1s0f1np1` .3.1 | — | `enP2p1s0f0np0` .3.2 |
| 192.168.4.0/24 (cable 2, half A) | — | `enp1s0f0np0` .4.1 | `enp1s0f1np1` .4.2 |
| 192.168.5.0/24 (cable 2, half B) | — | `enP2p1s0f0np0` .5.1 | `enP2p1s0f1np1` .5.2 |

Node 1's file (nodes 2 and 3 follow the table) [nv-3s]:

```yaml
# /etc/netplan/40-cx7.yaml   (chmod 600, then: sudo netplan apply)
network:
  version: 2
  ethernets:
    enp1s0f0np0:   {dhcp4: false, addresses: [192.168.0.1/24]}
    enP2p1s0f0np0: {dhcp4: false, addresses: [192.168.1.1/24]}
    enp1s0f1np1:   {dhcp4: false, addresses: [192.168.2.1/24]}
    enP2p1s0f1np1: {dhcp4: false, addresses: [192.168.3.1/24]}
```

Field practice from Capetron adds `renderer: networkd`, `mtu: 9000`, `link-local: []` and `dhcp6: false`
per interface, never a default route on a fabric interface, and removal of older netplan fragments
that still assign old addresses [cape-2n]. On NetworkManager OEM units, use one `nmcli` profile per
interface with `ipv4.never-default yes` (see [Two Sparks over one DAC](/clustering/two-node-dac.md)).

> **MTU: sources disagree.** NVIDIA's multi-Spark playbook says use `--mtu 1500` for the three-node
> ring (MTU 9000 only for a two-node direct link) and that this matches what Cluster Assistant sets
> [nv-multi]. Capetron sets 9000 on every fabric interface and saw a 1500/9000 mismatch stall NCCL
> bootstrap [cape-2n]. Whichever you pick, it must be identical on every interface; prove it with
> `ping -M do -s 8972` if you choose 9000.

## 3. Passwordless SSH

```bash
curl -O https://raw.githubusercontent.com/NVIDIA/dgx-spark-playbooks/refs/heads/main/nvidia/connect-two-sparks/assets/discover-sparks
bash ./discover-sparks     # several IPs per node is expected (four addressed interfaces) [nv-3s]
ssh <IP for Node 2> hostname
```

## 4. Validate before any model

Same order as the two-node runbook, once per cable: link at 200G on both halves, addresses and
routes, ping (jumbo if MTU 9000), then RDMA bandwidth per half [cape-2n]. Then an NCCL all-gather
across the three nodes; the ring needs two extra variables [nv-nccl]:

```bash
export NCCL_IB_SUBNET_AWARE_ROUTING=1
export NCCL_NET_PLUGIN=none
mpirun -np 3 -H <mgmt1>:1,<mgmt2>:1,<mgmt3>:1 ... $HOME/nccl-tests/build/all_gather_perf
```

Full environment in [NCCL over RoCE](/clustering/nccl-over-roce.md).

# Rollback

```bash
sudo rm /etc/netplan/40-cx7.yaml && sudo netplan apply   # on all three nodes [nv-3s]
```

# Limitations

- Three is the full-mesh ceiling: each unit has two ports. A fourth unit cannot reach every other
  unit directly [cape-2n]. Options for four are in [Switched fabric](/clustering/switched-fabric.md),
  including the switchless four-node ring.
- A second cable between the same two units adds a link, not speed; configure both halves of the
  first cable instead [cape-check].
- The OpenZeka "3-Node AI Cluster Setup Guide" in our source set is a mis-clip of their 4-node
  (switched) guide; no OpenZeka three-node content was available to cite.
