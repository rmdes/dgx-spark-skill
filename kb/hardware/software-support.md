---
type: hardware
title: Software support on sm_121
description: Where the GB10 software stack stands — sm_121 gaps in PyTorch, vLLM, FlashInfer and friends, what each DGX OS release fixed, and the honest "early days" assessment.
tags: [gb10, sm121, software, dgx-os, vllm, firmware]
resource: /hardware/software-support.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [sm_121, SM121, compute capability 12.1, DGX OS release notes, GB10 software maturity]
entities:
  - label: DGX OS
    kind: operating_system
  - label: sm_121
    kind: gpu_architecture
  - label: vLLM
    kind: inference_engine
relations:
  - type: describes
    target: /hardware/gb10-platform.md
  - type: affects
    target: /stacks/vllm.md
  - type: affects
    target: /stacks/sglang.md
  - type: affects
    target: /clustering/nccl-over-roce.md
  - type: related_to
    target: /field-reports/simon-willison-first-look.md
  - type: related_to
    target: /stacks/tensorfold.md
provenance:
  - source: https://docs.nvidia.com/dgx/dgx-spark/release-notes.html
    note: NVIDIA release notes, November 2025 to October 2026, and current component versions.
  - source: https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663
    note: Forum thread from a 4-node owner (opened 2026-01-15) with NVIDIA staff replies.
  - source: https://github.com/vllm-project/vllm/issues/36821
    note: vLLM issue "No sm_121 support on aarch64" (2026-03-11) and its follow-ups up to vLLM 0.29.0.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: Five failure classes of a stock vLLM image on sm_121, August 2026.
  - source: https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/
    note: Simon Willison launch-week review, "great hardware, early days for the ecosystem".
citations:
  - id: nv-rn
    text: "NVIDIA, DGX Spark Release Notes. https://docs.nvidia.com/dgx/dgx-spark/release-notes.html"
  - id: forum
    text: "NVIDIA Developer Forums, DGX Spark (SM121) Software Support is Severely Lacking — Official Roadmap Needed (2026-01-15). https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663"
  - id: vllm-36821
    text: "vLLM issue #36821, No sm_121 (Blackwell) support on aarch64 — DGX Spark / Acer GN100 (2026-03-11). https://github.com/vllm-project/vllm/issues/36821"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: cape-val
    text: "Capetron, GB10 cluster guide — 04 Validation (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/04-validation.md"
  - id: simonw
    text: "Simon Willison, NVIDIA DGX Spark: great hardware, early days for the ecosystem (2025-10-14). https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/"
  - id: sth
    text: "ServeTheHome, NVIDIA DGX Spark Review (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/4/"
  - id: oz-4n
    text: "OpenZeka, DGX Spark 4-Node AI Cluster Setup Guide (2026-07-24). https://whitepapers.openzeka.com/papers/dgx-spark-4node-cluster-setup/"
  - id: nv-nccl-v2
    text: "NVIDIA, Set Up NCCL for Multi-Node GPU Communication (playbook, 2026-10-14). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-nccl/README.md"
  - id: ours
    text: "Author's own boxes, 2026-10-30: platform comparison (COMPARISON-20261030.md section 6) in benchmarks/results/20261030-platform-comparison/ of this repository."
---

# Overview

The GB10 GPU is CUDA compute capability **12.1 (`sm_121`)** with 48 SMs [simonw]. It belongs to the
consumer/workstation Blackwell family (`sm_12x`, like the RTX 50xx and RTX PRO 6000), **not** the
datacenter `sm_100` line: NVIDIA staff confirmed on the forum that it has no `tcgen05` (the datacenter
Blackwell tensor-memory instructions) and that GB10 has "software parity" with RTX 50xx [forum].
That single fact explains most of the friction: software built for `sm_100` or `sm_120` often ships
no `sm_121` kernels, and the host CPU is Arm64, where many CUDA wheels arrived late [simonw] [vllm-36821].

The honest one-line state, October 2026: **it works, but only with the right builds**. Every
community recipe in this knowledge base carries patches or pinned images, and the vendor images
have needed patches as recently as August 2026 [cape-serve].

# Current versions (DGX Spark Founders Edition)

| Component | Version |
|---|---|
| DGX OS | 7.6.0 |
| GPU driver | 580.178.04 |
| CUDA Toolkit | 13.0.3 |
| TensorRT | 10.14.1 |
| Kernel | 7.0.0-1019 |
| UEFI | 1.111.17 |
| SoC firmware | 2.158.15 |

Source: release notes as clipped 2026-10-29 [nv-rn]. These apply only to the Founders Edition;
"GB10-based partner systems may not receive updates at the same time" [nv-rn].

# What each release fixed or added

| Release | Relevant change |
|---|---|
| Nov 2025 | Ubuntu 6.14 HWE kernel; JupyterLab on CUDA 13.0.2; unified-memory reporting in DGX Dashboard made consistent with CUDA guidance |
| Jan 2026 | ConnectX-7 hot plug (up to 18 W saved when unused); Wi-Fi/Bluetooth can be disabled in UEFI |
| Feb 2026 | Fixed a **multi-Spark performance regression** after DGX OS 7.4.0 |
| Apr 2026 | Enterprise: air-gapped deployment and updates, USB/local repository updates, cloud-init custom ISOs, skip the OOBE |
| Jun 2026 | NVIDIA Sync **Cluster Assistant**; NCCL 2.30u1 with updated support for the three-node ring |
| Jul 2026 | Improved **OOM handling** for unified memory, with user feedback under memory pressure; display reserved memory 2 GB or 4 GB |
| Oct 2026 | Linux 7.0 kernel; one image for 64 GB and 128 GB units; display carveout down to 512 MB headless; **fixed fans stopping in headless mode** at low idle power; native cloud-init |

