---
name: car-update-mileage
description: Update the current mileage for the 2013 Lexus RX450h
---

# Update Vehicle Mileage

Update the current mileage for the 2013 Lexus RX450h.

Load the lexus-maintenance skill and help the user update the current mileage:

1. Display the current stored mileage from `${CLAUDE_PLUGIN_ROOT}/data/vehicle.json`

2. Ask the user for the new current mileage

3. Validate that the new mileage is higher than the stored mileage

4. Update the vehicle.json file with:
   - New current_mileage value
   - Current timestamp in last_updated field

5. After updating, automatically check if any maintenance is now due by running the check-due command

6. Confirm the update was successful

This helps ensure accurate maintenance due date calculations based on mileage intervals.
