# Claude Code integration

> Enable Claude Code to execute CodeRabbit directly in your development workflow. Let AI code, review, and fix issues autonomously without human intervention.

## Autonomous AI development workflows

CodeRabbit CLI + Claude Code creates autonomous AI development workflows. Because Claude Code executes CodeRabbit directly as part of its process, you can customize the entire workflow to fit your needs. Ask Claude to implement a feature, run a code review, and fix any issues, all without human intervention.

This allows the integration to make AI coding more independent, with built-in quality gates that catch issues before they reach production.

## Video demo

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/IqBKf4u5MtA" title="CodeRabbit CLI + Claude Code integration demo" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

<Info>
  This guide covers integrating CodeRabbit CLI with Claude Code. For standalone
  CLI usage, see [CLI overview](/cli/overview).
</Info>

<Warning>
  **Windows users:** Claude Code requires WSL (Windows Subsystem for Linux) to
  run on Windows. See our [WSL on Windows guide](/cli/wsl-windows) for setup
  instructions before proceeding with this integration.
</Warning>

CodeRabbit analyzes your code changes and surfaces specific issues, then Claude Code applies fixes based on CodeRabbit's context-rich feedback.

## Why integrate these tools

<CardGroup cols={2}>
  <Card title="Expert issue detection" icon="search">
    CodeRabbit spots race conditions, memory leaks, and logic errors that generic linters miss. Same pattern recognition that powers our PR reviews.
  </Card>

  <Card title="AI-powered fixes" icon="wand">
    Claude Code implements fixes with full context from CodeRabbit's analysis.
    Complex architectural changes handled intelligently.
  </Card>

  <Card title="Context preservation" icon="brain">
    CodeRabbit's `--prompt-only` mode gives Claude Code succinct context about
    issues, including location, severity, and suggested approaches.
  </Card>

  <Card title="Continuous workflow" icon="refresh-cw">
    Stay in development flow - run reviews, apply fixes, and iterate without switching tools or losing mental context.
  </Card>
</CardGroup>

## Prerequisites

<Steps>
  <Step title="Install Claude Code">
    Install Claude Code following the platform-specific instructions. Ensure you can launch Claude Code from your terminal.
  </Step>

  <Step title="Install CodeRabbit CLI">
    Install the CodeRabbit CLI globally on your system:

    ```bash  theme={null}
    curl -fsSL https://cli.coderabbit.ai/install.sh | sh
    ```

    Restart your shell:

    ```bash  theme={null}
    source ~/.zshrc
    ```
  </Step>

  <Step title="Authenticate CodeRabbit within Claude">
    Authentication must be done within the Claude Code instance, separate from command line authentication.

    Ask Claude Code to start authentication:

    ```
    Run: coderabbit auth login
    ```

    Claude executes the command and provides a URL. Open the URL in your browser, log in to CodeRabbit, and copy the authentication token.

    Paste the token back to Claude Code.

    <Tip>
      Authentication persists across Claude Code instances - you only need to do this once.
    </Tip>
  </Step>

  <Step title="Verify setup">
    Test that Claude Code can run CodeRabbit commands:

    ```
    Run: coderabbit auth status
    ```

    Success shows your login status and confirms Claude can execute CodeRabbit commands.
  </Step>
</Steps>

## Integration workflow

### Use CodeRabbit as part of building new features

<Steps>
  <Step title="Request implementation + review">
    Ask Claude Code to implement a feature and run CodeRabbit analysis with issue fixes:

    ```
    Please implement phase 7.3 of the planning doc and then run coderabbit --prompt-only,
    let it run as long as it needs (run it in the background) and fix any issues.
    ```

    Key components:

    * **Implement the feature**: Claude codes the requested functionality
    * **Run CodeRabbit**: Uses `--prompt-only` flag for AI-optimized output
    * **Background execution**: Lets CodeRabbit run without blocking Claude
    * **Fix issues**: Claude addresses all problems CodeRabbit identifies
  </Step>

  <Step title="Claude implements and runs CodeRabbit">
    Claude Code:

    1. Implements the requested feature
    2. Runs `coderabbit --prompt-only` in the background
    3. Sets up a timer to check CodeRabbit's progress, or waits for you to prompt completion

    Manually prompt Claude to check if CodeRabbit is done:

    ```
    Is CodeRabbit finished running?
    ```
  </Step>

  <Step title="CodeRabbit analysis and task creation">
    When CodeRabbit completes, Claude Code: 1. Reads the `--prompt-only` output
    (plain text optimized for AI agents) 2. Creates a task list addressing each
    issue CodeRabbit surfaced 3. Shows you the planned fixes before implementing
    them
  </Step>

  <Step title="Automated issue resolution">
    Claude Code systematically works through the task list, implementing fixes for each CodeRabbit finding. The cycle continues until all critical issues are resolved.
  </Step>
