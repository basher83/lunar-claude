# Hide Pages from Navigation While Keeping Them Accessible

Hidden pages are removed from your site's navigation but remain publicly accessible to anyone who knows their URL. Use hidden pages for content that should be accessible or referenced as context for AI tools, but not discoverable through navigation.

## Overview

**Hidden pages**:
- Are removed from navigation menus
- Remain accessible via direct URL
- Use the same URL structure as regular pages
- Can be indexed for search/AI (with configuration)

**Use cases**:
- Content referenced from other pages
- Context for AI assistants
- Internal documentation accessible via direct links
- Beta or experimental features
- Deprecated content still needed for reference

**Note**: For strict access control, use authentication. For user-group-specific hiding, use personalization.

## Hiding Individual Pages

A page is hidden if it's **not included** in your `docs.json` navigation structure.

### Method: Remove from Navigation

Simply omit the page from your navigation:

**Before** (page visible):
```json
{
  "navigation": {
    "groups": [
      {
        "group": "Guides",
        "pages": [
          "getting-started",
          "advanced-topics",
          "hidden-reference"  // Visible in navigation
        ]
      }
    ]
  }
}
```

**After** (page hidden):
```json
{
  "navigation": {
    "groups": [
      {
        "group": "Guides",
        "pages": [
          "getting-started",
          "advanced-topics"
          // hidden-reference removed - now hidden but still accessible
        ]
      }
    ]
  }
}
```

### URL Access

Hidden pages use the same URL structure based on their file path:

- File: `guides/hidden-reference.mdx`
- URL: `docs.yoursite.com/guides/hidden-reference`

## Hiding Groups

Hide an entire group of pages by setting `hidden: true`:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "hidden": true,
        "pages": [
          "introduction",
          "installation",
          "quickstart"
        ]
      },
      {
        "group": "Guides",
        "pages": [
          "guide-1",
          "guide-2"
        ]
      }
    ]
  }
}
```

In this example, the "Getting Started" group is hidden, but the "Guides" group remains visible.

## Hiding Tabs

Hide a tab by adding the `hidden` property:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Home",
        "hidden": true,
        "pages": [
          "index",
          "quickstart"
        ]
      },
      {
        "tab": "Documentation",
        "pages": [
          "api-reference",
          "guides"
        ]
      }
    ]
  }
}
```

## Hiding OpenAPI Endpoints

For OpenAPI-generated pages, use the `x-hidden` extension in your OpenAPI specification:

```json
{
  "paths": {
    "/public-endpoint": {
      "get": {
        "summary": "Public endpoint",
        "description": "Visible in navigation"
      }
    },
    "/hidden-endpoint": {
      "get": {
        "x-hidden": true,
        "summary": "Hidden endpoint",
        "description": "Hidden from navigation but accessible via URL"
      }
    }
  }
}
```

**Use cases for `x-hidden`**:
- Endpoints you want to document but not promote
- Pages linked from other content
- Endpoints for specific users
- Deprecated endpoints still needed for reference

### Alternative: x-excluded

Use `x-excluded: true` to completely exclude an endpoint (no page generated):

```json
{
  "paths": {
    "/secret-endpoint": {
      "get": {
        "x-excluded": true,
        "summary": "Not documented"
      }
    }
  }
}
```

**Difference**:
- `x-hidden: true` - Creates page but hides from navigation
- `x-excluded: true` - No page generated at all

## SEO and Indexing

### Default Behavior

By default, hidden pages are **excluded** from:
- Search engine indexing
- Internal search within your docs
- AI assistant context

### Include Hidden Pages in Search/AI

To include hidden pages in search results and AI context, add to `docs.json`:

```json
{
  "seo": {
    "indexing": "all"
  }
}
```

**Options**:
- `"navigable"` (default) - Index only pages in navigation
- `"all"` - Index all pages, including hidden ones

### Exclude Specific Pages

To exclude a specific hidden page from indexing, add `noindex` to its frontmatter:

```yaml
---
title: "Internal Reference"
noindex: true
---
```

## Navigation Behavior on Hidden Pages

When users access hidden pages directly:

- **Sidebars**: May appear empty or show limited navigation
- **Dropdowns**: May not display properly
- **Tabs**: May shift layout or appear empty
- **Breadcrumbs**: May not show complete path

This is expected behavior since hidden pages aren't part of the navigation structure.

## Best Practices

1. **Document hidden pages**: Keep a list of hidden pages and their URLs for reference
2. **Link from visible content**: Link to hidden pages from other documentation
3. **Use descriptive URLs**: Make hidden page URLs memorable and logical
4. **Consider SEO**: Use `"indexing": "all"` if hidden pages should be searchable
5. **Use groups for organization**: Hide entire groups when hiding related content
6. **OpenAPI endpoints**: Use `x-hidden` for endpoints, not manual navigation removal
7. **Access control**: For strict access control, use authentication instead of hiding
8. **User groups**: Use personalization for group-specific page visibility

## Examples

### Example 1: Reference Documentation

Hide internal reference pages but keep them accessible:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "User Guides",
        "pages": [
          "getting-started",
          "advanced-features"
        ]
      }
      // Reference docs hidden but accessible at:
      // /reference/internal-api
      // /reference/deprecated-methods
    ]
  }
}
```

### Example 2: Beta Features

Hide beta features from main navigation:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Beta Features",
        "hidden": true,
        "pages": [
          "beta/feature-1",
          "beta/feature-2"
        ]
      }
    ]
  }
}
```

### Example 3: OpenAPI Hidden Endpoints

Hide specific API endpoints:

```json
{
  "paths": {
    "/users": {
      "get": {
        "summary": "Get users",
        "description": "Public endpoint"
      }
    },
    "/admin/users": {
      "get": {
        "x-hidden": true,
        "summary": "Admin endpoint",
        "description": "Hidden but accessible"
      }
    }
  }
}
```

### Example 4: AI Context Pages

Hide pages used as AI context but include in indexing:

```json
{
  "seo": {
    "indexing": "all"
  },
  "navigation": {
    "groups": [
      {
        "group": "Documentation",
        "pages": [
          "public-guide-1",
          "public-guide-2"
        ]
      }
      // Hidden pages accessible for AI context:
      // /context/technical-details
      // /context/troubleshooting
    ]
  }
}
```

## Comparison: Hiding vs. Other Methods

| Method | Navigation | Access | Use Case |
|--------|-----------|--------|----------|
| **Hidden pages** | Removed | Public URL | Reference content, AI context |
| **Authentication** | Visible to authorized users | Restricted | Secure content |
| **Personalization** | Visible based on user groups | Group-based | Role-specific content |
| **x-excluded** | N/A | No page created | Don't document at all |

## Troubleshooting

**Hidden page not accessible**:
- Verify the file path matches the URL structure
- Check that the file exists in your repository
- Ensure the file has valid frontmatter

**Hidden page still appears in search**:
- Check `seo.indexing` setting in `docs.json`
- Add `noindex: true` to page frontmatter if needed

**Navigation looks broken on hidden page**:
- This is expected—hidden pages aren't in navigation structure
- Consider using `mode: "custom"` or `mode: "wide"` for better layout

**OpenAPI endpoint still visible**:
- Verify `x-hidden: true` is correctly placed in OpenAPI spec
- Check that you're using the correct OpenAPI spec file
- Run `mint openapi-check` to validate your spec
