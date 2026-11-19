---
type: reference
title: NVIDIA DGX Spark playbooks — what is officially supported
description: Every playbook in NVIDIA's dgx-spark-playbooks repository (commit 3088315, October 2026), sorted by category with stated duration and risk, and which ones matter for a small team doing daily development on local models.
tags: [nvidia, playbooks, official-support, inference, fine-tuning, rag, agents, clustering, reference]
resource: /stacks/nvidia-playbooks.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [dgx-spark-playbooks, build.nvidia.com/spark, NVIDIA playbooks, official Spark playbooks]
entities:
  - label: dgx-spark-playbooks
    kind: repository
  - label: NVIDIA Sync
    kind: tool
  - label: Cluster Assistant
    kind: tool
  - label: NVIDIA PAIR
    kind: tool
  - label: spark-vllm-docker
    kind: tool
relations:
  - type: describes
    target: /hardware/software-support.md
  - type: references
    target: /stacks/vllm.md
  - type: references
    target: /stacks/sglang.md
  - type: references
    target: /stacks/speculative-decoding.md
  - type: references
    target: /stacks/quantization-formats.md
  - type: references
    target: /clustering/two-node-dac.md
  - type: references
    target: /clustering/three-node-ring.md
  - type: references
    target: /clustering/switched-fabric.md
  - type: references
    target: /clustering/cluster-tooling.md
  - type: compared_with
    target: /stacks/tensorfold.md
  - type: compared_with
    target: /stacks/exl3-exllamav3.md
