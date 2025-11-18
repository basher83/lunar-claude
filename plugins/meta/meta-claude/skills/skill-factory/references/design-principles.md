# Design Principles

## 1. Primitives First

Slash commands are the foundation. The skill orchestrates them using the SlashCommand tool. This follows the
multi-agent-composition principle: "Always start with prompts."

### 2. KISS State Management

TodoWrite provides visibility without complexity. No external state files, no databases, no complex checkpointing.
Simple, effective progress tracking.

### 3. Fail Fast

No complex recovery mechanisms. When something can't be auto-fixed or user declines a fix, exit immediately with
clear guidance. Preserves artifacts, provides next steps.

### 4. Context-Aware Entry

Detects workflow path from user's prompt. Explicit research location → Path 1. Ambiguous → Ask user. Natural
language interface.

### 5. Composable & Testable

Every primitive works standalone (power users) or orchestrated (guided users). Each command is independently
testable and verifiable.

### 6. Quality Gates

Sequential dependencies ensure quality: content before compliance, runtime before integration. Tiered validation
with non-blocking audit for comprehensive feedback.
