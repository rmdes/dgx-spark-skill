# NVIDIA FE vs Dell: box-level comparison (2026-10-30, read-only)

Done read-only with an AI assistant. Nothing was restarted, loaded or
changed on either box; no `.env` or key file was read. Raw data next to this file:

- `nvidia-fe-snapshot-20261030-2112.txt`: `box-snapshot.sh` run on the NVIDIA FE (vLLM was serving 3 requests at the time).
- `dell-gb10-baseline-20261030-2104.txt`: the Dell baseline.
- `box-extras-both-20261030-2115.txt`: an identical extra read-only probe on both boxes (DMI/BIOS, kernel cmdline, CPU governor,
  THP/vm, GPU clock/power counters, GPU processes, background CPU, container limits, vLLM entrypoint, env *names* only).

## 1. Side by side

**Different** (most likely relevant first):

| Item | NVIDIA FE (`nvidia-fe`) | Dell (`dell-gb10`) |
|---|---|---|
| **Machine** | **NVIDIA DGX Spark** (Founders Edition), board `P4242` | **Dell Pro Max with GB10 FCM1253**, board `038RY7` |
| **BIOS / UEFI** | `5.36_0ACUM027`, **2026-06-12**; UEFI device fw `0x02009b0b` | `5.36_4.1.0`, **2025-10-08**; UEFI device fw `4.1.0` (Dell) |
| **Embedded controller** | `0x03000508` | `0x02000c00` |
| SM clock under load | **2,496 MHz** (one sample, 95 % util, 3 requests) | ~2,390 MHz (benchmark load) |
| SW power-cap counter since boot | 24.2 s in 11 d 4 h (≈ 0.09 s/h) | 1.0 s in 2 h 14 m (≈ 0.45 s/h) |
| Kernel | `7.0.0-1019-nvidia` (modules `1019.19~24.04.2+2`) | `7.0.0-1024-nvidia` (A/B already ruled out in earlier A/B runs) |
| DGX OS OTA history | 7.6.0 (2026-10-19) | 7.5.0 then 7.6.0 (2026-09-23) |
| Embed/rerank vLLM image | `…6d5afe` (same as chat) | `…7bb73915` |
| Chat vLLM GPU memory | 70.7 GB (0.55, ruled out in earlier A/B runs) | 46.3 GB (0.40) |
| Embed/rerank GPU memory | 5.6 + 5.5 GB | 1.6 + 1.6 GB |
| RAM used / swap used | 96 GB / 10 GB | 70 GB / 0 GB |
| vm.swappiness | 60 | 15 |
| Background load | **heavier**: desktop session (Vivaldi, Waveterm, `dtop` ~49 % of a core), Hermes, OpenClaw, Open WebUI, SearXNG | lighter: promtail, exporters, RustDesk, mysqld, all ~1 % |
| Containers | 11 | 9 |
| **Memory (DMI)** | LPDDR5X **Micron** 128 GB, 8,533 MT/s (read with sudo) | LPDDR5X **SK Hynix** 128 GB, 8,533 MT/s |
| NVMe | Samsung `MZALC4T0HBL1` 4 TB | SK hynix PVC10 1 TB |

**Identical**: driver `580.178.04` (`nvidia-driver-580-open`), VBIOS `9A.0B.2D.00.00`, GPU firmware component `0x00000516`,
DGX SW build 7.2.3 / OTA 7.6.0, chat vLLM image `…6d5afe`, CUDA 13.0.2 / NCCL 2.28.3 in the image, kernel cmdline (apart
from the kernel version), CPU governor `performance` on all 20 cores with the same max frequencies (2.808 / 3.9 GHz),
THP `madvise`, vLLM container limits (no cpuset/CPU quota, ipc=host, shm 64 MB, memlock unlimited, same seccomp profile),
vLLM entrypoint `/serve.sh`, no clock-event reason active on either GPU, Ollama empty/absent on both.

## 2. Hypothesis (unconfirmed)

