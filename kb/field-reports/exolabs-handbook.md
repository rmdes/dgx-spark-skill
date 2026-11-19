---
type: report
title: "Field report: The DGX Spark Handbook (0xSero, EXO Labs blog)"
description: The most complete community overview of the DGX Spark in 2026 — prices, power, six models with measured speeds, a one-to-four Spark path, and why the Spark is a prefill and research box.
tags: [field-report, self-reported, handbook, power, cost, scaling, models, recipes]
resource: /field-reports/exolabs-handbook.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [DGX Spark Handbook, 0xSero handbook]
entities:
  - label: 0xSero
    kind: person
  - label: EXO Labs
    kind: organization
  - label: MiaAI Lab
    kind: organization
  - label: sparkDash
    kind: tool
  - label: b12x
    kind: library
relations:
  - type: cites
    target: /hardware/power-and-thermals.md
  - type: cites
    target: /hardware/cost-and-bom.md
  - type: cites
    target: /clustering/three-node-ring.md
  - type: cites
    target: /clustering/switched-fabric.md
  - type: cites
    target: /stacks/exl3-exllamav3.md
  - type: cites
    target: /stacks/quantization-formats.md
  - type: cites
    target: /stacks/sparkring-sparkcache.md
  - type: cites
    target: /field-reports/nvidia-agents-on-spark.md
provenance:
  - source: https://huggingface.co/blog/exolabs/the-dgx-spark-handbook
    note: Hugging Face blog post under EXO Labs, author 0xSero, published 2026-09-25. Mixes the author's own measurements, MiaAI Lab recipe READMEs and NVIDIA's published scaling numbers.
citations:
  - id: hb
    text: "0xSero (EXO Labs), The DGX Spark Handbook (2026-09-25). https://huggingface.co/blog/exolabs/the-dgx-spark-handbook"
---

# Overview

**Source type: self-reported, enthusiast owner; mixed provenance.** The author owns four Sparks on a MikroTik
switch and a 4× RTX PRO 6000 rig. Speeds come from his own tests, MiaAI Lab recipe READMEs and NVIDIA's blog;
the handbook says which per number, and so does this page [hb]. It is the broadest single overview available.

| Item | Detail |
|---|---|
| Who | 0xSero, published on the EXO Labs Hugging Face blog |
| Hardware | 4× DGX Spark + 200 GbE MikroTik switch; separate 4× RTX PRO 6000 rig |
| Workloads | Daily assistant and coding models, many agents at once, quantization/pruning research |
| Recommendation | "If I were starting over, I'd buy two on day one" [hb] |

# Cost (as reported, US)

| Item | Value |
|---|---|
| Founders Edition list price | $3,999, raised to $4,699 [hb] |
| Street price, September 2026 | cheapest ~$5,000; used ~$6,000; NVIDIA's site showed $7,999 on 21 September [hb] |
| Cables for two Sparks | NVIDIA 0.4 m $99.99 (often out of stock); Amphenol/Luxshare 0.5 m ~$159–187; NVIDIA MCP1650-V00AE30 ~$84 [hb] |
| Buying advice | Any GB10 OEM box works; get the 4 TB SSD; buy the cable with the second unit [hb] |

See [cost and bill of materials](/hardware/cost-and-bom.md).

# Power

