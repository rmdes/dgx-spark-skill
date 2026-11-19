<!-- ABOUTME: Raw llama-benchy results backing the knowledge base's own measurements on two GB10 boxes. -->
<!-- ABOUTME: Same command on both boxes, so rows are directly comparable. -->
# Benchmarks

Raw `llama-benchy` output behind the measured numbers in
[`kb/field-reports/our-home-spark-local-ai.md`](../kb/field-reports/our-home-spark-local-ai.md) and the
[Models × Sparks matrix](../kb/models/spark-matrix.md). Two boxes, one command, run directly against vLLM on
`127.0.0.1:8000` (gateway bypassed):

- **NVIDIA FE**: an NVIDIA DGX Spark Founders Edition.
- **Dell GB10**: a Dell Pro Max with GB10 (FCM1253).

```bash
uvx llama-benchy --base-url http://127.0.0.1:8000/v1 \
  --model nvidia/Qwen3.6-35B-A3B-NVFP4 --tokenizer nvidia/Qwen3.6-35B-A3B-NVFP4 \
  --pp 2048 --tg 128 --depth 0 8192 32768 --concurrency 1 5 --runs 2 \
  --enable-prefix-caching --latency-mode generation --format md
```

| File | Box | Setup |
|---|---|---|
| `results/20261021-0926-nvidia-fe-qwen3.6-35b-a3b-nvfp4.md` | NVIDIA FE | vLLM image `…6d5afe0e7d90`, memory 0.55, 16 seqs, priority scheduling |
| `results/20261030-1026-dell-gb10-qwen3.6-35b-a3b-nvfp4.md` | Dell GB10 | image `…7bb73915fd1e`, memory 0.40, 8 seqs; box idle (GPU 0 %) at start |
| `results/20261030-1118-dell-gb10-qwen3.6-35b-a3b-nvfp4-image-6d5afe.md` | Dell GB10 | A/B: same profile, image `…6d5afe0e7d90` (the FE's) via a temporary override |
| `results/20261030-1124-dell-gb10-qwen3.6-35b-a3b-nvfp4-baseline2.md` | Dell GB10 | baseline re-run on `…7bb73915fd1e` after rolling back, to measure run-to-run noise |
| `results/20261030-1820-dell-gb10-qwen3.6-35b-a3b-nvfp4-fe-config.md` | Dell GB10 | A/B: new image plus the FE's memory 0.55, 16 seqs and priority scheduling: no gain |
| `results/20261030-1916-dell-gb10-qwen3.6-35b-a3b-nvfp4-postreboot.md` | Dell GB10 | first start after a reboot (new kernel 7.0.0-1024): single-stream 81.5 tok/s; a plain vLLM restart brought it back to ~97–101, i.e. start-to-start variation, not the kernel |
| `results/20261030-1929-dell-gb10-ab-mtp-async/` | Dell GB10 | `ab-tuning.sh`: deployed profile vs MTP K=3 vs `--async-scheduling`, 3 fresh vLLM starts each, interleaved: the deployed profile wins or ties |
| `results/20261030-platform-comparison/` | both | read-only box snapshots (`box-snapshot.sh`), a memory-bandwidth probe (`membw.py`, `bandwidth-test.sh`) and the written comparison |

Memory bandwidth on the Dell GB10 (2026-10-30, PyTorch 2.13 in the `…6d5afe` image, 4 GiB buffers, 30 iterations, 3 runs):
device-to-device copy 243.7–246.8 GB/s, read-only reduction 246.1–246.5 GB/s (88–90 % of the ~273 GB/s peak). The FE has not been
measured while idle.

**Single-stream decode varies by up to ~20 % between vLLM starts on identical setups** (81–106 tok/s seen), so compare
variants over several fresh starts (`ab-tuning.sh` does three, interleaved), never one run each.

Result of the A/B series: switching the Dell box to the FE's vLLM image lifted its single-stream decode (post-change check
102.1 tok/s) and 3,846 tok/s for 2k prefill on a cached 8k context. A gap of 16–35 % to the FE remained and is not explained.

llama-benchy 0.4.0. Prefix caching is on, so the `ctx_pp` rows read the context once and the following `pp2048 @ dN` rows
measure prefill on top of a cached context.
