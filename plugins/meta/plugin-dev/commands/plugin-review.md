---
description: Comprehensive plugin review workflow with state tracking, best practice validation, and improvement recommendations
argument-hint: <plugin-path>
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill", "Task", "TodoWrite", "AskUserQuestion"]
---

# Plugin Review Workflow

Systematically review a Claude Code plugin against best practices from plugin-dev skills. Creates a state file to track progress and enables resumable reviews.

**Target plugin:** $ARGUMENTS

---

## Core Principles

- **State file tracking**: Create `.claude/<plugin-name>-review.local.md` to track all progress
- **Skill-based validation**: Load relevant plugin-dev skills and validate against documented patterns
- **Proof-based decisions**: When recommending changes, cite specific guidance from skills
- **Incremental commits**: Commit improvements as they're made, track commit SHAs in state file
- **Resumable**: If session ends, next session can continue from state file

---

## Phase 0: Setup

**Goal**: Validate plugin path and create state file

**Actions**:

1. Validate the plugin path exists and has `.claude-plugin/plugin.json`
2. Read plugin.json to get plugin name and version
3. Auto-discover plugin components:
   ```bash
   # Commands
   ls <plugin-path>/commands/*.md 2>/dev/null | wc -l

   # Agents
   ls <plugin-path>/agents/*.md 2>/dev/null | wc -l

   # Skills
   find <plugin-path>/skills -name "SKILL.md" 2>/dev/null | wc -l

   # Hooks
   test -f <plugin-path>/hooks/hooks.json && echo "yes" || echo "no"
   ```
4. Create state file at `.claude/<plugin-name>-review.local.md`:

```markdown
---
workflow: plugin-review
plugin: <plugin-name>
plugin_path: <plugin-path>
status: in_progress
started: <date>
last_updated: <date>
phase: discovery
plugin_version: <version>
---

# <Plugin-Name> Plugin Review

Comprehensive review against plugin-dev best practices.

## Component Inventory

| Component | Path | Count | Status |
|-----------|------|-------|--------|
| plugin.json | `.claude-plugin/plugin.json` | 1 | pending |
| README.md | `README.md` | 1 | pending |
| Commands | `commands/` | <n> | pending |
| Agents | `agents/` | <n> | pending |
| Skills | `skills/` | <n> | pending |
| Hooks | `hooks/` | <yes/no> | pending |

## Review Progress

### Phase 1: Commands
(to be filled during review)

### Phase 2: Agents
(to be filled during review)

### Phase 3: Skills
(to be filled during review)

### Phase 4: Metadata
(to be filled during review)

### Phase 5: Advanced Patterns
(to be filled during review)

## Commits
(to be filled as changes are committed)

## Next Steps
1. [ ] Phase 1: Review commands
2. [ ] Phase 2: Review agents
3. [ ] Phase 3: Review skills
4. [ ] Phase 4: Review metadata
5. [ ] Phase 5: Advanced patterns analysis
6. [ ] Commit changes
7. [ ] Version bump
8. [ ] Push to remote
```

5. Create todo list with all phases
6. Present component inventory to user and proceed to Phase 1

**Output**: State file created, components discovered

---

## Phase 1: Commands Review

**Goal**: Review each command against command-development skill

**Skip if**: Plugin has no commands

**Actions**:

1. Load command-development skill using Skill tool
2. Update state file: `phase: commands-review`
3. For each command file:
   - Read the command file
   - Check against skill criteria:
     - [ ] Has description in frontmatter
     - [ ] Has argument-hint if accepts arguments
     - [ ] Has allowed-tools (principle of least privilege)
     - [ ] Instructions written FOR Claude (not TO user)
     - [ ] Clear workflow structure
   - Document findings in state file
   - If issues found, propose fixes and get user approval
   - Apply approved fixes
4. Update state file with results for each command
5. If changes made, commit with descriptive message and record SHA in state file

**Output**: All commands reviewed, issues fixed, state file updated

---

## Phase 2: Agents Review

**Goal**: Review each agent against agent-development skill

**Skip if**: Plugin has no agents

**Actions**:

1. Load agent-development skill using Skill tool
2. Update state file: `phase: agents-review`
3. For each agent file:
   - Read the agent file
   - Check against skill criteria:
     - [ ] Valid identifier (3-50 chars, lowercase, hyphens)
     - [ ] Description has triggering conditions
     - [ ] Description has 2-4 `<example>` blocks
     - [ ] Examples use two-step assistant response pattern
     - [ ] Examples include proactive triggering (if applicable)
     - [ ] Tools follow least privilege principle
     - [ ] System prompt has: role, responsibilities, process, output format
     - [ ] Edge cases documented
     - [ ] Self-verification steps included
   - Document findings in state file
   - If issues found, propose fixes with proof from skill
   - Get user approval before applying
   - Apply approved fixes
