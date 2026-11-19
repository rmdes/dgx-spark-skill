---
type: component
title: SGLang on DGX Spark
description: SGLang on the GB10 — which published Spark recipes use it (Qwen3.8 27B, Ling 3.0 Flash, MiMo V2.6 Flash), its DSpark/DFlash2/MTP speculative modes, and the numbers measured on the box.
tags: [sglang, inference-engine, dspark, dflash2, mtp, single-node, multi-node]
resource: /stacks/sglang.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [SGLang, lmsysorg/sglang]
entities:
  - label: SGLang
    kind: inference_engine
  - label: DSpark
    kind: speculative_decoder
  - label: lmsysorg/sglang
    kind: container_image
relations:
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: implements
    target: /stacks/speculative-decoding.md
  - type: compared_with
    target: /stacks/vllm.md
  - type: compared_with
    target: /stacks/tensorfold.md
  - type: constrained_by
    target: /hardware/unified-memory-limits.md
  - type: summarized_in
    target: /models/spark-matrix.md
provenance:
  - source: https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md
    note: One-Spark Qwen3.8 27B recipe with three speculative modes, measured on-device (self-reported).
  - source: https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark/blob/ca840cb8d032353e24648aeee06312b0938348f6/README.md
    note: One-Spark Ling 3.0 Flash INT4 recipe with DSpark (self-reported).
  - source: https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks/blob/201be3e743d215291feee09fe470822ec453c63d/README.md
    note: Two-Spark MiMo V2.6 Flash recipe; detailed boot-failure notes (self-reported).
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: Independent comparison of an SGLang two-node lane against vLLM.
citations:
  - id: sgl-q27
    text: "MiaAI-Lab, Qwen3.8 27B on SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md"
  - id: sgl-ling
    text: "MiaAI-Lab, Ling-3.0-Flash SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark/blob/ca840cb8d032353e24648aeee06312b0938348f6/README.md"
  - id: sgl-mimo
    text: "MiaAI-Lab, MiMo-V2.6-Flash for 2x DGX Sparks (README). https://github.com/MiaAI-Lab/MiMo-V2.6-Flash-2x-DGX-Sparks/blob/201be3e743d215291feee09fe470822ec453c63d/README.md"
  - id: nv-sglang
    text: "NVIDIA, DGX Spark playbook — SGLang. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/sglang/README.md"
  - id: nv-forum
    text: "NVIDIA Developer Forums, DGX Spark (SM121) Software Support is Severely Lacking — Official Roadmap Needed (2026-01-15). https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric: vLLM on sm_121 (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
---

# Overview

SGLang is the second mainstream engine on DGX Spark. NVIDIA's playbook uses the CUDA 13 image
`lmsysorg/sglang:latest-cu130` [nv-sglang]. In January 2026 a four-node owner reported SGLang running "on an
unofficial branch with temporary workarounds" (sglang#11658 open); NVIDIA replied that it runs correctly via its
official custom wheel [nv-forum]. The published Spark recipes in practice pin **model-specific dev images**
(`lmsysorg/sglang:qwen38-27b`, `dev-qwen38-27b-dflash2`, `dev-Ling-3.0-flash`, a `nightly-dev-cu13` build), because
the features they need had not reached a release tag [sgl-q27] [sgl-ling] [sgl-mimo].

Where SGLang stands out on Spark is **speculative-decoding choice**: one recipe can boot with MTP, DSpark or DFlash2
and measure each. See [Speculative decoding](/stacks/speculative-decoding.md).

# Recipes that use it

| Recipe | Sparks | Weights | Drafter | 1 stream | Many streams |
|---|---|---|---|---|---|
| Qwen3.8 27B | 1 | NVFP4 (RadixArk, BF16 LM head) | DFlash2 | 56.6 tok/s (structural fixture) | 227.6 tok/s ×16 [sgl-q27] |
| Qwen3.8 27B | 1 | NVFP4 | DSpark block-7 | code 51.5, long essay 18.3 tok/s | n/p [sgl-q27] |
| Ling 3.0 Flash | 1 | INT4 (official) | DSpark | 83 tok/s | 136 tok/s ×6 [sgl-ling] |
| MiMo V2.6 Flash (309B, 15B active) | 2 (TP2 over RoCE) | MXFP4 experts, FP8 attention | EAGLE MTP (default) | prose 35.0, code 46.0 tok/s | prose 119.9, code 138.7 ×8 [sgl-mimo] |
| MiMo V2.6 Flash | 2 | same | DFlash | prose 25.8, code 69.8 tok/s | prose 103.0, code 190.3 ×8 [sgl-mimo] |

