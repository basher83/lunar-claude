# Claude Code Plugin Marketplace Engineering & Coding Rules

---

## READ-ONLY FILE

### **If you are an AI coding agent, you must follow these instructions exactly**

- **Never experiment or improvise**
- **Always clarify before acting if unsure**
- **No backwards compatibility; we follow a fix‑forward approach — remove deprecated code immediately**
- **Detailed errors over graceful failures, identify and fix issues fast**
- **Continuous improvement, embrace change and learn from mistakes**
- **KISS, keep it simple**
- **DRY, don't repeat yourself when appropriate**
- **YAGNI, don't implement features that are not needed**
- **Trust but verify, never blindly accept someone elses work without verifying it**

---

## Overview

**lunar-claude** is a personal Claude Code plugin marketplace for homelab and
infrastructure automation. It provides reusable AI-powered tools organized into
a structured plugin ecosystem.

---

## General Engineering Guidelines

- Referance official documentation prior to starting tasks.
- Take inventory of all the tools available to you and utilize them.
- An error is not an obstacle to bypass - it's information telling me you that something is wrong.
- Feeling stuck is not permission to improvise - it's a signal to investigate or ask.

---

## Your Role & Engineering Ethos

- Build for Maintainability, clarity, and explicitness.
- Simplicity and reliability over cleverness.
- Respect existing code and patterns. Audit before adding new code.

---

## Explicit "DO NOT" list

- **Do not add TODOs to code without informing the user**
- **Do not rationalize, trust the workflows**
- **Do not begin a task without verifying if there is a skill for it**
- **Do not skip steps in checklists**

---

## Working with Skills

- **Skills can not contain "anthropic" or "claude" in the name**
- **In skills (SKILL.md)**: Use **relative paths** like`reference.md` or `scripts/helper.py`

---

## Working with Plugins

- **In hooks/MCP servers**: Use `${CLAUDE_PLUGIN_ROOT}path/to/file`
