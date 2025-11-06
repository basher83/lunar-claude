# Plugin Auditor Agent Design

**Date:** 2025-11-06
**Status:** Design Complete
**Implementation:** Pending

## Purpose

The plugin-auditor agent validates Claude Code plugins against official specifications. It ensures plugins meet structural requirements, follow best practices, and integrate correctly with the Claude Code plugin system.

## Design Rationale

### Pattern Consistency

The plugin-auditor follows the claude-skill-auditor pattern:
- Bakes domain knowledge into the agent definition
- Uses standardized report format
- Limits tools to necessary operations
- Provides comprehensive checklists

This consistency makes the auditor system predictable and maintainable.

### Scope Determination

The plugin specification defines validation scope:
- Plugin manifest (`.claude-plugin/plugin.json`) is required
- All component directories (commands/, agents/, skills/, hooks/) are optional
- Components must follow placement rules when present

The auditor validates what exists, not what might exist.

## Agent Specification

### Frontmatter

```yaml
name: claude-plugin-auditor
description: Expert Claude Code plugin reviewer that validates plugins against official specifications. Use PROACTIVELY after creating or modifying any plugin structure, components, or manifests.
tools: Read, Grep, Glob, Bash
model: inherit
```

### Core Knowledge Base

The agent has expert-level knowledge from these sources:

- **plugins.md**: Plugin fundamentals, quickstart patterns, directory structure
- **plugins-reference.md**: Complete technical specs, schemas, component specifications
- **plugin-marketplaces.md**: Marketplace structure and distribution requirements

This knowledge is embedded in the agent prompt, not loaded dynamically.

## Validation Workflow

1. **Locate plugin directory** - Use Glob to find `.claude-plugin/plugin.json`
2. **Read all files** - Plugin manifest, component files, documentation
3. **Execute audit** - Systematically check every requirement
4. **Generate report** - Use standardized format with specific fixes

## Validation Checklist

### 1. Plugin Manifest (CRITICAL)

**Always validated:**
- `name` field exists
- `name` follows kebab-case format (no spaces, lowercase)
- JSON syntax is valid
- Path fields (if present) use relative paths starting with `./`

**Optional fields (validate if present):**
- `version` follows semantic versioning
- `description` is clear and informative
- `author` object has valid structure
- `homepage` and `repository` are valid URLs
- `keywords` array aids discoverability
- Component path overrides use correct format

### 2. Directory Structure

**Placement rules:**
- `.claude-plugin/` contains only `plugin.json`
- Component directories exist at plugin root
- No components inside `.claude-plugin/` directory

**Standard locations:**
- `commands/` for slash commands
- `agents/` for subagent definitions
- `skills/` for Agent Skills
- `hooks/` for event handlers
- `.mcp.json` for MCP servers

### 3. Component Validation (Conditional)

**Commands** (if `commands/` exists):
- Markdown files with YAML frontmatter
- `description` field in frontmatter
- Clear command purpose and usage

**Agents** (if `agents/` exists):
- Markdown files with agent structure
- `description` and `capabilities` in frontmatter
- Clear specialization and use cases

**Skills** (if `skills/` exists):
- Directories containing `SKILL.md` files
- Delegate deep validation to claude-skill-auditor
- Check basic structure and placement

**Hooks** (if `hooks/hooks.json` or inline exists):
- Valid JSON configuration
- Recognized event types
- Script paths use `${CLAUDE_PLUGIN_ROOT}`
- Scripts exist at specified paths

**MCP Servers** (if `.mcp.json` or inline exists):
- Valid JSON configuration
- Server commands and paths defined
- Environment variables properly configured

### 4. Cross-Component Coherence

**Reference validation:**
- Custom component paths in plugin.json point to existing files
- Hook scripts exist at specified paths
- No orphaned files or directories

**Consistency checks:**
- `${CLAUDE_PLUGIN_ROOT}` used for all plugin-relative paths
- Naming conventions consistent across components
- No conflicting configurations

