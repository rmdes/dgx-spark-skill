---
type: guide
title: Coding agents on local models
description: How to wire opencode, Claude Code, pi, Hermes, Aider, Continue, Open WebUI and OpenAI SDK clients to models served on DGX Sparks directly or through a gateway, and the traps that bite in daily use.
tags: ["coding-agents", "opencode", "claude-code", "litellm", "gateway", "openai-api", "anthropic-api", "tool-calling", "reasoning", "guide"]
resource: /stacks/coding-agents-on-local-models.md
timestamp: "2026-10-29T00:00:00Z"
aliases: ["local coding agents", "agent wiring", "LLM gateway for agents", "opencode on Spark"]
entities:
  - label: LiteLLM
    kind: gateway
  - label: toilgate
    kind: gateway
  - label: opencode
    kind: agent_harness
  - label: Claude Code
    kind: agent_harness
  - label: pi
    kind: agent_harness
  - label: Hermes Agent
    kind: agent_harness
  - label: Open WebUI
    kind: application
relations:
  - type: uses
    target: /stacks/tensorfold.md
  - type: uses
    target: /stacks/vllm.md
  - type: uses
    target: /stacks/sglang.md
  - type: cites
    target: /stacks/speculative-decoding.md
  - type: cites
    target: /field-reports/alex-ellis-four-sparks.md
  - type: cites
    target: /field-reports/alex-ellis-local-vs-opus.md
  - type: cites
    target: /field-reports/exolabs-handbook.md
  - type: cites
    target: /models/spark-matrix.md
provenance:
  - source: https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/api.md
    note: TensorFold API reference — OpenAI, Responses and Anthropic Messages routes, tools, reasoning, loop guard, Claude Code command.
  - source: https://mia-ai.net/models
    note: MiaAI-Lab recipe pages ("Talk to it" sections, API lists, thinking defaults). Self-reported.
  - source: https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/cli-coding-agent/README.md
    note: NVIDIA playbook — Claude Code, OpenCode and Codex CLI on one Spark via `ollama launch`.
  - source: https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/
    note: Alex Ellis — toilgate gateway, opencode/pi plugin, looping, prefill cost. Self-reported.
  - source: https://blog.alexellis.io/local-ai-is-not-opus/
    note: Alex Ellis — local vs frontier framing, opencode provider, prefix-cache thrashing. Self-reported, not Spark hardware.
citations:
  - id: tf-api
    text: "Ash Hart, TensorFold docs — Compatible APIs, commit d33dcfc. https://github.com/ashhart/TensorFold/blob/d33dcfc767ee093393c6bfa00b3949bd7b4d8e88/docs/api.md"
  - id: mia-glmf
    text: "MiaAI-Lab, GLM 5.3 Flash on two to four DGX Sparks with TensorFold. https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold"
  - id: mia-q27
    text: "MiaAI-Lab, Qwen3.8 27B on one DGX Spark with TensorFold. https://mia-ai.net/models/Qwen3.8-27B-DGX-Spark-TensorFold"
  - id: mia-fn2
    text: "MiaAI-Lab, Qwen3.8 Flash Next on two DGX Sparks with TensorFold. https://mia-ai.net/models/Qwen3.8-Flash-Dual-DGX-Sparks-TensorFold"
  - id: mia-bolt
    text: "MiaAI-Lab, Nemotron 3.5 Bolt on one DGX Spark with TensorFold. https://mia-ai.net/models/Nemotron-3.5-Bolt-TensorFold-DGX-Spark"
  - id: mia-ds4
    text: "MiaAI-Lab, DeepSeek V4.1 Flash 1017 on four DGX Sparks with TensorFold. https://mia-ai.net/models/DeepSeek-V4.1-Flash-1017-4x-DGX-Sparks-TensorFold"
  - id: sgl-q27
    text: "MiaAI-Lab, Qwen3.8 27B on SGLang for DGX Spark (README). https://github.com/MiaAI-Lab/Qwen3.8-27B-SGLang-DGX-Spark/blob/9fb18edf8cfb3364e8aa89258e6d5ab1fe1fd11a/README.md"
  - id: ds-hermes
    text: "MiaAI-Lab, DeepSeek-V4.1-Flash-1017 2x recipe — Hermes Agent guide (by Steve Darlow). https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/blob/d8e5b28da6ebcf539035be564a4a94d087b2f480/docs/hermes-agent.md"
  - id: nv-cli
    text: "NVIDIA, DGX Spark playbook — CLI Coding Agent. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/cli-coding-agent/README.md"
  - id: nv-vllm
    text: "NVIDIA, DGX Spark playbook — vLLM for Inference. https://github.com/NVIDIA/dgx-spark-playbooks/blob/30883150541743d580c9c347700c6ac99fc396d2/nvidia/vllm/README.md"
  - id: ae-4x
    text: "Alex Ellis, How and Why We Bought 4x DGX Sparks (2026-09-15). https://blog.alexellis.io/how-and-why-we-bought-4-dgx-sparks/"
  - id: ae-opus
    text: "Alex Ellis, Local Qwen isn't a worse Opus, it's a different tool (2026-06-17). https://blog.alexellis.io/local-ai-is-not-opus/"
  - id: hb
    text: "0xSero (EXO Labs), The DGX Spark Handbook (2026-09-25). https://huggingface.co/blog/exolabs/the-dgx-spark-handbook"
