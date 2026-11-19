---
type: runbook
title: Two Sparks over one DAC
description: Wire, address and prove a 2-node GB10 cluster on one QSFP112 cable — the minimal multi-Spark setup.
tags: [clustering, connectx-7, rdma, nccl, runbook]
resource: /clustering/two-node-dac.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [2-node cluster, Connect Two Sparks, direct-attach cluster]
entities:
  - label: QSFP112 DAC
    kind: cable
  - label: ib_write_bw
    kind: tool
  - label: gb10-cluster-check
    kind: tool
relations:
  - type: depends_on
    target: /hardware/gb10-platform.md
provenance:
  - source: https://build.nvidia.com/spark/connect-two-sparks
    note: NVIDIA official playbook (prerequisites, netplan, discover-sparks, rollback).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/02-two-and-three-nodes.md
    note: Field-tested addressing, MTU, persistence traps, link-check order.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/main/docs/04-validation.md
    note: RDMA validation commands and measured baselines.
citations:
  - id: nv-2s
    text: "NVIDIA, Connect Two Sparks playbook. https://build.nvidia.com/spark/connect-two-sparks"
  - id: cape-2n
    text: "Capetron, GB10 cluster guide — 02 Two and three nodes (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/main/docs/02-two-and-three-nodes.md"
  - id: cape-val
    text: "Capetron, GB10 cluster guide — 04 Validation (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/main/docs/04-validation.md"
  - id: cape-check
    text: "Capetron, gb10-cluster-check (MIT, read-only). https://github.com/capetron/gb10-cluster-check"
---

# Overview

Two GB10 units joined by **one QSFP112 cable** give one 200 Gb/s link made of two ~100 Gb/s PCIe halves
(see [GB10 platform](/hardware/gb10-platform.md)). NVIDIA rates the setup at about one hour including
validation, medium risk, reversible by removing the netplan file [nv-2s]. Three units is the
switchless ceiling (a ring, both ports used); a fourth needs a switch [cape-2n].

**What it buys:** room for models that do not fit in 128 GB (up to ~405B parameters on two units).
It does not make a model that already fits run faster, unless it is a mixture-of-experts model.

# Prerequisites

- Two GB10 systems on current OS and firmware, SSH and sudo on both, **the same username on both** [nv-2s].
- One approved QSFP112 DAC (0.4–0.5 m is enough side by side).
- Both units must sit close together: the cable is 0.5 m.

# Runbook

## 1. Cable

Plug the cable into the **same port on both units** (NVIDIA: avoids NCCL test issues) with the pull-tab
facing up; never force it [nv-2s]. Port 0 = left, next to the RJ-45. Check on both:

```bash
ibdev2netdev        # both halves of the cabled port must show (Up)
```

## 2. Addresses: one subnet per half, never a default route

Configure **both** halves, or you will measure ~111 Gb/s and wonder where the other half went [cape-2n].
On DGX Spark Founders Edition (netplan / systemd-networkd), node 1 — node 2 uses `.11`:

```yaml
# /etc/netplan/40-cx7.yaml   (chmod 600, then: sudo netplan apply)
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0f0np0:
      addresses: [192.168.100.10/24]
      mtu: 9000
      dhcp4: false
    enP2p1s0f0np0:
      addresses: [192.168.101.10/24]
      mtu: 9000
      dhcp4: false
```

> **NVIDIA vs field practice on MTU.** NVIDIA's playbook leaves the default MTU (1500) [nv-2s].
> Capetron sets **MTU 9000 on every fabric interface** and found that a 1500/9000 mismatch silently
> stalls NCCL bootstrap [cape-2n]. We follow Capetron, and prove it with the jumbo ping in step 4.

OEM units on NetworkManager (MSI and others) need one `nmcli` profile per half with
`ipv4.never-default yes`, and old carrier-down profiles must be brought down — they keep routes [cape-2n].

## 3. Passwordless SSH

```bash
bash ./discover-sparks    # NVIDIA script: finds both nodes, distributes keys [nv-2s]
ssh 192.168.100.11 hostname
```

## 4. Prove the link before any model

Run in this order; each step rules out a fault the next would misreport [cape-2n]:

| # | Check | Pass |
|---|---|---|
| 1 | `ethtool enp1s0f0np0 \| grep -E 'Speed\|Link'` (both halves) | `200000Mb/s`, `Link detected: yes` |
| 2 | `ip -br addr show enp1s0f0np0 enP2p1s0f0np0` and `ip route` | 2 addresses, 2 routes, no default route on fabric |
| 3 | `ping -M do -s 8972 -c 3 192.168.100.11` (and `.101.11`) | clean replies on both planes |
| 4 | RDMA bandwidth, one half then both (below) | ~111 Gb/s per half, ~196 Gb/s both |
| 5 | Same container image **digest** on both nodes | pinned digest, not a tag |

Or run all of 1–3 plus RoCE GID and NCCL variable checks at once with the read-only
`gb10-cluster-check --peer <half-A addr> --peer <half-B addr>` [cape-check].

RDMA bandwidth — start the server **detached**, or it dies with your SSH session and the client
reports "Couldn't connect", which looks like a firewall problem and is not [cape-val]:

```bash
# on node 2 (server)
nohup ib_write_bw -d rocep1s0f0 -x 3 -F -D 6 -s 65536 --report_gbits </dev/null >/tmp/ibw.log 2>&1 &
# on node 1 (client)
ib_write_bw -d rocep1s0f0 -x 3 -F -D 6 -s 65536 --report_gbits 192.168.100.11
```

`-x 3` is the RoCE v2 GID index; **it is not stable across nodes** — look it up under
`/sys/class/infiniband/<dev>/ports/1/gids/` and verify [cape-val]. For the both-halves figure run a second
pair on `roceP2p1s0f0` against the `.101` address at the same time and add the results.

## Expected numbers (direct cable)

| Test | Measured |
|---|---|
| One half | 111.86 Gb/s |
| Both halves at once | 98.04 + 98.04 = **196.08 Gb/s** (98 % of line rate) |
| One half, firmware-throttled NIC | 12.74 Gb/s — update OS + firmware, reboot, re-measure |

Source: [cape-val]. A single `iperf3` stream (~12 Gb/s) measures the Arm CPU, not the link.

## 5. Confirm the model really uses the fabric

Read the byte counters of the RDMA device before and after a serving run. If they did not move, NCCL fell
back to sockets over the management LAN — and a 27B model sharded that way over 10 GbE ran **3.6× slower
prefill and 2.4× slower decode** than on one unit [cape-2n].

# Rollback

```bash
sudo rm /etc/netplan/40-cx7.yaml && sudo netplan apply   # on both nodes [nv-2s]
```

# Limitations

- A bond over the two halves adds nothing for RDMA (NCCL uses both RDMA devices when listed in
  `NCCL_IB_HCA`) and is the thing that keeps stale routes [cape-2n].
- If a host firewall is on, multi-node vLLM needs full peer connectivity on both fabric subnets,
  not just the rendezvous port [cape-2n].
