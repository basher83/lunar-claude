#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
#     "langsmith[claude-agent-sdk]",
# ]
# ///
"""
NoteSmith - Concise Research Assistant

Purpose: interactive-repl-demo
Team: devops
Author: devops@spaceships.work

A Claude Agent SDK application demonstrating:
- Custom MCP tools (save_note, find_note)
- Hook-based safety (blocking dangerous commands)
- Interactive REPL with streaming responses
- WebFetch integration for URL summarization
- LangSmith tracing integration

Usage:
    ./scripts/note_smith.py

Environment Variables (for LangSmith tracing):
    LANGSMITH_API_KEY     - Your LangSmith API key
    LANGSMITH_PROJECT     - Project name (optional, defaults to "default")
    LANGSMITH_TRACING     - Set to "true" to enable tracing

Commands:
    /summarize <url>  - Summarize a webpage
    /note <text>      - Save a note locally
    /find <pattern>   - Search saved notes
    /help             - Show help
    /exit             - Quit

Examples:
    # Basic usage
    ./scripts/note_smith.py

    # With LangSmith tracing
    LANGSMITH_API_KEY=your_key LANGSMITH_TRACING=true ./scripts/note_smith.py

    # Then use interactive commands like:
    # /note Remember to check logs
    # /find logs
    # /summarize https://example.com
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookContext,
    HookMatcher,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)

# Configure LangSmith tracing if enabled
if os.getenv("LANGSMITH_TRACING", "").lower() == "true":
    try:
        from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

        configure_claude_agent_sdk()
        print("✓ LangSmith tracing enabled", file=sys.stderr)
    except ImportError:
        print("⚠ LangSmith not installed. Run: uv add langsmith[claude-agent-sdk]", file=sys.stderr)

# ----------------------------
# Storage (simple local notes)
# ----------------------------

NOTES_DIR = Path(__file__).parent / "notes"
NOTES_DIR.mkdir(exist_ok=True)


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_note_to_disk(text: str) -> str:
    path = NOTES_DIR / f"note_{_ts()}.txt"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    return str(path)


def grep_notes(pattern: str) -> list[str]:
    pat = pattern.lower()
    out: list[str] = []
    for p in NOTES_DIR.glob("*.txt"):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if pat in line.lower():
                out.append(f"{p.name}:{i}: {line}")
    return out


# ----------------------------
# Custom MCP tools
# ----------------------------


@tool("save_note", "Save a short note to local disk", {"text": str})
async def save_note(args: dict[str, Any]) -> dict[str, Any]:
    path = save_note_to_disk(args["text"])
    return {"content": [{"type": "text", "text": f"Saved note → {path}"}]}


@tool("find_note", "Find notes containing a pattern (case-insensitive)", {"pattern": str})
async def find_note(args: dict[str, Any]) -> dict[str, Any]:
    hits = grep_notes(args["pattern"])
    body = "\n".join(hits) if hits else "No matches."
    return {"content": [{"type": "text", "text": body}]}


UTILS_SERVER = create_sdk_mcp_server(
    name="notes_util",
    version="1.0.0",
    tools=[save_note, find_note],
)

# ----------------------------
# Optional safety hook (Bash)
# ----------------------------


async def block_dangerous_bash(
    input_data: dict[str, Any], tool_use_id: str | None, context: HookContext
):
    if input_data.get("tool_name") == "Bash":
        cmd = str(input_data.get("tool_input", {}).get("command", "")).strip().lower()
        if "rm -rf /" in cmd or "format c:" in cmd:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Dangerous command blocked",
                }
            }
    return {}


# ----------------------------
# Prompts & UI
# ----------------------------

SYSTEM_PROMPT = """You are NoteSmith, a concise research assistant.
- Prefer bullet answers with crisp takeaways.
- When the user asks to /summarize <url>, use WebFetch to retrieve and then summarize 5 key points + a 1-line TL;DR.
- When the user types /note <text>, call the custom save_note tool.
- When the user types /find <pattern>, call the custom find_note tool.
- Keep answers short unless asked to expand.
"""

HELP = """Commands:
  /summarize <url>      Summarize a webpage (WebFetch)
  /note <text>          Save a note locally
  /find <pattern>       Search saved notes
  /help                 Show this help
  /exit                 Quit
