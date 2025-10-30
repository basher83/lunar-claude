# Extending DeepWiki MCP to Save Outputs

If you want to continue using DeepWiki MCP but add save functionality, you can
create a Claude Code hook using the PostToolUse event:​

- Create `.claude/hooks/save-deepwiki-output.sh`

```bash
#!/bin/bash

## Read the tool output JSON from stdin

HOOK_DATA=$(cat)

## Extract tool name and check if it's deepwiki

TOOL_NAME=$(echo "$HOOK_DATA" | jq -r '.tool_name // empty')

if [[ "$TOOL_NAME" == *"deepwiki"* ]] || [[ "$TOOL_NAME" == *"wiki"* ]]; then

## Extract the content from tool output

  CONTENT=$(echo "$HOOK_DATA" | jq -r '.tool_output.content[0].text // empty')

## Generate filename with timestamp

  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  OUTPUT_DIR="$HOME/.claude/saved-docs"
  mkdir -p "$OUTPUT_DIR"

## Save to markdown file

  echo "$CONTENT" > "$OUTPUT_DIR/deepwiki_${TIMESTAMP}.md"

  echo "✓ Saved DeepWiki output to ${OUTPUT_DIR}/deepwiki_${TIMESTAMP}.md"
fi

exit 0
```

Make it executable:

```bash
chmod +x .claude/hooks/save-deepwiki-output.sh
```

Register the hook in ~/.claude/settings.json:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/save-deepwiki-output.sh"
          }
        ]
      }
    ]
  }
}
```

This automatically saves every DeepWiki MCP output to a timestamped markdown file.
