# Overview

> Get AI code reviews directly in your CLI before you commit. Catch race conditions, memory leaks, and security vulnerabilities without leaving your development environment.

<Warning>The CodeRabbit CLI is in Beta.</Warning>

## Review local changes

<Info>
  Looking for the full CodeRabbit experience? This page covers local CLI
  reviews. For complete code reviews on pull requests, see
  [Introduction](/overview/introduction).
</Info>

The CodeRabbit CLI analyzes your uncommitted changes using the same pattern recognition that powers our PR reviews. Review code as you write it, apply suggested fixes instantly, and catch critical issues while you still have full context in memory.

You can get your code reviewed before you commit and get feedback immediately when the code is fresh in your mind.

## Key features

<CardGroup cols={2}>
  <Card title="Review uncommitted changes" icon="code">
    Analyze your working directory for race conditions, null pointer exceptions,
    and logic errors before you commit.
  </Card>

  <Card title="One-step fixes" icon="wand-sparkles">
    Apply simple fixes like import corrections instantly. Hand complex
    architectural issues to your AI agent with full context.
  </Card>

  <Card title="Context-aware reviews" icon="brain">
    Paid users get reviews enhanced by learnings from your team's patterns -
    remembers your error handling styles, architectural decisions, and coding
    preferences.
  </Card>

  <Card title="Detects coding agent files" icon="folder-root">
    Automatically reads claude.md, .cursorrules, and custom team standards to
    enforce your specific coding guidelines in every review.
  </Card>
</CardGroup>

## AI agent integration

You're already using CodeRabbit for PR reviews. With the CLI, you can now catch issues before you commit - reviewing uncommitted changes while the code is fresh in your mind. CodeRabbit detects the problems, then your AI coding agent implements the fixes.

### Example prompt for your AI agent

Here's a complete prompt you can use with Claude Code, Cursor, or other AI coding agents:

```
Please implement phase 7.3 of the planning doc and then run coderabbit --prompt-only,
let it run as long as it needs (run it in the background) and fix any issues.
```

### Components of a good prompt

Breaking down what makes an effective CodeRabbit + AI agent workflow:

<Steps>
  <Step title="Run CodeRabbit CLI">
    Tell your AI agent to run CodeRabbit with the `--prompt-only` flag:

    ```bash  theme={null}
    coderabbit --prompt-only
    ```

    You can also specify review types or branches:

    ```bash  theme={null}
    # Review only uncommitted changes
    coderabbit --prompt-only --type uncommitted

    # With specific base branch
    coderabbit --prompt-only --base develop
    ```
  </Step>

  <Step title="Run in the background">
    CodeRabbit reviews can take 7-30+ minutes depending on the scope of changes. Instruct your AI agent to run CodeRabbit in the background and set up a timer to check periodically:

    ```
    Run coderabbit --prompt-only --type uncommitted in the background, let it take as long as it needs,
    and check on it periodically.
    ```
  </Step>

  <Step title="Evaluate and implement fixes">
    Once CodeRabbit completes, have your AI agent evaluate the findings and prioritize:

    ```
    Evaluate the fixes and considerations. Fix major issues only, or fix any critical
    issues and ignore the nits.
    ```

    This keeps your agent focused on meaningful improvements rather than minor style issues.
  </Step>

  <Step title="Verify with a second pass">
    Run CodeRabbit one more time to ensure fixes didn't introduce new issues:

    ```
    Once those changes are implemented, run CodeRabbit CLI one more time to make sure
    we addressed all the critical issues and didn't introduce any additional bugs.
    ```
  </Step>

  <Step title="Set loop limits">
    Prevent infinite iteration by setting clear completion criteria:

    ```
    Only run the loop twice. If on the second run you don't find any critical issues,
    ignore the nits and you're complete. Give me a summary of everything that was
    completed and why.
    ```

    This ensures your AI agent completes the task efficiently and provides a clear report.
  </Step>
</Steps>

### Integration guides

See detailed workflows for specific AI coding agents:

<CardGroup cols={2}>
  <Card title="Claude Code integration" icon="robot" href="/cli/claude-code-integration">
    Automated workflow with background execution and task-based fixes
  </Card>

  <Card title="Codex integration" icon="terminal" href="/cli/codex-integration">
    Integrated code review and fix implementation with Codex CLI
  </Card>
</CardGroup>

## Pricing and capabilities

<CardGroup cols={2}>
  <Card title="Free tier" icon="heart">
    Basic static analysis with limited daily usage.

    * Catches syntax errors, obvious logic issues, and common security patterns.
    * Perfect for individual developers trying out the CLI workflow.
    * **Rate limit**: 1 review per hour
  </Card>

  <Card title="Paid plans" icon="crown">
    Enhanced reviews powered by learnings from your codebase history plus higher rate limits.

    Paid users with linked GitHub accounts get:

    * **Learnings-powered reviews**: Remembers your team's preferred patterns for error handling, state management, and architecture
    * **Full contextual analysis**: Understands your imports, dependencies, and project structure
    * **Team standards enforcement**: Applies your documented coding guidelines automatically
    * **Advanced issue detection**: Spots subtle race conditions, performance bottlenecks, and security vulnerabilities
    * **Rate limits**:
      * Pro plan: 5 reviews per hour
      * Lite plan: 1 review per hour
  </Card>
