# Mint CLI Local Preview Guide

Use the Mint CLI to preview your documentation locally, test changes in real-time, and catch issues before deploying.

## Prerequisites

- **Node.js**: v20.17.0 or higher through v24 (LTS versions preferred)
- **Documentation directory**: Must contain a `docs.json` file

## Installation

Install the Mint CLI globally:

```bash
npm i -g mint
```

Or using pnpm:

```bash
pnpm add -g mint
```

**Alternative**: Run without global installation:

```bash
npx mint dev
```

## Local Preview

1. Navigate to your documentation directory (where `docs.json` is located)
2. Start the local development server:

```bash
mint dev
```

1. Open your browser to `http://localhost:3000`

The preview updates automatically as you edit files, allowing you to see changes in real-time.

## Benefits

- **Real-time updates**: View changes instantly as you write and edit
- **Pre-deployment testing**: Test appearance and functionality before deploying
- **Issue detection**: Catch problems like:
  - Broken links
  - Accessibility issues
  - Invalid OpenAPI specifications
  - Configuration errors

## Additional CLI Commands

These validation commands run independently and don't require `mint dev` to be running.

### Check for Broken Links

```bash
mint broken-links
```

Detects all non-existent relative links in your documentation. Can be run at any time.

### Accessibility Audit

```bash
mint a11y
```

Scans for common accessibility issues:

- Missing alt text on images
- Improper heading hierarchy
- Insufficient color contrast

Can be run independently of the dev server.

### Validate OpenAPI Specifications

```bash
mint openapi-check <openapiFilenameOrUrl>
```

Validates your OpenAPI document before deployment. Runs independently.

## Troubleshooting

### Local Preview Not Working

- Ensure Node.js v19+ is installed
- Run `mint dev` from the directory containing `docs.json`
- Check Node.js version: `node --version`

### Preview Doesn't Match Production

Update the CLI:

```bash
mint update
```

If `mint update` isn't available, reinstall:

```bash
npm i -g mint@latest
```

### Build Errors

Run `mint dev` locally to catch build errors before pushing. Common issues:

- Invalid `docs.json` syntax
- Missing or incorrect file paths in navigation
- Invalid frontmatter in MDX files
- Broken image links or missing image files

### OpenAPI Issues

If API pages aren't displaying correctly:

1. Run `mint dev` locally to reveal issues
2. Validate your OpenAPI document using `mint openapi-check`
3. Ensure OpenAPI version is 3.0+ (OpenAPI 2.0 is not supported)
4. Verify HTTP methods and paths match exactly in frontmatter and OpenAPI spec

## Best Practices

1. **Always preview locally** before committing changes
2. **Run validation commands** (`mint broken-links`, `mint a11y`) regularly
3. **Keep CLI updated** to match production rendering
4. **Test all links** after making navigation changes
5. **Validate OpenAPI specs** before adding API documentation

## Workflow

1. Make changes to your documentation files
2. **Visual preview** (optional): Run `mint dev` to start local preview and review changes at `http://localhost:3000`
3. **Validation** (can run independently): Run `mint broken-links` and `mint a11y` to check for issues
4. Fix any problems found
5. Commit and push when satisfied

**Note**: `mint broken-links` and `mint a11y` are static analysis commands that don't require the dev server. You can run them at any time, before or after starting `mint dev`.
