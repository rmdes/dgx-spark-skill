---
type: hardware
title: Power and thermals
description: What a GB10 draws idle, serving and flat out, what the January 2026 update changed at idle, how hot and loud it runs, and what 24/7 operation needs (no BMC on GB10 units).
tags: [gb10, dgx-spark, power, thermals, operations]
resource: /hardware/power-and-thermals.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [power draw, idle power, TDP, noise, 24/7 operation]
entities:
  - label: 240 W USB-PD power supply
    kind: power_supply
  - label: NVIDIA GB10
    kind: system_on_chip
relations:
  - type: describes
    target: /hardware/gb10-platform.md
  - type: related_to
    target: /hardware/unified-memory-limits.md
  - type: related_to
    target: /hardware/cost-and-bom.md
  - type: monitored_by
    target: /clustering/cluster-tooling.md
  - type: related_to
    target: /field-reports/servethehome-review.md
  - type: related_to
    target: /field-reports/exolabs-handbook.md
provenance:
  - source: https://docs.nvidia.com/dgx/dgx-spark/hardware.html
    note: NVIDIA Hardware Overview — PSU, TDP, operating environment.
  - source: https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/4/
    note: ServeTheHome review power page (2025-10-14), wall measurements at launch.
  - source: https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-dgx-spark-update-cuts-idle-power-by-32-percent-or-more-hot-plug-detection-on-connectx-nic-makes-for-a-more-efficient-ai-workstation
    note: Tom's Hardware (2026-02-12) on the ConnectX hot-plug idle-power update; our clip is truncated after the pre-update figure.
  - source: https://huggingface.co/blog/exolabs/the-dgx-spark-handbook
    note: EXO Labs DGX Spark Handbook (2026-09-25) — post-update idle figure and 4-node draw.
  - source: https://docs.nvidia.com/dgx/dgx-spark/release-notes.html
    note: Release notes — January 2026 CX-7 hot plug, October 2026 headless fan fix.
citations:
  - id: nv-hw
    text: "NVIDIA, DGX Spark User Guide — Hardware Overview. https://docs.nvidia.com/dgx/dgx-spark/hardware.html"
  - id: nv-rn
    text: "NVIDIA, DGX Spark Release Notes. https://docs.nvidia.com/dgx/dgx-spark/release-notes.html"
  - id: sth
    text: "ServeTheHome, NVIDIA DGX Spark Review — power consumption (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/4/"
  - id: toms
    text: "Tom's Hardware, Nvidia DGX Spark update cuts idle power by 32% or more (2026-02-12). https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-dgx-spark-update-cuts-idle-power-by-32-percent-or-more-hot-plug-detection-on-connectx-nic-makes-for-a-more-efficient-ai-workstation"
  - id: exo
    text: "EXO Labs (0xSero), The DGX Spark Handbook (2026-09-25). https://huggingface.co/blog/exolabs/the-dgx-spark-handbook"
  - id: exxact
    text: "Exxact, What You Need to Build a 4x NVIDIA DGX Spark Cluster. https://www.exxactcorp.com/blog/deep-learning/what-you-need-to-build-a-4x-nvidia-dgx-spark-cluster-switch-cabling-power"
  - id: ae-switches
    text: "Alex Ellis / MiaAI-Lab, Switched alternatives (2026-08-31). https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/switches.md"
  - id: ae-blog
    text: "Alex Ellis, How and Why We Bought 4x DGX Sparks (2026-09-15). https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/"
  - id: cape-hw
    text: "Capetron, GB10 cluster guide — 01 Hardware (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/01-hardware.md"
  - id: cape-bom
    text: "Capetron, GB10 cluster guide — 06 Bill of materials (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/06-bill-of-materials.md"
  - id: sparkdash
    text: "MiaAI-Lab, sparkDash README. https://github.com/MiaAI-Lab/sparkDash/blob/d229bff50120f475274c28d4faf223fdbb56795a/README.md"
---

# Overview

A GB10 is a desk-side machine with a laptop-class power envelope: a **240 W external supply**, of which
the GB10 SoC's TDP is **140 W** and about 100 W is left for the ConnectX-7, Wi-Fi, SSD and USB-C [nv-hw].
In practice it serves models at well under 100 W and idles in the low tens of watts since the
January 2026 update. The operational gap for 24/7 use is not power but **remote recovery**: GB10
units have no BMC [cape-bom].

