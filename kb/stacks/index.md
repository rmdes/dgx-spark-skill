# Serving stacks

Inference engines and orchestration used on Sparks, and when to pick each.

<!-- okf:generated:index begin -->
# component

* [EXL3 and ExLlamaV3 on Spark](/stacks/exl3-exllamav3.md) - ExLlamaV3's EXL3 trellis quantization (fractional bits per weight, mcg/mul1 codebooks) and the three ways it is served on DGX Spark — vLLM overlays, SparkRing's exl3-r7 runtime, and TensorFold.
* [SGLang on DGX Spark](/stacks/sglang.md) - SGLang on the GB10 — which published Spark recipes use it (Qwen3.8 27B, Ling 3.0 Flash, MiMo V2.6 Flash), its DSpark/DFlash2/MTP speculative modes, and the numbers measured on the box.
* [SparkRing and SparkCache](/stacks/sparkring-sparkcache.md) - SparkRing, a vLLM-based serving stack and custom RDMA collective layer for switchless 2- and 4-Spark clusters, and SparkCache, its persistent on-disk prompt cache — what they do, how they measure, and their published numbers.
* [TensorFold engine](/stacks/tensorfold.md) - Ash Hart's open-source inference engine (Python 0.6 line, native Zig 1.x line) with per-family CUDA kernels and exact speculative decoding — the engine behind the fastest published DGX Spark recipes.
* [vLLM on GB10 (sm_121)](/stacks/vllm.md) - Why stock vLLM images failed on the DGX Spark's sm_121 GPU, the community patch chain that fixed it, how vLLM's memory settings behave on unified memory, and what has been measured working.

# concept

* [Quantization formats on GB10](/stacks/quantization-formats.md) - NVFP4, MXFP4, FP8, INT4-AutoRound, MLX 4-bit and EXL3 compared for the DGX Spark — what each stores, the published quality numbers (KL, perplexity, GPQA, task scores) and the measured speed trade-offs on GB10.
* [Speculative decoding on Spark](/stacks/speculative-decoding.md) - How draft-and-verify decoding (MTP, EAGLE, DFlash2, DSpark, LiLiCorr, copy and n-gram drafts) multiplies per-stream speed on the bandwidth-bound GB10, what each drafter is, measured gains, when it hurts, and what "exact decoding" guarantees.

# guide

* [Coding agents on local models](/stacks/coding-agents-on-local-models.md) - How to wire opencode, Claude Code, pi, Hermes, Aider, Continue, Open WebUI and OpenAI SDK clients to models served on DGX Sparks directly or through a gateway, and the traps that bite in daily use.

# reference

* [NVIDIA DGX Spark playbooks — what is officially supported](/stacks/nvidia-playbooks.md) - Every playbook in NVIDIA's dgx-spark-playbooks repository (commit 3088315, October 2026), sorted by category with stated duration and risk, and which ones matter for a small team doing daily development on local models.
<!-- okf:generated:index end -->