provenance:
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/README.md
    note: Root README — the list of 69 published playbooks at commit 3088315.
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/tree/30883150541743d580c9c347700c6ac99fc396d2/nvidia
    note: Every playbook directory README (hardware matrix, Time & risk, What you'll accomplish), read 2026-10-29.
  - source: https://build.nvidia.com/spark
    note: Web catalogue of the same playbooks (taglines and update dates).
  - source: https://build.nvidia.com/spark/multi-sparks-through-switch
    note: Web page clipped from this URL renders the Connect Multiple DGX Sparks playbook (Beginner, 10 min).
citations:
  - id: nv-readme
    text: "NVIDIA, DGX Spark Playbooks — README (commit 3088315). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/README.md"
  - id: nv-tree
    text: "NVIDIA, dgx-spark-playbooks nvidia/ directory — per-playbook README files, Time & risk and hardware matrix sections (commit 3088315). https://github.com/NVIDIA/dgx-spark-playbooks/tree/30883150541743d580c9c347700c6ac99fc396d2/nvidia"
  - id: nv-web
    text: "NVIDIA, DGX Spark playbook catalogue. https://build.nvidia.com/spark"
  - id: nv-multi-web
    text: "NVIDIA, Connect Multiple DGX Sparks for Distributed Workloads (web). https://build.nvidia.com/spark/multi-sparks-through-switch"
  - id: nv-vllm
    text: "NVIDIA, Serve LLMs with vLLM on One Device (updated 2026-10-19). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-vllm/README.md"
  - id: nv-vllm-cl
    text: "NVIDIA, Serve LLMs with vLLM Across DGX Sparks (updated 2026-10-22). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-vllm-cluster/README.md"
  - id: nv-sglang
    text: "NVIDIA, Serve LLMs with SGLang. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-sglang/README.md"
  - id: nv-trt
    text: "NVIDIA, Serve LLMs with NVIDIA TensorRT-LLM. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-trt-llm/README.md"
  - id: nv-nemotron
    text: "NVIDIA, Serve Nemotron Nano and Super Models. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-nemotron/README.md"
  - id: nv-spec
    text: "NVIDIA, Speed Up Inference with Speculative Decoding. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-speculative-decoding/README.md"
  - id: nv-nvfp4
    text: "NVIDIA, Quantize Models to NVFP4 with NVIDIA Model Optimizer. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-nvfp4-quantization/README.md"
  - id: nv-llamacpp
    text: "NVIDIA, Serve Models with llama.cpp. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-llama-cpp/README.md"
  - id: nv-pair
    text: "NVIDIA, Install and Use NVIDIA PAIR with llama.cpp. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-pair/README.md"
  - id: nv-cli
    text: "NVIDIA, Set Up CLI Coding Agents with Local Inference. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-cli-coding-agent/README.md"
  - id: nv-vibe
    text: "NVIDIA, Set Up Vibe Coding in VS Code. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-vibe-coding/README.md"
  - id: nv-openshell
    text: "NVIDIA, Secure AI Agents with OpenShell. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-openshell/README.md"
  - id: nv-mac
    text: "NVIDIA, Build and Deploy a Multi-Agent Chatbot. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-multi-agent-chatbot/README.md"
  - id: nv-rag
    text: "NVIDIA, Build a RAG Application with AI Workbench. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-rag-ai-workbench/README.md"
  - id: nv-txt2kg
    text: "NVIDIA, Build Knowledge Graphs with txt2kg. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-txt2kg/README.md"
  - id: nv-pytorch
    text: "NVIDIA, Fine-Tune with PyTorch. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-pytorch-fine-tune/README.md"
  - id: nv-lf
    text: "NVIDIA, Fine-Tune LLMs with LLaMA Factory. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-llama-factory/README.md"
  - id: nv-multi
    text: "NVIDIA, Connect Multiple DGX Sparks for Distributed Workloads (updated 2026-09-24). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-connect-multiple-sparks/README.md"
  - id: nv-switch
    text: "NVIDIA, Connect Multiple DGX Sparks Through a Switch. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-multi-sparks-through-switch/README.md"
  - id: nv-llms
    text: "NVIDIA, Run Local LLMs. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/playbook-llms/README.md"
---

# Overview

NVIDIA publishes its supported DGX Spark workflows as step-by-step playbooks in
[NVIDIA/dgx-spark-playbooks](https://github.com/NVIDIA/dgx-spark-playbooks), mirrored on
[build.nvidia.com/spark](https://build.nvidia.com/spark) [nv-readme] [nv-web]. "Officially supported" in this
knowledge base means: a playbook exists and its hardware matrix lists **DGX Spark**.

State of the repository at commit `3088315` (read 2026-10-29) [nv-readme] [nv-tree]:

| Directory group | Count | What it is |
| --- | ---: | --- |
| `playbook-*` | 70 | Current playbooks. The root README lists 69 of them; `playbook-test` is an unlisted template. |
| unprefixed (`vllm`, `sglang`, `ollama` ...) | 47 | Older versions of the same playbooks, not linked from the root README. 46 of them have a `playbook-*` successor; only `ollama` has none (Ollama is now used inside `playbook-open-webui`, `playbook-cli-coding-agent` and `playbook-vibe-coding`). Not listed below. |
| `station-*` | 19 | DGX Station (GB300) versions. Not for Spark; not listed below. |

Of the 70 `playbook-*` directories, **51 list DGX Spark** (or are Spark-specific without a matrix), 11 list only
DGX Station, 5 target GeForce RTX / RTX PRO / RTX Spark PCs only, and 3 are test templates [nv-tree].
Several playbooks cover "DGX Spark or Station" in one document (vLLM, SGLang, NemoClaw, OpenShell, Hermes, NVFP4
quantization, txt2kg, ComfyUI, Brev).

# Playbooks that apply to DGX Spark

Duration and risk are copied from each playbook's "Time & risk" section [nv-tree]; "not stated" means the
playbook gives none. Times usually exclude or only roughly include model downloads.

## Inference servers and model serving

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Serve LLMs with vLLM on One Device](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vllm) | vLLM container as an NVIDIA Sync custom app (Intermediate) or manual recipe with tool-call checks (Advanced) | 15–30 min; Advanced +30 min | Low |
| [Serve LLMs with vLLM Across DGX Sparks](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vllm-cluster) | One model split across 2–4 Sparks via `spark-vllm-docker` recipes | 30 min or longer | Medium |
| [Serve LLMs with SGLang](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-sglang) | SGLang server with RadixAttention prefix cache and structured output | 30 min; 45–60 min for large MoE | Low |
| [Serve LLMs with NVIDIA TensorRT-LLM](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-trt-llm) | TensorRT-LLM OpenAI-compatible server, single- and multi-node | 60 min | Medium |
| [Deploy NVIDIA NIM for LLM Inference](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nim-llm) | Prebuilt NIM container (default: Nemotron 3.5 Lightning 30B-A3B) | 30 min | Low |
| [Serve Nemotron Nano and Super Models](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nemotron) | Nemotron-3-Nano on vLLM; Nemotron-3-Super NVFP4 on vLLM or TensorRT-LLM | 45 min | Low |
| [Serve Models with llama.cpp](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-llama-cpp) | Build llama.cpp for `sm_121`, serve a Qwen3.6-35B-A3B GGUF with `llama-server` | 30 min (+~21 GB download) | Low |
| [Serve LLMs with LM Studio](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-lm-studio) | Headless LM Studio (`llmster`) serving Nemotron 3.5 Super VL to a laptop | 30 min | Low |
| [Chat with LLMs Using Open WebUI and Ollama](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-open-webui) | Self-hosted chat UI with a local Ollama backend | 15–20 min | Low |
| [Run Local LLMs](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-llms) | Generic RTX/Spark guide: pick a model size, then Ollama / LM Studio / AnythingLLM | not stated | not stated |
| [Speed Up Inference with Speculative Decoding](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-speculative-decoding) | EAGLE-3 and draft-target decoding on TensorRT-LLM, optional multi-node | 30 min | Medium |
| [Quantize Models to NVFP4 with NVIDIA Model Optimizer](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nvfp4-quantization) | Produce and test an NVFP4 checkpoint (DeepSeek-R1-Distill-Llama-8B) | 60 min (45–90) | Medium |
| [Run Multi-Modal Inference with TensorRT](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-multi-modal-inference) | Text-to-image diffusion inference in the PyTorch container | 60 min | Medium |
| [Stream Real-Time Video to a Vision Language Model](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-live-vlm-webui) | Webcam-to-VLM testbed comparing backends | 30 min | Low |
| [Install and Use NVIDIA PAIR with llama.cpp](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-pair) | Routes independent requests across paired machines (Spark, RTX, Mac) | ~10 min + downloads | Low to medium |

## Coding and agents

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Set Up CLI Coding Agents with Local Inference](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-cli-coding-agent) | Claude Code, OpenCode or Codex CLI against a local Ollama Qwen3.6 model | 20 min | Low |
| [Set Up Vibe Coding in VS Code](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vibe-coding) | Continue.dev in VS Code against Ollama `gpt-oss:120b` | 30 min | Low |
| [Secure AI Agents with OpenShell](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-openshell) | Run a coding agent (Pi) in a kernel-level sandbox against local vLLM | 30 min | Medium |
| [Run Hermes Agent with a Local LLM](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-hermes-agent) | Nous Research terminal agent on local vLLM, optional Telegram | 30 min | Medium |
| [Run OpenClaw with a Local LLM](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-openclaw) | Always-on local-first agent with skills | 30 min | Medium to High |
| [Run NemoClaw with a Local LLM](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nemoclaw) | OpenClaw inside an OpenShell sandbox with local vLLM | 30–60 min | Medium |
| [Set Up Example NemoClaw Agents](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nemoclaw-applications) | Four ready agents on NemoClaw (news digest, software development, deck red-team, calendar) | 30–45 min | Medium |
| [Build and Deploy a Multi-Agent Chatbot](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-multi-agent-chatbot) | gpt-oss-120B supervisor with code, retrieval and image agents, MCP tools | 60 min | Medium |

## RAG and data

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Build a RAG Application with AI Workbench](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-rag-ai-workbench) | Agentic RAG with query routing and hallucination checks (Gradio) | 30–45 min | Low |
| [Build Knowledge Graphs with txt2kg](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-txt2kg) | Extract triples from documents with Ollama or vLLM into a graph DB | 30 min | Low |
| [Deploy a Video Search and Summarization Agent](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vss) | VSS 3.2.0 blueprint: video Q&A and alerts | 30–45 min | Medium |
| [Accelerate Data Science with CUDA-X Libraries](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-cuda-x-data-science) | GPU pandas / scikit-learn notebooks (RAPIDS) | 30 min | Low |
| [Accelerate Portfolio Optimization with cuOpt](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-portfolio-optimization) | Mean-CVaR portfolio optimisation notebook | 20 min | Low |
| [Accelerate Single-Cell RNA Data Analysis](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-single-cell) | Scanpy-style pipeline on GPU | 15 min | Low |
| [Run cuPyNumeric Across Two DGX Sparks](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-cupynumeric) | Distributed NumPy over two Sparks | 60 min | Medium |