| Setup | Draw | Basis |
|---|---|---|
| 1 Spark idle | 22–25 W | after NVIDIA's February update, Tom's Hardware as cited [hb] |
| 1 Spark serving | 60–90 W (STH); ~95–100 W (author's reading) | [hb] |
| 4 Sparks, one model (GLM-5.2) | ~500 W, ~125 W each | author's measurement [hb] |
| Switch | ~240 W | author [hb] |
| 4× RTX PRO 6000 rig | 1,600 W peak | author [hb] |

The author's monthly costs assume 24/7 draw at 18 US cents/kWh (one Spark ~$12, four Sparks ~$66–100). He notes a B300
moves roughly twice the bytes per joule; the Spark's advantage is running on a normal wall socket [hb]. See
[power and thermals](/hardware/power-and-thermals.md).

# Measured: the six models the author runs

Single user, speculative decoding on unless stated; every speed names its task because code/JSON drafts well and prose does not [hb].

| Model | Sparks | Measured speed (single user) |
|---|---|---|
| Qwen3.6-35B (NVFP4) | 1 | 95 tok/s short prompt; recipe: 317 tok/s total for eight users |
| Qwen3.8-27B (NVFP4) | 1 | 51.5 code, 23 chat, 18 essay |
| Qwen3.8-Flash-Next (NVFP4) | 1–2 | 48.7 prose (1 Spark); 52.1 on 2 Sparks, task not stated |
| GLM-5.3-Flash | 2–4 | 27 prose, 65 JSON (2 Sparks, EXL3 4-bit); 112 JSON with 8K prompt (4 Sparks) |
| DeepSeek-V4.1-Flash | 3–4 | 59 prose, 110 code, 121 JSON (4 Sparks); 47 with a 32K prompt |
| GLM-5.3 | 3–4 | 24 prose, 32 code |

Selected recipe figures quoted in the handbook: GLM-5.3-Flash EXL3 on 2 Sparks 62.9 tok/s single user and 146.5 total
for four, 850K context; DeepSeek-V4.1-Flash native on a 3-Spark ring 51.0 tok/s; on 4 Sparks 45.4 tok/s single and 134.2
total for sixteen, 1M context [hb]. One Spark serves Qwen3.6-35B to up to 8 concurrent sessions at about 40 tok/s each [hb].
See [GLM-5.3 family](/models/glm53-family.md), [DeepSeek V4 family](/models/deepseek-v4-family.md),
[Qwen3.8 Flash Next](/models/qwen38-flash-next.md).

# What worked

- **Two Sparks is the recommended stopping point for most people**; three need no switch (ring); four need a switch
  or an alpha-quality switchless ring stack (SparkRing) [hb]. See [three-node ring](/clustering/three-node-ring.md),
  [switched fabric](/clustering/switched-fabric.md), [SparkRing](/stacks/sparkring-sparkcache.md).
- **Quantization:** NVFP4 is read natively by the GB10; EXL3 allows arbitrary bit widths (GLM-5.3-Flash 176 GB at
  4 bits on two Sparks, 85 GB at 2 bits on one). "4 bits is the sweet spot" [hb]. See
  [quantization formats](/stacks/quantization-formats.md), [EXL3](/stacks/exl3-exllamav3.md).
- **Prefill and research.** Prompt reading runs 13–41× faster than writing on his runs; DeepSeek-V4.1-Flash on four Sparks
  read a 32K prompt at 3,360 tok/s while writing stayed around 70–95 tok/s. He moved pruning, EXL3 quantization and
  benchmarking to the Sparks ("2-3 days vs 12h is fine") [hb].
- **Scaling.** Quotes NVIDIA's test: time per output token 2.0× better on two Sparks, 3.7× on four; prompt reading only
  1.6× and 2.1× [hb]. Primary data in [NVIDIA's scaling blog](/field-reports/nvidia-agents-on-spark.md).

# What did not work

- "Linking Sparks works, but it's where the software is least polished. Follow a tested recipe and set aside an afternoon" [hb].
- sm_121 is its own kernel family; at launch much fast code did not run or ran slowly. Community kernels (b12x, an ExLlamaV3
  Arm fork) closed the gap [hb]. See [software support](/hardware/software-support.md).
- Some models split only by 2 or 4: "check that the recipe says 3x before you buy the third" [hb].
- One unit arrived bent in shipping (still works) [hb].
- "If a model won't start, it's almost always memory… One Spark runs one big model at a time" [hb].

# Caveats on the numbers

- The "546 / 819 / 1,092 GB/s" aggregate bandwidth figures are 273 GB/s multiplied by node count, presented as
  close-to-linear; the measured effect is NVIDIA's TPOT scaling above, not a bandwidth measurement [hb].
- Power: STH's 60–90 W serving figure and the author's ~95–100 W reading differ; both are shown.
- Several speeds are recipe-author numbers, not the handbook author's own.

# Takeaways

- The author's own path (one Spark, then a second plus cable, stop at two for most users) is a sensible growth path;
  his "buy two on day one" is the clearest owner recommendation in the sources.
- One Spark at ~40 tok/s × 8 sessions (Qwen3.6-35B) suggests one unit can carry a small team for a fast MoE model;
  extra units buy larger models (GLM-5.3-Flash, DeepSeek-V4.1-Flash), not more users per model.
- Four Sparks ≈ 500 W on one socket versus 1,600 W for a 4-GPU rig is a strong office-friendliness argument.
- Prices moved from $3,999 to $4,699 list and higher street prices in 2026; re-quote before buying.
