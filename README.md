<!-- ABOUTME: DGX Spark knowledge base — an OKF bundle of synthesis, plus the collection tooling and benchmarks behind it. -->
<!-- ABOUTME: Published as a site on GitHub Pages; raw sources live in the maintainer's Obsidian vault. -->
# dgx-spark-skill

A community knowledge base on running and clustering NVIDIA DGX Spark (GB10) for fully local AI work, with one, two or
more Sparks: hardware limits, cabling and NCCL, serving stacks, which model needs how many Sparks, and field reports from
people who already do this daily. Published as a site on GitHub Pages (enable it under *Settings → Pages → Source:
GitHub Actions*).

| Path | What |
|---|---|
| `kb/` | The knowledge base, as an [OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) bundle (plain Markdown + YAML frontmatter). |
| `sources.txt` | Manifest of every source collected, with skipped links and the reason. |
| `clip.py` | Collector: GitHub URL → whole-repo ingest (docs, recipes, charts); other URL → defuddle clip. |
| `test_clip.py` | Assert-based checks for `clip.py` (`python3 test_clip.py`). |
| `benchmarks/` | Raw llama-benchy results and scripts: an NVIDIA Founders Edition and a Dell Pro Max GB10, same command. |
| `check_site.py` | Smoke check of a built site: every local link has a target, graph not empty (`python3 check_site.py <dir>`). |
| `.github/workflows/pages.yml` | CI: validate, build, check, and deploy to GitHub Pages on push to `main`. |
| `vendor/okf-loom/` | [okf-loom](https://github.com/ojamin/okf-loom) runtime (Apache-2.0, Python 3.12+), pinned in `VENDORED.md`. |

## Read it

Locally, with a live wiki and graph view:

```bash
vendor/okf-loom/scripts/okf-loom serve kb --no-open      # http://127.0.0.1:8787
```

Never use `serve --tunnel` unless you mean to publish the bundle through a public Cloudflare link.

## Write / review the knowledge base

okf-loom needs Python **3.12+** in practice (its render path uses PEP 701 f-strings; upstream says 3.11).
`PYTHON=/usr/bin/python3` if your default is older. See [CONTRIBUTING.md](CONTRIBUTING.md) for the page conventions.

```bash
vendor/okf-loom/scripts/okf-loom index kb                # regenerate section index.md files
vendor/okf-loom/scripts/okf-loom validate kb --strict    # what CI runs
vendor/okf-loom/scripts/okf-loom render kb --out viz.html # one self-contained file

# Same gate as CI, before pushing:
vendor/okf-loom/scripts/okf-loom build kb --target static --out public && python3 check_site.py public
```

CI has **no PyYAML**, so okf-loom uses its stricter built-in YAML parser there; a frontmatter value with an apostrophe
inside an unquoted `[list]` passes locally and fails in CI, and so does a `!` anywhere in a frontmatter value (even quoted:
the fallback reads it as a YAML tag, so write "MR 3", not "MR !3"). Reproduce CI's parser locally by hiding site-packages,
and quote string list items in frontmatter:

```bash
printf '#!/bin/sh\nexec /usr/bin/python3 -S "$@"\n' > /tmp/py-ci && chmod +x /tmp/py-ci
PYTHON=/tmp/py-ci vendor/okf-loom/scripts/okf-loom validate kb --strict
```

A section shows up as a link on the home page only once it contains a concept: okf-loom renders no page for an empty
section, and `check_site.py` fails any link without a target. The generated `index.md` files in each section must be
committed up to date; CI regenerates them and fails on any difference.

## Collect sources

Sources go to an Obsidian vault (`$OBSIDIAN_VAULT`, default `~/Obsidian`, folder `DGX Spark/Sources/`), not into this repo:

```bash
./clip.py <url>                                        # one source
./clip.py $(grep -vE '^\s*(#|$)' sources.txt)          # re-collect everything
```

Lines marked `# MANUAL` in `sources.txt` block scrapers and were clipped by hand with Obsidian Web Clipper.

## Upgrading okf-loom

Vendored okf-loom is used as-is. To upgrade, re-copy `scripts/okf-loom` + `scripts/okf_loom/` from a newer checkout and
bump the commit in `vendor/okf-loom/VENDORED.md`.

## Licence

The vendored okf-loom keeps its Apache-2.0 licence. The knowledge base summarises third-party material and cites every
source; where a source carries a licence with conditions (for example the CC-BY-4.0 GB10 cluster guide), the page cites it
and the conditions still apply.
