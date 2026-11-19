---
type: component
title: vLLM on GB10 (sm_121)
description: Why stock vLLM images failed on the DGX Spark's sm_121 GPU, the community patch chain that fixed it, how vLLM's memory settings behave on unified memory, and what has been measured working.
tags: [vllm, sm121, gb10, nccl, unified-memory, multi-node, inference-engine]
resource: /stacks/vllm.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [vLLM, vllm serve, NGC vLLM container]
entities:
  - label: vLLM
    kind: inference_engine
  - label: sm_121
    kind: gpu_architecture
  - label: FlashInfer
    kind: kernel_library
  - label: NCCL
    kind: collective_library
relations:
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: depends_on
    target: /hardware/software-support.md
  - type: constrained_by
    target: /hardware/unified-memory-limits.md
  - type: uses
    target: /clustering/nccl-over-roce.md
  - type: compared_with
    target: /stacks/tensorfold.md
  - type: compared_with
    target: /stacks/sglang.md
  - type: extended_by
    target: /stacks/sparkring-sparkcache.md
  - type: extended_by
    target: /stacks/exl3-exllamav3.md
provenance:
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: Independent field report (August 2026) — failure classes, patch chain, measured configurations, memory rules.
  - source: https://github.com/vllm-project/vllm/issues/36821
    note: Upstream bug — no sm_121 kernels in prebuilt aarch64 builds; community workarounds.
  - source: https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663
    note: January 2026 forum thread from a 4-node owner and NVIDIA's reply.
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/vllm/README.md
    note: NVIDIA's official vLLM playbook for DGX Spark (support matrix, multi-Spark, Qwen3.6 recipe, UMA note).
