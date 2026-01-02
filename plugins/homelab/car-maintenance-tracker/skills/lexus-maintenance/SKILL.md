---
name: lexus-maintenance
description: AI-powered maintenance guidance for 2013 Lexus RX450h with NHTSA recall tracking and common issues awareness
---

# Lexus RX450h Maintenance Assistant

AI-powered maintenance guidance for 2013 Lexus RX450h with NHTSA recall tracking and common issues awareness.

## Description

This skill provides comprehensive maintenance guidance for the 2013 Lexus RX450h hybrid SUV, including:
- Scheduled maintenance tracking based on mileage and time intervals
- Hybrid-specific maintenance requirements (battery, inverter, cooling systems)
- NHTSA recall and TSB awareness for common issues
- Work order tracking and service history management
- Cost tracking and service provider management

## Triggers

Activate this skill when:
- Adding or reviewing vehicle maintenance records
- Checking what maintenance is due or coming due
- Recording completed work orders or services
- Investigating NHTSA recalls or common issues for 2013 Lexus RX450h
- Planning upcoming maintenance or service appointments
- Tracking maintenance costs and service providers

## Vehicle Specifications

**2013 Lexus RX450h Details:**
- Engine: 3.5L V6 with Hybrid Synergy Drive
- Transmission: ECVT (Electronically Controlled Continuously Variable Transmission)
- Hybrid System: Toyota Hybrid Synergy Drive with NiMH battery
- Recommended Oil: 0W-20 full synthetic
- Oil Capacity: 6.4 quarts with filter
- Fuel: 87 octane regular unleaded (premium recommended for performance)

## Maintenance Schedule

### Every 5,000 miles or 6 months:
- Engine oil and filter change (0W-20 synthetic)
- Tire rotation
- Multi-point inspection

### Every 15,000 miles or 12 months:
- Cabin air filter replacement
- Inspect hybrid system cooling system

### Every 30,000 miles:
- Engine air filter replacement
- Inspect brake pads and rotors
- Inspect suspension components

### Every 60,000 miles:
- Replace transmission (CVT) fluid
- Inspect drive belts
- Replace engine coolant (first time, then every 50,000 miles)

### Every 120,000 miles:
- Replace spark plugs (iridium)
- Inspect hybrid battery system thoroughly

### Every 24 months:
- Replace brake fluid

## Hybrid-Specific Maintenance

**Critical Hybrid Components:**
1. **Hybrid Battery Cooling System**: Check cooling fan and air filter annually
2. **Inverter Coolant**: Separate from engine coolant, check level regularly
3. **Brake System**: Regenerative braking reduces wear but brake fluid ages faster
4. **12V Auxiliary Battery**: Replace every 3-5 years (hybrid system stress)

**Common Hybrid Issues to Monitor:**
- Inverter coolant leaks (check under vehicle)
- Hybrid battery cooling fan operation
- Brake actuator performance (ABS/VSC lights)
- Power steering pump (electric assist)

## NHTSA Data Integration

The plugin maintains a cache of NHTSA data including:
- Safety recalls specific to 2013 RX450h
- Consumer complaints from NHTSA database
- Common failure patterns and trending issues

**To refresh NHTSA data:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py update
```

**To view recalls:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py recalls
```

**To view common issues:**
```bash
$ ${CLAUDE_PLUGIN_ROOT}/tools/nhtsa_api.py issues
```

## Work Order Management

### Adding Work Orders

When recording completed maintenance:
1. Include accurate mileage at time of service
2. Record complete description of work performed
3. Document parts replaced (part numbers if available)
4. Track costs including parts and labor separately
5. Note service provider for warranty tracking

### Tracking Service Providers

Maintain service provider information:
- Shop name and contact information
- Specialization (dealer, hybrid specialist, general)
- Warranty information
- Quality ratings and notes

## Data Files

**Vehicle Data:** `${CLAUDE_PLUGIN_ROOT}/data/vehicle.json`
- Current mileage
- VIN (optional)
- NHTSA cache (recalls, complaints, last fetched date)

**Maintenance Records:** `${CLAUDE_PLUGIN_ROOT}/data/maintenance-records.json`
- Work orders (completed services)
- Upcoming maintenance schedule
- Service providers

## Best Practices

1. **Update mileage regularly** to get accurate maintenance due dates
2. **Refresh NHTSA data monthly** to catch new recalls
3. **Use 0W-20 synthetic oil only** - critical for hybrid engine longevity
4. **Monitor hybrid battery cooling** - overheating reduces battery life
5. **Keep detailed records** - helpful for resale value and warranty claims
6. **Address recalls immediately** - safety-critical issues

## Common 2013 RX450h Issues

Known issues to monitor (will be updated from NHTSA data):
- Inverter coolant pump failure (check for leaks)
- Brake actuator issues (ABS/VSC warning lights)
- Transmission shift issues (software updates available)
- Water pump leaks (coolant smell or overheating)
- Dashboard cracking (TSB available for replacement)

## Commands

Use these slash commands for common operations:
- `/car-check-due` - Check maintenance due or coming due
- `/car-add-work-order` - Add completed service to records
- `/car-update-mileage` - Update current vehicle mileage
- `/car-view-recalls` - View NHTSA recalls for this vehicle
- `/car-view-history` - View recent work orders

## Notes

- Always use OEM or quality equivalent parts for hybrid components
- Lexus dealers have hybrid-specific diagnostic tools
- Independent hybrid specialists often provide better value than dealers
- Keep hybrid battery cooling vents clean (behind rear seat area)
- Monitor 12V auxiliary battery - hybrid system depends on it
