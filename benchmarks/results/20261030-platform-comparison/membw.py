# GPU memory bandwidth on a DGX Spark-class box: copy / read / write of 1 GiB buffers, CUDA-event timed.
import torch, statistics as st, platform
n = 1 << 30
a = torch.empty(n, dtype=torch.uint8, device="cuda"); b = torch.empty_like(a)
a.fill_(1); f = a.view(torch.float32)
def bench(fn, bytes_moved, it=30):
    for _ in range(5): fn()
    torch.cuda.synchronize(); r = []
    for _ in range(it):
        s, e = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
        s.record(); fn(); e.record(); e.synchronize(); r.append(bytes_moved / (s.elapsed_time(e) / 1e3) / 1e9)
    return st.median(r), max(r)
res = {
  "copy (rd+wr)": bench(lambda: b.copy_(a), 2 * n),
  "read (sum)":   bench(lambda: f.sum(), n),
  "write (fill)": bench(lambda: b.fill_(0), n),
}
print(platform.node(), torch.cuda.get_device_name(0), "torch", torch.__version__)
for k, (m, x) in res.items(): print(f"{k:14s} median {m:7.1f} GB/s   best {x:7.1f} GB/s")
