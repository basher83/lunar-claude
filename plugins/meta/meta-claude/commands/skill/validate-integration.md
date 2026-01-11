---
description: Test skill integration with Claude Code ecosystem (conflict detection and compatibility)
allowed-tools: Bash(test:*), Bash(find:*), Bash(rg:*), Bash(git:*), Read
---

# Skill Validate Integration

Test skill integration with Claude Code ecosystem (conflict detection and compatibility).

## Usage

```bash
/meta-claude:skill:validate-integration $ARGUMENTS
```

**Arguments:**

- `$1`: Path to the skill directory to validate (required)

## What This Does

Validates that the skill integrates cleanly with the Claude Code ecosystem:

- **Naming Conflicts:** Verifies no duplicate skill names exist
- **Functionality Overlap:** Checks for overlapping descriptions/purposes
- **Command Composition:** Tests compatibility with slash commands
- **Component Integration:** Validates interaction with other meta-claude components
- **Ecosystem Fit:** Ensures skill complements existing capabilities

**Note:** This is integration validation - it tests ecosystem compatibility, not runtime behavior.

## Instructions

Your task is to perform integration validation checks on the skill at the provided path.

### Step 1: Verify Skill Exists

Verify that the skill directory contains a valid SKILL.md file:

!`test -f "$1/SKILL.md" && echo "SKILL.md exists" || echo "Error: SKILL.md not found"`

If SKILL.md does not exist, report error and exit.

### Step 2: Extract Skill Metadata

Read the SKILL.md frontmatter to extract key metadata. The frontmatter format is:

```yaml
---
name: skill-name
description: Skill description text
---
```

**Extract the following from the skill at `$1/SKILL.md`:**

- Skill name
- Skill description
- Any additional metadata fields

Use this metadata for conflict detection and overlap analysis.

### Step 3: Check for Naming Conflicts

Search for existing skills with the same name across the marketplace.

**Find all SKILL.md files:**

!`find "$(git rev-parse --show-toplevel)/plugins" -type f -name "SKILL.md"`

**For each existing skill, perform the following analysis:**

1. Extract the skill name from frontmatter
2. Compare with the new skill's name (from `$1/SKILL.md`)
3. If names match, record as a naming conflict

**Detect these types of conflicts:**

- Exact name matches (case-insensitive comparison)
- Similar names that differ only by pluralization
- Names that differ only in separators (hyphens vs underscores)

### Step 4: Detect Functionality Overlap

Analyze skill descriptions to identify overlapping functionality:

**Compare:**

- Skill descriptions for semantic similarity
- Key phrases and trigger words
- Domain overlap (e.g., both handle "Docker containers")
- Use case overlap (e.g., both create infrastructure as code)

**Overlap categories:**

- **Duplicate:** Essentially the same functionality (HIGH concern)
- **Overlapping:** Significant overlap but different focus (MEDIUM concern)
- **Complementary:** Related but distinct functionality (LOW concern)
- **Independent:** No overlap (PASS)

**Analysis approach:**

1. **Extract key terms** from both descriptions:
   - Tokenize descriptions (split on whitespace, punctuation)
   - Remove stopwords (the, a, an, is, are, for, etc.)
   - Identify domain keywords (docker, kubernetes, terraform, ansible, etc.)

2. **Calculate semantic overlap score** using Jaccard similarity:
   - Intersection: Terms present in both descriptions
   - Union: All unique terms from both descriptions
   - Score = (Intersection size / Union size) * 100
   - Example: If 7 of 10 unique terms overlap → 70% score

3. **Categorize overlap based on score**:
   - **Duplicate:** >70% term overlap or identical purpose
   - **Overlapping:** 50-70% term overlap with different focus
   - **Complementary:** 30-50% overlap, related domain
   - **Independent:** <30% overlap

4. **Flag if overlap exceeds threshold** (>70% duplicate, >50% overlapping)

### Step 5: Test Slash Command Composition

Verify the skill can work with existing slash commands by checking for:

- References to non-existent commands
- Circular dependencies between skills and commands
- Incompatible parameter expectations
- Missing prerequisite commands

**Find all slash command references:**

!`rg -o '/[a-z][a-z0-9-]+\b' "$1/SKILL.md"`

**For each referenced command, perform these checks:**

1. Verify command exists in marketplace
2. Check parameter compatibility
3. Ensure no circular dependencies
4. Validate execution order makes sense

### Step 6: Validate Component Integration

Verify compatibility with other meta-claude components.

**Analyze integration with these meta-claude components:**

- **Skills:** Other skills in meta-claude plugin
- **Agents:** Agent definitions that might invoke this skill
- **Hooks:** Automation hooks that trigger skills
- **Commands:** Slash commands in the same plugin

**Perform these integration checks:**

1. Verify skill doesn't conflict with existing meta-claude workflows
2. Check if skill references valid agent definitions
3. Ensure skill uses correct hook event names
4. Validate skill works with plugin architecture

**Examples of what to verify:**