# Specification

| Item | Value | Source |
|---|---|---|
| Power supply | 240 W external, included, USB-PD; required — another or lower-rated supply may cause reduced performance, failure to boot or shutdowns | [nv-hw] [sth] |
| GB10 SoC TDP | 140 W | [nv-hw] |
| Operating temperature | 5–30 °C | [nv-hw] |
| Operating humidity | 10–90 % non-condensing | [nv-hw] |

# Measured draw (one unit)

| State | Draw | When / who | Source |
|---|---|---|---|
| Idle, at launch | 40–45 W | ServeTheHome, October 2025 | [sth] |
| Idle, before the update | ~37 W | Tom's Hardware | [toms] |
| Idle, after the update | 22–25 W | EXO Labs Handbook, citing Tom's Hardware (secondary) | [exo] |
| LLM inference, typical | 60–90 W, "very quiet" | ServeTheHome | [sth] |
| Serving a model | ~100 W | EXO Labs author's own reading | [exo] |
| CPU load only | 120–130 W | ServeTheHome | [sth] |
| CPU + GPU + other components | just under 200 W; never reached 240 W | ServeTheHome | [sth] |

All figures are third-party wall readings; none are NVIDIA specifications.

**The idle update.** NVIDIA's January 2026 release added ConnectX-7 hot-plug support, "saving up to
18 W of power when the adapter is not in use" [nv-rn]. Tom's Hardware headlined it as an idle cut of
32 % or more [toms]. The saving is for an unused adapter; NVIDIA does not state what a clustered
node, whose adapter is in use, saves.

# Clusters

| Setup | Draw | Source |
|---|---|---|
| 4 Sparks running one model (GLM-5.2) | ~500 W total, ~125 W per Spark | EXO Labs author's reading [exo] |
| MikroTik CRS804 switch | ~92 W typical, ~123 W under load | [exxact] |
| MikroTik CRS812 switch | 134 W max; ServeTheHome measured ~130–140 W with optics | [ae-switches] |
| 4 Sparks + CRS804, upper bound | "shouldn't exceed 1200 W" | [exxact] |

Per-Spark draw rises when a model is split across nodes because every Spark works on every token and
keeps its link busy [exo]. Four Sparks fit on one ordinary outlet circuit [exxact] [exo].

# Thermals and noise

- At 1–1.5 m the fan is "very difficult to hear" and stayed under 40 dBA outside stress tests [sth].
  Alex Ellis describes the Founders Edition as "extremely quiet whilst serving" [ae-blog].
- All GB10 units share the chip and a software power cap, so raw performance is essentially equal;
  the differences between OEM boxes are cooling and sustained-load behaviour [cape-bom]. The EXO
  Labs author reports units run cooler stood on their side with space around the mesh, and that some
  OEMs offer better airflow [exo].
- The switch, not the Sparks, is the noisy part of a cluster: the CRS812 is "loud with optics —
  rack it" [ae-switches].

# 24/7 operation

- **No BMC.** Capetron notes the MSI EdgeXpert has no BMC, so a physical power button is the only
  fallback [cape-hw], and recommends a **smart PDU** for anyone racking GB10 units remotely because a
  wedged unit needs a physical or PDU power cycle [cape-bom].
- **No Wake-on-LAN.** A DGX Spark does not wake from a magic packet [sparkdash].
- The usual cause of a wedged unit is running out of unified memory, not heat; see
  [unified memory limits](/hardware/unified-memory-limits.md).
- **Headless fan bug, fixed.** The October 2026 release fixed fans that stopped responding in headless
  (appliance) mode at low idle power draw [nv-rn] — update any unit that runs unattended.
- Optional power control: sparkDash can cap the GPU clock (`nvidia-smi -lgc`) per unit or fleet-wide,
  and tracks fleet energy [sparkdash].

# Limitations

- No NVIDIA-published idle or typical-load figure; everything above is third-party measurement.
- Our copy of the Tom's Hardware article is truncated after the ~37 W pre-update figure; the post-update
  number comes from the EXO Labs Handbook citing it.
- No source in our set measured sustained thermal throttling on a GB10.
