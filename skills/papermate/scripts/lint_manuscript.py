"""Advisory lint for manuscript drafts (.md/.txt/.tex).

Flags:
  1. numbers (decimals or percentages) that are not in the results ledger
  2. remaining [RESULT REQUIRED] / [UNVERIFIED] markers
  3. DOIs and URLs, listed so each can be checked against sources actually opened
  4. unsupported superlatives ("state-of-the-art", "first", "novel", ...)

Usage:
    python lint_manuscript.py draft.md --ledger results/ledger.jsonl

It is a safety net, not proof of correctness: a number can match the ledger and
still be misdescribed. Always read the flagged lines.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

NUM = re.compile(r"(?<![\w.])(\d+\.\d+|\d+(?:\.\d+)?\s?%)(?![\w])")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s\"<>)\]]+", re.I)
URL = re.compile(r"https?://[^\s\"<>)\]]+")
SUPER = re.compile(
    r"\b(state[- ]of[- ]the[- ]art|first (?:to|study|work)|novel|groundbreaking|"
    r"significantly|outperforms? all|best|unprecedented|never (?:been )?(?:done|studied))\b",
    re.I,
)


def load_ledger_values(path):
    vals = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            v = json.loads(line).get("value")
            if isinstance(v, (int, float)):
                vals.add(float(v))
    return vals


def matches(num_text, ledger_vals):
    t = num_text.replace(" ", "")
    pct = t.endswith("%")
    t = t.rstrip("%")
    try:
        x = float(t)
    except ValueError:
        return True
    decimals = len(t.split(".")[1]) if "." in t else 0
    tol = 0.5 * 10 ** (-decimals)  # rounding tolerance at the written precision
    for v in ledger_vals:
        candidates = (v * 100, v) if pct else (v, v * 100)
        if any(abs(c - x) <= tol + 1e-12 for c in candidates):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--ledger", default=None)
    args = ap.parse_args()

    text = open(args.draft, encoding="utf-8").read()
    lines = text.splitlines()
    ledger = load_ledger_values(args.ledger) if args.ledger else None

    issues = 0
    print(f"== Lint: {args.draft} ==")

    if ledger is None:
        print("[warn] no ledger given; skipping number check")
    else:
        for i, line in enumerate(lines, 1):
            if "[RESULT REQUIRED]" in line:
                continue
            masked = URL.sub(" ", DOI.sub(" ", line))  # ignore numbers inside DOIs/URLs
            for m in NUM.finditer(masked):
                if not matches(m.group(1), ledger):
                    issues += 1
                    print(f"[number not in ledger] line {i}: {m.group(1)}  |  {line.strip()[:100]}")

    for marker in ("[RESULT REQUIRED]", "[UNVERIFIED]"):
        hits = [i for i, l in enumerate(lines, 1) if marker in l]
        if hits:
            print(f"[open marker] {marker} x{len(hits)} at lines {hits[:15]}")

    dois = sorted({d.rstrip(".,;:") for d in DOI.findall(text)})
    urls = sorted(set(URL.findall(text)))
    if dois or urls:
        print(f"[verify] {len(dois)} DOI(s), {len(urls)} URL(s). Confirm each was opened this session:")
        for d in dois:
            print(f"   DOI {d}")
        for u in urls[:30]:
            print(f"   URL {u}")

    for i, line in enumerate(lines, 1):
        for m in SUPER.finditer(line):
            issues += 1
            print(f"[claim check] line {i}: '{m.group(0)}'  needs a cited comparison or softer wording")

    print(f"== {issues} item(s) to fix or confirm ==")
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
