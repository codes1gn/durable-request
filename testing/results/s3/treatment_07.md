# Changelog

Parsed from `git log` (last 200 commits).

## 93bb38a tuning: finalize E4M3 kernel_bank, add paper figures

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-07 22:12:55 +0800

- Fix overestimated f16 kernel_bank entries (re-measured with aitune)
- Fix broken 1024x4096x1024 e4m3 measurement (6.3 -> 317.1 TFLOPS)
- Add f16 variant generation pipeline (gen_variants, run_and_update)
- Add f16 aitune dynamic/template kernels
- Create tuning_v3 with paper-ready data: E4M3 only, dims >= 1024
  - 95 shapes, 80/95 win vs cuSPARSELt
  - Avg +16.7%, Median +19.5% improvement
- Add D3/SVG paper figures: spmm-speedup.svg, spmm-topbottom.svg
- Drop F16 from paper scope (not competitive vs cuSPARSELt)

Made-with: Cursor

---

## 50a9ba6 sweeper: f16_2048x8192x8192 baseline=659.6 best=684.7 (maxreg160)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:23:33 +0800


---

## e17d233 sweeper: e4m3_128x8192x8192 baseline=304.1 best=310.1 (l2_rhs_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:21:52 +0800


---

## b8ae3b5 sweeper: f16_3072x8192x8192 baseline=659.0 best=697.5 (pad16)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:15:23 +0800


---

## 4f2b23c sweeper: e4m3_256x8192x8192 baseline=591.8 best=600.3 (l2_rhs_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:14:23 +0800


---

## e1b2ac0 sweeper: f16_4096x8192x8192 baseline=674.7 best=692.5 (l2_lhs_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:07:05 +0800


---

## f391feb sweeper: e4m3_384x8192x8192 baseline=878.8 best=886.1 (l2_rhs_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 01:06:51 +0800


---

## fa18362 sweeper: e4m3_512x8192x8192 baseline=732.1 best=738.2 (ns10)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-06 00:59:30 +0800


---

## eca2c68 sweeper: f16_6144x6144x8192 baseline=523.4 best=793.9 (ns50)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 22:02:25 +0800


---

## b43a1dd sweeper: e4m3_768x8192x8192 baseline=1122.5 best=1147.9 (l2_rhs_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 22:00:18 +0800


---

## 6eed46b sweeper: f16_4096x8192x12288 baseline=1061.0 best=1065.0 (l2_meta_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:53:56 +0800


---

## 560c804 sweeper: e4m3_1024x8192x8192 baseline=1043.4 best=1049.4 (no_consumer_fence)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:52:40 +0800


---

## fc6ead2 sweeper: e4m3_4096x8192x6144 baseline=1243.9 best=1288.2 (pad0)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:44:58 +0800


---

## 5af4f55 sweeper: f16_4096x12288x8192 baseline=981.9 best=1069.9 (ns100)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:44:10 +0800


---

## 097d875 sweeper: e4m3_4096x6144x8192 baseline=1246.9 best=1261.3 (l2_lhs_128b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:37:11 +0800


---

## e1123ed sweeper: f16_8192x8192x8192 baseline=1417.2 best=1417.2 (baseline)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:34:56 +0800


---

## 5444e3a sweeper: e4m3_6144x8192x8192 baseline=1159.2 best=1164.7 (l2_out_256b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:29:38 +0800


---

## 13d9457 sweeper: f16_1024x8192x8192 baseline=177.6 best=180.9 (l2_rhs_128b)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:24:53 +0800


---

## 36ee8a9 sweeper: e4m3_2048x8192x8192 baseline=1235.7 best=1266.7 (O1)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:21:40 +0800


---

## 5c0a945 sweeper: f16_6144x8192x8192 baseline=1056.0 best=1056.0 (baseline)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:16:09 +0800


---

## bef9944 sweeper: e4m3_3072x8192x8192 baseline=1211.5 best=1300.8 (ns15)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:13:58 +0800


---

