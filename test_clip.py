# ABOUTME: Minimal assert-based checks for clip.py link rewriting and GitHub URL detection.
# ABOUTME: Run: python3 test_clip.py
from clip import GITHUB, rewrite_links

plan = {"docs/A.md": "docs/A.md", "recipes/r.json": "recipes/r.json.md", "img/x.png": "img/x.png"}
B = "https://github.com/o/r/blob/abc"
t = rewrite_links("[a](A.md#s) [r](../recipes/r.json) ![i](../img/x.png) [s](../run.py) [w](https://x.io) [h](#top)",
                  "docs/A.md", plan, B)
assert t == ("[a](A.md#s) [r](../recipes/r.json.md) ![i](../img/x.png) "
             f"[s]({B}/run.py) [w](https://x.io) [h](#top)"), t
assert GITHUB.match("https://github.com/MiaAI-Lab/sparkring/blob/main/docs/BOOTSTRAP.md").groups() == ("MiaAI-Lab", "sparkring")
assert GITHUB.match("https://github.com/FujitsuPolycom/sparkcache.git").groups() == ("FujitsuPolycom", "sparkcache")
assert not GITHUB.match("https://docs.nvidia.com/dgx/dgx-spark/index.html")
print("ok")
assert not GITHUB.match("https://github.com/vllm-project/vllm/issues/36821")  # issues/PRs are pages, not repo ingests
assert GITHUB.match("https://github.com/NVIDIA/dgx-spark-playbooks/tree/main/nvidia/dgx-dashboard")
print("ok2")

# free_path: same title from a different URL must never overwrite (multi-page articles)
import pathlib, tempfile
from clip import free_path
with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp)
    a = free_path(d, "Review", "https://x.io/review/")
    a.write_text('---\nsource: "https://x.io/review/"\n---\n')
    assert free_path(d, "Review", "https://x.io/review/") == a          # re-clip same URL: update in place
    b = free_path(d, "Review", "https://x.io/review/2/")
    assert b.name == "Review (2).md", b                                 # different URL: suffixed, a untouched
    b.write_text('---\nsource: "https://x.io/review/2/"\n---\n')
    assert free_path(d, "Review", "https://x.io/review/2/") == b
print("ok3")
