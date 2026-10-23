"""Render an animated, self-contained SVG contribution calendar."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    levels = {item["date"]: int(item["level"]) for item in data["days"]}
    end = max((date.fromisoformat(day) for day in levels), default=date.today())
    start = end - timedelta(days=370)
    start -= timedelta(days=start.weekday() + 1 if start.weekday() < 6 else 0)

    boxes = []
    cursor = start
    for week in range(54):
        for weekday in range(7):
            level = levels.get(cursor.isoformat(), 0)
            x, y = 58 + week * 14, 42 + weekday * 14
            delay = (week * 7 + weekday) * 0.006
            boxes.append(
                f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{PALETTE[min(level, 4)]}" '
                f'style="animation:appear .35s {delay:.3f}s both"/>'
            )
            cursor += timedelta(days=1)

    stats = data.get("stats", {})
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="186" viewBox="0 0 860 186" role="img" aria-label="GitHub contribution activity for {esc(data['username'])}">
  <style>
    .title {{ fill:#c9d1d9; font:600 15px ui-monospace, SFMono-Regular, Menlo, monospace }}
    .label {{ fill:#8b949e; font:12px ui-monospace, SFMono-Regular, Menlo, monospace }}
    @keyframes appear {{ from {{ opacity:0; transform:translate(-4px,-4px) }} to {{ opacity:1; transform:translate(0,0) }} }}
  </style>
  <rect width="860" height="186" rx="10" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="27" class="title">CONTRIBUTION ACTIVITY</text>
  <text x="24" y="55" class="label">Sun</text><text x="24" y="83" class="label">Tue</text><text x="24" y="111" class="label">Thu</text><text x="24" y="139" class="label">Sat</text>
  {''.join(boxes)}
  <text x="24" y="170" class="label">{stats.get('active_days', 0)} active days · {stats.get('current_streak', 0)} day streak</text>
  <text x="690" y="170" class="label">Less</text>
  {''.join(f'<rect x="{730+i*14}" y="160" width="10" height="10" rx="2" fill="{color}"/>' for i, color in enumerate(PALETTE))}
  <text x="805" y="170" class="label">More</text>
</svg>'''
    OUTPUT.write_text(svg + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
