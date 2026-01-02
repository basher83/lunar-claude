---
name: car-view-recalls
description: Display safety recalls and common issues for the 2013 Lexus RX450h from NHTSA data
---

# View NHTSA Recalls

Display safety recalls and common issues for the 2013 Lexus RX450h from NHTSA data.

Load the lexus-maintenance skill and:

1. Check when the NHTSA cache was last updated (from vehicle.json)

2. If cache is older than 30 days or empty, ask user if they want to refresh:
   - If yes, run: `${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py update`

3. Display recalls by running: `${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py recalls`

4. Display common issues by running: `${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py issues`

5. For each recall, provide:
   - NHTSA campaign number
   - Component affected
   - Summary of the issue
   - Consequence/risk
   - Recommended action

6. Advise the user to check with a Lexus dealer if any recalls apply to their VIN

Recalls are safety-critical and should be addressed immediately at no cost to the owner.
