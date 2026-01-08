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
    ./scripts/note_smith.py --model opus
    ./scripts/note_smith.py --notes-dir /tmp/notes

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

    # With custom model
    ./scripts/note_smith.py --model opus

    # With LangSmith tracing
    LANGSMITH_API_KEY=your_key LANGSMITH_TRACING=true ./scripts/note_smith.py

    # Then use interactive commands like:
    # /note Remember to check logs
    # /find logs
    # /summarize https://example.com
"""

import argparse
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

# ----------------------------
# Constants
# ----------------------------

DEFAULT_MODEL = "sonnet"
DEFAULT_NOTES_DIR = Path(__file__).parent / "notes"

SYSTEM_PROMPT = """You are NoteSmith, a concise research assistant.
- Prefer bullet answers with crisp takeaways.
- When the user asks to /summarize <url>, use WebFetch to retrieve and then summarize 5 key points + a 1-line TL;DR.
- When the user types /note <text>, call the custom save_note tool.
- When the user types /find <pattern>, call the custom find_note tool.
- Keep answers short unless asked to expand.
"""

HELP_TEXT = """Commands:
  /summarize <url>      Summarize a webpage (WebFetch)
  /note <text>          Save a note locally
  /find <pattern>       Search saved notes
  /help                 Show this help
  /exit                 Quit
"""


# ----------------------------
# Storage (simple local notes)
# ----------------------------

# Lazy initialization - set by main() before use
_notes_dir: Path | None = None


def _ensure_notes_dir() -> Path:
    """Get notes directory, creating it if needed. Must be initialized first."""
    if _notes_dir is None:
        raise RuntimeError("Notes directory not initialized. Call init_notes_dir() first.")
    _notes_dir.mkdir(exist_ok=True, parents=True)
    return _notes_dir


def init_notes_dir(path: Path) -> None:
    """Initialize the notes directory path (called from main)."""
    global _notes_dir
    _notes_dir = path


def _ts() -> str:
    """Generate timestamp string for note filenames."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_note_to_disk(text: str) -> str:
    """Save note text to disk with timestamp filename."""
    notes_dir = _ensure_notes_dir()
    path = notes_dir / f"note_{_ts()}.txt"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    return str(path)


def grep_notes(pattern: str) -> list[str]:
    """Search notes for pattern (case-insensitive)."""
    notes_dir = _ensure_notes_dir()
    pat = pattern.lower()
    out: list[str] = []
    for p in notes_dir.glob("*.txt"):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if pat in line.lower():
                out.append(f"{p.name}:{i}: {line}")
    return out


# ----------------------------
# Custom MCP tools
# ----------------------------


@tool("save_note", "Save a short note to local disk", {"text": str})
async def save_note(args: dict[str, Any]) -> dict[str, Any]:
    """MCP tool to save a note."""
    path = save_note_to_disk(args["text"])
    return {"content": [{"type": "text", "text": f"Saved note → {path}"}]}


@tool("find_note", "Find notes containing a pattern (case-insensitive)", {"pattern": str})
async def find_note(args: dict[str, Any]) -> dict[str, Any]:
    """MCP tool to search notes."""
    hits = grep_notes(args["pattern"])
    body = "\n".join(hits) if hits else "No matches."
    return {"content": [{"type": "text", "text": body}]}


def create_notes_server() -> Any:
    """Create MCP server with note tools."""
    return create_sdk_mcp_server(
        name="notes_util",
        version="1.0.0",
        tools=[save_note, find_note],
    )


# ----------------------------
# Optional safety hook (Bash)
# ----------------------------


async def block_dangerous_bash(
    input_data: dict[str, Any], _tool_use_id: str | None, _context: HookContext
) -> dict[str, Any]:
    """PreToolUse hook to block dangerous bash commands."""
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
# Utilities
# ----------------------------


def format_token_summary(usage: dict[str, Any]) -> str:
    """Format token usage for display."""
    total = usage.get("total_tokens")
    if total is None:
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if input_tokens is not None or output_tokens is not None:
            total = (input_tokens or 0) + (output_tokens or 0)
    if total is None:
        return "tokens=?"
    if "input_tokens" in usage or "output_tokens" in usage:
        return f"tokens={total} (in={usage.get('input_tokens', '?')}, out={usage.get('output_tokens', '?')})"
    return f"tokens={total}"


