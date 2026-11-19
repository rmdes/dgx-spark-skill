---
type: component
title: TensorFold engine
description: Ash Hart's open-source inference engine (Python 0.6 line, native Zig 1.x line) with per-family CUDA kernels and exact speculative decoding — the engine behind the fastest published DGX Spark recipes.
tags: [tensorfold, inference-engine, zig, speculative-decoding, openai-api, anthropic-api, engine-choice]
resource: /stacks/tensorfold.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [tensorfold-native, TensorFold Zig engine, TF]
entities:
  - label: TensorFold
    kind: inference_engine
  - label: tensorfold-native
    kind: binary
  - label: MiaAI-Lab recipes
    kind: recipe_collection
relations:
  - type: runs_on
    target: /hardware/gb10-platform.md
  - type: implements
    target: /stacks/speculative-decoding.md
  - type: reads
    target: /stacks/quantization-formats.md
  - type: compared_with
    target: /stacks/vllm.md
  - type: compared_with
    target: /stacks/sglang.md
  - type: powers
    target: /models/qwen38-27b-1x-tensorfold.md
  - type: summarized_in
    target: /models/spark-matrix.md
provenance:
  - source: https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/README.md
    note: Upstream README at commit d33dcfc (native release 1.1.9 quick start, model table, serve flags, exact decoding).
  - source: https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/RELEASE-NOTES-1.0.0.md
    note: 1.0.0 release notes — the switch from the Python engine to the native Zig engine.
  - source: https://mia-ai.net/models
    note: MiaAI-Lab recipe pages that patch TensorFold for DGX Spark; all numbers self-reported, measured with sparkDash.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md
    note: Independent stock-vLLM measurements used as the comparison point.
