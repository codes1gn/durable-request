================================================================================
# FILE: RESEARCH-PLAN.md
================================================================================

# CrokTile — Research Plan

## Title
**CrokTile: Compiler-Guided AI Auto-Tuning for High-Performance Structured Sparse GEMM on Hopper GPUs**

## Core Thesis

> AI-driven GPU kernel optimization systems operate on raw CUDA/Triton and
> discover resource violations only through expensive GPU measurements.
> CrokTile integrates a zero-cost abstraction DSL, compile-time resource
> modeling, and an agentic AI tuner that consumes compiler-emitted metadata
> as structured guardrails. This compiler-guided approach converges 5× faster
> than profiler-only agentic tuning: ~50 iterations and 10 minutes versus
> ~250 iterations and 50+ minutes for equivalent quality.

## Positioning (vs. Companion Papers)

| Aspect | gemm_sp_paper/ | ai-tune-croktile-paper/ | croktile_paper/ (this) |
|--------|---------------|------------------------|----------------------|
| Focus | Kernel optimization | AI agent + DSL design | AI auto-tune system design |
| Key claim | TFLOPS vs baselines | One request → SOTA | Compiler-guided 5× convergence |
| Innovation | Kernel algorithms | Zero-cost DSL + agent | Compiler stats as guardrails |
| Angle | HPC/systems | AI + SE | Systems + AI tuning |
| NCU | Used directly | Featured prominently | Hidden (compiler stats replace it) |
| Results style | Bar charts | Progression over time | Convergence + progression |

## Key Contributions

1. **Zero-cost abstraction DSL** — Compresses kernel source by 4× while
   compiling to expert-quality CUDA/CuTe. Raises information density per
   context token for AI agents. 353 compile-time hardware checks.

2. **Compile-time resource model** — Extracts register pressure, shared
   memory, pipeline depth, occupancy bounds as by-product of code generation.
   Prunes 30-40% of infeasible configurations. Roofline-occupancy ranking.

3. **Agentic AI tuner** — Consumes compiler metadata as guardrails for
   Bayesian search. Warm start from compiler ranking. Feasibility-enforced
   acquisition function. Converges 5× faster than profiler-only agents.

## Required Baselines

| # | Baseline | Type | Purpose |
|---|----------|------|---------|
| 1 | cuSPARSELt v0.8.1 | Vendor | Production baseline |
| 2 | Random search | Tuning | Lower bound |
| 3 | Black-box BO | Tuning | Classical baseline |
| 4 | Agent-only (profiler-based) | AI Tuning | State-of-art without compiler |
| 5 | Triton autotune | DSL | DSL baseline |

## Evaluation Dimensions

- Convergence speed: iterations to 95%/98% (compiler-guided vs profiler-only)
- Final TFLOPS vs cuSPARSELt
- Search space reduction via compile-time pruning
- Context engineering: token budget, history entries
- Ablation: pruning, scoring, agent individually
- Wall-clock tuning time end-to-end

## Hardware
- Primary: NVIDIA H800 PCIe (SM90, Hopper)
- CUDA 12.4, driver 550.54

## Project Structure

```
croktile_paper/
├── paper/
│   ├── main.tex              ← LaTeX source (ACM sigconf)
│   └── references.bib        ← BibTeX database
├── figures/
│   ├── src/                  ← Figure generation scripts (D3/SVG)
│   ├── out/                  ← Generated SVGs + PDFs
│   └── package.json
├── kernels/                  ← Kernel registry (completed best per shape)
│   ├── manifest.json         ← Scenarios, reference/baseline kernels, build config, region clustering
│   ├── gemm_sp_f16/          ← FP16 best kernels (one per shape, e.g. f16_4096x4096x4096_best.cu)
│   └── gemm_sp_e4m3/         ← FP8 E4M3 best kernels
├── tuning/                   ← All tuning artifacts (per-shape isolation)
│   ├── state.json            ← Global progress: which shapes are done/active/pending
│   ├── logs/<key>/           ← Per-shape results.tsv (key = <dtype>_<M>x<N>x<K>)
│   ├── srcs/<key>/           ← Per-shape kernel iterations (ALL kept)
│   ├── perf/<key>/           ← Per-shape timing + ncu outputs
│   └── checkpoints/<key>.json← Per-shape crash-safe checkpoint
├── ae/
│   ├── scripts/              ← Experiment automation
│   └── data/                 ← Convergence logs
├── .claude/skills/           ← AI tuning skills
│   ├── ai-tune-from-current-best/ ← Adapt reference best to all shapes (30 iter/shape, non-stop sweep)
│   └── ai-tune-from-scratch/      ← Deep-tune typical shapes from baseline (150 iter/shape, non-stop sweep)
├── .cursor/rules/            ← Agent behavior rules
├── Makefile
├── .gitignore
├── RESEARCH-PLAN.md          ← This file
└── literature-review.md      ← Literature survey
```

