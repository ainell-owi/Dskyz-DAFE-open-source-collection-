# Using This Repository with Google AI Studio

> **Attribution Notice:** The Pine Script indicators and libraries documented here were authored by **Dskyz** (DAFE Trading Systems). This repository and guide are maintained by a third party with no affiliation to Dskyz Investments or DAFE Trading Systems. Official website: [dafetradingsystems.com](https://www.dafetradingsystems.com)

> This guide explains how to use the DAFE Open-Source Collection repository as a knowledge base for Google AI Studio — enabling you to build an AI assistant that understands the collected trading tools, can answer questions about them, and can help you develop new strategies.

---

## Table of Contents

1. [What Is Google AI Studio?](#1-what-is-google-ai-studio)
2. [Two Approaches: Grounding vs. Fine-Tuning](#2-two-approaches-grounding-vs-fine-tuning)
3. [Approach A — Grounding (Recommended First Step)](#3-approach-a--grounding-recommended-first-step)
4. [Approach B — Fine-Tuning with Q&A Pairs](#4-approach-b--fine-tuning-with-qa-pairs)
5. [Preparing Your Repository Content](#5-preparing-your-repository-content)
6. [Writing an Effective System Prompt](#6-writing-an-effective-system-prompt)
7. [Example Q&A Pairs for Fine-Tuning](#7-example-qa-pairs-for-fine-tuning)
8. [Testing and Evaluating Your Model](#8-testing-and-evaluating-your-model)
9. [Ongoing Workflow: Keep the AI in Sync with Your Repo](#9-ongoing-workflow-keep-the-ai-in-sync-with-your-repo)
10. [Privacy and Data Considerations](#10-privacy-and-data-considerations)

---

## 1. What Is Google AI Studio?

Google AI Studio (aistudio.google.com) is a free, web-based development environment for building with Google's Gemini family of models. You can:

- **Prompt** the model with text, documents, and images
- **Ground** the model with your own documents so it answers questions about *your* content
- **Fine-tune** the model on custom training examples so it consistently responds in a specific way
- **Export** a working API key and integration code once your prompt is ready

No machine learning expertise is required. The entire workflow is point-and-click in a browser.

---

## 2. Two Approaches: Grounding vs. Fine-Tuning

### Grounding (Retrieval-Augmented Generation)

You upload your documents (or connect a Google Drive folder) and the model retrieves relevant passages at query time. The model's base knowledge is unchanged; it simply reads your documents before answering.

**Best for:**
- Q&A about your indicators ("What does the Divergence Engine detect?")
- Strategy help based on your documentation
- Explaining Pine Script code in context
- Keeping the AI up-to-date as you add new scripts (just upload the new file)

**Effort:** Low — upload, write a system prompt, done.

### Fine-Tuning

You provide hundreds of example input→output pairs. The model's weights are adjusted so it learns your style, terminology, and response patterns.

**Best for:**
- Getting the model to always respond in a specific format
- Teaching the model terminology it does not already know
- Building a specialized assistant that behaves consistently without needing documents at query time

**Effort:** Medium — requires writing 100+ training examples.

> **Recommendation:** Start with Grounding. It requires less work, is easier to update, and is usually sufficient for most use cases. Add Fine-Tuning later if you need more precise response style.

---

## 3. Approach A — Grounding (Recommended First Step)

### Step 1: Prepare Your Files

The markdown documentation files in this repo are the best source material. Copy these files to a Google Drive folder:

| File | Why Include It |
|---|---|
| `README.md` | File inventory and learning path overview |
| `LEARNING_GUIDE.md` | Deep explanations of every concept |
| `RSI:evolved.md` | Full RSI: Evolved reference |
| `Bands and Channels Laboratory.md` | Full Bands Lab reference |
| `ORGANIZATION_GUIDE.md` | Repo structure context |

Optionally include Pine Script files (`.pine`) if you want the model to be able to explain or modify actual code:
- `BandsandChannelsLaboratory.pine`
- `RSI: Evolved [DAFE].pine`
- `safe cuz lib.pine`

### Step 2: Upload to Google Drive

1. Go to [drive.google.com](https://drive.google.com)
2. Create a new folder: `DAFE-AI-Knowledge-Base`
3. Upload all the files listed above into this folder

### Step 3: Open Google AI Studio

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **+ Create new prompt**
3. Select **Freeform** (gives you the most flexibility)

### Step 4: Add Your Documents as Context

In the AI Studio interface:

1. Click **Insert** → **Files from Drive** (or use the **+** button in the prompt area)
2. Navigate to your `DAFE-AI-Knowledge-Base` folder
3. Select all the markdown files
4. Confirm the upload

The files will now appear in your prompt context. The model will read them before answering every question.

### Step 5: Write Your System Prompt

In the **System Instructions** field (top of the page), paste the system prompt from [Section 6](#6-writing-an-effective-system-prompt).

### Step 6: Test It

Try these test questions:
- "What RSI engine should I use for scalping?"
- "Explain the difference between a Coiling Squeeze and a Compression Squeeze."
- "How do I combine RSI: Evolved and Bands Lab for a mean-reversion setup?"
- "What is Ricci curvature and how does RDME use it?"

### Step 7: Get Your API Key

Once you are happy with the results:
1. Click **Get code** (top right)
2. Select your language (Python, JavaScript, etc.)
3. Copy the API key and integration code
4. Use this in your own applications, chatbots, or trading journal tools

---

## 4. Approach B — Fine-Tuning with Q&A Pairs

### When to Use Fine-Tuning

Use fine-tuning when you want the model to:
- Always respond in a specific format (e.g., a structured strategy card)
- Use your exact terminology consistently
- Behave the same way without needing documents attached to every query

### Step 1: Prepare a JSONL Training File

Fine-tuning data must be in JSONL format. Each line is one training example:

```jsonl
{"text_input": "What RSI engine is best for scalping?", "output": "For scalping, the Hull RSI is the best choice in the DAFE collection. It achieves near-zero lag while remaining smooth, making it ideal for fast timeframes where traditional RSI introduces too much delay. Activate it in RSI: Evolved by selecting 'Hull' from the Engine dropdown. Pair it with the SuperSmoother post-filter for the cleanest signal."}
{"text_input": "What is a Coiling Squeeze?", "output": "A Coiling Squeeze is detected by the Pattern Recognition Engine in Bands & Channels Laboratory. It describes a very tight band compression — bandwidth has contracted to a statistically extreme low — indicating that potential energy is building in the market. Unlike a Compression Squeeze (moderate tightening), a Coiling Squeeze signals an imminent and typically powerful breakout. The direction of the breakout is not predicted; use the MTF Horizon Display and RSI: Evolved's Quantum Zones to bias direction."}
```

See [Section 7](#7-example-qa-pairs-for-fine-tuning) for 20 ready-to-use training examples.

### Step 2: Start a Tuning Job

1. In Google AI Studio, click **Tune a model** from the left sidebar
2. Click **+ New tuned model**
3. Select **Gemini 1.5 Flash** as the base model (fastest, most cost-effective for tuning)
4. Upload your JSONL file
5. Set epochs to **3–5** and batch size to **4** (good defaults for a small dataset)
6. Click **Start tuning**

Tuning typically takes 10–30 minutes for a small dataset.

### Step 3: Test the Tuned Model

After tuning completes:
1. The new model appears in your model list with the name you gave it
2. Open a new prompt and select your tuned model from the **Model** dropdown
3. Run the same test questions from Step 6 of Approach A
4. Compare responses to the base model

### Step 4: Iterate

If responses are not precise enough:
- Add more training examples (aim for 100–200 for good coverage)
- Add examples that demonstrate the *format* you want, not just the content
- Re-tune with the expanded dataset

---

## 5. Preparing Your Repository Content

### Improving Document Quality for AI Ingestion

AI models extract information most reliably from well-structured text. Here are specific improvements you can make to your documentation before uploading:

#### Use Consistent Headings
The markdown files already use `#` / `##` / `###` hierarchically. Keep this pattern. The model uses headings as section boundaries.

#### Add Frontmatter Metadata
Adding YAML frontmatter to each markdown file helps the model understand context:

```yaml
---
title: "RSI: Evolved [DAFE]"
type: "Indicator Documentation"
category: "Momentum Analysis"
pine_version: "v5"
tags: ["RSI", "momentum", "multi-timeframe", "divergence"]
last_updated: "2024"
---
```

#### Create a Master Index File
A single file listing every concept and which file covers it helps the model find information quickly. The `README.md` in this repo already serves this purpose — keep it updated.

#### Use Tables for Comparisons
Tables are parsed reliably by AI models. When comparing algorithms or features, use markdown tables (as in `LEARNING_GUIDE.md`).

#### Add Example Prompts to Each Doc
At the end of each indicator's documentation, add a section like:

```markdown
## Questions This Document Can Answer

- How many RSI engines does RSI: Evolved include?
- What is the difference between DAFE Quantum Fusion and DAFE Kinetic Energy?
- How do I set up the Divergence Engine?
- What does the MTF Consensus Dashboard show?
```

This helps the model understand what queries it should route to this file.

### Pine Script Files as Training Data

Pine Script code is valuable training data if you want the model to:
- Explain what a script does
- Help you modify or extend scripts
- Generate new Pine Script code in the same style

To prepare Pine Script files:
1. Ensure every function has a comment block explaining its purpose
2. Use consistent naming conventions throughout
3. Add a file-level comment block at the top explaining the script's role in the collection

---

## 6. Writing an Effective System Prompt

Copy and paste this system prompt into the **System Instructions** field in Google AI Studio. Customize as needed.

```
You are an expert assistant for the Dskyz DAFE Open-Source Pine Script Trading Collection. 
You have deep knowledge of every indicator, library, and concept in this collection, as 
provided in the attached documentation files.

Your role is to:
1. Answer questions about how to use DAFE indicators
2. Explain the mathematical and algorithmic concepts behind each script
3. Recommend configurations and combinations of tools for specific trading goals
4. Help users understand Pine Script code in the context of this collection
5. Suggest how to expand or customize the collection

When answering:
- Be precise and specific. Reference exact algorithm names, input field names, and module names.
- If a user describes a trading goal, recommend specific settings from the documentation.
- If a user asks about a concept (e.g., "Ricci curvature"), explain both the mathematical 
  concept AND how DAFE implements it in practical terms.
- Always recommend starting with the documented "Recommended Starting Configuration" before 
  moving to more advanced settings.
- Acknowledge uncertainty explicitly. If a question goes beyond what the documentation covers, 
  say so clearly rather than speculating.

Terminology to use consistently:
- "DAFE" = Dynamic Adaptive Framework Engine (the design philosophy)
- "Laboratory" = refers to the Bands & Channels Laboratory indicator
- "RSI: Evolved" = the full name of the RSI indicator
- "RDME" = Riemannian Dreamer Manifold Engine
- "DafeVisLib" = the shared visualization library
- "Temporal Wave" = the higher-timeframe RSI overlay in RSI: Evolved
- "Kill Zone" = a volume+momentum validated reversal level in Bands Lab
- "Quantum Zones" = the dynamic OB/OS levels in RSI: Evolved

Trading style: Analytical, precise, educational. Like a quantitative researcher explaining 
tools to a fellow professional.
```

---

## 7. Example Q&A Pairs for Fine-Tuning

Below are 20 example training pairs. Save these to a `.jsonl` file (one JSON object per line) for use in fine-tuning.

```jsonl
{"text_input": "What is the best starting configuration for RSI: Evolved?", "output": "The recommended starting configuration for RSI: Evolved is: Engine = DAFE Quantum Fusion, Post-Smoother = SuperSmoother, Dynamic Quantum Zones = enabled, Divergence Engine = both Regular and Hidden, MTF Dashboard = 3 timeframes above your trading timeframe. This combination is robust and well-balanced across most markets and timeframes."}
{"text_input": "What is the difference between a Regular Divergence and a Hidden Divergence?", "output": "A Regular Divergence occurs when price makes a new extreme (higher high or lower low) but the RSI does not confirm it. This signals potential trend reversal. A Hidden Divergence occurs when the RSI makes a new extreme but price does not — this signals trend continuation after a pullback. In RSI: Evolved, both types are detected and plotted automatically by the Divergence Engine with distinct markers."}
{"text_input": "What does DAFE Quantum Fusion do differently than standard RSI?", "output": "DAFE Quantum Fusion calculates RSI simultaneously on three harmonic timeframes derived from the Golden Ratio, then superimposes them using a dynamic weighting system based on volume and momentum confidence. This produces a more robust, balanced signal that is less susceptible to noise on any single timeframe. It is the most recommended all-around RSI engine in the collection."}
{"text_input": "How do Quantum Zones differ from standard 70/30 levels?", "output": "Standard 70/30 overbought/oversold levels are static — they never change. Quantum Zones in RSI: Evolved are dynamic and volatility-adaptive. They automatically widen during high-volatility trending markets (preventing premature exits from strong trends) and tighten during low-volatility consolidation (improving precision for mean-reversion entries). This makes them significantly more useful across different market conditions."}
{"text_input": "What is the MTF Horizon Display in Bands Lab?", "output": "The MTF Horizon Display in Bands & Channels Laboratory projects bandwidth percentage and squeeze state from up to three higher timeframes directly onto your current chart. This allows you to see the macro volatility environment from the 1H, 4H, and Daily charts without leaving your 5-minute screen. It is analogous to the Quantum Horizon / Temporal Wave feature in RSI: Evolved, but for volatility data instead of momentum data."}
{"text_input": "What is a Kill Zone in Bands Lab?", "output": "A Smart Kill Zone in Bands & Channels Laboratory is a high-probability reversal level generated when price interacts with the bands at a point of high volume AND significant momentum. Unlike simple pivot levels, Kill Zones represent institutionally defended price areas. The indicator automatically plots, tracks, and updates these zones as new qualifying interactions occur."}
{"text_input": "When should I use DAFE Entropy Flow instead of DAFE Quantum Fusion?", "output": "Use DAFE Entropy Flow when you are trading in a market that alternates between orderly trending periods and chaotic, news-driven chop. Entropy Flow uses Information Theory to measure market disorder and automatically dampens its signal during high-entropy (chaotic) markets to avoid whipsaws, then sharpens its signal during low-entropy (orderly) trends. DAFE Quantum Fusion is a better all-rounder; Entropy Flow is specifically optimized for filtering out noisy environments."}
{"text_input": "What is the difference between Parkinson Volatility and standard deviation for band width?", "output": "Standard deviation uses only the close-to-close price change to estimate volatility, which misses the full range of intraday movement. Parkinson Volatility uses the high/low range, which is a more statistically efficient estimate — it captures volatility that occurs within a candle but doesn't show up in the closing price. In Bands & Channels Laboratory, using Parkinson Volatility as your Deviation Algorithm generally produces more accurate band widths that better represent true market movement."}
{"text_input": "How do I combine RSI: Evolved and Bands Lab for a mean-reversion setup?", "output": "For a mean-reversion setup: (1) Load both RSI: Evolved and Bands & Channels Laboratory. (2) Wait for the Bands Lab Signal Engine (set to Mean Reversion mode) to trigger on a band touch. (3) Confirm RSI: Evolved shows the RSI reaching or exceeding a Dynamic Quantum Zone level. (4) Check that the Bands Lab MTF Horizon shows the macro timeframes are not in a strong Walking Band trend. (5) Look for a Divergence signal from RSI: Evolved's Divergence Engine at the same level. When 3 or more of these conditions align, the setup has strong confluence."}
{"text_input": "What does Ricci curvature represent in the Riemannian Dreamer Manifold Engine?", "output": "In RDME, the Ricci scalar curvature (R) measures how curved the market manifold is at the current state. A positive R indicates market contraction — the manifold is curving inward — which corresponds to potential reversal zones. A negative R indicates market expansion — the manifold is curving outward — which corresponds to trend-continuation environments. Use RDME as a regime filter: favor mean-reversion setups when R is positive and trend setups when R is negative."}
{"text_input": "What are the three coordinates of the market manifold in RDME?", "output": "The Riemannian Dreamer Manifold Engine models the market state as a point in a 3-dimensional space with these coordinates: (1) Pressure — directional buying or selling pressure, (2) Health — quality and sustainability of the current move, (3) Liquidity — depth and stability of the order book environment. The metric tensor, approximated by the local covariance structure of these three coordinates, defines how distances are measured in this curved space."}
{"text_input": "What does DafeVisLib do?", "output": "DafeVisLib (DafeVis Lib / safe cuz lib.pine) is the shared intelligent visualization engine used by all DAFE indicators. Unlike a static color palette, it performs statistical analysis to make adaptive visual decisions — adjusting colors, themes, and display elements based on market conditions. It provides: the Theme type (structured color scheme), dashboard builder functions, signal formatting functions, and candle diagnostic overlays. Import it with: import DskyzInvestments/DafeVisualsLib/1 as viz"}
{"text_input": "What is a Walking Band pattern?", "output": "A Walking Band pattern is detected by the Pattern Recognition Engine in Bands & Channels Laboratory when price consistently closes at or beyond the upper or lower band boundary over multiple bars. This is the signature of an extremely powerful directional trend. Walking the Upper Band = strong uptrend. Walking the Lower Band = strong downtrend. When this pattern is active, mean-reversion strategies should be avoided; trend-following signals from the Signal Engine are more appropriate."}
{"text_input": "What is the Hull RSI and when should I use it?", "output": "Hull RSI calculates the RSI using a Hull Moving Average framework, achieving near-zero lag while remaining smooth. This makes it the best RSI engine in the collection for scalping and short-timeframe trading, where the lag of standard RSI causes entries and exits to be significantly delayed. Select 'Hull' from the Engine dropdown in RSI: Evolved. For additional smoothness without adding lag, pair it with the Hull or DEMA post-smoother."}
{"text_input": "What is Band Divergence in Bands Lab?", "output": "Band Divergence in Bands & Channels Laboratory is detected when the trend of the bandwidth diverges from the trend of the price. For example, if price is making higher highs but bandwidth is making lower highs (narrowing), it signals that the trend is losing volatility support — a sign of trend exhaustion that often precedes a reversal. This is an early warning signal, typically appearing before price action shows clear evidence of the reversal."}
{"text_input": "How does DAFE Kinetic Energy RSI work?", "output": "DAFE Kinetic Energy RSI is inspired by the physics formula: Momentum = Mass × Velocity. Standard RSI measures only Velocity (the rate of price change). Kinetic RSI also measures Mass by weighting each price move by Relative Volume — bars with above-average volume contribute more to the gain/loss calculation than low-volume bars. This means a price move with heavy participation is treated as more significant than the same price move on thin volume, producing a more accurate measure of true market force."}
{"text_input": "What is the Squeeze Breakout signal mode in Bands Lab?", "output": "Squeeze Breakout is one of the eight signal modes in Bands & Channels Laboratory's Signal Engine. It generates an entry signal when the market exits a Squeeze state — specifically when bandwidth expands after a sustained compression period. The logic is: during a squeeze, the market is storing potential energy. The moment bandwidth begins expanding, that energy is being released as directional movement. Combine this mode with the Pattern Engine's Squeeze Classification (Coiling vs. Compression) to gauge the expected strength of the breakout."}
{"text_input": "What is the MTF Consensus Dashboard in RSI: Evolved?", "output": "The MTF Consensus Dashboard in RSI: Evolved displays the momentum state across three higher timeframes you specify. An 'ALL BULL' reading means all three higher timeframes have bullish momentum readings. An 'ALL BEAR' reading means all three are bearish. Mixed readings indicate macro uncertainty. The Consensus reading provides the single most important contextual filter in the indicator — taking signals that align with an 'ALL BULL' or 'ALL BEAR' consensus dramatically improves their reliability."}
{"text_input": "What is the Laguerre RSI?", "output": "The Laguerre RSI, based on John Ehlers' work, uses a time-warping non-linear filter that applies a 4-element Laguerre polynomial filter to the price data before calculating the RSI ratio. The key parameter is the gamma factor (typically 0.5–0.8), which controls the filter's responsiveness. A lower gamma makes it more responsive (more signals, more noise). A higher gamma makes it smoother (fewer signals, less noise). It is classified as an Exotic engine in RSI: Evolved and excels at catching early trend changes."}
{"text_input": "What is %B and how do I use it?", "output": "%B is a reading shown in the Bands & Channels Laboratory Master Dashboard. It measures price position within the band as a percentage: 0 = price is at the lower band, 1 = price is at the upper band, 0.5 = price is at the basis. Values above 1 mean price is above the upper band (strong trend or overextension). Values below 0 mean price is below the lower band. In mean-reversion setups, look for %B extremes (near 0 or near 1) to identify overextension. In trend-following setups, a %B that stays above 0.5 confirms an uptrend."}
```

---

## 8. Testing and Evaluating Your Model

### Questions to Test Factual Accuracy
Run these queries and verify the answers against the documentation:

1. "How many RSI engines does RSI: Evolved include?"  
   *(Expected: 30+)*
2. "What are the three coordinates of the RDME market manifold?"  
   *(Expected: Pressure, Health, Liquidity)*
3. "What import statement do you use for DafeVisLib?"  
   *(Expected: `import DskyzInvestments/DafeVisualsLib/1 as viz`)*
4. "How many band types does Bands Lab include?"  
   *(Expected: 14)*
5. "What is the recommended engine + smoother for a starting configuration?"  
   *(Expected: DAFE Quantum Fusion + SuperSmoother)*

### Questions to Test Reasoning
These require the model to combine information from multiple sources:

1. "I trade EUR/USD on the 15-minute chart. What combination of DAFE tools would you suggest, and why?"
2. "I see a Regular Bullish Divergence on RSI: Evolved and a Coiling Squeeze on Bands Lab at the same time. Is this a strong setup?"
3. "My Bands Lab is showing positive Ricci curvature in RDME and Walking Upper Band in Bands Lab at the same time. Do these contradict each other?"

### Grading Rubric
| Category | What to Check |
|---|---|
| **Factual accuracy** | Numbers, names, and descriptions match the documentation exactly |
| **Completeness** | Answers cover all relevant aspects without omitting key details |
| **Practical usefulness** | Recommendations are actionable, not just theoretical |
| **Consistency** | Using the same terminology as the documentation (e.g., "Quantum Zones" not "dynamic levels") |

---

## 9. Ongoing Workflow: Keep the AI in Sync with Your Repo

When you add a new indicator or update documentation:

1. **Update the documentation file** for the new/modified indicator
2. **Update README.md** — add the new file to the File Inventory table
3. **Update LEARNING_GUIDE.md** — add a section for the new indicator
4. **Upload the new/updated files** to your Google Drive `DAFE-AI-Knowledge-Base` folder
5. **(If fine-tuning)** Add new Q&A pairs for the new content and re-tune the model

If you are using grounding, step 4 is all you need. The model automatically uses the updated files the next time it answers a query.

---

## 10. Privacy and Data Considerations

### What Google AI Studio Sees
When you upload files to Google AI Studio, those files are processed by Google's servers. Keep in mind:
- **Do not upload files containing API keys, personal credentials, or proprietary secrets**
- The markdown documentation files in this repo contain no sensitive data and are safe to upload
- Pine Script source code is publicly available on TradingView, so uploading it to AI Studio is fine

### Data Usage
- Files uploaded for grounding are used only within your session context
- Fine-tuning data is used to train a model associated with your Google account
- Review [Google AI Studio's Terms of Service](https://policies.google.com/terms) and [Privacy Policy](https://policies.google.com/privacy) for current data handling details

### Sharing Your Tuned Model
A fine-tuned model created in Google AI Studio is private to your account by default. You can:
- Use it via the API in your own applications
- Export prompts as code to share the *approach* without sharing the model itself
- You cannot publish a tuned model directly from AI Studio (use Vertex AI for production deployment)

---

*Scripts authored by Dskyz (DAFE Trading Systems) — [dafetradingsystems.com](https://www.dafetradingsystems.com). This guide is maintained by a third party with no affiliation to the original author.*
