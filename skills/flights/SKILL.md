---
name: flights
description: Search, compare, and triage flight options for travelers. Use when the user asks to find flights, compare airfare, estimate ticket prices, shortlist routes, check layover suitability, avoid specific transit countries, or evaluate whether an itinerary is good for elderly travelers, visa-sensitive travelers, or people with baggage/connection constraints.
---

# Flights

Use this skill to structure flight search work and turn messy fare options into a short, decision-ready recommendation.

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
4. Normalize options into a small comparison list.
5. Flag practical risks before recommending anything.

## What to optimize for

Prioritize in this order unless the user says otherwise:

1. legality and transfer feasibility
2. traveler suitability
3. total travel time and complexity
4. price

Do not recommend an itinerary only because it is cheap if the transfer looks fragile or may require an unexpected visa, airport change, self-transfer, or recheck of bags.

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

## China-passport / visa-sensitive heuristics

When the user mentions Chinese passport holders or missing visas/permits:

- treat transit rules as a first-class constraint
- avoid making hard claims about eligibility unless verified from the carrier or official policy
- if uncertain, label the route as "needs transit-rule confirmation"
- prefer routes with lower transit-friction when helping family members or older travelers

## Output format

Keep recommendations compact. Use bullets, not tables on chat surfaces.

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

- Read `references/triage-guide.md` when you need the ranking logic and risk checklist.
- Use `scripts/filter_itineraries.py` to score candidate itineraries after you collect raw options from screenshots, websites, or manual notes.
