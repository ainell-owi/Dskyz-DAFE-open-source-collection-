# Copilot Instructions — Dskyz DAFE Open-Source Collection

## Repository Overview

This is a **PineScript trading-indicator ecosystem** published by Dskyz (ainell-owi). It contains institutional-grade TradingView indicators and libraries: manifold-geometry engines, reinforcement-learning world models, DSP filters, 55+ moving averages, 30+ RSI engines, 40+ volatility algorithms, and multi-timeframe order-flow integration.

There is **no build system, test runner, or CI pipeline**. PineScript is compiled and executed exclusively inside the TradingView platform. There are no `npm`, `pip`, `make`, or shell scripts to run. Do not attempt to install dependencies or build the code locally.

---

## Language & Runtime

| Property | Value |
|----------|-------|
| Primary language | PineScript v5 and v6 |
| Runtime | TradingView platform (cloud) |
| Documentation | Markdown (`.md`) |
| No other languages | No JavaScript, Python, or shell scripts |

---

## Repository Layout

```
/                                      ← repo root
├── .github/
│   └── copilot-instructions.md        ← this file
├── BandsandChannelsLaboratory.pine    ← Indicator v5 — 40+ volatility algorithms
├── Bands and Channels Laboratory.md  ← Manual for the above
├── DafeVis Lib                        ← Library — extended visualization & dashboard
├── LEARNING_GUIDE.md                  ← Master-level PineScript patterns guide (primary doc)
├── LICENSE                            ← MIT
├── MA-trix Laboratory                 ← Indicator v5 — 55+ moving average algorithms
├── Market Structure Lib               ← Library v5 — multi-TF market architecture
├── README.md                          ← File inventory + learning path
├── RSI: Evolved [DAFE].pine           ← Indicator v5 — 30+ RSI engines + MTF dashboard
├── RSI:evolved.md                     ← Manual for the above
├── Riemannian_Dreamer_Manifold_Engine.pine  ← Indicator v6 — flagship, RL + geometry
├── Tick Asymmetry Index               ← Indicator — order-flow TAI
├── WHF - Wave Health and Failure v6   ← Indicator v6 — ML + Thompson Sampling
├── 369                                ← Indicator — Gann geometry + Bayesian KNN + Hurst
└── safe cuz lib.pine                  ← Library v5 — DafeVisLib themes, candle diagnostics
```

Files without a `.pine` extension are also PineScript source files (TradingView allows arbitrary filenames). Some documentation files have spaces in their names (e.g., `Bands and Channels Laboratory.md`) while the corresponding Pine files do not (e.g., `BandsandChannelsLaboratory.pine`) — this is an existing pattern in the repo.

---

## PineScript Conventions Used in This Repo

### Version declaration
Every file starts with one of:
```pine
//@version=5
//@version=6
```
`request.footprint()` (order-flow data) is only available in v6. Files that use it must declare `//@version=6`.

### User-Defined Types (UDTs)
UDTs are the central design pattern. Use `type` (or `export type` in libraries) to define structs:
```pine
export type Theme
    color p         // Primary accent
    color s         // Secondary accent
    color bull      // Bullish state
    color bear      // Bearish state
```
Always use `TypeName.new()` to instantiate. Default field values are set in the type declaration.

### Library system
```pine
//@version=5
library("DafeVisLib", overlay=true)

export get_theme(string name) => ...
```
Consumers import with:
```pine
import DskyzInvestments/DafeVisLib/1 as viz
Theme t = viz.get_theme("Neon Tokyo")
```

### Naming conventions
- Functions: `snake_case` for most (e.g., `zscore`, `auto_config`); functions with the `f_` prefix use camelCase after the prefix (e.g., `f_hurstExponent`, `f_impulse_score`)
- Types: `PascalCase` (e.g., `Theme`, `StructureLevel`, `WaveToken`)
- Variables: `camelCase` or `snake_case`
- Constants / series: `ALL_CAPS` is rare; most constants are plain `var float`

### Array ring-buffer pattern
```pine
var float[] buf = array.new_float(length, 0.0)
array.push(buf, value)
if array.size(buf) > length
    array.shift(buf)
```

### Guard pattern for confirmed bars
```pine
if barstate.isconfirmed
    // expensive calculations here
```

### Comment style
```pine
// @function description — single line
// @type description — for UDT declarations
```

---

## Key Algorithms & Where to Find Them

| Concept | File |
|---------|------|
| `export type` UDTs | `safe cuz lib.pine`, `Market Structure Lib` |
| `library()` / `import` / `export` | `safe cuz lib.pine`, `Market Structure Lib` |
| Dynamic arrays as ring buffers | `Riemannian_Dreamer_Manifold_Engine.pine` |
| `request.footprint()` order flow | `Riemannian_Dreamer_Manifold_Engine.pine`, `Tick Asymmetry Index` |
| Z-score normalization (`zscore()`) | `Riemannian_Dreamer_Manifold_Engine.pine` |
| Hurst exponent (`f_hurstExponent()`) | `Riemannian_Dreamer_Manifold_Engine.pine` |
| Ricci curvature approximation | `Riemannian_Dreamer_Manifold_Engine.pine` |
| Neural network forward pass + weight update | `WHF - Wave Health and Failure v6` |
| Thompson Sampling bandit | `WHF - Wave Health and Failure v6` |
| GRPO policy optimization | `Riemannian_Dreamer_Manifold_Engine.pine` |
| DSP filters (Butterworth, SuperSmoother) | `MA-trix Laboratory`, `RSI: Evolved [DAFE].pine` |
| Multi-timeframe structure | `Market Structure Lib`, `RSI: Evolved [DAFE].pine` |
| Adaptive color themes (`get_theme()`) | `safe cuz lib.pine` |
| Auto plot configuration (`auto_config()`) | `safe cuz lib.pine` |
| Signal filter pipeline | `MA-trix Laboratory`, `BandsandChannelsLaboratory.pine` |
| Elliott Wave scoring (`f_impulse_score()`) | `Riemannian_Dreamer_Manifold_Engine.pine` |

---

## How to Work on This Repository

1. **Editing Pine Script**: All `.pine` files and extension-less files in the root are PineScript source. Edit them as plain text.
2. **No local validation**: There is no linter or compiler available locally. Syntax correctness can only be verified by pasting into TradingView's Pine Editor.
3. **Documentation**: Update the relevant `.md` file alongside any indicator change. `LEARNING_GUIDE.md` is the master educational reference and `README.md` is the file inventory.
4. **Adding a new indicator**: Add the file to the root, register it in the `README.md` table, and add relevant entries to `LEARNING_GUIDE.md`.
5. **Adding a new library**: Follow the `safe cuz lib.pine` pattern — `library()` declaration, `export type` for all shared types, `export` for all public functions.
6. **No build artifacts to ignore**: There are no `node_modules`, `dist`, or compiled output directories.
