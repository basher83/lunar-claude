---
description: Create a slash command following skill best practices
argument-hint: [description of what command should do]
allowed-tools: Read, Write, Bash(test:*), AskUserQuestion
---

<!--
COMMAND: create-command
VERSION: 0.1.0
AUTHOR: plugin-dev
LAST UPDATED: 2025-01-18

PURPOSE:
Creates slash commands that comply with command-development skill requirements.
Infers command name and structure from natural language input, asks clarifying
questions only for genuine ambiguities.

USAGE:
  /create-command cmd to review pull requests by number
  /create-command deploy to staging with validation checks
  /create-command                    # Interactive if no context

ARGUMENTS:
  description: Natural language description of what command should do.
               Command name is inferred from purpose (verb-noun, kebab-case).

EXAMPLES:
  /create-command slash cmd that analyzes code for security issues
    → Infers name: analyze-security
    → Creates command with appropriate structure

  /create-command helper to run our standard test suite
    → Infers name: run-tests
    → Asks: location (project/personal/plugin)?

REQUIREMENTS:
  - command-development skill at ${CLAUDE_PLUGIN_ROOT}/skills/command-development/
  - Write access to target commands directory

RELATED COMMANDS:
  /create-agent - Create a new agent
  /create-hook - Create a new hook
  /validate-command - Validate existing command structure

TROUBLESHOOTING:
  - Skill not found: Verify ${CLAUDE_PLUGIN_ROOT}/skills/command-development/ exists
  - Command not appearing: Restart Claude Code, verify .md extension
  - Wrong location: Re-run with explicit location preference

CHANGELOG:
  v0.1.0 (2025-01-18): Initial release with natural language parsing
-->

# Create Slash Command

Guide the user through creating a complete, high-quality Claude Code slash command from initial concept to tested implementation. Follow a systematic approach: understand requirements, design components, clarify details, implement following best practices, validate, and test.

## Core Principles

- **Infer from context**: Parse $ARGUMENTS to understand command purpose. Derive name from purpose (verb-noun pattern, kebab-case).
- **Ask only for genuine gaps**: Do not ask for information already provided or easily inferred. Location and model override are valid clarification points.
- **Load command-development skill**: Use Skill tool to load full skill before implementation. Follow all patterns.
- **Follow best practices**: Apply patterns from the command-development skill's examples and references.
- **Use TodoWrite**: Track progress throughout all phases.
- **Validate output**: Run structural validation on created command.

**Initial request:** $ARGUMENTS

---

<!-- SECTION: PHASE 1 - REQUIREMENTS -->

## Phase 1: Requirements Understanding

**Goal**: Understand what command needs to do from natural language input

**Actions**:

1. Parse $ARGUMENTS to extract:
   - Command purpose (what it should do)
   - Inferred name (derive verb-noun pattern, kebab-case)
   - Any explicit constraints mentioned (tools, model, location)

2. If $ARGUMENTS is empty or too vague to determine purpose, use AskUserQuestion:
   - question: "What should this command do?"
   - header: "Purpose"
   - options: Provide 3-4 common command types relevant to context

3. Summarize understanding:
   - Inferred name: [derived from purpose]
   - Purpose: [what command does]
   - Arguments needed: [if any]
   - Tools required: [if any]

4. Confirm with user before proceeding

**Output**: Clear statement of command purpose and inferred name

---

<!-- SECTION: PHASE 2 - COMPONENT PLANNING -->

## Phase 2: Component Planning

**Goal**: Determine what command components will comprise a complete implementation

**MUST load command-development skill** using Skill tool before this phase.

**Actions**:

1. Load `${CLAUDE_PLUGIN_ROOT}/skills/command-development/SKILL.md`
2. Load relevant references based on command complexity:
   - `references/documentation-patterns.md` (if command needs full documentation)
   - `references/interactive-commands.md` (if command needs user interaction)
   - `examples/plugin-commands.md` (if plugin command)

3. Apply skill requirements to user request from Phase 1 and determine needed components:
   - **Frontmatter fields**: Which additional fields needed? (argument-hint, allowed-tools, model)
   - **Arguments**: Positional ($1, $2) or full ($ARGUMENTS)? Validation needed?
   - **Tools**: What tools does command need? (minimal necessary)
   - **File references**: Any @file patterns needed?
   - **Documentation**: Full block or minimal?
   - **Error handling**: What failure modes to handle?

4. Present component plan to user:

   | Component | Needed | Details |
   |-----------|--------|---------|
   | Frontmatter | Yes | description, argument-hint, allowed-tools |
   | Arguments | Yes/No | [pattern] |
   | Tools | Yes/No | [list] |
   | File refs | Yes/No | [patterns] |
   | Doc block | Full/Minimal | [sections] |
   | Validation | Yes/No | [what to validate] |

5. Get user confirmation or adjustments before proceeding

**Output**: Confirmed component plan ready for implementation

---

<!-- SECTION: PHASE 3 - CLARIFICATION -->