4. Update state file with results for each agent
5. If changes made, commit and record SHA

**Output**: All agents reviewed, issues fixed, state file updated

---

## Phase 3: Skills Review

**Goal**: Review each skill against skill-development skill

**Skip if**: Plugin has no skills

**Actions**:

1. Load skill-development skill using Skill tool
2. Update state file: `phase: skills-review`
3. For each skill:
   - Read SKILL.md
   - Check against skill criteria:
     - [ ] Third-person description ("This skill should be used when...")
     - [ ] Specific trigger phrases in description
     - [ ] Body uses imperative/infinitive form (not "you should")
     - [ ] Content length appropriate (1,500-2,000 words ideal)
     - [ ] Progressive disclosure (detailed content in references/)
     - [ ] References exist and are documented
     - [ ] No dynamic bash patterns in code blocks (GitHub #12781)
   - Document findings in state file
   - Propose fixes with proof from skill
   - Get user approval
   - Apply approved fixes
4. Update state file with results
5. If changes made, commit and record SHA

**Output**: All skills reviewed, issues fixed, state file updated

---

## Phase 4: Metadata Review

**Goal**: Review plugin.json and README against standards

**Actions**:

1. Load plugin-structure skill using Skill tool
2. Update state file: `phase: metadata-review`

**plugin.json check:**
- [ ] Has required field: name
- [ ] Has recommended fields: version, description, author, keywords
- [ ] Name follows kebab-case convention
- [ ] Version follows semver

**README.md check:**
- [ ] Overview section with component list
- [ ] Each command documented with workflow/purpose
- [ ] Each agent documented with capabilities and triggers
- [ ] Each skill documented with triggers and coverage
- [ ] Installation instructions
- [ ] Dependencies section (if applicable)
- [ ] Use cases with practical examples
- [ ] Version, author, license

3. Compare README against plugin-dev/README.md template pattern
4. Document findings in state file
5. Propose fixes and get approval
6. Apply approved fixes
7. If changes made, commit and record SHA

**Output**: Metadata reviewed, README improved, state file updated

---

## Phase 5: Advanced Patterns Analysis

**Goal**: Determine if plugin would benefit from additional patterns

**Actions**:

1. Update state file: `phase: advanced-patterns`

**plugin-settings analysis:**
- Load plugin-settings skill
- Analyze if plugin would benefit from `.local.md` configuration:
  - Does plugin have hooks that need enable/disable toggle?
  - Does agent need state persistence between invocations?
  - Are there project-specific settings that vary?
- Document decision with proof from skill
- If beneficial, recommend implementation

**plugin-structure analysis:**
- Load plugin-structure skill
- Verify structure compliance:
  - [ ] Manifest in `.claude-plugin/plugin.json`
  - [ ] Components at plugin root (not nested)
  - [ ] Kebab-case naming throughout
  - [ ] ${CLAUDE_PLUGIN_ROOT} used where needed
  - [ ] No unnecessary directories
- Document findings

2. Update state file with analysis results
3. If improvements identified, get user approval and implement

**Output**: Advanced patterns analyzed, recommendations documented

---

## Phase 6: Finalization

**Goal**: Commit remaining changes, version bump, push

**Actions**:

1. Update state file: `phase: finalization`
2. Show summary of all changes made:
   - List all commits with SHAs
   - List all issues found and fixed
   - List any skipped items with rationale
3. Ask user: "Ready to finalize? This will:"
   - Commit any uncommitted changes
   - Bump version (patch for improvements, minor for new features)
   - Push to remote
4. If approved:
   - Commit remaining changes
   - Bump version in plugin.json and README
   - Commit version bump
   - Push to remote
5. Update state file:
   - Set `status: complete`
   - Record final version
   - Mark all next steps complete

**Output**: Plugin review complete, changes committed and pushed

---

## State File Maintenance

**Throughout all phases:**

- Update `last_updated` date when making changes
- Update `phase` field when moving between phases
- Record commit SHAs immediately after committing
- Document decisions with rationale
- Track skipped items with explanation

**If resuming a review:**

1. Read existing state file
2. Identify current phase from `phase` field
3. Check `Next Steps` for uncompleted items
4. Resume from last incomplete step
5. Inform user: "Resuming review from Phase X: [phase name]"

---

## Quality Standards

Every recommendation must:

1. **Cite the skill**: Reference specific guidance from plugin-dev skills
2. **Show proof**: Quote relevant text from skill documentation
3. **Explain rationale**: Why this change improves the plugin
4. **Get approval**: Wait for user confirmation before making changes

---

## Begin Review

1. Validate plugin path: $ARGUMENTS
2. If path is empty or invalid, ask user for plugin path
3. Create state file and begin Phase 0: Setup
