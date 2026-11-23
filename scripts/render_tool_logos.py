#!/usr/bin/env python3
"""Write the "Tool logos" grid in logos.html from assets/logos/tools/tools.json.

The grid sits between the markers `<!-- tool-logos:start -->` and
`<!-- tool-logos:end -->`. Everything between them is generated: edit the
catalogue, then run this script, never the markup by hand.

Usage (from the repository root):
    python scripts/render_tool_logos.py           # rewrite the grid
    python scripts/render_tool_logos.py --check   # exit 1 if logos.html is stale
"""

from __future__ import annotations

import html
import json
import pathlib
import sys

PAGE = pathlib.Path("logos.html")
CATALOGUE = pathlib.Path("assets/logos/tools/tools.json")
START, END = "<!-- tool-logos:start -->", "<!-- tool-logos:end -->"
INDENT = "      "


def grid(entries: list[dict]) -> list[str]:
    lines = [f'{INDENT}<div class="tool-grid">']
    for entry in entries:
        lines += [
            f'{INDENT}  <div class="tool-card">',
            f'{INDENT}    <img src="{html.escape(entry["file"])}" alt="{html.escape(entry["alt"])}" loading="lazy">',
            f'{INDENT}    <div class="name">{html.escape(entry["name"])}</div>',
            f'{INDENT}    <div class="group">{html.escape(entry["group"])}</div>',
            f"{INDENT}  </div>",
        ]
    return lines + [f"{INDENT}</div>"]


def main() -> int:
    check = "--check" in sys.argv[1:]
    with PAGE.open(encoding="utf-8", newline="") as fh:
        page = fh.read()
    newline = "\r\n" if "\r\n" in page else "\n"
    head, sep_start, rest = page.partition(START)
    _, sep_end, tail = rest.partition(END)
    if not (sep_start and sep_end):
        print(f"{PAGE}: markers {START} and {END} not found")
        return 1
    entries = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    block = newline.join([START, *grid(entries), INDENT + END])
    fresh = head + block + tail
    if fresh == page:
        print(f"{PAGE} tool logo grid is current ({len(entries)} logos).")
        return 0
    if check:
        print(f"{PAGE} tool logo grid is stale: run python scripts/render_tool_logos.py")
        return 1
    with PAGE.open("w", encoding="utf-8", newline="") as fh:
        fh.write(fresh)
    print(f"{PAGE} tool logo grid rewritten ({len(entries)} logos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
