# Dskyz DAFE — Open-Source Pine Script Collection

> **DAFE** — *Dynamic Adaptive Forecasting Engine*
>
> A curated collection of Pine Script v6 indicators built on the DAFE
> framework.  Each script leverages machine-learning, Bayesian inference, and
> advanced market-structure logic to produce high-confidence, adaptive trading
> signals.

---

## 📁 Repository Structure

```
.
├── scripts/                        # Pine Script v6 source files (.pine)
│   ├── 369-vector-equilibrium.pine # 369 Vector Equilibrium [DAFE]
│   └── whf-wave-health-failure.pine # WHF — Wave Health & Failure Engine
├── tools/                          # Python data-collection & comparison utilities
│   ├── collect_data.py             # Parses .pine files → JSON metadata report
│   ├── compare_repos.py            # Compares local scripts vs GitHub ecosystem
│   └── requirements.txt            # Python dependencies (requests)
├── docs/                           # Generated reports (git-ignored by default)
│   └── collected_metadata.json     # Output of collect_data.py
├── .gitignore
├── LICENSE
└── README.md
```

> **Legacy files** (`369` and `WHF - Wave Health and Failure v6`) are kept at
> the repo root for backward-compatibility.  The canonical copies with proper
> `.pine` extensions live under `scripts/`.

---

## 🗂 Scripts

### ⬡ 369 Vector Equilibrium \[DAFE\]
`scripts/369-vector-equilibrium.pine` — 802 lines — Pine Script v6

A standalone overlay indicator combining sacred geometry (Rodin/369 coil
resonance, Gann angles) with modern quantitative techniques:

| Section | Description |
| --- | --- |
| 🎛️ INPUTS | 51 configurable inputs across 8 groups |
| 🎨 COLOR THEME SYSTEM | Multi-theme visual engine |
| ⚙️ UTILITY FUNCTIONS | Math/geometry helpers |
| 📐 CORE SERIES | EMA-based vector & equilibrium series |
| 📊 FOOTPRINT DELTA ENGINE | Tick-level order-flow pressure delta |
| 🔬 WPK REGIME ENGINE | Hurst exponent + DFA regime detection |
| 🔱 SINE-WEIGHTED PITCHFORK ENGINE | Harmonic Fibonacci pitchforks |
| 🧠 MEMORY BANK (KNN ENGINE) | k-Nearest-Neighbour signal voting |
| 🌡️ HEATMAP ENGINE | Sparse-decay angular/pressure heatmap |
| 🎯 SIGNAL GATING ENGINE | Bayesian multi-factor signal filter |
| 🎨 VISUAL ENGINE | Plots, bubbles, particles, ribbons, Gann rays |
| 🖥️ PROFESSIONAL DASHBOARD | On-chart HUD table |

**Key features:** no external library imports (fully self-contained),
Bayesian-weighted signal compositing, KNN memory voting, WPK regime
modulation, Hurst R/S analysis, Gann angular geometry.

---

### ⚡ WHF — Wave Health & Failure Engine
`scripts/whf-wave-health-failure.pine` — 768 lines — Pine Script v6

A neural-adaptive overlay indicator built on 7 DAFE shared libraries:

| Library Import | Alias | Purpose |
| --- | --- | --- |
| `DskyzInvestments/DafeRLMLLib/1` | `ml` | Reinforcement-learning / ML engine |
| `DskyzInvestments/DafeSPALib/1` | `spa` | Strategic Policy Allocation |
| `DskyzInvestments/DafeMLSPABridge/1` | `bridge` | ML ↔ SPA integration bridge |
| `DskyzInvestments/WickPressureLib/1` | `wpk` | Wick-physics pressure analysis |
| `DskyzInvestments/DafePatternsLib/1` | `pattern` | Neural pattern recognition |
| `DskyzInvestments/DafeVisLib/1` | `viz` | Shared visualisation library |
| `DskyzInvestments/DafeDashboardLib/1` | `dafe` | Shared dashboard / HUD library |

**Core thesis:** *Assume failure until proven healthy.*  Failed moves are
first-class signals, not noise.

**Key features:** 46 inputs, 7 alert conditions, Thompson-sampling ML
integration, SPA multi-arm bandit strategy selection, wick-physics regime
detection, neural zigzag, health trail, candle colouring, AI assistant panel.

---

## 🛠 Tools

### `tools/collect_data.py` — Pine Script Metadata Collector

Parses every `.pine` file in `scripts/` and extracts structured metadata —
version, title, inputs, library imports, sections, visual features, resource
limits, and more.  Outputs `docs/collected_metadata.json`.

```bash
# Install dependencies (one-time)
pip install -r tools/requirements.txt

# Run the collector
python tools/collect_data.py

# Custom paths
python tools/collect_data.py \
  --scripts-dir scripts/ \
  --output docs/collected_metadata.json
```

**Output fields per script:**
`pine_version`, `script_type`, `title`, `shorttitle`, `overlay`,
`line_count`, `blank_lines`, `comment_lines`, `limits`, `imports`,
`inputs` (total, by_type, groups, labels), `sections`, `features`
(var_declarations, plot_calls, table_new_calls, alert_calls, …).

---

### `tools/compare_repos.py` — GitHub Ecosystem Comparator

Searches GitHub for public Pine Script v6 indicator files and generates a
Markdown comparison report showing how the DAFE scripts compare against the
broader ecosystem (line count, imports, inputs, ML usage, alerts, tables, etc.).

```bash
# With a GitHub personal access token (recommended — higher rate limits)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
python tools/compare_repos.py

# Without a token (10 req/min limit — slower)
python tools/compare_repos.py --max-repos 10

# Custom options
python tools/compare_repos.py \
  --token ghp_xxxx \
  --query "knn bayesian" \
  --max-repos 30 \
  --output docs/comparison_report.md \
  --json
```

**Options:**

| Flag | Default | Description |
| --- | --- | --- |
| `--token` | `$GITHUB_TOKEN` | GitHub PAT for higher rate limits |
| `--query` | _(empty)_ | Extra keywords added to the search |
| `--max-repos` | `20` | Max remote scripts to analyse |
| `--local-dir` | `scripts/` | Directory containing your `.pine` files |
| `--output` | `docs/comparison_report.md` | Output Markdown file |
| `--json` | _(off)_ | Also write raw data as `.json` |

The report includes:
- Local scripts summary table
- GitHub ecosystem averages (line count, import rate, input count, ML/table/alert penetration)
- Per-script comparison with delta vs ecosystem mean

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/ainell-owi/Dskyz-DAFE-open-source-collection-
cd Dskyz-DAFE-open-source-collection-

# 2. Install Python deps
pip install -r tools/requirements.txt

# 3. Collect metadata
python tools/collect_data.py

# 4. Compare against GitHub ecosystem
export GITHUB_TOKEN=<your_token>
python tools/compare_repos.py
```

---

## 📜 License

See [LICENSE](LICENSE).