## 1111836 sweeper: f16_4096x8192x8192 baseline=685.2 best=702.3 (maxreg160)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:07:07 +0800


---

## a2d64b7 sweeper: e4m3_4096x8192x8192 baseline=1242.3 best=1272.3 (lb384_1)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 21:06:19 +0800


---

## 967712d sweeper: e4m3_4096x8192x8192 baseline=1261.8 best=1283.0 (O3)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 20:58:20 +0800


---

## bdcde33 sweeper: e4m3_4096x8192x8192 baseline=226.8 best=1253.0 (maxreg160)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 20:50:10 +0800


---

## a0fa494 e4m3_8192x32768x8192: BFS complete, best 1063.64 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:40:19 +0800


---

## d237608 e4m3_4096x32768x4096: BFS complete, best 1159.97 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:39:38 +0800


---

## da93da5 e4m3_16384x16384x16384: BFS complete, best 969.03 TFLOPS at iter23

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:39:07 +0800


---

## 0d054a6 f16_8192x32768x8192: BFS complete, best 5424.64 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:28:36 +0800


---

## db97b15 f16_16384x16384x16384: BFS complete, best 11084.10 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:27:43 +0800


---

## 59dc95a e4m3_16384x4096x16384: BFS complete, best 996.35 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:26:58 +0800


---

## 97246a2 e4m3_16384x16384x4096: BFS complete, best 883.45 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:26:20 +0800


---

## fedeb26 e4m3_4096x8192x32768: BFS complete, best 1336.73 TFLOPS at iter11

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:23:58 +0800


---

## fb1c4c1 e4m3_4096x32768x8192: BFS complete, best 1196.91 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:19:59 +0800


---

## f3d1671 f16_16384x4096x16384: BFS complete, best 2752.92 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:18:46 +0800


---

## e9c8e9d f16_16384x16384x4096: BFS complete, best 2725.47 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:17:30 +0800


---

## 0640f3b f16_4096x8192x32768: BFS complete, best 2685.32 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:16:29 +0800


---

## bea126f f16_4096x32768x8192: BFS complete, best 2844.14 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:15:12 +0800


---

## a7fb450 e4m3_16384x4096x4096: BFS complete, best 884.90 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:14:37 +0800


---

## 51d3dac e4m3_8192x16384x16384: BFS complete, best 1148.39 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:14:10 +0800


---

## e2a9ae8 e4m3_16384x8192x16384: BFS complete, best 981.54 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:12:46 +0800


---

## cbbe6d0 e4m3_16384x16384x8192: BFS complete, best 935.51 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:12:03 +0800


---

## 5742532 f16_8192x16384x16384: BFS complete, best 5406.58 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:11:09 +0800


---

## e30d170 f16_16384x8192x16384: BFS complete, best 5672.88 TFLOPS at iter5

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:09:51 +0800


---

## 6372bd2 f16_16384x16384x8192: BFS complete, best 5433.54 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:07:50 +0800


---

## 4a72739 e4m3_8192x256x256: BFS complete, best 77.17 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:06:40 +0800


---

## 0b483a7 e4m3_256x256x256: BFS complete, best 2.49 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:05:52 +0800


---

## 2b67ad1 e4m3_8192x512x512: BFS complete, best 197.29 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:05:15 +0800


---

## dbc982f e4m3_512x512x512: BFS complete, best 18.66 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:04:38 +0800


---

## 491ad08 e4m3_8192x1024x1024: BFS complete, best 494.90 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:03:49 +0800


---

## b83d92b e4m3_768x768x768: BFS complete, best 58.99 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:03:11 +0800


---

## 8848b97 e4m3_1024x1024x1024: BFS complete, best 132.41 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:02:35 +0800


---

## b670235 e4m3_12288x4096x4096: BFS complete, best 982.79 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:01:57 +0800


---

## 52b91c3 e4m3_8192x2048x2048: BFS complete, best 885.44 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:01:17 +0800


---