## Fine-tuning

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Fine-Tune Faster with Unsloth](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-unsloth) | LoRA / QLoRA with Unsloth in the PyTorch container | 60 min | Medium |
| [Fine-Tune with PyTorch](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-pytorch-fine-tune) | Full SFT, LoRA, QLoRA for Llama 3 3B–70B; optional two-node | 60 min | Medium |
| [Fine-Tune with NVIDIA NeMo](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nemo-fine-tune) | NeMo AutoModel fine-tuning of Hugging Face LLMs and VLMs | 45–90 min | Medium |
| [Fine-Tune LLMs with LLaMA Factory](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-llama-factory) | SFT / RLHF / QLoRA through one interface | 60 min setup; 1–7 h training | Medium |
| [Fine-Tune Vision Language Models](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vlm-finetuning) | LoRA and preference tuning of image/video VLMs | 2 h | Medium |
| [Fine-Tune FLUX.2 Klein for Custom Image Generation](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-flux-finetuning) | Concept LoRA for image generation | 4 h | Medium |

## Clustering

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Connect Multiple DGX Sparks for Distributed Workloads](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-connect-multiple-sparks) | 2–4 Sparks, direct / ring / switch, via NVIDIA Sync Cluster Assistant or manual scripts | 10 min (Sync); 1 h manual | Low (Sync); Medium manual |
| [Connect Two DGX Sparks for Distributed Workloads](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-connect-two-sparks) | One direct QSFP link, netplan, passwordless SSH | 60 min | Medium |
| [Connect Three DGX Sparks in a Ring Topology](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-connect-three-sparks) | Three-node switchless ring | 60 min | Medium |
| [Connect Multiple DGX Sparks Through a Switch](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-multi-sparks-through-switch) | Four or more Sparks on a 200G QSFP switch | 2 h | Medium |
| [Set Up NCCL for Multi-Node GPU Communication](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-nccl) | Build NCCL v2.31.2-1 for `sm_121`, run bandwidth tests on 2–4 nodes | 30 min | Medium |

