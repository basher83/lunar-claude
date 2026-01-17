# ADR Assistant Plugin

Human-in-the-loop Architecture Decision Record workflow for Claude Code.

## Philosophy

AI assists with research, formatting, and enumeration. Humans provide context, make judgments, and own decisions.

## Workflow

1. `/adr-assistant:new [topic]` - Gather context, generate assessment criteria
2. *Refine criteria in conversation*
3. `/adr-assistant:analyze` - Generate options matrix with risk ratings
4. *Refine analysis in conversation*
5. `/adr-assistant:generate [path]` - Output final ADR document

## State Management

Session state persists to `.claude/adr-session.yaml` between commands. This allows:

- Running commands across multiple sessions
- Reviewing/editing criteria before analysis
- Resuming interrupted workflows

## Commands

| Command | Purpose |
|---------|---------|
| `new` | Start ADR - gather context, generate criteria |
| `analyze` | Generate options matrix with risk ratings |
| `generate` | Output final ADR document |

## Skill

The `adr-methodology` skill provides:

- ADR templates (MADR, Nygard, Y-statement)
- Assessment criteria frameworks
- Risk rating definitions

## Installation

Add to your Claude Code plugins or copy to `.claude/plugins/adr-assistant/`.
