# TODO

**Need to review all plugins and see if and where they referance ai_docs/ directory as this will may cause plugin
to fail when installed into a new environment outside of this repository. Need to test/validate**

- [ ] `plugins/meta/meta-claude/README.md` Line 65

- [ ] `plugins/meta/meta-claude/skills/agent-creator/SKILL.md` Lines 14, 91 improperlly referances
  ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/command-creator/SKILL.md` Lines 14, 80 improperlly referances
  ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/hook-creator/SKILL.md` Lines 14, 87 improperlly referances
  ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/skill-creator/SKILL.md` Lines 14, 86 improperlly referances
  ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to
  find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by
  intereating the actualy knowledge into the skill.

- [ ] Need a `plugin-creator` skill that will create a new plugin directory structure and files. This will be a simple
  skill that will ask the user for the plugin name, description, category, keywords, and components needed. Then it
  will create the plugin directory structure and files.

- [ ] Need an automated process to update the `ai_docs/README.md` file with the latest information from the official
  Claude Code documentation. Several sub skills relay on this being updated. Goal is to define the URLs that need to
  be scraped in a central location and then the process will scrape the URLs and save to `ai_docs` with proper naming
  and formatting for LLM useage. Firecrawl SDK?

- [ ] Need to complete all TODOs in `plugins/devops/python-uv-tools/skills/python-uv-scripts` directory.
