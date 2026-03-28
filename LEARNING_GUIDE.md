# DAFE Master-Level PineScript — Learning Guide

> This guide walks you through the advanced PineScript patterns used in this collection. Every concept is anchored to actual code in the repo so you can follow along file-by-file.

---

## Table of Contents

1. [PineScript Versions in This Repo](#1-pinescript-versions-in-this-repo)
2. [The Library System — `library()`, `export`, `import`](#2-the-library-system)
3. [User-Defined Types (`type`)](#3-user-defined-types)
4. [Dynamic Arrays as Ring Buffers](#4-dynamic-arrays-as-ring-buffers)
5. [Footprint / Order Flow Data](#5-footprint--order-flow-data)
6. [Z-Score Normalization](#6-z-score-normalization)
7. [Hurst Exponent — Regime Detection](#7-hurst-exponent--regime-detection)
8. [Ricci Curvature — Market Geometry](#8-ricci-curvature--market-geometry)
9. [The World Model Neural Network](#9-the-world-model-neural-network)
10. [GRPO — Group Relative Policy Optimization](#10-grpo--group-relative-policy-optimization)
11. [Thompson Sampling (Bandit Algorithms)](#11-thompson-sampling-bandit-algorithms)
12. [DSP Filters — SuperSmoother, Butterworth, Laguerre](#12-dsp-filters)
13. [Adaptive Moving Averages — KAMA, VIDYA, Hull](#13-adaptive-moving-averages)
14. [Modular Algorithm Selection Pattern](#14-modular-algorithm-selection-pattern)
15. [Signal Filter Pipeline](#15-signal-filter-pipeline)
16. [The Theme and Visualization Engine](#16-the-theme-and-visualization-engine)
17. [Elliott Wave Scoring](#17-elliott-wave-scoring)
18. [Multi-Timeframe Architecture](#18-multi-timeframe-architecture)
19. [Candle Diagnostics (Wick Physics)](#19-candle-diagnostics-wick-physics)
20. [Putting It All Together — Indicator Architecture](#20-putting-it-all-together)

---

## 1. PineScript Versions in This Repo

The collection uses both **v5** and **v6**. You'll see the declaration at the top of every file:

```pine
//@version=5   // BandsandChannelsLaboratory.pine, MA-trix Laboratory, safe cuz lib.pine
//@version=6   // Riemannian_Dreamer_Manifold_Engine.pine, WHF - Wave Health and Failure v6
```

**Key differences you'll encounter:**

| Feature | v5 | v6 |
|---------|----|----|
| `request.footprint()` | ❌ not available | ✅ available |
| `library()` | ✅ | ✅ |
| `export type` | ✅ | ✅ |
| `var` arrays | ✅ | ✅ |
| `barstate.isconfirmed` guard | ✅ | ✅ |

When you see `request.footprint(...)` — that file requires v6.

---

## 2. The Library System

**Files:** `safe cuz lib.pine`, `Market Structure Lib`

PineScript libraries let you share types and functions across multiple indicators without copying code. The DAFE ecosystem is built on this pattern.

### Declaring a library

```pine
//@version=5
library("DafeVisLib", overlay=true)
```

The string `"DafeVisLib"` is the public name. `overlay=true` means it can be overlaid on a price chart.

### Exporting a type

From `safe cuz lib.pine`:

```pine
// @type Theme — Core color palette for consistent cross-indicator styling
export type Theme
    color p         // Primary accent
    color s         // Secondary accent
    color a         // Alert / highlight
    color bull      // Bullish state
    color bear      // Bearish state
    color neu       // Neutral state
    color bg        // Background
    color txt_hi    // High-contrast text
    color txt_lo    // Low-contrast / dim text
```

The `export` keyword makes `Theme` available to any indicator that imports this library. Without `export` the type is private to the library.

### Exporting a function

```pine
// @function get_theme — Returns a complete color palette by name
export get_theme(string name) =>
    Theme t = Theme.new()
    if name == "Neon"
        t.p := #FF00FF, t.s := #00FFFF, t.a := #FFFF00
        // ...
    t
```

Return value is always the last expression. `Theme.new()` creates a zero-initialized instance of the UDT.

### Importing a library in an indicator

From `WHF - Wave Health and Failure v6`:

```pine
import DskyzInvestments/DafeRLMLLib/1 as ml
import DskyzInvestments/DafeSPALib/1 as spa
import DskyzInvestments/DafeMLSPABridge/1 as bridge
import DskyzInvestments/WickPressureLib/1 as wpk
import DskyzInvestments/DafePatternsLib/1 as pattern
import DskyzInvestments/DafeVisLib/1 as viz
import DskyzInvestments/DafeDashboardLib/1 as dafe
```

Format: `import <username>/<LibraryName>/<version> as <alias>`

After import, call exported functions with `alias.function_name(...)`:

```pine
// Call get_theme exported from DafeVisLib, aliased as viz
Theme t = viz.get_theme("Neon Tokyo")
```

---

## 3. User-Defined Types

**Files:** `safe cuz lib.pine`, `Market Structure Lib`, `Riemannian_Dreamer_Manifold_Engine.pine`

UDTs (User-Defined Types) are Pine's equivalent of structs. They are the central design pattern in this repo — instead of passing 10 separate variables to a function, you pass one typed object.

### Defining a type

From `Market Structure Lib`:

```pine
//@type Single structural price level with metadata and liquidity context
export type StructureLevel
    float          price          = na
    string         level_type     = ""
    string         timeframe      = ""
    float          strength       = 0.5
    int            age            = 0
    int            touch_count    = 0
    int            last_touch_bar = 0
    float          delta_at_level = 0.0
    bool           is_broken      = false
    LevelLiquidity liquidity      = na   // nested UDT
```

Default values after `=` are used when you call `StructureLevel.new()` with no arguments.

### Nesting types

`StructureLevel` contains a `LevelLiquidity` field — one UDT nested inside another:

```pine
export type LevelLiquidity
    float  delta_at_level    = 0.0
    float  absorption_rate   = 0.0
    float  spread_quality    = 0.5
    float  volume_quality    = 0.5
    float  aggressor_ratio   = 0.5
    float  hold_probability  = 0.5
    float  break_probability = 0.5
    string action_type       = "neutral"
    int    sample_count      = 0
```

### Creating instances

```pine
StructureLevel lvl = StructureLevel.new()      // all defaults
StructureLevel lvl2 = StructureLevel.new(price=1234.5, level_type="resistance", timeframe="1D")
```

### The WaveToken type (RDME)

The `Riemannian_Dreamer_Manifold_Engine.pine` defines `WaveToken` — one of the most feature-rich UDTs in the repo:

```pine
type WaveToken
    int   direction        // +1 = up, -1 = down
    int   degree           // Elliott degree: 1, 2, or 3
    int   startBar
    int   endBar
    float startPrice
    float endPrice
    int   duration
    float magnitude
    float atrMagnitude
    float angle
    float pressureScore    // manifold pressure coordinate
    float healthScore      // manifold health coordinate
    float liquidityScore   // manifold liquidity coordinate
    float fpBuyVol         // footprint buy volume
    float fpSellVol        // footprint sell volume
    float fpDeltaVol       // buy - sell
    float fpDeltaEff       // delta efficiency (direction-adjusted)
    float pocShift         // POC movement during swing
    float vaAccept         // value area acceptance
    float absorptionRate
    float conviction
    float exhaustion
    float trap
    int   siegeHits
    float siegeDecay
    float siegePressure
    float siegeDeltaAlign
    bool  thirdPushFlag
    float siegeBreakProb
    float siegeFailProb
```

18+ fields per swing — this is what lets downstream functions like `f_impulse_score()` reason about wave quality without needing raw OHLCV data.

---

## 4. Dynamic Arrays as Ring Buffers

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

Pine's `array` functions let you implement a **capped rolling buffer** — the single most important data structure in this codebase. The pattern: push new bars, shift old ones when the buffer is full.

### Declaration

```pine
var array<int>   hBars   = array.new_int()
var array<float> hBuy    = array.new_float()
var array<float> hSell   = array.new_float()
var array<float> hDelta  = array.new_float()
// ... 11 parallel arrays, all the same length
```

`var` means "initialize once, persist across bars."

### Filling the buffer each bar

```pine
array.push(hBars, bar_index)
array.push(hBuy, fpBuy)
array.push(hSell, fpSell)
array.push(hDelta, fpDelta)
// ... push to every array
```

### Capping at max size — the ring buffer

```pine
if array.size(hBars) > i_histMax      // i_histMax = 1400
    array.shift(hBars)               // remove oldest element
    array.shift(hBuy)
    array.shift(hSell)
    array.shift(hDelta)
    // ... shift every array
```

`array.push` adds to the end (newest). `array.shift` removes from the front (oldest). The result is a sliding window of exactly `i_histMax` bars.

### Iterating the buffer

```pine
for i = 0 to array.size(hBars) - 1
    int bi = array.get(hBars, i)
    if bi >= startB and bi <= endB
        float pr = array.get(hPress, i)
        float de = array.get(hDelta, i)
        // process ...
```

This is used in `f_scan_siege()` to look back through the history for touches on a structural level — something you cannot do with simple `close[i]` referencing because the swing endpoints are dynamic.

### Wave token array

```pine
var array<WaveToken> waveTokens = array.new<WaveToken>()

// Add new token:
array.push(waveTokens, upTok)

// Cap at max:
if array.size(waveTokens) > i_tokenMax
    array.shift(waveTokens)

// Access by index:
WaveToken t5 = array.get(waveTokens, tokCount - 1)   // most recent
WaveToken t1 = array.get(waveTokens, tokCount - 5)   // 5th-most-recent
```

---

## 5. Footprint / Order Flow Data

**File:** `Riemannian_Dreamer_Manifold_Engine.pine` (v6 only)

Footprint data gives you **real buy/sell volume decomposition** per bar — the most informative market data available. Because footprint requires premium data feeds, every usage includes a graceful OHLCV fallback.

### Requesting footprint data

```pine
footprint fp = request.footprint(i_fpTicks, i_fpVA)
```

- `i_fpTicks`: tick resolution per row (e.g. 100 ticks per footprint row)
- `i_fpVA`: value area percentage (e.g. 70 = 70% of volume)

### Extracting values with graceful fallback

```pine
// Buy volume: use footprint if available, else approximate from candle structure
float fpBuy  = nz(not na(fp) ? fp.buy_volume()  : volume * (close - low)  / rng, 0.0)
float fpSell = nz(not na(fp) ? fp.sell_volume() : volume * (high - close) / rng, 0.0)
float fpDelta = nz(not na(fp) ? fp.delta()      : (fpBuy - fpSell), 0.0)
```

The ternary `not na(fp) ? fp.buy_volume() : ...` is the fallback pattern. If footprint data isn't available (free account, wrong chart type), the OHLCV formula `volume * (close - low) / range` approximates buy-side pressure from candle position.

### Point of Control (POC) and Value Area

```pine
if not na(fp)
    volume_row vahRow = fp.vah()   // value area high row
    volume_row valRow = fp.val()   // value area low row
    volume_row pocRow = fp.poc()   // point of control row
    fpVah  := vahRow.up_price()
    fpVal  := valRow.down_price()
    fpPocU := pocRow.up_price()
    fpPocL := pocRow.down_price()
```

POC = the price level with the most volume traded in that bar. Value area = the price range containing 70% of volume. These are key institutional reference levels.

### Derived metrics

```pine
float fpTotalVol   = math.max(fpBuy + fpSell, 1.0)
float fpDeltaRatio = nz(fpDelta / fpTotalVol, 0.0)   // signed: +1 = all buys, -1 = all sells
float fpBuyRatio   = nz(fpBuy / fpTotalVol, 0.5)
float fpImbalance  = math.abs(fpBuyRatio - 0.5) * 2.0 // 0 = balanced, 1 = extreme one-sided

// Absorption: price moves opposite to delta — hidden resistance/support
float fpAbsorption = ((close > open and fpDelta < 0) or (close < open and fpDelta > 0)) ? 1.0 :
                     (rng < atr14 * 0.5 and volume > smaVol20 ? 0.8 : 0.0)
```

**Absorption** is key: if the bar closes up but delta was negative (more selling), institutions were absorbing retail selling — a bullish sign at support levels.

---

## 6. Z-Score Normalization

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

Z-scoring is used throughout the codebase to make heterogeneous series (price, volume, delta) comparable on the same scale. The helper function:

```pine
zscore(float src, int len, float cap) =>
    float avg = nz(ta.sma(src, len), src)
    float sd  = nz(ta.stdev(src, len), 1.0)
    float z   = sd > 0 ? (src - avg) / sd : 0.0
    nz(clamp(z, -cap, cap), 0.0)
```

- `cap` limits the output to `[-cap, +cap]` — prevents extreme outliers from dominating signals
- `nz(..., 0.0)` handles the `na` case on the first few bars before `len` bars are available

**Usage example** — normalizing wick size:

```pine
float uW = high - math.max(open, close)      // raw upper wick in price units
float uZ = zscore(uW, i_zLen, 4.0)          // z-score: "how extreme is this wick?"
```

Now `uZ > 2` means the wick is 2+ standard deviations above normal — an objective, adaptive threshold that works on any instrument without hardcoding price levels.

---

## 7. Hurst Exponent — Regime Detection

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

The Hurst exponent H measures **trend persistence** vs **mean-reversion** in a time series. H is calculated using Rescaled Range (R/S) analysis:

```pine
f_hurstExponent(float src, int length) =>
    float mean = nz(ta.sma(src, length), src)
    float sumDev = 0.0
    float maxDev = 0.0
    float minDev = 0.0
    for i = 0 to length - 1
        float deviation = nz(src[i], src) - mean
        sumDev += deviation
        maxDev := math.max(maxDev, sumDev)
        minDev := math.min(minDev, sumDev)
    float rangeRS = maxDev - minDev           // R: range of cumulative deviations
    float stdDev = nz(ta.stdev(src, length), 1.0)
    float rs = stdDev > 0 ? rangeRS / stdDev : 1.0  // R/S ratio
    float h = rs > 0 ? math.log(rs) / math.log(length) : 0.5
    nz(clamp(h, 0.2, 0.8), 0.5)
```

The formula: `H = log(R/S) / log(n)`

**Interpretation:**
- `H > 0.5` → Trending market. Price deviates persistently in one direction.
- `H < 0.5` → Mean-reverting market. Price oscillates around the mean.
- `H ≈ 0.5` → Random walk. No predictable structure.

**How it's used** — adaptive pivot length:

```pine
float hurst    = f_hurstExponent(close, i_hurstPer)
int   dynPivot = int(clamp(math.round(i_basePivot * (1.5 - hurst)), i_minPivot, i_maxPivot))
```

When `hurst = 0.7` (strong trend): `dynPivot = basePivot * (1.5 - 0.7) = basePivot * 0.8` → shorter pivot → detects shorter swings → catches emerging waves earlier.

When `hurst = 0.3` (mean-reverting): `dynPivot = basePivot * (1.5 - 0.3) = basePivot * 1.2` → longer pivot → filters noise → avoids false signals in choppy markets.

This is **the** master-level pattern: let market behavior determine your analysis parameters instead of fixing them.

---

## 8. Ricci Curvature — Market Geometry

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

This is the most mathematically advanced concept in the repo. The market state is modeled as a point on a 3D Riemannian manifold (coordinates: Pressure, Health, Liquidity). Curvature of the manifold indicates whether price is in a reversal zone or trend zone.

The Ricci scalar approximation:

```pine
float retSeries  = nz(ta.change(close) / close[1], 0.0)    // log-return proxy
float volOfVol   = ta.stdev(ta.stdev(retSeries, 14), 34)   // volatility of volatility
float volOfVolMA = ta.sma(ta.stdev(retSeries, 14), 34)      // its moving average
float ricciRaw   = nz((volOfVol - volOfVolMA) * 65.0 / atr14, 0.0)
float ricciSmooth = ta.ema(ricciRaw, 8)

bool  isHyperbolic = ricciSmooth < -1.2   // negative curvature → expansion
bool  isSpherical  = ricciSmooth > 1.2    // positive curvature → contraction
bool  isFlat       = math.abs(ricciSmooth) <= 1.2  // flat → random walk
```

**Intuition:**
- **Spherical (positive R):** The market is "curving back on itself" — volatility of volatility is increasing, suggesting price expansion is unsustainable. Reversal zone.
- **Hyperbolic (negative R):** The market is "opening up" — volatility of volatility is decreasing relative to baseline. Trend can continue.
- **Flat:** Neither regime dominates. Low-conviction environment.

This maps the second derivative of volatility onto geometry — a proxy for Ricci curvature without differential equation machinery.

---

## 9. The World Model Neural Network

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

The "Dreamer" is a 3×3 linear neural network that **predicts the next bar's manifold state** from the current state. It learns online — weights update every confirmed bar using gradient descent.

### State representation

The 3 manifold coordinates per bar:

```pine
float pLvl = nz(pressureBar)  / 100.0   // normalized -1 to +1
float hLvl = nz(healthBar)    / 100.0
float lLvl = nz(liquidityBar) / 100.0
```

### Weight matrix (3×3 + bias vector)

```pine
var float w00 = 1.0, var float w01 = 0.0, var float w02 = 0.0
var float w10 = 0.0, var float w11 = 1.0, var float w12 = 0.0
var float w20 = 0.0, var float w21 = 0.0, var float w22 = 1.0
var float b0 = 0.0, var float b1w = 0.0, var float b2w = 0.0
```

Initialized as the identity matrix — "predict that next bar equals this bar." The network learns deviations from that baseline.

### Forward pass (prediction)

```pine
float predP = b0  + w00*ps0 + w01*ps1 + w02*ps2   // predict next Pressure
float predH = b1w + w10*ps0 + w11*ps1 + w12*ps2   // predict next Health
float predL = b2w + w20*ps0 + w21*ps1 + w22*ps2   // predict next Liquidity
```

`ps0`, `ps1`, `ps2` are the **previous bar's** state (saved from last iteration).

### Error and novelty

```pine
float e0 = nz(pLvl - predP, 0.0)   // actual minus predicted
float e1 = nz(hLvl - predH, 0.0)
float e2 = nz(lLvl - predL, 0.0)
predErr := nz(math.sqrt((e0*e0 + e1*e1 + e2*e2) / 3.0), 0.0)  // RMS error

// High prediction error = novel/unusual market state
novelty    := nz(clamp(predErr * 100.0 / 40.0, 0.0, 1.5), 0.1)
plasticity := nz(clamp(0.10 + novelty * 0.60, 0.10, 1.00), 0.10)
```

`plasticity` is the adaptive learning rate multiplier — the network learns **faster when the market is doing something new**, and slower in familiar regimes.

### Weight update (online gradient descent)

```pine
float lr = (i_wmLR * plasticity) * 0.0001
w00 := nz(clamp(w00 + lr * e0 * ps0, -5.0, 5.0), w00)
w01 := nz(clamp(w01 + lr * e0 * ps1, -5.0, 5.0), w01)
// ... all 9 weights and 3 biases updated similarly
b0  := nz(clamp(b0 + lr * e0 * 50.0, -100.0, 100.0), b0)
```

This is standard **stochastic gradient descent**: `w += learning_rate * error * input`. The `clamp(-5, 5)` prevents weight explosion.

---

## 10. GRPO — Group Relative Policy Optimization

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

After the world model predicts the next state, the GRPO system evaluates **3 action modes** (Conservative, Neutral, Aggressive) by running **Monte Carlo imagination rollouts** and picking the best Sharpe ratio.

### Imagination rollout structure

```pine
for a = 0 to 2               // 3 action modes
    for p = 0 to 1           // 2 Monte Carlo paths per action
        float pVal = 0.0
        float disc = 1.0     // discount factor
        for step = 0 to i_imagDepth - 1    // N forward steps
            // Add Monte Carlo noise scaled by market uncertainty
            float seed = bar_index * 1000.0 + a * 100.0 + p * 10.0 + step
            float ns0 = b0 + w00*ds0 + w01*ds1 + w02*ds2 + prand(seed) * noiseScale
            // ...
            float stepR = latentMean * stepHarm * (1.0 - failRisk * 0.55)
            pVal += disc * stepR    // discounted reward
            disc *= 0.93            // 7% decay per step
```

`prand(seed)` is a deterministic pseudo-random function using the sine trick:

```pine
prand(float s) =>
    float fract = math.abs(s) * 12.9898 + 78.233
    float r = math.sin(fract) * 43758.5453
    r - math.floor(r)
```

This gives repeatable noise for the same bar — important because Pine re-executes on each chart update.

### Sharpe ratio selection

```pine
float meanV = tV / 2.0                                    // average reward across 2 paths
float varV  = math.abs((tV2 / 2.0) - meanV * meanV)      // variance
float sharpe = meanV / (math.sqrt(varV) + EPS)            // risk-adjusted return
if sharpe > bestSharpe
    bestSharpe := sharpe
    bestAct    := a                                        // 0=Conservative, 1=Neutral, 2=Aggressive
```

### Policy update (softmax + advantage)

Agents track cumulative P&L. Each agent's advantage drives a softmax policy update every `i_grpoEvery` bars:

```pine
var GrpoAgent ag0 = GrpoAgent.new(0.0, 0, 0.0)  // Conservative
var GrpoAgent ag1 = GrpoAgent.new(0.0, 0, 0.0)  // Neutral
var GrpoAgent ag2 = GrpoAgent.new(0.0, 0, 0.0)  // Aggressive
```

The winning action mode adjusts the signal threshold `actThr`. If Conservative wins, the threshold rises (more selective); if Aggressive wins, it falls (more signals).

---

## 11. Thompson Sampling (Bandit Algorithms)

**File:** `WHF - Wave Health and Failure v6` (via `DafeSPALib`)

Thompson Sampling solves the **exploration vs exploitation problem**: you have multiple sub-strategies, but don't know which works best in the current regime. The algorithm allocates trading trust to strategies based on their Beta-distributed performance posteriors.

From the WHF tooltip:

```pine
var string TT_SPA = '🎯 SUCCESS PROPENSITY ANALYSIS\n\n' +
    'Uses \'Thompson Sampling\' to allocate trust to different sub-strategies.\n\n' +
    '• Arms: Number of internal strategies competing.\n' +
    '• Decay: Memory factor. How fast it forgets old data.\n' +
    '• Trauma: How severely the system penalizes a loss.\n' +
    '• Epsilon: Exploration rate (trying new things vs sticking to what works).'
```

The inputs that control it:

```pine
int   i_spaArms    = input.int(4, "Strategy Arms", ...)   // competing sub-strategies
float i_spaDecay   = input.float(0.95, "Memory Decay", ...)  // EMA-like forgetting
float i_spaTrauma  = input.float(2.0, "Trauma Factor", ...)  // loss penalty multiplier
float i_spaEpsilon = input.float(0.10, "Epsilon", ...)       // exploration probability
```

**How it works conceptually:**
- Each "arm" (sub-strategy) has a Beta distribution `Beta(α, β)` where α = wins, β = losses
- Each bar, sample from each arm's distribution
- Pick the arm with the highest sample
- If it wins, increment α; if it loses, increment β (×trauma)
- Epsilon% of the time, pick a random arm to explore

The system automatically shifts trust toward whichever strategy is working **in the current market regime** without you manually switching modes.

---

## 12. DSP Filters

**Files:** `MA-trix Laboratory `, `RSI: Evolved [DAFE].pine`

Digital Signal Processing filters remove high-frequency noise while preserving trend information. The collection implements several:

### Ehlers SuperSmoother (2-pole)

Available as a post-smoother in `MA-trix Laboratory `:

```pine
// SuperSmoother: Ehlers 2-pole filter
// Eliminates aliasing above Nyquist frequency while preserving trend
// Coefficient derivation from filter design theory:
//   a1 = exp(-1.414 * π / len)
//   b1 = 2 * a1 * cos(1.414 * 180 / len)
//   c2 = b1, c3 = -a1^2, c1 = 1 - c2 - c3
//   out = c1*(src + src[1])/2 + c2*out[1] + c3*out[2]
```

This is preferable to SMA/EMA because it has **zero lag at the filter cutoff** — unlike EMA which has phase shift at all frequencies.

### Laguerre Filter

A non-linear time-warping filter. Uses 4 poles (γ damping factor):

```pine
// Laguerre RSI uses Laguerre-transformed price series:
// L0 = (1-γ)*src + γ*L0[1]
// L1 = -γ*L0 + L0[1] + γ*L1[1]
// L2 = -γ*L1 + L1[1] + γ*L2[1]
// L3 = -γ*L2 + L2[1] + γ*L3[1]
// RSI-like calculation on L0-L3
```

The Laguerre transform **expands recent time** (more weight to recent bars) while **compressing older time** — adapting the effective lookback dynamically.

### Butterworth filter

A maximally flat frequency response in the passband:

```pine
// Available as "Butterworth MA" in MA-trix Laboratory
// 2-pole: no ripple in passband, sharp rolloff above cutoff
// Used when you need clean trend extraction without oscillation artifacts
```

**When to use which filter:**
- **SuperSmoother**: General noise reduction, responsive
- **Butterworth**: Clean trend line, minimal distortion
- **Laguerre**: Best lag/smoothness tradeoff for oscillators
- **Gaussian**: Maximum smoothness, accepts more lag

---

## 13. Adaptive Moving Averages

**File:** `MA-trix Laboratory `, `RSI: Evolved [DAFE].pine`

Adaptive MAs change their speed based on market conditions. Three key examples:

### KAMA (Kaufman Adaptive Moving Average)

Uses the Efficiency Ratio (ER) to adapt:

```pine
// Efficiency Ratio: how directionally efficient is price movement?
f_er(src, len) =>
    change_sum = math.sum(math.abs(src - src[1]), len)   // total path length
    math.abs(src - src[len]) / math.max(change_sum, 1e-10)  // direct distance / path

// ER near 1.0 = trending (all movement in one direction)
// ER near 0.0 = choppy (lots of movement, little net progress)

// KAMA fast/slow EMA factors:
// kama := kama[1] + (ER * (fast - slow) + slow)^2 * (src - kama[1])
```

When ER ≈ 1 (trending), KAMA behaves like a fast EMA. When ER ≈ 0 (ranging), it flattens. **No parameter tuning needed across different instruments.**

### Hull MA

Eliminates lag by using the difference between a fast and slow WMA:

```pine
// Hull MA = WMA(2*WMA(src, len/2) - WMA(src, len), sqrt(len))
// The 2*fast - slow trick cancels the lag of WMA
// Final WMA(sqrt(len)) smooths the result
```

Hull MA often looks "magical" to Pine beginners — it's nearly lag-free because the error-correction term (2×fast - slow) extrapolates ahead.

### VIDYA (Variable Index Dynamic Average)

Uses the Chande Momentum Oscillator (CMO) as the adaptive factor:

```pine
// CMO = (up_sum - dn_sum) / (up_sum + dn_sum) * 100
// VIDYA adapts based on momentum strength:
// vidya = src * k * |CMO/100| + vidya[1] * (1 - k * |CMO/100|)
// When momentum is high → VIDYA tracks price closely
// When momentum is low → VIDYA barely moves
```

---

## 14. Modular Algorithm Selection Pattern

**Files:** `MA-trix Laboratory `, `BandsandChannelsLaboratory.pine`, `RSI: Evolved [DAFE].pine`

The pattern for exposing 50+ algorithms through a single `input.string` dropdown:

### Step 1 — Define the array of options

```pine
var string[] MA_TYPES = array.from(
    "SMA", "EMA", "WMA", "VWMA", "RMA (Wilder)", "SMMA",
    "DEMA", "TEMA", "Hull MA", "ZLEMA", "ALMA", "T3 Tillson",
    "KAMA", "VIDYA", "FRAMA", "McGinley Dynamic", "Jurik (JMA)",
    // ... 55+ total
    "DAFE Flux Reactor", "DAFE Tensor Flow", "DAFE Quantum Step")
```

### Step 2 — Input with options list

```pine
i_ma1_type = input.string("EMA", "📊 MA1 (Primary/Fast) Type",
    options=["SMA", "EMA", "WMA", ...], group=g_ma_core, tooltip=TT_MA_TYPE)
```

### Step 3 — Dispatch function

The `f_get_ma(src, len, type)` function is a large if/else chain or switch that calls the correct implementation:

```pine
f_get_ma(series float src, int len, string ma_type) =>
    float result = na
    if ma_type == "SMA"
        result := ta.sma(src, len)
    else if ma_type == "EMA"
        result := ta.ema(src, len)
    else if ma_type == "Hull MA"
        float hma_half = ta.wma(src, math.max(len / 2, 1))
        float hma_full = ta.wma(src, len)
        result := ta.wma(2.0 * hma_half - hma_full, math.max(math.round(math.sqrt(len)), 1))
    else if ma_type == "KAMA"
        // ... KAMA implementation
    // ... 55+ branches
    result
```

This pattern — **define once, select via string** — means you can swap any algorithm in any position (MA1, MA2, MA3) with a single dropdown change. The indicator's logic remains identical regardless of which algorithm is selected.

---

## 15. Signal Filter Pipeline

**File:** `MA-trix Laboratory `

Professional indicators don't fire signals on every crossover — they gate signals through multiple confirming conditions. The filter pipeline pattern:

### Independent filter conditions

Each filter is computed separately and returns a boolean:

```pine
// Volume filter
bool vol_ok = true
if i_vol_enable
    float vol_avg = ta.sma(volume, i_vol_len)
    vol_ok := i_vol_mode == "Above Average"   ? volume > vol_avg :
              i_vol_mode == "Above Threshold" ? volume > vol_avg * i_vol_mult :
              i_vol_mode == "Climax Detection"? volume > vol_avg * 2.0 : true

// Volatility filter
bool volty_ok = true
if i_volatility_enable
    float atr_val = ta.atr(i_volatility_atr_len)
    float atr_avg = ta.sma(atr_val, 50)
    volty_ok := i_volatility_mode == "BB Expansion" ? atr_val > atr_avg : true

// Trend filter (ADX)
bool trend_ok = true
if i_trend_enable
    [diplus, diminus, adx] = ta.dmi(i_trend_adx_len, i_trend_adx_len)
    trend_ok := i_trend_mode == "Require Strong Trend" ? adx > i_trend_adx_thresh : true

// Momentum filter
bool mom_ok = true
if i_mom_enable
    float rsi_val = ta.rsi(close, i_mom_rsi_len)
    mom_ok := i_mom_mode == "RSI Confirmation" ? 
              (bull_signal ? rsi_val > i_mom_rsi_bull : rsi_val < i_mom_rsi_bear) : true

// Time cooldown filter
bool time_ok = bar_index - last_signal_bar >= i_min_bars
```

### Combined gate

```pine
bool filters_pass = not i_enable_filters or (vol_ok and volty_ok and trend_ok and mom_ok and time_ok)
bool final_bull   = raw_bull_signal and filters_pass
bool final_bear   = raw_bear_signal and filters_pass
```

This is the "AND gate" pattern — each filter must pass independently. The key insight is that each filter is **optional and independently toggleable** by the user, but the pipeline structure stays the same.

---

## 16. The Theme and Visualization Engine

**File:** `safe cuz lib.pine`

### Theme system

Every theme is a `Theme` UDT (9 colors). Usage:

```pine
Theme t = viz.get_theme("Neon Tokyo")
// t.bull = #00FF99 (neon green)
// t.bear = #FF3366 (neon red)
// t.bg   = #09000D (near-black background)
```

Available themes: Neon Tokyo, Ocean Depths, Arctic Aurora, Classic Terminal, Cyber, Matrix, Gold, Ice, Blood, DAFE Signature.

### Auto-configuration

The `auto_config()` function analyzes a data series and **automatically determines** the best plot style, colors, and zones:

```pine
export auto_config(series float src, string title, Theme t) =>
    MetricAnalysis a = analyze(src)     // fingerprint the data
    PlotConfig cfg = PlotConfig.new()
    // Select color based on data type
    color base_c = t.neu
    if a.data_type == "oscillator"
        base_c := a.norm_value < 50 ?
            color.from_gradient(a.norm_value, 0, 50, t.bear, t.neu) :
            color.from_gradient(a.norm_value, 50, 100, t.neu, t.bull)
    else if a.data_type == "momentum"
        base_c := src > 0 ? t.bull : t.bear
    // Select line width based on regime
    cfg.width := a.regime == "volatile" ? 3 : a.regime == "squeeze" ? 1 : 2
    // Select style based on data type
    if a.data_type == "oscillator"
        cfg.style := "line"
        cfg.show_zones := true
        cfg.z_hi := 70.0, cfg.z_lo := 30.0
    else if a.data_type == "volume"
        cfg.style := "columns"
    cfg
```

The `analyze()` function identifies whether data is an oscillator (0–100 bounded), momentum (centered on 0), price, or volume — then `auto_config` chooses appropriate visualization for each type.

### Gradient colors

```pine
// 2-point gradient: low=bear color, high=bull color
export gradient_color(float value, color c1, color c2) =>
    color.from_gradient(value, 0, 100, c1, c2)

// 3-point gradient: bear→neutral→bull
export gradient_3(float value, color c_low, color c_mid, color c_hi) =>
    value <= 50 ?
        color.from_gradient(value, 0, 50, c_low, c_mid) :
        color.from_gradient(value, 50, 100, c_mid, c_hi)
```

### Adaptive transparency

```pine
// Higher confidence (z-score extreme) = more opaque plot
export adaptive_alpha(float z_score, int base_alpha = 50) =>
    float intensity = math.min(math.abs(z_score) / 3.0, 1.0)
    int result_alpha = int(base_alpha * (1.0 - intensity))
    math.max(result_alpha, 0)
```

When the z-score is near 0, the plot is nearly transparent (base_alpha opacity). When z-score is extreme (±3+), the plot is fully opaque. This makes extreme readings visually "pop" without any manual threshold.

---

## 17. Elliott Wave Scoring

**File:** `Riemannian_Dreamer_Manifold_Engine.pine`

The Elliott mapper applies structural rules to the last 5 (impulse) or 3 (correction) wave tokens and scores their pattern quality.

### Impulse wave rules

```pine
f_impulse_score(WaveToken t1, WaveToken t2, WaveToken t3, WaveToken t4, WaveToken t5) =>
    bool bull = t1.direction==1 and t2.direction==-1 and t3.direction==1
             and t4.direction==-1 and t5.direction==1
    float score = 0.0
    if bull or bear
        float r2 = t2.magnitude / math.max(t1.magnitude, EPS)  // Wave 2 retracement
        float r3 = t3.magnitude / math.max(t1.magnitude, EPS)  // Wave 3 extension
        float r4 = t4.magnitude / math.max(t3.magnitude, EPS)  // Wave 4 retracement
        score := 40.0                                           // base: directions correct
        score += r2 >= 0.20 and r2 <= 0.95 ? 10.0 : 0.0       // wave 2 valid retracement
        score += r3 >= 0.60              ? 15.0 : 0.0           // wave 3 >= 60% of wave 1
        score += r4 >= 0.15 and r4 <= 0.85 ? 10.0 : 0.0       // wave 4 valid retracement
        score += t3.magnitude > t1.magnitude * 0.50 ? 10.0 : 0.0 // wave 3 not shortest
        bool noOverlap = bull ? t4.endPrice >= t1.endPrice * 0.99 : ...  // Elliott rule 1
        score += noOverlap ? 15.0 : 0.0
```

**Wave 3 authenticity** uses footprint data to confirm the impulse isn't a trap:

```pine
wave3Auth := clamp(
    clamp(t3.fpDeltaEff, 0.0, 1.0) * 0.24    // delta efficiency (real buying)
  + clamp((t3.vaAccept + 1.0)/2.0, 0.0, 1.0) * 0.20  // value area acceptance
  + clamp(t3.pocShift/2.0, 0.0, 1.0) * 0.15  // POC migrating in wave direction
  + clamp(t3.conviction, 0.0, 1.0) * 0.12    // institutional conviction
  + (1.0 - clamp(t3.absorptionRate, 0.0, 1.0)) * 0.09 // low absorption = clean move
  + clamp(t3.siegeBreakProb, 0.0, 1.0) * 0.20  // structural break confirmed
, 0.0, 1.0)
```

**Wave 5 terminal risk** flags exhaustion:

```pine
termRisk := clamp(
    t5.exhaustion * 0.28          // absorption + weak delta
  + t5.trap * 0.20                // delta opposing price direction
  + t5.siegeFailProb * 0.22       // structure likely to fail
  + ((t5.thirdPushFlag and t5.siegeHits >= 3) ? 0.12 : 0.0)  // 3rd test = exhaustion
  + ((t5.fpDeltaEff < t3.fpDeltaEff * 0.70) ? 0.10 : 0.0)   // weakening delta
  + ((t5.pocShift < t3.pocShift * 0.60) ? 0.08 : 0.0)        // weakening POC migration
, 0.0, 1.0)
```

This is what separates this Elliott mapper from basic pivot-counting tools: every wave quality assessment is backed by **order flow data**.

---

## 18. Multi-Timeframe Architecture

**File:** `Market Structure Lib`, `RSI: Evolved [DAFE].pine`

### Container types

The Market Structure Lib defines a hierarchy:

```pine
// Single timeframe
export type TimeframeStructure
    string                tf              = ""
    float                 poc             = na
    float                 vah             = na
    float                 val_            = na
    array<StructureLevel> levels          = na
    SiegeCorridor         res_corridor    = na
    SiegeCorridor         sup_corridor    = na
    float                 bias            = 0.0
    int                   last_update_bar = 0

// Multi-timeframe container (up to 4 timeframes)
export type MultiTFStructure
    TimeframeStructure tf1 = na
    TimeframeStructure tf2 = na
    TimeframeStructure tf3 = na
    TimeframeStructure tf4 = na
```

### Key principle: No `request.security()` inside loops

Pine's MTF calls must be at the top level, not inside functions called per-bar. The library pattern wraps this correctly — the library's `update_structure()` function takes pre-calculated values from the indicator's top level.

### Confluence zones

```pine
export type ConfluenceZone
    float  center      = na
    float  width       = 0.01
    int    tf_count    = 0      // how many timeframes have a level here
    float  strength    = 0.0
    string zone_type   = "neutral"
```

A confluence zone is where levels from multiple timeframes overlap. More timeframes agreeing on the same price level = stronger zone.

---

## 19. Candle Diagnostics (Wick Physics)

**File:** `safe cuz lib.pine`, `WHF - Wave Health and Failure v6`

### CandleDiag type

```pine
export type CandleDiag
    float body_pct    // Body as % of total candle range
    float upper_wick  // Upper wick as % of range
    float lower_wick  // Lower wick as % of range
    bool  is_doji     // body_pct < 10%
    bool  is_hammer   // lower_wick > 2x body
    bool  is_shooter  // upper_wick > 2x body
    bool  is_marubozu // body_pct > 85%
    string bias       // "bull", "bear", "neutral"
```

### diagnose_candle() function

```pine
export diagnose_candle() =>
    CandleDiag d = CandleDiag.new()
    float rng  = math.max(high - low, syminfo.mintick)
    float body = math.abs(close - open)
    float u_wick = high - math.max(open, close)
    float l_wick = math.min(open, close) - low
    d.body_pct   := body / rng * 100
    d.upper_wick := u_wick / rng * 100
    d.lower_wick := l_wick / rng * 100
    d.is_doji    := d.body_pct < 10
    d.is_hammer  := l_wick > body * 2 and u_wick < body * 0.5
    d.is_shooter := u_wick > body * 2 and l_wick < body * 0.5
    d.is_marubozu := d.body_pct > 85
    d.bias := close > open ? "bull" : close < open ? "bear" : "neutral"
    d
```

### Wick anomaly detection in WHF

The WPK (Wick Pressure Kernel) in WHF detects **statistically unusual wicks**:

```pine
// Z-score of wick size flags anomalous candle auction behavior
// Input parameter:
float i_wpkAnomalyZ = input.float(2.0, "Anomaly Z-Score Threshold", ...)
// "A Z-Score of 2.0 means the wick is in the top ~2.3% of historical wicks"
```

A large upper wick at resistance = aggressive selling absorbed by buyers (or vice versa). Clustering of anomalous wicks at the same price level = high-conviction zone.

---

## 20. Putting It All Together

The architecture of every major DAFE indicator follows this layered pattern:

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: RAW DATA                                      │
│  OHLCV + request.footprint() + request.security()      │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: FEATURE ENGINEERING                           │
│  Z-scores, Hurst exponent, delta ratios, absorption,   │
│  manifold coordinates, candle diagnostics               │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: STRUCTURAL ANALYSIS                           │
│  Pivot detection, WaveToken building, Siege corridors, │
│  Elliott wave scoring, market structure levels          │
├─────────────────────────────────────────────────────────┤
│  LAYER 4: INTELLIGENCE ENGINE                           │
│  World model (neural net), GRPO policy, Thompson       │
│  Sampling, Bayesian weighting, KNN classification      │
├─────────────────────────────────────────────────────────┤
│  LAYER 5: SIGNAL GENERATION                             │
│  Triadic verdict + threshold + filter pipeline         │
├─────────────────────────────────────────────────────────┤
│  LAYER 6: VISUALIZATION                                 │
│  Theme system, adaptive colors, labels, dashboard,     │
│  siege corridors, wave lines, geodesic projections     │
└─────────────────────────────────────────────────────────┘
```

### Key design principles to internalize

**1. Graceful degradation.** Every footprint/premium-data call has a fallback:
```pine
float fpBuy = nz(not na(fp) ? fp.buy_volume() : volume * (close - low) / rng, 0.0)
```

**2. `nz()` everywhere.** Any calculation involving division, `na`-possible series, or early bars must be wrapped:
```pine
float h = rs > 0 ? math.log(rs) / math.log(length) : 0.5
nz(clamp(h, 0.2, 0.8), 0.5)   // handles na AND clamps to valid range
```

**3. `var` for persistent state.** Neural network weights, arrays, regime states — use `var` to initialize once:
```pine
var float w00 = 1.0          // persists across all bars
var array<WaveToken> tokens  = array.new<WaveToken>()
```

**4. `barstate.isconfirmed` guard.** Computationally heavy updates (weight updates, array management, P&L evaluation) should only run on confirmed bars to avoid being re-triggered on repaints:
```pine
if barstate.isconfirmed
    // update neural network weights
    // evaluate trade jobs
    // run GRPO policy update
```

**5. Scale everything with ATR.** Any hardcoded price distance becomes wrong on a different instrument. Always divide by `atr14` or normalize with z-score:
```pine
float tol = atr14 * i_tolAtrMult      // NOT: tol = 5.0 (useless hardcode)
float atrMag = magnitude / math.max(atr14, syminfo.mintick)
```

**6. clamp() instead of naked math.** When combining multiple scored factors into a [0,1] range:
```pine
float breakProb = clamp(
    0.15 + dAlign*0.30 + pressure*0.20 + (1.0-decay)*0.10 + breakV/h*0.25,
    0.0, 1.0)
```

---

## Where to Go Next

Once you're comfortable with these patterns, the natural next step is building your own indicator on top of the library infrastructure:

1. **Import `DafeVisLib`** (`safe cuz lib.pine`) — get themes, auto-config, gradient colors for free
2. **Import `MarketStructureLib`** (`Market Structure Lib`) — get POC/VA, siege corridors, multi-TF structure
3. **Define your own `type`** for your indicator's state object
4. **Use z-scoring** to normalize your inputs — never hardcode thresholds
5. **Add a Hurst regime gate** — different behavior in trending vs ranging markets
6. **Build a filter pipeline** — volume, volatility, trend strength, momentum
7. **Add `barstate.isconfirmed` guards** around any stateful updates

The hallmark of master-level PineScript is not using more functions — it is **building systems that adapt to the instrument, timeframe, and market regime automatically**, without the user needing to retune parameters.
