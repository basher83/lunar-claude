# TODO

**Need to review all plugins and see if and where they referance ai_docs/ directory as this will cause plugin to fail when installed into a new environment outside of this repository.**

- [ ] `plugins/meta/meta-claude/README.md` Line 65

- [ ] `plugins/meta/meta-claude/skills/agent-creator/SKILL.md` Lines 14, 91 improperlly referances ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/command-creator/SKILL.md` Lines 14, 80 improperlly referances ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/hook-creator/SKILL.md` Lines 14, 87 improperlly referances ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by intereating the actualy knowledge into the skill.

- [ ] `plugins/meta/meta-claude/skills/skill-creator/SKILL.md` Lines 14, 86 improperlly referances ai_docs/plugins-referance.md. This will not work because ai_docs/ is not in the plugin root directory. We need to find a way to make this work. Either by adding the ai_docs/ directory to the plugin root directory or by intereating the actualy knowledge into the skill.
