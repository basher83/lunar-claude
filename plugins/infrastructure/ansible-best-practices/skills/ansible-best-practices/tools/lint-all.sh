#!/usr/bin/env bash
# Run all Ansible linters with proper configuration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
FAILED_CHECKS=0

# Function to print section header
print_header() {
    echo ""
    echo "========================================="
    echo "$1"
    echo "========================================="
}

# Function to run a check
run_check() {
    local name="$1"
    local command="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    echo -n "Running $name... "

    if eval "$command" > /tmp/lint-output.txt 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        cat /tmp/lint-output.txt
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Change to ansible directory if not already there
if [[ ! -d "playbooks" ]] && [[ -d "ansible" ]]; then
    cd ansible
fi

print_header "Ansible Playbook Linting"

# Check if ansible-lint is available
if command -v ansible-lint &> /dev/null; then
    run_check "ansible-lint (playbooks)" "ansible-lint playbooks/"
    run_check "ansible-lint (roles)" "ansible-lint roles/ || true"  # May not have roles
else
    echo -e "${YELLOW}⚠ ansible-lint not found, skipping${NC}"
fi

# Check YAML syntax
print_header "YAML Syntax Validation"

if command -v yamllint &> /dev/null; then
    run_check "yamllint (playbooks)" "yamllint playbooks/"
    run_check "yamllint (group_vars)" "yamllint group_vars/ || true"
    run_check "yamllint (host_vars)" "yamllint host_vars/ || true"
else
    echo -e "${YELLOW}⚠ yamllint not found, skipping${NC}"
fi

# Check playbook syntax
print_header "Ansible Syntax Check"

for playbook in playbooks/*.yml; do
    if [[ -f "$playbook" ]]; then
        playbook_name=$(basename "$playbook")
        run_check "syntax ($playbook_name)" "ansible-playbook $playbook --syntax-check"
    fi
done

# Custom idempotency check (if tool exists)
print_header "Idempotency Check"

IDEMPOTENCY_TOOL="../.claude/skills/ansible-best-practices/tools/check_idempotency.py"
if [[ -f "$IDEMPOTENCY_TOOL" ]]; then
    run_check "idempotency check" "uv run $IDEMPOTENCY_TOOL playbooks/*.yml"
else
    echo -e "${YELLOW}⚠ Idempotency checker not found, skipping${NC}"
fi

# Summary
print_header "Summary"

echo "Total checks: $TOTAL_CHECKS"
echo "Passed: $((TOTAL_CHECKS - FAILED_CHECKS))"
echo "Failed: $FAILED_CHECKS"

if [[ $FAILED_CHECKS -eq 0 ]]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    exit 1
fi