Source: [nv-rn].

Firmware matters for the fabric: a power-throttled ConnectX-7 delivered 12.74 Gb/s of RDMA while
every status tool showed 200G, and an OS + firmware update fixed it [cape-val]. OpenZeka saw the
same class of problem and updates first [oz-4n]:

```bash
sudo apt update && sudo apt dist-upgrade
sudo fwupdmgr refresh --force && sudo fwupdmgr upgrade
sudo reboot
```

# The gaps, as reported

## January 2026 — forum thread from a 4-node owner [forum]

| Area | Owner's report | NVIDIA reply |
|---|---|---|
| PyTorch | No CUDA 13 Arm64 wheels on PyPI; custom index needed | Custom index is by design for every CUDA variant |
| Triton | Issue closed by treating sm121 as sm80 | Fixes in Triton 3.6.0, then only in PyTorch's test index |
| FlashInfer | Compilation failures on GB10 | sm12x supported from 0.5.3 (staff first cited a non-existent version, then corrected) |
| CUTLASS | FP8 kernels fail to dispatch on sm121 | Compatible from 4.2.0 |
| MoE kernels | No tuned configs for GB10 | "Area of active development" |
| vLLM | Workarounds needed; `--enforce-eager` "20–30 % performance loss" (owner's estimate) | `--enforce-eager` required "in certain versions"; vLLM 0.13.0 supported |
| SGLang | Runs on a community branch | Also runs from official wheels |

Two community voices in the same thread: one said marketing as a "baby Grace Blackwell" is
misleading because it is "much closer to RTX5090/6000", yet "still the best device of its class" and
production-ready for their own workflows; the same contributor added that the prebuilt vLLM cu130
wheels "work just fine now" [forum].

## March–October 2026 — vLLM issue #36821 [vllm-36821]

- Reported 2026-03-11: vLLM containers shipped PyTorch built only up to `sm_120`; vLLM crashed at
  startup on GB10. Workaround: build from source with `TORCH_CUDA_ARCH_LIST=12.1a`.
- A PR proposed adding 12.1 to every vLLM build configuration; PyTorch fixes for a CMake bug that
  mangles `12.1` were in review. PyTorch cu130 aarch64 nightlies ship `12.0+PTX` (JIT forward compatibility).
- Latest comment in our copy: the published **vLLM 0.29.0** aarch64 wheel is "very close to working"
  on GB10, but its `_qutlass_C` extension contains `sm_100` code only.

## August 2026 — a stock vendor image on four units [cape-serve]

The day-zero vLLM image for GLM-5.3-Flash failed five ways before the first token: attention backend
gated to the wrong capability, a FlashInfer NaN at 64–256-row batches, a silent NCCL 2.30.7 → 2.29.7
downgrade, a CUTLASS DSL mismatch, and a Programmatic Dependent Launch race. GB10 also has roughly
**101 KB of opt-in shared memory versus Hopper's 228 KB**, which kernels written for
Hopper assume. Capetron's lesson: on this GPU, assume backend selection, kernel library version and
NCCL version are wrong until a multi-node run produces a coherent answer [cape-serve].

## Launch week — "great hardware, early days for the ecosystem" [simonw]

Simon Willison (preview unit, October 2025): CUDA on Arm64 was the trap — a PyTorch 2.7 CUDA wheel for
Arm worked, 2.8 he could not get; NVIDIA's container and playbooks made it much easier in the week of
launch; Ollama worked out of the box; "too early" for a confident recommendation. ServeTheHome, the
same week: "not the most mature NVIDIA platform out there" yet [sth].

## Seen on the author's own boxes (2026-10-30)

- **Stale NVIDIA CDI spec blocks new GPU containers.** On the home Spark, `libnvidia-egl-wayland1` went 1.1.21 → 1.1.23 on
  2026-10-23; `nvidia-cdi-refresh` only reacts to driver/toolkit events, so `/var/run/cdi/nvidia.yaml` kept pointing at the
  deleted file. Running containers were unaffected; every new `docker run --gpus` failed with `failed to fulfil mount
  request` — the next vLLM restart would have been an outage. Fix: `sudo systemctl start nvidia-cdi-refresh.service`; lasting
  fix: an apt `DPkg::Post-Invoke` hook that refreshes the spec after every dpkg run, now as `make cdi-refresh` in the author's stack [ours]. A second box, whose spec is regenerated at boot, had the same
  exposure.
- **A kernel upgrade without the matching NVIDIA module package boots the box without a GPU** — check
  `lsmod | grep nvidia` against `uname -r` before rebooting into a new kernel.

# What this means for a team

- Use an engine and recipe that someone has already run on GB10 — see the
  [models matrix](/models/spark-matrix.md), [TensorFold](/stacks/tensorfold.md), [vLLM](/stacks/vllm.md).
- Pin image **digests**, pin NCCL (NVIDIA's playbook builds NCCL v2.31.2-1 for `sm_121` from source
  [nv-nccl-v2]), and re-validate after every DGX OS update.
- Keep the whole cluster on the same OS and firmware; OEM units may lag Founders Edition updates [nv-rn].

# Limitations

- Most gap reports are owner reports on forums and GitHub, not systematic tests. Status changes
  monthly; date every claim you repeat.
- No source gives an NVIDIA roadmap for `sm_121` kernel optimizations; the forum thread asked and did
  not get one [forum].
