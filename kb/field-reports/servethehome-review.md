---
type: report
title: "Field report: ServeTheHome DGX Spark review (hardware, networking, performance, power, verdict)"
description: ServeTheHome's four-page launch review of a pre-production DGX Spark — hardware and GB10 details, a ConnectX-7 that measured only ~96 Gb/s in iperf3, untuned Ollama speeds, wall power and noise, and a "game-changer for local AI development" verdict despite 273 GB/s of memory bandwidth.
tags: [field-report, independent-press, hardware, networking, performance, power, noise, review]
resource: /field-reports/servethehome-review.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [STH DGX Spark review, ServeTheHome GB10 review]
entities:
  - label: ServeTheHome
    kind: organization
  - label: DGX Spark
    kind: system
  - label: ConnectX-7
    kind: network_controller
  - label: MikroTik CRS812-8DS-2DQ-2DDQ
    kind: network_switch
  - label: NVIDIA Sync
    kind: tool
  - label: Ollama
    kind: inference_engine
relations:
  - type: cites
    target: /hardware/power-and-thermals.md
  - type: cites
    target: /hardware/gb10-platform.md
  - type: related_to
    target: /clustering/two-node-dac.md
  - type: related_to
    target: /clustering/switched-fabric.md
  - type: related_to
    target: /hardware/software-support.md
provenance:
  - source: https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/
    note: ServeTheHome review, page 1 (intro, hardware overview), 2025-10-14. NVIDIA supplied a pre-production unit.
  - source: https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/2/
    note: Page 2 (GB10 SoC, ConnectX-7, RoCE, MikroTik switch, iperf3), 2025-10-14. Several results are only in screenshots; only the article text was collected.
  - source: https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/3/
    note: Page 3 (topology, software, performance, Geekbench, teething challenges), 2025-10-14.
  - source: https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/4/
    note: Page 4 (power, lessons learned, final words), 2025-10-14.
  - source: https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-dgx-spark-update-cuts-idle-power-by-32-percent-or-more-hot-plug-detection-on-connectx-nic-makes-for-a-more-efficient-ai-workstation
    note: Tom's Hardware, 2026-02-12, on the later idle-power update (clip partial).
citations:
  - id: sth1
    text: "ServeTheHome, NVIDIA DGX Spark Review: The GB10 Machine is so Freaking Cool, page 1 (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/"
  - id: sth2
    text: "ServeTheHome, NVIDIA DGX Spark Review: The GB10 Machine is so Freaking Cool, page 2 (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/2/"
  - id: sth3
    text: "ServeTheHome, NVIDIA DGX Spark Review: The GB10 Machine is so Freaking Cool, page 3 (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/3/"
  - id: sth
    text: "ServeTheHome, NVIDIA DGX Spark Review: The GB10 Machine is so Freaking Cool, page 4 (2025-10-14). https://www.servethehome.com/nvidia-dgx-spark-review-the-gb10-machine-is-so-freaking-cool/4/"
  - id: toms
    text: "Tom's Hardware, Nvidia DGX Spark update cuts idle power by 32% or more (2026-02-12). https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-dgx-spark-update-cuts-idle-power-by-32-percent-or-more-hot-plug-detection-on-connectx-nic-makes-for-a-more-efficient-ai-workstation"
---

# Overview

**Source type: independent hardware press, vendor-supplied hardware.** NVIDIA sent ServeTheHome a
**pre-production** unit; the reviewer had also pre-ordered two units with the copper DAC bundle, which had not
arrived at publication [sth1]. The review was written within days of receiving the box ("less than a week") and
dates from launch, October 2025 [sth1] [sth]. Read it as a launch baseline: firmware, drivers and the NIC
behaviour have changed since (see Conflicts below). Several results (Geekbench, the four-way iperf3 run, RoCE
output) appear only in screenshots; our collected copy has the article text only, so those numbers are
"not published" here.

# Hardware

