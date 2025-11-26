# Agent Skills in the SDK

> Extend Claude with specialized capabilities using Agent Skills in the Claude Agent SDK

## Overview

Agent Skills extend Claude with specialized capabilities that Claude autonomously invokes when relevant. Skills are packaged as `SKILL.md` files containing instructions, descriptions, and optional supporting resources.

For comprehensive information about Skills, including benefits, architecture, and authoring guidelines, see the [Agent Skills overview](/en/docs/agents-and-tools/agent-skills/overview).

## How Skills Work with the SDK

When using the Claude Agent SDK, Skills are:

1. **Defined as filesystem artifacts**: Created as `SKILL.md` files in specific directories (`.claude/skills/`)
2. **Loaded from filesystem**: Skills are loaded from configured filesystem locations. You must specify `settingSources` (TypeScript) or `setting_sources` (Python) to load Skills from the filesystem
3. **Automatically discovered**: Once filesystem settings are loaded, Skill metadata is discovered at startup from user and project directories; full content loaded when triggered
4. **Model-invoked**: Claude autonomously chooses when to use them based on context
5. **Enabled via allowed\_tools**: Add `"Skill"` to your `allowed_tools` to enable Skills

Unlike subagents (which can be defined programmatically), Skills must be created as filesystem artifacts. The SDK does not provide a programmatic API for registering Skills.

  **Default behavior**: By default, the SDK does not load any filesystem settings. To use Skills, you must explicitly configure `settingSources: ['user', 'project']` (TypeScript) or `setting_sources=["user", "project"]` (Python) in your options.

## Using Skills with the SDK

To use Skills with the SDK, you need to:

1. Include `"Skill"` in your `allowed_tools` configuration
2. Configure `settingSources`/`setting_sources` to load Skills from the filesystem

Once configured, Claude automatically discovers Skills from the specified directories and invokes them when relevant to the user's request.

  ```python Python theme={null}
  import asyncio
  from claude_agent_sdk import query, ClaudeAgentOptions

  async def main():
      options = ClaudeAgentOptions(
```

```python
cwd="/path/to/project",  # Project with .claude/skills/          cwd="/path/to/project",  # Project with .claude/skills/
          setting_sources=["user", "project"],  # Load Skills from filesystem
          allowed_tools=["Skill", "Read", "Write", "Bash"]  # Enable Skill tool
      )

```

```python
async for message in query(      async for message in query(
          prompt="Help me process this PDF document",
          options=options
      ):
          print(message)

  asyncio.run(main())
  ```

options: {    options: {
      cwd: "/path/to/project",  // Project with .claude/skills/
      settingSources: ["user", "project"],  // Load Skills from filesystem
      allowedTools: ["Skill", "Read", "Write", "Bash"]  // Enable Skill tool
    }
  })) {
    console.log(message);
  }

  ```text

## Skill Locations

Skills are loaded from filesystem directories based on your `settingSources`/`setting_sources` configuration:

* **Project Skills** (`.claude/skills/`): Shared with your team via git - loaded when `setting_sources` includes `"project"`
* **User Skills** (`~/.claude/skills/`): Personal Skills across all projects - loaded when `setting_sources` includes `"user"`
* **Plugin Skills**: Bundled with installed Claude Code plugins

## Creating Skills

Skills are defined as directories containing a `SKILL.md` file with YAML frontmatter and Markdown content. The `description` field determines when Claude invokes your Skill.

**Example directory structure**:

```bash  theme={null}
.claude/skills/processing-pdfs/
└── SKILL.md
  ```

For complete guidance on creating Skills, including SKILL.md structure, multi-file Skills, and examples, see:

* [Agent Skills in Claude Code](/en/docs/claude-code/skills): Complete guide with examples
* [Agent Skills Best Practices](/en/docs/agents-and-tools/agent-skills/best-practices): Authoring guidelines and naming conventions

## Tool Restrictions

  The `allowed-tools` frontmatter field in SKILL.md is only supported when using Claude Code CLI directly. **It does not apply when using Skills through the SDK**.

  When using the SDK, control tool access through the main `allowedTools` option in your query configuration.

To restrict tools for Skills in SDK applications, use the `allowedTools` option:

  Import statements from the first example are assumed in the following code snippets.

  ```python Python theme={null}
  options = ClaudeAgentOptions(
      setting_sources=["user", "project"],  # Load Skills from filesystem
```

```python
allowed_tools=["Skill", "Read", "Grep", "Glob"]  # Restricted toolset      allowed_tools=["Skill", "Read", "Grep", "Glob"]  # Restricted toolset
  )

  async for message in query(
      prompt="Analyze the codebase structure",
```python
options=options      options=options
  ):
      print(message)
  ```

options: {    options: {
      settingSources: ["user", "project"],  // Load Skills from filesystem
      allowedTools: ["Skill", "Read", "Grep", "Glob"]  // Restricted toolset
    }
  })) {
    console.log(message);
  }

  ```text

## Discovering Available Skills

To see which Skills are available in your SDK application, simply ask Claude:

  ```python Python theme={null}
  options = ClaudeAgentOptions(
      setting_sources=["user", "project"],  # Load Skills from filesystem
```python
allowed_tools=["Skill"]      allowed_tools=["Skill"]
  )

  async for message in query(
      prompt="What Skills are available?",
```python
options=options      options=options
  ):
      print(message)
  ```

options: {    options: {
      settingSources: ["user", "project"],  // Load Skills from filesystem
      allowedTools: ["Skill"]
    }
  })) {
    console.log(message);
  }

  ```text

