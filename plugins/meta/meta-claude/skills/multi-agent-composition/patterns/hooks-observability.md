# Hooks for Observability and Control

> "When it comes to agentic coding, observability is everything. How well you can observe, iterate, and improve your agentic system is going to be a massive differentiating factor."

Claude Code hooks provide deterministic control over agent behavior and enable comprehensive monitoring of multi-agent systems.

## What Are Hooks?

**Hooks are lifecycle event handlers that let you execute custom code at specific points in Claude Code's execution.**

```text
Agent Lifecycle:
├── pre-tool-use hook → Before any tool executes
├── [Tool executes]
├── post-tool-use hook → After tool completes
├── notification hook → When agent needs input
├── sub-agent-stop hook → When sub-agent finishes
└── stop hook → When agent completes response
```

**Two killer use cases:**

1. **Observability** - Know what your agents are doing
2. **Control** - Steer and block agent behavior

## The Five Hooks

### 1. pre-tool-use

**When it fires:** Before any tool executes

**Use cases:**

- Block dangerous commands (`rm -rf`, destructive operations)
- Prevent access to sensitive files (`.env`, `credentials.json`)
- Log tool attempts before execution
- Validate tool parameters

**Available data:**

```json
{
  "toolName": "bash",
  "toolInput": {
    "command": "rm -rf /",
    "description": "Remove all files"
  }
}
```

**Example: Block dangerous commands**

```python
# .claude/hooks/pre-tool-use.py
# /// script
# dependencies = []
# ///

import sys
import json
import re

def is_dangerous_remove_command(tool_name, tool_input):
    """Block any rm -rf commands"""
    if tool_name != "bash":
        return False

    command = tool_input.get("command", "")
    dangerous_patterns = [
        r'\brm\s+-rf\b',
        r'\brm\s+-fr\b',
        r'\brm\s+.*-[rf].*\*',
    ]

    return any(re.search(pattern, command) for pattern in dangerous_patterns)

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("toolName")
    tool_input = input_data.get("toolInput", {})

    if is_dangerous_remove_command(tool_name, tool_input):
        # Block the command
        output = {
            "allow": False,
            "message": "❌ Blocked dangerous rm command"
        }
    else:
        output = {"allow": True}

    print(json.dumps(output))

if __name__ == "__main__":
    main()
```

**Configuration in settings.json:**

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "matcher": {},  // Empty = matches all tools
        "commands": [
          "uv run .claude/hooks/pre-tool-use.py"
        ]
      }
    ]
  }
}
```

### 2. post-tool-use

**When it fires:** After a tool completes execution

**Use cases:**

- Log tool execution results
- Track which tools are used most frequently
- Measure tool execution time
- Build observability dashboards
- Summarize tool output with small models

**Available data:**

```json
{
  "toolName": "write",
  "toolInput": {
    "file_path": "/path/to/file.py",
    "content": "..."
  },
  "toolResult": {
    "success": true,
    "output": "File written successfully"
  }
}
```

**Example: Event logging with summarization**

```python
# .claude/hooks/post-tool-use.py
import sys
import json
import os
from anthropic import Anthropic

def summarize_event(tool_name, tool_input, tool_result):
    """Use Haiku to summarize what happened"""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Summarize this tool execution in 1 sentence:
Tool: {tool_name}
Input: {json.dumps(tool_input, indent=2)}
Result: {json.dumps(tool_result, indent=2)}

