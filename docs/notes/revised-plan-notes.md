Modified Recommendation: Start with rumdl, then add Claude
Big discovery: rumdl is basically "ruff for markdown" - it's a Rust tool explicitly modeled after ruff with 49-60x speed improvement over markdownlint. It even has the same commands (rumdl lint, rumdl format), LSP support, and reads your existing .markdownlint.json configs.
Revised Implementation Path:

Start with rumdl immediately for Layer 1

cargo install rumdl
It's a drop-in replacement for markdownlint-cli2
Has VS Code extension: rumdl vscode
Can auto-fix the same 24 rules that markdownlint can

Build a single uv script

python   # doc-agent.py

# !/usr/bin/env uv run

## /// script

## dependencies = ["click", "rich"]

## ///

## Just wrap rumdl + add Claude analysis

Add Claude for what rumdl CAN'T fix

Grammar and prose quality
Missing documentation sections
Cross-link validation
Badge updates (your specific pain point)

Skip Layer 3 entirely - the research shows code-docs matching is incredibly complex and probably not worth it for your use case

Why this is better:

rumdl gives you instant wins - 24 auto-fixable rules at blazing speed
You still get to build the fun part - the Claude integration for intelligent analysis
Solves your actual problem faster - you wanted "ruff fix for markdown" and rumdl is literally that

The research also revealed that markdown's fundamental ambiguity means you'll never get Python-level determinism. But rumdl + Claude gives you the best of both worlds: fast mechanical fixes plus intelligent content analysis.
