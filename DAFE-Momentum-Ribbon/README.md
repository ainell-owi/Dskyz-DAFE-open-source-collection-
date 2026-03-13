# DAFE Momentum Ribbon

**Author:** Dskyz  
**Versions available:** v6  
**Type:** Overlay indicator  
**Recommended timeframes:** 1 h and above

---

## Overview

The **DAFE Momentum Ribbon** renders a multi-EMA ribbon directly on the price chart.  
Eight exponential moving averages — spaced logarithmically from a fast to a slow period — are plotted and colour-filled to reveal the current momentum phase at a glance.

The ribbon **fans out** during strong trends and **compresses** during consolidation, giving traders an intuitive read on trend strength without a separate sub-pane.

### Momentum State

| Ribbon Shape | Interpretation |
|-------------|----------------|
| All EMAs stacked (fast on top, slow on bottom) | Strong bullish momentum |
| All EMAs stacked (slow on top, fast on bottom) | Strong bearish momentum |
| EMAs crossing / overlapping | Ranging / momentum shift |

### Signals

| Signal | Condition |
|--------|-----------|
| 🔼 Momentum Up label | Fastest EMA crosses **above** the slowest EMA |
| 🔽 Momentum Down label | Fastest EMA crosses **below** the slowest EMA |

---

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Fast EMA | 8 | Shortest ribbon EMA period |
| Slow EMA | 89 | Longest ribbon EMA period |
| Signal Labels | true | Toggle crossover label display |
| Bull Color | Green | Ribbon fill when fast > slow |
| Bear Color | Red | Ribbon fill when fast < slow |

---

## How It Works

1. Eight EMA periods are interpolated between the **Fast** and **Slow** inputs.
2. Each EMA is plotted; fills are drawn between adjacent pairs.
3. Fill colours are determined by comparing the fastest EMA to the slowest EMA.
4. A crossover/crossunder of the two extreme EMAs fires the optional signal label.

---

## Usage Notes

- Best used on trending instruments (crypto, forex majors, indices).
- A tightly bunched ribbon in a range is a low-risk entry zone ahead of a breakout.
- Combine with the **DAFE Adaptive Trend Engine** for a confluence-based approach.

---

## Files

| File | Pine Script Version |
|------|---------------------|
| [`DAFE-Momentum-Ribbon_v6.pine`](./DAFE-Momentum-Ribbon_v6.pine) | v6 |
