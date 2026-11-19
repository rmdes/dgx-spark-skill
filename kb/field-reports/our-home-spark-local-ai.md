---
type: report
title: "Field report: a home Spark stack (local-ai)"
description: A single DGX Spark Founders Edition run as a home AI server - one vLLM behind a LiteLLM gateway over Tailscale - with measured benchmarks of four models and the engine research behind its design.
tags: [field-report, self-measured, vllm, litellm, tailscale, benchmarks]
resource: /field-reports/our-home-spark-local-ai.md
timestamp: "2026-10-30T00:00:00Z"
aliases: ["local-ai", "home Spark"]
entities:
  - label: local-ai
    kind: repository
  - label: llama-benchy
    kind: benchmark
  - label: Tailscale
    kind: network
relations:
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: uses
    target: /stacks/vllm.md
provenance:
  - source: the author's local-ai repository (commit 44a41f9, 2026-10-30)
    note: README, models/README.md, models/*/profile.env, scripts/bench.sh, benchmarks/results/*.md and docs/inference-stack-research-2026-10.md. Read-only; no secrets read.
citations:
  - id: la-readme
    text: "local-ai, README.md (architecture, endpoints, measured profile table, memory notes)."
  - id: la-bench
    text: "local-ai, scripts/bench.sh and benchmarks/results/20261019-* and 20261021-0926-qwen3.6-35b-a3b-nvfp4.md (llama-benchy)."
  - id: la-research
    text: "local-ai, docs/inference-stack-research-2026-10.md (engine and launcher research, 2026-10-19)."
  - id: la-models
    text: "local-ai, models/README.md and models/*/profile.env."
---

# Overview

**Source type: self-operated, self-measured (one author).** An NVIDIA DGX Spark Founders Edition runs the `local-ai`
stack: one vLLM chat engine plus embedding and reranker servers behind a LiteLLM gateway with one virtual key per app or
machine, all in Docker Compose, reachable over Tailscale [la-readme]. A reboot brings everything back.

| | |
|---|---|
| Gateway | LiteLLM on `:4000` (LAN) and `:4443` (tailnet); virtual keys kept as code in `config/litellm/keys.yaml` |
| Chat model (daily) | `nvidia/Qwen3.6-35B-A3B-NVFP4` with MTP speculative decoding, GPU memory fraction 0.55 |
| RAG models | Qwen3-Embedding-0.6B, Qwen3-Reranker-0.6B |
| Apps on the box | Open WebUI, Hermes Agent, OpenClaw, Dozzle |
| Aliases | `chat`, `coder`, `think` (+ others); apps use aliases, never model ids |

Sources: [la-readme] [la-models]. The rule that apps reference aliases means a model swap changes no client config; see
[coding agents on local models](/stacks/coding-agents-on-local-models.md) for the gateway pattern. The same model was also
measured on a Dell Pro Max GB10: it ran 16-35 % slower with identical software (raw numbers in `benchmarks/`, see
[GB10 platform](/hardware/gb10-platform.md)).

# Measured on the Founders Edition

llama-benchy, prefill 2,048 tokens, generation 128, depth 0 / 8k / 32k, concurrency 1 and 5, 2 runs, speculative decoding
on, non-thinking, desktop session running [la-bench] [la-readme]:

| Profile | Weights | Load → ready | Decode 1× | Decode 5× aggregate | Prefill pp2048 | Decode 1× @ 32k | Tool call |
|---|---|---|---|---|---|---|---|
| `qwen3.6-35b-a3b-nvfp4` (daily) | 19 GB | 161 s | **108 tok/s** (117 on 2026-10-21) | **219** (230) | **7,700** (8,400) | 97 | ok |
| `qwen3.6-35b-a3b-fp8` (rollback) | 35 GB | 160 s | 55 tok/s | 154 | 4,700 | 58 | ok |
| `qwen3.8-flash-next-fp4` (176B total) | 96 GB on disk | 944 s | 34 tok/s | 62 | 2,000 | 34 | ok |
| `nemotron-3.5-super-vl-nvfp4` (120B, vision) | 70 GB | 342 s | 21 tok/s | 50 | 2,700 | 8 | ok |

Figures dated 2026-10-19; the 2026-10-21 re-run at memory 0.55 is in brackets [la-readme] [la-bench].

**Against the catalogs:** the same Qwen3.8 Flash Next on one Spark measured 34 tok/s here with stock vLLM, where the
MiaAI-Lab TensorFold recipe reports 55.6 ([matrix](/models/spark-matrix.md)) — consistent with the finding that engine and
recipe move the numbers as much as the hardware.

# What the engine research concluded (2026-10-19)

From the research that led to this stack [la-research]:

| Engine / tool | Verdict for a single Spark |
|---|---|
| vLLM | primary engine; batches properly (≈290–320 tok/s aggregate at 8 streams reported) |
| llama.cpp | secondary, for big GGUFs and fast swaps; slower decode on this model |
| Ollama | skip: no batching (8 concurrent ≈ 1 concurrent) |
| SGLang | experiment only (Spark "not yet validated" in its cookbook, sm_121 patches) |
| TensorRT-LLM, NIM | skip for Qwen (compile errors on sm_121a; short NIM list) |
| Single-maintainer engines (TensorFold, ds4, exllamav3 fork…) | ignore for production |
| sparkrun | wrapper bugs and floating images; keep it as a recipe resolver, not a runtime |

The biggest lever was **the checkpoint, not the engine**: moving Qwen3.6-35B from FP8 to NVFP4 on the same vLLM roughly
doubled single-stream decode (45–52 → 108–117 tok/s) and freed ~16 GB [la-research] [la-readme]. Tool calls need the
`qwen3_xml` parser on Qwen3.6 [la-research].

# Lessons

- Pin images by digest; a floating nightly ran out of memory where an older image worked [la-research].
- 121 GiB is visible to CUDA and a desktop takes 10–15 GB of it; `--gpu-memory-utilization` is a fraction of the 121 GiB.
  Vision-encoder profiling can spike memory, which is why the Qwen3.6 profiles are text-only [la-readme].
- earlyoom kills the largest inference process first; the gateway and its database are protected [la-readme].

# What to take from it

- A single Spark with one 35B-class NVFP4 model, a gateway and a handful of apps is a complete, usable home server.
- Engine policy that held up: vLLM as the baseline, single-maintainer engines as research only. Numbers from one-person
  engines (see the [matrix](/models/spark-matrix.md)) are best cases.
- `make bench` (llama-benchy, settings in `benchmarks/README.md`) is a repeatable benchmark; use the same settings on your
  own box so results are comparable.
