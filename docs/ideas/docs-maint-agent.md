# Building a Documentation Maintenance Agent with Claude Agent SDK in Python

Given your Python background and specific requirements, here's a comprehensive approach to
building an automated GitHub documentation maintenance agent using the Claude Agent SDK.

## **Recommended Architecture: Multi-Agent Orchestration Pattern**

For your use case, you should implement a **multi-agent orchestration workflow** where a main
orchestrator delegates specialized tasks to subagents. This approach achieves 90.2% better
performance compared to single-agent systems and prevents context pollution.[^1][^2]

### **Your Workflow Structure:**

**Orchestrator Agent** → Coordinates the overall documentation review process
**Subagent 1: Markdown Linter** → Validates and fixes markdown syntax
**Subagent 2: Link Validator** → Checks internal and external links
**Subagent 3: Grammar Checker** → Reviews content for grammar and clarity
**Subagent 4: Content Analyzer** → Identifies knowledge gaps and ensures completeness

## **Implementation Approach**

### **Step 1: Set Up Your Python Environment**

```python
# Install required dependencies
pip install claude-agent-sdk
npm install -g @anthropic-ai/claude-code
```

### **Step 2: Core Implementation with Python SDK**

Based on the official Python SDK documentation, here's your baseline implementation:[^3][^4]

```python
import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def documentation_maintenance_agent(repo_path: str):
    """
    Main orchestrator for documentation maintenance
    """
    options = ClaudeAgentOptions(
        cwd=repo_path,
        allowed_tools=["Read", "Write", "Grep", "Glob", "Bash"],
        permission_mode='requestPermission',  # Human-in-the-loop for safety
        max_turns=10,
        system_prompt="""You are a documentation maintenance specialist.
        Your responsibilities:
        1. Lint all markdown files and fix syntax errors
        2. Validate all links (internal and external)
        3. Review grammar and clarity
        4. Identify documentation gaps for the repository

        Coordinate with specialized subagents for each task.""",
        agents=[
            {
                "name": "markdown-linter",
                "description": "Validates and auto-fixes markdown syntax issues",
                "system_prompt": "Fix markdown formatting errors, ensure consistent styling",
                "allowed_tools": ["Read", "Write", "Grep"]
            },
            {
                "name": "link-validator",
                "description": "Checks all markdown links for validity",
                "system_prompt": "Validate internal file links and external URLs, report broken links",
                "allowed_tools": ["Read", "Bash", "WebFetch"]
            },
            {
                "name": "grammar-reviewer",
                "description": "Reviews documentation for grammar and clarity",
                "system_prompt": "Check grammar, spelling, tone, and readability. Suggest improvements",
                "allowed_tools": ["Read"]
            },
            {
                "name": "content-analyzer",
                "description": "Identifies documentation completeness and gaps",
                "system_prompt": "Analyze repo structure and docs to find missing documentation",
                "allowed_tools": ["Read", "Grep", "Glob", "Bash"]
            }
        ]
    )

    prompt = """
    Review all markdown documentation in this repository:
    1. Find all .md files
    2. Run markdown linting and fix errors
    3. Validate all links (internal and external)
    4. Check grammar and writing quality
    5. Identify any documentation gaps based on the codebase

    Create a detailed report with findings and auto-fix what you can.
    """

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

# Run the agent
asyncio.run(documentation_maintenance_agent("/path/to/your/repo"))
```

### **Step 3: Integrate MCP Servers for Specialized Tools**

The Claude Agent SDK supports Model Context Protocol (MCP) for extending capabilities. You
should integrate specialized MCP servers for markdown linting:[^5][^6]

**Markdown Linting MCP Server**:[^6][^7][^5]

- Auto-fixes 30 out of 52 markdownlint rules
- Validates against CommonMark and GitHub Flavored Markdown
- Provides detailed error reporting

**Setup:**

```python
options = ClaudeAgentOptions(
    mcp_config="/path/to/mcp-config.json",
    # ... other options
)
```

**MCP Configuration** (`mcp-config.json`):

