# Hardware

GB10 platform: specs, memory, networking (ConnectX-7), power, sm121 software support.

<!-- okf:generated:index begin -->
# hardware

* [GB10 platform (DGX Spark and OEM twins)](/hardware/gb10-platform.md) - What every GB10 workstation is — 128 GB unified memory at 273 GB/s, a 20-core Arm CPU, and a ConnectX-7 NIC with two 200 Gb/s QSFP ports.
* [Power and thermals](/hardware/power-and-thermals.md) - What a GB10 draws idle, serving and flat out, what the January 2026 update changed at idle, how hot and loud it runs, and what 24/7 operation needs (no BMC on GB10 units).
* [Software support on sm_121](/hardware/software-support.md) - Where the GB10 software stack stands — sm_121 gaps in PyTorch, vLLM, FlashInfer and friends, what each DGX OS release fixed, and the honest "early days" assessment.
* [Unified memory limits](/hardware/unified-memory-limits.md) - How much of the 128 GB a model really gets on a GB10, how weights, KV cache and the runtime share it, why running out freezes the host, and the sizing and guard rules that keep a Spark up.

# reference

* [Cost and bill of materials](/hardware/cost-and-bom.md) - Dated unit prices for DGX Spark and its OEM twins in the EU and US, the cable, breakout and switch prices, and the parts list for 2-, 3- and 4-node builds.
<!-- okf:generated:index end -->
