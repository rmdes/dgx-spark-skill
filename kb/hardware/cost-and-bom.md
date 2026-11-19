---
type: reference
title: Cost and bill of materials
description: Dated unit prices for DGX Spark and its OEM twins in the EU and US, the cable, breakout and switch prices, and the parts list for 2-, 3- and 4-node builds.
tags: [cost, pricing, bom, procurement]
resource: /hardware/cost-and-bom.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [DGX Spark price, GB10 price, bill of materials, BOM, cluster budget]
entities:
  - label: DGX Spark Founders Edition
    kind: product
  - label: Lenovo ThinkStation PGX
    kind: product
  - label: QSFP112 DAC 0.5 m
    kind: cable
  - label: MikroTik CRS812-8DS-2DQ-2DDQ-RM
    kind: network_switch
relations:
  - type: costs
    target: /clustering/two-node-dac.md
  - type: costs
    target: /clustering/three-node-ring.md
  - type: costs
    target: /clustering/switched-fabric.md
  - type: describes
    target: /hardware/gb10-platform.md
  - type: related_to
    target: /field-reports/alex-ellis-four-sparks.md
provenance:
  - source: https://pi3g.com/nvidia-dgx-spark-price/
    note: pi3g / BuyZero EU net price list from distributor data sent 3–18 September 2026 (page dated 2026-09-23), plus price history.
  - source: https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/06-bill-of-materials.md
    note: Capetron BOM — prices paid or listed August–September 2026, US unit list prices observed June 2026.
  - source: https://petronellatech.com/hardware/dgx-spark-cluster-cable/
    note: Cable retail page (2026-10-06) — single and multipack prices, US only.
  - source: https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/switches.md
    note: UK switch prices and stock checked 2026-08-31, plus MSRPs.
citations:
  - id: pi3g
    text: "pi3g (Maximilian Batz), NVIDIA DGX Spark Price (Q4 2026). EU and US Pricing, All Models Compared (2026-09-23). https://pi3g.com/nvidia-dgx-spark-price/"
  - id: cape-bom
    text: "Capetron, GB10 cluster guide — 06 Bill of materials (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/06-bill-of-materials.md"
  - id: cape-parts
    text: "Capetron, GB10 cluster guide — 08 Parts and where to buy (CC-BY-4.0). https://github.com/capetron/gb10-cluster-guide/blob/51905a2adbcb5582593146a14b4760f8908048c0/docs/08-parts-and-where-to-buy.md"
  - id: petro-cable
    text: "Petronella, DGX Spark Cable, NJAAKK-N911 Alternative: $159 (2026-10-06). https://petronellatech.com/hardware/dgx-spark-cluster-cable/"
  - id: petro-sw
    text: "Petronella, From Two DGX Sparks to a Switched Fabric (2026-09-05). https://petronellatech.com/blog/dgx-spark-cluster-from-two-sparks-to-a-switched-fabric/"
  - id: ae-switches
    text: "Alex Ellis / MiaAI-Lab, Switched alternatives (prices checked 2026-08-31). https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/switches.md"
  - id: ae-fabric
    text: "Alex Ellis / MiaAI-Lab, The ring fabric — addressing template and MTU. https://github.com/MiaAI-Lab/glm-5.3-flash-4x-dgx-spark-switchless/blob/2b92a8f62e6f73b5a0268198a01e29b280db0e06/docs/fabric.md"
  - id: ae-blog
    text: "Alex Ellis, How and Why We Bought 4x DGX Sparks (2026-09-15). https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/"
  - id: forum
    text: "NVIDIA Developer Forums, DGX Spark (SM121) Software Support is Severely Lacking (thread opened 2026-01-15). https://forums.developer.nvidia.com/t/dgx-spark-sm121-software-support-is-severely-lacking-official-roadmap-needed/357663"
  - id: simonw
    text: "Simon Willison, NVIDIA DGX Spark: great hardware, early days for the ecosystem (2025-10-14). https://simonwillison.net/2025/Oct/14/nvidia-dgx-spark/"
  - id: exxact
    text: "Exxact, What You Need to Build a 4x NVIDIA DGX Spark Cluster. https://www.exxactcorp.com/blog/deep-learning/what-you-need-to-build-a-4x-nvidia-dgx-spark-cluster-switch-cabling-power"
