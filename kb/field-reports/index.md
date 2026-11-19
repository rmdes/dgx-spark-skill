# Field reports

Teams and individuals running daily development work on local AI hardware.

<!-- okf:generated:index begin -->
# report

* [Field report (vendor): NVIDIA on scaling agents and workloads across DGX Sparks](/field-reports/nvidia-agents-on-spark.md) - NVIDIA's own benchmarks for agent-style long-context inference, concurrency, and one-to-four-node scaling of inference and fine-tuning on DGX Spark.
* [Field report: a home Spark stack (local-ai)](/field-reports/our-home-spark-local-ai.md) - A single DGX Spark Founders Edition run as a home AI server - one vLLM behind a LiteLLM gateway over Tailscale - with measured benchmarks of four models and the engine research behind its design.
* [Field report: EXO 1.0 splits prefill (DGX Spark) and decode (Mac Studio)](/field-reports/exo-spark-mac-studio.md) - EXO Labs' early-access experiment — prefill on a DGX Spark, decode on an M3 Ultra Mac Studio, KV cache streamed layer by layer — for 2.8× faster end-to-end inference than the Mac alone.
* [Field report: local Qwen is not a worse Opus, it is a different tool](/field-reports/alex-ellis-local-vs-opus.md) - Alex Ellis's account of six months running Qwen 27B on an RTX 6000 Pro for a small software business — what local models did well, where they looped, and why it is an operations problem.
* [Field report: OpenFaaS Ltd buys four DGX Sparks](/field-reports/alex-ellis-four-sparks.md) - Alex Ellis (OpenFaaS Ltd) on why a small software company moved from one RTX 6000 Pro to four DGX Sparks for private coding, support and red-teaming, and what the numbers really were.
* [Field report: Petronella's six-node GB10 cluster on two MikroTik switches](/field-reports/capetron-six-node-cluster.md) - Petronella Technology Group's measured build of six GB10 workstations (4 MSI + 2 DGX Spark) on a switched 200G RoCE fabric — what broke, what it measured, and why six units serve as pools rather than one model.
* [Field report: ServeTheHome DGX Spark review (hardware, networking, performance, power, verdict)](/field-reports/servethehome-review.md) - ServeTheHome's four-page launch review of a pre-production DGX Spark — hardware and GB10 details, a ConnectX-7 that measured only ~96 Gb/s in iperf3, untuned Ollama speeds, wall power and noise, and a "game-changer for local AI development" verdict despite 273 GB/s of memory bandwidth.
* [Field report: Simon Willison's first look at the DGX Spark (launch week)](/field-reports/simon-willison-first-look.md) - Simon Willison's launch-day review of a preview DGX Spark — great hardware, but CUDA-on-ARM64 software pain, and an ecosystem that only arrived on embargo day.
* [Field report: State of Local AI 2026 (beginner guide, partial capture)](/field-reports/state-of-local-ai-2026.md) - A 2026 beginner's guide arguing that local AI is now affordable and that cloud usage limits make owning your models a dependency hedge; only the introduction and glossary were captured.
* [Field report: The DGX Spark Handbook (0xSero, EXO Labs blog)](/field-reports/exolabs-handbook.md) - The most complete community overview of the DGX Spark in 2026 — prices, power, six models with measured speeds, a one-to-four Spark path, and why the Spark is a prefill and research box.
<!-- okf:generated:index end -->
