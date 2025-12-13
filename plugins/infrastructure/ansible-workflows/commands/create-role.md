---
description: Scaffold a new Ansible role with standard directory structure
argument-hint: <role-name>
allowed-tools: Write, Bash, Read
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

After scaffolding, hand off to `ansible-generator` agent with the role path to implement tasks.

Report: role path, files created, variable prefix, next steps.