```json
{
  "mcpServers": {
    "markdownlint": {
      "command": "npx",
      "args": ["markdownlint-mcp-server"]
    }
  }
}
```

### **Step 4: GitHub Actions Integration**

For automated, continuous documentation maintenance, integrate with GitHub Actions:[^8][^9]

```yaml
# .github/workflows/doc-maintenance.yml
name: Documentation Maintenance

on:
  pull_request:
    paths:
      - '**.md'
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  maintain-docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          pip install claude-agent-sdk
          npm install -g @anthropic-ai/claude-code

      - name: Run documentation agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/doc_maintenance_agent.py

      - name: Create PR with fixes
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "docs: automated documentation maintenance"
          branch: docs/automated-fixes
          title: "Automated Documentation Improvements"
          body: "Auto-generated documentation fixes by Claude Agent"
```

## **Best Practices for Your Implementation**

### **1. Use Filesystem-Based Agent Configuration**[^2]

Store your subagent configurations in `.claude/agents/` for easier maintenance:

```text
.claude/
├── agents/
│   ├── markdown-linter.md
│   ├── link-validator.md
│   ├── grammar-reviewer.md
│   └── content-analyzer.md
├── settings.json
└── CLAUDE.md
```

**Example subagent file** (`.claude/agents/markdown-linter.md`):

```markdown
---
name: markdown-linter
description: Validates and auto-fixes markdown syntax issues
allowedTools:
  - Read
  - Write
  - Grep
---

You are a markdown linting specialist. Your job is to:
- Identify markdown syntax errors
- Fix formatting inconsistencies
- Ensure adherence to CommonMark standards
- Apply consistent styling across all documents
```

### **2. Implement Validation Hooks**[^10][^11]

Use hooks for automated validation before committing changes:

```json
// .claude/settings.json
{
  "hooks": {
    "beforeWrite": "npm run lint:markdown",
    "afterWrite": "git diff --stat"
  }
}
```

### **3. Leverage Parallel Subagent Execution**[^1][^2]

Run independent validation tasks in parallel for faster processing:

```python
# The SDK handles parallel execution automatically when subagents
# don't have dependencies on each other
options = ClaudeAgentOptions(
    agents=[
        # These will run in parallel when possible
        {"name": "markdown-linter", ...},
        {"name": "link-validator", ...},
        {"name": "grammar-reviewer", ...}
    ]
)
```

### **4. Maintain Separate Context Windows**[^2][^1]

Each subagent gets its own 200K token context window, preventing context pollution when
analyzing large documentation sets. The orchestrator maintains global state while subagents work
independently.

## **Tools and Integrations**

### **Markdown Validation Tools**

**markdownlint-mcp**: MCP server providing linting and auto-fix capabilities[^5][^6]
**markdown-link-validator**: CLI tool for validating internal and external links[^12]
**next-validate-link**: Automatic link checking with URL fragment validation[^13]

### **Grammar and Style Checking**

Since you're working in Python, integrate AI-powered grammar checking through the agent's
natural language capabilities rather than external tools. Claude Sonnet 4.5 has strong grammar
and writing quality analysis built-in.[^14][^15]

### **Link Validation Strategy**

For link validation, use a combination approach:

1. **Internal links**: Use filesystem tools (Read, Grep, Glob) to verify file
   existence[^12]
2. **External links**: Use WebFetch tool or Bash with curl to check HTTP status
   codes[^16][^17]
3. **GitHub Actions integration**: Run `gaurav-nelson/github-action-markdown-link-check` for
   automated CI/CD validation[^17][^18]

## **Production Deployment Strategy**

### **Phase 1: Manual Execution** (Week 1-2)

Run the agent locally on your repos, review outputs, and refine prompts based on results.

### **Phase 2: Scheduled Automation** (Week 3-4)

Deploy GitHub Actions workflow with weekly scheduled runs, generating PR reports for human review.

### **Phase 3: Event-Driven Automation** (Week 5+)

Trigger on PR events for real-time documentation validation, with auto-approval for low-risk
fixes (markdown linting) and human review for content changes.[^9][^8]

## **Human-in-the-Loop Considerations**