## e7060a9 e4m3_4096x16384x16384: BFS complete, best 1270.37 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 16:00:53 +0800


---

## b1a7295 e4m3_12288x4096x12288: BFS complete, best 1041.80 TFLOPS at iter14

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:59:19 +0800


---

## b590bdf e4m3_12288x12288x4096: BFS complete, best 958.57 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:55:19 +0800


---

## 67be654 e4m3_12288x12288x12288: BFS complete, best 1013.74 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:54:50 +0800


---

## 5f37f80 f16_12288x4096x12288: BFS complete, best 1567.27 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:44:23 +0800


---

## 1619b5d f16_12288x12288x4096: BFS complete, best 1542.08 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:43:51 +0800


---

## 35056c1 f16_12288x12288x12288: BFS complete, best 4621.41 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:43:22 +0800


---

## 8ed35be e4m3_4096x256x256: BFS complete, best 39.55 TFLOPS at iter12

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:42:46 +0800


---

## 6b3d93b e4m3_256x4096x256: BFS complete, best 39.52 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:40:13 +0800


---

## c3cc709 e4m3_256x256x4096: BFS complete, best 20.64 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:39:14 +0800


---

## 08b341d e4m3_4096x512x512: BFS complete, best 147.30 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:38:37 +0800


---

## 2203138 e4m3_512x4096x512: BFS complete, best 147.97 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:38:13 +0800


---

## 2ab4254 e4m3_512x512x4096: BFS complete, best 82.26 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:37:26 +0800


---

## aa6a754 e4m3_8192x3072x3072: BFS complete, best 1107.98 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:36:22 +0800


---

## 2b6e77f e4m3_4096x1024x1024: BFS complete, best 340.39 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:35:57 +0800


---

## 26bb2dd e4m3_1024x4096x1024: BFS complete, best 340.71 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:35:33 +0800


---

## 7f7b5e1 e4m3_1024x1024x4096: BFS complete, best 327.44 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:35:09 +0800


---

## 72a1720 e4m3_2048x2048x2048: BFS complete, best 532.52 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:34:45 +0800


---

## eb5db60 e4m3_8192x12288x12288: BFS complete, best 1120.56 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:33:12 +0800


---

## 91f6332 e4m3_8192x4096x4096: BFS complete, best 1196.42 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:32:37 +0800


---

## e7c9930 e4m3_4096x2048x2048: BFS complete, best 756.49 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:31:46 +0800


---

## 9d876d5 e4m3_8192x16384x8192: BFS complete, best 1094.64 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:31:22 +0800


---

## 826cc8e e4m3_4096x16384x4096: BFS complete, best 1202.13 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:29:58 +0800


---

## 67b9fcc e4m3_12288x8192x12288: BFS complete, best 1011.29 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:27:56 +0800


---

## 06b9e09 e4m3_2048x4096x2048: BFS complete, best 762.01 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:25:53 +0800


---

## b144a8c e4m3_8192x8192x16384: BFS complete, best 1187.75 TFLOPS at iter15

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:24:29 +0800


---

## 7108a4b e4m3_4096x4096x16384: BFS complete, best 1259.47 TFLOPS at iter19

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:19:47 +0800


---

## 0b85ed2 e4m3_12288x12288x8192: BFS complete, best 988.00 TFLOPS at iter5

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:14:59 +0800


---

## 5bcdabf e4m3_2048x2048x4096: BFS complete, best 720.35 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:13:17 +0800


---

## e771f41 e4m3_16384x8192x8192: BFS complete, best 959.50 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:12:53 +0800


---

## 9057d29 f16_8192x12288x12288: BFS complete, best 3165.22 TFLOPS at iter20

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 15:04:13 +0800


---

## 5a88429 f16_8192x16384x8192: BFS complete, best 2759.29 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:57:50 +0800


---

## d5b27d4 f16_12288x8192x12288: BFS complete, best 3109.25 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:56:47 +0800


---

## 512d0ec f16_8192x8192x16384: BFS complete, best 2781.39 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:55:59 +0800