---

# Overview

Sparks only become "daily development on local AI" once the tools you use can reach them. Every engine in this
bundle ([TensorFold](/stacks/tensorfold.md), [vLLM](/stacks/vllm.md), [SGLang](/stacks/sglang.md), Ollama) exposes an
OpenAI-compatible `/v1` API; some also answer Anthropic's `/v1/messages`, which Claude Code needs. A common pattern, and
the one in the closest field report, is: **clients → one gateway (keys, routing, metrics) → per-Spark engine
endpoints** [ae-4x].

```
opencode / pi / Hermes / Aider / Continue / Open WebUI / SDKs
        │  OpenAI API, scoped key per user or app
        ▼
   gateway (e.g. LiteLLM on :4000; "toilgate" at OpenFaaS)   ← keys, model allow-list, budget, rpm, usage DB
        │
        ├─► Spark A: vLLM (+ Ollama long tail)   (loopback-only, no auth on the engine)
        └─► Spark B..: TensorFold / vLLM / SGLang recipe on :8888   (one endpoint per model)
```

In the single-Spark version of this, the gateway is the only front door, the engines bind `127.0.0.1` with no
authentication, and every consumer uses `http://<gateway>:4000/v1` with its own key. Extra Sparks are added as more
gateway backends, so users keep the same base URL and key. Whether a given LiteLLM version also answers Anthropic's
`/v1/messages` (for Claude Code) is not verified in the public sources used here.

# Why a gateway

| Need | Evidence or practice |
|---|---|
| Model discovery when a box changes model or goes down | toilgate "discovers the self-hosted models across various machines"; it solved manual tunnels where the machine "may change the model it's serving, it may be down" [ae-4x] |
| Who uses what | toilgate records usage metrics; OAuth for humans, API keys for bots [ae-4x]. A LiteLLM-style gateway can keep per-app and per-person virtual keys in a database that monitoring can read |
| Revocable, scoped access | Good practice: hand out per-app keys with a model allow-list, budget and rpm limit, never the master key |
| One config for all harnesses | Alex Ellis replaced hand-copied `opencode.json` files with an opencode and pi plugin that lists all gateway models at start-up, plus an "auto" mode [ae-4x] [ae-opus] |
| Stable names while models change | Good practice: expose aliases such as `chat`, `coder`, `think` that always point at the active model, so switching the model never changes a client's config. A new alias must be added to a key's allow-list before that key can use it |
| Operations | Alex Ellis: once a second person uses it, local AI "turns into an operations problem" — identity, access control, metering, quotas, routing, power monitoring [ae-opus] |

Gateway settings worth deciding deliberately: retries and request timeouts (long reasoning replies need generous
timeouts), dropping unsupported parameters per engine, and **no silent fallbacks** from one model to another (see
Traps).

# Per client