### 5. Documentation & Best Practices

**Recommended elements:**
- README.md describes plugin purpose and usage
- LICENSE file specifies terms
- Semantic versioning in plugin.json
- Keywords aid plugin discovery
- CHANGELOG.md tracks version history

## Report Format

The auditor generates reports matching claude-skill-auditor structure:

### Executive Summary
- Overall status (PASS / NEEDS_IMPROVEMENT / FAIL)
- Issue counts by severity
- Files reviewed
- Plugin location

### Critical Issues ❌
**Must fix before use**

Format per issue:
- **Issue**: Brief description
- **Location**: file:line or section
- **Current**: What exists now
- **Required**: What specification demands
- **Fix**: Specific action to resolve
- **Reference**: Which specification this violates

### Warnings ⚠️
**Should fix for quality**

Format per warning:
- **Issue**: Brief description
- **Location**: file:line or section
- **Current**: What exists now
- **Recommended**: What improves quality
- **Impact**: Why this matters
- **Reference**: Which best practice this relates to

### Suggestions 💡
**Consider improving**

Format per suggestion:
- **Enhancement**: Description
- **Benefit**: Why this improves the plugin
- **Example**: How to implement

### Category Breakdown
Checklist results with ✓/✗ indicators for each validated item

### Actionable Recommendations
Numbered list of specific fixes with file:line references

### Positive Observations ✅
What the plugin does well (balanced feedback)

### Testing Recommendations
How to verify the plugin works correctly

### Compliance Summary
Percentage compliance with official requirements and best practices

## Issue Prioritization

### Critical (Must Fix)
Violations of required specifications:
- Missing or invalid plugin.json
- Invalid `name` field
- Components in wrong directories
- Invalid JSON syntax

### Warning (Should Fix)
Violations of best practices:
- Missing README.md
- No version specified
- Incorrect component format
- Missing documentation

### Suggestion (Consider)
Optional improvements:
- Add keywords for discoverability
- Include LICENSE file
- Add CHANGELOG.md
- Improve documentation clarity

## Tool Usage

- **Read**: Examine plugin.json, component files, documentation
- **Grep**: Search for patterns (reserved words, path formats, XML tags)
- **Glob**: Find component files and directories
- **Bash**: Count lines, check directory structure, verify file placement

## Integration Points

### With claude-skill-auditor
When the plugin contains skills:
- Perform high-level structure check
- Note that skills exist
- Recommend running claude-skill-auditor for deep skill validation
- Do not duplicate skill-specific checks

### With Plugin System
The auditor validates against:
- Official plugin specifications from docs.claude.com
- Claude Code's plugin loading requirements
- Marketplace distribution standards

## Success Criteria

A plugin passes audit when:
1. Plugin manifest exists and validates
2. All present components follow their specifications
3. Directory structure matches requirements
4. Cross-component references are valid
5. No critical issues remain

Warnings and suggestions do not prevent passing.

## Implementation Notes

### Agent Location
`.claude/agents/claude-plugin-auditor.md`

### Invocation Patterns
- Automatic: "Review the plugin structure"
- Explicit: "Use claude-plugin-auditor to validate this plugin"
- Proactive: After any plugin structure or manifest changes

### Context Management
- Operates in separate context window
- Returns complete report to main thread
- Does not maintain state between invocations

## Future Considerations

### Marketplace Validation
Future versions could validate:
- Marketplace.json structure
- Plugin source paths
- Marketplace metadata

### Automated Fixes
Could offer to fix common issues:
- Create missing README.md
- Add version field to plugin.json
- Fix directory structure

### Integration Testing
Could validate:
- Plugin actually loads in Claude Code
- Commands appear in /help
- Agents appear in /agents
- Hooks execute correctly

## References

- Claude Code official documentation (docs.claude.com)
- claude-skill-auditor agent definition
- multi-agent-composition framework
- Plugin specification from plugins-reference.md
