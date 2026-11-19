#!/usr/bin/env python3
# ABOUTME: Smoke-checks a built okf-loom site before it is published: every local href/src resolves to a file,
# ABOUTME: and the graph is not empty. Usage: python3 check_site.py public   (exit 1 on any failure)
"""A green build is not a working site: okf-loom happily links to section pages it never generates."""
import json
import pathlib
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.targets.append(value)


def broken_links(site: pathlib.Path) -> list[str]:
    """Local links (no scheme, not a fragment) whose target file is missing from the built site."""
    broken = []
    for page in sorted(site.rglob("*.html")):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for target in parser.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:  # external, protocol-relative, or #fragment only
                continue
            path = unquote(url.path)
            resolved = (site / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
            if path.endswith("/") or resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.resolve().is_file():
                broken.append(f"{page.relative_to(site)} -> {target}")
    return broken


def concept_count(site: pathlib.Path) -> int:
    graph = json.loads((site / "__data" / "graph.json").read_text(encoding="utf-8"))
    return len(graph.get("nodes", []))


def main(site: pathlib.Path) -> int:
    failures = [f"broken link: {b}" for b in broken_links(site)]
    nodes = concept_count(site)
    if nodes == 0:
        failures.append("graph has 0 concepts: the site would publish an empty graph")
    for f in failures:
        print(f"FAIL {f}")
    print(f"{'FAIL' if failures else 'OK'}: {nodes} concepts, {len(failures)} problem(s) in {site}")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or not pathlib.Path(sys.argv[1], "index.html").is_file():
        sys.exit("usage: check_site.py <built-site-dir containing index.html>")
    sys.exit(main(pathlib.Path(sys.argv[1])))
