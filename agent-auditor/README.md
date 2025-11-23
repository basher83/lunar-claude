# Agent Auditor

Comprehensive auditing system for Claude Code skills, agents, and components.

## Overview

This repository contains all research, development, and implementation artifacts related to the skill auditor system - a tool for validating Claude Code skills against official Anthropic specifications and ensuring effectiveness for auto-invocation.

## Structure

```text
agent-auditor/
├── docs/                    # Documentation
│   ├── research/            # Research and analysis
│   └── guides/              # User guides
├── src/                     # Source code
│   ├── skill_auditor/       # Python SDK
│   └── tests/              # Test suite
├── agents/                  # Claude Code agent definitions
├── commands/                # Claude Code command definitions
└── MIGRATION.md            # Migration checklist
```

## What's Included

### Research & Documentation

- Architecture decisions and design rationale
- Problem analysis and root cause investigations
- Implementation documentation and plans
- Testing results and validation reports
- Agent evolution history
- Development notes and observations

### Source Code

- Python SDK for deterministic skill auditing
- Metrics extraction and validation logic
- Test suite with comprehensive coverage
- CLI application

See [SDK Reference](docs/api/sdk-reference.md) for detailed usage and API documentation.

### Agent Definitions

- Multiple versions of skill-auditor agents (v3-v6)
- Evolution showing progression from non-deterministic to deterministic approaches

### Commands

- Claude Code commands for skill validation and auditing

## Quick Start

*This is a packaging of content from lunar-claude repository. See MIGRATION.md for next steps to create standalone repository.*

## Key Concepts

- **Deterministic Auditing**: Python-based extraction ensures consistent results across runs
- **Effectiveness Validation**: Checks not just compliance but also auto-invocation potential
- **Progressive Disclosure**: Validates skills follow correct information architecture patterns

## Origin

This content was extracted from the `lunar-claude` repository where it was developed as part of the meta-claude plugin. All original files remain in their original locations - this is a copy for migration purposes.
