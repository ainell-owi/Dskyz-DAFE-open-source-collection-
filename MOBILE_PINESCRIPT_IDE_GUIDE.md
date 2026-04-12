# Mobile PineScript v6 IDE — GitHub Repository Research Guide

> **Research Goal:** Identify GitHub repositories that allow users to code PineScript version 6 in an IDE running on a phone (Android or iOS).

---

## Summary

There is currently **no dedicated, feature-complete PineScript v6 IDE app** for phones on GitHub or in app stores. However, a practical mobile workflow is achievable by combining:

1. A **general-purpose mobile code editor** (with optional custom syntax support)
2. A **PineScript v6 syntax/language resource** (grammar file or reference repo)
3. TradingView's **mobile web editor** for compilation and execution

The repositories below are the best available matches, organized by category.

---

## Table of Contents

1. [Mobile Code Editor Apps](#1-mobile-code-editor-apps)
2. [PineScript v6 Language Tools (Desktop/Portable)](#2-pinescript-v6-language-tools)
3. [PineScript v6 Reference Repositories](#3-pinescript-v6-reference-repositories)
4. [Recommended Mobile Workflow](#4-recommended-mobile-workflow)
5. [iOS Notes](#5-ios-notes)

---

## 1. Mobile Code Editor Apps

These are the most capable open-source code editor apps for phones found on GitHub. None ship with built-in PineScript v6 support, but each supports extensible syntax highlighting that can be adapted for Pine.

---

### 🥇 Acode — `Acode-Foundation/Acode`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/Acode-Foundation/Acode |
| **Platform** | Android |
| **Language** | JavaScript |
| **Stars** | ~5,000 |
| **License** | GPLv3 |
| **Last Active** | 2025–2026 |

**Why it matters for PineScript v6:**
- Plugin system allows adding **custom language syntax definitions** using Ace Editor grammar rules
- 100+ languages supported out of the box; Pine can be added via a plugin
- [Plugin SDK / template](https://github.com/Acode-Foundation/acode-plugin) is publicly documented
- GitHub integration, FTP/SFTP remote editing, multi-file project support
- The most mature and widely-used open-source mobile IDE for Android

**How to add PineScript syntax:** Create an Acode plugin that registers Pine Script as a language in Ace Editor, adapting the keyword and token lists from the VS Code extensions listed in Section 2.

---

### 🥈 Xed-Editor — `Xed-Editor/Xed-Editor`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/Xed-Editor/Xed-Editor |
| **Platform** | Android |
| **Language** | Java |
| **Stars** | 1,847 |
| **License** | GPL |
| **Last Active** | April 2026 (actively maintained) |
| **Topics** | `mobile-ide`, `code-editor-mobile`, `android-app` |

**Why it matters for PineScript v6:**
- Actively maintained full-featured mobile IDE tagged `mobile-ide` on GitHub
- Supports custom text/code editing with syntax rules
- Good for writers who want a lightweight Android IDE without heavy plugin overhead

---

### 🥉 Visual-Code-Space — `Visual-Code-Space/Visual-Code-Space`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/Visual-Code-Space/Visual-Code-Space |
| **Platform** | Android |
| **Language** | Kotlin (Jetpack Compose) |
| **Stars** | 623 |
| **License** | GPL |
| **Last Active** | April 2026 |
| **Topics** | `mobile-ide`, `code-editor`, `ai`, `kotlin` |

**Why it matters for PineScript v6:**
- Modern Jetpack Compose UI; AI code-generation support built in
- Tagged `mobile-ide`; actively maintained
- AI integration could assist with Pine Script code suggestions even without native Pine syntax support

---

## 2. PineScript v6 Language Tools

These repositories provide PineScript v6 syntax definitions, language server features, and IDE integrations. Although primarily designed for desktop editors, their **grammar files and keyword lists can be ported** to a mobile editor plugin.

---

### `jpantsjoha/pinescript-vscode-extension`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/jpantsjoha/pinescript-vscode-extension |
| **Platform** | VS Code (desktop) |
| **Language** | TypeScript |
| **Stars** | 19 |
| **Description** | Comprehensive PineScript **v6** support: IntelliSense-quality completions, parameter hints, syntax highlighting, rich documentation |
| **Last Active** | March 2026 |

**Key asset:** The TextMate grammar (`.tmLanguage.json`) and completion provider inside this extension define the full v6 keyword set. This grammar file can be extracted and loaded into mobile editors that support TextMate grammars (e.g., Acode via plugin).

---

### `revanthpobala/pinescript-vscode-extension`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/revanthpobala/pinescript-vscode-extension |
| **Platform** | VS Code (desktop) |
| **Language** | TypeScript |
| **Stars** | 15 |
| **Description** | Linter, syntax highlighter, auto-complete for TradingView's Pine Script |
| **Last Active** | March 2026 |

An alternative/fork with linting support. Useful as a second source for keyword lists and grammar rules.

---

### `deepentropy/intellij-pinescript`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/deepentropy/intellij-pinescript |
| **Platform** | IntelliJ IDEA / JetBrains (desktop) |
| **Language** | Java |
| **Stars** | 10 |
| **Description** | PineScript **v6** Language Support plugin for IntelliJ IDEA |
| **Last Active** | March 2026 |

**Key asset:** Includes a JFlex/PSI lexer and grammar for PineScript v6. The grammar definitions are language-agnostic enough to be referenced when writing a custom syntax mode for a mobile editor.

---

## 3. PineScript v6 Reference Repositories

These repositories do not provide IDE functionality but serve as **authoritative v6 documentation resources** — useful when writing code without a live TradingView connection.

---

### `codenamedevan/pinescriptv6`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/codenamedevan/pinescriptv6 |
| **Description** | Full PineScript v6 reference organized for AI code editors and LLMs |

Structured Markdown/JSON exports of Pine v6 built-in functions, types, and methods. Useful for feeding into AI-assisted editors or for offline reference on a phone.

---

### `Zkalish/pinescriptv6`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/Zkalish/pinescriptv6 |
| **Description** | Pine Script v6 documentation reformatted for LLMs and human readability |

Companion to the above; useful as a second reference source.

---

### `filipenunes75/PineScript-V6`

| Property | Value |
|----------|-------|
| **URL** | https://github.com/filipenunes75/PineScript-V6 |
| **Description** | Simple PineScript v6 code snippets and examples repository |

Code-sharing repo with v6 examples. Good for copy-pasting from a phone browser into TradingView's mobile web editor.

---

## 4. Recommended Mobile Workflow

Since no single app provides a complete PineScript v6 mobile IDE today, the best phone-based workflow combines the tools above:

### Step 1 — Install a Mobile Code Editor

**Android (recommended):** Install **Acode** from [GitHub releases](https://github.com/Acode-Foundation/Acode/releases) or [Google Play](https://play.google.com/store/apps/details?id=com.foxdebug.acodefree). It has the most mature plugin ecosystem for adding custom language support.

**Fallback options:**
- **Xed-Editor** ([GitHub](https://github.com/Xed-Editor/Xed-Editor)) — good for plain-text editing without plugin overhead
- **Visual-Code-Space** ([GitHub](https://github.com/Visual-Code-Space/Visual-Code-Space)) — AI-assisted, modern UI

### Step 2 — Add PineScript v6 Syntax Highlighting

Extract the TextMate grammar from `jpantsjoha/pinescript-vscode-extension`:

```
syntaxes/pine-script.tmLanguage.json   (or .tmLanguage)
```

In **Acode**, create a plugin using the [Acode plugin template](https://github.com/Acode-Foundation/acode-plugin) and register this grammar with Ace Editor:

```js
// Inside your Acode plugin's index.js
ace.define("ace/mode/pine_script", ..., function(acequire, exports) {
    // Register PineScript tokens from the tmLanguage keyword lists
    exports.Mode = function() { ... };
});
```

### Step 3 — Reference v6 Docs Offline

Bookmark or clone `codenamedevan/pinescriptv6` for offline access. The structured Markdown files let you look up built-in functions, types, and syntax rules without internet access.

### Step 4 — Compile and Run on TradingView

Open TradingView's mobile web interface (`tradingview.com`) in your phone's browser. Navigate to **Pine Editor** and paste your code to compile and test it. TradingView's web editor is the official runtime for PineScript v6 and works in mobile browsers.

---

## 5. iOS Notes

The options for iOS are more limited:

- **No open-source native iOS code IDE** with a plugin system comparable to Acode was found on GitHub.
- **Working Code** ([App Store, not open-source](https://apps.apple.com/app/working-copy/id896694807)) and **Textastic** support syntax highlighting but lack Pine-specific grammars.
- The best iOS approach remains using **TradingView's mobile web editor** via Safari, which provides the full Pine v6 compile-and-run experience.
- For offline editing, any iOS plain-text editor (1Writer, iA Writer, etc.) can be used to draft `.pine` files; compile them later in TradingView.

---

## Quick Reference Table

| Repository | Category | Platform | Stars | Pine v6 Support |
|-----------|----------|----------|-------|-----------------|
| [Acode-Foundation/Acode](https://github.com/Acode-Foundation/Acode) | Mobile IDE | Android | ~5,000 | Via plugin (adaptable) |
| [Xed-Editor/Xed-Editor](https://github.com/Xed-Editor/Xed-Editor) | Mobile IDE | Android | 1,847 | Plain-text editing |
| [Visual-Code-Space/Visual-Code-Space](https://github.com/Visual-Code-Space/Visual-Code-Space) | Mobile IDE | Android | 623 | AI-assisted editing |
| [jpantsjoha/pinescript-vscode-extension](https://github.com/jpantsjoha/pinescript-vscode-extension) | Language Tool | VS Code | 19 | Full v6 (grammar source) |
| [revanthpobala/pinescript-vscode-extension](https://github.com/revanthpobala/pinescript-vscode-extension) | Language Tool | VS Code | 15 | v5/v6 linter + highlighter |
| [deepentropy/intellij-pinescript](https://github.com/deepentropy/intellij-pinescript) | Language Tool | IntelliJ | 10 | Full v6 plugin |
| [codenamedevan/pinescriptv6](https://github.com/codenamedevan/pinescriptv6) | Reference | Any | — | v6 reference docs |
| [Zkalish/pinescriptv6](https://github.com/Zkalish/pinescriptv6) | Reference | Any | — | v6 reference docs |
| [filipenunes75/PineScript-V6](https://github.com/filipenunes75/PineScript-V6) | Reference | Any | — | v6 code examples |

---

## Key Finding

> **No repository on GitHub provides a turn-key PineScript v6 IDE app for phones (Android or iOS) as of April 2026.** The closest practical solution is: **Acode (Android)** + an **Acode plugin** built from the VS Code extension grammars (e.g., `jpantsjoha/pinescript-vscode-extension`) + **TradingView's mobile web editor** for compilation. For iOS, TradingView's mobile web editor is the primary option.

---

*Last updated: April 2026 — Maintained alongside the DAFE Open-Source Collection.*
