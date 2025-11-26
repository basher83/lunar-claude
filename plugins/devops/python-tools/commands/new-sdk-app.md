---
description: Create and setup a new Claude Agent SDK application (Python)
argument-hint: [project-name]
---

You are tasked with helping the user create a new Claude Agent SDK application using Python. Follow these steps carefully:

## Reference Documentation

Before starting, use the **claude-agent-sdk skill** to ensure you follow SDK best practices:

```bash
# Load the skill to access patterns and examples
/skill claude-agent-sdk
```

The skill provides:

- SDK templates (assets/sdk-template.py)
- Official examples (examples/)
- Best practices and patterns (references/)
- Validation checklist (assets/sdk-validation-checklist.md)

Also reference the official documentation:

- Python SDK reference: <https://docs.claude.com/en/api/agent-sdk/python>

**IMPORTANT**: Always check for and use the latest SDK version (targeting >= 0.1.6).

## Gather Requirements

IMPORTANT: Ask these questions one at a time. Wait for the user's response before asking the next question. This makes it easier for the user to respond.

Ask the questions in this order (skip any that the user has already provided via arguments):

1. **Project name** (ask first): "What would you like to name your project?"

   - If $ARGUMENTS is provided, use that as the project name and skip this question
   - Wait for response before continuing

2. **Agent type** (ask second, but skip if #1 was sufficiently detailed): "What kind of agent are you building? Some examples:

   - Coding agent (SRE, security review, code review)
   - Orchestrator with subagents (multi-agent workflows)
   - Business agent (customer support, content creation)
   - Custom agent (describe your use case)"
   - Wait for response before continuing

3. **Starting point** (ask third): "Would you like:

   - A minimal query() example for simple tasks
   - A ClaudeSDKClient example for multi-turn conversations
   - An orchestrator with subagents
   - Start from the SDK template (assets/sdk-template.py)"
   - Wait for response before continuing

4. **Project structure** (ask fourth): "What project structure would you prefer:

   - Single-file uv script (self-contained with `# /// script` header)
   - Standard Python project with pyproject.toml"
   - Wait for response before continuing

After all questions are answered, proceed to create the setup plan.

## Setup Plan

Based on the user's answers, create a plan that includes:

1. **Project initialization**:

   - Create project directory (if it doesn't exist)
   - **For uv scripts**: Create single Python file with `# /// script` header including `claude-agent-sdk` dependency
   - **For standard projects**:
     - Initialize with `pyproject.toml`
     - Add `claude-agent-sdk` to dependencies
     - Configure Python version requirements (>= 3.8)

2. **Check for Latest Versions**:

   - BEFORE installing, check PyPI for the latest version: <https://pypi.org/project/claude-agent-sdk/>
   - Inform the user which version you're using (targeting >= 0.1.6)

3. **SDK Installation**:

   - **For uv scripts**: Dependencies specified in script header, no separate installation needed
   - **For standard projects**:
     - Install with `pip install claude-agent-sdk` or add to pyproject.toml
     - After installation, verify with `pip show claude-agent-sdk`

4. **Create starter files**:

   Based on user's choice:

   - **query() example**: Simple one-shot task (no conversation memory)
   - **ClaudeSDKClient example**: Multi-turn conversation with context
   - **Orchestrator**: Main orchestrator with programmatically registered subagents
   - **SDK template**: Copy from `assets/sdk-template.py` and customize

   All files should include:
   - Proper imports (`claude_agent_sdk`, `anyio`)
   - SDK best practices (system_prompt, allowed_tools, permission_mode)
   - Error handling
   - Clear comments explaining each part

5. **Authentication setup**:

   - Explain that the SDK uses local Claude Code authentication
   - No `.env` files needed when running with Claude Code
   - If running standalone, API key can be set via environment variable

6. **Optional: Create .claude directory structure**:
   - Offer to create `.claude/agents/` directory for subagent definitions
   - Provide example agent markdown files if building an orchestrator

## Implementation

After gathering requirements and getting user confirmation on the plan:

1. Check for latest SDK version on PyPI
2. Execute the setup steps
3. Create all necessary files based on project structure choice:
   - **Uv script**: Single file with proper script header
   - **Standard project**: pyproject.toml + source files
4. Install dependencies if standard project (uv scripts handle deps automatically)
5. Verify installed versions and inform the user
6. Create a working example based on their starting point:
   - Use patterns from the claude-agent-sdk skill
   - Reference examples from `examples/` directory
   - Follow SDK best practices
7. Add helpful comments explaining SDK concepts:
   - What `ClaudeAgentOptions` does
   - Why `system_prompt="claude_code"` for orchestrators
   - Tool restrictions and permission modes
   - Async runtime choice (anyio vs asyncio)
8. **VERIFY THE CODE WORKS BEFORE FINISHING**:
   - Verify imports are correct
   - Check for syntax errors
   - Validate SDK patterns match documentation
   - Ensure agent names match if using orchestrator
   - **DO NOT consider the setup complete until the code verifies successfully**

## Verification

After all files are created and dependencies are installed, launch the **agent-sdk-verifier-py** agent to validate that the Agent SDK application is properly configured and ready for use:

1. Use the Task tool to launch the `agent-sdk-verifier-py` subagent
2. The agent will check:
   - SDK installation and configuration
   - Proper imports and SDK patterns
   - query() vs ClaudeSDKClient usage
   - Orchestrator requirements (system_prompt, Task tool, agent registration)
   - Permission and security settings
   - Best practices adherence
3. Review the verification report and address any issues before completing setup

## Getting Started Guide

Once setup is complete and verified, provide the user with:

1. **Next steps**:

   - **For uv scripts**: Run with `uv run <script-name>.py` (automatically handles dependencies)
   - **For standard projects**:
     - Activate virtual environment if needed
     - Run with `python main.py` or `python src/main.py`
   - Authentication uses local Claude Code session (no API key setup needed)

2. **Useful resources**:

   - Python SDK reference: <https://docs.claude.com/en/api/agent-sdk/python>
   - claude-agent-sdk skill: `/skill claude-agent-sdk` for patterns and examples
   - Key concepts to explore:
     - System prompts (preset vs custom)
     - Permissions (permission_mode and callbacks)
     - Tools (allowed_tools restrictions)
     - MCP servers (custom tools)
     - Subagents (programmatic registration)

3. **Common next steps**:
   - Customize the system prompt for your use case
   - Add custom tools via SDK MCP servers (see `examples/mcp_calculator.py`)
   - Configure permission callbacks for fine-grained control
   - Create and register subagents programmatically
   - Review examples in the skill: `examples/hooks.py`, `examples/streaming_mode.py`
   - Validate changes with `assets/sdk-validation-checklist.md`

## Important Notes

- **ALWAYS USE LATEST SDK VERSION**: Check PyPI for the latest version (targeting >= 0.1.6)
- **VERIFY CODE WORKS BEFORE FINISHING**:
  - Verify imports are correct
  - Check syntax
  - Validate SDK patterns (query() vs ClaudeSDKClient, system_prompt, tools)
  - Ensure agent names match if using orchestrator
  - Launch agent-sdk-verifier-py for comprehensive validation
  - Do NOT consider the task complete until verification passes
- **USE THE CLAUDE-AGENT-SDK SKILL**: Reference patterns and examples from the skill
- **FOLLOW SDK BEST PRACTICES**:
  - Use `system_prompt="claude_code"` for orchestrators
  - Register agents programmatically via `agents={}`
  - Include `"Task"` in orchestrator's allowed_tools
  - Choose appropriate runtime (anyio.run or asyncio.run)
  - Restrict tools to minimum needed per agent
- Always check if directories/files already exist before creating them
- Ensure all code examples are functional and include proper error handling
- Use patterns compatible with the latest SDK version
- Make the experience interactive and educational
- **ASK QUESTIONS ONE AT A TIME** - Do not ask multiple questions in a single response

Begin by asking the FIRST requirement question only. Wait for the user's answer before proceeding to the next question.
