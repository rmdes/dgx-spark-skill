#!/usr/bin/env python3
# ABOUTME: Clips web pages to clean Markdown via defuddle (npx) into a dedicated folder of the Obsidian vault.
# ABOUTME: Usage: ./clip.py <url> [<url> ...] — frontmatter matches Obsidian Web Clipper; re-clipping overwrites.
"""Fetch documentation pages as Obsidian notes (Web Clipper-style frontmatter, filename = page title)."""
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

VAULT = pathlib.Path(os.environ.get("OBSIDIAN_VAULT", pathlib.Path.home() / "Obsidian"))
DEST = pathlib.Path(os.environ.get("CLIP_DIR", VAULT / "DGX Spark"))


def note_name(title: str, url: str) -> str:
    """Obsidian-safe filename from the page title; drops the 'Page — Site' doubled suffix."""
    parts = [p.strip() for p in re.split(r"\s+[—|–-]\s+", title) if p.strip()]
    name = parts[0] if parts else url.rstrip("/").rsplit("/", 1)[-1]
    name = re.sub(r'[\\/:*?"<>|#^\[\]]', " ", name)  # chars Obsidian/Windows reject in names/links
    return re.sub(r"\s+", " ", name).strip()[:120] or "untitled"


def free_path(folder: pathlib.Path, name: str, url: str) -> pathlib.Path:
    """Same URL → same file (re-clip updates it); a different URL with the same title gets a suffix, never overwrites.

    Multi-page articles share one title: without this, page 2 silently replaced page 1.
    """
    slug = [s for s in url.split("?")[0].rstrip("/").split("/") if s][-1]
    for n in range(100):
        candidate = folder / (f"{name}.md" if n == 0 else f"{name} ({slug}).md" if n == 1 else f"{name} ({slug} {n}).md")
        if not candidate.exists():
            return candidate
        if re.search(rf"^source: {re.escape(json.dumps(url, ensure_ascii=False))}$", candidate.read_text(encoding="utf-8"), re.M):
            return candidate
    raise RuntimeError(f"too many notes titled {name!r}")


def clip(url: str) -> pathlib.Path:
    out = subprocess.run(
        ["npx", "--loglevel=silent", "-y", "defuddle", "parse", url, "--json", "--md"],
        capture_output=True, text=True, timeout=180,
    )
    if out.returncode != 0:
        raise RuntimeError(f"defuddle failed: {out.stderr.strip()[-500:]}")
    data = json.loads(out.stdout)
    if not data.get("content", "").strip():
        raise RuntimeError("defuddle returned empty content (JS-rendered page?)")

    q = lambda v: json.dumps(v, ensure_ascii=False)  # JSON strings are valid YAML scalars
    lines = ["---", f"title: {q(data.get('title', ''))}", f"source: {q(url)}"]
    if data.get("author"):
        lines += ["author:", f"  - {q('[[' + data['author'] + ']]')}"]
    if data.get("published"):
        lines.append(f"published: {data['published'][:10]}")
    lines += [
        f"created: {datetime.date.today().isoformat()}",
        f"description: {q(data.get('description', ''))}",
        "tags:", '  - "clippings"', "  - dgx-spark",
        "---", "",
    ]

    web = DEST / "Sources" / "web"
    web.mkdir(parents=True, exist_ok=True)
    dest = free_path(web, note_name(data.get("title", ""), url), url)
    dest.write_text("\n".join(lines) + data["content"].strip() + "\n", encoding="utf-8")
    return dest


