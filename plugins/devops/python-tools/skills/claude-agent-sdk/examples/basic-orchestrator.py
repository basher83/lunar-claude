#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.6",
# ]
# ///
"""
Basic Orchestrator Pattern with Subagents

This example demonstrates the recommended pattern for building an
orchestrator that delegates work to specialized subagents.

Key patterns:
- Programmatic agent registration
- Orchestrator with claude_code system prompt
- Subagents with restricted tools
- Async/await streaming
"""

import asyncio
import os

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


def get_sdk_options() -> ClaudeAgentOptions:
    """
    Create ClaudeAgentOptions with programmatically defined subagents.

    Returns:
        Configured options for ClaudeSDKClient
    """
    return ClaudeAgentOptions(
        # CRITICAL: Orchestrator needs claude_code preset to use Task tool
        system_prompt="claude_code",
        # Orchestrator tools - include Task for delegating to subagents
        allowed_tools=["Bash", "Task", "Read", "Write", "Edit"],
        # Auto-accept file edits for automated workflow
        permission_mode="acceptEdits",
        # Programmatically register subagents (SDK best practice)
        agents={
            "analyzer": AgentDefinition(
                description="Analyzes code structure and identifies patterns",
                prompt="""You are a code analyzer.

Your role:
- Examine code structure and architecture
- Identify patterns and anti-patterns
- Suggest improvements

Use Read, Grep, and Glob to explore the codebase.
Return analysis in structured format.""",
                tools=["Read", "Grep", "Glob"],
                model="sonnet",
            ),
            "fixer": AgentDefinition(
                description="Fixes identified code issues",
                prompt="""You are a code fixer.

Your role:
- Apply fixes based on analysis
- Follow project conventions
- Test changes after applying

Use Read, Edit, and Bash to implement and verify fixes.""",
                tools=["Read", "Edit", "Bash"],
                model="sonnet",
            ),
        },
        model="claude-sonnet-4-5-20250929",
    )


async def main():
    """Run orchestrator workflow."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return

    print("🚀 Starting Basic Orchestrator")
    print("=" * 60)

    options = get_sdk_options()

    async with ClaudeSDKClient(options=options) as client:
        # Orchestrator delegates to analyzer subagent
        prompt = """Use the 'analyzer' subagent to examine the code in this directory.

The analyzer should:
1. Find all Python files
2. Identify code patterns
3. Return a structured analysis report

Wait for the analyzer to complete its work."""

        print("\n📨 Sending query to orchestrator...")
        await client.query(prompt)

        print("\n💬 Receiving response...\n")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                # Print Claude's responses
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}\n")

            elif isinstance(message, ResultMessage):
                # Print execution summary
                print("\n" + "=" * 60)
                print("✅ Workflow Complete")
                print(f"Duration: {message.duration_ms}ms")
                if message.total_cost_usd:
                    print(f"Cost: ${message.total_cost_usd:.4f}")
                print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
