---
type: report
title: "Field report: Simon Willison's first look at the DGX Spark (launch week)"
description: Simon Willison's launch-day review of a preview DGX Spark — great hardware, but CUDA-on-ARM64 software pain, and an ecosystem that only arrived on embargo day.
tags: [field-report, launch, software-support, arm64, sm121]
resource: /field-reports/simon-willison-first-look.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [great hardware early days for the ecosystem, Willison DGX Spark]
entities:
  - label: Simon Willison
    kind: person
  - label: llama.cpp
    kind: inference_engine
  - label: Ollama
    kind: inference_engine
  - label: Tailscale
    kind: tool
relations:
  - type: cites
    target: /hardware/software-support.md
  - type: cites
    target: /hardware/gb10-platform.md
provenance:
  - source: https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/
    note: Blog post, 2025-10-14. NVIDIA supplied a preview unit; no payment, no editorial input requested (author's statement).
citations:
  - id: sw
    text: "Simon Willison, NVIDIA DGX Spark: great hardware, early days for the ecosystem (2025-10-14). https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/"
---

# Overview

**Source type: independent writer, vendor-supplied hardware.** NVIDIA sent a preview unit; the author says he
was not paid and NVIDIA asked for no editorial input beyond an embargo date [sw]. This is the state of things
at launch (October 2025), a year before this knowledge base; read it as a baseline, not as current status.

| Item | Detail |
|---|---|
| Who | Simon Willison, developer and blogger, previously Mac/MLX-based |
| Hardware | 1× DGX Spark preview unit, 4 TB NVMe; retail "around $4,000" at launch [sw] |
| Workload | Exploration: building llama.cpp, running small models, Docker with GPU, remote access |
| Tools | Claude Code inside disposable Docker containers; Tailscale; Open WebUI |

# What worked

- **NVIDIA's CUDA container** (`nvcr.io/nvidia/cuda:13.0.1-devel-ubuntu24.04`) removed most early friction [sw].
- **Claude Code as an installer.** Asked to build llama.cpp with GPU support and run a model, it did so
  "flawlessly" and wrote up notes [sw].
- **Tailscale** gave phone and laptop access from anywhere in minutes [sw].
- **Ecosystem on embargo day:** Ollama worked out of the box; LM Studio shipped a build; vLLM had an NGC
  container; llama.cpp published benchmarks [sw].
- **Documentation** improved "substantially" in the week before launch: getting-started guide, DGX dashboard, playbooks [sw].

# What did not work

- **CUDA on ARM64.** Much software assumes x86. A PyTorch 2.7 CUDA wheel for ARM worked, 2.8 did not; the PyTorch
  ARM ecosystem was "pretty confusing" [sw].
- **CUDA 12 vs 13.** CUDA 13 was very new and many tutorials expected 12 [sw].
- **Little documentation** for most of the month before launch [sw].

# Measured

| Figure | Value | Source |
|---|---|---|
| Memory seen by `free -h` | 119 GiB total, 112 GiB available (128 GB ≈ 119 GiB) | author [sw] |
| GPU | GB10, compute capability sm_121, 48 SMs | author [sw] |
| GPT-OSS 20B MXFP4, llama.cpp | ~3,600 tok/s prompt, ~59 tok/s generation | Georgi Gerganov's benchmark, quoted [sw] |
| GLM-4.5-Air GGUF, llama.cpp | ~817 tok/s prompt, ~18 tok/s generation | same, quoted [sw] |

# Verdict

"Too early for me to provide a confident recommendation", but the ecosystem progress in the launch week was
"very reassuring" [sw].

# Takeaways

- The ARM64 + sm_121 friction he hit is still visible a year later: vLLM images pinned by digest, sm_121-specific launch
  settings, and a box that boots without its GPU if a kernel upgrade lacks the matching NVIDIA module — see
  [software support](/hardware/software-support.md). Budget engineer time for it per new model.
- Remote access over a mesh VPN and a browser chat front-end were part of the useful setup from day one; the
  [home Spark stack](/field-reports/our-home-spark-local-ai.md) uses both.
- Launch-era speed figures (e.g. 18 tok/s for GLM-4.5-Air) predate MoE + speculative-decoding recipes; do not use them
  as current numbers.
