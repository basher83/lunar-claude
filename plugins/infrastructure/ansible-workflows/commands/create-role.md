---
description: Scaffold a new Ansible role with standard directory structure
argument-hint: <role-name>
allowed-tools: ["Write", "Bash", "Read"]
model: sonnet
---

Create an Ansible role named `$ARGUMENTS` following production patterns.

Load the `ansible-role-design` and `ansible-fundamentals` skills first.

If no role name provided, ask for one.

**Role location:** `ansible/roles/$ARGUMENTS/`

**Create this structure:**

```text
ansible/roles/$ARGUMENTS/
├── defaults/main.yml
├── tasks/main.yml
├── handlers/main.yml
├── meta/main.yml
└── README.md
```

**Variable prefix:** Convert role name to snake_case (e.g., `docker-host` → `docker_host_*`)

**defaults/main.yml:** Role-prefixed variables with defaults
**tasks/main.yml:** Main task router with validation
**handlers/main.yml:** Service restart handlers (if applicable)
**meta/main.yml:** Galaxy metadata with platform support
**README.md:** Usage documentation

**After scaffolding, initialize the pipeline:**

1. Create the `.claude/` directory if it doesn't exist:
   ```bash
   mkdir -p "$CLAUDE_PROJECT_DIR/.claude"
   ```

2. Ensure `.gitignore` contains ansible-workflows patterns (append if missing):
```text
# Ansible Workflows plugin state (auto-added)
.claude/ansible-workflows.local.md
.claude/ansible-workflows.*.bundle.md
```

3. Write state file `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.local.md`:
```yaml
---
active: true
pipeline_phase: generating
target_path: ansible/roles/$ARGUMENTS/
current_agent: ansible-generator
started_at: "[ISO timestamp]"
validation_attempts: 0
last_validation_passed: true
---

# Ansible Workflows Pipeline

Target: ansible/roles/$ARGUMENTS/
Type: role
```

4. Write scaffolding bundle `$CLAUDE_PROJECT_DIR/.claude/ansible-workflows.scaffolding.bundle.md`:
```yaml
---
source_agent: create-role
target_agent: ansible-generator
timestamp: "[ISO timestamp]"
target_path: ansible/roles/$ARGUMENTS/
target_type: role
---

# Scaffolding Bundle

## Target Path
ansible/roles/$ARGUMENTS/

## User Requirements
[Capture any user-specified requirements or context]

## Files Created
- ansible/roles/$ARGUMENTS/defaults/main.yml
- ansible/roles/$ARGUMENTS/tasks/main.yml
- ansible/roles/$ARGUMENTS/handlers/main.yml
- ansible/roles/$ARGUMENTS/meta/main.yml
- ansible/roles/$ARGUMENTS/README.md

## Variable Prefix
[snake_case version of role name]

## Next Steps
Implement the role tasks based on user requirements.
```

5. Hand off to `ansible-generator` agent with the role path

Report: role path, files created, variable prefix, pipeline initialized.
