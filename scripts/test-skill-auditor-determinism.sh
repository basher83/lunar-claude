#!/bin/bash
# Test skill-auditor for deterministic output across multiple runs

set -e

SKILL_PATH="${1:-plugins/meta/meta-claude/skills/skill-factory}"
RUNS=3

echo "Testing skill-auditor determinism with $RUNS runs on: $SKILL_PATH"
echo "=================================================================="

# Run auditor multiple times and extract key metrics
for i in $(seq 1 $RUNS); do
    echo "Run $i..."
    ./scripts/skill-auditor.py "$SKILL_PATH" > "/tmp/audit-run-$i.txt" 2>&1

    # Extract deterministic metrics to separate file
    {
        grep "^**Status:**" "/tmp/audit-run-$i.txt" || echo "No status found"
        grep "^   - Quoted phrases:" "/tmp/audit-run-$i.txt" || echo "No quoted phrases count"
        grep "^   - Domain indicators:" "/tmp/audit-run-$i.txt" || echo "No domain indicators count"
        grep "^   - Line count:" "/tmp/audit-run-$i.txt" || echo "No line count"
        grep "^- Blockers:" "/tmp/audit-run-$i.txt" || echo "No blocker count"
        grep "^- Warnings:" "/tmp/audit-run-$i.txt" || echo "No warning count"
    } > "/tmp/audit-metrics-$i.txt"

    cat "/tmp/audit-metrics-$i.txt"
done

echo ""
echo "Comparing runs for consistency..."

# Compare extracted metrics (not full output, as Claude text varies)
if diff -q /tmp/audit-metrics-1.txt /tmp/audit-metrics-2.txt && \
   diff -q /tmp/audit-metrics-2.txt /tmp/audit-metrics-3.txt; then
    echo "✅ PASS: All runs produced identical metrics (deterministic)"
    exit 0
else
    echo "❌ FAIL: Runs produced different metrics (non-deterministic)"
    echo ""
    echo "Metric differences:"
    diff /tmp/audit-metrics-1.txt /tmp/audit-metrics-2.txt || true
    exit 1
fi
