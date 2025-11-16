# Brainstorming for a create-review-validate cycle for the meta-Claude plugin

## Overview

The create-review-validate cycle is a process for creating, reviewing, and validating Claude Code components. It is a way to ensure that the components are created correctly and are compliant with the official specifications. This should be an orchestrated effort across slash commands and agents as well as skills within the meta-Claude plugin itself. This way a user can simply say "let's create a new skill" and there will be predefined actions that can occur to create review and validate the skill. For the skill example we should be able to point to specific research that's already been done within the repo or provide a sentence or two that can induce a research workflow to gather the appropriate context for the skill that the user is looking to implement.

## Example Workflow #1

1. User requests to create a new coderabbit skill.
2. User has already conducted research and has moved the research to the [claude-dev-sandbox](../plugins/meta/claude-dev-sandbox) plugin. In this case research is located in `plugins/meta/claude-dev-sandbox/skills/coderabbit/`
3. A scout agent should be dispatched to `plugins/meta/claude-dev-sandbox/skills/coderabbit/` to gather what is contained within the provided directory.
4. Now that the main agent has context of what is available in the directory, the agent needs to load the skill-creator skill to create the skill.
   - Can we delegate this to a subagent? Can subagents load skills? I think yes but need to verify with multi-agent composition skill. If we can't delegate this to a subagent, we can use the skill-creator skill directly.
5. Skill is created by either delegating to a subagent or directly using the skill-creator skill.
6. Skill is reviewed
7. Skill is validated

## Example Workflow #2

1. User requests to create a new coderabbit skill.
2. User has NOT conducted research and wants to create a new skill from scratch.
3. A mini brainstorming workflow should occur to gather the requirements and intentionsfor the skill.
4. Once the scope of the skill is defined, then kick off a research workflow to utilize some helper scripts to research the internet and scrape documentation. A specific to creating the skill should output this into the Research sub-directory as a start point for gathering research materials.
5. Once the research materials are brought into the research sub-directory, an initial review of the results should occur to start a planning phase for restructuring and formatting of the data into a skill format. This could be a good Scout agent task.
6. Conduct the initial formatting and cleaning of the data. This doesn't need to be super in-depth but at least getting it close to good prior to kicking off the skill creation itself.
7. Kick off the skill creation workflow. Skill is created by either delegating to a subagent or directly using the skill-creator skill.
8. Skill is reviewed
9. Skill is validated

## Planning

- [ ] Start with primitives. Create distinct prompts (a.k.a. slash commands) for each phase.
- [ ] Review and identify which prompts or slash commands can be delegated to a sub-agent to increase the efficiency of the workflow
- [ ] Review and identify if any scripts are needed for hooks or anything of that nature, helper scripts, to assist in the entire workflow for the plugin
