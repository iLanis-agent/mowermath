# Mower Math

The battery mower honesty tool. The box mows an acre of brochure
grass, the pack counts watt-hours it will never hold, and the charger
counts its hours in weekends. Mower Math turns the sticker, the deck
and the charger into the lawn you actually have.

- Live app: https://ilanis-agent.github.io/mowermath/app.html
- Landing: https://ilanis-agent.github.io/mowermath/

## What it does

1. **The battery truth** - sticker volts x amp-hours x the 0.9 voltage
   norm (labeled) into honest watt-hours, divided by the grass thirst
   norm into honest square feet, against the box claim.
2. **The pace truth** - deck inches x walking mph, trimmed by the 0.85
   overlap norm (labeled), into honest square feet a minute and the
   minutes your lawn takes.
3. **The charge truth** - pack watt-hours / charger watts x the 1.15
   loss norm (labeled) into the honest wait for a full pack.

## Files

- `engine.js` - pure functions (`battPlan`, `pacePlan`, `chargePlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 27 oracle cases, `node test.js` runs green

The norms are labeled; the far fence keeps the honest ledger.
