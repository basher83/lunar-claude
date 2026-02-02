#!/usr/bin/env python3
"""PreToolUse hook: Block hardcoded secrets in Edit/Write operations."""

import json
import re
import sys


def main() -> None:
    input_data = json.load(sys.stdin)
    tool_input = input_data.get("tool_input", {})

    content = tool_input.get("new_string", "") or tool_input.get("content", "")
    if not content:
        return

    secret_patterns = [
        # Key=value assignments with actual values
        r"(?:API_KEY|SECRET_KEY|PASSWORD|TOKEN|PRIVATE_KEY)\s*[=:]\s*[\"\x27\\]?[A-Za-z0-9_/+=-]{8,}",
        # Known secret prefixes
        r"sk-[A-Za-z0-9]{20,}",
        r"ghp_[A-Za-z0-9]{36,}",
        r"ghu_[A-Za-z0-9]{36,}",
        r"AKIA[0-9A-Z]{16}",
        r"xox[bpras]-[A-Za-z0-9-]+",
        # Bare export of secrets
        r"export\s+(?:API_KEY|SECRET_KEY|DATABASE_URL|PASSWORD|TOKEN|AWS_SECRET_ACCESS_KEY|PRIVATE_KEY)\s*=\s*[\"\x27\\]?[^\s\"\x27]+",
    ]

    for pattern in secret_patterns:
        match = re.search(pattern, content)
        if match:
            snippet = match.group()[:40]
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": (
                            f"Hardcoded secret detected: {snippet}...\n\n"
                            "Use fnox or infisical instead:\n"
                            "  fnox set SECRET_NAME value\n"
                            "  fnox exec -- your-command\n"
                            "  infisical run -- your-command"
                        ),
                    }
                )
            )
            return


if __name__ == "__main__":
    main()
