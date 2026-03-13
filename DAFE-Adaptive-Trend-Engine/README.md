# DAFE Adaptive Trend Engine

**Author:** Dskyz  
**Versions available:** v5 · v6  
**Type:** Overlay indicator  
**Recommended timeframes:** 15 m and above

---

## Overview

The **DAFE Adaptive Trend Engine** plots an ATR-adaptive trend channel directly on the price chart.  
The channel centre is a smoothed EMA; the upper and lower bands expand and contract in real-time with the Average True Range, keeping the channel proportional to current volatility.

A colour-coded ribbon between the bands indicates the prevailing trend:

- 🟢 **Green** — bullish trend (price above centre EMA)  
- 🔴 **Red** — bearish trend (price below centre EMA)

### Signals

| Signal | Condition |
|--------|-----------|
| 🔼 Buy label | Price closes **above the upper band** from below |
| 🔽 Sell label | Price closes **below the lower band** from above |

---

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| EMA Length | 50 | Lookback period for the centre EMA |
| ATR Length | 14 | Lookback period for the ATR |
| ATR Multiplier | 2.0 | Scales the band width relative to ATR |
| Signal Labels | true | Toggle buy/sell label display |

---

## How It Works

1. A 50-period EMA is calculated on the closing price.
2. The ATR is calculated and multiplied by the `ATR Multiplier`.
3. Upper band = EMA + (ATR × multiplier); Lower band = EMA − (ATR × multiplier).
4. The fill between the bands is coloured based on whether the close is above or below the EMA.
5. Crossover/crossunder of the bands triggers optional signal labels.

---

## Usage Notes

- Works best on liquid assets with clear trending phases (e.g. major crypto pairs, indices, large-cap equities).
- Widen the `ATR Multiplier` on noisy, ranging markets to reduce false signals.
- Combine with a volume filter or a momentum oscillator to increase conviction.

---

## Files

| File | Pine Script Version |
|------|---------------------|
| [`DAFE-Adaptive-Trend-Engine_v6.pine`](./DAFE-Adaptive-Trend-Engine_v6.pine) | v6 |
| [`DAFE-Adaptive-Trend-Engine_v5.pine`](./DAFE-Adaptive-Trend-Engine_v5.pine) | v5 |