| Item | As reported | Source |
|---|---|---|
| Size | 150 × 150 × 50.5 mm | [sth1] |
| Chassis | Hard porous front for airflow, large bottom vent and rubber pad, gold metal sides | [sth1] |
| Rear I/O | Power button, USB-C power (USB-PD) input, 3× USB-C 20 Gbps with DisplayPort alt mode, HDMI | [sth1] |
| Networking | Realtek 10GbE (10GBASE-T, driver included in DGX OS), ConnectX-7 with 2× 200GbE ports (described as QSFP56, 4 × 50 Gbps PAM4), MediaTek Wi-Fi 7 | [sth1] [sth2] |
| Storage (review unit) | 4 TB NVMe SSD | [sth3] |
| Power adapter | 240 W USB-PD | [sth] |

# GB10

| Item | As reported | Source |
|---|---|---|
| CPU | 20 Arm cores: 10 Cortex-X925 + 10 Cortex-A725; Arm side is MediaTek IP | [sth2] [sth3] |
| GPU | Blackwell, 48 compute units in the topology map; ~1 PFLOP sparse FP4, "roughly the same" as a GeForce RTX 5070 | [sth3] |
| CPU–GPU link | C2C NVLink | [sth2] |
| Memory | 128 GB LPDDR5X unified (one pool, no fixed CPU/GPU split as on AMD Strix Halo); DGX Dashboard shows 120 GB | [sth2] [sth3] |
| Memory bandwidth | 273 GB/s | [sth] |
| GPU L2 cache | 24 MB; 600 GB/s aggregate bandwidth (more than twice the LPDDR5X figure) | [sth2] |
| SoC TDP | 140 W (SoC, not system power) | [sth2] |
| Process / packaging | TSMC 3 nm, 2.5D packaging | [sth2] |

# Networking and topology

- **ConnectX-7 is a large part of the value.** STH compares it to the 2-port 200GbE ConnectX-7 OCP NIC 3.0 card,
  which sells used for "$900+" [sth2]. RDMA/RoCE between two Sparks was shown working [sth2].
- **PCIe link.** STH saw "only a 32GT/s PCIe x4 link" on the ConnectX-7. iperf3 across both ports gave the same
  **~96 Gb/s** as one port; a four-way bound iperf3 run (the NIC shows up as four devices), over DACs and through a
  switch, is shown only in a screenshot whose caption reads "getting 100Gbps only" [sth2].
- **Switch.** The same RoCE output worked through a MikroTik CRS812 DDQ (QSFP56-DD ports split to 2× 200GbE).
  A direct DAC auto-negotiated 200GbE; the switch needed port speed set to 200 Gb/s manually [sth2].
  See [switched fabric](/clustering/switched-fabric.md).

# Software

- DGX OS (Ubuntu-based, NVIDIA drivers and tools built in) and the DGX Dashboard. Setup works locally or over
  Wi-Fi, with the Spark acting as an access point [sth3].
- **NVIDIA Sync** manages SSH tunnels so web UIs on the Spark appear on `localhost` of the laptop; with
  Tailscale added the reviewer used the unit headless from ~1000 km away and called the combination "an
  absolute winner" [sth3]. Cursor, VS Code and NVIDIA AI Workbench integrations were offered out of the box [sth3].
- NVIDIA ships tutorials (LLMs, image generation, fine-tuning, RAG) with the system [sth3].

# Measured

**Inference (untuned, out-of-the-box Ollama via Open WebUI, single user)** [sth3]:

| Model | Decode speed |
|---|---|
| gpt-oss 20B | often over 49 tok/s |
| gpt-oss 120B | 14.48 tok/s |
| Qwen3 32B | 9–10 tok/s |

STH says more benchmarks would follow; none are on these pages. Geekbench 5 CPU comparisons against AMD Strix
Halo systems are screenshots only (scores not published in the text); STH calls the CPU "actually quite quick"
and "probably the best Arm-Ubuntu mini PC right now" [sth3].

**Power and noise** [sth]:

| Condition | Power at the wall | Source |
|---|---|---|
| Idle (launch firmware) | 40–45 W | [sth] |
| CPU load only | 120–130 W | [sth] |
| CPU + GPU + other components | just under 200 W; never reached 240 W | [sth] |
| Typical LLM inference | 60–90 W | [sth] |
| GPU idle in `nvidia-smi` | dropped from 13 W to 4 W after an update | [sth3] |
| Noise | fan hard to hear at 1–1.5 m; never hit 40 dBA outside stress tests | [sth] |