---

# Overview

Every price below carries its date and whether it is net or gross. Prices have **risen** since launch:
the Founders Edition launched at $3,999 in October 2025 and NVIDIA raised it to $4,699 in February 2026,
citing memory shortages [pi3g]. pi3g does not expect prices to fall while the DRAM shortage lasts
[pi3g] — that is a reseller's view, not a forecast we can verify. Re-quote before ordering.

# Unit prices

## EU, net (excl. VAT and shipping) — pi3g / BuyZero, distributor data 3–18 September 2026 [pi3g]

| Model | Storage | Net EUR | Lead time quoted |
|---|---|---|---|
| Lenovo ThinkStation PGX (no OS) | 1 TB | €5,038 | mid-October |
| Gigabyte AI TOP ATOM (PCIe Gen4) | 4 TB | €5,492 | end of September |
| HP ZGX Nano G1n | 2 TB | €5,496 | 4–5 days |
| **NVIDIA DGX Spark Founders Edition (PNY)** | 4 TB | **€5,612** | end of September |
| Dell Pro Max with GB10 | 4 TB | €5,667 | end of September |
| MSI EdgeXpert | 4 TB | €5,777 | 1–2 weeks |
| Lenovo ThinkStation PGX | 2 TB | €5,834 | 3–4 days |
| Dell Pro Max with GB10 | 2 TB | €5,914 | mid-December |
| Acer Veriton GN100 | 4 TB | €6,013 | 4–5 days |
| ASUS Ascent GX10 | 1 TB | €6,394 | 3–4 weeks |
| HP ZGX Nano G1n | 4 TB | €6,985 | 4–5 days |
| Lenovo ThinkStation PGX | 4 TB | €7,214 | end of September |
| ASUS Ascent GX10 | 4 TB | €7,265 | 3–4 days |
| ASUS Ascent GX10 | 2 TB | €8,096 | November |
| DGX Spark **64 GB** (OEM partners) | TBC | from €3,150 | TBC (launched October 2026) |

With German VAT (19 %) the cheapest 128 GB unit, the 1 TB Lenovo PGX, is €5,995 gross [pi3g].
The same page lists the 64 GB unit at "$4999" in its USD column, which does not match its own €→$
conversion; treat the 64 GB USD figure as unreliable [pi3g]. All GB10 units share the chip and power
cap, so these are differences in storage, OS, chassis and cooling, not speed [cape-bom].

## US and UK

| Date | Item | Price | Source |
|---|---|---|---|
| Jan 2025 | Project DIGITS announced | from $3,000 | [pi3g] |
| Mar 2025 | ASUS Ascent GX10 1 TB announced | $2,999 | [pi3g] |
| Oct 2025 | Founders Edition launch | $3,999 ("around $4,000") | [pi3g] [simonw] |
| Feb 2026 | Founders Edition list after NVIDIA's increase | $4,699 (+$700, 18 %) | [pi3g] |
| Jun 2026 | 4 TB list prices observed: Gigabyte ATOM $3,999; ASUS GX10 ~$4,149; Founders Edition $4,699; MSI EdgeXpert ~$4,000 | as listed | [cape-bom] |
| Sep 2026 | Cheapest on Amazon US (Micro Center); NVIDIA store out of stock | $4,999.99 | [pi3g] |
| before 2026-09-15 | Two Founders Edition 4 TB, UK (Scan) | "almost 10000 GBP" for two; ~£600 back via NVIDIA Inception | [ae-blog] |

NVIDIA Inception (startups) and Education discount programmes exist [pi3g] [ae-blog].

# Cables

| Item | Price | Date | Source |
|---|---|---|---|
| 0.5 m QSFP112 DAC (Amphenol NJAAKR-0006), single | $159 | 2026-10-06 | [petro-cable] |
| 2-pack | $299 ($149.50 each) | 2026-10-06 | [petro-cable] |
| 3-pack ring kit | $435 ($145 each) | 2026-10-06 | [petro-cable] |
| 4-pack four-node ring kit | $568 | 2026-10-06 | [petro-cable] |
| QSFP56-DD → 2 × QSFP56 breakout (NADDOD Q2Q56-400G-CU1) | $138 each, paid | build notes 2026-08-17 | [cape-bom] |
| 2 × DAC cables, owner-reported | $290 | forum post in thread opened 2026-01-15 | [forum] |

