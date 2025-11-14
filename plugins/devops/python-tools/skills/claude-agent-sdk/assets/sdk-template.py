#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
# ]
# ///
"""
Claude Agent SDK Project Template

This template provides a starting point for building SDK applications.

Usage:
1. Copy this file to your project
2. Customize the agent definitions
3. Update the prompt and workflow
4. Run: ./your-script.py

Note: Uses anyio for async runtime (official SDK examples use anyio).
"""

import os

import anyio  # Official SDK examples use anyio
from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


def get_sdk_options() -> ClaudeAgentOptions:
    """Configure SDK options with agents."""
    return ClaudeAgentOptions(
        # Use claude_code preset for orchestrators
        system_prompt={"type": "preset", "preset": "claude_code"},
        # Allow orchestrator to use Task tool for delegation
        allowed_tools=["Bash", "Task", "Read", "Write"],
        # Permission mode: "default", "acceptEdits", or "rejectEdits"
        permission_mode="acceptEdits",
        # Define subagents programmatically
        agents={
            "example-agent": AgentDefinition(
                description="Replace with agent purpose/when to use",
                prompt="Replace with agent's system prompt and instructions",
                tools=["Read", "Grep"],  # Limit to needed tools
                model="sonnet",  # or "opus", "haiku", "inherit"
            ),
        },
        model="claude-sonnet-4-5",
    )


async def main():
    """Main workflow."""
    # Verify API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return

    print("🚀 Starting SDK Application")
    print("=" * 60)

    # Get SDK configuration
    options = get_sdk_options()

    # Create client and send query
    async with ClaudeSDKClient(options=options) as client:
        # Replace with your actual prompt
        prompt = "Your task description here"

        print(f"\n📨 Query: {prompt}\n")
        await client.query(prompt)

        # Stream responses
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}\n")

            elif isinstance(message, ResultMessage):
                print("\n" + "=" * 60)
                print("✅ Complete")
                if message.duration_ms:
                    print(f"Duration: {message.duration_ms}ms")
                if message.total_cost_usd:
                    print(f"Cost: ${message.total_cost_usd:.4f}")
                print("=" * 60)


if __name__ == "__main__":
    anyio.run(main)  # Official SDK examples use anyio.run()
