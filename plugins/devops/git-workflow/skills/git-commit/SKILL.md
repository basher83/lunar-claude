---
name: git-commit
description: Run hooks and create clean, logical commits via the commit-craft agent.
when_to_use: |
  Trigger when the user has uncommitted changes and either explicitly asks to commit
  ("commit this", "create commits", "let's commit all this") or has just finished a
  feature/refactor that needs to be split into atomic commits. The commit-craft agent
  groups related changes, runs pre-commit hooks, and writes conventional-format messages.

  <example>
  user: "I've finished the authentication module"
  assistant: "I'll use the commit-craft agent to organize these changes into atomic commits."
  </example>
context: fork
agent: git-workflow:commit-craft
---

Create clean, atomic commits for the current workspace changes.
