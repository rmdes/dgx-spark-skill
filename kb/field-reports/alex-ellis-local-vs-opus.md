---
type: report
title: "Field report: local Qwen is not a worse Opus, it is a different tool"
description: Alex Ellis's account of six months running Qwen 27B on an RTX 6000 Pro for a small software business — what local models did well, where they looped, and why it is an operations problem.
tags: [field-report, self-reported, qwen, coding-agents, looping, rtx-6000-pro]
resource: /field-reports/alex-ellis-local-vs-opus.md
timestamp: "2026-10-29T00:00:00Z"
aliases: ["Local Qwen isn't a worse Opus", "local-ai-is-not-opus"]
entities:
  - label: Alex Ellis
    kind: person
  - label: RTX PRO 6000 Blackwell
    kind: gpu
  - label: llama.cpp
    kind: inference_engine
  - label: Qwopus
    kind: model
relations:
  - type: precedes
    target: /field-reports/alex-ellis-four-sparks.md
  - type: cites
    target: /stacks/speculative-decoding.md
provenance:
  - source: https://blog.alexellis.io/local-ai-is-not-opus/
    note: Blog post by Alex Ellis, published 2026-06-17. Self-reported; not a DGX Spark report (RTX 6000 Pro and RTX 3090s).
citations:
  - id: ae-opus
    text: "Alex Ellis, Local Qwen isn't a worse Opus, it's a different tool (2026-06-17). https://blog.alexellis.io/local-ai-is-not-opus/"
---

# Overview

**Source type: self-reported, independent user. Not a Spark report** — the hardware is a discrete GPU. It is
in this knowledge base because it is the most candid public account of what a dense ~27B local model can and
cannot do for daily software work, and it is the prequel to the
[four-Spark purchase](/field-reports/alex-ellis-four-sparks.md) [ae-opus].

| Item | Detail |
|---|---|
| Who | Alex Ellis, OpenFaaS Ltd; Go infrastructure products; small team |
| Hardware | RTX PRO 6000 Blackwell 96 GB (~12,000 USD, later ~15,400 USD); earlier 2× RTX 3090 |
| Models | Qwen 3.6 27B base and the Qwopus fine-tune, Q8 GGUF, MTP drafter |
| Engine | Two independent llama.cpp instances (full 262K context each) |
| Access | opencode via a self-written gateway/provider (toilgate) |

# What worked

- **Customer support on data that cannot leave.** Enterprise customers' diagnostic dumps go through an
  air-gapped local model in an ephemeral VM [ae-opus].
- **Revenue recovery.** Feeding the telemetry database to a local model revealed a customer under-paying by about
  4–5× for over 12 months; "that revenue recovery alone paid for the card" [ae-opus].
- **Bounded repo work.** With a detailed AGENTS.md (the arkade project), the local model added CLIs faster than
  human contributors and tested its work. Reading and explaining codebases is called a "superpower" [ae-opus].
- **Speed.** About 93% MTP acceptance; decode went from a stable 67 tok/s to 130–200 tok/s sustained [ae-opus].

# What did not work

| Problem | Detail |
|---|---|
| Looping | Repeated the same list for about half an hour, burning 600 W; a second kind of loop when stuck at the edge of its ability. Seen by the author and a team member [ae-opus] |
| Long-horizon agentic work | "Don't hand it long-horizon, unsupervised agentic work"; the 15K USD card did not fix it [ae-opus] |
| Go code review | Would not stay brief; hallucinated concurrency issues and race conditions; experiment shut down [ae-opus] |
| Arithmetic | Read 27.3K as 273,000 in telemetry analysis; inferred churn wrongly [ae-opus] |
| Shared instance | Two agents on one llama.cpp instance invalidate each other's prefix cache; `--parallel 2` halves context [ae-opus] |
| vLLM on 2× 3090 | 3 tok/s slower than llama.cpp, slow weight loading, still looped [ae-opus] |

# Measured

| Figure | Value | Note |
|---|---|---|
| Decode, Qwen 3.6 27B Q8 + MTP | 67 → 130–200 tok/s | RTX 6000 Pro, self-reported [ae-opus] |
| MTP acceptance | ~93% | [ae-opus] |
| Power, RTX 6000 Pro inference | 600 W | Shelly plugs at the wall [ae-opus] |
| Power, 2× RTX 3090 | ~750 W combined, "extremely noisy" | [ae-opus] |
| SWE-Bench Verified, Qwen 3.6 27B vs Claude Opus 4.8 | 77.2 vs 88.6% | vendor benchmark figures quoted by the author; he argues they overstate real-world parity [ae-opus] |

# Verdict

Local Qwen is "not near Opus levels" but has real value for specialised, bounded tasks. Once a second person
uses it, local AI "turns into an operations problem": identity, access control, metering, quotas, routing and
power monitoring [ae-opus].

# Takeaways

- Set expectations correctly: a local ~27–35B model replaces cloud for bounded, supervised tasks
  (support, repo chores, codebase Q&A), not for unattended long-horizon agent work.
- A smoke test (a completion and a tool call) is not a quality benchmark, and a small agentic benchmark saturates quickly.
  A harder, task-based local-vs-cloud comparison is needed before claiming more.
- The operations list (identity, metering, quotas, routing) is what a LiteLLM-style gateway provides; see
  [coding agents on local models](/stacks/coding-agents-on-local-models.md).
- Concurrency matters for a team: one shared single-slot instance thrashes; that argues for more memory/units
  rather than more users per box.
