---
description: Interactive wizard for creating new plugins in lunar-claude marketplace
---

# New Plugin

Create a new plugin in the lunar-claude marketplace using the template structure.

## Process

Follow these steps to create a properly structured plugin:

### Step 1: Gather Plugin Information

Ask the user for:

- **Plugin name** (kebab-case, no spaces)
- **Description** (one-line summary)
- **Category** (meta, infrastructure, devops, or homelab)
- **Keywords** (comma-separated for searchability)
- **Components needed** (skills, agents, hooks, commands)

### Step 2: Validate Plugin Name

Check that:

- Name uses kebab-case format
- Name is unique (not in current marketplace.json)
- Name is descriptive and clear

### Step 3: Create Plugin Directory

1. Copy template to appropriate category:

   ```bash
   cp -r templates/plugin-template/ plugins/<category>/<plugin-name>/
   ```

2. Navigate to new plugin directory

### Step 4: Customize Plugin Files

1. Update `.claude-plugin/plugin.json`:
   - Replace `PLUGIN_NAME` with actual name
   - Replace `PLUGIN_DESCRIPTION` with description
   - Replace `KEYWORD1`, `KEYWORD2` with actual keywords

2. Update `README.md`:
   - Replace all `PLUGIN_NAME` placeholders
   - Replace `PLUGIN_DESCRIPTION`
   - Remove component sections not being used

3. Remove unused component directories:
   - If not using agents, remove `agents/`
   - If not using skills, remove `skills/`
   - If not using hooks, remove `hooks/`
   - Always keep `commands/` (can be empty with .gitkeep)

### Step 5: Update Marketplace Manifest

1. Read current `.claude-plugin/marketplace.json`

2. Add new plugin entry to `plugins` array:

   ```json
   {
     "name": "plugin-name",
     "source": "./plugins/<category>/<plugin-name>",
     "description": "plugin description",
     "version": "0.1.0",
     "category": "category-name",
     "keywords": ["keyword1", "keyword2"],
     "author": {
       "name": "basher83"
     }
   }
   ```

3. Write updated marketplace.json

4. Validate JSON syntax with `jq`

### Step 6: Create Initial Commit

```bash
git add plugins/<category>/<plugin-name>/
git add .claude-plugin/marketplace.json
git commit -m "feat: add <plugin-name> plugin

Create new <category> plugin: <description>
Initial version 0.1.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 7: Provide Next Steps

Tell the user:

**Plugin created successfully!**

Location: `plugins/<category>/<plugin-name>/`

Next steps:

1. Add your components (skills, agents, hooks, commands)
2. Update README.md with usage examples
3. Test locally: `/plugin marketplace add .`
4. Install: `/plugin install <plugin-name>@lunar-claude`

## Examples

### Example: Creating infrastructure plugin

User input:

- Name: terraform-tools
- Description: Terraform and OpenTofu helpers
- Category: infrastructure
- Keywords: terraform, opentofu, iac
- Components: skills, commands

Result:

- Created `plugins/infrastructure/terraform-tools/`
- Added to marketplace.json under infrastructure category
- Ready for component development

### Example: Creating homelab plugin

User input:

- Name: proxmox-ops
- Description: Proxmox cluster operations
- Category: homelab
- Keywords: proxmox, virtualization, homelab
- Components: agents, commands

Result:

- Created `plugins/homelab/proxmox-ops/`
- Added to marketplace.json under homelab category
- Removed unused skills and hooks directories
