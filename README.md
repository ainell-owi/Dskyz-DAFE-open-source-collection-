# Dskyz DAFE — Open-Source Collection

> **Attribution Notice**
> The Pine Script indicators and libraries in this collection were authored by **Dskyz** (also known as **DAFE Trading Systems**). This repository is maintained by a third party who has **no affiliation** with Dskyz Investments or DAFE Trading Systems. All intellectual property belongs to the original author.
> Official website: [dafetradingsystems.com](https://www.dafetradingsystems.com)

---

## 📚 Table of Contents

- [What Is This Collection?](#what-is-this-collection)
- [File Inventory](#file-inventory)
- [6-Step Learning Path](#6-step-learning-path)
- [Concept Quick-Reference](#concept-quick-reference)
- [Using This Repo with Google AI Studio](#using-this-repo-with-google-ai-studio)
- [Further Reading](#further-reading)

---

## What Is This Collection?

The DAFE (Dynamic Adaptive Framework Engine) collection is a suite of advanced TradingView Pine Script indicators and shared libraries authored by **Dskyz** (DAFE Trading Systems). This repository is a third-party collection of those publicly released scripts and is not affiliated with or endorsed by the original author.

Each script is built around a core philosophy stated by the original author: markets are dynamic, multi-dimensional systems, and your tools should be too.

Rather than offering single-purpose indicators, every piece in this collection is a **modular research environment** — a laboratory where you can swap algorithms, compare outputs, and build a toolkit perfectly calibrated to your market.

---

## File Inventory

| File | Type | Description |
|---|---|---|
| `BandsandChannelsLaboratory.pine` | Indicator | 40+ algorithm volatility & envelope engine with MTF Horizon, Kill Zones, and Pattern Recognition |
| `Bands and Channels Laboratory.md` | Docs | Full guide for the Bands & Channels Laboratory indicator |
| `RSI: Evolved [DAFE].pine` | Indicator | 30+ RSI engines, 15+ smoothers, Quantum Horizon visualization, Divergence Engine |
| `RSI:evolved.md` | Docs | Full guide for RSI: Evolved |
| `Riemannian_Dreamer_Manifold_Engine.pine` | Indicator | Advanced market-as-manifold framework using Riemannian geometry and Ricci curvature |
| `MA-trix Laboratory` | Indicator | Moving average research environment with multiple MA families |
| `Market Structure Lib` | Library | Reusable market-structure detection functions |
| `DafeVis Lib` | Library | Intelligent visualization engine — adaptive themes, dashboards, signal formatting |
| `safe cuz lib.pine` | Library | Alias/export file for DafeVisLib (`import DskyzInvestments/DafeVisualsLib/1 as viz`) |
| `Tick Asymmetry Index` | Indicator | Measures directional imbalance in tick-level data |
| `WHF - Wave Health and Failure v6` | Indicator | Wave structure health monitoring and failure detection |
| `369` | Indicator | Numerological/cyclical pattern framework |
| `LICENSE` | Legal | Repository license |

---

## 6-Step Learning Path

Follow this path to go from zero to confident with the DAFE collection:

**Step 1 — Understand the Philosophy**
Read the philosophy sections in `RSI:evolved.md` and `Bands and Channels Laboratory.md`. Both explain *why* these tools were built and the limitations of standard indicators they address.

**Step 2 — Learn the Shared Libraries**
Open `safe cuz lib.pine` (DafeVisLib) and `Market Structure Lib`. These are the shared building blocks used across all indicators. Understanding them will help you read any script in the collection.

**Step 3 — Start with RSI: Evolved**
Load `RSI: Evolved [DAFE].pine` in TradingView. Use the "DAFE Quantum Fusion" engine with "SuperSmoother" as a starting point (recommended in the docs). Explore the MTF Dashboard and Divergence Engine.

**Step 4 — Add Bands & Channels Laboratory**
Load `BandsandChannelsLaboratory.pine`. Pair it with RSI: Evolved to get both a momentum and a volatility read at the same time. Read `Bands and Channels Laboratory.md` to understand Squeeze Classification and Kill Zones.

**Step 5 — Explore the Advanced Frameworks**
Open `Riemannian_Dreamer_Manifold_Engine.pine`. This is the most mathematically complex script — it models the market as a Riemannian manifold with Ricci curvature. Read the inline comments carefully.

**Step 6 — Customize and Combine**
Use `DafeVis Lib` to apply consistent styling across custom scripts. Study `MA-trix Laboratory` for center-line options and `Tick Asymmetry Index` / `WHF` for additional confluence signals.

---

## Concept Quick-Reference

| Concept | Where to Find It | What It Does |
|---|---|---|
| 30+ RSI Engines | `RSI: Evolved [DAFE].pine` | Hull, Laguerre, KAMA, DAFE Quantum Fusion, Entropy Flow, and more |
| Quantum Horizon / Temporal Wave | `RSI: Evolved [DAFE].pine` | Projects higher-timeframe RSI waves onto the current chart |
| Dynamic Quantum Zones | `RSI: Evolved [DAFE].pine` | Volatility-adaptive OB/OS levels that "breathe" |
| 22 Basis Algorithms | `BandsandChannelsLaboratory.pine` | Center-line choices: SMA → Hull MA → KAMA → DAFE Tensor Cloud |
| 16 Deviation Algorithms | `BandsandChannelsLaboratory.pine` | Band-width choices: Std Dev → Parkinson → DAFE Dark Matter |
| MTF Horizon Display | `BandsandChannelsLaboratory.pine` | Projects higher-TF band metrics (Bandwidth %, Squeeze) onto current chart |
| Smart Kill Zones | `BandsandChannelsLaboratory.pine` | Volume + momentum validated reversal zones |
| Pattern Recognition | `BandsandChannelsLaboratory.pine` | Auto-detects Squeezes, Walking Bands, Band Divergences |
| Riemannian Manifold Model | `Riemannian_Dreamer_Manifold_Engine.pine` | Market modeled as 3D curved space; Ricci curvature = stress/expansion |
| DafeVisLib Theming | `safe cuz lib.pine` / `DafeVis Lib` | Adaptive color themes, dashboard builders, signal formatters |
| Divergence Engine | `RSI: Evolved [DAFE].pine` | Auto-detects regular & hidden divergences |
| Wave Health & Failure | `WHF - Wave Health and Failure v6` | Monitors wave structure integrity in real time |

---

## Using This Repo with Google AI Studio

This repository's documentation is structured so it can be used directly as a knowledge base for Google AI Studio. See **[GOOGLE_AI_STUDIO_GUIDE.md](GOOGLE_AI_STUDIO_GUIDE.md)** for step-by-step instructions on:

- Uploading repository files as AI context
- Writing a system prompt that makes the model an expert in DAFE tools
- Creating Q&A training pairs from this documentation
- Fine-tuning vs. grounding (which approach fits your goal)

---

## Further Reading

| Document | Purpose |
|---|---|
| [LEARNING_GUIDE.md](LEARNING_GUIDE.md) | Deep-dive educational guide through every concept in the collection |
| [GOOGLE_AI_STUDIO_GUIDE.md](GOOGLE_AI_STUDIO_GUIDE.md) | How to use this repo to train or ground a Google AI Studio model |
| [ORGANIZATION_GUIDE.md](ORGANIZATION_GUIDE.md) | Recommendations for growing and maintaining this repository |
| [RSI:evolved.md](RSI:evolved.md) | Complete RSI: Evolved indicator reference |
| [Bands and Channels Laboratory.md](Bands%20and%20Channels%20Laboratory.md) | Complete Bands & Channels Laboratory reference |

---

*Scripts authored by Dskyz (DAFE Trading Systems) — [dafetradingsystems.com](https://www.dafetradingsystems.com). This collection is maintained by a third party with no affiliation to the original author.*

