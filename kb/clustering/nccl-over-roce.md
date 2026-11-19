---
type: reference
title: NCCL over RoCE on GB10
description: The NCCL environment that makes multi-Spark collectives use the 200G RoCE fabric (HCAs, GID index, socket interface, ring variables) and the known traps.
tags: [nccl, roce, rdma, clustering, reference, vllm]
resource: /clustering/nccl-over-roce.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [NCCL environment, NCCL_IB_HCA, RoCE v2 GID index, nccl-tests]
entities:
  - label: NCCL
    kind: library
  - label: nccl-tests
    kind: benchmark
  - label: ib_write_bw
    kind: tool
relations:
  - type: depends_on
    target: /hardware/gb10-platform.md
  - type: used_by
    target: /clustering/two-node-dac.md
  - type: used_by
    target: /clustering/three-node-ring.md
  - type: used_by
    target: /clustering/switched-fabric.md
  - type: used_by
    target: /stacks/vllm.md
  - type: related_to
    target: /stacks/sparkring-sparkcache.md
  - type: validated_by
    target: /clustering/cluster-tooling.md
provenance:
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: "The section NCCL over RoCE, the environment that works — vLLM launchers on 4 and 6 GB10 units (August 2026)."
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/nccl/README.md
    note: NVIDIA NCCL playbook — build for sm_121, nccl-tests, ring variables.
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-nccl/README.md
    note: Updated NCCL playbook (2026-10-14), NCCL v2.31.2-1, nccl-tests pinned v2.19.7.
  - source: https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/nccl/README.md
    note: Patched NCCL runtime contract for direct pairs and four-rank direct-cable cycles.
citations:
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: cape-val
    text: "Capetron, GB10 cluster guide — 04 Validation (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/04-validation.md"
  - id: cape-2n
    text: "Capetron, GB10 cluster guide — 02 Two and three nodes (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/02-two-and-three-nodes.md"
  - id: nv-nccl
    text: "NVIDIA, NCCL for Multiple Sparks (playbook, 2025-12-15). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/nccl/README.md"
  - id: nv-nccl-v2
    text: "NVIDIA, Set Up NCCL for Multi-Node GPU Communication (playbook, 2026-10-14). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-nccl/README.md"
  - id: nv-multi
    text: "NVIDIA, Connect Multiple DGX Sparks (playbook, updated 2026-09-24). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-multiple-sparks/README.md"
  - id: sr-nccl
    text: "MiaAI-Lab sparkring, Patched NCCL fallback. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/nccl/README.md"
  - id: sr-cable
    text: "MiaAI-Lab sparkring, Direct-cable qualification. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/spark_transport/CABLE_QUALIFICATION.md"
  - id: ae-recipe
    text: "Alex Ellis / MiaAI-Lab, GLM-5.3-Flash 4x switchless recipe. https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/recipe.md"
  - id: oz-4n
    text: "OpenZeka, DGX Spark 4-Node AI Cluster Setup Guide (2026-07-24). https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/"
  - id: cape-check
    text: "Capetron, gb10-cluster-check README (known issues). https://github.com/capetron/gb10-cluster-check"
---

# Overview

NCCL is the collective library vLLM, SGLang and TensorFold use to talk across Sparks. On GB10 it must
be told explicitly to use the ConnectX-7 RDMA devices; otherwise it can **silently fall back to
sockets over the management LAN** [cape-serve]. Capetron measured what that costs: a dense 27B FP8 model
went from 1,963 / 8.3 tok/s (prefill / decode, one unit) to 539 / 3.5 tok/s sharded over 10 GbE
[cape-2n].

Each QSFP port is two PCIe halves, each with its own RDMA device (`rocep1s0f0` and `roceP2p1s0f0`
for Port 0); see [GB10 platform](/hardware/gb10-platform.md).

# The variables that matter