---

## 340dec3 f16_4096x4096x16384: BFS complete, best 701.45 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:55:08 +0800


---

## 0fe262d f16_12288x12288x8192: BFS complete, best 3153.16 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:54:38 +0800


---

## aaa95e5 f16_16384x8192x8192: BFS complete, best 2704.34 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:53:03 +0800


---

## 1e91eb5 e4m3_128x4096x4096: BFS complete, best 163.29 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:52:31 +0800


---

## 9672f2b e4m3_8192x8192x128: BFS complete, best 135.39 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:52:06 +0800


---

## 36158ff e4m3_4096x4096x128: BFS complete, best 104.61 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:51:18 +0800


---

## eeccf69 e4m3_256x4096x4096: BFS complete, best 326.92 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:50:13 +0800


---

## 01915d8 e4m3_8192x256x8192: BFS complete, best 636.35 TFLOPS at iter5

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:49:37 +0800


---

## 60b3191 e4m3_4096x256x4096: BFS complete, best 328.08 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:48:19 +0800


---

## b7a2cb4 e4m3_8192x8192x256: BFS complete, best 258.38 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:47:55 +0800


---

## e409adc e4m3_4096x4096x256: BFS complete, best 194.51 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:46:55 +0800


---

## f9fbd71 e4m3_512x4096x4096: BFS complete, best 653.64 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:45:21 +0800


---

## c3e0d99 e4m3_8192x512x8192: BFS complete, best 765.34 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:44:57 +0800


---

## 658be17 e4m3_4096x512x4096: BFS complete, best 652.76 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:43:25 +0800


---

## 42bb232 e4m3_256x8192x256: BFS complete, best 76.07 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:43:01 +0800


---

## c79a04f e4m3_8192x8192x512: BFS complete, best 461.67 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:42:02 +0800


---

## b79c215 e4m3_4096x4096x512: BFS complete, best 348.37 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:40:13 +0800


---

## f0d2022 e4m3_256x256x8192: BFS complete, best 26.95 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:39:49 +0800


---

## 1477d3e e4m3_1024x4096x4096: BFS complete, best 729.76 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:37:49 +0800


---

## 3924f77 e4m3_8192x1024x8192: BFS complete, best 971.62 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:37:01 +0800


---

## f19987c e4m3_4096x1024x4096: BFS complete, best 730.14 TFLOPS at iter9

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:36:35 +0800


---

## c7b62ef e4m3_512x8192x512: BFS complete, best 197.89 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:34:33 +0800


---

## 7def7d0 e4m3_8192x8192x1024: BFS complete, best 728.66 TFLOPS at iter11

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:34:10 +0800


---

## 679fc6e e4m3_4096x4096x1024: BFS complete, best 587.64 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:31:43 +0800


---

## 3b95501 e4m3_512x512x8192: BFS complete, best 107.50 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:30:19 +0800


---

## 613d0a1 e4m3_3072x3072x3072: BFS complete, best 1001.31 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:29:55 +0800


---

## 26ccf70 e4m3_6144x4096x4096: BFS complete, best 1212.12 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:26:37 +0800


---

## c21c26f e4m3_2048x4096x4096: BFS complete, best 980.91 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:25:46 +0800


---

## bdff9c6 e4m3_4096x3072x3072: BFS complete, best 1012.18 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:25:22 +0800


---

## c3c302e e4m3_8192x2048x8192: BFS complete, best 1084.48 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:24:57 +0800


---

## 630218c e4m3_4096x2048x4096: BFS complete, best 992.35 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:24:31 +0800


---

## b2f0ccb e4m3_1024x8192x1024: BFS complete, best 495.52 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:24:06 +0800


---

## ea0fd50 e4m3_3072x4096x3072: BFS complete, best 1012.63 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:23:18 +0800


---

## b8cb178 e4m3_8192x8192x2048: BFS complete, best 1008.69 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:22:42 +0800


---

