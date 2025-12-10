---
paths: plugins/**/SKILL.md, plugins/**/skills/**
---

# Skill Development Standards

## SKILL.md Structure

Every skill requires a `SKILL.md` file with:

1. **Title** - Clear, descriptive name
2. **Description** - What the skill provides
3. **Triggers** - Concrete activation conditions
4. **Instructions** - Step-by-step guidance
5. **References** - Links to supporting files

## Skill Directory Layout

```text
skills/<skill-name>/
├── SKILL.md              # Main skill definition (required)
├── references/           # Reference documentation
├── examples/             # Example code/configs
├── patterns/             # Reusable patterns
├── anti-patterns/        # Common mistakes to avoid
├── tools/                # Helper scripts
└── workflows/            # Multi-step procedures
```

## Trigger Patterns

Triggers should be **concrete and actionable**, not vague:

**Good triggers:**
- "When creating a new Ansible role"
- "When configuring Proxmox cloud-init templates"
- "When writing PEP 723 inline script metadata"

**Bad triggers:**
- "When working with infrastructure"
- "When needed"
- "For Python tasks"

## Reference Organization

- Keep references focused and specific
- Use markdown files for documentation
- Include working code examples
- Document anti-patterns explicitly