Later data: Tom's Hardware measured about 37 W at idle and reported (2026-02-12) an update that cuts idle power
by 32% or more via hot-plug detection on the ConnectX NIC [toms]. STH also notes QSFP56 optics "can use a decent
amount of power" [sth]. See [power and thermals](/hardware/power-and-thermals.md).

# What worked

- 128 GB of unified memory lets one small box run larger, more accurate models on data that cannot go to a cloud
  provider, and hold several models at once [sth] [sth3].
- 200 GbE RDMA networking for clustering instead of improvised Thunderbolt links [sth].
- Remote use via NVIDIA Sync + Tailscale [sth3].
- Small enough for carry-on luggage; "the best, albeit not cheap, Arm desktop/mini PC on the market by a long-shot" [sth].

# What did not work

- **273 GB/s memory bandwidth.** "I would love it if they had double the memory bandwidth"; it makes the device "more
  of a prototyping machine" compared with an RTX Pro 6000 Blackwell, which scaled out is "much faster" [sth].
- **Display output.** 1440p over HDMI gave a garbled picture on LG OLEDs and ultrawide monitors did not work; a 4K
  display at 60 Hz did [sth3].
- **Maturity.** Behaviour changed between updates on the early sample; "not the most mature NVIDIA platform" in its
  just-released state; that it "probably gets better over time" involves "a bit of faith" [sth3] [sth].
- **NIC throughput** measured at ~96 Gb/s, not 200 Gb/s, at launch [sth2] (see Conflicts).

# Verdict

"If I had the opportunity to buy another, I would do it immediately." A "game-changer for local AI development" that
provides "a new capability that did not exist with PCIe GPUs" [sth]. STH expects it to "democratize being able to run
large local models", calls it a must-have "(maybe more than one)" for many AI developers, and something "dangerously
close" to a recommendation for every executive tasked with bringing AI into an organisation [sth] [sth1].

# Conflicts with other concepts

- **ConnectX-7 bandwidth.** STH (launch, pre-production unit, iperf3/TCP) saw one PCIe Gen5 x4 link and ~96 Gb/s total
  across both ports [sth2]. [GB10 platform](/hardware/gb10-platform.md) states, from NVIDIA's later documentation and
  Capetron, that the NIC uses **two** independent Gen5 x4 links (each port appears as two interfaces) and that both
  halves together reach ~200 Gb/s; [Two Sparks over one DAC](/clustering/two-node-dac.md) reports 196 Gb/s in an RDMA
  test. Likely explanations — STH testing only one half of each port, TCP limits, or early firmware — are not stated in
  either source. Treat the 200 Gb/s figure as dependent on using both halves and RDMA, and verify it on your own pair.
- **Port/cable naming.** STH describes the ports as 200GbE QSFP56 (4 × 50G PAM4) [sth1]; GB10 platform lists the
  approved cables as QSFP112 DACs rated 400G, negotiated at 200G. Both agree on 200 Gb/s per port; only the
  form-factor label differs.
- Power figures match [power and thermals](/hardware/power-and-thermals.md); no conflict.

# Takeaways

- 60–90 W during LLM inference and a fan under 40 dBA [sth] mean a few Sparks can sit in an office or rack without
  special power or cooling planning.
- STH frames it as a prototyping/development box, not a maximum-throughput server [sth]. That fits "daily local-AI
  development" better than "production inference for a whole organisation".
- The NVIDIA Sync + Tailscale pattern [sth3] means the box can run
  headless and be reached from a laptop.
- Untuned Ollama speeds (gpt-oss 120B at 14.48 tok/s, Qwen3 32B at 9–10 tok/s) [sth3] are a launch-day floor, not
  what a tuned stack does today; compare with [GB10 platform](/hardware/gb10-platform.md) and the bandwidth-bound
  decode argument there when explaining why MoE models are the right choice.
- The launch-day ~96 Gb/s iperf3 result [sth2] is why the demo should show an RDMA bandwidth test on both halves of
  the DAC link, as in [Two Sparks over one DAC](/clustering/two-node-dac.md), rather than claim 200 Gb/s from the spec.
