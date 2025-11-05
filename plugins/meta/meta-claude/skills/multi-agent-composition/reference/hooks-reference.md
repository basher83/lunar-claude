# Claude Code Hooks Reference

**Lifecycle hooks for observability and control** - Execute commands at specific points in Claude Code's execution.

## Table of Contents

- [Overview](#overview)
- [The Nine Lifecycle Hooks](#the-nine-lifecycle-hooks)
  - [1. pre-tool-use](#1-pre-tool-use)
  - [2. post-tool-use](#2-post-tool-use)
  - [3. notification](#3-notification)
  - [4. stop](#4-stop)
  - [5. sub-agent-stop](#5-sub-agent-stop)
  - [6. user-prompt-submit](#6-user-prompt-submit)
  - [7. pre-compact](#7-pre-compact)
  - [8. session-start](#8-session-start)
  - [9. session-end](#9-session-end)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [The Two Killer Use Cases](#the-two-killer-use-cases)
- [Philosophy](#philosophy)
- [Next Steps](#next-steps)

## Overview

Hooks enable you to:
- **Control** what Claude Code can do (block dangerous commands)
- **Observe** what Claude Code is doing (log all tool usage)
- **Automate** responses to lifecycle events (notifications, cleanup)

> "Hooks are great. This is deterministic automation that executes commands at specific lifecycle events. This is where we add determinism rather than always relying on the agent to decide."

## The Nine Lifecycle Hooks

### 1. pre-tool-use

**When it fires:** Before any tool runs

**Purpose:** Control / blocking

**Use cases:**
- Block dangerous commands (rm -rf, etc.)
- Prevent access to sensitive files (.env, credentials)
- Validate tool inputs before execution
- Add safety checks

**Input data provided:**
```json
{
  "tool_name": "bash",
  "tool_input": {
    "command": "rm -rf /important/data"
  }
}
```

**How to block:** Return non-zero exit code from your hook script

**Example:**
```python
# .claude/hooks/pre-tool-use.py
import sys
import json

data = json.loads(sys.stdin.read())

if data['tool_name'] == 'bash':
    command = data['tool_input'].get('command', '')
    if 'rm -rf' in command:
        print("❌ Blocked dangerous command")
        sys.exit(1)  # Non-zero = block

sys.exit(0)  # Zero = allow
```

---

### 2. post-tool-use

**When it fires:** After a tool runs

**Purpose:** Observability / logging

**Use cases:**
- Log all tool usage
- Track which files are read/written
- Monitor API calls and costs
- Record tool outputs for analysis

**Input data provided:**
```json
{
  "tool_name": "bash",
  "tool_input": {
    "command": "ls -la"
  },
  "tool_output": "[command output here]",
  "success": true
}
```

**Cannot block:** Tool already executed

**Example:**
```python
# .claude/hooks/post-tool-use.py
import sys
import json
from pathlib import Path

data = json.loads(sys.stdin.read())

# Log to file
log_file = Path(".claude/logs/post-tool-use.json")
logs = json.loads(log_file.read_text()) if log_file.exists() else []
logs.append(data)
log_file.write_text(json.dumps(logs, indent=2))
```

---

### 3. notification

**When it fires:** When Claude Code needs user input

**Purpose:** Awareness / automation

**Use cases:**
- Get notified when permission is needed
- Trigger external notifications (phone, Slack)
- Automate permission responses (careful!)
- Track permission requests

**Input data provided:**
```json
{
  "type": "permission_request",
  "tool_name": "bash",
  "message": "Your agent needs your input"
}
```

**Example:**
```python
# .claude/hooks/notification.py
import sys
import json

data = json.loads(sys.stdin.read())

# Send notification
import subprocess
subprocess.run([
    "osascript", "-e",
    f'display notification "{data["message"]}" with title "Claude Code"'
])
```

---

### 4. stop

**When it fires:** Every time Claude Code finishes responding

**Purpose:** Observability / completion tracking

**Use cases:**
- Capture full chat transcript
- Announce completion (text-to-speech)
- Trigger next steps in workflow
- Save conversation state

**Input data provided:**
```json
{
  "transcript_path": "/path/to/chat.jsonl",
  "session_id": "abc123",
  "messages_count": 42
}
```

**Critical for observability:** This is when you capture the full conversation

**Example:**
```python
# .claude/hooks/stop.py
import sys
import json
import shutil
from pathlib import Path

data = json.loads(sys.stdin.read())

# Copy full transcript to logs
transcript = Path(data['transcript_path'])
if transcript.exists():
    log_dir = Path(".claude/logs")
    log_dir.mkdir(exist_ok=True)
    shutil.copy(transcript, log_dir / "chat.json")

# Announce completion (text-to-speech)
import subprocess
subprocess.run([
    "say", "All set and ready for your next step"
])
```

---

### 5. sub-agent-stop

**When it fires:** When a sub-agent completes

**Purpose:** Track parallel agent completion

**Use cases:**
- Monitor multi-agent workflows
- Track which agents finished
- Announce sub-agent completion
- Aggregate sub-agent results

**Input data provided:**
```json
{
  "agent_id": "sub-agent-123",
  "agent_name": "code-analyzer",
  "status": "completed",
  "transcript_path": "/path/to/sub-agent-transcript.jsonl"
}
```

**Example:**
```python
# .claude/hooks/sub-agent-stop.py
import sys
import json

data = json.loads(sys.stdin.read())

# Log sub-agent completion
agent_name = data.get('agent_name', 'unknown')
print(f"✅ Sub-agent '{agent_name}' completed")

# Announce
import subprocess
subprocess.run([
    "say", f"Sub agent {agent_name} complete"
])
```

---

### 6. user-prompt-submit

**When it fires:** When the user submits a prompt, before Claude processes it

**Purpose:** Prompt validation / context injection

**Use cases:**
- Add context based on the prompt (timestamps, environment info)
- Validate prompts for sensitive information
- Block certain types of prompts
- Transform user input before processing

**Input data provided:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/chat.jsonl",
  "prompt": "Write a function to calculate factorial"
}
```

**Special behavior:** Hook stdout is added as context for Claude

**Example:**
```python
# .claude/hooks/user-prompt-submit.py
import sys
import json
from datetime import datetime

data = json.loads(sys.stdin.read())

# Add timestamp context
print(f"Current time: {datetime.now().isoformat()}")

# Check for sensitive patterns
if any(word in data['prompt'].lower() for word in ['password', 'secret', 'key']):
    print("⚠️ Warning: Prompt may contain sensitive information", file=sys.stderr)
    sys.exit(2)  # Block prompt processing

sys.exit(0)
```

---

### 7. pre-compact

**When it fires:** Before Claude Code runs a compact operation

**Purpose:** Awareness / pre-compaction actions

**Use cases:**
- Save current state before compaction
- Log compaction triggers
- Prepare context for post-compact state
- Track auto-compact frequency

**Input data provided:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/chat.jsonl",
  "trigger": "manual",  // or "auto"
  "custom_instructions": ""
}
```

**Matchers:**
- `manual` - User ran `/compact`
- `auto` - Triggered by full context window

**Example:**
```python
# .claude/hooks/pre-compact.py
import sys
import json
from pathlib import Path
import shutil
from datetime import datetime

data = json.loads(sys.stdin.read())

# Save transcript before compaction
if data['trigger'] == 'auto':
    print(f"🔄 Auto-compact triggered at {datetime.now()}")

    # Backup transcript
    transcript = Path(data['transcript_path'])
    if transcript.exists():
        backup_dir = Path(".claude/backups")
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(transcript, backup_dir / f"pre-compact-{timestamp}.jsonl")

sys.exit(0)
```

---

### 8. session-start

**When it fires:** When Claude Code starts a new session or resumes

**Purpose:** Context loading / environment setup

**Use cases:**
- Load development context (recent changes, open issues)
- Set environment variables
- Install dependencies
- Initialize project state

**Input data provided:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/chat.jsonl",
  "source": "startup"  // or "resume", "clear", "compact"
}
```

**Matchers:**
- `startup` - Fresh session start
- `resume` - Resumed with `--resume`, `--continue`, or `/resume`
- `clear` - After `/clear`
- `compact` - After auto or manual compact

**Special feature:** Can persist environment variables via `CLAUDE_ENV_FILE`

**Example:**
```python
# .claude/hooks/session-start.py
import sys
import json
import os
from pathlib import Path

data = json.loads(sys.stdin.read())

# Load project context
if data['source'] == 'startup':
    print("🚀 Session started - loading project context...")

    # Persist environment variables
    if env_file := os.getenv('CLAUDE_ENV_FILE'):
        with open(env_file, 'a') as f:
            f.write('export NODE_ENV=development\n')
            f.write('export DEBUG=true\n')

    # Output context for Claude
    recent_commits = "Recent commits: [TODO: fetch from git]"
    open_issues = "Open issues: [TODO: fetch from issue tracker]"
    print(f"{recent_commits}\n{open_issues}")

sys.exit(0)
```

---

### 9. session-end

**When it fires:** When Claude Code session ends

**Purpose:** Cleanup / session logging

**Use cases:**
- Save session statistics
- Clean up temporary files
- Archive transcripts
- Log session duration

**Input data provided:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/chat.jsonl",
  "reason": "exit"  // or "clear", "logout", "prompt_input_exit", "other"
}
```

**Cannot block:** Session ends regardless

**Example:**
```python
# .claude/hooks/session-end.py
import sys
import json
from pathlib import Path
from datetime import datetime

data = json.loads(sys.stdin.read())

# Log session end
log_file = Path(".claude/logs/sessions.jsonl")
log_file.parent.mkdir(exist_ok=True)

log_entry = {
    "timestamp": datetime.now().isoformat(),
    "session_id": data['session_id'],
    "reason": data['reason']
}

with open(log_file, 'a') as f:
    f.write(json.dumps(log_entry) + '\n')

print(f"📊 Session logged: {data['reason']}")
```

---

## Configuration

Hooks are configured in settings.json:

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "matcher": {},  // Empty = always run
        "commands": ["uv run .claude/hooks/pre-tool-use.py"]
      }
    ],
    "post-tool-use": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/post-tool-use.py"]
      }
    ],
    "notification": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/notification.py"]
      }
    ],
    "stop": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/stop.py"]
      }
    ],
    "sub-agent-stop": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/sub-agent-stop.py"]
      }
    ],
    "user-prompt-submit": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/user-prompt-submit.py"]
      }
    ],
    "pre-compact": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/pre-compact.py"]
      }
    ],
    "session-start": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/session-start.py"]
      }
    ],
    "session-end": [
      {
        "matcher": {},
        "commands": ["uv run .claude/hooks/session-end.py"]
      }
    ]
  }
}
```

**Key points:**
- Hooks are **arrays** - can have multiple matchers/commands
- **Matchers** filter when hook runs (empty = always)
- **Commands** can be Python, TypeScript (bun), or shell scripts
- Commands receive data via **stdin**
- pre-tool-use can **block** by returning non-zero exit code

## Best Practices

### 1. Use Isolated Single-File Scripts

**Recommended:** Astral UV single-file Python scripts

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

import sys
import json

data = json.loads(sys.stdin.read())
# Your logic here
```