## Tools and access

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Use NVIDIA Sync to Connect Remotely to Your AI Compute](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-connect-to-your-spark) | NVIDIA Sync desktop app: SSH tunnels and custom apps | 5 min | Low |
| [Set Up Tailscale for Remote Access](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-tailscale) | Tailnet access without port forwarding | 30 min | Medium |
| [Set Up VS Code for Local and Remote Development](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-vscode) | ARM64 VS Code locally or remote via Sync | 10 min | Low |
| [Monitor Your AI Compute with DGX Dashboard](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-dgx-dashboard) | Local web UI: updates, GPU status, JupyterLab (port 11000) | 30 min | Low |
| [Register AI Compute with Brev](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-brev) | Register the Spark as a shared remote Brev workspace | 5–10 min | Low |
| [Run cuTile Kernels on DGX Spark](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-cutile-kernels) | TileGym cuTile Python kernels and benchmarks | 60 min | Low |
| [Accelerate JAX Performance](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-jax) | JAX tutorial container (marimo) | 2 h | Medium |

## Media and robotics

| Playbook | What it does | Duration | Risk |
| --- | --- | --- | --- |
| [Generate Images and Videos with ComfyUI](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-comfyui) | FLUX, Wan, HunyuanVideo, SD workflows | 2 h | Medium |
| [Set Up Isaac Sim and Isaac Lab](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-isaac) | Build Isaac Sim from source on aarch64, RL sample | 30 min | Medium |
| [Build an AI Photo Booth with Reachy and DGX Spark](https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/playbook-spark-reachy-photo-booth) | gpt-oss-20b + FLUX.1-Kontext + Parakeet ASR demo | 2 h | Medium |

# Playbooks that do not apply to DGX Spark

Listed for completeness; the hardware matrix of each names other hardware only [nv-tree].

