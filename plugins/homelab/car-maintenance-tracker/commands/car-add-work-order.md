---
name: car-add-work-order
description: Record a completed maintenance service or work order for the 2013 Lexus RX450h
---

# Add Work Order

Record a completed maintenance service or work order for the 2013 Lexus RX450h.

Load the lexus-maintenance skill and help the user add a new work order by:

1. Ask the user for the following information:
   - Description of work performed (e.g., "Oil change and tire rotation")
   - Vehicle mileage at time of service
   - Total cost of service
   - Service provider name
   - Any additional notes (optional)

2. Validate the information:
   - Ensure mileage is reasonable (not lower than previous records)
   - Ensure cost is a valid number
   - Confirm all required fields are provided

3. Use the maintenance_manager.py add_work_order function to save the record

4. If the service corresponds to a scheduled maintenance item (oil change, tire rotation, etc.), ask if they want to update the maintenance schedule

5. Confirm the work order was added successfully and display the updated work order count

Remember to update the vehicle's current mileage if this is higher than the stored value.
