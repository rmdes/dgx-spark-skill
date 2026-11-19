---
type: index
okf_version: "0.1"
title: DGX Spark knowledge base
description: A community knowledge base on running and clustering NVIDIA DGX Spark (GB10) for fully local AI work, with 1, 2 or more Sparks.
tags: [dgx-spark, gb10, local-ai]
timestamp: "2026-11-19T00:00:00Z"
---

# DGX Spark knowledge base

What is known about running NVIDIA DGX Spark (GB10) workstations, alone and clustered over QSFP112 400G direct-attach
cables, for day-to-day development with local models. It is meant to help you tune your own local AI setup on one, two or
more Sparks.

Every claim cites its original source; the collected sources are listed in
[`sources.txt`](https://github.com/rmdes/dgx-spark-skill/blob/main/sources.txt). Figures marked *self-measured* come
from the author's own boxes (raw results in
[`benchmarks/`](https://github.com/rmdes/dgx-spark-skill/tree/main/benchmarks)); everything else is reported by the
cited source and has not been reproduced here.

**Start here:** the [Models × Sparks matrix](/models/spark-matrix.md) lists every published Spark recipe, how many Sparks
it needs and how fast it runs, and [coding agents on local models](/stacks/coding-agents-on-local-models.md) covers the
gateway pattern that makes a local stack usable by a team.

| Section | Question it answers |
|---|---|
| [Hardware](/hardware/index.md) | What is a GB10 box, what does it draw, where are the software gaps? |
| [Clustering](/clustering/index.md) | How do I wire and validate 2, 3 or 4 Sparks? |
| [Serving stacks](/stacks/index.md) | vLLM, SGLang, TensorFold, EXL3, sparkring: which one for what? |
| [Models](/models/index.md) | Which model needs how many Sparks, at what speed, with which recipe? |
| [Field reports](/field-reports/index.md) | Who already does daily development on local AI rigs, and how did it go? |

Numbers in this knowledge base are snapshots from autumn 2026; recipes and prices move fast, so check the date on each
page. Corrections and additions are welcome (see the repository's contributing notes).