| Target | Playbooks (`nvidia/` directory) |
| --- | --- |
| DGX Station only (GB300) | `playbook-connect-two-stations`, `playbook-dgx-station-ai-skills`, `playbook-gr00t`, `playbook-healthcare-agent`, `playbook-kernel-dev-ft`, `playbook-local-coding-agent` (the Spark equivalent is `playbook-cli-coding-agent`), `playbook-mig`, `playbook-nanochat`, `playbook-nvfp4-pretraining`, `playbook-sglang-inference` (the Spark equivalent is `playbook-sglang`), `playbook-topic-modeling`, plus all 19 `station-*` directories |
| GeForce RTX / RTX PRO / RTX Spark PCs | `playbook-fine-tuning` (methods overview, no commands), `playbook-multi-gpu`, `playbook-video-gen-guide`, `playbook-visual-gen-ai`, `playbook-living-home` |
| Templates | `playbook-test`, `playbook-test-spark`, `playbook-test-station` |

# What matters for a small team

The case here: a small team doing daily development on local models, starting with two Sparks on one DAC and
possibly growing to four. Facts below are what the playbooks state, not measurements.

## Inference servers

- **vLLM, one Spark** — NVIDIA's own recipe table for DGX Spark: on 64 GB units, Qwen3.8 27B (NVFP4) and
  Nemotron 3.5 Bolt 74B A9B; on 128 GB units, Qwen3.8 Flash-Next and Qwen3.8 27B (NVFP4). The Qwen3.8 27B and
  Bolt scripts load a second draft model for speculative decoding [nv-vllm]. See [vLLM](/stacks/vllm.md),
  [Qwen3.8 Flash-Next](/models/qwen38-flash-next.md), [Nemotron 3.5](/models/nemotron-35.md),
  [speculative decoding](/stacks/speculative-decoding.md).
- **vLLM, several Sparks** — the guided NVIDIA Sync path supports two to four Sparks; worked command-line examples
  exist only for two. All Sparks in one cluster must have the same memory size. Two-Spark recipes: Qwen3.8
  Flash-Next on 2 × 64 GB, GLM 5.3 Flash (`nvidia/GLM-5.3-Flash-FP4-Local`) on 2 × 128 GB. The launcher is the
  community repository `eugr/spark-vllm-docker`, which NVIDIA's playbook calls directly [nv-vllm-cl].
  See [GLM 5.3 family](/models/glm53-family.md).
- **SGLang** — models listed as validated on DGX Spark: Nemotron-3-Nano-Omni-30B-A3B, GPT-OSS-20B/120B (MXFP4),
  Llama-3.1-8B (FP8/NVFP4), Llama-3.3-70B (NVFP4), Qwen3-8B/14B/32B, Phi-4 multimodal and reasoning-plus
  [nv-sglang]. No Qwen3.8 or GLM entry on the Spark list. See [SGLang](/stacks/sglang.md).
- **TensorRT-LLM** — the only playbook that names a multi-node model: Qwen3-235B-A22B NVFP4; single-node uses
  `release:1.3.0rc13`, multi-node `release:1.3.0rc5` [nv-trt]. The speculative-decoding playbook runs
  GPT-OSS-120B with EAGLE-3 or Llama-3.3-70B with a draft model on one Spark, and Qwen3-235B-A22B with `TP=2`
  across two [nv-spec].
- **Nemotron** — Nano on `vllm/vllm-openai:v0.20.0`; Super NVFP4 on `vllm/vllm-openai:cu130-nightly` or
  TensorRT-LLM `1.3.0rc9`; settings assume ~128 GB unified memory [nv-nemotron].
- **llama.cpp** — built from source with `CMAKE_CUDA_ARCHITECTURES=121a-real`, example
  `unsloth/Qwen3.6-35B-A3B-MTP-GGUF:UD-Q4_K_XL` [nv-llamacpp]. NVIDIA's generic guide recommends Qwen 3.6 35B as
  the starting model on DGX Spark [nv-llms].
- **Quantization** — the NVFP4 playbook quantizes only an 8B model as its example and warns that quantization
  can change quality [nv-nvfp4]. See [quantization formats](/stacks/quantization-formats.md).

## Coding agents

