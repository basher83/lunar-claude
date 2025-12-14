#!/bin/bash
# Post-session evaluation script
# Run this AFTER closing the Claude session to check generated code quality

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <path-to-generated-ansible-file-or-dir>"
    echo ""
    echo "Example:"
    echo "  $0 ansible/playbooks/install-docker.yml"
    echo "  $0 ansible/roles/docker/"
    exit 1
fi

TARGET="$1"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)

echo "=========================================="
echo "Ansible Workflows - Post-Session Evaluation"
echo "=========================================="
echo "Target: $TARGET"
echo "Time: $TIMESTAMP"
echo ""

# Check if target exists
if [[ ! -e "$TARGET" ]]; then
    echo "ERROR: Target does not exist: $TARGET"
    exit 1
fi

echo "=== 1. Syntax Check ==="
if uv run ansible-playbook "$TARGET" --syntax-check 2>&1; then
    echo "PASS: Syntax check passed"
else
    echo "FAIL: Syntax check failed"
fi
echo ""

echo "=== 2. Ansible Lint ==="
LINT_OUTPUT=$(uv run ansible-lint "$TARGET" 2>&1 || true)
LINT_ERRORS=$(echo "$LINT_OUTPUT" | grep -c "error" || echo "0")
LINT_WARNINGS=$(echo "$LINT_OUTPUT" | grep -c "warning" || echo "0")
echo "$LINT_OUTPUT"
echo ""
echo "Summary: $LINT_ERRORS errors, $LINT_WARNINGS warnings"
echo ""

echo "=== 3. FQCN Check ==="
# Look for short module names (modules without dots)
SHORT_MODULES=$(grep -En "^\s+-\s+[a-z_]+:" "$TARGET" 2>/dev/null | grep -v "name:" | grep -v "when:" | grep -v "register:" | grep -v "loop:" | grep -v "vars:" | grep -v "block:" | grep -v "rescue:" | grep -v "always:" || echo "")
if [[ -z "$SHORT_MODULES" ]]; then
    echo "PASS: No obvious short module names found"
else
    echo "WARNING: Possible short module names (should use FQCN):"
    echo "$SHORT_MODULES"
fi
echo ""

echo "=== 4. Idempotency Indicators ==="
# Check for command/shell without changed_when
COMMAND_TASKS=$(grep -En "ansible.builtin.(command|shell):" "$TARGET" 2>/dev/null || echo "")
if [[ -n "$COMMAND_TASKS" ]]; then
    echo "Found command/shell tasks:"
    echo "$COMMAND_TASKS"
    echo ""
    # Check if changed_when exists near these
    CHANGED_WHEN_COUNT=$(grep -c "changed_when:" "$TARGET" 2>/dev/null || echo "0")
    echo "changed_when directives found: $CHANGED_WHEN_COUNT"
else
    echo "No command/shell tasks found"
fi
echo ""

echo "=== 5. Security Indicators ==="
# Check for potential hardcoded secrets
SECRETS=$(grep -Ein "(password|secret|token|api_key).*[:=].*['\"][^{]" "$TARGET" 2>/dev/null || echo "")
if [[ -z "$SECRETS" ]]; then
    echo "PASS: No obvious hardcoded secrets"
else
    echo "WARNING: Potential hardcoded secrets:"
    echo "$SECRETS"
fi

# Check for no_log usage
NO_LOG_COUNT=$(grep -c "no_log:" "$TARGET" 2>/dev/null || echo "0")
echo "no_log directives found: $NO_LOG_COUNT"
echo ""

echo "=========================================="
echo "Evaluation complete. Review results above."
echo "=========================================="
