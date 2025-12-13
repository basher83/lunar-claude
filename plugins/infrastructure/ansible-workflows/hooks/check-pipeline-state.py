#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Stop hook for ansible-workflows pipeline.

Blocks session stop when an active pipeline exists.
Provides guidance for continuing the pipeline.
"""

import json
import os
import sys
from pathlib import Path

# Gitignore patterns for ansible-workflows state files
GITIGNORE_PATTERNS = """\
# Ansible Workflows plugin state (auto-added)
.claude/ansible-workflows.local.md
.claude/ansible-workflows.*.bundle.md
"""


def ensure_gitignore(project_dir: Path) -> None:
    """Ensure project .gitignore contains ansible-workflows patterns."""
    gitignore_path = project_dir / ".gitignore"
    marker = "ansible-workflows.local.md"

    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if marker in content:
            return  # Already configured
        # Append patterns
        with gitignore_path.open("a") as f:
            f.write("\n" + GITIGNORE_PATTERNS)
    else:
        # Create new .gitignore
        gitignore_path.write_text(GITIGNORE_PATTERNS)


# Phase to next agent mapping
PHASE_NEXT_AGENT = {
    "scaffolding": "ansible-generator",
    "generating": "ansible-validator",
    "validating": "ansible-reviewer",  # or ansible-debugger if failed
    "debugging": "ansible-validator",
    "reviewing": None,  # Complete or needs rework
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    try:
        end_idx = content.index("---", 3)
        frontmatter_text = content[3:end_idx].strip()
        body = content[end_idx + 3 :].strip()

        frontmatter = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                elif value.isdigit():
                    value = int(value)
                frontmatter[key] = value

        return frontmatter, body
    except ValueError:
        return {}, content


def main() -> None:
    """Process Stop hook event."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Get project directory
    cwd = hook_input.get("cwd", os.getcwd())
    project_dir = Path(cwd)

    # State file location
    state_file = project_dir / ".claude" / "ansible-workflows.local.md"

    # No state file = no active pipeline
    if not state_file.exists():
        print(json.dumps({}))
        return

    # Read state
    state_content = state_file.read_text()
    state, _ = parse_frontmatter(state_content)

    # Check if pipeline is active
    if not state.get("active", False):
        print(json.dumps({}))
        return

    # Ensure gitignore is configured for state files
    ensure_gitignore(project_dir)

    # Active pipeline - block stop
    current_phase = state.get("pipeline_phase", "unknown")
    target_path = state.get("target_path", "unknown")
    validation_attempts = state.get("validation_attempts", 0)
    last_passed = state.get("last_validation_passed", True)

    # Determine next agent
    if current_phase == "validating" and not last_passed:
        next_agent = "ansible-debugger"
    else:
        next_agent = PHASE_NEXT_AGENT.get(current_phase, "unknown")

    # Check for max retries exceeded
    if validation_attempts >= 3 and not last_passed:
        result = {
            "decision": "block",
            "reason": f"""[ansible-workflows] Pipeline stalled after {validation_attempts} validation attempts.

Target: {target_path}
Phase: {current_phase}

Options:
1. Review errors manually and fix
2. Set 'active: false' in .claude/ansible-workflows.local.md to abort
3. Continue with ansible-debugger for another attempt""",
        }
        print(json.dumps(result))
        return

    # Normal case - active pipeline, prompt to continue
    result = {
        "decision": "block",
        "reason": f"""[ansible-workflows] Active pipeline detected - cannot stop session.

Target: {target_path}
Current phase: {current_phase}
Next agent: {next_agent}

To continue the pipeline:
  Dispatch the {next_agent} agent with context from bundle files.
  Read .claude/ansible-workflows.*.bundle.md for handoff context.

To abort the pipeline:
  Set 'active: false' in .claude/ansible-workflows.local.md""",
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