| Client | API it needs | Engines in the sources that provide it | Config shown in a source? |
|---|---|---|---|
| opencode | OpenAI-compatible (`@ai-sdk/openai-compatible`) | Any `/v1` endpoint or gateway; Ollama via `ollama launch opencode` [nv-cli] | Yes — generic example below |
| Claude Code | Anthropic Messages (`/v1/messages`) | TensorFold (`/v1/messages` + `/count_tokens`) [tf-api] [mia-glmf]; SGLang [sgl-q27]; Ollama via `ollama launch claude` [nv-cli] | Yes — env vars below [tf-api] [sgl-q27] |
| Claude Code via LiteLLM | Anthropic Messages | Not verified in the public sources | No |
| pi | OpenAI-compatible | Any OpenAI-style address [hb]; toilgate plugin [ae-4x] | Not documented in the sources |
| Hermes Agent (Nous Research) | OpenAI-compatible, "custom endpoint" | TensorFold recipes, no recipe change needed [ds-hermes] | Yes — below [ds-hermes] |
| Codex CLI | — | Ollama via `ollama launch codex` [nv-cli] | Launch command only [nv-cli] |
| Aider, Continue, Zed | OpenAI-compatible provider | Gateway or engine: base_url `…/v1`, per-user key, model name | Not documented in the sources |
| Open WebUI | OpenAI-compatible | Gateway or engine as an OpenAI connection | Not in this bundle |
| OpenAI SDK, LangChain, LlamaIndex | OpenAI-compatible | Any: recipes say "any OpenAI client works" with `base_url = http://<head>:8888/v1` [mia-glmf] [mia-ds4] | base_url + key + model only |

**opencode against a gateway** — a generic example (key referenced by file, never inlined). Model IDs must be the
gateway's route names, not engine-native tags:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "spark-gateway": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Spark gateway (LAN)",
      "options": {
        "baseURL": "http://<gateway-host>:4000/v1",
        "apiKey": "{file:/home/YOUR_USER/.config/opencode/spark-gateway.key}"
      },
      "models": {
        "<route-name>": {
          "name": "Local coding model",
          "limit": { "context": <route-context-tokens>, "output": 8192 }
        }
      }
    }
  },
  "model": "spark-gateway/<route-name>"
}
```

Practical rules: a model ID that is an engine tag instead of a gateway route name returns 400; `{file:...}` needs an
absolute path; a trailing newline in the key file is a silent 401; a gateway on plain HTTP should not cross untrusted
network segments, so use an SSH tunnel to `127.0.0.1:4000` there.

**Claude Code directly against TensorFold** (default TensorFold port 8080; recipes use 8888) [tf-api]:

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:8080 ANTHROPIC_API_KEY=local claude --model local-model
```

The model name is the ID from `/v1/models` [tf-api]. For SGLang, set `ANTHROPIC_BASE_URL=http://127.0.0.1:8888` with
no `/v1` suffix — Claude Code appends it [sgl-q27]. TensorFold's Messages route accepts tools, `tool_choice`,
`thinking` and Claude Code's `context_management` directive; server-side tools, documents and redacted thinking return
400, `cache_control` hints allocate nothing (prefix caching stays automatic), and JSON-schema output (including Claude
Code title requests) needs the grammar component [tf-api]. Going direct bypasses gateway keys and metrics; TensorFold
has its own `--api-key` / `--api-key-file` and key scopes [tf-api].

**Hermes Agent** custom endpoint (`config.yaml`) [ds-hermes]:

```yaml
model:
  provider: custom
  base_url: http://127.0.0.1:8888/v1
  default: DeepSeek-V4.1-Flash-1017
  context_length: 1048576
```

The guide warns: verify `/v1/models` and the `model` field of real replies rather than trusting an alias; keep the
endpoint loopback or private; the context value is configured capacity, not a stress-tested window [ds-hermes].

**One-Spark shortcut (no gateway).** NVIDIA's playbook wires Claude Code, OpenCode or Codex CLI to Ollama with one
command and no config files, e.g. `ollama launch claude --model qwen3.6` (Ollama ≥ 0.15) [nv-cli]. Good for a demo on one
box; it gives no per-user keys or metrics.

# Traps (with evidence)

