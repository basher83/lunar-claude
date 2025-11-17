---
description: Fully automated research gathering for skill creation
argument-hint: skill-name [sources]
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Skill Research

Gather research materials for skill creation with intelligent automation.

## Purpose

Automate the research phase of skill creation by:

- Selecting appropriate research tools based on context
- Executing research scripts with correct parameters
- Organizing research into skill-specific directories
- Providing clean, attributed source materials for skill authoring

## Inputs

Parse arguments from `$ARGUMENTS`:

- **Required:** `skill-name` - Name of skill being researched (kebab-case)
- **Optional:** `sources` - URLs, keywords, or categories to research

## Research Script Selection

Choose the appropriate research script based on input context:

### 1. If User Provides Specific URLs

When `sources` contains one or more URLs (http/https):

```bash
scripts/firecrawl_scrape_url.py "<url>" --output "docs/research/skills/<skill-name>/<filename>.md"
```

Run for each URL provided.

### 2. If Researching Claude Code Patterns

When skill relates to Claude Code functionality (skills, commands, agents,
hooks, plugins, MCP):

Ask user to confirm if this is about Claude Code:

```text
This appears to be related to Claude Code functionality.
Use official Claude Code documentation? [Yes/No]
```

If yes:

```bash
scripts/jina_reader_docs.py --output-dir "docs/research/skills/<skill-name>"
```

### 3. General Topic Research (Default)

For all other cases, use Firecrawl web search with intelligent category selection.

First, conduct a mini brainstorm with the user to refine scope:

```text
Let's refine the research scope for "<skill-name>":

1. What specific aspects should we focus on?
2. Which categories are most relevant?
   - github (code examples, repositories)
   - research (academic papers, technical articles)
   - pdf (documentation, guides)
   - web (general web content - default)

3. Any specific keywords or search terms to include?
```

Then execute:

```bash
scripts/firecrawl_sdk_research.py "<query>" \
  --limit <num-results> \
  --category <category> \
  --output "docs/research/skills/<skill-name>/research.md"
```

**Default parameters:**

- `limit`: 10 (adjustable based on scope)
- `category`: Based on user input or omit for general web search
- `query`: Skill name + refined keywords from brainstorm

## Output Directory Management

All research saves to: `docs/research/skills/<skill-name>/`

**If custom path provided via --output-dir flag:**

Use custom path instead of default location.

Parse flags from `$ARGUMENTS`:

```text
/skill-research coderabbit --output-dir plugins/meta/claude-dev-sandbox/skills/coderabbit/research
```

## Execution Process

### Step 1: Parse Arguments

Extract skill name and sources from `$ARGUMENTS`:

- Split arguments by space
- First argument: skill name (required)
- Remaining arguments: sources (optional)
- Check for `--output-dir` flag and extract custom path if present

**Validation:**

- Skill name must be kebab-case (lowercase with hyphens)
- Skill name cannot be empty
- If custom output path, verify parent directory exists

### Step 2: Determine Research Strategy

Analyze sources to select script:

```text
If sources contain URLs (starts with http:// or https://):
  → Use firecrawl_scrape_url.py for each URL

Else if skill-name matches Claude Code patterns:
  (Contains: skill, command, agent, hook, plugin, mcp, slash, subagent)
  → Ask user if they want official Claude Code docs
  → If yes: Use jina_reader_docs.py

Else:
  → Use firecrawl_sdk_research.py with brainstorm
```

### Step 3: Create Output Directory

```bash
mkdir -p "docs/research/skills/<skill-name>"
```

Or use custom path if `--output-dir` provided.

### Step 4: Execute Research Script

Run selected script with appropriate parameters based on selection logic.

**Environment check:**

Before running Firecrawl scripts, verify API key:

```bash
if [ -z "$FIRECRAWL_API_KEY" ]; then
  echo "Error: FIRECRAWL_API_KEY environment variable not set"
  echo "Set it with: export FIRECRAWL_API_KEY='fc-your-api-key'"
  exit 1
fi
```

**Script execution patterns:**

**For URL scraping:**

```bash
for url in $urls; do
  filename=$(echo "$url" | sed 's|https\?://||' | sed 's|/|-|g' | cut -c1-50)
  scripts/firecrawl_scrape_url.py "$url" \
    --output "docs/research/skills/<skill-name>/${filename}.md"
done
```

**For Claude Code docs:**

```bash
scripts/jina_reader_docs.py \
  --output-dir "docs/research/skills/<skill-name>"
```

**For general research:**

```bash
scripts/firecrawl_sdk_research.py "$query" \
  --limit $limit \
  --category $category \
  --output "docs/research/skills/<skill-name>/research.md"
```

### Step 5: Verify Research Output

Check that research files were created:

```bash
ls -lh "docs/research/skills/<skill-name>/"
```

Display summary:

```text
✓ Research completed for <skill-name>

Output directory: docs/research/skills/<skill-name>/
Files created: X files
Total size: Y KB

Research materials ready for formatting and skill creation.

Next steps:
  1. Review research materials
  2. Run: /skill-format docs/research/skills/<skill-name>
  3. Run: /skill-create <skill-name> docs/research/skills/<skill-name>
```

## Error Handling

### Missing FIRECRAWL_API_KEY

```text
Error: FIRECRAWL_API_KEY environment variable not set.

Firecrawl research scripts require an API key.

Set it with:
  export FIRECRAWL_API_KEY='fc-your-api-key'

Get your API key from: https://firecrawl.dev

Alternative: Use manual research and skip this step.
```

Exit with error code 1.

### Script Execution Failures

If research script fails:

```text
Error: Research script failed with exit code X

Script: <script-name>
Command: <full-command>
Error output: <stderr>

Troubleshooting:
  - Verify API key is valid
  - Check network connectivity
  - Verify script permissions (chmod +x)
  - Review script output above for specific errors

Research failed. Fix the error and try again.
```

Exit with error code 1.

### Invalid Skill Name

```text
Error: Invalid skill name format: <skill-name>

Skill names must:
  - Use kebab-case (lowercase with hyphens)
  - Contain only letters, numbers, and hyphens
  - Not start or end with hyphens
  - Not contain consecutive hyphens

Examples:
  ✓ docker-compose-helper
  ✓ git-workflow-automation
  ✗ DockerHelper (use docker-helper)
  ✗ git__workflow (no consecutive hyphens)

Please provide a valid skill name.
```

Exit with error code 1.

### No Sources Provided for URL Scraping

If user provides no sources but you detect they want URL scraping:

```text
No URLs provided for research.

Usage:
  /skill-research <skill-name> <url1> [url2] [url3]

Example:
  /skill-research docker-best-practices https://docs.docker.com/develop/dev-best-practices/

Or run without URLs for general web research:
  /skill-research docker-best-practices
```

Exit with error code 1.

## Examples

### Example 1: General Research with Defaults

User invocation:

```bash
/skill-research ansible-vault-security
```

Process:

1. Detect no URLs, not Claude Code specific
2. Mini brainstorm with user about scope
3. Execute firecrawl_sdk_research.py:

   ```bash
   scripts/firecrawl_sdk_research.py \
     "ansible vault security best practices" \
     --limit 10 \
     --output docs/research/skills/ansible-vault-security/research.md
   ```

4. Display summary with next steps

### Example 2: Scraping Specific URLs

User invocation:

```bash
/skill-research terraform-best-practices \
  https://developer.hashicorp.com/terraform/tutorials \
  https://spacelift.io/blog/terraform-best-practices
```

Process:

1. Detect URLs in arguments
2. Create output directory: `docs/research/skills/terraform-best-practices/`
3. Scrape each URL:
   - `developer-hashicorp-com-terraform-tutorials.md`
   - `spacelift-io-blog-terraform-best-practices.md`
4. Display summary with file list

### Example 3: Claude Code Documentation

User invocation:

```bash
/skill-research skill-creator-advanced
```

Process:

1. Detect "skill" in name, matches Claude Code pattern
2. Ask: "This appears to be related to Claude Code functionality. Use
   official Claude Code documentation? [Yes/No]"
3. User: Yes
4. Execute: `scripts/jina_reader_docs.py --output-dir docs/research/skills/skill-creator-advanced`
5. Display summary with downloaded docs list

### Example 4: Custom Output Directory

User invocation:

```bash
/skill-research coderabbit --output-dir plugins/meta/claude-dev-sandbox/skills/coderabbit/research
```

Process:

1. Parse `--output-dir` flag and extract custom path
2. Verify parent directory exists: `plugins/meta/claude-dev-sandbox/skills/coderabbit/`
3. Create research directory: `plugins/meta/claude-dev-sandbox/skills/coderabbit/research/`
4. Execute general research (no URLs, not Claude Code specific)
5. Save to custom path instead of default `docs/research/skills/`

### Example 5: Research with Category Filtering

User invocation:

```bash
/skill-research machine-learning-pipelines
```

Process:

1. Mini brainstorm reveals focus on academic research papers
2. User selects category: `research`
3. Execute firecrawl_sdk_research.py:

   ```bash
   scripts/firecrawl_sdk_research.py \
     "machine learning pipelines" \
     --limit 10 \
     --category research \
     --output docs/research/skills/machine-learning-pipelines/research.md
   ```

4. Display summary

## Success Criteria

Research is successful when:

1. Research scripts execute without errors
2. Output directory contains research files
3. Files are non-empty and contain markdown content
4. Summary displays file count and total size
5. Next steps guide user to formatting and creation phases

## Exit Codes

- **0:** Success - research completed and saved
- **1:** Failure - invalid input, missing API key, script errors, or execution failures