| Variable | Value on GB10 | Why |
|---|---|---|
| `NCCL_NET` | `IB` | Force the RDMA transport; `NCCL_IB_DISABLE=1` alone still probes ibverbs [cape-serve] |
| `NCCL_IB_DISABLE` | `0` | [cape-serve] |
| `NCCL_IB_HCA` | `rocep1s0f0,roceP2p1s0f0` (both halves) or one device | Both halves are needed for ~200 Gb/s; one device caps NCCL near 100 Gb/s [cape-check] |
| `NCCL_IB_GID_INDEX` | look it up (was `3` on every Capetron unit) | RoCE v2 GID that maps to the half's IPv4; **not stable across nodes** [cape-val] |
| `NCCL_IB_ROCE_VERSION_NUM`, `NCCL_IB_ADDR_FAMILY` | `2`, `AF_INET` | [cape-serve] |
| `NCCL_SOCKET_IFNAME` (+ `GLOO_`, `TP_`) | a fabric interface, e.g. `enp1s0f0np0` — or the management NIC on a ring | Bootstrap only; it must exist and route, not be fast [cape-2n] [sr-nccl] |
| `NCCL_CUMEM_ENABLE` | `0` | [cape-serve] [sr-nccl] |
| `NCCL_NVLS_ENABLE`, `NCCL_CROSS_NIC`, `NCCL_IB_MERGE_NICS` | `0`, `0`, `0` (switch) | Capetron's switched launcher [cape-serve] |
| `NCCL_IB_SUBNET_AWARE_ROUTING` | `1` on 3- and 4-node rings | Lets NCCL pick the rail whose /24 holds the peer [nv-nccl] [sr-nccl] |
| `NCCL_NET_PLUGIN` | `none` on the 3-node ring | [nv-nccl] |

Find the GID index rather than hard-coding it [cape-val]:

```bash
hca=rocep1s0f0
for i in /sys/class/infiniband/$hca/ports/1/gids/*; do
  idx=${i##*/}
  echo "$idx $(cat $i) $(cat /sys/class/infiniband/$hca/ports/1/gid_attrs/types/$idx 2>/dev/null)"
done   # pick the RoCE v2 entry ending in this half's IPv4 address
```

# Container flags (vLLM, multi-node)

```bash
docker run ... \
  --ulimit memlock=-1:-1 --ulimit nofile=1048576:1048576 --cap-add IPC_LOCK \
  --device /dev/infiniband:/dev/infiniband \
  -e NCCL_NET=IB -e NCCL_IB_DISABLE=0 \
  -e NCCL_IB_HCA=rocep1s0f0,roceP2p1s0f0 \
  -e NCCL_IB_GID_INDEX=3 -e NCCL_IB_ROCE_VERSION_NUM=2 -e NCCL_IB_ADDR_FAMILY=AF_INET \
  -e NCCL_IB_ADDR_RANGE=198.51.100.0/24 \
  -e NCCL_SOCKET_IFNAME=enp1s0f0np0 -e GLOO_SOCKET_IFNAME=enp1s0f0np0 -e TP_SOCKET_IFNAME=enp1s0f0np0 \
  -e NCCL_NVLS_ENABLE=0 -e NCCL_CROSS_NIC=0 -e NCCL_IB_MERGE_NICS=0 -e NCCL_CUMEM_ENABLE=0 \
  -e NCCL_IGNORE_CPU_AFFINITY=1 -e NCCL_DEBUG=WARN ...
```

From Capetron's switched-fabric launchers; substitute your subnet and GID [cape-serve]. Six-rank
NCCL exceeds Docker's default `nofile=1024`; four ranks fit by luck [cape-serve].

# Ring profiles (no switch)

**Two-rank direct pair** (sparkring contract): one HCA, `NCCL_IB_SUBNET_AWARE_ROUTING=0`,
`NCCL_CROSS_NIC=1`, Tree left enabled because both ranks are adjacent [sr-nccl].

**Four-rank cycle** needs a patched NCCL that skips Tree/PAT connection setup (which would need
non-adjacent peers) [sr-nccl] [ae-recipe]:

```text
LD_PRELOAD=<patched libnccl.so.2>  VLLM_NCCL_SO_PATH=<same>
NCCL_SKIP_TREE_CONNECT=1  NCCL_ALGO=Ring
NCCL_IB_HCA=<two direct roce devices>  NCCL_IB_SUBNET_AWARE_ROUTING=1  NCCL_IB_SUBNET_PREFIX_LEN=24
NCCL_IB_MERGE_NICS=0  NCCL_CROSS_NIC=1  NCCL_IB_GID_INDEX=3  NCCL_CUMEM_ENABLE=0
NCCL_SOCKET_IFNAME=<management interface>     # bootstrap only; payload stays on RoCE
```

