# Hook Spec

A hook is a JSON configuration that triggers automation in response to Claude Code events. Hooks can execute shell commands or prompt-based LLM evaluations before, during, or after tool use and session events.

## Hook Configuration Location

Hooks are configured in settings files:

```text
.claude/settings.json           # Project-level (shared via git)
~/.claude/settings.json         # User-level (personal)
<plugin-root>/hooks.json        # Plugin-level (bundled with plugin)
```

## Hook Structure

Hooks are defined as a JSON object mapping event names to arrays of hook configurations:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Hook Configuration Properties

### Required Properties

- `hooks`
  - Array of hook definitions to execute
  - Each hook must have a `type` property

### Optional Properties

- `matcher`
  - Pattern to match tool names or event subtypes
  - Required for: `PreToolUse`, `PostToolUse`, `PermissionRequest`
  - Supports: exact strings, regex patterns (`Edit|Write`), or `*` for all
  - Example: `"matcher": "Bash"` or `"matcher": "Read|Write|Edit"`

## Hook Definition Properties

### For Command Hooks

- `type` (required)
  - Must be `"command"`
- `command` (required)
  - Bash command to execute
  - Supports `$CLAUDE_PROJECT_DIR` variable
  - Example: `"command": "npm run lint"`
- `timeout` (optional)
  - Execution timeout in seconds
  - Default: 60

### For Prompt Hooks

- `type` (required)
  - Must be `"prompt"`
- `prompt` (required)
  - LLM prompt for evaluation
  - Use `$ARGUMENTS` placeholder for hook input
  - Example: `"prompt": "Review this command for security: $ARGUMENTS"`
- `timeout` (optional)
  - Evaluation timeout in seconds
  - Default: 30

## Hook Events

| Event | Matcher | Description |
|-------|---------|-------------|
| `PreToolUse` | Required | Before tool execution |
| `PostToolUse` | Required | After successful tool completion |
| `PermissionRequest` | Required | When permission dialog is shown |
| `Notification` | Required | When Claude sends notifications (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`) |
| `UserPromptSubmit` | No | When user submits a prompt |
| `Stop` | No | When main Claude agent finishes |
| `SubagentStop` | No | When a subagent finishes |
| `PreCompact` | Required | Before context compaction (`manual`, `auto`) |
| `SessionStart` | Required | Session begins/resumes (`startup`, `resume`, `clear`, `compact`) |
| `SessionEnd` | No | When session ends |

## Hook Input

Hooks receive JSON via stdin containing:

### Common Fields

- `session_id` - Current session identifier
- `transcript_path` - Path to conversation transcript
- `cwd` - Current working directory
- `permission_mode` - Current permission mode
- `hook_event_name` - Name of the triggering event

### Event-Specific Fields

- `tool_name` - Name of the tool (PreToolUse, PostToolUse)
- `tool_input` - Tool input parameters (PreToolUse, PostToolUse)
- `tool_response` - Tool output (PostToolUse only)

## Hook Output

### Exit Codes

- `0` - Success (stdout shown in verbose mode)
- `2` - Blocking error (stderr used as error message)
- Other - Non-blocking error (stderr shown in verbose mode)

### JSON Output (Optional)

Return JSON with exit code 0 for structured responses:

```json
{
  "continue": true,
  "stopReason": "optional stop message",
  "suppressOutput": false,
  "systemMessage": "optional warning to Claude"
}
```

### Prompt Hook Response Schema

```json
{
  "decision": "approve|block",
  "reason": "explanation for the decision",
  "continue": false,
  "stopReason": "message if stopping",
  "systemMessage": "warning to add to context"
}
```

## Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Bash command intercepted'",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --fix",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Additional Information

- Hooks execute in the order they are defined
- Multiple hooks can be attached to the same event
- Plugin hooks are merged with user and project hooks
- Use `$CLAUDE_PLUGIN_ROOT` in plugin hooks for portable paths

## Version History

- 1.0 (2025-10-16) Public Launch