## Build Commands

```bash
# From croktile_paper/:
make paper            # compile LaTeX
make figures          # generate SVG figures
make svg2pdf          # convert SVGs to PDFs
make watch            # tectonic watch mode

# From workspace root (builds both papers):
make                  # compile both papers
make paper2           # croktile_paper only
```


================================================================================
# FILE: literature-review.md
================================================================================

# Literature Review: Compiler-Guided AI Auto-Tuning for GPU Kernels

## 1. GPU Kernel DSLs and Zero-Cost Abstractions

### 1.1 CUTLASS and CuTe
CUTLASS 3.x introduces a five-layer abstraction hierarchy built on CuTe's
layout algebra. CuTe provides compile-time layout composition with zero
runtime overhead. The CuTe DSL (2025) extends this to Python via JIT.
**Gap:** 4,000+ tokens per kernel — impractical for LLM context windows.

### 1.2 Triton
Block-level programming model with LLVM backend. `@triton.autotune` supports
brute-force sweeping with optional user-defined pruning.
**Gap:** No compile-time occupancy feedback; pruning is user-defined, not compiler-derived.

### 1.3 TileLang
Explicit memory placement primitives. Carver-based template generation for
candidate ranking. Fewest LOC (22 for GEMM).
**Gap:** No resource-aware pruning; TVM backend limits Hopper feature access.

### 1.4 Hexcute
Automates layout synthesis via constraint programming. Demonstrates compile-time
reasoning about data layout as substitute for runtime exploration.

---

## 2. LLM-Driven Kernel Optimization

### 2.1 Agentic Systems
| System | Approach | Limitation |
|--------|----------|------------|
| CUDA Agent | Agentic RL, 6K training tasks | Raw CUDA, no compiler feedback |
| KernelSkill | Dual-level memory, skill library | Raw CUDA, no compile-time checks |
| KernelAgent | Hardware-profiling multi-agent loop | Profiler-only, no compile-time pruning |
| AutoKernel | Iterative agent-driven search | Triton/CUDA, profiler post-hoc only |
| Astra | Multi-agent (coding, testing, profiling) | Parallel sub-agents, expensive |
| KernelBlaster | Memory-augmented in-context RL | Knowledge base, no compiler integration |
| PRAGMA | Profiler-guided multi-agent | Closed feedback but no compile-time model |
| CudaForge | Coder + Judge agents | Hardware feedback but post-execution only |

### 2.2 Positioning of CrokTile
All prior LLM-driven systems operate on raw CUDA/Triton and discover resource
violations only through GPU execution. CrokTile's compiler-emitted metadata
(register pressure, shared memory, occupancy) enables pruning 30-40% of
candidates before any GPU measurement, providing a 5× convergence speedup
over profiler-only agents.

---

## 3. Classical Auto-Tuning

### 3.1 Cost-Model Approaches
- **Ansor/TVM:** Learned cost model from hardware measurements. Effective within
  compiler-defined spaces but requires 1000+ measurements.
- **MetaSchedule:** Probabilistic search space with transfer learning.
- **BaCO:** Bayesian optimization for compiler parameter spaces.
- **Helion:** LFBO for Triton autotuning; 36.5% tuning time reduction.

### 3.2 Limitations for Structural Search
Classical autotuners cannot make structural changes (warp specialization,
barrier merging, TMA staging) that dominate the performance gap. CrokTile
combines LLM reasoning (for structural changes) with compiler guidance
(for convergence acceleration).

---

## 4. Context Engineering & Agent Design

- **SWE-Agent:** Agent-Computer Interface determines effectiveness more than model.
  Direct parallel: DSL as ACI for kernel optimization.
- **Self-correction literature:** Iterative improvement depends on external feedback
  quality. CrokTile's 353 compile-time checks provide structured feedback.
- **Context engineering surveys (2025):** Formal framework for information density
  per token. CrokTile instantiates this for GPU kernel domain.

---

## 5. Gap Analysis

| Existing System | Strength | Gap CrokTile Fills |
|----------------|----------|-------------------|
| CUDA Agent, KernelSkill | Strong search strategies | No compile-time resource feedback |
| Triton autotune | Easy decorator-based | No occupancy feedback, exhaustive search |
| BaCO, Ansor | Sample-efficient BO | Cannot make structural changes |
| KernelAgent, PRAGMA | Hardware profiling feedback | Post-execution only, no compile-time pruning |
| CuTe DSL | Zero-cost abstraction | 4K+ tokens, no auto-tuning integration |

**CrokTile fills the gap:** DSL co-designed for AI agents (compact, structured
feedback) + compile-time resource model (zero-cost pruning and ranking) +
agentic tuner (compiler metadata as guardrails) = 5× convergence over
profiler-only approaches.


