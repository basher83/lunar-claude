---
name: car-check-due
description: Check what maintenance is due or coming due soon for the 2013 Lexus RX450h
---

# Check Due Maintenance

Check what maintenance is due or coming due soon for the 2013 Lexus RX450h.

Load the lexus-maintenance skill and run the maintenance check script to display:
- Maintenance items that are DUE now (based on mileage and time intervals)
- Maintenance items COMING DUE soon (within 80% of interval)
- Status message if all maintenance is up to date

Execute: `${CLAUDE_PLUGIN_ROOT}/tools/maintenance_manager.py check-due`

Present the results in a clear, organized format and provide recommendations for scheduling any due maintenance.
