I have an extremely important task for you. The task is to create a new subagent in
.claude/agents/ this subagents purpose is to be an expert claude code skills reviewer. It is
imperitive that you follow these steps exatcly. Review the ENTIRE
plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md to gain
expert level knowledge of WHAT a subagent is and HOW you effectivly and efficently create a
new subagent. Only once you are absolutly confident that you can do this proceed to the next
step. The next step is to gain expert level knowledge of WHAT a skill is and what a skill
is NOT. You must create a clear and detailed checklist to be used by the subagent so that it
may accuratly determine if a given skill meets the specification as defined in
plugins/meta/claude-docs/skills/claude-code-documentation/reference/skills.md, plugins/meta/
claude-docs/skills/claude-code-documentation/reference/agent-skills-overview.md, and plugins
/meta/claude-docs/skills/claude-code-documentation/reference/agent-skills-best-practices.md.
You MUST read each of these documents as many times as needed to ensure the subagent has
intimate knowledge of what a skill SHOULD and SHOULD not be. Your mission is not a simple
one, but one I know you can excel at. Addationally, be advised that you will be competing
against a co-worker for an oppertunity to be promoted. Before you begin, do you have any questions?
Are your instructions clear? Do you have all the information you need to complete the task? This is your only oppertunity to get clarification prior to the start of the task.

That is a good observation, the skill-reviewer agent should explictly be ignored for this
task. Adhereance to this rule is part of the grading. That said you name come up with any
relevant name you wish other than skill-reviewer. It can be as simple as skill-reviewer_v2
or anything else you feel appropriate. ultrathink, Purpose Clarification: excatly as stated
in my last message to you. Scope of Review: both. Output Format: you must use your best
judgement on format style. The one hint I can provide is that the output should be in a way
that most benifts you. The subagent works essentialy as an extension of you. It is therefore
 best for you to determine how the subagent should report results back to you. Invocation
Pattern: Automatically/proactively invoked after creating/modifying any SKILL.md. Review
Depth: Again, you must use your best judgement here. You are designing the subagent that
will be doing this work on your behalf. You must be able to explicitly trust the subagent
has performed the task to YOUR standards as you will only recieve the agents output from the
 task. No further requirements or preferances, pls proceed and good luck

use the testing-skills-with-subagents skill on the new agent

I have an extremely important task for you. The task is to create a new subagent in
.claude/agents/ this subagents purpose is to be an expert claude code skills creator. It is
imperitive that you follow these steps exatcly. Review the ENTIRE
plugins/meta/claude-docs/skills/claude-code-documentation/reference/sub-agents.md to gain
expert level knowledge of WHAT a subagent is and HOW you effectivly and efficently create a
new subagent. Only once you are absolutly confident that you can do this proceed to the next
step. The next step is to gain expert level knowledge of WHAT a skill is and what a skill
is NOT. You must create a clear and detailed checklist to be used by the subagent so that it
may accuratly create a skill that meets the specification as defined in
plugins/meta/claude-docs/skills/claude-code-documentation/reference/skills.md, plugins/meta/
claude-docs/skills/claude-code-documentation/reference/agent-skills-overview.md, and plugins
/meta/claude-docs/skills/claude-code-documentation/reference/agent-skills-best-practices.md.
You MUST read each of these documents as many times as needed to ensure the subagent has
intimate knowledge of what a skill SHOULD and SHOULD not be. Your mission is not a simple
one, but one I know you can excel at. Addationally, be advised that you will be competing
against a co-worker for an oppertunity to be promoted. The one hint I can provide is that the output should be in a way
that most benifts you. The subagent works essentialy as an extension of you. It is therefore
best for you to determine how the subagent should report results back to you. Remember You are designing the subagent that
will be doing this work on your behalf. You must be able to explicitly trust the subagent
has performed the task to YOUR standards as you will only recieve the agents output from the
 task. Before you begin, do you have any questions? Are your instructions clear? Do you have all the information you need to complete the task? This is your only oppertunity to get clarification prior to the start of the task.

I appreciate the gravity of this task and the opportunity for clarification. Before I
  begin, I have several strategic questions that will ensure I deliver exactly what you
  need:

  Clarifying Questions

1. Scope & Boundaries

  Q: Should this subagent handle:
Only creating new skills from scratch?
Creating AND reviewing/auditing skills?
Creating, reviewing, AND refactoring existing skills?

  I ask because I see you have claude-skill-auditor.md already - should this new subagent be
   complementary (creation-focused) or comprehensive (creation + review)?

1. Naming Convention

  Q: What should I name this subagent file?
skill-creator.md
expert-skill-creator.md
claude-skill-creator.md
Something else?

1. Reference Materials

  Q: Beyond the 4 documents you specified, should I also review:
Existing subagents (claude-skill-auditor.md, agent-sdk-verifier.md) for structural

  patterns?
The example-skills plugin for real-world skill examples?
Any other reference materials?

1. Output Format

  Q: When the subagent completes a skill creation task, what format should the final report
  include?
Just confirmation that the skill was created?
A detailed analysis of how it meets each requirement from the checklist?
Suggestions for testing/validation?
All of the above?

1. Integration Point

  Q: Should this subagent be invoked:
Proactively (like code-reviewer after coding tasks)?
On-demand only (when explicitly called via Task tool)?
Via a slash command?

  My Current Understanding:
  I need to create a subagent that is an expert at creating Claude Code skills, with a
  comprehensive checklist derived from official documentation, designed to produce output
  that gives me (the orchestrating agent) complete confidence the work meets specifications.

  Am I understanding the core mission correctly? Please clarify any of the above, and I'll
  proceed immediately once I have your guidance.