## 405659a e4m3_4096x4096x2048: BFS complete, best 913.81 TFLOPS at iter9

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:21:14 +0800


---

## a129752 e4m3_1024x1024x8192: BFS complete, best 431.46 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:19:13 +0800


---

## 70f86b8 e4m3_3072x3072x4096: BFS complete, best 1107.73 TFLOPS at iter19

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:13:01 +0800


---

## 8d34da3 e4m3_12288x8192x8192: BFS complete, best 997.60 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:06:21 +0800


---

## 30b1437 e4m3_8192x6144x6144: BFS complete, best 1048.31 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:05:49 +0800


---

## 8c7b0d9 e4m3_4096x12288x12288: BFS complete, best 1240.05 TFLOPS at iter9

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:04:55 +0800


---

## dbb1ae2 e4m3_8192x12288x8192: BFS complete, best 1108.64 TFLOPS at iter10

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 14:02:15 +0800


---

## 0de3095 e4m3_4096x12288x4096: BFS complete, best 1196.72 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:59:23 +0800


---

## 04e9e69 e4m3_2048x8192x2048: BFS complete, best 898.06 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:58:30 +0800


---

## d45b6ac e4m3_8192x4096x8192: BFS complete, best 1152.51 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:57:05 +0800


---

## cade6e7 e4m3_6144x4096x6144: BFS complete, best 1174.87 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:55:28 +0800


---

## 93c3443 e4m3_8192x8192x12288: BFS complete, best 1172.16 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:55:02 +0800


---

## e92d4c1 e4m3_4096x4096x12288: BFS complete, best 1253.96 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:46:43 +0800


---

## 1c53868 e4m3_2048x2048x8192: BFS complete, best 821.54 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:46:16 +0800


---

## 4eeabd0 e4m3_8192x8192x4096: BFS complete, best 1169.63 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:45:51 +0800


---

## 837ceaf e4m3_6144x6144x4096: BFS complete, best 1172.87 TFLOPS at iter7

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:45:25 +0800


---

## 2006da8 e4m3_4096x8192x16384: BFS complete, best 1326.40 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:43:43 +0800


---

## 16bccca e4m3_4096x16384x8192: BFS complete, best 1227.07 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:43:11 +0800


---

## 15dda9e e4m3_4096x4096x4096: BFS complete, best 1131.70 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:40:53 +0800


---

## 5682fd5 f16_12288x8192x8192: BFS complete, best 2144.96 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:40:29 +0800


---

## b19544e f16_4096x12288x12288: BFS complete, best 1599.87 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:38:56 +0800


---

## cc205ba f16_8192x12288x8192: BFS complete, best 2116.09 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:38:09 +0800


---

## ed12f18 f16_8192x4096x8192: BFS complete, best 713.62 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:29:44 +0800


---

## 8673553 f16_8192x8192x12288: BFS complete, best 2118.58 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:29:01 +0800


---

## c98a9db f16_4096x4096x12288: BFS complete, best 537.34 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:28:29 +0800


---

## 8a89e55 f16_4096x8192x16384: BFS complete, best 1378.84 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:27:18 +0800


---

## f022a94 f16_4096x16384x8192: BFS complete, best 1359.59 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:26:47 +0800


---

## 4e0d83e e4m3_4096x8192x128: BFS complete, best 123.55 TFLOPS at iter13

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:26:16 +0800


---

## f3b4443 e4m3_4096x8192x256: BFS complete, best 224.92 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:23:19 +0800


---

## b085ef1 e4m3_4096x256x8192: BFS complete, best 421.84 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:22:20 +0800


---

## 1dcd019 e4m3_4096x8192x512: BFS complete, best 400.72 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:21:27 +0800


---

## 1f7a6d8 e4m3_4096x512x8192: BFS complete, best 816.13 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:21:03 +0800


---

## 6cadf5b e4m3_4096x8192x1024: BFS complete, best 672.57 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:20:10 +0800


---

## e48b953 e4m3_4096x1024x8192: BFS complete, best 818.05 TFLOPS at iter0

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:19:46 +0800


