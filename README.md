# Dskyz · DAFE Open-Source Collection

A curated collection of high-level [Pine Script](https://www.tradingview.com/pine-script-docs/) indicators and strategies written by **Dskyz**.

---

## 📂 Repository Structure

Each script lives in its own folder. The folder always contains:

| File | Purpose |
|------|---------|
| `README.md` | Description, inputs, signals, and usage notes |
| `<name>_v6.pine` | Pine Script **version 6** source |
| `<name>_v5.pine` *(optional)* | Pine Script **version 5** source (included when a back-port is provided) |

```
Dskyz-DAFE-open-source-collection-/
├── README.md                          ← you are here
│
├── DAFE-Adaptive-Trend-Engine/
│   ├── README.md
│   ├── DAFE-Adaptive-Trend-Engine_v6.pine
│   └── DAFE-Adaptive-Trend-Engine_v5.pine
│
└── DAFE-Momentum-Ribbon/
    ├── README.md
    └── DAFE-Momentum-Ribbon_v6.pine
```

---

## 📜 Scripts

| Script | v5 | v6 | Description |
|--------|----|----|-------------|
| [DAFE-Adaptive-Trend-Engine](./DAFE-Adaptive-Trend-Engine/) | ✅ | ✅ | ATR-adaptive trend channel with bull/bear signals |
| [DAFE-Momentum-Ribbon](./DAFE-Momentum-Ribbon/) | — | ✅ | Multi-EMA momentum ribbon with gradient coloring |

---

## 🚀 How to Use

1. Open [TradingView](https://www.tradingview.com/) and navigate to the **Pine Editor** (`/pine-editor`).
2. Copy the contents of the desired `.pine` file.
3. Paste into the Pine Editor and click **Add to chart**.

> **Tip:** Use the **v6** file whenever possible — v6 scripts benefit from the latest Pine Script features and optimisations.

---

## 📄 License

Released under the [MIT License](./LICENSE). Feel free to study, modify, and share.
