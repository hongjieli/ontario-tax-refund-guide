#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List


def score_item(item: Dict[str, Any]) -> Dict[str, Any]:
    score = 100
    notes: List[str] = []

    if item.get("excluded_transit"):
        score -= 60
        notes.append("passes through excluded transit country/region")
    if item.get("self_transfer"):
        score -= 35
        notes.append("self-transfer")
    if item.get("airport_change"):
        score -= 35
        notes.append("airport change")
    if item.get("overnight"):
        score -= 20
        notes.append("overnight layover")
    if item.get("visa_unclear"):
        score -= 25
        notes.append("transit/visa rule unclear")

    layover_min = item.get("layover_min")
    if isinstance(layover_min, (int, float)):
        if layover_min < 90:
            score -= 20
            notes.append("tight layover")
        elif 120 <= layover_min <= 240:
            score += 8
            notes.append("comfortable layover")

    stops = item.get("stops")
    if isinstance(stops, int):
        if stops > 1:
            score -= 20
            notes.append("more than one stop")
        elif stops == 0:
            score += 12
            notes.append("nonstop")
        elif stops == 1:
            score += 4
            notes.append("one stop")

    duration_h = item.get("duration_h")
    if isinstance(duration_h, (int, float)) and duration_h > 24:
        score -= 10
        notes.append("long total travel time")

    item["score"] = max(score, 0)
    item["notes"] = notes

    if item["score"] >= 85:
        item["label"] = "strong"
    elif item["score"] >= 65:
        item["label"] = "okay"
    else:
        item["label"] = "avoid"
    return item


def main() -> int:
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        print("Input must be a JSON array of itinerary objects.", file=sys.stderr)
        return 1
    scored = [score_item(dict(x)) for x in data]
    scored.sort(key=lambda x: (-x.get("score", 0), x.get("price", float("inf"))))
    json.dump(scored, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