| Trap | What happens | Fix / evidence |
|---|---|---|
| Thinking model + small `max_tokens` | Reasoning goes to `reasoning_content`; the answer can be empty | Recipes say "give replies enough `max_tokens`" (examples use 1,000–2,000) [mia-glmf] [mia-q27] [mia-fn2]; on Nemotron 3.5 Bolt reasoning and answer share `max_tokens` (default 32,768) [mia-bolt]. TensorFold's `--thinking-reserve N` keeps the client's `max_tokens` for the answer on lane engines [tf-api] |
| Thinking switches differ per engine | Qwen recipes: `"chat_template_kwargs": {"enable_thinking": false}` [mia-q27]; TensorFold: `reasoning_effort: none` disables thinking [tf-api] | A gateway can make this uniform, for example reasoning off by default on every route with a separate `think` alias that turns it on |
| Gateway fallback substitution | If a route silently falls back to another model, an evaluation can grade the wrong model | Configure no fallbacks between different models, and log `x-litellm-model-name` per request to prove which model answered |
| Liveness lies | `/v1/models` can stay 200 while completions hang | Probe with a real completion (and ideally a tool call) through the gateway, not the model list |
| Looping when unattended | Qwen looped ~30 min at ~1000 W at the wall on the RTX 6000 Pro; DeepSeek looped once on a Korean character [ae-4x] | Supervise; TensorFold has opt-in `--loop-guard` / `--loop-guard-stop` (ends with `finish_reason: content_filter`, code `reasoning_loop`) [tf-api]; GLM recipe `TF_GLM_LOOP_GUARD=1` [mia-glmf] |
| Tool calling varies by engine | Some server/model pairs emit prose but no tool calls | NVIDIA: a direct Claude Code setup on an Anthropic-compatible Ollama endpoint "produces prose but does not edit files" [nv-cli]. vLLM needs `--tool-call-parser qwen3_xml --enable-auto-tool-choice` in NVIDIA's recipe [nv-vllm]; SGLang needs `--tool-call-parser qwen3_coder` and no extra flag, the hermes parser "would never parse" [sgl-q27]; TensorFold's `glm-zig` backend cannot enforce `tool_choice: required` [tf-api]. For Qwen3.6-style XML tool calls, the parser must match the model's format, not hermes |
| Context window vs prefill time | A long window is not free: 200k tokens cold at 2,000 tok/s is ~100 s [ae-4x] | GLM 5.3 Flash: prefill 1,978.9 tok/s at 32k on two Sparks; a cold 226k prompt 126.6 s on three [mia-glmf]. GLM spill tier: 15/15 200k conversations resumed in 0.8 s vs 110 s [mia-glmf] |
| Shared instance thrashing | Two agents on one llama.cpp instance invalidate each other's cached prefix; `--parallel 2` halves context [ae-opus] | Give agents their own slot/instance or a multi-stream engine (GLM recipe: 4 streams over a shared pool) [mia-glmf] |
| Wrong context limit in the client | opencode can overflow silently if `limit.context` is missing or wrong | Set `limit.context` to the route's real context limit, not a number copied from another model |

# Local vs frontier: how to frame it

Alex Ellis's team uses local models as a **different tool**, not a cheaper Opus [ae-opus]. His summary: Claude and Codex
do most of his coding and can run unattended for long stretches; a local Qwen 27B in opencode is valuable for bounded,
supervised jobs (customer diagnostics that cannot leave the building, repo chores with a good AGENTS.md, codebase
Q&A) and fails when treated like Claude [ae-opus]. His rule: "Don't hand it long-horizon, unsupervised agentic work"
[ae-opus]. After buying Sparks he splits roles: a fast dense Qwen as the focused, closely handled model, and DeepSeek V4
Flash on two Sparks as the slower "explorer" for larger, mostly unsupervised tasks with 1M context [ae-4x]. Details:
[local vs Opus](/field-reports/alex-ellis-local-vs-opus.md), [four Sparks](/field-reports/alex-ellis-four-sparks.md).

Speeds per model and Spark count are in the [Models × Sparks matrix](/models/spark-matrix.md); how drafters change
decode speed is in [speculative decoding](/stacks/speculative-decoding.md); the throughput background for many agents
per box is in the [EXO Labs handbook](/field-reports/exolabs-handbook.md).

# Limitations

- Claude Code through a LiteLLM gateway is not documented in the public sources here; the documented path is pointing it
  at an engine's own Anthropic route, outside gateway keys and metrics.
- No source in this bundle shows a config file for Aider, Continue or pi; only base URL, key and model are documented.
- Recipe numbers (MiaAI-Lab, TensorFold) are self-reported; Alex Ellis found one recipe's 65–85 tok/s claim was really
  30–40 tok/s in use [ae-4x].

# Open questions

- Does a given LiteLLM version serve Anthropic `/v1/messages` well enough for Claude Code, and with which settings?
- How do local models compare with cloud models on your own tasks? A task-based comparison is better than a small
  saturated agentic benchmark; log which model actually answered each request so numbers stay attributable.
- Which of the documented direct setups (per-engine Anthropic routes) can be put behind gateway keys and metrics?
