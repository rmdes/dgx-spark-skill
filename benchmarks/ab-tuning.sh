#!/usr/bin/env bash
# ABOUTME: A/B of vLLM launch variants on a Dell Pro Max GB10: 3 fresh starts per variant, interleaved, llama-benchy each.
# ABOUTME: Variants live in temporary untracked profiles; an EXIT trap always restores the deployed profile.
set -uo pipefail
# A checkout with models/<profile>/serve.sh, scripts/wait-ready.sh and docker compose (e.g. local-ai).
cd "${STACK_DIR:-$HOME/local-ai}"
P=qwen3.6-35b-a3b-nvfp4
OUT=~/bench/ab-$(date +%Y%m%d-%H%M)
mkdir -p "$OUT"

mk() { rm -rf "models/_ab-$1"; cp -r "models/$P" "models/_ab-$1"; }
mk k3
sed -i 's/"num_speculative_tokens": 2/"num_speculative_tokens": 3/' models/_ab-k3/serve.sh
mk async
sed -i 's/--enable-prefix-caching --enable-chunked-prefill \\/--enable-prefix-caching --enable-chunked-prefill --async-scheduling \\/' models/_ab-async/serve.sh

# Refuse to run if an edit did not apply: a silent no-op variant would look like "no effect".
grep -q '"num_speculative_tokens": 3' models/_ab-k3/serve.sh || { echo "k3 edit failed"; rm -rf models/_ab-*; exit 1; }
grep -q -- '--async-scheduling' models/_ab-async/serve.sh || { echo "async edit failed"; rm -rf models/_ab-*; exit 1; }

restore() {
  docker compose up -d --force-recreate vllm >/dev/null 2>&1
  READY_TIMEOUT=1200 scripts/wait-ready.sh >/dev/null 2>&1 && echo "restored deployed profile" || echo "RESTORE FAILED"
  rm -rf models/_ab-k3 models/_ab-async
  echo "checkout changes: $(git status --short | wc -l)"
}
trap restore EXIT

for r in 1 2 3; do
  for v in base k3 async; do
    prof=$P; [[ $v != base ]] && prof=_ab-$v
    MODEL_PROFILE=$prof docker compose up -d --force-recreate vllm >/dev/null 2>&1
    if ! READY_TIMEOUT=1200 scripts/wait-ready.sh >/dev/null 2>&1; then
      echo "$v r$r FAILED to start"; docker logs --tail 15 spark-vllm 2>&1; continue
    fi
    HF_HUB_OFFLINE=1 ~/.local/bin/uvx llama-benchy --base-url http://127.0.0.1:8000/v1 \
      --model nvidia/Qwen3.6-35B-A3B-NVFP4 --tokenizer nvidia/Qwen3.6-35B-A3B-NVFP4 \
      --pp 2048 --tg 128 --depth 0 32768 --concurrency 1 5 --runs 2 \
      --enable-prefix-caching --latency-mode generation \
      --save-result "$OUT/$v-r$r.md" --format md >/dev/null 2>&1
    echo "done $v r$r $(date +%H:%M)"
  done
done
echo "results in $OUT"