- If skill references `/meta-claude:skill:create`, verify it exists
- If skill mentions "skill-auditor agent", verify agent exists
- If skill uses hooks, verify hook events are valid
- If skill depends on scripts, verify they exist

### Step 7: Assess Ecosystem Fit

Evaluate whether the skill complements existing capabilities:

**Assessment criteria:**

- **Fills a gap:** Provides functionality not currently available
- **Enhances existing:** Improves or extends current capabilities
- **Consolidates:** Combines fragmented functionality
- **Replaces:** Better alternative to existing skill (requires justification)

**Red flags:**

- Skill provides identical functionality to existing skill
- Skill conflicts with established patterns
- Skill introduces breaking changes
- Skill duplicates without clear improvement

### Generate Integration Report

Generate a structured report in the following format:

```markdown
## Integration Validation Report: <skill-name>

**Overall Status:** PASS | FAIL

### Summary

[1-2 sentence overview of integration validation results]

### Validation Results

- Naming Conflicts: PASS | FAIL
- Functionality Overlap: PASS | FAIL
- Command Composition: PASS | FAIL
- Component Integration: PASS | FAIL
- Ecosystem Fit: PASS | FAIL

### Conflicts Found

#### Critical (Must Resolve)
[Conflicts that prevent integration]
- [ ] Conflict description with affected component

#### Warning (Should Review)
[Potential issues that need attention]
- [ ] Issue description with recommendation

#### Info (Consider)
[Minor considerations or enhancements]
- [ ] Suggestion for better integration

### Integration Details

**Existing Skills Analyzed:** [count]
**Commands Referenced:** [list]
**Agents Referenced:** [list]
**Conflicts Detected:** [count]
**Overlap Analysis:**
- Duplicate functionality: [list]
- Overlapping functionality: [list]
- Complementary skills: [list]

### Recommendations

[Specific, actionable suggestions for improving integration]

### Next Steps

[What to do based on validation results]
```

## Error Handling

**If SKILL.md not found:**

```text
Error: SKILL.md not found at $1
```

Report this error and advise verifying the path is correct or running `/meta-claude:skill:create` first.

**If integration validation passes:**

Report the following:

- Status: "Integration Validation: PASS"
- Validation results summary
- Any complementary skills found
- Success confirmation

**If integration validation fails:**

Report the following:

- Status: "Integration Validation: FAIL"
- All conflicts categorized by severity
- Specific resolution recommendations
- Failure indication

**Conflict Severity Levels:**

- **Critical:** Must resolve before deployment (exact name conflict, duplicate functionality)
- **Warning:** Should address before deployment (high overlap, missing commands)
- **Info:** Consider for better integration (similar names, potential consolidation)

## Pass Criteria

Integration validation PASSES if:

- No exact naming conflicts found
- Functionality overlap below threshold (<50%)
- All referenced commands exist
- Compatible with meta-claude architecture
- Complements existing ecosystem

Integration validation FAILS if:

- Exact skill name already exists
- Duplicate functionality without improvement
- References non-existent commands
- Breaks existing component integration
- Conflicts with established patterns

## Examples

**Skill with clean integration:**

```bash
/meta-claude:skill:validate-integration plugins/meta/meta-claude/skills/docker-security
# Output: Integration Validation: PASS
# - No naming conflicts detected
# - Functionality is complementary to existing skills
# - All referenced commands exist
# - Compatible with meta-claude components
# - Fills gap in security analysis domain
```

**Skill with naming conflict:**

```bash
/meta-claude:skill:validate-integration /path/to/duplicate-skill
# Output: Integration Validation: FAIL
#
# Conflicts Found:
# Critical:
# - Skill name 'skill-factory' already exists in plugins/meta/meta-claude/skills/skill-factory
# - Exact duplicate functionality: both create SKILL.md files
# Recommendation: Choose different name or consolidate with existing skill
```

**Skill with functionality overlap:**

```bash
/meta-claude:skill:validate-integration /path/to/overlapping-skill
# Output: Integration Validation: FAIL
#
# Conflicts Found:
# Warning:
# - 75% description overlap with 'python-code-quality' skill
# - Both skills handle Python linting and formatting
# - Referenced command '/run-pytest' does not exist
# Recommendation: Consider consolidating or clearly differentiating scope
```

**Skill with minor concerns:**

```bash
/meta-claude:skill:validate-integration /path/to/new-skill
# Output: Integration Validation: PASS
#
# Info:
# - Skill name similar to 'ansible-best-practice' (note singular vs plural)
# - Could complement 'ansible-best-practices' skill with cross-references
# - Consider mentioning relationship in description
```

## Notes

- This validation tests **ecosystem integration**, not runtime or compliance
- Run after `/meta-claude:skill:validate-runtime` passes
- Focuses on conflicts with existing skills, commands, and components
- Sequential dependency: requires runtime validation to pass first
- Integration issues often require human judgment to resolve
- Consider both technical conflicts and strategic fit
- Some overlap may be acceptable if skills serve different use cases
- Clear differentiation in descriptions helps avoid false positives
