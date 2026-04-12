# Dskyz — DAFE Trading Systems: Open-Source Collection

> **A professional-grade PineScript ecosystem** — manifold geometry, reinforcement learning, DSP filters, 55+ moving averages, 30+ RSI engines, 40+ volatility algorithms, multi-timeframe order flow integration, and a full library infrastructure for building institutional-grade indicators.

---

## 📦 What's in This Repo?

| File | Type | Description |
|------|------|-------------|
| [`Riemannian_Dreamer_Manifold_Engine.pine`](Riemannian_Dreamer_Manifold_Engine.pine) | Indicator (v6) | Markets as curved Riemannian manifolds + Dreamer RL world model |
| [`RSI: Evolved [DAFE].pine`](<RSI: Evolved [DAFE].pine>) | Indicator (v5) | 30+ RSI engine families + 15+ smoothers + divergence + MTF dashboard |
| [`BandsandChannelsLaboratory.pine`](BandsandChannelsLaboratory.pine) | Indicator (v5) | 40+ volatility algorithms — basis, deviation, band type modular system |
| [`WHF - Wave Health and Failure v6`](<WHF - Wave Health and Failure v6>) | Indicator (v6) | Neural adaptive wave scoring — ML + Thompson Sampling + Wick Physics |
| [`MA-trix Laboratory `](<MA-trix Laboratory >) | Indicator (v5) | 55+ moving average algorithms with smart signal filters |
| [`369`](369) | Indicator | 369 Vector Equilibrium — Gann geometry + Bayesian KNN + Hurst |
| [`Tick Asymmetry Index`](<Tick Asymmetry Index>) | Indicator | Order flow TAI — footprint + heuristic tick imbalance estimation |
| [`safe cuz lib.pine`](<safe cuz lib.pine>) | Library (v5) | DafeVisLib — themes, gradients, candle diagnostics, auto plot config |
| [`Market Structure Lib`](<Market Structure Lib>) | Library (v5) | Multi-TF market architecture — POC/VA, siege corridors, confluence zones |
| [`DafeVis Lib`](<DafeVis Lib>) | Library | Extended visualization and dashboard system |
| [`RSI:evolved.md`](RSI:evolved.md) | Docs | RSI: Evolved manual — all engines, smoothers, modules explained |
| [`Bands and Channels Laboratory.md`](<Bands and Channels Laboratory.md>) | Docs | Bands Laboratory manual — algorithms, patterns, signals |
| [`MOBILE_PINESCRIPT_IDE_GUIDE.md`](MOBILE_PINESCRIPT_IDE_GUIDE.md) | Docs | GitHub research guide — coding PineScript v6 in a phone-based IDE |

---

## 🗺️ Learning Path

If you're new to this collection, read in this order:

1. **[`LEARNING_GUIDE.md`](LEARNING_GUIDE.md)** — Start here. Structured walkthrough of every master-level pattern used across the codebase: custom types, libraries, arrays, footprint data, z-scoring, Hurst exponent, DSP filters, neural networks in Pine, Thompson Sampling, and more. All examples are drawn directly from these files.

2. **[`safe cuz lib.pine`](<safe cuz lib.pine>)** — Read the library first. It shows the cleanest, most teachable examples of `export type`, `export` functions, theme systems, and statistical helpers.

3. **[`MA-trix Laboratory `](<MA-trix Laboratory >)** — A self-contained indicator. See how 55+ algorithms are organized with `input.string` option arrays, tooltip groups, and adaptive filters.

4. **[`BandsandChannelsLaboratory.pine`](BandsandChannelsLaboratory.pine)** and **[`RSI: Evolved [DAFE].pine`](<RSI: Evolved [DAFE].pine>)** — Study the modular algorithm selection pattern and multi-mode signal architecture.

5. **[`WHF - Wave Health and Failure v6`](<WHF - Wave Health and Failure v6>)** — Introduces library imports (`import DskyzInvestments/...`), ML engine, and Thompson Sampling.

6. **[`Riemannian_Dreamer_Manifold_Engine.pine`](Riemannian_Dreamer_Manifold_Engine.pine)** — The flagship. Differential geometry, Hurst-modulated pivots, footprint integration, RL world model, GRPO policy optimization.

---

## 🧠 Key Concepts at a Glance

| Concept | Where to Find It |
|---------|-----------------|
| `export type` UDTs (User-Defined Types) | `safe cuz lib.pine`, `Market Structure Lib` |
| `library()` / `import` / `export` pattern | `safe cuz lib.pine`, `Market Structure Lib` |
| Dynamic arrays as ring buffers | `Riemannian_Dreamer_Manifold_Engine.pine` |
| `request.footprint()` order flow | `Riemannian_Dreamer_Manifold_Engine.pine`, `Tick Asymmetry Index` |
| Z-score normalization | `Riemannian_Dreamer_Manifold_Engine.pine` (`zscore()` helper) |
| Hurst exponent (R/S analysis) | `Riemannian_Dreamer_Manifold_Engine.pine` (`f_hurstExponent()`) |
| Ricci curvature approximation | `Riemannian_Dreamer_Manifold_Engine.pine` |
| Neural network forward pass + weight update | `WHF - Wave Health and Failure v6` (via `DafeRLMLLib`) |
| Thompson Sampling bandit | `WHF - Wave Health and Failure v6` (via `DafeSPALib`) |
| GRPO policy optimization | `Riemannian_Dreamer_Manifold_Engine.pine` |
| DSP filters (Butterworth, SuperSmoother) | `MA-trix Laboratory `, `RSI: Evolved [DAFE].pine` |
| Multi-timeframe structure | `Market Structure Lib`, `RSI: Evolved [DAFE].pine` |
| Adaptive color themes | `safe cuz lib.pine` (`get_theme()`) |
| Auto plot configuration | `safe cuz lib.pine` (`auto_config()`) |
| Signal filter pipeline | `MA-trix Laboratory `, `BandsandChannelsLaboratory.pine` |
| Elliott Wave scoring | `Riemannian_Dreamer_Manifold_Engine.pine` (`f_impulse_score()`) |

---

## 📄 License

MIT © 2026 ainell-owi