**Benefits:**
- No external codebase dependencies
- Self-contained with inline dependencies
- Easy to test standalone
- Works with any Python version

**Alternatives:** TypeScript with bun, shell scripts

### 2. Organize in Dedicated Directory

```text
.claude/
└── hooks/
    ├── pre-tool-use.py
    ├── post-tool-use.py
    ├── notification.py
    ├── stop.py
    ├── sub-agent-stop.py
    └── utils/
        ├── tts.py           # Text-to-speech utilities
        ├── logging.py       # Shared logging functions
        └── validation.py    # Shared validation logic
```

### 3. Protect Your Context

Don't let hooks consume Claude's context:
- Keep hook scripts **separate** from main codebase
- Don't require hooks to read large files
- Use efficient data structures (JSON, not text dumps)

### 4. Essential Hooks to Implement

**Minimum viable observability:**
1. **post-tool-use** - Log all tool usage
2. **stop** - Capture full chat transcript

**Bonus for safety:**
3. **pre-tool-use** - Block dangerous commands

**Bonus for UX:**
4. **stop** - Text-to-speech completion announcement
5. **sub-agent-stop** - Track multi-agent workflows

## Common Patterns

### Pattern 1: Block Dangerous Commands

```python
DANGEROUS_PATTERNS = ['rm -rf', 'sudo rm', 'dd if=', 'mkfs']

def is_dangerous_command(command):
    return any(pattern in command for pattern in DANGEROUS_PATTERNS)

if is_dangerous_command(data['tool_input'].get('command', '')):
    print("❌ Command blocked")
    sys.exit(1)
```