</Steps>

### Example: API integration implementation

This example shows the workflow implementing a webhook handler for payment processing:

<Steps>
  <Step title="Start implementation">
    ```bash  theme={null}
    # Working on payment webhook feature
    git checkout -b feature/payment-webhooks
    ```
  </Step>

  <Step title="Run integrated workflow">
    Tell Claude Code to implement and review:

    ```
    Implement the payment webhook handler from the spec document.
    Then run coderabbit --prompt-only in the background and fix any issues.
    ```
  </Step>

  <Step title="CodeRabbit analysis">
    CodeRabbit analyzes the webhook code and identifies issues: - Missing
    signature verification - Race conditions in payment state updates -
    Insufficient error handling for network failures - Webhook replay attack
    vulnerabilities
  </Step>

  <Step title="Claude Code fixes">
    Claude Code automatically applies fixes: - Adds HMAC signature verification -
    Implements database transactions for state consistency - Adds retry logic with
    exponential backoff - Includes idempotency key handling
  </Step>

  <Step title="Verification">
    The workflow continues until all critical issues are resolved. Claude Code reports completion.
  </Step>
</Steps>

<Tip>
  The `--prompt-only` mode provides Claude Code with token-efficient but
  succinct context about each issue, including file locations, problem
  descriptions, and suggested fixes.
</Tip>

## Optimization tips

### Use prompt-only mode for efficiency

When running CodeRabbit manually before Claude Code, use `--prompt-only` for optimal AI agent integration:

```bash  theme={null}
coderabbit --prompt-only
```

This mode:

* Provides succinct issue context
* Uses token-efficient formatting
* Includes specific file locations and line numbers
* Suggests fix approaches without overwhelming detail

### Configure CodeRabbit for Claude Code

CodeRabbit automatically reads your `claude.md` file, so you can add context there on how code reviews should run, your coding standards, and architectural preferences.

<Info>This is a Pro paid plan feature.</Info>

## Troubleshooting

### CodeRabbit not finding issues

If CodeRabbit isn't detecting expected issues:

1. **Check authentication status**: Run `coderabbit auth status` (authentication improves review quality but isn't required)
2. **Verify git status**: CodeRabbit analyzes tracked changes - check `git status`
3. **Consider review type**: Use the `--type` flag to specify what to review:
   * `coderabbit --type uncommitted` - only uncommitted changes
   * `coderabbit --type committed` - only committed changes
   * `coderabbit --type all` - both committed and uncommitted (default)
4. **Specify base branch**: If your main branch isn't `main`, use `--base`:
   * `coderabbit --base develop`
   * `coderabbit --base master`
5. **Review file types**: CodeRabbit focuses on code files, not docs or configuration

### Claude Code not applying fixes

If Claude Code isn't implementing CodeRabbit's suggestions:

1. **Ensure background execution**: Include "let it run as long as it needs (run it in the background)" in your prompt
2. **Use prompt-only mode**: Ensure you're using `coderabbit --prompt-only` for better AI integration
3. **Provide explicit context**: Tell Claude Code to "fix the issues found by CodeRabbit" explicitly
4. **Check if review finished**: The review may still be running - prompt Claude Code: "Is CodeRabbit finished running?"
5. **Address timeout issues**: If CodeRabbit seems to stop early, prompt Claude to "let CodeRabbit take as long as it takes"

### Managing review duration

CodeRabbit reviews may take 7 to 30+ minutes depending on the scope of changes:

1. **Ensure background execution**: Configure Claude Code to run CodeRabbit in the background so you can continue working
2. **Review smaller changesets**: Adjust what you're reviewing to reduce analysis time:
   * Use `--type uncommitted` to review only uncommitted changes
   * Work on smaller feature branches compared to main
   * Break large features into smaller, reviewable chunks
3. **Configure the diff scope**: Control what changes are analyzed:
   * **Review uncommitted changes only**: Use `--type uncommitted` to analyze just working directory changes
   * **Configure base branch**: Use `--base develop` or `--base main` to set the comparison point
   * **Use feature branches**: Work on focused feature branches instead of large staging branches

<Note>
  The integration creates a more thorough review process than either tool alone.
  Expect comprehensive analysis that catches issues that would otherwise reach
  production.
</Note>
