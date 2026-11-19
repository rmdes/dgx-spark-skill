# Clustering

Wiring, configuring and validating multi-Spark clusters: 2-node DAC, 3-node, switched fabric.

<!-- okf:generated:index begin -->
# reference

* [Cluster tooling for GB10](/clustering/cluster-tooling.md) - The tools that set up, check and watch a multi-Spark cluster — NVIDIA Sync Cluster Assistant and discover-sparks, the read-only gb10-cluster-check, sparkrun, and the sparkDash dashboard.
* [NCCL over RoCE on GB10](/clustering/nccl-over-roce.md) - The NCCL environment that makes multi-Spark collectives use the 200G RoCE fabric (HCAs, GID index, socket interface, ring variables) and the known traps.

# runbook

* [Four or more Sparks — switch or switchless ring](/clustering/switched-fabric.md) - How to join four or more GB10 units — a MikroTik CRS812 200G switch with its breakout, RSTP and second-bridge traps, or the switchless four-node ring used by community TP4 recipes.
* [Three Sparks in a ring](/clustering/three-node-ring.md) - Wire, address and validate three GB10 units as a switchless ring of three QSFP cables, and what a third unit buys over two.
* [Two Sparks over one DAC](/clustering/two-node-dac.md) - Wire, address and prove a 2-node GB10 cluster on one QSFP112 cable — the minimal multi-Spark setup.
<!-- okf:generated:index end -->
