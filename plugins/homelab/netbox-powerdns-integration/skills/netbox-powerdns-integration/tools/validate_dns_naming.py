#!/usr/bin/env -S uv run --script --quiet
# /// script
# dependencies = []
# ///
"""
Validate DNS names against Virgo-Core naming convention.

Naming Convention: <service>-<NN>-<purpose>.<domain>
Example: docker-01-nexus.spaceships.work

Usage:
    ./validate_dns_naming.py docker-01-nexus.spaceships.work
    ./validate_dns_naming.py --file hostnames.txt
    ./validate_dns_naming.py --check-format docker-1-nexus.spaceships.work
"""

import argparse
import re
import sys
from typing import Tuple


class DNSNameValidator:
    """Validates DNS names against naming convention."""

    # Pattern: <service>-<NN>-<purpose>.<domain>
    PATTERN = r'^[a-z0-9-]+-\d{2}-[a-z0-9-]+\.[a-z0-9.-]+$'

    # Common service types
    KNOWN_SERVICES = {
        'docker', 'k8s', 'proxmox', 'storage', 'db', 'network',
        'app', 'vip', 'service', 'test', 'dev', 'staging', 'prod'
    }

    def __init__(self):
        self.pattern = re.compile(self.PATTERN)

    def validate(self, name: str) -> Tuple[bool, str, dict]:
        """
        Validate DNS name.

        Returns:
            (is_valid, message, details_dict)
        """
        # Basic pattern match
        if not self.pattern.match(name):
            return False, "Name doesn't match pattern: <service>-<NN>-<purpose>.<domain>", {}

        # Split into components
        parts = name.split('.')
        if len(parts) < 2:
            return False, "Must include domain", {}

        hostname = parts[0]
        domain = '.'.join(parts[1:])

        # Split hostname
        components = hostname.split('-')
        if len(components) < 3:
            return False, "Hostname must have at least 3 components: <service>-<NN>-<purpose>", {}

        service = components[0]
        number = components[1]
        purpose = '-'.join(components[2:])  # Purpose can have hyphens

        # Validate number component (must be 2 digits)
        if not number.isdigit() or len(number) != 2:
            return False, f"Number component '{number}' must be exactly 2 digits (01-99)", {}

        # Additional checks
        warnings = []

        # Check for known service type
        if service not in self.KNOWN_SERVICES:
            warnings.append(f"Service '{service}' not in known types (informational)")

        # Check for uppercase
        if name != name.lower():
            return False, "Name must be lowercase only", {}

        # Check for invalid characters
        if not re.match(r'^[a-z0-9.-]+$', name):
            return False, "Name contains invalid characters (only a-z, 0-9, -, . allowed)", {}

        # Build details
        details = {
            'service': service,
            'number': number,
            'purpose': purpose,
            'domain': domain,
            'warnings': warnings
        }

        message = "Valid"
        if warnings:
            message = f"Valid (with warnings: {', '.join(warnings)})"

        return True, message, details

    def validate_batch(self, names: list) -> dict:
        """
        Validate multiple names.

        Returns:
            {
                'valid': [(name, details), ...],
                'invalid': [(name, reason), ...]
            }
        """
        results = {'valid': [], 'invalid': []}

        for name in names:
            name = name.strip()
            if not name or name.startswith('#'):
                continue

            is_valid, message, details = self.validate(name)
            if is_valid:
                results['valid'].append((name, details))
            else:
                results['invalid'].append((name, message))

        return results


def print_validation_result(name: str, is_valid: bool, message: str, details: dict, verbose: bool = False):
    """Print formatted validation result."""
    status = "✓" if is_valid else "✗"
    print(f"{status} {name}: {message}")

    if verbose and is_valid and details:
        print(f"    Service: {details.get('service')}")
        print(f"    Number: {details.get('number')}")
        print(f"    Purpose: {details.get('purpose')}")
        print(f"    Domain: {details.get('domain')}")

        warnings = details.get('warnings', [])
        if warnings:
            print(f"    Warnings:")
            for warning in warnings:
                print(f"      - {warning}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate DNS names against Virgo-Core naming convention",
        epilog="Pattern: <service>-<NN>-<purpose>.<domain>\nExample: docker-01-nexus.spaceships.work"
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="DNS name to validate"
    )
    parser.add_argument(
        "--file",
        help="File containing DNS names (one per line)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed component breakdown"
    )
    parser.add_argument(
        "--check-format",
        action="store_true",
        help="Only check format, don't suggest corrections"
    )

    args = parser.parse_args()

    validator = DNSNameValidator()

    # Batch mode from file
    if args.file:
        try:
            with open(args.file, 'r') as f:
                names = f.readlines()
        except IOError as e:
            print(f"❌ Failed to read file: {e}", file=sys.stderr)
            sys.exit(1)

        results = validator.validate_batch(names)

        print(f"\n📊 Validation Results:")
        print(f"   Valid: {len(results['valid'])}")
        print(f"   Invalid: {len(results['invalid'])}")

        if results['invalid']:
            print(f"\n✗ Invalid Names:")
            for name, reason in results['invalid']:
                print(f"   {name}")
                print(f"      Reason: {reason}")

        if results['valid']:
            print(f"\n✓ Valid Names:")
            for name, details in results['valid']:
                print(f"   {name}")
                if args.verbose:
                    print(f"      Service: {details['service']}, Number: {details['number']}, Purpose: {details['purpose']}")

        sys.exit(0 if len(results['invalid']) == 0 else 1)

    # Single name mode
    if not args.name:
        print("❌ Provide a DNS name or use --file", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    is_valid, message, details = validator.validate(args.name)
    print_validation_result(args.name, is_valid, message, details, args.verbose)

    # Provide suggestions for common mistakes
    if not is_valid and not args.check_format:
        print(f"\n💡 Common Issues:")
        print(f"   - Use lowercase only: {args.name.lower()}")
        print(f"   - Use hyphens, not underscores: {args.name.replace('_', '-')}")
        print(f"   - Number must be 2 digits: docker-1-app → docker-01-app")
        print(f"   - Pattern: <service>-<NN>-<purpose>.<domain>")
        print(f"   - Example: docker-01-nexus.spaceships.work")

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
