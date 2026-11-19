---
type: guide
title: "Reference stack: local-ai, and what to adopt next"
description: Maps a real single-Spark stack (local-ai - vLLM behind LiteLLM, with apps) onto this knowledge base - which community practices it already follows, and a backlog of what to test and adopt next, each with the page that justifies it.
tags: [stack, reference, local-ai, vllm, litellm, backlog, best-practices]
resource: /stacks/local-ai-reference-stack.md
timestamp: "2026-11-20T00:00:00Z"
aliases: ["local-ai stack", "adoption backlog", "what to adopt next"]
entities:
  - label: local-ai
    kind: repository
  - label: LiteLLM
    kind: gateway
  - label: vLLM
    kind: inference_engine
relations:
  - type: depends_on
    target: /field-reports/our-home-spark-local-ai.md
  - type: uses
    target: /stacks/vllm.md
  - type: uses
    target: /stacks/coding-agents-on-local-models.md
  - type: cites
    target: /stacks/speculative-decoding.md
  - type: cites
    target: /stacks/quantization-formats.md
  - type: cites
    target: /stacks/sparkring-sparkcache.md
  - type: cites
    target: /clustering/two-node-dac.md
  - type: cites
    target: /hardware/software-support.md
  - type: cites
    target: /hardware/unified-memory-limits.md
  - type: cites
    target: /models/registry-recipes.md
provenance:
  - source: the author's local-ai repository (github.com/rmdes/local-ai), state of 2026-11-19
    note: README, Makefile, config/aliases.txt, models/README.md, models/qwen3.6-35b-a3b-nvfp4/serve.sh and scripts/claude-code-env.sh. Read-only; no secrets read.
citations:
  - id: la
    text: "local-ai, README.md, Makefile, config/aliases.txt, models/README.md and models/qwen3.6-35b-a3b-nvfp4/serve.sh (state of 2026-11-19)."
  - id: la-cc
    text: "local-ai, scripts/claude-code-env.sh (points Claude Code at the gateway's Anthropic-compatible /v1/messages)."
---

# Overview

`local-ai` is one DGX Spark run as a complete home AI server: one vLLM chat engine, small embedding and reranker engines,
a LiteLLM gateway with a virtual key per app or person, and the apps on top, all in Docker Compose [la]. The
[field report](/field-reports/our-home-spark-local-ai.md) covers what it is and how fast it runs. This page is the bridge
between that stack and the rest of this knowledge base: **where the stack already follows community practice, and what
this knowledge base says to try next.** It is the working backlog for evolving the stack.

How it is meant to be used: pick an item from the backlog, run the stated test on the Spark, record the result in
`benchmarks/`, then either adopt the change in the stack or write down why not. Findings that generalise go back into the
relevant page.

# How the stack maps onto the knowledge base