Keep humans involved for critical decisions:[^19][^20]

- **Auto-approve**: Markdown syntax fixes, whitespace cleanup, link formatting
- **Require review**: Grammar changes, content rewrites, structural reorganization
- **Flag for attention**: Missing documentation sections, broken external links

Set `permission_mode='requestPermission'` for changes requiring human approval, or use
`'acceptEdits'` for automated fixes.[^4][^3]

## **Cost and Performance Optimization**

**Use tiered models**:[^1]

- Orchestrator: Claude Opus 4 for strategic planning
- Subagents: Claude Sonnet 4 for specific tasks (40-60% cost reduction)

**Implement context compaction**:[^10]
The SDK automatically summarizes and compacts context to prevent token overflow during long-running sessions.

**Monitor with analytics**:[^21]
Integrate MLflow or similar tools to track agent performance, success rates, and identify optimization opportunities.

## **Example Output Structure**

Your agent should generate structured reports:

```markdown
# Documentation Maintenance Report
Generated: 2025-10-24

## Markdown Linting Results
- **Files processed**: 23
- **Issues found**: 47
- **Auto-fixed**: 42
- **Requires review**: 5

## Link Validation
- **Total links**: 156
- **Valid**: 148
- **Broken**: 8 (see details below)

## Grammar and Clarity
- **Files reviewed**: 23
- **Suggestions**: 31
- **Critical**: 3
- **Minor**: 28

## Documentation Gaps
- Missing: API reference for `/auth` endpoint
- Incomplete: Installation instructions for Windows
- Outdated: Deployment guide (references v1.2, current is v2.1)
```

This comprehensive approach leverages the Claude Agent SDK's strengths in Python, uses proven
multi-agent patterns, and provides a scalable foundation for maintaining documentation across
multiple repositories.[^22][^15][^11][^10][^2]
<span style="display:none">
[^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45]
[^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68]
[^69][^70][^71][^72][^73]
</span>

<div align="center">⁂</div>

[^1]: <https://www.cursor-ide.com/blog/claude-subagents>

[^2]: <https://docs.claude.com/en/api/agent-sdk/subagents>

[^3]: <https://github.com/anthropics/claude-agent-sdk-python>

[^4]: <https://docs.claude.com/en/api/agent-sdk/python>

[^5]: <https://mcpmarket.com/server/markdownlint>

[^6]: <https://github.com/ernestgwilsonii/markdownlint-mcp>

[^7]: <https://mcp.aibase.com/server/1917147567886102530>

[^8]: <https://docs.claude.com/en/docs/claude-code/github-actions>

[^9]: <https://github.com/anthropics/claude-code-action>

[^10]: <https://joshuaberkowitz.us/blog/news-1/claude-agent-sdk-revolutionizes-automation-for-developers-1295>

[^11]: <https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/>

[^12]: <https://github.com/webhintio/markdown-link-validator>

[^13]: <https://next-validate-link.vercel.app>

[^14]: <https://www.agenticfirst.ai/blog/ai-agent-for-github-documentation>

[^15]: <https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk>

[^16]: <https://duncant.co.uk/tools/link-checker>

[^17]: <https://blog.mdconvrt.com/enhancing-project-quality-automating-markdown-link-checks-with-gaurav-nelson-github-action-markdown-link-check/>

[^18]: <https://geoffhudik.com/tech/2020/10/05/automate-checking-markdown-links-with-github-actions/>

[^19]: <https://www.youtube.com/watch?v=DqzG-XNjV3M>

[^20]: <https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf>

[^21]: <https://mlflow.org/blog/mlflow-autolog-claude-agents-sdk>

[^22]: <https://blog.promptlayer.com/building-agents-with-claude-codes-sdk/>

[^23]: <https://tartansandal.github.io/vim/markdown/remark/2021/10/05/vim-remark.html>

[^24]: <https://techcommunity.microsoft.com/blog/educatordeveloperblog/docaider-automated-documentation-maintenance-for-open-source-github-repositories/4245588>

[^25]: <https://www.youtube.com/watch?v=NfgYfqQBc_8>