Claude will list the available Skills based on your current working directory and installed plugins.

## Testing Skills

Test Skills by asking questions that match their descriptions:

  ```python Python theme={null}
  options = ClaudeAgentOptions(
      cwd="/path/to/project",
```python
setting_sources=["user", "project"],  # Load Skills from filesystem      setting_sources=["user", "project"],  # Load Skills from filesystem
      allowed_tools=["Skill", "Read", "Bash"]
  )

  async for message in query(
      prompt="Extract text from invoice.pdf",
```python
options=options      options=options
  ):
      print(message)
  ```

options: {    options: {
      cwd: "/path/to/project",
      settingSources: ["user", "project"],  // Load Skills from filesystem
      allowedTools: ["Skill", "Read", "Bash"]
    }
  })) {
    console.log(message);
  }

  ```text

Claude automatically invokes the relevant Skill if the description matches your request.

## Troubleshooting

### Skills Not Found

**Check settingSources configuration**: Skills are only loaded when you explicitly configure `settingSources`/`setting_sources`. This is the most common issue:

  ```python Python theme={null}

## Wrong - Skills won't be loaded

  options = ClaudeAgentOptions(
      allowed_tools=["Skill"]
  )

## Correct - Skills will be loaded

  options = ClaudeAgentOptions(
      setting_sources=["user", "project"],  # Required to load Skills
```python
allowed_tools=["Skill"]      allowed_tools=["Skill"]
  )
  ```

allowedTools: ["Skill"]    allowedTools: ["Skill"]
  };

  ```text

For more details on `settingSources`/`setting_sources`, see the [TypeScript SDK reference](/en/api/agent-sdk/typescript#settingsource) or [Python SDK reference](/en/api/agent-sdk/python#settingsource).

**Check working directory**: The SDK loads Skills relative to the `cwd` option. Ensure it points to a directory containing `.claude/skills/`:

  ```python Python theme={null}

## Ensure your cwd points to the directory containing .claude/skills/

  options = ClaudeAgentOptions(
      cwd="/path/to/project",  # Must contain .claude/skills/
```python
setting_sources=["user", "project"],  # Required to load Skills      setting_sources=["user", "project"],  # Required to load Skills
      allowed_tools=["Skill"]
  )
  ```

settingSources: ["user", "project"],  // Required to load Skills    settingSources: ["user", "project"],  // Required to load Skills
    allowedTools: ["Skill"]
  };

  ```text

See the "Using Skills with the SDK" section above for the complete pattern.

**Verify filesystem location**:

```bash  theme={null}

## Check project Skills

ls .claude/skills/*/SKILL.md

## Check personal Skills

ls ~/.claude/skills/*/SKILL.md
  ```

### Skill Not Being Used

**Check the Skill tool is enabled**: Confirm `"Skill"` is in your `allowedTools`.

**Check the description**: Ensure it's specific and includes relevant keywords. See [Agent Skills Best Practices](/en/docs/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions) for guidance on writing effective descriptions.

### Additional Troubleshooting

For general Skills troubleshooting (YAML syntax, debugging, etc.), see the [Claude Code Skills troubleshooting section](/en/docs/claude-code/skills#troubleshooting).

## Related Documentation

### Skills Guides

* [Agent Skills in Claude Code](/en/docs/claude-code/skills): Complete Skills guide with creation, examples, and troubleshooting
* [Agent Skills Overview](/en/docs/agents-and-tools/agent-skills/overview): Conceptual overview, benefits, and architecture
* [Agent Skills Best Practices](/en/docs/agents-and-tools/agent-skills/best-practices): Authoring guidelines for effective Skills
* [Agent Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills): Example Skills and templates

### SDK Resources

* [Subagents in the SDK](/en/api/agent-sdk/subagents): Similar filesystem-based agents with programmatic options
* [Slash Commands in the SDK](/en/api/agent-sdk/slash-commands): User-invoked commands
* [SDK Overview](/en/api/agent-sdk/overview): General SDK concepts
* [TypeScript SDK Reference](/en/api/agent-sdk/typescript): Complete API documentation
* [Python SDK Reference](/en/api/agent-sdk/python): Complete API documentation
