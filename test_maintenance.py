# ABOUTME: Assert-based checks for the pure functions in maintenance.py (no network): run `python3 test_maintenance.py`.
# ABOUTME: Covers URL extraction, probe classification and pinned-commit discovery.
import maintenance as m

# URL extraction: trailing punctuation, markdown wrappers, balanced parens, placeholders, local hosts.
text = (
    "See [docs](https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html). Also https://example.com/x, "
    "(https://en.wikipedia.org/wiki/Foo_(bar)) and `https://huggingface.co/blog/exolabs/the-dgx-spark-handbook`; "
    "local http://127.0.0.1:8000/v1 and http://<head>:8888/v1 and https://github.com/o/r/blob/{sha}/x are not sources."
)
urls = m.extract_urls(text)
assert "https://docs.vllm.ai/en/latest/serving/parallelism_scaling.html" in urls, urls
assert "https://en.wikipedia.org/wiki/Foo_(bar)" in urls, urls
assert "https://huggingface.co/blog/exolabs/the-dgx-spark-handbook" in urls, urls
assert not any("127.0.0.1" in u or "example.com" in u or "{sha}" in u or "<head>" in u for u in urls), urls
print("ok")

# Classification: only 404/410/DNS/refused count as dead; bot-blocking and server errors do not.
assert m.classify(200, None) == "ok" and m.classify(301, None) == "ok"
assert m.classify(404, None) == "dead" and m.classify(410, None) == "dead"
assert m.classify(403, None) == "blocked" and m.classify(429, None) == "blocked"
assert m.classify(503, None) == "transient" and m.classify(None, "other") == "transient"
assert m.classify(None, "dns") == "dead" and m.classify(None, "refused") == "dead"
print("ok2")

# Pinned commits are read from blob/tree URLs with a full 40-hex sha; the most frequent one wins.
sha_a, sha_b = "a" * 40, "b" * 40
assert m.PIN.findall(f"https://github.com/Foo/Bar/blob/{sha_a}/docs/x.md") == [("Foo", "Bar", sha_a)]
assert m.PIN.findall("https://github.com/Foo/Bar/blob/main/docs/x.md") == []
assert m.GITHUB_REPO.findall("https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/x") == [("NVIDIA", "dgx-spark-playbooks")]
print("ok3")
