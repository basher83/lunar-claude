# Monorepo Configuration Guide

Configure Mintlify to deploy documentation from a specific directory within a monorepo. This setup allows you to maintain documentation alongside your code in repositories that contain multiple projects or services.

## Prerequisites

- Admin access to your Mintlify project
- Documentation files organized in a dedicated directory within your monorepo
- A valid `docs.json` file in your documentation directory

## Setup Steps

### 1. Access Git Settings

Navigate to **Git Settings** in your Mintlify dashboard.

### 2. Enable Monorepo Mode

Select the **"Set up as monorepo"** toggle button.

### 3. Set Documentation Path

Enter the relative path to your docs directory:

- Example: If your docs are in the `documentation/` directory, enter `/documentation`
- Example: If your docs are in the `docs/` directory, enter `/docs`

<Warning>
**Important**: Do not include a trailing slash in the path. Use `/docs` not `/docs/`.
</Warning>

### 4. Save Changes

Select **Save changes** to apply the configuration.

## Directory Structure

Your monorepo should have this structure:

```text
/your-monorepo
  |- main.ts
  |- documentation/          # Your docs directory
  |   |- docs.json          # Must be in the docs directory
  |   |- index.mdx
  |   |- getting-started/
  |   |   |- installation.mdx
  |   |- roles/
  |   |   |- system_user.mdx
  |- ansible/
  |- terraform/
  |- other-projects/
```

## Important Configuration Notes

### docs.json Location

- **Must be in your documentation directory** (not repository root)
- All page references in `docs.json` should be relative to the documentation directory
- Paths are relative to the documentation directory, not the repository root

### Path Format

- Use relative paths starting with `/`
- Do not include trailing slashes
- Examples:
  - ✅ `/documentation`
  - ✅ `/docs`
  - ❌ `/documentation/`
  - ❌ `documentation`

## Example Configuration

If your documentation is in `/documentation`:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "name": "Virgo-Core",
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Getting Started",
            "pages": [
              "index",
              "getting-started/prerequisites",
              "getting-started/installation"
            ]
          }
        ]
      }
    ]
  }
}
```

**Note**: Page paths like `"getting-started/prerequisites"` are relative to the `/documentation` directory, not the repository root.

## Verification

After configuration:

1. Check that your `docs.json` is valid and includes required fields
2. Verify page paths in `docs.json` are relative to your documentation directory
3. Test deployment to ensure Mintlify can access your documentation files

## Troubleshooting

### Documentation Not Deploying

- Verify the path in Git Settings matches your actual directory structure
- Ensure `docs.json` is in the documentation directory (not repository root)
- Check that all page paths in `docs.json` are relative to the documentation directory

### Path Errors

- Remove trailing slashes from the path configuration
- Use absolute paths starting with `/` (e.g., `/docs` not `docs`)
- Verify the directory exists in your repository

## Reference

- [Mintlify Monorepo Documentation](https://mintlify.com/docs/deploy/monorepo)
- [docs.json Schema](https://mintlify.com/docs.json)
