# Repository Organization Guide

> **Attribution Notice:** The Pine Script indicators and libraries referenced in this guide were authored by **Dskyz** (DAFE Trading Systems). This repository and guide are maintained by a third party with no affiliation to Dskyz Investments or DAFE Trading Systems. Official website: [dafetradingsystems.com](https://www.dafetradingsystems.com)

> Recommendations for structuring, naming, and growing the DAFE Open-Source Collection as it expands.

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [Recommended Folder Structure](#2-recommended-folder-structure)
3. [File Naming Conventions](#3-file-naming-conventions)
4. [Documentation Standards](#4-documentation-standards)
5. [Adding a New Indicator](#5-adding-a-new-indicator)
6. [Adding a New Library](#6-adding-a-new-library)
7. [Versioning Strategy](#7-versioning-strategy)
8. [README Maintenance Checklist](#8-readme-maintenance-checklist)
9. [Known Issues in the Current Repo](#9-known-issues-in-the-current-repo)

---

## 1. Current State Assessment

### What Works Well
- Every major indicator has a dedicated markdown documentation file written in consistent style
- The shared library architecture (`DafeVisLib`, `Market Structure Lib`) is cleanly separated from individual indicators
- Documentation is detailed, technically accurate, and follows a consistent philosophy section → algorithm tour → module guide → best practices structure

### What Needs Improvement
- **Flat structure**: All 14 files sit at the root with no subfolders. As the collection grows beyond ~20 files, navigation becomes difficult
- **Inconsistent file names**: Some files lack extensions (e.g., `MA-trix Laboratory`, `Market Structure Lib`) and some have literal newline bytes (ASCII 0x0A) embedded directly in their filesystem names — not just displayed whitespace. This is confirmed by inspecting the raw bytes of `ls` output and is a filesystem artifact from how they were originally created
- **Minimal README**: The original README was only 2 lines. (Now fixed.)
- **No metadata**: Markdown files have no frontmatter, making it harder for tools (AI studio, static site generators, search) to categorize them
- **No version tags**: There is no clear indication of which Pine Script version (v5/v6) each file targets, or what TradingView release version they correspond to

---

## 2. Recommended Folder Structure

As the collection grows, organize files into this structure:

```
Dskyz-DAFE-open-source-collection-/
│
├── README.md                          ← Collection overview (keep at root)
├── LEARNING_GUIDE.md                  ← Primary educational resource (keep at root)
├── GOOGLE_AI_STUDIO_GUIDE.md          ← AI training guide (keep at root)
├── ORGANIZATION_GUIDE.md              ← This file (keep at root)
├── LICENSE                            ← License (keep at root)
│
├── indicators/                        ← Standalone TradingView indicators
│   ├── momentum/
│   │   ├── RSI_Evolved_DAFE.pine
│   │   ├── RSI_Evolved_DAFE.md
│   │   └── Tick_Asymmetry_Index.pine
│   ├── volatility/
│   │   ├── BandsandChannelsLaboratory.pine
│   │   ├── BandsandChannelsLaboratory.md
│   │   └── WHF_Wave_Health_Failure_v6.pine
│   ├── structure/
│   │   ├── MA_trix_Laboratory.pine
│   │   └── 369.pine
│   └── experimental/
│       └── Riemannian_Dreamer_Manifold_Engine.pine
│
├── libraries/                         ← Shared Pine Script libraries
│   ├── DafeVisLib.pine
│   ├── DafeVisLib.md
│   ├── MarketStructureLib.pine
│   └── MarketStructureLib.md
│
├── docs/                              ← Supplementary documentation
│   ├── images/                        ← Screenshots, charts, diagrams
│   └── examples/                      ← Example setups and strategy configs
│
└── ai-training/                       ← AI Studio training data
    ├── knowledge-base/                ← Curated files for AI grounding
    │   └── (symlinks or copies of key .md files)
    └── training-pairs.jsonl           ← Fine-tuning Q&A pairs
```

### Why This Structure?
- **`indicators/` subfolders** group tools by analytical category. When you have 30+ indicators, being able to open the `momentum/` folder and see only momentum tools is much faster than scanning a flat list
- **`libraries/`** separates reusable code from standalone scripts, making it immediately clear which files are imports vs. standalone indicators
- **`docs/images/`** provides a home for screenshots, which dramatically improve documentation quality without cluttering the root
- **`ai-training/`** keeps AI-specific files organized and separate from the core source code

---

## 3. File Naming Conventions

### Pine Script Files
Use `Snake_Case_With_Capitals.pine` format, matching how TradingView names exported scripts:

| ❌ Current (Problematic) | ✅ Recommended |
|---|---|
| `RSI: Evolved [DAFE].pine` (special chars) | `RSI_Evolved_DAFE.pine` |
| `BandsandChannelsLaboratory.pine` | `BandsandChannelsLaboratory.pine` ✓ (already good) |
| `MA-trix Laboratory` (no extension) | `MA_trix_Laboratory.pine` |
| `Market Structure Lib` (no extension) | `MarketStructureLib.pine` |
| `DafeVis Lib` (no extension, newline) | `DafeVisLib.pine` |
| `Tick Asymmetry Index` (no extension) | `Tick_Asymmetry_Index.pine` |
| `WHF - Wave Health and Failure v6` | `WHF_Wave_Health_Failure_v6.pine` |
| `369` (no extension) | `369_Cyclical_Framework.pine` |

**Rules:**
1. Always include the `.pine` extension
2. No spaces in filenames — use underscores
3. No special characters (`: [ ] -`) in filenames
4. No embedded newline characters (a known issue with some current files)
5. Version numbers go at the end: `WHF_Wave_Health_Failure_v6.pine`

### Markdown Documentation Files
Each indicator/library gets exactly one `.md` file with the same base name:

```
BandsandChannelsLaboratory.pine    →    BandsandChannelsLaboratory.md
RSI_Evolved_DAFE.pine              →    RSI_Evolved_DAFE.md
DafeVisLib.pine                    →    DafeVisLib.md
```

---

## 4. Documentation Standards

Every indicator's markdown file should follow this template:

```markdown
---
title: "Indicator Name [DAFE]"
type: "Indicator"           # or "Library"
category: "Momentum"        # Momentum / Volatility / Structure / Experimental
pine_version: "v5"          # or v6
status: "Stable"            # Stable / Beta / Experimental
tags: ["tag1", "tag2"]
---

# Indicator Name [DAFE]: Subtitle

> One-sentence summary.

## Philosophy
...

## What Makes This Different
...

## Algorithm Library / Core Concepts
...

## Key Modules
...

## Recommended Starting Configuration
...

## Best Practices & Disclaimer
...

## Questions This Document Can Answer
- Question 1?
- Question 2?
```

The **Questions This Document Can Answer** section is optional but highly recommended if you plan to use the repo with Google AI Studio grounding (see `GOOGLE_AI_STUDIO_GUIDE.md`).

---

## 5. Adding a New Indicator

Follow this checklist when adding a new indicator to the collection:

- [ ] **Name the file correctly**: `IndicatorName_Category.pine` — no spaces, no special characters, `.pine` extension
- [ ] **Place it in the right subfolder**: `indicators/momentum/`, `indicators/volatility/`, `indicators/structure/`, or `indicators/experimental/`
- [ ] **Add a file-level comment block** at the top of the Pine Script:
  ```pine
  // ============================================================
  // Indicator Name [DAFE]
  // Version: 1.0
  // Author: Dskyz (DAFE Trading Systems)
  // Category: Momentum / Volatility / Structure
  // Pine Script Version: v5
  // Description: One paragraph description of what this does.
  // ============================================================
  ```
- [ ] **Write a documentation file**: `IndicatorName.md` following the template in Section 4
- [ ] **Update README.md**: Add a row to the File Inventory table
- [ ] **Update LEARNING_GUIDE.md**: Add a subsection under the appropriate category
- [ ] **Update `ai-training/knowledge-base/`**: Copy or symlink the new `.md` file
- [ ] **Add Q&A pairs**: Add 5–10 training examples to `ai-training/training-pairs.jsonl`

---

## 6. Adding a New Library

Libraries are different from indicators — they are imported by other scripts, not run standalone.

- [ ] **Place in `libraries/` folder**
- [ ] **Declare with `library()` in Pine Script**, not `indicator()`
- [ ] **Export every public function** using the `export` keyword
- [ ] **Document every exported function** with a comment block immediately before the function:
  ```pine
  // @function calculateSomething
  // @param source <series float> The price source to calculate on
  // @param length <int> Lookback period
  // @returns <series float> The calculated value
  export calculateSomething(series float source, simple int length) =>
      ...
  ```
- [ ] **Write a documentation file**: Explain what the library provides, usage examples, and all exported functions
- [ ] **Update README.md**: Add to File Inventory table with Type = "Library"

---

## 7. Versioning Strategy

### For Indicators
Use version comments in the Pine Script header and increment when making significant changes:

```pine
// Version: 1.0   Initial release
// Version: 1.1   Added MTF Dashboard
// Version: 2.0   Migrated to Pine Script v6, full rewrite of signal engine
```

Use GitHub **releases** (or git **tags**) to mark stable versions of the whole collection:
- `v1.0.0` — first stable release of the collection
- `v1.1.0` — new indicator added
- `v1.0.1` — bug fix to existing indicator

### For Libraries
Libraries published to TradingView have explicit version numbers in their import path:
```pine
import DskyzInvestments/DafeVisualsLib/1 as viz
//                                      ^ version number
```

Increment this number (and update all importers) when making breaking changes to a library's exported API.

---

## 8. README Maintenance Checklist

Run through this checklist whenever you make changes to the repo:

- [ ] **File Inventory table** — does every file in the repo have a row?
- [ ] **Links in Further Reading** — do all linked files still exist with the correct names?
- [ ] **6-Step Learning Path** — does it still make sense given the current set of files? If you added an important new tool, should it be in the learning path?
- [ ] **Concept Quick-Reference table** — are all major concepts in the collection represented?

---

## 9. Known Issues in the Current Repo

These are known filesystem/naming issues in the repository as of the current state. Address these when possible:

| File | Issue | Fix |
|---|---|---|
| `DafeVis Lib` | One literal newline byte (0x0A) embedded in the filename itself; no `.pine` extension | Rename to `DafeVisLib.pine` |
| `RSI: Evolved [DAFE].pine` | Special characters (`: [ ]`) **and** two literal newline bytes (0x0A) embedded in the filename itself | Rename to `RSI_Evolved_DAFE.pine` |
| `MA-trix Laboratory` | No `.pine` extension | Rename to `MA_trix_Laboratory.pine` |
| `Market Structure Lib` | No `.pine` extension | Rename to `MarketStructureLib.pine` |
| `Tick Asymmetry Index` | No `.pine` extension | Rename to `Tick_Asymmetry_Index.pine` |
| `WHF - Wave Health and Failure v6` | Spaces and dashes; no extension | Rename to `WHF_Wave_Health_Failure_v6.pine` |
| `369` | No extension; ambiguous name | Rename to `369_Cyclical_Framework.pine` |

> **Important:** Before renaming files, check whether any of these filenames are referenced in TradingView's Published Scripts system. TradingView uses its own internal IDs, so renaming the local file won't break TradingView links — but any manual cross-references in documentation will need to be updated.

---

*Scripts authored by Dskyz (DAFE Trading Systems) — [dafetradingsystems.com](https://www.dafetradingsystems.com). This guide is maintained by a third party with no affiliation to the original author.*