**The gap is the platform, not the software: a Dell Pro Max GB10 on Dell's year-old BIOS 4.1.0 against an NVIDIA DGX Spark on
a June 2026 NVIDIA BIOS.** Same SoC, but a different board, cooling, embedded controller and firmware, which set how the shared
power budget and the memory subsystem are clocked, and a **different DRAM vendor** (Micron vs SK Hynix) at the same rated
8,533 MT/s. Same speed grade does not mean the same timings/latency: each BIOS trains its own parts, so the memory path is
the prime suspect.

Why this fits:
- Everything software-side that could matter is now identical or already ruled out by A/B on the Dell box (image, driver,
  VBIOS, DGX OS, kernel, vLLM flags), and the FE box is faster despite carrying **more** background load and memory pressure.
- The gap **grows with context**: single stream +16 % (116.5 vs 100.2), at 32k +35 % (104.8 vs 77.6). Long-context decode is
  dominated by KV-cache reads, i.e. memory bandwidth/latency. A pure SM-clock difference (~4 %: 2,496 vs ~2,390 MHz) cannot
  explain 35 %; a slower memory path or a stricter power policy can.
- The Dell box hits the software power cap ~5× as often per hour (both are small; counters reset at boot, so the comparison is
  rough).

What would make it wrong: equal memory bandwidth on both boxes in a synthetic test (then look at CPU-side scheduling
latency instead, and at the start-to-start spread (up to ~20 %, see `benchmarks/README.md`).

## 3. Cheapest tests, in order

1. **Free, now:** check Dell's support page for the Pro Max with GB10 (FCM1253) for a BIOS newer than 4.1.0 and read its
   release notes for performance, memory or power items. Also look in the Dell BIOS setup for a thermal/power mode
   (needs a reboot: Dell box only, after checking the box is idle).
2. **Cheap, about 1 minute per box:** a synthetic GPU memory-bandwidth test with no vLLM involved. For example, a 20-second
   device-to-device copy loop in PyTorch inside the existing vLLM image (`docker run --rm --gpus all <image …6d5afe> python -c …`),
   or `nvbandwidth`. Run it on the Dell whenever its gateway is idle; on the NVIDIA FE **only when the owner says it is
   free**. A ~15–30 % lower bandwidth on the Dell confirms the hypothesis; equal numbers refute it.
3. Only if 2 shows a gap and Dell has nothing newer: ask Dell/NVIDIA whether the Pro Max GB10 runs a different memory or
   power profile than the Founders Edition.

Before 2, align the small software differences so the test is clean: embed/rerank image (`…6d5afe` on both) and, on the FE
box, no desktop session load during the run.

## Notes

- The NVIDIA FE's numbers (116.5 etc.) come from one or two vLLM starts; the ~20 % start-to-start spread still
  applies. Several fresh starts on the FE are still to be run.

## 4. Result: memory bandwidth on the Dell (2026-10-30 21:2x)

Run with `membw.py` (this folder) inside the deployed chat vLLM image, with the gateway idle (0 calls in 5 min, vLLM 0 running /
0 waiting), ~20 s, 2 GiB of buffers, nothing restarted:
`docker run --rm -i --gpus all --entrypoint python3 <spark-vllm image> - < membw.py`

| Pattern (1 GiB, 30 rounds) | Median | Best |
|---|---|---|
| copy (read + write) | 246.0 GB/s | 250.9 GB/s |
| read (`sum`) | 239.8 GB/s | 241.9 GB/s |
| write (`fill`) | 198.4 GB/s | 198.9 GB/s |

GPU at 2,405 MHz, 38 → 39 °C, no throttling. Theoretical peak for 256-bit LPDDR5X at 8,533 MT/s ≈ 273 GB/s, so the Dell
already streams at **88–90 % of peak**.

**What this does to the hypothesis:** raw streaming bandwidth can't be the main cause. Even a NVIDIA FE at the theoretical
273 GB/s would be only ~14 % above 240, far short of the 35 % gap at 32k context. The platform difference, if it is the cause,
must be in **access latency / random-access behavior** (paged KV-cache reads at long context: DRAM timings by vendor and BIOS
training, page-table/TLB and cache behavior) or on the **CPU side** (per-token scheduling overhead), not in throughput.

**Next cheapest tests:**
1. The same `membw.py` on the NVIDIA FE when the box is free (pins down how much the FE box gains from bandwidth
   at all; expected: within a few %).
2. A random-access / pointer-chase GPU test (latency-bound, 4–64 KB blocks at random offsets, like paged KV reads) on both.
   A clear gap there would support the platform hypothesis in its latency form.
3. CPU side: vLLM's per-step overhead (time between decode steps at 1 stream, from the vLLM metrics or a `py-spy dump`
   during a short benchmark) on both boxes.

