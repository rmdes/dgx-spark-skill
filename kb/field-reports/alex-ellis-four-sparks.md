---
type: report
title: "Field report: OpenFaaS Ltd buys four DGX Sparks"
description: Alex Ellis (OpenFaaS Ltd) on why a small software company moved from one RTX 6000 Pro to four DGX Sparks for private coding, support and red-teaming, and what the numbers really were.
tags: [field-report, self-reported, team-usage, deepseek, glm, switchless, gateway]
resource: /field-reports/alex-ellis-four-sparks.md
timestamp: "2026-10-29T00:00:00Z"
aliases: [How and Why We Bought 4x DGX Sparks, Alex Ellis four Sparks]
entities:
  - label: Alex Ellis
    kind: person
  - label: OpenFaaS Ltd
    kind: organization
  - label: toilgate
    kind: tool
  - label: RigMark
    kind: benchmark
  - label: switchless-nccl
    kind: tool
relations:
  - type: follows
    target: /field-reports/alex-ellis-local-vs-opus.md
  - type: cites
    target: /models/deepseek-v4-family.md
  - type: cites
    target: /models/glm53-family.md
  - type: compares_to
    target: /clustering/switched-fabric.md
provenance:
  - source: https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/
    note: Blog post by Alex Ellis, published 2026-09-15. Self-reported by the buyer; no vendor sponsorship stated.
citations:
  - id: ae-4x
    text: "Alex Ellis, How and Why We Bought 4x DGX Sparks (2026-09-15). https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/"
---

# Overview

**Source type: self-reported, independent buyer.** Alex Ellis runs OpenFaaS Ltd, a small company building
infrastructure software (OpenFaaS, SlicerVM, Inlets) used in regulated industries. After a few months on one
RTX 6000 Pro running Qwen 27B, the team bought two DGX Sparks, then two more, to run larger
mixture-of-experts models locally [ae-4x]. The post is the follow-up to
[Local Qwen isn't a worse Opus](/field-reports/alex-ellis-local-vs-opus.md).

| Item | Detail |
|---|---|
| Who | Alex Ellis, founder, small software team (OpenFaaS Ltd, UK) |
| Hardware | 4× DGX Spark Founders Edition, 4 TB; existing RTX 6000 Pro (Qwen) |
| Fabric | 4-node switchless ring, patched NCCL; no switch bought |
| Models | Qwen 3.6–3.8 27B (GPU), DeepSeek V4 Flash 0731 (2 Sparks), GLM-5.3 Flash TP4 (4 Sparks) |
| Workloads | Coding agents (opencode, pi), product planning and reports, customer support, red-teaming own code |
| Access | Internal LLM gateway "toilgate": OAuth for humans, API keys for bots, usage metrics |

# Why they bought

- **Data that cannot leave.** Customer Kubernetes dumps and core IP; the author rejects "zero data retention"
  promises as still being data sharing [ae-4x].
- **Red-teaming.** Cloud providers flag offensive-security work; joining a big lab's cyber-defence programme
  can require disabling ZDR. Both DeepSeek and GLM complied with red-team prompts without abliterated weights [ae-4x].
- **Model size.** GLM 5.2 has 753B parameters; no consumer GPU holds it, a Spark cluster does [ae-4x].
- **Not cost per token.** "It may well take you years to recoup the costs on that basis compared to coding plans" [ae-4x].

# What worked

- **DeepSeek V4 Flash 0731 on two Sparks** became the "explorer" model: 1M-token context per session against
  Qwen's 256K native, used for larger unsupervised tasks. During a week of trial on a friend's two units the author
  pushed about 70–100M tokens per day, cache hits included [ae-4x]. See [DeepSeek V4 family](/models/deepseek-v4-family.md).
- **GLM-5.3 Flash TP4 on four Sparks** without a switch: a ring (A–B, A–C, B–D, C–D) where non-adjacent units
  relay through a neighbour via patched NCCL. The author says speed "seems on par with a switched setup";
  no numbers given [ae-4x]. Compare [switched fabric](/clustering/switched-fabric.md) and
  [GLM-5.3 family](/models/glm53-family.md).
- **A week-long red-team contest** (Qwen vs DeepSeek vs GLM-5.3 Flash, ranks R0–R8 over six private repos,
  run by a governor agent) found real High, Medium and Low vulnerabilities, since fixed [ae-4x].
- **A team gateway** (toilgate) solved model discovery, who-uses-what metrics, OAuth and API keys, with an opencode
  and pi plugin that lists all models at start-up [ae-4x].
- Setup is headless (Wi-Fi hotspot onboarding); units are "extremely quiet whilst serving" [ae-4x].

# What did not work

| Problem | Detail |
|---|---|
| Inflated speed claims | Community recipe claimed 65–85 tok/s for DeepSeek V4 Flash on 2 Sparks; that was "counting to 200". Real use was often 30–40 tok/s [ae-4x] |
| Looping | Qwen on the RTX 6000 Pro looped unattended for 30 minutes at about 1000 W at the wall; DeepSeek looped once on a Korean character [ae-4x] |
| Abliterated weights | Drafter acceptance rate dropped sharply; base model already compliant (11/12 vs 12/12 security prompts) [ae-4x] |
| Quantization variance | GLM 5.3 Flash NVFP4: NVIDIA's build was 20% faster at prefill but 7% slower at decode than LibertAI's [ae-4x] |
| Platform risk | DeepSeek 4.1 Flash weights are almost double V4 Flash 0731; NVIDIA reportedly halting first-edition production (OEM variants continue) [ae-4x] |

# Measured / money

| Figure | Value |
|---|---|
| Two Sparks, 4 TB, UK | almost 10,000 GBP [ae-4x] |
| NVIDIA Inception discount via reseller | about 600 GBP back [ae-4x] |
| RTX 6000 Pro | bought ~8,500 GBP, later ~16,000 GBP [ae-4x] |
| Switch avoided | MikroTik CRS804 DDQ, 1,500 GBP [ae-4x] |
| DeepSeek V4 Flash, 2 Sparks, real use | often 30–40 tok/s [ae-4x] |

All figures are self-reported. The author published [RigMark](https://github.com/alexellis/rigmark) to benchmark
coding and agentic workloads consistently, because speed claims depend on task type (prose slowest,
"count to 200" fastest, code up to 2× prose), context and concurrency [ae-4x]. See
[speculative decoding](/stacks/speculative-decoding.md).

# Verdict

"The Sparks have absolutely won me over for utility, value for money, and performance." The 4 TB drive is called
essential; buying four of one generation is a risk the author accepts because today's models keep their value [ae-4x].

# Takeaways for a small team

- The closest match to a small team with a privacy-first motive: a shared gateway in front of several Sparks, with the
  gateway as the operations layer (see [coding agents on local models](/stacks/coding-agents-on-local-models.md)).
- Two Sparks were enough for a DeepSeek V4 Flash-class "explorer" at 30–40 tok/s real-world. Four were bought only for a
  753B-class red-team model. That supports starting with 2–3 units unless a 700B-class model is a goal.
- Plan for supervision: looping and inflated recipe numbers were real. Measure on your own tasks before trusting speeds.
- The author does not claim cost savings over cloud subscriptions; the case is data protection, capacity and independence.
