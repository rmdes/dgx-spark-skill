---
type: reference
title: Cluster tooling for GB10
description: The tools that set up, check and watch a multi-Spark cluster — NVIDIA Sync Cluster Assistant and discover-sparks, the read-only gb10-cluster-check, sparkrun, and the sparkDash dashboard.
tags: [clustering, tooling, monitoring, validation, reference]
resource: /clustering/cluster-tooling.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [gb10-cluster-check, Cluster Assistant, NVIDIA Sync, discover-sparks, sparkDash, sparkrun]
entities:
  - label: NVIDIA Sync Cluster Assistant
    kind: tool
  - label: discover-sparks
    kind: tool
  - label: gb10-cluster-check
    kind: tool
  - label: sparkrun
    kind: tool
  - label: sparkDash
    kind: dashboard
relations:
  - type: validates
    target: /clustering/two-node-dac.md
  - type: validates
    target: /clustering/three-node-ring.md
  - type: validates
    target: /clustering/switched-fabric.md
  - type: validates
    target: /clustering/nccl-over-roce.md
  - type: monitors
    target: /hardware/unified-memory-limits.md
  - type: monitors
    target: /hardware/power-and-thermals.md
provenance:
  - source: https://docs.nvidia.com/sync/latest/cluster-assistant.html
    note: NVIDIA Sync User Guide — Cluster Assistant steps, supported topologies, limits.
  - source: https://github.com/capetron/gb10-cluster-check
    note: gb10-cluster-check README (MIT, v0.1.0) — checks, sample output, known issues.
  - source: https://github.com/MiaAI-Lab/sparkDash/blob/d229bff50120f475274c28d4faf223fdbb56795a/README.md
    note: sparkDash README (Apache 2.0), version 2.70.0.
  - source: https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/
    note: OpenZeka's use of sparkrun for SSH mesh and CX7 configuration on a 4-node cluster.
citations:
  - id: nv-ca
    text: "NVIDIA, Cluster Assistant for Configuring a Multi-Node DGX Spark Cluster — NVIDIA Sync User Guide. https://docs.nvidia.com/sync/latest/cluster-assistant.html"
  - id: nv-rn
    text: "NVIDIA, DGX Spark Release Notes. https://docs.nvidia.com/dgx/dgx-spark/release-notes.html"
  - id: nv-multi
    text: "NVIDIA, Connect Multiple DGX Sparks (playbook, updated 2026-09-24). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-multiple-sparks/README.md"
  - id: nv-3s
    text: "NVIDIA, Connect Three DGX Spark in a Ring Topology (playbook). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/connect-three-sparks/README.md"
  - id: cape-check
    text: "Capetron, gb10-cluster-check (MIT, read-only). https://github.com/capetron/gb10-cluster-check"
  - id: sparkdash
    text: "MiaAI-Lab, sparkDash — multi-unit monitoring dashboard for NVIDIA DGX Spark (Apache 2.0). https://github.com/MiaAI-Lab/sparkDash/blob/d229bff50120f475274c28d4faf223fdbb56795a/README.md"
  - id: oz-4n
    text: "OpenZeka, DGX Spark 4-Node AI Cluster Setup Guide (2026-07-24). https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/"
---

# Overview

| Tool | Job | Changes the system? | Scope |
|---|---|---|---|
| NVIDIA Sync **Cluster Assistant** | Discover nodes, configure the ConnectX-7 network, speed-test links, set up SSH | Yes (netplan, SSH keys) | 2–4 DGX Spark/GB10 units [nv-ca] |
| `discover-sparks` | Node discovery and SSH key distribution | SSH keys only | Used in the 2- and 3-node playbooks [nv-3s] |
| `spark_cluster_setup` / `setup-cluster.sh` | Scripted network + SSH setup with `--dry-run` | Yes | 2, 3-ring, 4-ring, switch [nv-multi] |
| **gb10-cluster-check** | Read-only health check of the fabric on one node | No | Any GB10 [cape-check] |
| **sparkrun** | Cluster management, SSH mesh, CX7 config, launch model recipes | Yes | Used by OpenZeka on 4 nodes [oz-4n] |
| **sparkDash** | Live dashboard of GPU, unified memory, RoCE, LLM metrics; benchmarks | No (opt-in power/clock actions) | Any number of units [sparkdash] |

# NVIDIA Sync Cluster Assistant

Shipped in the June 2026 DGX OS release, in NVIDIA Sync **Settings → Cluster Assistant** [nv-rn].
NVIDIA's estimate: 10 minutes, low risk, versus about an hour for the manual path [nv-multi].