</CardGroup>

<Tip>
  Paid users get nearly all PR review features in the CLI, including learnings
  and contextual analysis. Only chat, docstrings, and unit test generation
  remain exclusive to PR reviews.
</Tip>

Contact [sales@coderabbit.ai](mailto:sales@coderabbit.ai) for custom rate limits or enterprise needs.

<Info>
  **Platform support**: Currently available on Apple (Intel and Apple Silicon)
  and Linux. Windows support is not available at this time.
</Info>

## Video demo

See CodeRabbit CLI in action with Claude Code:

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/IqBKf4u5MtA" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

## Getting started

<Steps>
  <Step title="Install CLI">
    Download and install the CodeRabbit CLI to start reviewing code locally.

    ```bash  theme={null}
    curl -fsSL https://cli.coderabbit.ai/install.sh | sh
    ```
  </Step>

  <Step title="Restart your shell">
    After installation, restart your shell or reload your shell configuration.

    ```bash  theme={null}
    # Restart your shell or run:
    source ~/.zshrc
    ```
  </Step>

  <Step title="Authenticate">
    Link your CodeRabbit account to enable personalized reviews based on your team's patterns.

    ```bash  theme={null}
    coderabbit auth login
    # or use the short alias
    cr auth login
    ```

    Follow the browser redirect to sign in and copy the access token back to your CLI.
  </Step>

  <Step title="Review your code">
    Analyze your Git repository for issues using the CodeRabbit CLI.

    ```bash  theme={null}
    coderabbit
    # use plain mode or prompt-only mode when using it with Claude Code, Codex CLI, Gemini CLI, etc.
    coderabbit --plain
    ```

    If your main branch is not `main`, specify your base branch:

    ```bash  theme={null}
    coderabbit --base develop
    # or for other base branches
    coderabbit --base master
    ```

    CodeRabbit scans your working directory and provides specific feedback with suggested fixes.
  </Step>

  <Step title="Apply suggestions">
    Review findings in your terminal and either apply quick fixes or send complex issues to your AI coding agent.
  </Step>
</Steps>

## Review modes

The CLI offers different output formats to fit your workflow:

```bash  theme={null}
# Interactive mode (default) - full interface with browsable findings
coderabbit

# Plain text mode - detailed feedback with fix suggestions
coderabbit --plain

# Prompt-only mode - minimal output optimized for AI agents
coderabbit --prompt-only
```

## Working with review results

CodeRabbit analyzes your code and surfaces specific issues with actionable suggestions. Each finding includes the problem location, explanation, and recommended fix.

Example findings include:

* **Race condition detected**: "This goroutine accesses shared state without proper locking"
* **Memory leak potential**: "Stream not closed in error path - consider using defer"
* **Security vulnerability**: "SQL query uses string concatenation - switch to parameterized queries"
* **Logic error**: "Function returns nil without checking error condition first"

### Browse and apply suggestions

In interactive mode, use the arrow keys to navigate to a finding and press enter to see the detailed explanation and suggested fix inline in your CLI.

For simple issues like missing imports, syntax errors, or formatting problems, choose **Apply suggested change** to fix immediately.

### Use AI coding agents

For AI agent integration, see the [AI agent integration](#ai-agent-integration) section for detailed workflow guidance and integration guides.

### Managing comments

* **Ignore**: Hide findings you want to address later
* **Restore**: Click collapsed findings in the sidebar to show again

## Command reference

| Command                    | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `coderabbit`               | Run code review (interactive mode by default)                |
| `coderabbit --plain`       | Output detailed feedback in plain text format                |
| `coderabbit --prompt-only` | Show minimal output optimized for AI agents                  |
| `coderabbit auth`          | Authentication commands                                      |
| `coderabbit review`        | AI-driven code reviews with interactive or plain text output |
| `cr`                       | Short alias for all coderabbit commands                      |

### Additional options

| Option                    | Description                                                                  |
| ------------------------- | ---------------------------------------------------------------------------- |
| `-t, --type <type>`       | Review type: all, committed, uncommitted (default: "all")                    |
| `-c, --config <files...>` | Additional instructions for CodeRabbit AI (e.g., claude.md, coderabbit.yaml) |
| `--base <branch>`         | Base branch for comparison                                                   |
| `--base-commit <commit>`  | Base commit on current branch for comparison                                 |
| `--cwd <path>`            | Working directory path                                                       |
| `--no-color`              | Disable colored output                                                       |

<Note>
  PR reviews and CLI reviews will differ, even if run on the same code. CLI
  reviews optimize for immediate feedback during active development, while PR
  reviews provide comprehensive team collaboration context and broader
  repository analysis.
</Note>

## Uninstall

Remove CodeRabbit CLI based on how you installed it.

### If installed using install script

```bash  theme={null}
rm $(which coderabbit)
```

This removes the CodeRabbit binary from your PATH.

### If installed using Homebrew

```bash  theme={null}
brew remove coderabbit
```