GITHUB = re.compile(r"https://github\.com/([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?(?:(?:blob|tree)/.*)?$")
SKIP_MD = {"LICENSE.md", "THIRD_PARTY_NOTICES.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"}
RECIPE_DIRS = {"recipes", "recipe", "config", "configs", "profiles", "deploy"}
SKIP_DIRS = {".git", ".github", "LICENSES", "test-fixtures"}
RECIPE_EXT = {".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml", ".env": "bash",
              ".example": "bash", ".sh": "bash"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")
SPARK = re.compile(r"spark|gb10|sm_?121", re.I)
RECIPE_MAX = 64_000  # real recipes are 4-10 KB; bigger files under recipes/ are benchmark evidence or SBOMs
IMAGE_MAX = 1_000_000  # big PNGs are UI screenshots; their links fall back to GitHub


def repo_plan(root: pathlib.Path) -> dict[str, str]:
    """Map repo-relative path -> vault-relative name for everything worth keeping (docs, recipes, images)."""
    spark_repo = bool(re.search(r"spark|dgx", root.name, re.I))
    plan = {}
    for f in root.rglob("*"):
        rel = f.relative_to(root)
        if not f.is_file() or SKIP_DIRS & set(rel.parts):
            continue
        ext, key, size = f.suffix.lower(), rel.as_posix(), f.stat().st_size
        if ext == ".md" and f.name not in SKIP_MD:
            plan[key] = key
        elif ext in RECIPE_EXT and RECIPE_DIRS & set(rel.parts[:-1]) and size <= RECIPE_MAX:
            # generic repos (e.g. a multi-GPU registry) only contribute their Spark recipes
            if spark_repo or SPARK.search(key) or SPARK.search(f.read_text(errors="replace")):
                plan[key] = key + ".md"  # wrapped in a note: Obsidian doesn't index raw json/yaml
        elif ext in IMAGE_EXT and size <= IMAGE_MAX:
            plan[key] = key
    return plan


def rewrite_links(text: str, src: str, plan: dict[str, str], blob: str) -> str:
    """Relative links to kept files follow the vault names; anything else points to GitHub at the pinned commit."""
    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"^([a-z]+:|#|<)", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        resolved = os.path.normpath(os.path.join(os.path.dirname(src), path)).replace(os.sep, "/")
        if resolved.startswith(".."):
            return m.group(0)
        if resolved in plan:
            new = os.path.relpath(plan[resolved], os.path.dirname(src) or ".").replace(os.sep, "/")
        else:
            new = f"{blob}/{resolved}"
        return f"{m.group(1)}{new}{'#' + anchor if anchor else ''}{m.group(3)}"
    return LINK.sub(fix, text)


def ingest_repo(owner: str, repo: str) -> pathlib.Path:
    """Shallow-clone a GitHub repo and mirror its docs, recipes and images into Sources/<repo>/ (regenerated)."""
    import shutil
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / repo
        subprocess.run(["git", "clone", "-q", "--depth", "1", f"https://github.com/{owner}/{repo}.git", str(src)],
                       check=True, timeout=300)
        sha = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"],
                             capture_output=True, text=True, check=True).stdout.strip()
        blob = f"https://github.com/{owner}/{repo}/blob/{sha}"
        plan = repo_plan(src)

        out = DEST / "Sources" / repo
        if out.exists():
            shutil.rmtree(out)  # Sources/ is generated: our own notes live in Knowledge/
        q = lambda v: json.dumps(v, ensure_ascii=False)
        for rel, name in sorted(plan.items()):
            dest = out / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            f = src / rel
            if f.suffix.lower() in IMAGE_EXT:
                shutil.copyfile(f, dest)
                continue
            body = f.read_text(encoding="utf-8", errors="replace")
            if name != rel:  # recipe/config wrapped as a note
                body = f"# {f.name}\n\n```{RECIPE_EXT[f.suffix.lower()]}\n{body.rstrip()}\n```\n"
                kind = "recipe"
            else:
                body = rewrite_links(body, rel, plan, blob)
                kind = "doc"
            heading = re.search(r"^#\s+(.+)$", body, re.M)
            front = [
                "---", f"title: {q(heading.group(1).strip() if heading else f.stem)}",
                f"source: {q(f'{blob}/{rel}')}", f"repo: {q(f'{owner}/{repo}')}", f"commit: {sha[:12]}",
                f"created: {datetime.date.today().isoformat()}",
                "tags:", '  - "clippings"', "  - dgx-spark", f"  - source/{repo.lower()}", f"  - kind/{kind}",
                "---", "",
            ]
            dest.write_text("\n".join(front) + body, encoding="utf-8")
        kinds = {"recipe": sum(1 for r, n in plan.items() if r != n),
                 "image": sum(1 for r in plan if pathlib.Path(r).suffix.lower() in IMAGE_EXT)}
        print(f"     {len(plan) - kinds['recipe'] - kinds['image']} docs, {kinds['recipe']} recipes, "
              f"{kinds['image']} images @ {sha[:12]}")
        return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: clip.py <url> [<url> ...]   (github.com/<owner>/<repo>/... = whole-repo ingest)")
    if not DEST.parent.exists():
        sys.exit(f"destination parent missing (vault not mounted?): {DEST.parent}")
    failed = 0
    for u in sys.argv[1:]:
        try:
            m = GITHUB.match(u)
            print(f"OK   {ingest_repo(*m.groups()) if m else clip(u)}  <- {u}")
        except Exception as e:  # keep going on batch input, report at the end
            failed += 1
            print(f"FAIL {u}: {e}", file=sys.stderr)
    sys.exit(1 if failed else 0)
