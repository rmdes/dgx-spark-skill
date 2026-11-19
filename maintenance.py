#!/usr/bin/env python3
# ABOUTME: Scheduled maintenance checks for the knowledge base: dead external links and GitHub sources that moved on.
# ABOUTME: Usage: maintenance.py links|repos [--out report.md]; prints FINDINGS=<n> (also to $GITHUB_OUTPUT). Stdlib only.
"""Keep the knowledge base honest as the world changes.

links  every external URL in kb/ and sources.txt still resolves (dead = 404/410/DNS; blocked and 5xx are only noted)
repos  every GitHub repo in sources.txt: how far its default branch is ahead of the commit pinned in kb/ citations
"""
import argparse
import concurrent.futures
import json
import os
import pathlib
import re
import socket
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).parent
UA = "dgx-spark-kb-maintenance/1.0 (link and source freshness check)"
URL = re.compile(r"https?://[^\s>\]\"'`<]+")  # parentheses allowed; unbalanced trailing ones are trimmed below
SKIP_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "example.com", "example.org"}
BLOCKED = {401, 403, 429, 451, 999}  # sites that refuse automated clients: not evidence of a dead link
GITHUB_REPO = re.compile(r"https://github\.com/([^/\s)>\]]+)/([^/\s)>\]#?]+)")
PIN = re.compile(r"github\.com/([^/\s]+)/([^/\s]+)/(?:blob|tree)/([0-9a-f]{40})\b")


def extract_urls(text: str) -> set[str]:
    """External URLs in Markdown/plain text; trailing punctuation stripped; placeholders and local hosts dropped."""
    urls = set()
    for raw in URL.findall(text):
        url = raw.rstrip(".,;:!?*_")
        while url.endswith(")") and url.count("(") < url.count(")"):
            url = url[:-1]
        host = url.split("/")[2].split(":")[0].lower() if url.count("/") >= 2 else ""
        if not host or host in SKIP_HOSTS or "{" in url or "$" in url or "…" in url or "..." in url:
            continue
        urls.add(url)
    return urls


def classify(status: int | None, error: str | None) -> str:
    """ok / blocked / transient / dead for one probe result."""
    if error is not None:
        return "dead" if error in ("dns", "refused") else "transient"
    if status is None:
        return "transient"
    if status < 400:
        return "ok"
    if status in BLOCKED:
        return "blocked"
    if status in (404, 410):
        return "dead"
    return "transient"  # 5xx, 408, other 4xx: look again next week before calling it dead


def probe(url: str) -> tuple[int | None, str | None]:
    """(status, error-kind). HEAD first, GET when the server dislikes HEAD."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.status, None
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (400, 403, 404, 405, 501):
                continue
            return e.code, None
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                return None, "dns"
            if isinstance(e.reason, ConnectionRefusedError):
                return None, "refused"
            return None, "other"
        except (TimeoutError, OSError):
            return None, "other"
    return None, "other"


def collect_urls() -> dict[str, list[str]]:
    """url -> files that mention it."""
    found: dict[str, list[str]] = {}
    files = sorted((ROOT / "kb").rglob("*.md")) + [ROOT / "sources.txt"]
    for f in files:
        for u in extract_urls(f.read_text(encoding="utf-8")):
            found.setdefault(u, []).append(f.relative_to(ROOT).as_posix())
    return found


def check_links() -> tuple[str, int]:
    urls = collect_urls()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(urls, pool.map(probe, urls)))
    groups: dict[str, list[tuple[str, str]]] = {"dead": [], "transient": [], "blocked": []}
    for url, (status, err) in results.items():
        kind = classify(status, err)
        if kind != "ok":
            groups[kind].append((url, str(status) if status else err or "?"))
    lines = [f"Checked {len(urls)} external URLs from `kb/` and `sources.txt`.", ""]
    if groups["dead"]:
        lines += ["## Dead (404, 410 or unresolvable)", ""]
        lines += [f"- {u} ({s}) in {', '.join(f'`{p}`' for p in urls[u][:3])}" for u, s in sorted(groups["dead"])]
        lines.append("")
    if groups["transient"]:
        lines += ["## Failed this run (5xx, timeout, other); recheck next week", ""]
        lines += [f"- {u} ({s})" for u, s in sorted(groups["transient"])]
        lines.append("")
    lines.append(f"Refused automated clients (not counted as dead): {len(groups['blocked'])}.")
    return "\n".join(lines) + "\n", len(groups["dead"])


def api(path: str) -> dict:
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def pins() -> dict[tuple[str, str], str]:
    """(owner, repo) -> the pinned commit that appears most often in kb/ citations."""
    counts: dict[tuple[str, str], dict[str, int]] = {}
    for f in (ROOT / "kb").rglob("*.md"):
        for owner, repo, sha in PIN.findall(f.read_text(encoding="utf-8")):
            c = counts.setdefault((owner.lower(), repo.lower()), {})
            c[sha] = c.get(sha, 0) + 1
    return {k: max(v, key=v.get) for k, v in counts.items()}


def tracked_repos() -> list[tuple[str, str]]:
    seen: dict[tuple[str, str], tuple[str, str]] = {}
    for line in (ROOT / "sources.txt").read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("#") and "MANUAL" not in line:
            continue
        for owner, repo in GITHUB_REPO.findall(line):
            repo = repo.removesuffix(".git")
            seen.setdefault((owner.lower(), repo.lower()), (owner, repo))
    return sorted(seen.values())


def check_repos() -> tuple[str, int]:
    pinned = pins()
    rows, errors = [], []
    for owner, repo in tracked_repos():
        try:
            info = api(f"/repos/{owner}/{repo}")
            branch = info["default_branch"]
            sha = pinned.get((owner.lower(), repo.lower()))
            if sha:
                cmp = api(f"/repos/{owner}/{repo}/compare/{sha}...{branch}")
                rows.append((cmp["ahead_by"], f"{owner}/{repo}", f"pinned `{sha[:10]}`, {cmp['ahead_by']} commit(s) behind `{branch}`, last push {info['pushed_at'][:10]}"))
            else:
                rows.append((-1, f"{owner}/{repo}", f"no pinned commit in `kb/`, last push {info['pushed_at'][:10]}"))
        except urllib.error.HTTPError as e:
            errors.append(f"- {owner}/{repo}: HTTP {e.code} ({'repository gone or private' if e.code == 404 else 'API error'})")
        except (urllib.error.URLError, TimeoutError, KeyError) as e:
            errors.append(f"- {owner}/{repo}: {e}")
    moved = sorted((r for r in rows if r[0] > 0), reverse=True)
    lines = [f"Checked {len(rows) + len(errors)} GitHub repos listed in `sources.txt`; "
             f"{sum(1 for r in rows if r[0] >= 0)} have a commit pinned in `kb/`.", ""]
    if moved:
        lines += ["## Pinned sources whose repository has moved on", "",
                  "Re-read the changed docs, update the affected pages and their dates, then re-pin the commit.", ""]
        lines += [f"- [{name}](https://github.com/{name}): {text}" for _, name, text in moved]
        lines.append("")
    if errors:
        lines += ["## Could not be checked", ""] + errors + [""]
    return "\n".join(lines) + "\n", len(moved) + len(errors)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("check", choices=("links", "repos"))
    ap.add_argument("--out", help="write the Markdown report here")
    args = ap.parse_args()
    report, findings = check_links() if args.check == "links" else check_repos()
    if args.out:
        pathlib.Path(args.out).write_text(report, encoding="utf-8")
    print(report)
    print(f"FINDINGS={findings}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"findings={findings}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