[^26]: <https://docs.claude.com/en/api/agent-sdk/overview>

[^27]: <https://earthly.dev/blog/markdown-lint/>

[^28]: <https://bestaiagents.ai/agent/dosu>

[^29]: <https://www.anthropic.com/news/skills>

[^30]: <https://github.com/funbox/markdown-lint>

[^31]: <https://aiagentstore.ai/ai-agent/dosu>

[^32]: <https://www.reddit.com/r/ClaudeAI/comments/1nwuzyq/tutorial_heres_how_to_create_agents_with_claude/>

[^33]: <https://github.com/DavidAnson/markdownlint/issues/80>

[^34]: <https://github.com/OpenBMB/RepoAgent>

[^35]: <https://keptn.sh/stable/docs/contribute/docs/markdownlint/>

[^36]: <https://github.com/PrefectHQ/ControlFlow>

[^37]: <https://stevekinney.com/courses/ai-development/integrating-with-github-actions>

[^38]: <https://github.com/barnett617/markdownlint-mcp-server>

[^39]: <https://www.llamaindex.ai/blog/automate-workflows-with-document-agents-a-complete-tutorial-to-building-context-aware-AI>

[^40]: <https://docs.langchain.com/oss/python/langgraph/workflows-agents>

[^41]: <https://textlint.org/docs/mcp/>

[^42]: <https://langchain-ai.github.io/langgraph/tutorials/workflows/>

[^43]: <https://github.com/anthropics/claude-agent-sdk-demos>

[^44]: <https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/>

[^45]: <https://github.com/openai/openai-agents-python>

[^46]: <https://www.reddit.com/r/aiagents/comments/1nuh1kq/claude_agent_sdk_build_ai_agents_that_actually/>

[^47]: <https://lobehub.com/mcp/thornzero-mcp-server-go>

[^48]: <https://www.aitopia.ai/grammar-checker/>

[^49]: <https://www.jotform.com/ai/best-ai-grammar-checker/>

[^50]: <https://quillbot.com/grammar-check>

[^51]: <https://zapier.com/blog/best-ai-grammar-checker-rewording-tool/>

[^52]: <https://wiki.rusefi.com/HOWTO-validate-links/>

[^53]: <https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/>

[^54]: <https://www.grammarly.com/grammar-check>

[^55]: <https://www.arsturn.com/blog/getting-started-with-the-claude-code-sdk-to-orchestrate-multiple-ai-instances>

[^56]: <https://www.trinka.ai>

[^57]: <https://github.com/wshobson/agents>

[^58]: <https://www.grammarly.com/ai-agents>

[^59]: <https://www.flowforma.com/blog/document-workflow-automation>

[^60]: <https://shipyard.build/blog/your-first-python-github-action/>

[^61]: <https://www.youtube.com/watch?v=i6N8oQQ0tUE>

[^62]: <https://www.signwell.com/resources/document-automaton/>

[^63]: <https://dev.to/dineshsonachalam/a-github-action-that-automatically-generates-updates-markdown-content-like-your-readme-md-from-external-or-remote-files-hp7>

[^64]: <https://www.secoda.co/learn/best-practices-in-automated-documentation>

[^65]: <https://stackoverflow.com/questions/67507373/how-to-attach-a-markdown-page-to-github-actions-workflow-run-summary>

[^66]: <https://www.datacamp.com/tutorial/how-to-use-claude-agent-sdk>

[^67]: <https://www.marconet.com/blog/expert-tips-for-implementing-document-automation>

[^68]: <https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions>

[^69]: <https://www.reddit.com/r/BusinessIntelligence/comments/1msp3e9/how_do_you_even_start_with_automating_internal/>

[^70]: <https://www.reddit.com/r/LocalLLaMA/comments/1dedy61/i_am_building_a_tool_to_create_agents_in_a/>

[^71]: <https://www.irisglobal.com/blog/document-workflow-automation-checklist/>

[^72]: <https://github.com/openai/agents.md>

[^73]: <https://thedigitalprojectmanager.com/topics/best-practices/document-management-workflow/>
