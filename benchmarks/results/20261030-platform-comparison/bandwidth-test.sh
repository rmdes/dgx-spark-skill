#!/usr/bin/env bash
# ABOUTME: One-minute GPU memory-bandwidth test for a GB10 (device-to-device copy + read-only reduction, 3 runs) in a throwaway container.
# ABOUTME: Usage: bash bandwidth-test.sh [GiB per buffer, default 1]. Refuses to run without memory headroom. Saves a result file.
set -euo pipefail
gib="${1:-1}"
# Same image on both Sparks so the comparison is fair (the chat vLLM image both run since 2026-10-30).
image="ghcr.io/spark-arena/dgx-vllm-eugr-nightly@sha256:6d5afe0e7d904b8113512ebefc943d2b50ded6cc770dc65d749eab627adfb6cd"
out="$HOME/bandwidth-$(hostname)-$(date +%Y%m%d-%H%M).txt"

# Unified memory: running short starts earlyoom, which kills the largest inference process (vLLM).
need_gib=$(( gib * 2 + 8 ))   # two buffers + container/CUDA overhead + margin
avail_gib=$(awk '/MemAvailable/ {printf "%d", $2/1048576}' /proc/meminfo)
if (( avail_gib < need_gib )); then
  echo "refusing: ${avail_gib} GiB available, need ${need_gib} GiB for ${gib} GiB buffers. Try a smaller size or a quieter moment." >&2
  exit 1
fi
docker image inspect "$image" >/dev/null 2>&1 || { echo "image not present on this box: $image" >&2; exit 1; }

{
  echo "host $(hostname)  $(date -Is)  buffers ${gib} GiB x2  MemAvailable ${avail_gib} GiB"
  nvidia-smi --query-gpu=utilization.gpu,clocks.sm --format=csv,noheader | sed 's/^/gpu before: /'
  docker run --rm --gpus all -e GIB="$gib" --entrypoint python3 "$image" -c '
import os, time, torch
n = int(os.environ["GIB"]) * (1 << 28)          # float32 elements per GiB = 2**28
a = torch.ones(n, device="cuda"); b = torch.empty_like(a); size = a.numel() * 4
def bw(fn, moved, reps=30):
    fn(); torch.cuda.synchronize(); t = time.perf_counter()
    for _ in range(reps): fn()
    torch.cuda.synchronize(); return moved * reps / (time.perf_counter() - t) / 1e9
for i in range(3):
    copy = bw(lambda: b.copy_(a), 2 * size)      # read + write
    read = bw(lambda: a.sum(), size)             # read only
    print(f"run {i+1}: copy {copy:6.1f} GB/s   read {read:6.1f} GB/s")
print(torch.cuda.get_device_name(0), "torch", torch.__version__)
' 2>&1 | grep -E "^run|torch"
} | tee "$out"
echo "saved to $out"