citations:
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric: vLLM on sm_121 (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
  - id: vllm-36821
    text: "vLLM issue #36821, No sm_121 (Blackwell) support on aarch64 — NVIDIA DGX Spark / Acer GN100 (2026-03-11). https://github.com/vllm-project/vllm/issues/36821"
  - id: nv-forum
    text: "NVIDIA Developer Forums, DGX Spark (SM121) Software Support is Severely Lacking — Official Roadmap Needed (2026-01-15). https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663"
  - id: nv-vllm
    text: "NVIDIA, DGX Spark playbook — vLLM for Inference (last updated 2026-06-12). https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/vllm/README.md"
  - id: vllm-par
    text: "vLLM docs, Parallelism and Scaling. https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html"
  - id: ds-vllm2
    text: "MiaAI-Lab, DeepSeek v4.1 Flash EXL3 2.9 bpw for 2x DGX Sparks (vLLM, README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks/blob/6f7d1590ad49a2b8995188e45d7b9db31e677452/README.md"
---

# Overview

vLLM is the general-purpose engine with NVIDIA's backing on DGX Spark: there is an NGC container
(`nvcr.io/nvidia/vllm`), an official playbook, and a published model support matrix [nv-vllm]. It is also the
engine where the GB10's young software stack hurt most. The GB10 GPU is compute capability 12.1 (`sm_121`), and in
2026 prebuilt vLLM builds, and several day-zero model images, did not run on it without patches [vllm-36821]
[cape-serve]. The evidence splits by model: NVIDIA's playbook (updated June 2026) lists models marked supported
from its container [nv-vllm], while new models in August 2026 still needed a **community patch chain**
[cape-serve].

For which engine to pick per job, see [TensorFold — which engine for which job](/stacks/tensorfold.md).

# Why stock images failed

**Build-time gap (early 2026).** The prebuilt PyTorch inside vLLM images carried kernels only through `sm_120`, so
vLLM crashed at startup on the Spark; runtime variables do not fix prebuilt binaries [vllm-36821]. In that issue the
only working local option the reporter found was Ollama. Fixes proposed there: build from source with
`TORCH_CUDA_ARCH_LIST=12.1a`, and PR #38484 adding 12.1 to vLLM's published build configurations; the community
images `eugr/spark-vllm-docker` and build scripts were also offered [vllm-36821].

**Ecosystem gap.** A four-node owner listed the January 2026 state: no official CUDA 13 ARM64 PyTorch wheels on
PyPI, Triton treating sm121 as sm80, FlashInfer compile failures, CUTLASS FP8 kernels not dispatching, no MoE
configs for GB10, the NGC vLLM container "stuck at v0.11" [nv-forum]. NVIDIA replied that vLLM 0.13.0 is supported
on DGX Spark (aarch64 cu130 wheel), that sm80-class kernels run because tensor-core behaviour is similar, and that
GB10 has software parity with RTX 50 (same sm12x family) [nv-forum]. The original poster disputed several version
numbers in that reply. See [Software support](/hardware/software-support.md).

**Model-specific failures (August 2026).** Capetron tried the day-zero vendor image for GLM-5.3-Flash on four GB10s
and hit five distinct failures before a first token [cape-serve]:

| # | Symptom | Cause | Community fix |
|---|---|---|---|
| 1 | Dies in warmup | Only sparse-MLA backend enabled for capability 12 required a rotary dim of 64; the NoPE backend was gated to capability 9 | Extend the gate to 12, use its FA2 path |
| 2 | NaN at 64–256-row batches | FlashInfer release bug on sm_121 | Install a FlashInfer nightly, delete the AOT kernel cache |
| 3 | `ncclCommInitRank` internal error | The nightly pulled NCCL down from 2.30.7 to 2.29.7 | Re-pin NCCL 2.30.7 in the same layer |
| 4 | CuTeDSL warmup breaks | CUTLASS DSL version mismatch | Re-pin the qualified version |
| 5 | Random NaN on some boots | Programmatic Dependent Launch race in Triton kernels enabled for capability ≥ 9 | Gate PDL to capabilities 9 and 10 |

Plus: initialize the sparse indexer's top-k buffer, and cap the FP8 KV tile so it fits the GB10's ~101 KB of opt-in
shared memory instead of Hopper's 228 KB [cape-serve]. Their lesson: "assume the image's attention backend selection,
kernel library version, and NCCL version are all wrong until a multi-node run has produced a coherent answer." The
failures looked like network faults, model bugs or hardware faults, and none were [cape-serve].

# Memory on unified memory

The GB10 exposes about 121 GiB to CUDA out of 128 GB, and the OS shares it [cape-serve]. vLLM's knobs do not behave
as on a discrete GPU:

- **`--gpu-memory-utilization` is not a cap here.** Committed memory tracks weights plus runtime; a two-node GLM boot
  failed five times at memory before a recipe's explicit `--kv-cache-memory 4445787956` worked [cape-serve].
- **Container memory limits do not protect the host:** GPU and unified-memory allocations are not cgroup-charged
  [cape-serve].
- **0.85 utilization leaves 1–4 % MemAvailable**; each 0.01 is about 1.2 GiB. Capetron's rules: 0.65 for TP4 + EP,
  0.72–0.75 for a standing single-node endpoint with `--kv-cache-dtype fp8_e4m3`, never 0.85 [cape-serve].
- **Guard the host:** a loop that `docker rm -f`s the container below 12 % MemAvailable. If `earlyoom` is installed,
  its 10 % default kills the vLLM worker silently (`OOMKilled=false`) [cape-serve].
- **Long prompts, not boot, set the floor.** On the DeepSeek EXL3 recipe every extra 0.5 GiB of KV pool cost ~1 GiB of
  prefill margin; a 3 GiB pool booted but died at ~470k of a 600k prompt [ds-vllm2].
- NVIDIA's own workaround when memory errors appear within capacity: flush the page cache with
  `sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'` [nv-vllm].

More in [Unified memory limits](/hardware/unified-memory-limits.md).

# What works (measured)

**Independent (Capetron, stock community patch chain, temperature 0, warm pass)** [cape-serve]:

| Model, layout | Decode prose / code / math | Prefill (warm) | 6-stream aggregate | KV cache |
|---|---|---|---|---|
| Qwen3.8 Flash Next NVFP4, 1 Spark (n-gram table mmap'd) | 24.8 / 31.1 / 33.8 | 2,376 tok/s | 86.4 tok/s | 296,636 tokens |
| Qwen3.8 Flash Next NVFP4, 2 Sparks TP2 | 35.3 / 36.0 / 53.2 | 2,303 tok/s | 118.1 tok/s | 1,850,932 tokens |
| Qwen3.8 Flash Next NVFP4, 4 Sparks TP4 + EP | 39.6 / 57.0 / 76.9 | 3,547 tok/s | 167.4 tok/s | 2,643,285 tokens |
| GLM-5.3-Flash NVFP4, 2 Sparks TP2, MTP-4 | 16.0 / 21.4 / 31.1 | 1,495 tok/s | 52.1 tok/s | 507,041 tokens |
| GLM-5.3-Flash NVFP4, 4 Sparks TP4, MTP-4 | 26.5 / 38.1 / 46.7 | 3,840 tok/s | 91.2 tok/s | 2,246,948 tokens |

Findings that carry over: plain TP4 of Qwen3.8 Flash Next cannot load (NVFP4 MoE kernel alignment), so add
`--enable-expert-parallel`; TP6 and pipeline parallelism both fail for that model; eager mode beat piecewise CUDA
graphs; MTP-4 beat MTP-6; six Sparks serve best as three TP2 pairs (~386 tok/s across 18 streams) [cape-serve].
For scale, four H200s run the same GLM model at 233–339 tok/s per stream, roughly ten times four GB10s [cape-serve].

**NVIDIA-listed models** run from the NGC container with `vllm serve <hf-handle>`, including GPT-OSS-20B/120B
(MXFP4), Llama-3.3-70B NVFP4, Qwen3-32B NVFP4 and Nemotron-3-Super-120B NVFP4 [nv-vllm]. The playbook's two-Spark
example serves Llama 3.3 70B at TP2, and warns that a 405B AWQ-INT4 model has "insufficient memory headroom for
production use" [nv-vllm].

Faster vLLM-based recipes exist (MiaAI-Lab, SparkRing) — see the [Models × Sparks matrix](/models/spark-matrix.md) and
[SparkRing and SparkCache](/stacks/sparkring-sparkcache.md).

# Runbook

NVIDIA's agent-ready Qwen3.6 35B recipe on one Spark (verbatim flags from the playbook) [nv-vllm]:

```bash
docker run -it --gpus all -p 8000:8000 \
  -e HF_TOKEN="$HF_TOKEN" -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:latest nvidia/Qwen3.6-35B-A3B-NVFP4 \
  --host 0.0.0.0 --port 8000 --tensor-parallel-size 1 --trust-remote-code \
  --kv-cache-dtype fp8 --attention-backend flashinfer --moe-backend marlin \
  --gpu-memory-utilization 0.4 --max-model-len 262144 --max-num-seqs 4 \
  --max-num-batched-tokens 8192 --enable-chunked-prefill --async-scheduling \
  --enable-prefix-caching \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3,"moe_backend":"triton"}' \
  --load-format fastsafetensors --reasoning-parser qwen3 \
  --tool-call-parser qwen3_xml --enable-auto-tool-choice
```

Multi-node essentials from Capetron's launchers [cape-serve]:

- `--ulimit nofile=1048576:1048576` on every container (six-rank NCCL exceeded Docker's default 1024).
- Set `NCCL_NET=IB` explicitly; otherwise NCCL can fall back to sockets over the management LAN silently.
- Pin the image **digest** on all nodes (a nightly tag from two days gave an NCCL version mismatch).
- Mount the whole Hugging Face cache, not a snapshot directory (snapshots are relative symlinks).
- Start worker ranks first, then the head.

Details of the RoCE environment: [NCCL over RoCE](/clustering/nccl-over-roce.md).

# Limitations

- **Multi-node launcher: sources differ.** NVIDIA's two-Spark playbook uses Ray via `run_cluster.sh` [nv-vllm];
  Capetron reports Ray "is not in the aarch64 images" they used and launches with vLLM's native
  `--nnodes / --node-rank / --distributed-executor-backend mp` [cape-serve]. Check the image you pull.
- vLLM's generic advice is TP within a node and PP across nodes [vllm-par]; a Spark has one GPU, so every multi-Spark
  deployment is TP (or EP) across the network link, and some models cannot be split by PP at all [cape-serve].
- One Capetron configuration loaded only once per boot (`CUDA error: operation not permitted` on restart); recovery
  was a reboot of both nodes, root cause not found [cape-serve].
- Capetron's GLM numbers come from a single setup in August 2026; vLLM moves fast, so re-measure before quoting.
