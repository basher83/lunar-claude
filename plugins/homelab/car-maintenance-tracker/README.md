# Car Maintenance Tracker

AI-powered maintenance assistant for 2013 Lexus RX450h with NHTSA API integration for recalls, TSBs, and common issues tracking.

## Overview

This plugin provides comprehensive vehicle maintenance tracking and scheduling specifically designed for the **2013 Lexus RX450h** hybrid SUV. It integrates with the NHTSA (National Highway Traffic Safety Administration) API to provide real-time information about safety recalls, consumer complaints, and common issues.

## Features

- ✅ **Automated Maintenance Scheduling**: Track maintenance intervals based on mileage and time
- ✅ **Hybrid-Specific Guidance**: Special attention to hybrid battery, inverter, and regenerative braking systems
- ✅ **NHTSA Integration**: Automatic fetching of recalls, TSBs, and consumer complaints
- ✅ **Work Order Tracking**: Complete service history with costs and providers
- ✅ **Due Date Calculations**: Intelligent reminders for upcoming maintenance
- ✅ **Cost Analytics**: Track maintenance spending over time

## Installation

This plugin is part of the lunar-claude marketplace. It's located at:

```text
plugins/homelab/car-maintenance-tracker/
```

## Quick Start

### 1. Update Your Vehicle Information

First, update your vehicle's current mileage and optionally add your VIN:

```bash
/car-update-mileage
```

### 2. Fetch NHTSA Data

Get the latest recalls and common issues for your 2013 Lexus RX450h:

```bash
/car-view-recalls
```

This will automatically fetch data from NHTSA if the cache is empty or outdated.

### 3. Check What's Due

See what maintenance is due or coming due soon:

```bash
/car-check-due
```

### 4. Record Completed Service

After getting service, add a work order:

```bash
/car-add-work-order
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/car-check-due` | Check maintenance due or coming due soon |
| `/car-add-work-order` | Record completed service or maintenance |
| `/car-update-mileage` | Update current vehicle mileage |
| `/car-view-recalls` | View NHTSA recalls and common issues |
| `/car-view-history` | View recent work orders and service history |

## Skills

### `lexus-maintenance`

The lexus-maintenance skill provides AI-powered guidance for maintaining your 2013 Lexus RX450h, including:

- Scheduled maintenance intervals (oil changes, filters, fluids, etc.)
- Hybrid-specific maintenance requirements
- Common issues to monitor
- Best practices for hybrid vehicle care
- Integration with NHTSA recall and complaint data

**Activates when:**
- Adding or reviewing maintenance records
- Checking due maintenance
- Investigating recalls or common issues
- Planning service appointments

## Data Storage

The plugin stores data in JSON files:

### `data/vehicle.json`
Stores vehicle information and NHTSA cache:
```json
{
  "vehicle": {
    "year": 2013,
    "make": "Lexus",
    "model": "RX450h",
    "vin": "",
    "current_mileage": 0,
    "last_updated": ""
  },
  "nhtsa_cache": {
    "recalls": [],
    "complaints": [],
    "last_fetched": null
  }
}
```

### `data/maintenance-records.json`
Stores work orders and maintenance schedule:
```json
{
  "work_orders": [
    {
      "id": 1,
      "date": "2024-01-15T10:30:00",
      "description": "Oil change and tire rotation",
      "mileage": 75000,
      "cost": 89.99,
      "provider": "Lexus of Hometown",
      "notes": "Used 0W-20 synthetic"
    }
  ],
  "upcoming_maintenance": [...],
  "service_providers": []
}
```

## Maintenance Schedule (2013 RX450h)

### Regular Intervals