## 5. NVIDIA FE under live production load (live production load)

`docker exec -i vllm python3 - < membw.py` (a new container could not start, see below). vLLM was decoding 2–3
requests at 95 % GPU, 2,496 MHz, 61 °C throughout; it stayed healthy and kept serving.

| Pattern (1 GiB, 30 rounds) | Median | Best |
|---|---|---|
| copy (read + write) | 106.8 GB/s | 131.8 GB/s |
| read (`sum`) | 111.2 GB/s | 147.5 GB/s |
| write (`fill`) | 101.4 GB/s | 135.9 GB/s |

**Not comparable with section 4**: this is the bandwidth *left over* while vLLM decodes on the same memory, not the box's
capacity. Fair comparison: rerun on the NVIDIA FE during a ~20 s idle window (0 running/0 waiting).

## 6. Side finding: NVIDIA FE can't start new GPU containers (stale CDI spec)

`docker run --gpus all …` on the NVIDIA FE fails: `failed to fulfil mount request: open
/usr/lib/aarch64-linux-gnu/libnvidia-egl-wayland.so.1.1.21: no such file or directory` (also with
`NVIDIA_DRIVER_CAPABILITIES=compute,utility`).

- `/var/run/cdi/nvidia.yaml` was generated 2026-10-19 and still lists egl-wayland **1.1.21**; dpkg upgraded
  `libnvidia-egl-wayland1` to **1.1.23** on 2026-10-23. `nvidia-cdi-refresh.path` only fires on driver/toolkit events, so the
  spec was never refreshed.
- Running containers are unaffected (their mounts date from their start), but **the next start of `vllm` (make up,
  reboot, crash restart) would fail the same way**.
- Fix (root, doesn't touch running containers): `sudo systemctl start nvidia-cdi-refresh.service` (or
  `sudo nvidia-ctk cdi generate --output=/var/run/cdi/nvidia.yaml`), then check with a throwaway
  `docker run --rm --gpus all <image> nvidia-smi -L`. Worth checking the Dell's spec after its next driver-adjacent
  update too (it works today).
- **Fixed 2026-10-30 21:26** (the owner, `sudo systemctl start nvidia-cdi-refresh.service`): spec regenerated, 2 refs to
  1.1.23, 0 to 1.1.21; a throwaway `docker run --rm --gpus all <vllm image> nvidia-smi -L` sees the GB10; running stack untouched.
- **It will come back** at the next library update outside the driver/toolkit (the refresh unit doesn't watch those). Lasting fix
  for the stack: an apt hook, e.g. `/etc/apt/apt.conf.d/99-nvidia-cdi-refresh` with
  `DPkg::Post-Invoke { "systemctl start nvidia-cdi-refresh.service || true"; };`, so every dpkg run refreshes the spec.
- **Hook installed 2026-10-30 21:28** (by hand on the box): `/etc/apt/apt.conf.d/99-nvidia-cdi-refresh`, root-owned,
  644; `apt-config dump` shows `DPkg::Post-Invoke:: "systemctl start nvidia-cdi-refresh.service || true"`. Every dpkg run now
  refreshes the CDI spec. Rollback: `sudo rm /etc/apt/apt.conf.d/99-nvidia-cdi-refresh`.
