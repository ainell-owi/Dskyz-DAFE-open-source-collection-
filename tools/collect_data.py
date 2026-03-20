#!/usr/bin/env python3
"""
collect_data.py — DAFE Pine Script Metadata Collector
======================================================
Parses all .pine files in the scripts/ directory and extracts structured
metadata (version, indicator name, inputs, imports, sections, line counts,
etc.). Outputs a JSON report to docs/collected_metadata.json.

Usage:
    python tools/collect_data.py [--scripts-dir <path>] [--output <path>]

Options:
    --scripts-dir   Path to directory containing .pine files  (default: scripts/)
    --output        Output JSON file path  (default: docs/collected_metadata.json)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Regex patterns for Pine Script v6 constructs
# ---------------------------------------------------------------------------
RE_VERSION       = re.compile(r"^//@version=(\d+)", re.MULTILINE)
RE_INDICATOR     = re.compile(
    r'^(?:indicator|strategy|library)\s*\(\s*["\']([^"\']+)["\']',
    re.MULTILINE,
)
RE_SHORTTITLE    = re.compile(r'shorttitle\s*=\s*["\']([^"\']+)["\']')
RE_OVERLAY       = re.compile(r'\boverlay\s*=\s*(true|false)')
RE_IMPORT        = re.compile(r'^import\s+(\S+)\s+as\s+(\w+)', re.MULTILINE)
RE_INPUT         = re.compile(
    r'input\.(int|float|bool|string|color|source|timeframe|symbol|price|session|text_area|enum)\s*\(',
    re.MULTILINE,
)
RE_INPUT_LABEL   = re.compile(
    r'input\.[a-z_]+\s*\([^,)]*,\s*["\']([^"\']+)["\']',
    re.MULTILINE,
)
RE_INPUT_GROUP   = re.compile(r'\bgroup\s*=\s*["\']([^"\']+)["\']')
RE_SECTION       = re.compile(
    r'^\s*//\s*[=─╔╚]{4,}.*?(?:\n\s*//.*?)*\n\s*//\s*[║│]?\s*([^║│\n]{3,60})',
    re.MULTILINE,
)
RE_FUNCTION_DEF  = re.compile(r'^(\w+)\s*\(', re.MULTILINE)
RE_MAX_BARS      = re.compile(r'max_bars_back\s*=\s*(\d+)')
RE_MAX_LINES     = re.compile(r'max_lines_count\s*=\s*(\d+)')
RE_MAX_LABELS    = re.compile(r'max_labels_count\s*=\s*(\d+)')
RE_MAX_BOXES     = re.compile(r'max_boxes_count\s*=\s*(\d+)')
RE_PRECISION     = re.compile(r'precision\s*=\s*(\d+)')
RE_VAR_DECL      = re.compile(r'\bvar\s+(?:int|float|bool|string|color|array|matrix|map|label|line|box|linefill|polyline|table)\b')
RE_ARRAY_FROM    = re.compile(r'array\.from\s*\(')
RE_PLOT          = re.compile(r'\bplot\s*\(')
RE_PLOTSHAPE     = re.compile(r'\bplotshape\s*\(')
RE_TABLE_NEW     = re.compile(r'\btable\.new\s*\(')
RE_ALERT         = re.compile(r'\balertcondition\s*\(|\balert\s*\(')


def extract_section_names(source: str) -> list[str]:
    """Extract human-readable section names from decorated comment blocks."""
    # Match both ===== and ═══ style headers
    names = []
    for m in re.finditer(
        r'//\s*(?:[=─╔]{4,}.*\n\s*//\s*[║│]?\s*)?([^/\n]{4,60})\s*\n\s*//\s*[=─╚╝]{4,}',
        source,
        re.MULTILINE,
    ):
        candidate = m.group(1).strip().strip("║│ ")
        if candidate and not re.match(r'^[=─╔╚╝╗]{3,}$', candidate):
            names.append(candidate)
    return names


def extract_inputs(source: str) -> dict:
    """Return aggregated input metadata."""
    types = {}
    for m in RE_INPUT.finditer(source):
        t = m.group(1)
        types[t] = types.get(t, 0) + 1

    groups: dict[str, int] = {}
    for m in RE_INPUT_GROUP.finditer(source):
        g = m.group(1).strip()
        groups[g] = groups.get(g, 0) + 1

    labels = RE_INPUT_LABEL.findall(source)

    return {
        "total": sum(types.values()),
        "by_type": types,
        "groups": groups,
        "labels": labels,
    }


def extract_imports(source: str) -> list[dict]:
    """Return list of library imports with namespace and alias."""
    return [
        {"namespace": m.group(1), "alias": m.group(2)}
        for m in RE_IMPORT.finditer(source)
    ]


def extract_limits(source: str) -> dict:
    """Extract Pine Script resource limits declared in the indicator() call."""

    def _first(pattern):
        m = pattern.search(source)
        return int(m.group(1)) if m else None

    return {
        "max_bars_back":    _first(RE_MAX_BARS),
        "max_lines_count":  _first(RE_MAX_LINES),
        "max_labels_count": _first(RE_MAX_LABELS),
        "max_boxes_count":  _first(RE_MAX_BOXES),
        "precision":        _first(RE_PRECISION),
    }


def extract_features(source: str) -> dict:
    """Count usage of notable Pine Script features."""
    return {
        "var_declarations":  len(RE_VAR_DECL.findall(source)),
        "array_from_calls":  len(RE_ARRAY_FROM.findall(source)),
        "plot_calls":        len(RE_PLOT.findall(source)),
        "plotshape_calls":   len(RE_PLOTSHAPE.findall(source)),
        "table_new_calls":   len(RE_TABLE_NEW.findall(source)),
        "alert_calls":       len(RE_ALERT.findall(source)),
    }


def parse_pine_file(path: Path) -> dict:
    """Parse a single .pine file and return its metadata dict."""
    source = path.read_text(encoding="utf-8", errors="replace")
    lines  = source.splitlines()

    version_m   = RE_VERSION.search(source)
    ind_m       = RE_INDICATOR.search(source)
    short_m     = RE_SHORTTITLE.search(source)
    overlay_m   = RE_OVERLAY.search(source)

    script_type_m = re.search(r'^(indicator|strategy|library)\s*\(', source, re.MULTILINE)

    return {
        "file":        path.name,
        "path":        str(path),
        "parsed_at":   datetime.now(timezone.utc).isoformat(),
        "pine_version": int(version_m.group(1)) if version_m else None,
        "script_type":  script_type_m.group(1) if script_type_m else "unknown",
        "title":        ind_m.group(1) if ind_m else path.stem,
        "shorttitle":   short_m.group(1) if short_m else None,
        "overlay":      overlay_m.group(1) == "true" if overlay_m else None,
        "line_count":   len(lines),
        "blank_lines":  sum(1 for ln in lines if not ln.strip()),
        "comment_lines": sum(1 for ln in lines if ln.strip().startswith("//")),
        "limits":       extract_limits(source),
        "imports":      extract_imports(source),
        "inputs":       extract_inputs(source),
        "sections":     extract_section_names(source),
        "features":     extract_features(source),
    }


def collect_all(scripts_dir: Path) -> list[dict]:
    """Collect metadata for all .pine files found under scripts_dir."""
    pine_files = sorted(scripts_dir.glob("**/*.pine"))
    if not pine_files:
        print(f"[warn] No .pine files found under {scripts_dir}", file=sys.stderr)
        return []
    results = []
    for p in pine_files:
        print(f"  → Parsing {p.name} …")
        try:
            results.append(parse_pine_file(p))
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            print(f"  [error] {p.name}: {exc}", file=sys.stderr)
    return results


def build_summary(records: list[dict]) -> dict:
    """Build a high-level summary across all collected records."""
    if not records:
        return {}
    total_lines   = sum(r["line_count"]   for r in records)
    total_imports = sum(len(r["imports"]) for r in records)
    total_inputs  = sum(r["inputs"]["total"] for r in records)

    all_lib_ns = sorted({
        imp["namespace"]
        for r in records
        for imp in r["imports"]
    })

    return {
        "script_count":    len(records),
        "total_lines":     total_lines,
        "total_imports":   total_imports,
        "total_inputs":    total_inputs,
        "library_namespaces": all_lib_ns,
        "generated_at":    datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect metadata from Pine Script files in this repository."
    )
    parser.add_argument(
        "--scripts-dir",
        default="scripts",
        help="Directory containing .pine files (default: scripts/)",
    )
    parser.add_argument(
        "--output",
        default="docs/collected_metadata.json",
        help="Output JSON file path (default: docs/collected_metadata.json)",
    )
    args = parser.parse_args()

    repo_root   = Path(__file__).parent.parent
    scripts_dir = (repo_root / args.scripts_dir).resolve()
    output_path = (repo_root / args.output).resolve()

    if not scripts_dir.exists():
        print(f"[error] Scripts directory not found: {scripts_dir}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Collecting metadata from: {scripts_dir}")
    records = collect_all(scripts_dir)

    payload = {
        "summary": build_summary(records),
        "scripts": records,
    }

    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nMetadata written to: {output_path}")
    print(f"  {len(records)} script(s) parsed, "
          f"{payload['summary'].get('total_lines', 0)} total lines.")


if __name__ == "__main__":
    main()
