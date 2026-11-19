# Log

## 2026-11-19

- Prepared for public release on GitHub Pages: internal planning material removed, benchmark files relabelled by vendor
  (NVIDIA Founders Edition, Dell Pro Max GB10), "our/work" wording made neutral, the coding-agents guide rewritten around
  public sources only.

## 2026-10-30

- **Platform comparison** (read-only, two boxes): a Dell Pro Max GB10 (Dell BIOS 4.1.0, 2025-10) and an NVIDIA Founders
  Edition (BIOS 2026-06) with otherwise identical software. Dell memory bandwidth ~246 GB/s (88–90 % of peak), so raw
  bandwidth does not explain the gap; open hypotheses are memory latency and CPU-side overhead.
- **Tuning A/B on the Dell box** (3 fresh starts per variant): MTP K=3 worse, `--async-scheduling` neutral. A reboot (new
  kernel) changed nothing once start-to-start variation (up to ~20 % single-stream) is accounted for; no GPU throttling.
- **Image A/B on the Dell box**: the Founders Edition's vLLM image doubled 2k prefill on cached context
  (2,334 → 3,987 at 8k; 1,677 → 3,741 at 32k) and lifted single-stream decode ~13–17 %; 5-stream decode unchanged.
- New trap on the software-support page: a stale NVIDIA CDI spec blocks new GPU containers; an apt hook refreshes it.
- GLM 5.3 Flash DFlash2 drafter licence (CC BY-NC-ND) noted on the model page.
- Registry recipes: all 46 local-ai-registry Spark recipes, 5 lab-measured vs 41 author-reported.
- NVIDIA playbooks overview (51 Spark playbooks); coding agents on local models (gateway, clients, traps).
- ServeTheHome report rebuilt from all 4 pages; per-port bandwidth conflict (~96 vs ~196 Gb/s) stated on the GB10 page.

## 2026-10-29

- Full coverage: stacks (7), clustering (+4), hardware (+4), models (+4 families) and field reports.
- Models × Sparks matrix: 23 Spark recipe rows from the mia-ai.net catalog (snapshot 2026-10-29), cross-checked against
  Capetron's stock-vLLM runs.
- First concepts: GB10 platform, two Sparks over one DAC, Qwen3.8 27B on one Spark.
- Bundle created with five sections (hardware, clustering, stacks, models, field-reports).