| Service | Mileage | Time | Notes |
|---------|---------|------|-------|
| Oil & Filter | 5,000 mi | 6 mo | 0W-20 synthetic only |
| Tire Rotation | 5,000 mi | 6 mo | Check pressure |
| Cabin Air Filter | 15,000 mi | 12 mo | |
| Engine Air Filter | 30,000 mi | - | |
| Transmission Fluid | 60,000 mi | - | CVT hybrid transmission |
| Coolant | 100,000 mi | - | Then every 50k |
| Spark Plugs | 120,000 mi | - | Iridium plugs |
| Brake Fluid | - | 24 mo | Critical for hybrid braking |

### Hybrid-Specific Maintenance

- **Hybrid Battery Cooling System**: Annual inspection
- **Inverter Coolant**: Check level regularly (separate from engine coolant)
- **12V Auxiliary Battery**: Replace every 3-5 years
- **Regenerative Brake System**: Inspect annually

## NHTSA API Integration

The plugin uses the free NHTSA API to fetch:

- **Safety Recalls**: Official recalls by campaign number
- **Consumer Complaints**: Real owner complaints filed with NHTSA
- **Common Issues**: Trending problems for this vehicle

Data is cached locally and refreshed on demand (recommended monthly).

### Manual API Usage

You can also use the API tools directly:

```bash
# Update NHTSA cache
./tools/nhtsa_api.py update

# View recalls
./tools/nhtsa_api.py recalls

# View common issues
./tools/nhtsa_api.py issues
```

## Tools

### `nhtsa_api.py`

Python script for NHTSA API integration using PEP 723 inline dependencies.

**Features:**
- Fetch recalls by make/model/year
- Fetch consumer complaints
- Cache results locally
- Display formatted tables

**Requirements:**
- Python 3.13+
- uv (for dependency management)
- requests, rich (auto-installed via uv)

### `maintenance_manager.py`

Python script for maintenance record management.

**Features:**
- Add work orders
- Check due maintenance
- List work order history
- Update maintenance intervals
- Calculate due dates based on mileage and time

**Requirements:**
- Python 3.13+
- uv
- rich (auto-installed via uv)

## Tips for Best Results

1. **Update mileage regularly** (monthly) for accurate due date calculations
2. **Refresh NHTSA data monthly** to catch new recalls immediately
3. **Use 0W-20 synthetic oil ONLY** - critical for hybrid engine longevity
4. **Keep detailed notes** in work orders - helps with resale value
5. **Track your service providers** - build relationships with hybrid specialists
6. **Monitor hybrid battery cooling** - keep vents behind rear seat clear

## Known Issues for 2013 RX450h

Common problems reported to NHTSA (will vary based on cached data):

- Inverter coolant pump failures
- Brake actuator issues (ABS/VSC lights)
- Transmission shift quality (software updates available)
- Water pump leaks
- Dashboard cracking (TSB available)

## Customization

### Adding Custom Maintenance Items

Edit `data/maintenance-records.json` to add custom maintenance items to the `upcoming_maintenance` array:

```json
{
  "id": "custom-item",
  "name": "Custom Maintenance Item",
  "interval_miles": 10000,
  "interval_months": 12,
  "last_completed_mileage": null,
  "last_completed_date": null,
  "notes": "Your custom notes"
}
```

### Adjusting Intervals

You can customize maintenance intervals in `data/maintenance-records.json` to match your driving conditions:

- **Severe driving conditions**: Reduce intervals by 25-50%
- **Highway driving**: Can extend some intervals slightly
- **Hybrid battery**: More frequent inspections in hot climates

## Dependencies

- Python 3.13+
- uv (for PEP 723 script dependency management)
- requests library (auto-installed)
- rich library (auto-installed)

## Support

For issues or questions:
1. Check the lexus-maintenance skill for guidance
2. Review NHTSA data for common issues
3. Consult Lexus dealer or hybrid specialist

## Version History

- **0.1.0** (2025-01-02): Initial release
  - Basic maintenance tracking
  - NHTSA API integration
  - Slash commands for common operations
  - 2013 RX450h specific maintenance schedule

## License

Part of the lunar-claude plugin marketplace.

## Author

basher83
