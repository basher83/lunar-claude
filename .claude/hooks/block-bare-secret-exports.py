#!/usr/bin/env python3
"""PreToolUse hook: Block bare export of secret-like env vars in Bash."""

import json
import re
import sys

SAFE_VARS = frozenset({
    "PATH", "HOME", "USER", "SHELL", "TERM", "EDITOR", "LANG",
    "LC_ALL", "LC_CTYPE", "PYTHONPATH", "NODE_PATH", "GOPATH",
    "VIRTUAL_ENV", "CONDA_PREFIX", "XDG_CONFIG_HOME", "XDG_DATA_HOME",
    "PS1", "PROMPT", "DISPLAY", "WAYLAND_DISPLAY", "TZ", "PAGER",
    "MISE_ENV", "MISE_SHELL",
})

SECRET_INDICATORS = [
    "KEY", "SECRET", "TOKEN", "PASSWORD", "CREDENTIAL",
    "AUTH", "DATABASE_URL", "REDIS_URL", "MONGO_URI",
    "CONNECTION_STRING", "DSN",
]


def main() -> None:
    input_data = json.load(sys.stdin)
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")
    if not command:
        return

    # Allow commands wrapped in fnox or infisical
    if "fnox exec" in command or "infisical run" in command:
        return

    export_pattern = r"export\s+([A-Z_][A-Z0-9_]*)\s*=\s*[\"\x27\\]?([^\s\"\x27]+)"
    matches = re.findall(export_pattern, command)

    for var_name, _value in matches:
        if var_name in SAFE_VARS:
            continue
        if any(ind in var_name for ind in SECRET_INDICATORS):
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": (
                            f"Bare export of secret-like variable: {var_name}\n\n"
                            "Use fnox or infisical instead:\n"
                            "  fnox exec -- your-command\n"
                            "  infisical run -- your-command\n"
                            "  mise run task-name  (if task wraps fnox)"
                        ),
                    }
                )
            )
            return


if __name__ == "__main__":
    main()
