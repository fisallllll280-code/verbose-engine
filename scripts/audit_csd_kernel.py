"""Read-only structural audit for the preserved, unclassified CSD source artifact.

This tool does not execute or rewrite the target file. It identifies possible
language/document markers for forensic review; it is not a language parser.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

DEFAULT_TARGET = Path("vaixlns/csd/kernel.mixed-source.txt")

MARKERS = {
    "LNS document": re.compile(r"(?m)^\s*VAIXLNS_ROOT\.lns\s*$"),
    "Rust item": re.compile(r"(?m)^\s*(?:pub\s+)?(?:struct|enum|impl|trait)\s+[A-Z][A-Za-z0-9_]*"),
    "TOML section": re.compile(r"(?m)^\s*\[[A-Za-z0-9_.-]+\]\s*$"),
    "Markdown heading": re.compile(r"(?m)^\s{0,3}#{1,6}\s+\S"),
    "Python module guard": re.compile(r"(?m)^\s*if __name__\s*==\s*['\"]__main__['\"]\s*:"),
}


def audit_text(text: str) -> dict:
    findings = []
    for label, pattern in MARKERS.items():
        matches = list(pattern.finditer(text))
        if matches:
            findings.append({
                "marker": label,
                "count": len(matches),
                "lines": [text.count("\n", 0, m.start()) + 1 for m in matches[:20]],
            })
    suffixes = {
        "python": len(re.findall(r"(?m)^\s*(?:def|class|async\s+def)\s+", text)),
        "rust": len(re.findall(r"(?m)^\s*(?:pub\s+)?fn\s+[a-zA-Z_]", text)),
        "markdown_headings": len(re.findall(r"(?m)^\s{0,3}#{1,6}\s+\S", text)),
    }
    return {
        "schema": "vaixlns.csd-kernel-structure-audit.v1",
        "target_language": "unclassified_mixed_source",
        "findings": findings,
        "heuristic_counts": suffixes,
        "interpretation": (
            "Review markers in context. This heuristic is not a parser and does not "
            "prove that the file is invalid or that each marker is executable code."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when any structural marker is found")
    args = parser.parse_args()
    try:
        source = args.target.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": str(exc), "target": str(args.target)}))
        return 2
    report = audit_text(source)
    report["target"] = str(args.target)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.strict and report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
