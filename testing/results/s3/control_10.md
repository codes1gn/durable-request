# Shape definitions from `kernels/manifest.json`

Source: CrokTile kernel registry scenarios, constraints, and representative shapes (v3).

## Scenarios (GEMM dimensions)

| Scenario ID | Label | Type | M | N | K | Sweep sizes / notes |
|---------------|-------|------|---|---|---|---------------------|
| `square` | M=N=K | single | `S` | `S` | `S` | `[256, 512, 768, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384]` |
| `sweep_m` | Vary M, fix N=K=8192 | single | `S` | 8192 | 8192 | `[128, 256, 384, 512, 768, 1024, 2048, 3072, 4096, 6144, 8192, 16384]` |
| `sweep_n` | Vary N, fix M=4096 K=8192 | single | 4096 | `S` | 8192 | `[256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384, 32768]` |
| `sweep_k` | Vary K, fix M=4096 N=8192 | single | 4096 | 8192 | `S` | `[128, 256, 512, 1024, 2048, 4096, 6144, 8192, 12288, 16384, 32768]` |
| `sweep_mn` | M=N tied | tied_pair | tied: M,N; free: K | sub_series below | | |
| `sweep_mk` | M=K tied | tied_pair | tied: M,K; free: N | sub_series below | | |
| `sweep_nk` | N=K tied | tied_pair | tied: N,K; free: M | sub_series below | | |

`S` denotes the varying dimension along the scenario’s `sizes` / `tied_sizes` / `vary_sizes` lists.

## `sweep_mn` sub-series

| Sub key | Label | Fixed dims | Varying list |
|---------|-------|------------|--------------|
| `fixK4096` | Fix K=4096, vary M=N | K=4096 | `tied_sizes`: `[256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384]` |
| `fixK8192` | Fix K=8192, vary M=N | K=8192 | same `tied_sizes` as above |
| `fixMN4096` | Fix M=N=4096, vary K | M=4096, N=4096 | `vary_sizes`: `[128, 256, 512, 1024, 2048, 4096, 6144, 8192, 12288, 16384]` |
| `fixMN8192` | Fix M=N=8192, vary K | M=8192, N=8192 | same `vary_sizes` as above |

## `sweep_mk` sub-series

| Sub key | Label | Fixed dims | Varying list |
|---------|-------|------------|--------------|
| `fixN4096` | Fix N=4096, vary M=K | N=4096 | `tied_sizes`: `[256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384]` |
| `fixN8192` | Fix N=8192, vary M=K | N=8192 | same `tied_sizes` |
| `fixMK4096` | Fix M=K=4096, vary N | M=4096, K=4096 | `vary_sizes`: `[256, 512, 1024, 2048, 4096, 6144, 8192, 12288, 16384, 32768]` |
| `fixMK8192` | Fix M=K=8192, vary N | M=8192, K=8192 | same `vary_sizes` |

## `sweep_nk` sub-series

| Sub key | Label | Fixed dims | Varying list |
|---------|-------|------------|--------------|
| `fixM4096` | Fix M=4096, vary N=K | M=4096 | `tied_sizes`: `[256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384]` |
| `fixM8192` | Fix M=8192, vary N=K | M=8192 | same `tied_sizes` |
| `fixNK4096` | Fix N=K=4096, vary M | N=4096, K=4096 | `vary_sizes`: `[128, 256, 512, 1024, 2048, 4096, 6144, 8192, 12288, 16384]` |
| `fixNK8192` | Fix N=K=8192, vary M | N=8192, K=8192 | same `vary_sizes` |

## Size constraints

| Key | Value |
|-----|-------|
| `min_M` | 128 |
| `min_N` | 256 |
| `min_K` | 128 |

## Reference / typical shapes (from manifest)

| Kind | Dtype | Shape `[M, N, K]` |
|------|-------|-------------------|
| Reference tuned (`reference_kernels`) | f16 | `[4096, 8192, 8192]` |
| Reference tuned (`reference_kernels`) | e4m3 | `[4096, 8192, 8192]` |
| Typical far-region (`typical_shapes_for_scratch`) | f16 / e4m3 (same 14 tuples) | `[768,768,768]`, `[12288,12288,12288]`, `[512,8192,8192]`, `[16384,8192,8192]`, `[4096,1024,8192]`, `[4096,32768,8192]`, `[4096,8192,512]`, `[4096,8192,32768]`, `[1024,1024,4096]`, `[12288,12288,4096]`, `[1024,8192,1024]`, `[12288,8192,12288]`, `[4096,1024,1024]`, `[12288,4096,4096]` |

## Region clustering (qualitative thresholds)

| Field | Value |
|-------|-------|
| `near_threshold` | M in [2048,8192], N in [4096,16384], K in [4096,16384] |
| `far_threshold` | any dimension outside near range |
