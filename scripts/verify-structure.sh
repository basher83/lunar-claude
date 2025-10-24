#!/usr/bin/env bash
set -euo pipefail

# Verify lunar-claude marketplace structure

echo "Verifying lunar-claude marketplace structure..."

# Check core directories
echo "✓ Checking core directories..."
[[ -d "plugins/meta" ]] || { echo "✗ Missing plugins/meta"; exit 1; }
[[ -d "plugins/infrastructure" ]] || { echo "✗ Missing plugins/infrastructure"; exit 1; }
[[ -d "plugins/devops" ]] || { echo "✗ Missing plugins/devops"; exit 1; }
[[ -d "plugins/homelab" ]] || { echo "✗ Missing plugins/homelab"; exit 1; }
[[ -d "templates/plugin-template" ]] || { echo "✗ Missing templates/plugin-template"; exit 1; }

# Check marketplace.json
echo "✓ Checking marketplace.json..."
[[ -f ".claude-plugin/marketplace.json" ]] || { echo "✗ Missing marketplace.json"; exit 1; }
jq empty .claude-plugin/marketplace.json || { echo "✗ Invalid JSON in marketplace.json"; exit 1; }

# Check template structure
echo "✓ Checking template structure..."
[[ -f "templates/plugin-template/.claude-plugin/plugin.json" ]] || { echo "✗ Missing template plugin.json"; exit 1; }
[[ -f "templates/plugin-template/README.md" ]] || { echo "✗ Missing template README"; exit 1; }
[[ -f "templates/plugin-template/agents/example-agent.md" ]] || { echo "✗ Missing example agent"; exit 1; }
[[ -f "templates/plugin-template/skills/example-skill/SKILL.md" ]] || { echo "✗ Missing example skill"; exit 1; }

# Check meta-claude plugin
echo "✓ Checking meta-claude plugin..."
[[ -d "plugins/meta/meta-claude" ]] || { echo "✗ Missing meta-claude plugin"; exit 1; }
[[ -f "plugins/meta/meta-claude/.claude-plugin/plugin.json" ]] || { echo "✗ Missing meta-claude manifest"; exit 1; }

# Check meta-claude skills
echo "✓ Checking meta-claude skills..."
[[ -f "plugins/meta/meta-claude/skills/skill-creator/SKILL.md" ]] || { echo "✗ Missing skill-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/agent-creator/SKILL.md" ]] || { echo "✗ Missing agent-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/hook-creator/SKILL.md" ]] || { echo "✗ Missing hook-creator"; exit 1; }
[[ -f "plugins/meta/meta-claude/skills/command-creator/SKILL.md" ]] || { echo "✗ Missing command-creator"; exit 1; }

# Check meta-claude command
echo "✓ Checking meta-claude command..."
[[ -f "plugins/meta/meta-claude/commands/new-plugin.md" ]] || { echo "✗ Missing new-plugin command"; exit 1; }

# Verify marketplace contains meta-claude
echo "✓ Checking marketplace registration..."
jq -e '.plugins[] | select(.name == "meta-claude")' .claude-plugin/marketplace.json > /dev/null || { echo "✗ meta-claude not in marketplace"; exit 1; }

echo ""
echo "✅ All verification checks passed!"
echo "Marketplace structure is valid and complete."