Petronella ships to **US addresses only**, free shipping; returns carry a 15 % restocking fee plus $20
[petro-cable]. For Belgium we need an EU source: the Lenovo 4X91U42988 cable (owners reported overseas
shipping in one to two weeks) and DigiKey (reported to ship internationally) are the alternatives
listed [cape-parts]; no EU price is published in the collected sources. The switchless four-node ring recipe
runs on 0.4–0.5 m Amphenol **100G QSFP28** DACs; price not published [ae-fabric].

# Switches (only for four or more nodes, or if you want one)

UK prices including 20 % VAT, checked **2026-08-31** [ae-switches]:

| Switch | UK price | Stock then | MSRP | Max power |
|---|---|---|---|---|
| CRS504-4XQ-IN (4 × 100G) | from £599.44 | out of stock UK-wide | $799 | 41 W |
| CRS520-4XS-16XQ-RM (16 × 100G) | £1,679.99 | 3 in stock | $2,195 | 150 W |
| CRS804-4DDQ-hRM (4 × 400G) | £1,139.99 (≈£1,009 elsewhere) | pre-order, batches 2 Oct / 18 Dec 2026 | $1,295 | 123 W |
| **CRS812-8DS-2DQ-2DDQ-RM** (2 × 400G + 2 × 200G) | £1,040.64 (£867.20 ex VAT) | 5 available | $1,295 | 134 W |

Conflicting figure: Alex Ellis put the CRS804 at **1500 GBP** in his 2026-09-15 post [ae-blog] against
£1,139.99 in the 2026-08-31 snapshot from the same team's repository [ae-switches]. Capetron
and Petronella decline to quote switch prices [cape-bom] [petro-sw]. A forum owner reported $1,000 for
their switch (thread opened 2026-01-15; model not stated) [forum].

# Bill of materials by cluster size

Fabric parts only; add the units from the tables above. US cable prices from [petro-cable] and
[cape-bom]; switch from [ae-switches].

| Build | Units | Cables | Other | Fabric cost |
|---|---|---|---|---|
| 2 nodes, direct | 2 | 1 × QSFP112 DAC | — | $159 |
| 3 nodes, ring | 3 | 3 × QSFP112 DAC | — | $435 (3-pack) |
| 4 nodes, switchless ring | 4 | 4 × DAC | patched NCCL; recipe must support the ring | $568 (4-pack) |
| 4 nodes, one switch | 4 | 4 × QSFP112 DAC | 2 × breakout, 1 × CRS812 | $874 + switch (£1,040.64 inc VAT on 2026-08-31) |
| 6 nodes, two switches | 6 | 6 × DAC | 3 × breakout, 1 ISL DAC, 2 switches | $1,311–$1,470 + two switches |
| 8 nodes, two switches | 8 | 8 × DAC | 4 × breakout, 1 ISL DAC, 2 switches | $1,748–$1,907 + two switches |

The 2-, 3-, 4-switch, 6- and 8-node rows are from [cape-bom] and [petro-sw]; the 4-node ring kit price
is from [petro-cable].

Items the sources recommend but do not price: a **smart PDU** for remote power cycling (no BMC) and
rack space/power for the switch [cape-bom]. Exxact's 4-node build uses the CRS804 and either four
QSFP-DD → QSFP56 cables or two breakouts; it publishes no prices [exxact].

# Worked example

Starting from two units: going to three adds one unit and two cables
(the pair's existing cable plus two more make the 3-cable ring); going to four adds two units and either a
4-cable ring or a switch. With EU Founders Edition pricing of €5,612 net per unit (September 2026)
[pi3g], units dominate the budget; the fabric is $435–$874 plus an optional switch.

# Limitations

- No EU cable or EU switch prices in the collected sources; switch prices are UK.
- Every price here is a snapshot; pi3g and Petronella are sellers of what they price.