How these clients connect through a shared gateway, and the traps, are in
[coding agents on local models](/stacks/coding-agents-on-local-models.md). For model choice beyond NVIDIA's own
recipes see the [matrix](/models/spark-matrix.md) and the [registry recipes](/models/registry-recipes.md).

- **CLI coding agents** — Claude Code, OpenCode or Codex CLI launched with `ollama launch` against
  `qwen3.6:35b-a3b-mtp-q4_K_M` (~23 GB; `q8_0` ~39 GB; `bf16` ~71 GB) [nv-cli].
- **IDE** — Continue.dev in VS Code against Ollama `gpt-oss:120b` [nv-vibe].
- **Sandboxing** — OpenShell runs a coding agent with filesystem, network and process isolation against a
  locally served vLLM model, no external API keys [nv-openshell]. Relevant before agents touch internal repos.
- **Multi-agent** — supervisor on gpt-oss-120B with MCP servers as tools, served by llama.cpp and TensorRT-LLM
  [nv-mac].

## RAG

- Agentic RAG in AI Workbench (query routing, relevancy and hallucination checks) [nv-rag] and txt2kg knowledge
  graphs from markdown/text/CSV with Ollama or vLLM [nv-txt2kg]. Both are demos to start from, not production
  stacks.

## Fine-tuning

- PyTorch playbook: full SFT, LoRA, QLoRA for Llama 3 from 3B to 70B, optionally over two nodes [nv-pytorch].
  LLaMA Factory states 1–7 h of training depending on model and dataset [nv-lf]. Unsloth and NeMo cover the
  same ground with other tooling.

## Several Sparks for a team

- **Cabling** — NVIDIA Sync Cluster Assistant supports two to four Sparks and requires the April 2026 DGX OS
  release or later. Layouts: two direct, three in a ring, four in a ring (manual path only), or a switch; do not
  mix direct and switched links [nv-multi] [nv-multi-web]. MTU 9000 only for a two-Spark direct link, 1500 for
  every other layout [nv-multi]. See [two-node DAC](/clustering/two-node-dac.md),
  [three-node ring](/clustering/three-node-ring.md), [switched fabric](/clustering/switched-fabric.md),
  [cluster tooling](/clustering/cluster-tooling.md).
- **Switch** — at least four QSFP56-DD ports at 200 Gb/s; 400 Gb/s ports can be split with breakout cables
  [nv-switch].
- **Serving many users rather than one big model** — NVIDIA PAIR routes each independent request to a machine
  that has the model; it does not pool memory or split a model across machines [nv-pair]. This is the official
  option for "one model per Spark, shared by the team", next to tensor-parallel vLLM for "one model across
  Sparks".

# Limitations

- **Source conflict on four Sparks without a switch.** `playbook-connect-multiple-sparks` documents a four-Spark
  direct ring (manual path only) [nv-multi], while `playbook-vllm-cluster` says a switch is required for four
  Sparks [nv-vllm-cl] and `playbook-multi-sparks-through-switch` starts at four nodes on a switch [nv-switch].
  The community four-node ring is covered in [switched fabric](/clustering/switched-fabric.md).
- **Web URL mismatch.** The page clipped from `build.nvidia.com/spark/multi-sparks-through-switch` shows the
  "Connect Multiple DGX Sparks" playbook (Beginner, 10 min), not the switch playbook [nv-multi-web].
- **No performance numbers.** The playbooks give setup time and risk, not tokens per second or concurrency.
  Throughput comes from the field reports and measurements elsewhere in this knowledge base.
- **Not covered officially.** No playbook mentions TensorFold or EXL3 / ExLlamaV3 (searched across the whole
  repository at commit 3088315) [nv-tree]. Both are community routes: see [TensorFold](/stacks/tensorfold.md)
  and [EXL3 / ExLlamaV3](/stacks/exl3-exllamav3.md). The vLLM cluster playbook itself depends on the community
  `spark-vllm-docker` project [nv-vllm-cl], so the line between "official" and "community" is not clean.
- **Moving target.** Key playbooks changed within weeks of this snapshot (vLLM 2026-10-19, vLLM cluster 2026-10-22, Connect Multiple
  2026-09-24) [nv-vllm] [nv-vllm-cl] [nv-multi]. This page reflects commit 3088315 only.