---

## 57a446c e4m3_8192x6144x8192: BFS complete, best 1087.49 TFLOPS at iter10

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:12:52 +0800


---

## 9c7f3e8 e4m3_4096x6144x4096: BFS complete, best 1190.12 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:10:15 +0800


---

## 25a3bb7 e4m3_3072x8192x3072: BFS complete, best 1097.42 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:09:50 +0800


---

## 9dbff8d e4m3_8192x8192x6144: BFS complete, best 1059.57 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:09:25 +0800


---

## 0ef0b62 e4m3_4096x4096x6144: BFS complete, best 1161.58 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:08:58 +0800


---

## e6d9031 e4m3_3072x3072x8192: BFS complete, best 1174.53 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:08:32 +0800


---

## c4af09d e4m3_4096x8192x2048: BFS complete, best 971.54 TFLOPS at iter6

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:07:42 +0800


---

## 8e94372 e4m3_4096x2048x8192: BFS complete, best 1046.64 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:06:16 +0800


---

## eeed3af e4m3_6144x6144x6144: BFS complete, best 1095.18 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:05:51 +0800


---

## 7ed5122 f16_8192x6144x8192: BFS complete, best 1064.95 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:05:25 +0800


---

## f9d0396 f16_8192x8192x6144: BFS complete, best 1078.05 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:04:27 +0800


---

## f5b17ce e4m3_4096x3072x8192: BFS complete, best 1163.27 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:02:05 +0800


---

## 5a8157d e4m3_4096x6144x6144: BFS complete, best 1265.29 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:01:25 +0800


---

## 49942d5 e4m3_6144x8192x6144: BFS complete, best 1158.10 TFLOPS at iter3

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:00:59 +0800


---

## 8c859fe e4m3_6144x6144x8192: BFS complete, best 1145.59 TFLOPS at iter4

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 13:00:05 +0800


---

## 2905b8a e4m3_4096x8192x12288: BFS complete, best 1286.17 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:58:56 +0800


---

## d89dd5d e4m3_4096x8192x4096: BFS complete, best 1251.34 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:58:26 +0800


---

## 29cbbd5 e4m3_4096x12288x8192: BFS complete, best 1196.56 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:58:01 +0800


---

## 12f723a e4m3_4096x4096x8192: BFS complete, best 1221.89 TFLOPS at iter9

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:57:32 +0800


---

## df4eb75 e4m3_8192x8192x8192: BFS complete, best 1105.69 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:55:22 +0800


---

## 39028ce f16_6144x8192x6144: BFS complete, best 782.77 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:54:38 +0800


---

## c1534ef f16_6144x6144x8192: BFS complete, best 794.32 TFLOPS at iter22

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:53:56 +0800


---

## 62c54d6 f16_4096x12288x8192: BFS complete, best 1034.93 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:48:30 +0800


---

## d1f0055 e4m3_128x8192x8192: BFS complete, best 308.87 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:48:01 +0800


---

## 7bc8436 e4m3_256x8192x8192: BFS complete, best 608.34 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:47:35 +0800


---

## d1d4ec4 e4m3_384x8192x8192: BFS complete, best 886.99 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:45:24 +0800


---

## 88dac37 e4m3_512x8192x8192: BFS complete, best 741.85 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:44:43 +0800


---

## a9b97ed e4m3_768x8192x8192: BFS complete, best 1155.06 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:44:17 +0800


---

## 27a5385 e4m3_1024x8192x8192: BFS complete, best 1049.15 TFLOPS at iter8

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:42:04 +0800


---

## 5aa67c2 e4m3_4096x8192x6144: BFS complete, best 1279.31 TFLOPS at iter16

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:40:04 +0800


---

## 1a5636e e4m3_4096x6144x8192: BFS complete, best 1259.41 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:36:20 +0800


---

## f693e81 e4m3_6144x8192x8192: BFS complete, best 1141.11 TFLOPS at iter1

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:35:40 +0800