## Phase 3: Clarification (if needed)

**Goal**: Resolve genuine ambiguities only

**Actions**:

1. **Location** (if not clear from context), use AskUserQuestion:
   - question: "Where should this command be installed?"
   - header: "Location"
   - options:
     - Project (.claude/commands/ - shared with team)
     - Personal (~/.claude/commands/ - available everywhere)
     - Plugin (${CLAUDE_PLUGIN_ROOT}/commands/ - bundled with plugin)

2. **Model override** (only if command has specific compute needs), use AskUserQuestion:
   - question: "Does this command need a specific model?"
   - header: "Model"
   - options:
     - Inherit (use conversation's current model)
     - Haiku (fast, simple tasks)
     - Sonnet (standard complexity)
     - Opus (complex analysis)

3. Skip questions where reasonable defaults exist or context makes answer obvious

**Output**: All genuine ambiguities resolved

---

<!-- SECTION: PHASE 4 - IMPLEMENTATION -->

## Phase 4: Implementation

**Goal**: Create Slash Command file following skill patterns

**Actions**:

1. Write frontmatter:
   - description: Clear, actionable, under 60 characters
   - argument-hint: Document expected arguments (if any)
   - allowed-tools: Minimal necessary set (if any)
   - model: Only if override needed

2. Write HTML comment documentation block (from documentation-patterns.md):
   - COMMAND, VERSION, AUTHOR, LAST UPDATED
   - PURPOSE, USAGE, ARGUMENTS, EXAMPLES
   - REQUIREMENTS, TROUBLESHOOTING, CHANGELOG

3. Write command body:
   - Instructions FOR Claude (not messages TO user)
   - Use $1, $2 for positional args, $ARGUMENTS for all
   - Add @file references for file loading
   - Add inline section comments for complex logic

4. Add validation and error handling:
   - Validate arguments if needed
   - Handle missing arguments gracefully
   - Provide helpful error messages

5. Write to determined location

**Output**: Slash Command implemented

---

<!-- SECTION: PHASE 5 - VALIDATION -->

## Phase 5: Validation

**Goal**: Ensure command meets quality standards

**Actions**:

1. Structural validation:

   - Check YAML frontmatter present (starts with `---`)
   - Verify `description` field exists
   - Check `argument-hint` format if present
   - Validate `allowed-tools` is array if present
   - Ensure markdown content exists

2. Quality checklist:
   - [ ] Instructions written FOR Claude (not TO user)
   - [ ] description under 60 characters
   - [ ] argument-hint matches actual usage
   - [ ] allowed-tools is minimal necessary
   - [ ] HTML comment documentation block present
   - [ ] Error handling for missing arguments

3. Generate test matrix for created command:

   | Test Case | Invocation | Expected |
   |-----------|------------|----------|
   | No args | /[name] | [behavior] |
   | Valid args | /[name] [example] | [behavior] |
   | Invalid args | /[name] [bad] | [error message] |

4. If any check fails, fix before presenting

**Output**: Validated command ready for use

---

## Final Output

Present to user:

1. Created command file path
2. Validation results summary
3. Suggested first test invocation: `/[name] [example args]`

---

## Important Notes

### Throughout All Phases

- **Use TodoWrite** to track progress at every phase
- **Load skills with Skill tool** when working on command components
- **Ask for user confirmation** at key decision points
- **Follow command-development skill patterns** as reference
- **Apply best practices**:
  - Commands written FOR Claude (not TO user)
  - description under 60 characters
  - allowed-tools minimal necessary
  - ${CLAUDE_PLUGIN_ROOT} for plugin paths

## Key Decision Points

- After Phase 1: Confirm command purpose and inferred name
- After Phase 2: Confirm component plan before implementation
- After Phase 5: Present completed command with test invocation

---

## Example Workflow

### User Request

"/create-command review PR and check for common issues"

### Phase 1: Requirements Understanding

- Purpose: Review pull requests for code quality issues
- Inferred name: `review-pr`
- Arguments needed: PR number
- Tools required: Bash (gh CLI)

### Phase 2: Component Planning

| Component | Needed | Details |
|-----------|--------|----------|
| Frontmatter | Yes | description, argument-hint, allowed-tools |
| Arguments | Yes | $1 for PR number |
| Tools | Yes | Bash(gh:*), Read |
| File refs | No | — |
| Doc block | Full | All sections |
| Validation | Yes | Check PR number provided |

### Phase 3: Clarification

- Location: Ask user (project vs personal vs plugin)
- Model: Skip (standard complexity, inherit is fine)

### Phase 4: Implementation

- Write frontmatter with description, argument-hint, allowed-tools
- Add HTML comment documentation block
- Write command body: fetch PR, analyze changes, report issues
- Add validation for missing PR number argument

### Phase 5: Validation

- Structural checks pass
- Quality checklist complete
- Test matrix generated

---

**Begin with Phase 1: Requirements Understanding**
