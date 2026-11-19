#!/usr/bin/env bash
# ABOUTME: Read-only snapshot of a DGX Spark (kernel, DGX OS, GPU, memory, containers, vLLM queue) for comparing two Sparks.
# ABOUTME: Queries only: no restarts, no load, no secrets read. Run on the box: bash box-snapshot.sh
set -u
out="${1:-$HOME/spark-snapshot-$(hostname)-$(date +%Y%m%d-%H%M).txt}"
{
  echo "== host";            hostname; uptime
  echo "== kernel";          uname -r
  echo "== dgx os";          grep -E "SWBUILD_VERSION|OTA_VERSION|OTA_DATE" /etc/dgx-release 2>/dev/null || echo "no /etc/dgx-release"
  echo "== gpu";             nvidia-smi --query-gpu=name,driver_version,vbios_version,pstate,temperature.gpu,power.draw,clocks.sm,clocks.max.sm,utilization.gpu,clocks_event_reasons.active --format=csv 2>&1
  echo "== nvidia modules";  echo "loaded: $(lsmod | grep -c '^nvidia')"
  echo "package for the running kernel:"; dpkg -l "linux-modules-nvidia-*-$(uname -r)" 2>/dev/null | awk '/^ii/ {print "  " $2, $3}' || true
  echo "driver package:"; dpkg -l 2>/dev/null | awk '/^ii/ && $2 ~ /^nvidia-driver/ {print "  " $2, $3}'
  echo "== memory";          free -g
  echo "== containers";      docker ps --format "{{.Names}}  {{.Image}}  {{.Status}}" 2>&1 | grep -iE "vllm|litellm|ollama|embed|rerank" || echo "none matched (or no docker access)"
  echo "== vllm images";     docker ps --format "{{.Names}} {{.Image}}" 2>/dev/null | grep -i vllm | while read -r n _; do docker inspect "$n" --format "$n {{.Config.Image}}" 2>/dev/null; done
  echo "== ollama";          ollama ps 2>&1 | head -6
  echo "== vllm queue";      curl -s -m 5 127.0.0.1:8000/metrics | grep -E '^vllm:num_requests_(running|waiting)\{' | sed 's/{[^}]*}//' | grep . || echo "no vllm metrics on :8000"
} 2>&1 | tee "$out"
echo; echo "saved to $out"
