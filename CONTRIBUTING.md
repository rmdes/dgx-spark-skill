<!-- ABOUTME: How to add or correct a page in the DGX Spark knowledge base. -->
<!-- ABOUTME: Short on purpose: the rules are the ones CI enforces. -->
# Contributing

Corrections and additions are welcome: open an issue, or a pull request against `kb/`.

## Page conventions

- One concept per Markdown file under `kb/<section>/`, with YAML frontmatter (`type`, `title`, `description`, `tags`,
  `resource`, `timestamp`). Copy an existing page of the same type as a template.
- **Cite everything.** Each claim carries a bracketed id (`[cape-serve]`) that resolves to a `citations:` entry with a URL.
  Say whether a figure is *self-reported* by the source, *independently measured*, or *self-measured* by the maintainer.
- State the date and the hardware for any number. Recipes and prices move fast.
- Link other pages root-relative (`/stacks/vllm.md`). Every link must resolve.
- Quote string list items in frontmatter and never put a `!` in a frontmatter value (CI parses without PyYAML; see the
  README).

## Before you push

```bash
vendor/okf-loom/scripts/okf-loom index kb
vendor/okf-loom/scripts/okf-loom validate kb --strict
vendor/okf-loom/scripts/okf-loom build kb --target static --out public && python3 check_site.py public
```

CI runs the same steps on every pull request and deploys only from `main`.

## Measurements

If you add benchmark results, include the exact command, the engine and image versions, the hardware (vendor and BIOS if
known) and at least three fresh starts: single-stream decode varied by up to ~20 % between vLLM starts on identical setups.
