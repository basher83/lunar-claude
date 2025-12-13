#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""SubagentStop hook for ansible-workflows pipeline.

Validates per-agent completion and updates pipeline state.
Runs when any subagent considers stopping.
"""

import json
import os
import sys
from datetime import UTC, datetime
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


# Pipeline phase transitions based on agent completion
AGENT_PHASE_MAP = {
    "ansible-generator": ("generating", "validating"),
    "ansible-validator": ("validating", None),  # Next phase depends on result
    "ansible-debugger": ("debugging", "validating"),
    "ansible-reviewer": ("reviewing", None),  # Complete or needs rework
}

# Expected bundle files per agent
AGENT_BUNDLES = {
    "ansible-generator": ".generating.bundle.md",
    "ansible-validator": ".validating.bundle.md",
    "ansible-debugger": ".debugging.bundle.md",
    "ansible-reviewer": None,  # Reviewer doesn't write bundles
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    try:
        end_idx = content.index("---", 3)
        frontmatter_text = content[3:end_idx].strip()
        body = content[end_idx + 3:].strip()

        # Simple YAML parsing for our known keys
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


def write_state_file(state_path: Path, frontmatter: dict, body: str) -> None:
    """Write state file with YAML frontmatter."""
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, str) and " " in value:
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(body)
    state_path.write_text("\n".join(lines))


def main() -> None:
    """Process SubagentStop hook event."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No valid input, nothing to do
        print(json.dumps({}))
        return

    # Get project directory from hook input
    cwd = hook_input.get("cwd", os.getcwd())
    project_dir = Path(cwd)

    # Check which agent just completed (from transcript or session context)
    # The SubagentStop hook receives context about the stopping subagent
    transcript_path = hook_input.get("transcript_path", "")
    session_id = hook_input.get("session_id", "")

    # State file location
    state_dir = project_dir / ".claude"
    state_file = state_dir / "ansible-workflows.local.md"

    # If no state file exists, this isn't an ansible-workflows pipeline
    if not state_file.exists():
        print(json.dumps({}))
        return

    # Read current state
    state_content = state_file.read_text()
    state, body = parse_frontmatter(state_content)

    # Check if pipeline is active
    if not state.get("active", False):
        print(json.dumps({}))
        return

    # Ensure gitignore is configured for state files
    ensure_gitignore(project_dir)

    current_agent = state.get("current_agent", "")
    current_phase = state.get("pipeline_phase", "")

    # Check if this is an ansible-* agent
    if not current_agent.startswith("ansible-"):
        print(json.dumps({}))
        return

    # Validate agent wrote its bundle (if expected)
    expected_bundle = AGENT_BUNDLES.get(current_agent)
    if expected_bundle:
        bundle_file = state_dir / f"ansible-workflows{expected_bundle}"
        if not bundle_file.exists():
            # Bundle missing - remind agent to write it
            result = {
                "message": f"[ansible-workflows] {current_agent} should write context bundle before completing. Expected: .claude/ansible-workflows{expected_bundle}"
            }
            print(json.dumps(result))
            return

    # Determine next phase based on agent
    if current_agent in AGENT_PHASE_MAP:
        _, next_phase = AGENT_PHASE_MAP[current_agent]

        if current_agent == "ansible-validator":
            # Check if validation passed (read from bundle)
            bundle_file = state_dir / "ansible-workflows.validating.bundle.md"
            if bundle_file.exists():
                bundle_content = bundle_file.read_text()
                bundle_state, _ = parse_frontmatter(bundle_content)
                if bundle_state.get("validation_passed", False):
                    next_phase = "reviewing"
                    state["last_validation_passed"] = True
                else:
                    next_phase = "debugging"
                    state["last_validation_passed"] = False
                    state["validation_attempts"] = state.get("validation_attempts", 0) + 1

        elif current_agent == "ansible-reviewer":
            # Check if approved
            bundle_file = state_dir / "ansible-workflows.validating.bundle.md"
            if bundle_file.exists():
                bundle_content = bundle_file.read_text()
                if "APPROVED" in bundle_content.upper():
                    # Pipeline complete
                    state["active"] = False
                    state["completed_at"] = datetime.now(UTC).isoformat()
                    next_phase = "complete"
                else:
                    next_phase = "debugging"

        if next_phase and next_phase != "complete":
            state["pipeline_phase"] = next_phase
            # Map phase to next agent
            phase_agent_map = {
                "validating": "ansible-validator",
                "reviewing": "ansible-reviewer",
                "debugging": "ansible-debugger",
            }
            state["current_agent"] = phase_agent_map.get(next_phase, "")

    # Update state file
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    updated_body = f"{body}\n\n[{timestamp}] {current_agent} completed -> {state.get('pipeline_phase', 'unknown')}"
    write_state_file(state_file, state, updated_body)

    # Output guidance for main session
    if state.get("active", False):
        next_agent = state.get("current_agent", "")
        result = {
            "message": f"[ansible-workflows] Pipeline continuing: {current_agent} -> {next_agent}. Dispatch {next_agent} with context from .claude/ansible-workflows.*.bundle.md"
        }
    else:
        result = {
            "message": "[ansible-workflows] Pipeline complete. All validation passed and changes approved."
        }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