| Layer | What the stack does [la] | Background in this knowledge base |
|---|---|---|
| Engine | vLLM, image pinned by digest; one launch script per model profile that *is* the `vllm serve` command | [vLLM on GB10](/stacks/vllm.md) |
| Model choice | Qwen3.6 35B-A3B in NVFP4 as the daily driver, FP8 as rollback; profiles derived from community recipes with recorded provenance | [Models × Sparks matrix](/models/spark-matrix.md), [registry recipes](/models/registry-recipes.md), [quantization formats](/stacks/quantization-formats.md) |
| Gateway | LiteLLM; apps use aliases (`chat`, `coder`, `think`), never model ids; per-alias thinking switch and scheduler priority | [coding agents on local models](/stacks/coding-agents-on-local-models.md) |
| Access | One scoped virtual key per app or person with a model allow-list; master key admin-only | [coding agents on local models](/stacks/coding-agents-on-local-models.md) |
| Memory | GPU memory fraction 0.55 of the ~121 GiB visible; resident RAG engines at 0.05 each; earlyoom kills the largest inference process first | [unified memory limits](/hardware/unified-memory-limits.md) |
| Host hygiene | Refreshes the NVIDIA CDI spec after every package run; checks the kernel and NVIDIA module match | [software support](/hardware/software-support.md) |
| Measurement | `make bench` (llama-benchy) and `make smoke` (a completion plus a tool call through the gateway) | [benchmarks](https://github.com/rmdes/dgx-spark-skill/tree/main/benchmarks) |

# Practices already followed

| Practice | Why it matters | Source page | How the stack does it [la] |
|---|---|---|---|
| Checkpoint before engine | NVFP4 instead of FP8 on the same engine roughly doubled single-stream decode and freed ~16 GB | [field report](/field-reports/our-home-spark-local-ai.md) | `qwen3.6-35b-a3b-nvfp4` is the daily driver |
| FP8 KV cache | Twice the tokens per GiB at the same speed | [quantization formats](/stacks/quantization-formats.md) | `--kv-cache-dtype fp8` |
| Prefix caching | Long agent contexts are prompt-bound, not decode-bound | [NVIDIA agents on Spark](/field-reports/nvidia-agents-on-spark.md) | `--enable-prefix-caching --enable-chunked-prefill` |
| Pin images by digest | A floating nightly tag gave an NCCL version mismatch, and another ran out of memory on a home Spark | [vLLM on GB10](/stacks/vllm.md) | `VLLM_IMAGE` pinned in each `profile.env` |
| Stable aliases | Swapping a model must not change any client config | [coding agents on local models](/stacks/coding-agents-on-local-models.md) | `make model P=<profile>`; aliases follow `@current` |
| Scoped keys, no master key in clients | Revocable, auditable access | [coding agents on local models](/stacks/coding-agents-on-local-models.md) | `config/litellm/keys.yaml`, allow-lists per key |
| Probe liveness with a real completion | `/v1/models` can stay 200 while completions hang | [coding agents on local models](/stacks/coding-agents-on-local-models.md) | `make smoke` runs a completion and a tool call |
| Guard the host against memory exhaustion | No clean OOM on unified memory; the host can freeze | [unified memory limits](/hardware/unified-memory-limits.md) | earlyoom plus a lowered memory fraction |
| Keep the CDI spec fresh | A stale spec blocks every new GPU container | [software support](/hardware/software-support.md) | apt hook in `config/apt/` |

# Adoption backlog

Ordered by expected value for a single, shared Spark. Status is what the stack's own documentation shows today.

| # | Item | Why (source) | Test on the Spark | Status |
|---|---|---|---|---|
| 1 | **Speculative decoding under concurrency** | A drafter can help one user and hurt a shared endpoint: one independent run gained 48 % alone and lost 47 % aggregate at six streams ([speculative decoding](/stacks/speculative-decoding.md)) | A/B the daily driver with MTP on and off at 1, 5 and 8 concurrent streams, several fresh starts each (`benchmarks/ab-tuning.sh` already automates interleaved starts) | The stack runs MTP with two draft tokens [la]; on a second box three tokens was worse and async scheduling neutral ([benchmarks](https://github.com/rmdes/dgx-spark-skill/tree/main/benchmarks)); the on/off comparison under load is not recorded |
| 2 | **A task-based quality benchmark** | Speed claims depend on task type, context and concurrency; a smoke test is not a quality benchmark ([Alex Ellis, four Sparks](/field-reports/alex-ellis-four-sparks.md), [local vs Opus](/field-reports/alex-ellis-local-vs-opus.md)) | Run RigMark, and a small set of real tasks, on the daily driver and on any candidate model; record the exact setup | `make bench` measures speed only [la] |
| 3 | **Verify the Claude Code route end to end** | Some server and model pairs emit prose but make no edits ([coding agents on local models](/stacks/coding-agents-on-local-models.md)) | Run a real multi-file edit task through the gateway's `/v1/messages`; note the LiteLLM version, alias and settings that worked, and what broke | The repository ships a script that points Claude Code at the gateway [la-cc]; that it completes edit tasks is not documented |
| 4 | **Persistent prompt cache** | SparkCache restores the longest matching prefix across evictions and restarts, but is labelled experimental ([sparkring and SparkCache](/stacks/sparkring-sparkcache.md)) | Measure cold-start prefill on a 32k agent context with and without it; check the memory cost on the shared pool | Not used |
| 5 | **A second Spark over one cable** | Two Sparks run models that one cannot (DeepSeek V4.1 Flash, GLM 5.3 Flash class); for several users, independent endpoints beat one sharded model ([matrix](/models/spark-matrix.md), [two-node runbook](/clustering/two-node-dac.md)) | Follow the runbook, prove the link with `ib_write_bw`, then serve one explorer model and compare it with the daily driver on the same tasks | Single node |
| 6 | **Re-check the engine policy against independent measurements** | The stack treats single-maintainer engines as research only; most registry figures are author-reported, and only a minority were lab-measured ([registry recipes](/models/registry-recipes.md), [TensorFold](/stacks/tensorfold.md), [SGLang](/stacks/sglang.md)) | When a recipe for your model gains independent measurements, run it next to the vLLM profile with `make bench` on the same box | Policy documented in the stack's research notes [la] |
| 7 | **Remote power control** | The GB10 has no BMC; a wedged unit needs a physical or smart-PDU power cycle ([power and thermals](/hardware/power-and-thermals.md)) | Put the Spark behind a smart PDU and test a remote cycle and the reboot-to-ready time | Not documented |

# Keeping the backlog honest

- Re-test after any change of vLLM image, kernel or driver: single-stream decode varied by up to ~20 % between starts on
  identical setups, so use three or more fresh starts per variant.
- A finding that disagrees with a page here is more valuable than one that confirms it: update the page and its date.
- Prefer one change per experiment, and keep the raw output in `benchmarks/`.

# Limitations

- The stack's state is read from its repository on 2026-11-19; the repository changes faster than this page.
- Status entries say what the stack's documentation shows, not whether something has been tried and not written down.
- The stack is a single desktop GB10 with apps running on it; results may differ on a headless or clustered box.