The GLM-5.3-Flash ring recipe also pins `NCCL_PROTO=LL,LL128,Simple`, `NCCL_MIN/MAX_NCHANNELS=4`
and `NCCL_P2P_LEVEL=SYS` [ae-recipe]. NVIDIA recommends /24 subnets because NCCL's subnet-aware
routing defaults to /24 [nv-multi].

# Building NCCL and running nccl-tests

NVIDIA's playbook builds NCCL from source for `sm_121` [nv-nccl-v2]:

```bash
git clone -b v2.31.2-1 https://github.com/NVIDIA/nccl.git ~/nccl/ && cd ~/nccl/
make -j src.build NVCC_GENCODE="-gencode=arch=compute_121,code=sm_121"
git clone -b v2.19.7 https://github.com/NVIDIA/nccl-tests.git ~/nccl-tests/ && cd ~/nccl-tests && make MPI=1
mpirun -np 2 -H <mgmt1>:1,<mgmt2>:1 -x NCCL_SOCKET_IFNAME=enP7s7 ... $HOME/nccl-tests/build/all_gather_perf -b 16G -e 16G
```

Version history: the 2025-12-15 playbook used v2.30.7-1; the 2026-10-14 update moved to v2.31.2-1 and
pinned nccl-tests v2.19.7 because v2.20.0+ adds GIN tests that fail to link with the system OpenMPI
[nv-nccl] [nv-nccl-v2].

**nccl-tests numbers: not published** in any source we hold — NVIDIA's playbooks give the commands
but no expected bus bandwidth. The fabric numbers that are published are RDMA (`ib_write_bw`):

| Test | Result |
|---|---|
| One half, direct cable | 111.86 Gb/s [cape-val] |
| Both halves, direct cable | 196.08 Gb/s [cape-val] |
| Both halves, through a CRS812 switch | 196 Gb/s [cape-val] |
| One subnet, OpenZeka 4-node switch | ~100–111 Gb/s; latency ~1–3 µs [oz-4n] |

# Traps

| Symptom | Cause | Source |
|---|---|---|
| `ncclCommInitRank` internal error on RoCE | Installing a FlashInfer nightly silently downgraded NCCL 2.30.7 → 2.29.7; re-pin it | [cape-serve] |
| "Message truncated: received 176 bytes instead of 172" | Two nodes on the same nightly tag pulled on different days — NCCL mismatch; pin image digest | [cape-serve] |
| NCCL bootstrap stalls, small pings fine | MTU 1500 on one end of a 9000 fabric | [cape-2n] |
| Ring works but decode ~2.7× slower, no error | Rails left at MTU 1500 | [ae-recipe] |
| Hang right after `Using PYNCCL all-reduce backends` (4-node ring) | First-collective state wedge; tear down all four ranks and relaunch | [ae-recipe] |
| Model "runs" but RDMA byte counters did not move | Socket fallback over the LAN | [cape-val] |

One more measured nuance: for GLM-5.3-Flash TP4, giving NCCL both RDMA devices per node raised
prefill 9 % but cut decode 5–9 %, because that all-reduce is latency-bound; Capetron keeps one
device for GLM and both for Qwen3.8-Flash-Next TP4+EP [cape-serve].

> **MTU, again.** NVIDIA's cluster script uses MTU 9000 only for a two-node direct link and 1500 for
> rings and switches, matching Cluster Assistant [nv-multi]. Capetron, OpenZeka and the switchless-ring
> recipe all run 9000 [cape-2n] [oz-4n] [ae-recipe]. No source compares the two on the same cluster.

Before serving on a direct-cable ring, sparkring qualifies every cable with bidirectional payload
tests and error counters, because "link-up and ping are not enough" [sr-cable]. See
[SparkRing and SparkCache](/stacks/sparkring-sparkcache.md).