All self-reported by the recipe author (MiaAI-Lab). The 27B README itself warns that two boots of the same image
differed 6.5 % on its essay probe and that code deltas under 15 % are noise [sgl-q27].

Independent comparison: Capetron measured MiaAI-Lab's SGLang two-node lane for Qwen3.8 Flash Next against vLLM; it
**tied on code and lost on prose, math, aggregate and prefill**, so they kept vLLM [cape-serve].

# Measured details worth knowing

- **Ling 3.0 Flash:** DSpark is 2.2× the built-in MTP (NEXTN) at one stream (83 vs 37 tok/s) and 1.8× at six
  (136 vs 76); accepted length 5.2–6.4 tokens per step [sgl-ling].
- **Qwen3.8 27B:** DFlash2 vs EAGLE/MTP on the same session: 2.25× on code (24.20 → 54.56 tok/s) and 1.41× on the
  essay (18.19 → 25.61) [sgl-q27]. MTP steps 3/1/4 were the measured optimum; NGRAM drafting ran ~30 % under MTP
  [sgl-q27].
- **Tuning ceiling:** every kernel-path and config/host experiment on the 27B measured zero net gain; the shipped
  config is the local optimum on that box [sgl-q27].
- **Context:** 27B serves native 262k with 10 concurrent requests; up to 1M with YaRN, but only ~2 full 1M requests
  fit (~33 GB of KV each in a ~75 GB pool) [sgl-q27].

# Memory on unified memory

- `--mem-fraction-static` sets the share of the unified pool given to weights + KV. On Ling at 0.87 the KV pool is
  576,930 tokens and host MemAvailable sits at ~9.5 GiB; at 0.75 it is 237,922 tokens with ~24 GB free [sgl-ling].
- MiMo's recipe kills SGLang below 4 GiB MemAvailable "which ends in an exited container instead of a rebooted
  Spark" [sgl-mimo].
- **Source conflict:** the Ling README recommends `DOCKER_MEMORY` (a container cap) "so the container dies before the
  host OOMs" [sgl-ling]; Capetron reports that GPU and unified-memory allocations are not cgroup-charged, so a
  container memory cap did not engage [cape-serve]. Prefer a MemAvailable guard; see
  [Unified memory limits](/hardware/unified-memory-limits.md).
- Weight loading: SGLang's default mmap loader took 525 s for an 82 GiB rank on GB10 (CUDA pageable copies fault mmap
  pages 4 KiB at a time); a patch that clones one tensor at a time cut it to 96 s [sgl-mimo].

# Runbook

```bash
# NVIDIA playbook image check
docker run --rm --gpus all lmsysorg/sglang:latest-cu130 nvidia-smi

# Ling 3.0 Flash recipe (one Spark, DSpark, 256k context, 6 concurrent)
git clone https://github.com/MiaAI-Lab/Ling-3.0-Flash-SGLang-DSpark-DGX-Spark.git
cd Ling-3.0-Flash-SGLang-DSpark-DGX-Spark
./start.sh --download-only
./start.sh                       # SPEC_ALGO=nextn or off for the alternatives
curl -fsS http://127.0.0.1:8888/v1/models
```

# Limitations

- The drafter is a **boot-time** choice: no per-request switch, no dual-drafter mode [sgl-mimo].
- EAGLE MTP on MiMo requires decode CUDA graphs off (`CUDA_GRAPH_MAX_BS_DECODE=0`) or the boot fails [sgl-mimo].
- DSpark with YaRN on the 27B: the YaRN override leaks into the draft config and crashes at boot; keep 262k [sgl-q27].
- MiMo's MXFP4 experts need a recent nightly (sglang PR #40448); older engines expand the experts to FP8 and take
  the node down [sgl-mimo].
- MiMo on 2 Sparks: four node reboots and two OOM kills during bring-up; concurrency scaling and needle tests are
  marked "not measured" by the author [sgl-mimo].