async def async_input(prompt: str) -> str:
    """Non-blocking input using executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: input(prompt).strip())


def configure_langsmith() -> None:
    """Configure LangSmith tracing if enabled via environment."""
    if os.getenv("LANGSMITH_TRACING", "").lower() == "true":
        try:
            from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

            configure_claude_agent_sdk()
            print("✓ LangSmith tracing enabled", file=sys.stderr)
        except ImportError:
            print(
                "⚠ LangSmith not installed. Run: uv add langsmith[claude-agent-sdk]",
                file=sys.stderr,
            )


# ----------------------------
# CLI
# ----------------------------


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="NoteSmith - Interactive research assistant using Claude Agent SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Start with default settings
  %(prog)s --model opus             Use Claude Opus model
  %(prog)s --notes-dir ~/notes      Custom notes directory

Environment:
  LANGSMITH_TRACING=true            Enable LangSmith tracing
  LANGSMITH_API_KEY=<key>           LangSmith API key
""",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=["sonnet", "opus", "haiku"],
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=DEFAULT_NOTES_DIR,
        help=f"Directory for storing notes (default: {DEFAULT_NOTES_DIR})",
    )
    return parser.parse_args()


# ----------------------------
# Main app
# ----------------------------


async def repl_loop(client: ClaudeSDKClient, model: str) -> None:
    """Main REPL loop for user interaction."""
    while True:
        try:
            user = await async_input("\nYou: ")
        except EOFError:
            print("\nBye!")
            break

        if not user:
            continue
        if user.lower() in {"/exit", "exit", "quit"}:
            print("Bye!")
            break
        if user.lower() in {"/help", "help"}:
            print(HELP_TEXT)
            continue

        # Lightweight command parsing (system prompt also guides tool usage)
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

        # Send query and stream response
        try:
            await client.query(prompt)

            model_used: str | None = None
            usage: dict[str, Any] = {}
            cost: float | None = None

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    if model_used is None:
                        model_used = message.model
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="", flush=True)
                        elif isinstance(block, ToolUseBlock):
                            print(
                                f"\n🛠️  Using tool: {block.name} with input: {json.dumps(block.input)}"
                            )
                        elif isinstance(block, ToolResultBlock) and isinstance(block.content, list):
                            for part in block.content:
                                if part.get("type") == "text":
                                    print(f"\n🔎 Tool says: {part.get('text')}")
                elif isinstance(message, ResultMessage):
                    usage = message.usage or {}
                    cost = message.total_cost_usd

            # Footer to stderr
            footer = (
                f"\n\n— Turn done. model={model_used or model} "
                f"{format_token_summary(usage)} cost={cost if cost is not None else '?'} —"
            )
            print(footer, file=sys.stderr)

        except Exception as e:
            print(f"\n[red]Error:[/red] {e}", file=sys.stderr)


async def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Initialize notes directory (lazy - no side effect at import)
    init_notes_dir(args.notes_dir)

    # Configure tracing if enabled
    configure_langsmith()

    # Create MCP server
    utils_server = create_notes_server()

    options = ClaudeAgentOptions(
        model=args.model,
        system_prompt=SYSTEM_PROMPT,
        permission_mode="acceptEdits",
        allowed_tools=[
            "WebFetch",
            "Read",
            "Write",
            "Grep",
            "Glob",
            "mcp__utils__save_note",
            "mcp__utils__find_note",
        ],
        mcp_servers={"utils": utils_server},
        hooks={"PreToolUse": [HookMatcher(hooks=[block_dangerous_bash])]},  # pyright: ignore[reportArgumentType]
        setting_sources=None,
    )

    print(f"💡 NoteSmith (Claude {args.model.title()})\n")
    print(HELP_TEXT)

    try:
        async with ClaudeSDKClient(options=options) as client:
            await repl_loop(client, args.model)
    except KeyboardInterrupt:
        print("\n\nInterrupted. Bye!")
    except Exception as e:
        print(f"Error initializing SDK client: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