"""

# Use the broadest model label for compatibility; switch to "sonnet-4.5" if your CLI lists it.
MODEL = "sonnet"

# ----------------------------
# Main app
# ----------------------------


async def main():
    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        permission_mode="acceptEdits",
        allowed_tools=[
            # Built-ins (Claude may use these if relevant)
            "WebFetch",
            "Read",
            "Write",
            "Grep",
            "Glob",
            # Our MCP tools (SDK prefixes mcp__<alias>__<toolname>)
            "mcp__utils__save_note",
            "mcp__utils__find_note",
        ],
        mcp_servers={"utils": UTILS_SERVER},
        hooks={"PreToolUse": [HookMatcher(hooks=[block_dangerous_bash])]},
        setting_sources=None,  # no filesystem settings; everything is programmatic
    )

    print("💡 NoteSmith (Claude Sonnet)\n")
    print(HELP)

    async with ClaudeSDKClient(options=options) as client:
        while True:
            user = input("\nYou: ").strip()
            if not user:
                continue
            if user.lower() in {"/exit", "exit", "quit"}:
                print("Bye!")
                break
            if user.lower() in {"/help", "help"}:
                print(HELP)
                continue

            # Lightweight command parsing (the system prompt also guides tool usage)
            if user.startswith("/summarize "):
                url = user.split(" ", 1)[1].strip()
                prompt = f"Summarize this URL using WebFetch and return 5 bullets + TL;DR:\n{url}"
            elif user.startswith("/note "):
                text = user.split(" ", 1)[1]
                prompt = f'Please call tool save_note with text="{text}"'
            elif user.startswith("/find "):
                patt = user.split(" ", 1)[1]
                prompt = f'Please call tool find_note with pattern="{patt}"'
            else:
                prompt = user

            await client.query(prompt)

            # -------- Response streaming with footer to STDERR --------
            model_used = None
            usage = None
            cost = None

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    if model_used is None:
                        model_used = message.model  # e.g., "sonnet" or "sonnet-4.5"
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="", flush=True)  # stdout
                        elif isinstance(block, ToolUseBlock):
                            print(
                                f"\n🛠️  Using tool: {block.name} with input: {json.dumps(block.input)}"
                            )
                        elif isinstance(block, ToolResultBlock) and isinstance(block.content, list):
                            for part in block.content:
                                if isinstance(part, dict) and part.get("type") == "text":
                                    print(f"\n🔎 Tool says: {part.get('text')}")
                elif isinstance(message, ResultMessage):
                    usage = message.usage or {}
                    cost = message.total_cost_usd
                    # Do not break early; let stream end naturally

            # Footer (model + tokens + cost) → STDERR so normal output stays clean
            def _token_summary(u: dict) -> str:
                total = u.get("total_tokens")
                if total is None:
                    it, ot = u.get("input_tokens"), u.get("output_tokens")
                    if it is not None or ot is not None:
                        total = (it or 0) + (ot or 0)
                if total is None:
                    return "tokens=?"
                if "input_tokens" in u or "output_tokens" in u:
                    return f"tokens={total} (in={u.get('input_tokens', '?')}, out={u.get('output_tokens', '?')})"
                return f"tokens={total}"

            footer = (
                f"\n\n— Turn done. model={(model_used or options.model)} "
                f"{_token_summary(usage or {})} cost={cost if cost is not None else '?'} —"
            )
            print(footer, file=sys.stderr)


# Entry
if __name__ == "__main__":
    asyncio.run(main())