What it does, in order [nv-ca]:

1. Device checks: SSH reachable, GB10 hardware, minimum OS (April 2026 release or later), sudo.
2. Username/UID/GID check, with an offer to standardize them.
3. Network check: detects interfaces and cabling, warns if a link is not 200 Gbit/s.
4. **Link speed test** per link against a lower bound of **184 Gbit/s**.
5. Key-based SSH with per-node aliases (five-minute timeout per machine).

Limits [nv-ca]:

- 2–4 devices. Direct cabling for 2 or 3 units; four units **require a switch** in Cluster Assistant.
- No mixed topologies, one cable per link, GB10/DGX Spark only.
- Network only: it does not set up inference, Slurm or Kubernetes.
- To add a node you delete the cluster and recreate it.

# discover-sparks

NVIDIA's script from the two- and three-node playbooks: finds the other Sparks and sets up
bidirectional passwordless SSH; prompts for each node's password the first time [nv-3s].

```bash
curl -O https://raw.githubusercontent.com/NVIDIA/dgx-spark-playbooks/refs/heads/main/nvidia/connect-two-sparks/assets/discover-sparks
bash ./discover-sparks
```

# gb10-cluster-check

A Python-stdlib, read-only check from Capetron (MIT). Every command is a query; one PASS/WARN/FAIL/SKIP
line per check, `--json`, exit code 1 on any FAIL [cape-check].

```bash
git clone https://github.com/capetron/gb10-cluster-check.git && cd gb10-cluster-check
./gb10-cluster-check --peer <half-A peer> --peer <half-B peer>
sudo ./gb10-cluster-check                    # adds the cable EEPROM check
./gb10-cluster-check --peer <peer> --bw      # after starting ib_write_bw / iperf3 servers on the peer
```

What it catches [cape-check]:

| Check | Fails or warns on |
|---|---|
| Link, both PCIe halves | one half down, below 200G, link drops since boot (warns above 3) |
| RDMA counters | more than 1,000 `packet_seq_err` / `out_of_sequence` since boot |
| Cable EEPROM (root) | not QSFP, longer than 3 m, below 200G |
| MTU | differs across fabric interfaces (fail), below 9000 (warn) |
| Addressing | both halves in one subnet, default route via fabric, route into a carrier-down interface |
| Peers | unreachable, or small ping passes and jumbo ping fails |
| RoCE GID / NCCL env | no RoCE v2 GID for the IPv4; `NCCL_IB_HCA` lists only one half; GID index mismatch |
| `--bw` | RDMA below ~95 Gb/s for one half (FAIL below 50) |

In its published sample run it found a link at 200G that had dropped and come back **21 times since
boot**, invisible to normal status commands [cape-check].

# sparkrun

OpenZeka installs it with `uvx sparkrun setup`; the wizard takes node IPs, a cluster name and SSH
user, builds the SSH mesh, configures CX7 networking, adds the user to the docker group and offers to
install **earlyoom**. It does not configure DCB/PFC on the Sparks [oz-4n]. Models are launched from a
recipe YAML with `sparkrun run <recipe>.yaml` [oz-4n].

# sparkDash

A web dashboard (React 19 / Express 5, Docker) for one or many Sparks over SSH, by Mia's AI Lab;
README at version 2.70.0 [sparkdash]. Relevant for a team cluster:

- **Unified memory** view (GB10 128 GB pool, GPU/CPU split) and health findings: GPU hot at 85/90 °C,
  unified memory low (warns under 3 GB, critical under 1.5 GB), Xid errors, kernel OOM kills [sparkdash].
- **RoCE / RDMA panel** per port: link rate, MTU, traffic, drops, PFC/DSCP, `out_of_buffer`, sequence
  errors, CNPs; alerts when a RoCE link goes down or loss counters keep rising. No switch telemetry [sparkdash].
- **LLM probe** auto-detects vLLM, SGLang, llama.cpp, TensorFold, EXL3 and others; decode, prefill
  (1k–300k sweep) and a seeded **quality bench** (GSM8K, MMLU samples and more) [sparkdash].
- Head/worker roles, Prometheus `/metrics` export, fleet energy and token totals, GPU clock cap [sparkdash].
- Wake-on-LAN does **not** wake a DGX Spark from a magic packet [sparkdash].

The [models matrix](/models/spark-matrix.md) figures are sparkDash measurements.

# Limitations

- Cluster Assistant and NVIDIA's helper top out at four nodes through a switch; larger clusters are
  manual [nv-ca] [nv-multi].
- gb10-cluster-check `--bw` never starts anything on the peer; you start the one-shot servers yourself [cape-check].