citations:
  - id: tf-readme
    text: "Ash Hart, TensorFold README (Apache-2.0), commit d33dcfc. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/README.md"
  - id: tf-100
    text: "Ash Hart, TensorFold 1.0.0 release notes. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/RELEASE-NOTES-1.0.0.md"
  - id: tf-zig
    text: "Ash Hart, TensorFold Zig engine preview. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/ZIG-PREVIEW.md"
  - id: tf-exl3
    text: "Ash Hart, TensorFold docs — EXL3 weights. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/recipes/exl3.md"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: mia-fn1
    text: "MiaAI-Lab, Qwen3.8 Flash Next on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold"
  - id: mia-fn2
    text: "MiaAI-Lab, Qwen3.8 Flash Next on two DGX Sparks with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-glm3
    text: "MiaAI-Lab, GLM 5.3 on three DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-EXL3-3x-DGX-Sparks-TensorFold"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek V4.1 Flash 1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: ds-tf2
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 EXL3 on 2x DGX Sparks with TensorFold (README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/blob/d8e5b28da6ebcf539035be564a4a94d087b2f480/README.md"
  - id: ds-vllm2
    text: "MiaAI-Lab, DeepSeek v4.1 Flash EXL3 2.9 bpw for 2x DGX Sparks (vLLM, README). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-EXL3-2x-DGX-Sparks/blob/6f7d1590ad49a2b8995188e45d7b9db31e677452/README.md"
  - id: glm-vllm2
    text: "MiaAI-Lab, GLM-5.3 Flash EXL3 on DGX Spark (vLLM, README). https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks/blob/a8cc40ddef876f033e0f1b4d8f178b0fee2a5351/README.md"
  - id: sgl-q27
    text: "MiaAI-Lab, Qwen3.8 27B on SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md"
  - id: sr-readme
    text: "SparkRing README (Apache-2.0), commit b9cd552. https://github.com/MiaAI-Lab/sparkring/blob/b9cd552fdf8ea92edb5d4c0f83ac29bed8d1e6cf/README.md"
  - id: cape-serve
    text: "Capetron, GB10 cluster guide — 05 Serving models across the fabric: vLLM on sm_121 (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/05-serving-models.md"
---

# Overview

TensorFold, by Ash Hart (Apache-2.0), serves language models on Apple Silicon and NVIDIA GPUs behind an
OpenAI-compatible API [tf-readme]. Two things set it apart from [vLLM](/stacks/vllm.md) and
[SGLang](/stacks/sglang.md):

- **One code path per model family.** Each family (Qwen3.8-27B, Flash Next, GLM-5.3-Flash, Nemotron, DeepSeek-V4,
  Gemma 4 …) brings its own kernels and its own draft verification instead of one generic path [mia-q27].
- **Exact decoding as a hard rule.** "Every accepted draft must equal the token the same native engine would produce
  with `"draft": false`." Resumed requests must equal fresh ones, and each concurrent stream must equal its solo run
  [tf-readme]. See [Speculative decoding](/stacks/speculative-decoding.md).

On DGX Spark it is the engine of the fastest recipes in the [Models × Sparks matrix](/models/spark-matrix.md), almost
all of them published by one lab (MiaAI-Lab) as patched TensorFold builds.

# Two engines: Python 0.6 and native Zig 1.x

| Line | What it is | Status (README at d33dcfc) |
|---|---|---|
| Python 0.6.x | Python engine, frozen at 0.6.6 on the `python-0.6` branch / `v0.6.6` tag | Still the base of several Spark recipes (27B, GLM-5.3-Flash, full GLM 5.3 all patch **v0.6.0**) [mia-q27] [mia-glm3] |
| Native Zig 1.x | `tensorfold-native`: loading, tokenizing, chat templates and inference in one Zig process, no Python at runtime | 1.0.0 shipped it; quick start installs **1.1.9**; release archive `linux-aarch64` targets the GB10 [tf-readme] [tf-100] |

What 1.0.0 recorded for CUDA on the GB10: greedy and sampled replies equal the one-token reference, concurrent
streams equal their solo runs, and decode runs **1.01× to 1.10× the Python 0.6.6 engine** on the same Spark [tf-100].
The Zig preview's speed tables (essay 277 tok/s vs ~220 for the Python engine) are from an **M5 Max Mac**, not a
Spark [tf-zig].

The native server exposes `/v1/chat/completions`, `/v1/completions`, Responses, **Anthropic Messages** and token
counting, tool calls, streaming, `/health` and `/metrics` [tf-100]. The GLM-5.3-Flash recipe advertises the Anthropic
route explicitly "so Claude Code and the Anthropic SDKs talk to it directly, without a translating proxy" [mia-glmf].

# What the MiaAI recipes patch

The recipes do not run stock TensorFold; each pins a TensorFold version and adds patches.

| Recipe | TensorFold base | What the patches add |
|---|---|---|
| Qwen3.8 27B, 1 Spark | v0.6.0 + 5 patches | up to 50 images + video, opt-in YaRN to 1,048,576 tokens, FP8 attention cache on by default, memory reserve 0, pinned KV pool [mia-q27] |
| Nemotron 3.5 Bolt, 1 Spark | Zig engine at a pinned 1.0.12 commit | a new **Bolt backend** (`libbolt.so`) plugged in through the lane interface (`verify`/`keep`/`draft`), video input [mia-bolt] |
| Qwen3.8 Flash Next, 1 Spark | Zig engine 1.1.4 | patches 0011–0015: NVIDIA's FP4 QAD checkpoint (CSF-compressed NVFP4 scales, MXFP8 linears), draft tuning, faster prompt pass [mia-fn1] |
| Qwen3.8 Flash Next, 2 Sparks | Zig engine, `zig-flashnext` branch | 9 patches: Flash Next port, two ranks, serving, kernel set, vision helper [mia-fn2] |
| GLM 5.3 Flash, 2–4 Sparks | v0.6.0 + 68 patches | 3-rank engine (patches 0066–0068), Anthropic API backport, spill tier, 4-Spark ring on a `tp4` branch [mia-glmf] [mia-glm3] |
| GLM 5.3 (full), 3 Sparks | v0.6.0 + 110 patches | 3-rank layout, mixed-width EXL3 loader, DSpark drafts, context parallelism, 4-bit KV cache, NVMe prompt cache [mia-glm3] |
| DeepSeek V4.1 Flash 1017, 4 Sparks | Zig engine at BertholomusAI's `deepseek-v41-zig-tp4` branch + 25 patches | DeepSeek's FP8/MXFP4 checkpoint as published, ring node order, video input, tool-call arguments [mia-ds4] |

**Source conflict, for the record:** upstream TensorFold says DeepSeek checkpoints are **not served by any release
binary** (whole-model gate #827 still open) [tf-readme]; the DeepSeek recipes run a contributor's fork, not a
TensorFold release [mia-ds4]. Likewise the upstream EXL3 page says "No model serves an EXL3 checkpoint in this
release" [tf-exl3], while the README's model table lists a GLM-5.3-Flash EXL3/TR3 native path as experimental
[tf-readme]. Treat EXL3 and DeepSeek on TensorFold as recipe-level, not release-level, support.

# Measured (self-reported, sparkDash)

All rows: MiaAI-Lab recipe pages, measured by the recipe author through the OpenAI API. Not reproduced by us.

| Recipe | Sparks | 1 request (prose) | Many requests (aggregate) | Prefill, ~32k prompt |
|---|---|---|---|---|
| Nemotron 3.5 Bolt 74B-A9B | 1 | 71.0 tok/s | 166.6 ×8 | 1,375 tok/s [mia-bolt] |
| Qwen3.8 27B | 1 | 58.3 tok/s | 220.6 ×8 | 1,633 tok/s [mia-q27] |
| Qwen3.8 Flash Next (NVIDIA FP4 QAD) | 1 | 55.6 tok/s | 156.1 ×5 | 2,735 tok/s [mia-fn1] |
| Qwen3.8 Flash Next (NVFP4) | 2 | 67.4 tok/s | 390.1 ×16 | 2,575 tok/s [mia-fn2] |
| GLM 5.3 Flash (EXL3 4 bpw) | 2 / 3 / 4 | 60.4 / 77.6 / 95.2 tok/s | 108.8 ×4 (2 Sparks) | 1,979 tok/s (2 Sparks) [mia-glmf] |
| GLM 5.3 full (EXL3 2.75 bpw) | 3 | 31.3 tok/s (code 41.7) | 48.2 ×4 (`CP=0`) | 591 tok/s [mia-glm3] |
| DeepSeek V4.1 Flash 1017 (FP8 + MXFP4) | 4 | 65.8 tok/s | 165.3 ×8 | 4,127 tok/s [mia-ds4] |

# Which engine for which job

Evidence only; dates, checkpoints and probes differ between rows, so read these as directions, not rankings.

**One user, one Spark (interactive coding):** the per-family TensorFold recipes publish the highest single-stream
numbers on one Spark (27B: 58.3 tok/s prose, 136.9 code [mia-q27]). The same model on SGLang with DFlash2 reached
56.6 tok/s on a structural fixture but 25.4 tok/s on a long-essay probe [sgl-q27]. The independent stock-vLLM
measurement of Qwen3.8 Flash Next on one Spark (RadixArk NVFP4 checkpoint, August 2026) was 24.8 tok/s prose,
against 55.6 for the TensorFold recipe on NVIDIA's FP4 QAD checkpoint (October 2026) [cape-serve] [mia-fn1].

**Same model, same Sparks, two engines (2 Sparks):**

| Model | vLLM recipe | TensorFold recipe |
|---|---|---|
| GLM 5.3 Flash, EXL3 4 bpw | 36.1 tok/s prose, 54.6 code [glm-vllm2] | 60.4 tok/s prose [mia-glmf] |
| DeepSeek V4.1 Flash, EXL3 2.9 bpw | 31.6 tok/s prose ×1 [ds-vllm2] | 74.9 tok/s prose ×1 (the 1017 revision of the checkpoint) [ds-tf2] |

The vLLM GLM recipe's own README now tells readers to use the TensorFold version, which "runs faster" [glm-vllm2].

**Many users (a team endpoint):** aggregate throughput is where engines converge and where topology matters more.
TensorFold 27B: 220.6 tok/s at 8 requests [mia-q27]; SGLang 27B with DFlash2: 227.6 tok/s at 16 [sgl-q27].
Independent data says the cheapest way to serve many users is **one model copy per Spark**: four single-Spark
vLLM endpoints of Qwen3.8 Flash Next give about 345 tok/s aggregate against 167 tok/s for the same model sharded over
the same four Sparks [cape-serve]. Speculative decoding can also *lower* aggregate throughput under load (see
[Speculative decoding](/stacks/speculative-decoding.md)).

**Biggest model:** only TensorFold recipes publish the full GLM 5.3 (~273 GiB checkpoint, 3 Sparks) [mia-glm3] and
DeepSeek V4.1 Flash 1017 unquantized (~510 GB, 4 Sparks) [mia-ds4]. The vLLM-based
[SparkRing](/stacks/sparkring-sparkcache.md) stack publishes the highest **aggregate** numbers on 4 Sparks
(DeepSeek-V4-Flash-0731: 508.11 tok/s at 32 concurrent, 68.84 at 1) [sr-readme].

**Support and risk:** vLLM and SGLang have NVIDIA playbooks and vendor images; TensorFold has none, the Spark
recipes come from a small group of community authors, and recipes change several times a week. A TensorFold
recipe is the fastest way to a demo; vLLM is the safer base for a service other people depend on.

# Examples

```bash
# Native release on a GB10 (from the upstream README)
V=1.1.9
curl -fLO "https://github.com/ashhart/TensorFold/releases/download/v$V/tensorfold-$V-linux-aarch64.tar.gz"
curl -fLO "https://github.com/ashhart/TensorFold/releases/download/v$V/tensorfold-$V-linux-aarch64.tar.gz.sha256"
sha256sum -c "tensorfold-$V-linux-aarch64.tar.gz.sha256"
tar -xzf "tensorfold-$V-linux-aarch64.tar.gz"
export PATH="$PWD/tensorfold-$V-linux-aarch64/bin:$PATH"
tensorfold-native pull TensorFold/Qwen3.8-27B-MLX-4bit
tensorfold-native pull z-lab/Qwen3.8-27B-DFlash2
tensorfold-native serve TensorFold/Qwen3.8-27B-MLX-4bit --name local-model \
  --drafter z-lab/Qwen3.8-27B-DFlash2      # listens on 127.0.0.1:8080 by default

# Compare against the exact serial reference on any request
curl -s http://127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"local-model","messages":[{"role":"user","content":"hi"}],"draft":false}'
```

Useful serve flags: `--parallel N|auto` (auto asks for up to 8 streams), `--prompt-cache-gib`, `--compact-at`
(context compaction, off by default), `--no-drafts`, `--api-key-file` [tf-readme].

# Limitations

- **Unified-memory freeze.** Several recipes warn that running out of unified memory freezes the Spark instead of
  failing a process; they keep a 10 GiB floor or a guard that stops the rank first [mia-fn1] [mia-glm3]. See
  [Unified memory limits](/hardware/unified-memory-limits.md).
- "Exact" is relative to one checkpoint, backend, settings and runtime. Different quantizations and backends can
  produce different outputs [tf-readme]; lossy defaults such as FP8 KV or FP8 prompts are lossy against BF16.
- Some recipe features refuse requests rather than degrade: Flash Next refuses structured outputs, `logprobs` and
  `n` ≠ 1 with HTTP 400 [mia-fn1]; Bolt does not serve logprobs or grammar-constrained decoding [mia-bolt].
- All Spark numbers above are self-reported by recipe authors; we have not reproduced them on our units yet.