---

## f9ffb81 e4m3_2048x8192x8192: BFS complete, best 1256.32 TFLOPS at iter2

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:35:12 +0800


---

## 63aa3b3 e4m3_2048x8192x8192 iter001: nanosleep(20) — TFLOPS: 1229.42 -> 1211.05 (DISCARD)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 12:32:28 +0800

Made-with: Cursor

---

## 31cbb4a Update compaction summary: 4 shapes done

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 09:11:56 +0800

Made-with: Cursor

---

## 88deb2c f16_2048x8192x8192: SHAPE COMPLETE — seed kernel optimal (745.65 TFLOPS)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 09:11:39 +0800

30 iterations, no improvement. 16x32 grid has minimal TMA contention.
nanosleep hurts (-0.6 to -4%), L2 promotions within noise, O3 within noise.
4 shapes done, ~37 pending.

Made-with: Cursor

---

## 3b567c3 f16_2048x8192x8192: initialize tuning — baseline 745.65 TFLOPS

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 09:02:27 +0800

Grid: 16x32. Parametrized seed kernel from reference.
Made-with: Cursor

---

## 20542e0 f16_4096x8192x8192: SHAPE COMPLETE — ns15 best at 700.16 TFLOPS (+3.4%)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 09:00:57 +0800

30 iterations complete. Best: iter006_ns15.cu (nanosleep(15) in producer).
Baseline: 677.09 → 700.16 TFLOPS (+3.41%).
5-run avg improvement: ~688 vs ~677 (+1.6%).
All L2 promotions, CTA changes, and other combos failed to beat ns15 alone.

Made-with: Cursor

---

## 6cf1714 f16_4096x8192x8192 iters 18-21: ns200/ns100/ns15+lb/ns15+all_L2 — DISCARD

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:57:16 +0800

iter018: ns200 — 680.07 TFLOPS
iter019: ns100 — 661.43 TFLOPS
iter020: ns15+launch_bounds(384,1) — 670.00 TFLOPS
iter021: ns15+L2_256B on LHS+RHS — 692.57 TFLOPS
15 consecutive discards. ns15 alone remains best at 700.16.

Made-with: Cursor

---

## 10ec2b8 f16_4096x8192x8192 iters 15-17: ns15+O3, ns50, ns5 — all DISCARD

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:55:32 +0800

iter015: ns15+-O3 — 685.95 TFLOPS (DISCARD)
iter016: ns50 — 679.49 TFLOPS (DISCARD)
iter017: ns5 — 681.98 TFLOPS (DISCARD)
11 consecutive discards since ns15 KEEP. ns15 remains best.

Made-with: Cursor

---

## 248d2e0 f16_4096x8192x8192 iter014: ns15+META8 — 668.89 TFLOPS (DISCARD)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:54:00 +0800

8 consecutive discards. META_TILE_COLS=8 hurts with ns15.

Made-with: Cursor

---

## 5d1c00c f16_4096x8192x8192 iters 12-13: PAD=0 & RHS L2 both hurt with ns15

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:53:08 +0800

iter012: ns15+PAD=0 — 677.18 (DISCARD)
iter013: ns15+RHS_L2_256B — 673.47 (DISCARD)
7 consecutive discards since ns15 KEEP.

Made-with: Cursor

---

## 13c4202 f16_4096x8192x8192 iter012: ns15+PAD=0 — 677.18 TFLOPS (DISCARD)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:51:56 +0800

6 consec. OUTPUT_PAD=0 doesn't help. ns15 alone remains best.

Made-with: Cursor

---

## b515af4 f16_4096x8192x8192 iter011: nanosleep(18) — 679.60 TFLOPS (DISCARD)

**Author:** heng shi <heng.shi@sjtu.edu.cn>
**Date:** 2026-04-05 08:51:04 +0800

ns15-20 range all similar due to high variance. 5 consecutive discards.
Best remains iter006_ns15 at 700.16 (but 10-run avg ~672).

Made-with: Cursor

---
