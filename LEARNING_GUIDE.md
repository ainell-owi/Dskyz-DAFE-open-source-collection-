# DAFE Collection — Learning Guide

> This guide is the primary educational resource for the Dskyz DAFE Open-Source Collection. It walks you through the philosophy, architecture, and practical use of every script in the library.

---

## Table of Contents

1. [Philosophy: Why DAFE Exists](#1-philosophy-why-dafe-exists)
2. [The Modular Architecture](#2-the-modular-architecture)
3. [Shared Libraries (Start Here)](#3-shared-libraries-start-here)
4. [RSI: Evolved — Momentum Intelligence](#4-rsi-evolved--momentum-intelligence)
5. [Bands & Channels Laboratory — Volatility Intelligence](#5-bands--channels-laboratory--volatility-intelligence)
6. [Riemannian Dreamer Manifold Engine — Geometric Intelligence](#6-riemannian-dreamer-manifold-engine--geometric-intelligence)
7. [Supporting Indicators](#7-supporting-indicators)
8. [How to Combine Tools for Confluence](#8-how-to-combine-tools-for-confluence)
9. [Pine Script Concepts Used in This Collection](#9-pine-script-concepts-used-in-this-collection)
10. [Glossary](#10-glossary)

---

## 1. Philosophy: Why DAFE Exists

Most retail indicators are built on a single assumption: that one formula fits all markets, all timeframes, and all traders. Bollinger Bands use a 20-period SMA and a 2x standard-deviation envelope — the same values in every chart. RSI defaults to 14 periods and static 70/30 levels — unchanged since Welles Wilder described them in 1978.

DAFE (Dynamic Adaptive Framework Engine) was built on the opposite assumption: **markets are dynamic, multi-dimensional systems, and analytical tools should be too.**

Every script in this collection is designed to be:

- **Modular** — swap algorithms without rewriting code
- **Adaptive** — settings that respond to market conditions automatically
- **Multi-timeframe aware** — decisions informed by the full temporal context
- **Visually intelligent** — information presented in the most intuitive form possible

This is not a collection of "set it and forget it" indicators. It is a laboratory. You are expected to experiment.

---

## 2. The Modular Architecture

Every major DAFE indicator is built on the same three-layer design:

```
┌─────────────────────────────────────────────────────┐
│  LAYER 3 — Visualization & Dashboard                │
│  (DafeVisLib, chart overlays, dashboard tables)     │
├─────────────────────────────────────────────────────┤
│  LAYER 2 — Signal & Pattern Intelligence            │
│  (divergence engine, pattern recognition, signals)  │
├─────────────────────────────────────────────────────┤
│  LAYER 1 — Core Calculation Engine                  │
│  (swappable algorithm families)                     │
└─────────────────────────────────────────────────────┘
```

This layering means you can change a single algorithm in Layer 1 and have the change flow automatically through signal detection (Layer 2) and visualization (Layer 3). There is no cascading rewrite required.

---

## 3. Shared Libraries (Start Here)

Before diving into the indicators, understand the two shared libraries that power the entire collection.

### DafeVisLib (`DafeVis Lib` / `safe cuz lib.pine`)

**What it is:** An intelligent visualization engine. Beyond static color choices, this library performs statistical analysis and makes adaptive visual decisions based on market conditions.

**Key exports:**
- `Theme` type — a structured color scheme with fields for primary, secondary, alert, bullish, bearish, neutral, background, and text colors
- Dashboard builder functions — create on-chart tables with consistent styling
- Signal formatting functions — apply regime-aware formatting to any signal
- Candle diagnostic overlays

**How to use it in your own scripts:**
```pine
import DskyzInvestments/DafeVisualsLib/1 as viz
```

**Why this matters:** Every DAFE indicator uses the same visual layer, so you get a consistent look-and-feel across all tools. When you change a theme in one indicator, the design language carries over.

### Market Structure Lib (`Market Structure Lib`)

**What it is:** A library of reusable market-structure detection functions. These are the primitives for identifying swing highs/lows, structure breaks, and order blocks.

**Why this matters:** Rather than reimplementing swing detection in every indicator, all DAFE tools can call these shared functions. Consistency in structure detection is critical — if your RSI indicator and your Bands indicator define "swing high" differently, they will disagree on signals.

---

## 4. RSI: Evolved — Momentum Intelligence

> **File:** `RSI: Evolved [DAFE].pine`  
> **Full Docs:** `RSI:evolved.md`

### The Core Idea

Standard RSI is a 14-period ratio of average gains to average losses, smoothed with Wilder's RMA. It is a single, fixed lens on momentum.

RSI: Evolved gives you **30+ different lenses**, each with a different mathematical philosophy, and then layers advanced post-processing on top.

### The Algorithm Families

#### The Classics
- **Wilder's RSI** — the original; uses RMA smoothing
- **Cutler's RSI** — uses SMA instead of RMA; more stable in trending markets
- **EMA RSI / WMA RSI** — weight recent price changes more heavily

#### The Low-Lag Warriors
- **Hull RSI** — exceptional balance of smoothness and near-zero lag; ideal for scalping
- **DEMA / TEMA** — double/triple EMA composites that cancel out most lag
- **ZLEMA** — removes lag by adjusting the source with its own historical data

#### The Exotics
- **Laguerre RSI** — time-warping, non-linear filter by John Ehlers; very responsive to trend changes
- **Fisher Transform RSI** — normalizes output to a Gaussian distribution; peaks/troughs are sharper
- **KAMA RSI** — adaptive speed: slow in choppy markets, fast in strong trends
- **Connors RSI** — composite of momentum, streak, and relative rank; good for mean-reversion setups

#### The Volume-Based
- **Volume-Weighted RSI** — gains/losses weighted by volume; measures conviction
- **MFI (Money Flow Index)** — classic volume+price momentum
- **VWAP-Weighted RSI** — uses VWAP proximity as a volume weighting factor

#### The DAFE Proprietary Engines
These are the crown jewels. You will not find these anywhere else.

| Engine | Physics Analogy | Best For |
|---|---|---|
| **DAFE Quantum Fusion** | Three harmonic timeframes superimposed via Golden Ratio | All-around; best default |
| **DAFE Kinetic Energy** | Momentum = Mass × Velocity (volume = mass) | Measuring true force of a move |
| **DAFE Spectral** | Digital Signal Processing; separates signal from noise | Clean, low-whipsaw signals |
| **DAFE Entropy Flow** | Information Theory; dampens signal in chaotic markets | Filtering out high-entropy chop |

### The Post-Processing Stack

After the raw RSI is calculated, you can pass it through a second algorithm:

1. **Smoothing Filter** — choose from 15+ options including Hull, KAMA, SuperSmoother, Butterworth, Gaussian, and Jurik-Style
2. **Regime Filter** — optionally scale the RSI's output based on trend, volatility, or momentum regime

### Key Modules

#### Quantum Horizon & Temporal Wave
Projects RSI (or MFI, or Stoch RSI) from up to three higher timeframes directly onto your current chart as "glowing, flowing" wave overlays. Each wave sits in its own gridded channel with 30/50/70 reference levels.

**How to read it:** When all three temporal waves are pointing the same direction as your current-chart RSI, momentum is strongly aligned across timeframes. When they diverge, be cautious.

#### Dynamic Quantum Zones
The 70/30 overbought/oversold levels automatically widen during high-volatility trends and tighten during consolidation. This prevents premature exits from strong trends and improves precision during mean-reversion setups.

#### Divergence Engine
Auto-detects:
- **Regular Bullish Divergence** — price makes lower low, RSI makes higher low → potential reversal up
- **Regular Bearish Divergence** — price makes higher high, RSI makes lower high → potential reversal down
- **Hidden Bullish Divergence** — price makes higher low, RSI makes lower low → trend continuation up
- **Hidden Bearish Divergence** — price makes lower high, RSI makes higher high → trend continuation down

#### MTF Consensus Dashboard
Shows momentum state across three higher timeframes. "ALL BULL" / "ALL BEAR" readings are the strongest confluence signals.

#### RSI Bands
Bollinger Bands, Keltner Channels, or other band types applied *to the RSI line itself*. A pierce of the upper/lower RSI band signals a statistical extreme in momentum.

### Recommended Starting Configuration
- **Engine:** DAFE Quantum Fusion
- **Post-Smoother:** SuperSmoother
- **Zones:** Dynamic (enabled)
- **Divergence:** Both Regular and Hidden
- **MTF Dashboard:** 3 timeframes above your trading timeframe

---

## 5. Bands & Channels Laboratory — Volatility Intelligence

> **File:** `BandsandChannelsLaboratory.pine`  
> **Full Docs:** `Bands and Channels Laboratory.md`

### The Core Idea

A band indicator has three components:
1. **Basis (Center Line)** — what is the mean?
2. **Deviation (Width)** — how far does price typically deviate from the mean?
3. **Band Type (Logic)** — what envelope construction rule is used?

Standard Bollinger Bands lock you into one choice for each component: SMA, standard deviation, and symmetric envelope. Bands & Channels Laboratory makes all three fully swappable.

### Algorithm Library

#### 22 Basis Algorithms (Center Line)
From classic (SMA, EMA, WMA) to zero-lag (Hull MA, DEMA, TEMA) to adaptive (KAMA, VIDYA) to proprietary (DAFE Tensor Cloud — a 4D average of OHLC data).

#### 16 Deviation Algorithms (Band Width)
From simple (Standard Deviation, ATR) to statistically robust (Parkinson Volatility, Garman-Klass, Yang-Zhang) to advanced (Ulcer Index, Choppiness) to proprietary (DAFE Dark Matter, DAFE Entropy, DAFE Elastic).

**Key distinction:** Parkinson, Garman-Klass, and Yang-Zhang use the high/low range and open/close data to estimate volatility more efficiently than standard deviation. They are better at capturing intraday volatility that gets hidden by close-to-close calculations.

#### 14 Band Types (Envelope Logic)
- **Bollinger Bands** — symmetric, mean-reverting
- **Keltner Channels** — ATR-based, trend-following
- **Donchian Channels** — highest high / lowest low
- **DAFE Quantum Bands** — noise-canceling step function; cleaner transitions

### Key Modules

#### MTF Horizon Display
Projects bandwidth percentage or squeeze state from up to three higher timeframes onto your current chart. You can see at a glance whether the macro environment is compressing or expanding.

#### Smart Kill Zones
Price levels where price interacted with the bands on **high volume with significant momentum**. These represent institutionally defended levels — not just simple pivots. The indicator tracks, plots, and updates these zones automatically.

#### Pattern Recognition Engine

| Pattern | What It Means |
|---|---|
| **Squeeze: Coiling** | Very tight compression; high potential energy; breakout likely |
| **Squeeze: Compression** | Moderate squeeze; market digesting; watch for direction |
| **Walking Upper Band** | Price consistently closing above/at upper band; powerful uptrend |
| **Walking Lower Band** | Price consistently closing below/at lower band; powerful downtrend |
| **Band Divergence** | Bandwidth trend diverges from price trend; exhaustion signal |

#### Signal Engine
Eight distinct signal modes:
- **Mean Reversion** — signal on band touch
- **Squeeze Breakout** — signal on squeeze expansion
- **Trend Following** — signal on sustained band walk
- **Smart Composite** — multi-factor scoring; only highest-quality setups

#### Master Dashboard
At-a-glance read of: %B (price position in band), Bandwidth %, Volatility Regime, current Pattern, most recent Signal, and (when enabled) backtested Win Rate, Profit Factor, and Robustness Score.

### Recommended Starting Configuration
- **Basis:** Hull MA (zero-lag, smooth)
- **Deviation:** Parkinson Volatility (robust intraday estimate)
- **Band Type:** Bollinger (familiar, well-understood behavior)
- **Pattern Engine:** Enabled
- **MTF Horizon:** 1 level above your trading timeframe

---

## 6. Riemannian Dreamer Manifold Engine — Geometric Intelligence

> **File:** `Riemannian_Dreamer_Manifold_Engine.pine`

### The Core Idea

This is the most mathematically advanced script in the collection. It models the market as a **Riemannian manifold** — a curved geometric space — rather than a flat time series.

### The Framework

The market state at any moment is represented as a point in a 3-dimensional manifold with coordinates:

| Coordinate | Meaning |
|---|---|
| **Pressure** | Directional buying/selling pressure |
| **Health** | Quality and sustainability of the current move |
| **Liquidity** | Depth and stability of the order book environment |

### Key Concepts

#### Metric Tensor
The metric tensor defines how "distances" are measured in this curved space. In RDME, it is approximated by the local covariance structure of the three coordinates. This allows the model to account for the fact that equal price moves may have very different geometric "distances" depending on the health and liquidity context.

#### Ricci Scalar Curvature (R)
The Ricci curvature summarizes how curved the manifold is at the current market state:

- **Positive R (Market Contraction)** — the manifold is curving inward; this corresponds to potential reversal zones
- **Negative R (Market Expansion)** — the manifold is curving outward; this corresponds to trend-continuation environments

#### Mahalanobis Distance
RDME uses a Mahalanobis-inspired distance metric rather than Euclidean distance. This means outlier states (unusual combinations of pressure, health, and liquidity) are properly identified as extreme events, not just large numbers.

### How to Use It
RDME is best used as a **regime filter** rather than a signal generator. When Ricci curvature is strongly positive, be cautious of trend-following entries. When it is strongly negative, trend-continuation setups have stronger geometric support.

Pair RDME with RSI: Evolved (signal timing) and Bands & Channels Laboratory (volatility context) for a three-dimensional analytical framework.

---

## 7. Supporting Indicators

### MA-trix Laboratory
A moving average research environment. Contains multiple MA families side by side for direct comparison. Use this to select the best center-line algorithm for your market before applying it in Bands & Channels Laboratory.

### Tick Asymmetry Index
Measures directional imbalance in tick-level data. High positive asymmetry = more buying ticks than selling ticks even when price is flat — often a leading indicator of upward pressure. Best used on tick charts or very short timeframes.

### WHF — Wave Health and Failure v6
Monitors the internal health of wave structures. A "failing" wave (one that does not reach its projected target before pulling back) often precedes a structural reversal. Use alongside Market Structure Lib for complete structural context.

### 369
A cyclical/numerological framework. Plots price levels based on the Rodin 3-6-9 pattern. More experimental than the other scripts; treat as confluence only.

---

## 8. How to Combine Tools for Confluence

The highest-probability setups occur when multiple independent analytical layers agree. Here are three example frameworks:

### Framework 1: Momentum + Volatility (Basic)
1. Load **RSI: Evolved** + **Bands & Channels Laboratory**
2. Wait for RSI to reach a Dynamic Quantum Zone (oversold/overbought)
3. Confirm price is at or near a band boundary in Bands Lab
4. Check that the Pattern Engine shows a Squeeze (if entering on a breakout) or a Band Touch in a non-trending regime (if entering on mean reversion)
5. Enter on a Signal confirmation from the Bands Lab Signal Engine

### Framework 2: Momentum + Volatility + Structure (Intermediate)
1. Add **Market Structure Lib** overlays to mark swing highs/lows
2. Use RSI: Evolved's Divergence Engine — look for regular divergences at swing points
3. Confirm a Smart Kill Zone from Bands Lab aligns with the swing structure level
4. Use the MTF Consensus Dashboard (RSI) and MTF Horizon (Bands Lab) to confirm macro alignment

### Framework 3: Full Geometric Framework (Advanced)
1. All of Framework 2, plus:
2. Check **RDME** Ricci curvature — favor mean-reversion setups when R is positive, trend setups when R is negative
3. Check **Tick Asymmetry Index** for order flow confirmation
4. Check **WHF** for wave health — enter only if the current wave is "healthy"

---

## 9. Pine Script Concepts Used in This Collection

If you want to read, modify, or learn from the scripts, these are the key Pine Script v5/v6 concepts you will encounter:

| Concept | Where It Appears | What to Learn |
|---|---|---|
| `library()` declaration | `DafeVis Lib`, `Market Structure Lib` | How to create reusable Pine Script modules |
| `export` keyword | `safe cuz lib.pine` | How to expose functions from a library |
| `import` statement | Any indicator using DafeVisLib | How to consume a published library |
| `type` declaration | DafeVisLib `Theme` type | Pine Script user-defined types (UDTs) |
| `matrix` functions | RDME | Used for metric tensor calculations |
| `request.security()` | RSI: Evolved, Bands Lab | Multi-timeframe data requests |
| `ta.divergence` patterns | RSI: Evolved | Manual divergence detection logic |
| `table.new()` / `table.cell()` | All dashboards | On-chart table/dashboard creation |
| `method` keyword | Advanced scripts | Object-oriented patterns in Pine Script v5+ |

---

## 10. Glossary

| Term | Definition |
|---|---|
| **ATR** | Average True Range — a measure of recent price volatility |
| **Band Walk** | When price consistently closes at or beyond a band boundary; signature of a strong trend |
| **Bandwidth %** | (Upper Band − Lower Band) / Basis × 100; measures relative band width |
| **%B** | (Price − Lower Band) / (Upper Band − Lower Band); measures price position within the band (0 = lower band, 1 = upper band) |
| **Confluence** | Multiple independent analytical signals agreeing at the same price level / time |
| **DAFE** | Dynamic Adaptive Framework Engine — the system design philosophy for this collection |
| **Divergence (Regular)** | Price makes a new extreme; oscillator does not → potential reversal |
| **Divergence (Hidden)** | Oscillator makes a new extreme; price does not → trend continuation |
| **Entropy** | In information theory, a measure of disorder or unpredictability in a system |
| **Hull MA** | A moving average using weighted MAs to achieve near-zero lag |
| **KAMA** | Kaufman Adaptive Moving Average — automatically adjusts its speed to market noise |
| **Kill Zone** | A high-probability reversal level validated by volume and momentum |
| **Laguerre Filter** | A time-warping non-linear filter developed by John Ehlers |
| **Mahalanobis Distance** | A multi-dimensional distance metric that accounts for correlations between variables |
| **MTF** | Multi-TimeFrame — analysis or visualization using data from multiple timeframes simultaneously |
| **Parkinson Volatility** | A volatility estimate using high/low range; more efficient than close-to-close std dev |
| **Ricci Curvature** | In Riemannian geometry, a measure of how curved a manifold is at a given point |
| **Riemannian Manifold** | A curved geometric space with a defined metric for measuring distances |
| **RMA** | Wilder's Smoothing Average (Running Moving Average); used in the original RSI |
| **Squeeze** | When band width contracts significantly below its historical average; precedes expansion |
| **SuperSmoother** | A digital signal processing filter by John Ehlers; removes noise while preserving signal |
| **VWAP** | Volume Weighted Average Price — the average price weighted by volume |
| **ZLEMA** | Zero-Lag EMA — reduces lag by adjusting the source with historical error |

---

*"The hard part is not making the decision to buy or sell, but having the patience and discipline to wait for the right setup." — Mark Weinstein*

*Dskyz (DAFE Trading Systems) — Taking you to school.*