Be concise and focus on what was accomplished."""

    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Small, fast, cheap
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def main():
    input_data = json.load(sys.stdin)

    # Generate summary using small model
    summary = summarize_event(
        input_data.get("toolName"),
        input_data.get("toolInput", {}),
        input_data.get("toolResult", {})
    )

    # Log the event with summary
    event = {
        "toolName": input_data["toolName"],
        "summary": summary,
        "timestamp": input_data.get("timestamp")
    }

    # Send to observability server
    send_to_server(event)

if __name__ == "__main__":
    main()
```

**Why small models?** "I've sent thousands of these events. I've spent less than 20 cents. This is where small fast models really shine."

### 3. notification

**When it fires:** When Claude Code needs user input (permission request)

**Use cases:**

- Text-to-speech notifications
- Send alerts to phone/Slack
- Log permission requests
- Auto-approve specific tools

**Available data:**

```json
{
  "message": "Your agent needs your input",
  "context": {
    "toolName": "bash",
    "command": "bun run apps/hello.ts"
  }
}
```

**Example: Text-to-speech notification**

```python
# .claude/hooks/notification.py
import sys
import json
import subprocess

def speak(text):
    """Use 11Labs API for text-to-speech"""
    subprocess.run([
        "uv", "run",
        ".claude/hooks/utils/text-to-speech-elevenlabs.py",
        text
    ])

def main():
    input_data = json.load(sys.stdin)
    message = input_data.get("message", "Your agent needs your input")

    # Speak the notification
    speak(message)

    # Log it
    print(json.dumps({"notified": True}))

if __name__ == "__main__":
    main()
```

### 4. stop

**When it fires:** Every time Claude Code finishes responding

**Use cases:**

- Copy full chat transcript for analysis
- Completion notifications (text-to-speech)
- Session logging
- Performance metrics
- Agent output summarization

**Available data:**

```json
{
  "transcriptPath": "/path/to/chat-transcript.json",
  "sessionId": "abc123",
  "timestamp": "2025-01-05T14:30:00Z"
}
```

**Example: Save full conversation**

```python
# .claude/hooks/stop.py
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

def main():
    input_data = json.load(sys.stdin)
    transcript_path = input_data.get("transcriptPath")

    if not transcript_path:
        return

    # Copy transcript to logs directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    session_id = input_data.get("sessionId", "unknown")

    logs_dir = Path(".claude/logs")
    logs_dir.mkdir(exist_ok=True)

    dest = logs_dir / f"chat-{timestamp}-{session_id[:8]}.json"
    shutil.copy(transcript_path, dest)

    # Announce completion
    subprocess.run([
        "uv", "run",
        ".claude/hooks/utils/text-to-speech.py",
        "All set and ready for your next step"
    ])

    print(json.dumps({"logged": True, "file": str(dest)}))

if __name__ == "__main__":
    main()
```

**Key insight:** "The stop event is the perfect time to copy the entire chat conversation. This is key for observability. What happened? How can we improve it?"

### 5. sub-agent-stop

**When it fires:** When a sub-agent completes its work

**Use cases:**

- Track parallel sub-agent completion
- Per-agent performance metrics
- Multi-agent orchestration logging
- Progress notifications for long-running jobs

**Available data:**

```json
{
  "subAgentId": "agent-123",
  "transcriptPath": "/path/to/sub-agent-transcript.json",
  "sessionId": "parent-abc123",
  "timestamp": "2025-01-05T14:32:00Z"
}
```

**Example: Sub-agent completion tracking**

```python
# .claude/hooks/sub-agent-stop.py
import sys
import json

def main():
    input_data = json.load(sys.stdin)

    # Log sub-agent completion
    event = {
        "type": "sub-agent-complete",
        "agentId": input_data.get("subAgentId"),
        "timestamp": input_data.get("timestamp")
    }

    # Send to observability system
    send_event(event)

    # Announce
    speak("Sub agent complete")

if __name__ == "__main__":
    main()
```

## Multi-Agent Observability Architecture

When scaling to 3, 5, 10+ agents, hooks enable comprehensive system visibility.

### Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     Multiple Agents                          │
│  Agent 1    Agent 2    Agent 3    ...    Agent N            │
│    │          │          │                  │                │
│    └──────────┴──────────┴──────────────────┘                │
│                        │                                      │
│                   Hooks fire                                  │
│                        ↓                                      │
└─────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   Bun/Node Server                            │
│  ┌────────────────┐         ┌──────────────┐               │
│  │  HTTP Endpoint │────────→│   SQLite DB  │               │
│  │  /events       │         │  (persistence)│               │
│  └────────────────┘         └──────────────┘               │
│         │                                                     │
│         └────────────→ WebSocket Broadcast                   │
└─────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  Web Client (Vue/React)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Live Activity Pulse (1min/3min/5min windows)        │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Event Stream (filtered by app/session/event type)   │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Event Details (with AI summaries)                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

**1. One-Way Data Stream**

```text
Agent → Hook → Server → Database + WebSocket → Client
```

"This one-way data stream keeps things really simple. Every agent is responsible for summarizing their work in the hook before they send it off."

**Benefits:**

- Simple architecture
- Easy to reason about
- No bidirectional complexity
- Fast real-time updates

**2. Event Summarization at the Edge**

```python
# In the hook (runs on agent side)
def send_event(app_name, event_type, event_data, summarize=True):
    if summarize:
        # Use Haiku to summarize before sending
        summary = summarize_with_haiku(event_data)
        event_data["summary"] = summary

    # Send to server
    requests.post("http://localhost:3000/events", json={
        "app": app_name,
        "type": event_type,
        "data": event_data,
        "sessionId": os.getenv("CLAUDE_SESSION_ID")
    })
```

**Why summarize at the edge?**

- Reduces server load
- Cheaper (uses small models locally)
- Human-readable summaries immediately available
- No server-side LLM dependencies

**3. Persistent + Real-Time Storage**

```sql
-- SQLite schema
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    source_app TEXT NOT NULL,
    session_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    raw_payload JSON,
    summary TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Dual persistence:**

- SQLite for historical queries and analysis
- WebSocket for live streaming to UI

### Implementation Example

**Hook script structure:**

```python
# .claude/hooks/utils/send-event.py
# /// script
# dependencies = ["anthropic", "requests"]
# ///

import sys
import json
import os
import requests
from anthropic import Anthropic

def summarize_with_haiku(event_data, event_type):
    """Generate 1-sentence summary using Haiku"""
    if event_type not in ["pre-tool-use", "post-tool-use"]:
        return None

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"Summarize this {event_type} event in 1 sentence: {json.dumps(event_data)}"

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

def send_event(app_name, event_type, event_data, summarize=False):
    """Send event to observability server"""

    payload = {
        "app": app_name,
        "sessionId": os.getenv("CLAUDE_SESSION_ID", "unknown"),
        "eventType": event_type,
        "data": event_data,
        "timestamp": event_data.get("timestamp")
    }

    if summarize:
        payload["summary"] = summarize_with_haiku(event_data, event_type)

    try:
        response = requests.post(
            "http://localhost:3000/events",
            json=payload,
            timeout=1
        )
        return response.status_code == 200
    except Exception as e:
        # Don't break agent if observability fails
        print(f"Warning: Failed to send event: {e}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: send-event.py <app-name> <event-type> [--summarize]")
        sys.exit(1)

    app_name = sys.argv[1]
    event_type = sys.argv[2]
    summarize = "--summarize" in sys.argv

    # Read event data from stdin
    event_data = json.load(sys.stdin)

    success = send_event(app_name, event_type, event_data, summarize)
    print(json.dumps({"sent": success}))

if __name__ == "__main__":
    main()
```

**Using in hooks:**

```python
# .claude/hooks/post-tool-use.py
import sys
import json
import subprocess

def main():
    input_data = json.load(sys.stdin)

    # Send to observability system with summarization
    subprocess.run([
        "uv", "run",
        ".claude/hooks/utils/send-event.py",
        "my-app",  # App name
        "post-tool-use",  # Event type
        "--summarize"  # Generate AI summary
    ], input=json.dumps(input_data), text=True)

    print(json.dumps({"logged": True}))

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Use Isolated Scripts (Astral UV Pattern)

**Why:** Hooks should be self-contained, portable, and not depend on your codebase.

```python
# /// script
# dependencies = ["anthropic", "requests"]
# ///

# Astral UV single-file script
# Runs independently with: uv run script.py
# Auto-installs dependencies
```

**Benefits:**

- Works in any codebase
- No virtual environment setup
- Portable across projects
- Easy to test in isolation

**Alternative: Bun for TypeScript**

```typescript
// .claude/hooks/post-tool-use.ts
// Run with: bun run post-tool-use.ts

import { readSync } from "fs";

const input = JSON.parse(readSync(0, "utf-8"));
// ... hook logic
```

### 2. Never Block the Agent

```python
def main():
    try:
        # Hook logic
        send_to_server(event)
    except Exception as e:
        # Log but don't fail
        print(f"Warning: {e}", file=sys.stderr)
        # Always output valid JSON
        print(json.dumps({"error": str(e)}))
```

**Rule:** If observability fails, the agent should continue working.

### 3. Use Small Fast Models for Summaries

```text
Cost comparison (1,000 events):
├── Opus: $15 (overkill for summaries)
├── Sonnet: $3 (still expensive)
└── Haiku: $0.20 ✅ (perfect for this)
```

"Thousands of events, less than 20 cents. Small fast cheap models shine here."

### 4. Hash Session IDs for UI Consistency

```python
import hashlib

def color_for_session(session_id):
    """Generate consistent color from session ID"""
    hash_val = int(hashlib.md5(session_id.encode()).hexdigest()[:6], 16)
    return f"#{hash_val:06x}"
```

**Result:** Same agent = same color in UI, making it easy to track.

### 5. Filter and Paginate Events

```javascript
// Client-side filtering
const filteredEvents = events
  .filter(e => e.app === selectedApp || selectedApp === "all")
  .filter(e => e.eventType === selectedType || selectedType === "all")
  .slice(0, 100); // Limit displayed events

// Auto-refresh
setInterval(() => fetchLatestEvents(), 5000);
```

### 6. Multiple Hooks Per Event

```json
{
  "hooks": {
    "stop": [
      {
        "matcher": {},
        "commands": [
          "uv run .claude/hooks/stop-chat-log.py",
          "uv run .claude/hooks/stop-tts.py",
          "uv run .claude/hooks/stop-notify.py"
        ]
      }
    ]
  }
}
```

**Hooks run sequentially** in the order specified.

### 7. Matcher Patterns for Selective Execution

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "matcher": {
          "toolName": "bash"
        },
        "commands": ["uv run .claude/hooks/bash-validator.py"]
      },
      {
        "matcher": {
          "toolName": "write",
          "toolInput": {
            "file_path": "**/.env"
          }
        },
        "commands": ["uv run .claude/hooks/block-env-write.py"]
      }
    ]
  }
}
```

## Directory Structure Best Practice

```text
.claude/
├── commands/           # Slash commands
├── agents/             # Sub-agent definitions
└── hooks/              # ← New essential directory
    ├── settings.json   # Hook configuration
    ├── pre-tool-use.py
    ├── post-tool-use.py
    ├── notification.py
    ├── stop.py
    ├── sub-agent-stop.py
    └── utils/          # Shared utilities
        ├── send-event.py
        ├── text-to-speech-elevenlabs.py
        ├── text-to-speech-openai.py
        └── summarize-haiku.py
```

## Real-World Use Cases

### Use Case 1: Block Dangerous Operations

```python
# .claude/hooks/pre-tool-use.py

BLOCKED_COMMANDS = [
    r'\brm\s+-rf\b',      # rm -rf
    r'\bsudo\s+rm\b',     # sudo rm
    r'\bgit\s+push.*--force\b',  # git push --force
    r'\bdocker\s+system\s+prune\b',  # docker system prune
]

BLOCKED_FILES = [
    r'\.env$',
    r'credentials\.json$',
    r'\.ssh/id_rsa$',
    r'aws.*credentials',
]

def is_blocked(tool_name, tool_input):
    if tool_name == "bash":
        command = tool_input.get("command", "")
        return any(re.search(p, command) for p in BLOCKED_COMMANDS)

    if tool_name in ["read", "write", "edit"]:
        file_path = tool_input.get("file_path", "")
        return any(re.search(p, file_path) for p in BLOCKED_FILES)

    return False
```

### Use Case 2: Multi-Agent Task Board

```text
Observability UI showing:

Active Agents (5):
├── [Agent 1] Planning feature (12s ago)
├── [Agent 2] Writing tests (45s ago) ⚠️ Needs input
├── [Agent 3] Building UI (2m ago)
├── [Agent 4] Deploying (5m ago) ✅ Complete
└── [Agent 5] Monitoring (ongoing)

Recent Events (filtered: post-tool-use):
├── Agent 3: Wrote src/components/Button.tsx
├── Agent 1: Read src/api/endpoints.ts
├── Agent 4: Bash: git push origin main
└── Agent 2: Test failed: test/auth.test.ts
```

### Use Case 3: Long-Running AFK Agents

```bash
# Start agent with background work
/background "Implement entire auth system" --report agents/auth-report.md

# Agent works autonomously
# Hooks send notifications:
# - "Starting authentication module"
# - "Database schema created"
# - "Tests passing"
# - "All set and ready for your next step"

# You're notified via text-to-speech when complete
```

### Use Case 4: Debugging Agent Behavior

```python
# Filter stop events to analyze full chat transcripts

for event in events.filter(type="stop"):
    transcript = json.load(open(event.transcriptPath))

    # Analyze:
    # - What files did agent read?
    # - What tools were used most?
    # - Where did agent get confused?
    # - What patterns led to errors?
```

## Performance Considerations

### Webhook Timeouts

```python
# Don't block agent on slow external services
try:
    requests.post(webhook_url, json=event, timeout=0.5)  # 500ms max
except requests.Timeout:
    # Log locally instead
    log_to_file(event)
```

### Database Size Management

```sql
-- Rotate old events
DELETE FROM events
WHERE timestamp < datetime('now', '-30 days');

-- Or archive
INSERT INTO events_archive SELECT * FROM events
WHERE timestamp < datetime('now', '-30 days');

DELETE FROM events
WHERE id IN (SELECT id FROM events_archive);
```

### Event Batching

```python
# Batch events before sending
events_buffer = []

def send_event(event):
    events_buffer.append(event)

    if len(events_buffer) >= 10:
        flush_events()

def flush_events():
    requests.post(server_url, json={"events": events_buffer})
    events_buffer.clear()
```

## Integration with Observability Platforms

### Datadog

```python
from datadog import statsd

def send_to_datadog(event):
    statsd.increment(f"claude.tool.{event['toolName']}")
    statsd.histogram(f"claude.duration.{event['toolName']}", event['duration'])
```

### Prometheus

```python
from prometheus_client import Counter, Histogram

tool_counter = Counter('claude_tool_executions', 'Tool executions', ['tool_name'])
tool_duration = Histogram('claude_tool_duration_seconds', 'Tool duration', ['tool_name'])

def send_to_prometheus(event):
    tool_counter.labels(tool_name=event['toolName']).inc()
    tool_duration.labels(tool_name=event['toolName']).observe(event['duration'])
```

### Slack

```python
import requests

def send_to_slack(event):
    if event['eventType'] == 'notification':
        requests.post(
            os.getenv("SLACK_WEBHOOK_URL"),
            json={"text": f"🤖 Agent needs input: {event['message']}"}
        )
```

## Key Principles

1. **If you don't measure it, you can't improve it** - Observability is critical for scaling agents

2. **Keep hooks simple and isolated** - Use single-file scripts (UV, bun, shell)

3. **Never block the agent** - Hooks should be fast and fault-tolerant

4. **Small models for summaries** - Haiku is perfect and costs pennies

5. **One-way data streams** - Simple architecture beats complex bidirectional systems

6. **Context, Model, Prompt** - Even with hooks, the big three still matter

## Source Attribution

**Primary source:** Multi-Agent Observability transcript (complete system architecture, WebSocket streaming, event summarization, SQLite persistence)

**Supporting source:** Hooked transcript (5 hooks fundamentals, pre-tool-use implementation, text-to-speech integration, isolated scripts pattern)

**Key quotes:**

- "When it comes to agentic coding, observability is everything." (Hooked)
- "This one-way data stream keeps things really simple." (Multi-Agent Observability)
- "Thousands of events, less than 20 cents. Small fast models shine here." (Multi-Agent Observability)

## Related Documentation

- [Hooks Reference](../reference/hooks-reference.md) - Complete API reference for all 5 hooks
- [Multi-Agent Case Studies](../examples/multi-agent-case-studies.md) - Real observability systems in action
- [Core 4 Framework](../reference/core-4-framework.md) - Context, Model, Prompt, Tools

---

**Remember:** Observability isn't optional when scaling agents. If you can't see what they're doing, you can't scale them effectively.
