# TODO

**Need to review all plugins and see if and where they referance ai_docs/ directory as this will may cause plugin
to fail when installed into a new environment outside of this repository. Need to test/validate**

- [ ] `plugins/meta/meta-claude/README.md` Line 66 - References `ai_docs/` directory

- [ ] `plugins/meta/meta-claude/skills/agent-creator/SKILL.md` Lines 15, 95 - Improperly references
  `ai_docs/plugins-referance.md`. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  integrating the actual knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/command-creator/SKILL.md` Lines 15, 83 - Improperly references
  `ai_docs/plugins-referance.md`. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  integrating the actual knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/hook-creator/SKILL.md` Lines 16, 91 - Improperly references
  `ai_docs/plugins-referance.md`. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  integrating the actual knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/skill-creator/SKILL.md` - **File does not exist** in this location. Only exists
  in `examples/skills/skill-creator/SKILL.md`. Need to either create it in the plugin directory or remove this todo if
  not needed. If created, it should not reference `ai_docs/plugins-referance.md` as it will not work because ai_docs/
  is not in the plugin root directory.

- [ ] Need a `plugin-creator` skill that will create a new plugin directory structure and files. This will be a simple
  skill that will ask the user for the plugin name, description, category, keywords, and components needed. Then it
  will create the plugin directory structure and files. **Note:** A `/new-plugin` command exists, but no plugin-creator
  skill exists yet.

- [X] Need an automated process to update the `ai_docs/README.md` file with the latest information from the official
  Claude Code documentation. Several sub skills relay on this being updated. Goal is to define the URLs that need to
  be scraped in a central location and then the process will scrape the URLs and save to `ai_docs` with proper naming
  and formatting for LLM useage. Firecrawl SDK?

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/patterns/system-automation.md` (line 53).
  Expand to include: Complete psutil monitoring patterns, safe subprocess execution, SSH automation patterns

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/patterns/security-patterns.md` (line 24).
  Expand to include: Complete Infisical integration patterns, best practices for secret rotation, multi-environment
  secret management

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/patterns/data-processing.md` (line 46).
  Expand to include: Complete Polars patterns, performance optimization techniques, large file processing strategies

- [ ] Complete TODO in
  `plugins/devops/python-tools/skills/python-uv-scripts/reference/dependency-management.md` (line 55).
  Expand to include: Complete version specifier syntax, dependency resolution strategies, security scanning integration

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/workflows/team-adoption.md` (line 50).
  Expand to include: Detailed training materials, complete adoption roadmap, team communication templates

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/workflows/testing-strategies.md` (line 64).
  Expand to include: Complete testing patterns, mocking external dependencies, test organization strategies

- [ ] Complete TODO in `plugins/devops/python-tools/skills/python-uv-scripts/workflows/ci-cd-integration.md` (line 59).
  Expand to include: Complete GitHub Actions examples, GitLab CI patterns, pre-commit hook configurations
