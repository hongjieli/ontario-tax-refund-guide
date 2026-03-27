#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List


def caveats(item: Dict[str, Any]) -> List[str]:
    out = []
    if item.get("self_transfer"):
        out.append("self-transfer")
    if item.get("airport_change"):
        out.append("airport change")
    if item.get("overnight"):
        out.append("overnight layover")
    if item.get("visa_unclear"):
        out.append("transit rule needs confirmation")
    return out


def line(item: Dict[str, Any]) -> str:
    airlines = "/".join(item.get("airlines", [])) if item.get("airlines") else "Unknown airline"
    price = item.get("price", "?")
    currency = item.get("currency", "")
    layover = item.get("layover_airport", "?")
    layover_min = item.get("layover_min", "?")
    duration_h = item.get("duration_h", "?")
    label = item.get("label", "okay").upper()
    cv = caveats(item)
    caveat_text = f" | caveat: {', '.join(cv)}" if cv else ""
    return (
        f"- [{label}] {item.get('route', '?')} | {airlines} | {currency} {price} | "
        f"{duration_h}h total | layover {layover} {layover_min}m{caveat_text}"
    )


def main() -> int:
    data = json.load(sys.stdin)
    if not isinstance(data, list):
        print("Input must be a JSON array.", file=sys.stderr)
        return 1
    if not data:
        print("No itineraries provided.")
        return 0

    lines = [line(x) for x in data]
    strong = [x for x in data if x.get("label") == "strong"]
    okay = [x for x in data if x.get("label") == "okay"]

    print("Recommended options:")
    for l in lines:
        print(l)

    best = (strong or okay or data)[0]
    print("\nBottom line:")
    print(f"- Best overall pick: {best.get('route', '?')} ({best.get('currency', '')} {best.get('price', '?')})")
    if strong:
        cheapest_strong = min(strong, key=lambda x: x.get("price", float("inf")))
        print(f"- Cheapest strong option: {cheapest_strong.get('route', '?')} ({cheapest_strong.get('currency', '')} {cheapest_strong.get('price', '?')})")
    easiest = max(data, key=lambda x: x.get("score", 0))
    print(f"- Easiest-looking option: {easiest.get('route', '?')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
