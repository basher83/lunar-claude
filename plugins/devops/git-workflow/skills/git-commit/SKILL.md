---
name: git-commit
description: |
  Run hooks and create clean, logical commits

  <example>
  Context: User just finished implementing a feature across multiple files.
  user: "I've finished adding the authentication module"
  assistant: "Great! You have changes across several files."
  <commentary>
  User completed coding task with multiple modified files. Proactively trigger commit-craft to organize changes into clean atomic commits.
  </commentary>
  assistant: "I'll use the commit-craft agent to organize these changes into logical, atomic commits."
  </example>

  <example>
  Context: User explicitly requests commit creation.
  user: "create commits for these changes"
  assistant: "I'll analyze your changes and group them logically."
  <commentary>
  Explicit commit request. Agent will identify related changes and create well-structured commits.
  </commentary>
  assistant: "I'll use the commit-craft agent to create clean, atomic commits following conventional format."
  </example>

  <example>
  Context: User has uncommitted work and wants to commit.
  user: "let's commit all this"
  assistant: "Let me review what's changed first."
  <commentary>
  User wants to commit work. Agent analyzes changes and creates multiple atomic commits rather than one large commit.
  </commentary>
  assistant: "I'll use the commit-craft agent to organize these into logical commits."
  </example>

  <example>
  Context: Large refactoring with many file changes.
  user: "I've refactored the database layer, ready to commit"
  assistant: "That's a significant change set."
  <commentary>
  Large changeset after refactoring. Agent will split into reviewable chunks and group related changes.
  </commentary>
  assistant: "I'll use the commit-craft agent to split this into reviewable, atomic commits."
  </example>
context: fork
agent: git-workflow:commit-craft
---

Create clean, atomic commits for the current workspace changes.
