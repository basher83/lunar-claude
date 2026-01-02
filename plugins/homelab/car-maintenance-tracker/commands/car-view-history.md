---
name: car-view-history
description: Display recent work orders and maintenance history for the 2013 Lexus RX450h
---

# View Maintenance History

Display recent work orders and maintenance history for the 2013 Lexus RX450h.

Load the lexus-maintenance skill and:

1. Ask the user how many recent work orders to display (default: 10)

2. Execute: `${CLAUDE_PLUGIN_ROOT}/tools/maintenance_manager.py list-orders [limit]`

3. Display the work order history including:
   - Work order ID
   - Date of service
   - Mileage at time of service
   - Description of work performed
   - Cost
   - Service provider

4. Calculate and display summary statistics:
   - Total maintenance costs (all time)
   - Average cost per service
   - Most frequent service provider
   - Time since last service
   - Miles since last service

5. Identify any patterns or recommendations:
   - If oil changes are overdue
   - If services are clustered at one provider (good for warranty)
   - If costs are trending up (may indicate aging vehicle issues)

This helps track maintenance investment and identify your most reliable service providers.
