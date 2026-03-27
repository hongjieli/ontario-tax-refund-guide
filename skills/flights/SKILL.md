---
name: flights
description: Search, compare, and triage flight options for travelers. Use when the user asks to find flights, compare airfare, estimate ticket prices, shortlist routes, check layover suitability, avoid specific transit countries, or evaluate whether an itinerary is good for elderly travelers, visa-sensitive travelers, or people with baggage/connection constraints.
---

# Flights

Use this skill to convert messy flight search results into a short, practical recommendation.

## Workflow

1. Gather the minimum search inputs:
   - origin
   - destination
   - date or date window
   - one-way or round-trip
   - passenger count
   - cabin
2. Ask only for missing constraints that materially change results:
   - max stops
   - avoid countries/regions
   - airport flexibility
   - budget
   - traveler constraints such as age, visa status, baggage, overnight-transfer tolerance
3. Search with available web tools or user-provided screenshots.
4. Normalize candidate itineraries into JSON.
5. Use the scoring script to rank them.
6. Use the summary script to produce a user-facing recommendation.

## Search behavior

Prefer a small number of good options over a giant dump.

When the search source is unstable or hard to automate:

- ask the user for screenshots of candidate results if needed
- still apply this skill's screening rules
- be explicit about what is verified vs assumed

## Safety and quality rules

Optimize in this order unless the user says otherwise:

1. legality and transfer feasibility
2. traveler suitability
3. total travel time and complexity
4. price

Do not recommend an itinerary only because it is cheap if the transfer looks fragile or may require an unexpected visa, airport change, self-transfer, or baggage recheck.

## Required checks before recommending

For each promising itinerary, verify as much as possible from the listing:

- number of stops
- layover airport(s)
- self-transfer vs protected connection
- airport change or terminal change
- overnight layover
- baggage through-check likelihood if known
- whether the route passes through countries the user wants to avoid
- whether a visa-sensitive traveler may face transit issues

If a transfer policy cannot be verified, say so clearly.

## Elderly / conservative-travel heuristics

Prefer these when the traveler is older or wants minimum hassle:

- one ticket / protected connection
- one stop max
- no airport changes
- no overnight layovers
- layovers roughly 2–4 hours
- avoid self-transfer itineraries
- prefer familiar hubs or same-country domestic connection over complicated international transit when rules are unclear

Read `references/elderly-and-visa.md` when the user mentions parents, grandparents, Chinese passports, missing visas, or "most convenient" travel.

## Output format

Keep recommendations compact. Use bullets, not markdown tables on chat surfaces.

For each option include:

- route
- airline(s)
- price
- total duration
- layover airport and duration
- why it is good
- any caveat
- recommendation level: strong / okay / avoid

Then end with a short bottom line such as:

- cheapest viable option
- easiest option
- best overall pick

## Bundled resources

- Read `references/triage-guide.md` for the ranking logic and risk checklist.
- Read `references/elderly-and-visa.md` for conservative routing guidance.
- Use `references/input-example.json` as the input shape.
- Run `scripts/filter_itineraries.py` to score candidate itineraries.
- Run `scripts/summarize_itineraries.py` to generate a concise traveler-facing summary.