### Pattern 2: Block Environment File Access

```python
def is_env_file_access(tool_name, tool_input):
    if tool_name in ['Read', 'read', 'cat']:
        file_path = tool_input.get('file_path', '')
        return '.env' in file_path
    return False

if is_env_file_access(data['tool_name'], data['tool_input']):
    print("❌ Environment file access blocked")
    sys.exit(1)
```

### Pattern 3: Comprehensive Logging

```python
import json
from pathlib import Path
from datetime import datetime

def log_tool_use(data):
    log_dir = Path(".claude/logs")
    log_dir.mkdir(exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": data['tool_name'],
        "tool_input": data['tool_input'],
        "tool_output": data.get('tool_output'),
        "success": data.get('success')
    }

    log_file = log_dir / "post-tool-use.jsonl"
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

log_tool_use(data)
```

### Pattern 4: Text-to-Speech Completion

```python
def announce_completion(message="All set and ready for your next step"):
    import subprocess

    # macOS
    subprocess.run(["say", message])

    # Or use TTS service (11Labs, OpenAI TTS, etc.)
    # ... call API here

announce_completion()
```

## The Two Killer Use Cases

### 1. Observability

> "When it comes to agentic coding, observability is everything. If you can't measure it, you can't improve it."

**What to observe:**
- All tool calls (post-tool-use)
- Full chat transcripts (stop)
- Agent completions (sub-agent-stop)
- Permission requests (notification)

**Why it matters:**
- Understand what your agents are doing
- Debug issues faster
- Improve prompts based on data
- Track costs and performance
- Scale with confidence

### 2. Control

**What to control:**
- Block dangerous operations (pre-tool-use)
- Prevent sensitive file access (pre-tool-use)
- Validate inputs before execution (pre-tool-use)

**Why it matters:**
- Safety in YOLO mode
- Protect production systems
- Compliance requirements
- Peace of mind

## Philosophy

> "If you really want to scale, you need both agents AND deterministic workflows."

Hooks balance:
- **Agent autonomy** (let Claude decide)
- **Deterministic control** (enforce rules)

The best agentic systems use both.

## Next Steps

For implementation patterns and examples, see [patterns/hooks-observability.md](../patterns/hooks-observability.md)
