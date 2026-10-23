"""Fetch public GitHub contribution data without a token."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Kenshiro-me"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "contributions.json"


def streak(days: list[dict[str, object]]) -> int:
    levels = {item["date"]: int(item["level"]) for item in days}
    current = 0
    cursor = date.today()
    while levels.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    return current


def main() -> None:
    response = requests.get(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "Kenshiro-me-profile-readme"},
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    days = []
    for cell in soup.select("[data-date][data-level]"):
        day = cell.get("data-date")
        level = cell.get("data-level")
        if day and level is not None:
            days.append({"date": day, "level": int(level)})

    if not days:
        raise RuntimeError("GitHub contribution calendar was not found in the response")

    active_days = sum(int(item["level"]) > 0 for item in days)
    payload = {
        "username": USERNAME,
        "updated": date.today().isoformat(),
        "days": days,
        "stats": {"active_days": active_days, "current_streak": streak(days)},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
