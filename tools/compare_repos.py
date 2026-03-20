#!/usr/bin/env python3
"""
compare_repos.py — DAFE Pine Script v6 Repository Comparator
=============================================================
Searches GitHub for public repositories containing Pine Script v6 indicator
files, collects their metadata, and produces a Markdown comparison report
showing how the DAFE scripts stack up against the broader ecosystem.

Usage:
    python tools/compare_repos.py [options]

Options:
    --token       GitHub personal access token (or set GITHUB_TOKEN env var)
    --query       Extra search keywords appended to the default query
    --max-repos   Maximum number of GitHub repos to analyse  (default: 20)
    --local-dir   Path to local scripts/ folder  (default: scripts/)
    --output      Output Markdown report path  (default: docs/comparison_report.md)
    --json        Also write raw comparison data as JSON alongside the report

Requirements:
    pip install requests

Note: Without a GitHub token the API rate-limit is 10 requests/minute.
      With a token it rises to 5 000 requests/hour.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("[error] 'requests' is not installed.  Run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

GITHUB_API = "https://api.github.com"
SEARCH_CODE_URL = f"{GITHUB_API}/search/code"
SEARCH_REPO_URL = f"{GITHUB_API}/search/repositories"


def _headers(token: str | None) -> dict:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _get(url: str, params: dict, headers: dict, retries: int = 3) -> dict:
    """GET with simple retry / rate-limit back-off."""
    for attempt in range(retries):
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 403:
            reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait  = max(1, reset - int(time.time())) + 2
            print(f"  [rate-limit] sleeping {wait}s …", file=sys.stderr)
            time.sleep(wait)
            continue
        if resp.status_code == 422:
            # Unprocessable — search query issue, not worth retrying
            break
        time.sleep(2 ** attempt)
    return {}


# ---------------------------------------------------------------------------
# Remote metadata extraction
# ---------------------------------------------------------------------------

RE_VERSION    = re.compile(r"^//@version=(\d+)", re.MULTILINE)
RE_INDICATOR  = re.compile(
    r'^(?:indicator|strategy|library)\s*\(\s*["\']([^"\']+)["\']', re.MULTILINE
)
RE_IMPORT     = re.compile(r'^import\s+(\S+)\s+as\s+(\w+)', re.MULTILINE)
RE_INPUT      = re.compile(
    r'input\.(int|float|bool|string|color|source|timeframe|symbol|price|session|text_area|enum)\s*\(',
    re.MULTILINE,
)
RE_TABLE      = re.compile(r'\btable\.new\s*\(')
RE_ML_HINT    = re.compile(r'\b(?:knn|svm|naive_bayes|neural|ml\.|reinforcement|rl\.)\b', re.I)
RE_ARRAY      = re.compile(r'\barray\.(new|from|push|pop|get|set)\b')
RE_ALERT      = re.compile(r'\balertcondition\s*\(|\balert\s*\(')


def parse_raw_pine(raw: str) -> dict:
    """Extract key metrics from raw Pine Script source text."""
    version_m = RE_VERSION.search(raw)
    ind_m     = RE_INDICATOR.search(raw)
    lines     = raw.splitlines()
    return {
        "pine_version":   int(version_m.group(1)) if version_m else None,
        "title":          ind_m.group(1) if ind_m else "(unknown)",
        "line_count":     len(lines),
        "import_count":   len(RE_IMPORT.findall(raw)),
        "input_count":    len(RE_INPUT.findall(raw)),
        "has_table":      bool(RE_TABLE.search(raw)),
        "has_ml_hints":   bool(RE_ML_HINT.search(raw)),
        "uses_arrays":    bool(RE_ARRAY.search(raw)),
        "has_alerts":     bool(RE_ALERT.search(raw)),
    }


def fetch_file_content(raw_url: str, headers: dict) -> str | None:
    """Fetch raw file content from GitHub."""
    try:
        resp = requests.get(raw_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.text
    except requests.RequestException as exc:
        print(f"  [warn] Could not fetch {raw_url}: {exc}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Local metadata extraction (mirrors collect_data.py logic, lightweight)
# ---------------------------------------------------------------------------

def parse_local_pine(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    m   = parse_raw_pine(raw)
    m["file"] = path.name
    m["source"] = "local"
    return m


# ---------------------------------------------------------------------------
# GitHub search
# ---------------------------------------------------------------------------

def search_pine_v6_repos(
    extra_query: str,
    max_repos:   int,
    headers:     dict,
) -> list[dict]:
    """Search GitHub for repos with Pine Script v6 indicator files."""
    if max_repos <= 0:
        return []

    base_query = '//@version=6 indicator language:Pine'
    if extra_query:
        base_query += f' {extra_query}'

    params = {"q": base_query, "per_page": min(max_repos, 30)}
    print(f"  Searching GitHub: {base_query!r}")
    data   = _get(SEARCH_CODE_URL, params, headers)
    items  = data.get("items", [])
    print(f"  Found {len(items)} code result(s) (capped at {max_repos})")

    repos_seen: set[str] = set()
    results = []

    for item in items[:max_repos]:
        repo      = item.get("repository", {})
        repo_full = repo.get("full_name", "")
        if repo_full in repos_seen:
            continue
        repos_seen.add(repo_full)

        raw_url = (
            item.get("html_url", "")
            .replace("https://github.com/", "https://raw.githubusercontent.com/")
            .replace("/blob/", "/")
        )

        file_content = fetch_file_content(raw_url, headers)
        if not file_content:
            continue

        meta = parse_raw_pine(file_content)
        meta.update({
            "repo":        repo_full,
            "file":        item.get("name", ""),
            "html_url":    item.get("html_url", ""),
            "repo_stars":  repo.get("stargazers_count"),
            "repo_url":    repo.get("html_url", ""),
            "source":      "github",
        })
        results.append(meta)
        print(f"    ✓ {repo_full}/{item.get('name', '')}")
        time.sleep(0.3)   # polite pacing

    return results


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

COMPARISON_FIELDS = [
    ("pine_version",  "Pine Version"),
    ("line_count",    "Lines of Code"),
    ("import_count",  "Library Imports"),
    ("input_count",   "Inputs"),
    ("has_table",     "Dashboard Table"),
    ("has_ml_hints",  "ML / AI Logic"),
    ("uses_arrays",   "Array Usage"),
    ("has_alerts",    "Alerts"),
]


def compare(local_scripts: list[dict], remote_scripts: list[dict]) -> dict:
    """Build comparison data structure."""
    remote_v6     = [r for r in remote_scripts if r.get("pine_version") == 6]
    remote_non_v6 = [r for r in remote_scripts if r.get("pine_version") != 6]

    def avg(lst, key):
        vals = [x[key] for x in lst if isinstance(x.get(key), (int, float))]
        return round(sum(vals) / len(vals), 1) if vals else None

    def pct(lst, key):
        if not lst:
            return None
        return round(100 * sum(1 for x in lst if x.get(key)) / len(lst), 1)

    ecosystem_stats = {
        "count":          len(remote_v6),
        "avg_lines":      avg(remote_v6, "line_count"),
        "avg_imports":    avg(remote_v6, "import_count"),
        "avg_inputs":     avg(remote_v6, "input_count"),
        "pct_tables":     pct(remote_v6, "has_table"),
        "pct_ml":         pct(remote_v6, "has_ml_hints"),
        "pct_arrays":     pct(remote_v6, "uses_arrays"),
        "pct_alerts":     pct(remote_v6, "has_alerts"),
    }

    return {
        "local":            local_scripts,
        "remote_v6":        remote_v6,
        "remote_non_v6":    remote_non_v6,
        "ecosystem_stats":  ecosystem_stats,
        "generated_at":     datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def _bool_icon(val) -> str:
    if val is True:
        return "✅"
    if val is False:
        return "❌"
    return "—"


def render_markdown_report(data: dict) -> str:
    local           = data["local"]
    remote_v6       = data["remote_v6"]
    eco             = data["ecosystem_stats"]
    generated_at    = data["generated_at"]

    lines = [
        "# DAFE Pine Script v6 — Repository Comparison Report",
        "",
        f"> Generated: {generated_at}",
        "",
        "---",
        "",
        "## 📁 Local Scripts (this repo)",
        "",
    ]

    # Local scripts table
    header_cols = ["File", "Title", "Lines", "Imports", "Inputs",
                   "Table", "ML Hints", "Arrays", "Alerts"]
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cols)) + " |")
    for s in local:
        lines.append(
            f"| `{s.get('file','')}` "
            f"| {s.get('title', '—')} "
            f"| {s.get('line_count', '—')} "
            f"| {s.get('import_count', '—')} "
            f"| {s.get('input_count', '—')} "
            f"| {_bool_icon(s.get('has_table'))} "
            f"| {_bool_icon(s.get('has_ml_hints'))} "
            f"| {_bool_icon(s.get('uses_arrays'))} "
            f"| {_bool_icon(s.get('has_alerts'))} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 🌐 GitHub Pine Script v6 Ecosystem",
        "",
        f"Analysed **{eco.get('count', 0)}** Pine Script v6 files from public GitHub repos.",
        "",
        "| Metric | Ecosystem Average |",
        "| --- | --- |",
        f"| Lines of Code | {eco.get('avg_lines') or '—'} |",
        f"| Library Imports | {eco.get('avg_imports') or '—'} |",
        f"| Inputs | {eco.get('avg_inputs') or '—'} |",
        f"| Scripts with Dashboard Table | {eco.get('pct_tables') or '—'}{'%' if eco.get('pct_tables') is not None else ''} |",
        f"| Scripts with ML / AI Logic | {eco.get('pct_ml') or '—'}{'%' if eco.get('pct_ml') is not None else ''} |",
        f"| Scripts using Arrays | {eco.get('pct_arrays') or '—'}{'%' if eco.get('pct_arrays') is not None else ''} |",
        f"| Scripts with Alerts | {eco.get('pct_alerts') or '—'}{'%' if eco.get('pct_alerts') is not None else ''} |",
        "",
    ]

    if remote_v6:
        lines += [
            "### 🔍 Sampled Remote Scripts",
            "",
            "| Repo | File | Lines | Imports | ML | Stars | Link |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for s in remote_v6:
            stars = s.get("repo_stars")
            star_str = str(stars) if stars is not None else "—"
            lines.append(
                f"| `{s.get('repo', '—')}` "
                f"| `{s.get('file', '—')}` "
                f"| {s.get('line_count', '—')} "
                f"| {s.get('import_count', '—')} "
                f"| {_bool_icon(s.get('has_ml_hints'))} "
                f"| {star_str} "
                f"| [link]({s.get('html_url', '#')}) |"
            )
        lines.append("")

    # Per-script comparison
    lines += [
        "---",
        "",
        "## 📊 Per-Script Comparison vs Ecosystem Averages",
        "",
    ]
    for s in local:
        lines += [
            f"### `{s.get('file', '?')}`  —  *{s.get('title', '?')}*",
            "",
            "| Feature | This Script | Ecosystem Avg |",
            "| --- | --- | --- |",
        ]
        avg_lines   = eco.get("avg_lines") or 0
        avg_imports = eco.get("avg_imports") or 0
        avg_inputs  = eco.get("avg_inputs") or 0
        eco_count   = eco.get("count", 0)

        def _pct_label(key):
            val = eco.get(key)
            return f"{val}%" if val is not None else "—"

        def _diff(val, avg):
            if val is None or not eco_count:
                return str(val) if val is not None else "—"
            delta = val - avg
            sign  = "+" if delta >= 0 else ""
            return f"{val} ({sign}{delta:.0f} vs avg)"

        lines += [
            f"| Lines of Code | {_diff(s.get('line_count'), avg_lines)} | {avg_lines if eco_count else '—'} |",
            f"| Library Imports | {_diff(s.get('import_count'), avg_imports)} | {avg_imports if eco_count else '—'} |",
            f"| Inputs | {_diff(s.get('input_count'), avg_inputs)} | {avg_inputs if eco_count else '—'} |",
            f"| Dashboard Table | {_bool_icon(s.get('has_table'))} | {_pct_label('pct_tables')} have it |",
            f"| ML / AI Logic | {_bool_icon(s.get('has_ml_hints'))} | {_pct_label('pct_ml')} have it |",
            f"| Array Usage | {_bool_icon(s.get('uses_arrays'))} | {_pct_label('pct_arrays')} have it |",
            f"| Alerts | {_bool_icon(s.get('has_alerts'))} | {_pct_label('pct_alerts')} have it |",
            "",
        ]

    lines += [
        "---",
        "",
        "*Report generated by `tools/compare_repos.py` — DAFE open-source collection.*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare local Pine Script v6 scripts against GitHub ecosystem."
    )
    parser.add_argument("--token",      default=os.environ.get("GITHUB_TOKEN"),
                        help="GitHub PAT (or set GITHUB_TOKEN env var)")
    parser.add_argument("--query",      default="",
                        help="Extra keywords for GitHub code search")
    parser.add_argument("--max-repos",  type=int, default=20,
                        help="Max number of GitHub repos to analyse (default 20)")
    parser.add_argument("--local-dir",  default="scripts",
                        help="Path to local scripts/ folder (default: scripts/)")
    parser.add_argument("--output",     default="docs/comparison_report.md",
                        help="Output Markdown file (default: docs/comparison_report.md)")
    parser.add_argument("--json",       action="store_true",
                        help="Also save raw comparison data as JSON")
    args = parser.parse_args()

    repo_root    = Path(__file__).parent.parent
    scripts_dir  = (repo_root / args.local_dir).resolve()
    output_path  = (repo_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = _headers(args.token)

    # ── Collect local scripts ──────────────────────────────────────────────
    pine_files = sorted(scripts_dir.glob("**/*.pine"))
    if not pine_files:
        print(f"[warn] No .pine files found under {scripts_dir}", file=sys.stderr)
    print(f"Parsing {len(pine_files)} local script(s) …")
    local_scripts = [parse_local_pine(p) for p in pine_files]

    # ── Search GitHub ──────────────────────────────────────────────────────
    if not args.token:
        print("[warn] No GitHub token — unauthenticated API, stricter rate limits apply.")
    print(f"Searching GitHub for Pine Script v6 repos (max {args.max_repos}) …")
    remote_scripts = search_pine_v6_repos(args.query, args.max_repos, headers)

    # ── Compare ────────────────────────────────────────────────────────────
    data     = compare(local_scripts, remote_scripts)
    report   = render_markdown_report(data)
    output_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {output_path}")

    if args.json:
        json_path = output_path.with_suffix(".json")
        json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSON data written to: {json_path}")


if __name__ == "__main__":
    main()
