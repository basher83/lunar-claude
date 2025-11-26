# Configure Page Metadata, Titles, and Frontmatter Properties

Every page in Mintlify starts with frontmatter—YAML metadata enclosed by `---` at the beginning of the file. Frontmatter controls how your page appears and behaves.

## Basic Structure

All frontmatter must be enclosed in `---` delimiters:

```yaml
---
title: "Page Title"
description: "Page description"
---
```

## Core Metadata Properties

### Title

The page title appears in navigation, browser tabs, and as the H1 heading:

```yaml
---
title: "Getting Started Guide"
---
```

**Note**: The `title` property serves as the H1 heading for accessibility. Each page should have exactly one H1.

### Description

A brief description that appears under the title and improves SEO:

```yaml
---
title: "API Authentication"
description: "Complete guide to implementing API authentication with code examples"
---
```

### Sidebar Title

A shorter title displayed in the sidebar navigation:

```yaml
---
title: "Complete Installation Guide for All Platforms"
sidebarTitle: "Installation"
---
```

## Visual Properties

### Icon

Display an icon next to the page title in the sidebar:

```yaml
---
title: "Documentation"
icon: "book"
---
```

**Icon Options**:
- Font Awesome icon name: `"book"`
- Lucide icon name: `"book-open"`
- URL to external icon: `"https://example.com/icon.svg"`
- File path: `"/icons/custom-icon.svg"`
- Custom SVG: `{<svg>...</svg>}`

### Icon Type

For Font Awesome icons, specify the style:

```yaml
---
title: "Documentation"
icon: "book"
iconType: "solid"  # Options: regular, solid, light, thin, sharp-solid, duotone, brands
---
```

### Tag

Display a tag next to the page title:

```yaml
---
title: "New Features"
tag: "NEW"
---
```

Common tag values: `"NEW"`, `"BETA"`, `"DEPRECATED"`, `"UPDATED"`

## Page Modes

Control the page layout using the `mode` property:

### Default Mode

Standard layout with sidebar navigation and table of contents (no `mode` specified):

```yaml
---
title: "Standard Page"
---
```

### Wide Mode

Hides the table of contents. Useful for pages without headings or when you need extra horizontal space:

```yaml
---
title: "Wide Page"
mode: "wide"
---
```

**Available**: All themes

### Center Mode

Removes sidebar and table of contents, centering the content. Useful for changelogs:

```yaml
---
title: "Changelog"
mode: "center"
---
```

**Available**: Mint and Linden themes only

### Custom Mode

Minimalist layout with only the top navbar. Perfect for landing pages:

```yaml
---
title: "Landing Page"
mode: "custom"
---
```

**Available**: All themes

## SEO Metadata

### Basic SEO Tags

Most SEO meta tags are automatically generated. You can override them:

```yaml
---
title: "Page Title"
description: "Page description"
keywords: ["keyword1", "keyword2"]
---
```

### Open Graph Tags

For social media sharing:

```yaml
---
title: "Page Title"
description: "Page description"
"og:title": "Social Media Title"
"og:description": "Social media description"
"og:image": "/images/social-preview.jpg"
"og:url": "https://docs.example.com/page"
"og:type": "article"
"og:image:width": 1200
"og:image:height": 630
---
```

**Note**: Meta tags with colons must be wrapped in quotes.

### Twitter Card Tags

```yaml
---
"twitter:title": "Twitter Card Title"
"twitter:description": "Twitter card description"
"twitter:image": "/images/twitter-preview.jpg"
"twitter:card": "summary_large_image"
"twitter:site": "@yourhandle"
---
```

### Disable Indexing

Prevent search engines from indexing a page:

```yaml
---
title: "Internal Page"
noindex: true
---
```

Or use robots meta tag:

```yaml
---
title: "Page Title"
robots: "noindex, nofollow"
---
```

## OpenAPI-Specific Frontmatter

### Document Endpoints

Link to OpenAPI operations:

```yaml
---
title: "Get Users"
description: "Returns all users from the system"
openapi: "openapi.json GET /users"
---
```

With file path for multiple specs:

```yaml
---
title: "Create User"
openapi: "/path/to/openapi-1.json POST /users"
deprecated: true
version: "1.0"
---
```

### API Playground

Reference API endpoints directly:

```yaml
---
title: "API Endpoint"
api: "POST https://api.example.com/users"
---
```

Or with OpenAPI:

```yaml
---
title: "Endpoint Page"
openapi: "GET /endpoint"
---
```

## External Links

Link to external sites directly from navigation:

```yaml
---
title: "npm Package"
url: "https://www.npmjs.com/package/example"
---
```

## Access Control

### Groups

Restrict page visibility to specific user groups (requires authentication):

```yaml
---
title: "Admin Dashboard"
groups: ["admin", "super-admin"]
---
```

Users must belong to at least one listed group to access the page.

### Public Pages

Make a page publicly accessible even when authentication is enabled:

```yaml
---
title: "Public Documentation"
public: true
---
```

## RSS Feed

Enable RSS feed icon for changelog pages:

```yaml
---
title: "Changelog"
rss: true
---
```

## Custom Metadata

Add any valid YAML frontmatter for custom properties:

```yaml
---
title: "API Documentation"
product: "API"
version: "1.0.0"
category: "reference"
author: "John Doe"
---
```

Custom metadata can be used for filtering, organization, or integration with other tools.

## Complete Examples

### Standard Documentation Page

```yaml
---
title: "Getting Started with Our API"
description: "Learn how to authenticate and make your first API request"
sidebarTitle: "Getting Started"
icon: "rocket"
tag: "NEW"
---
```

### API Endpoint Page

```yaml
---
title: "Create User"
description: "Create a new user account in the system"
openapi: "openapi.json POST /users"
deprecated: false
version: "2.0"
---
```

### Changelog Page

```yaml
---
title: "Product Changelog"
description: "Latest updates and improvements"
mode: "center"
rss: true
---
```

### Landing Page

```yaml
---
title: "Welcome"
description: "Get started with our platform"
mode: "custom"
---
```

### SEO-Optimized Page

```yaml
---
title: "Complete Guide to API Authentication"
description: "Step-by-step guide with code examples for implementing secure API authentication"
keywords: ["api", "authentication", "security", "tutorial"]
"og:title": "API Authentication Guide"
"og:description": "Learn how to implement secure API authentication"
"og:image": "/images/og-auth-guide.jpg"
"og:type": "article"
"twitter:card": "summary_large_image"
"twitter:image": "/images/twitter-auth-guide.jpg"
---
```

### Restricted Access Page

```yaml
---
title: "Admin Configuration"
description: "Administrative settings and configuration options"
groups: ["admin"]
icon: "shield"
---
```

## Best Practices

1. **Always include title**: Every page needs a `title` property
2. **Add descriptions**: Improve SEO and help users understand page content
3. **Use sidebarTitle**: When page titles are long, provide shorter sidebar versions
4. **Consistent icons**: Use consistent icon sets across related pages
5. **Meaningful tags**: Use tags sparingly and consistently (e.g., "NEW", "BETA")
6. **SEO optimization**: Include relevant keywords and Open Graph tags for important pages
7. **Accessibility**: Remember that `title` serves as H1—don't add another H1 in content
8. **Mode selection**: Choose appropriate page modes based on content type
9. **Custom metadata**: Use custom properties for organization and filtering
10. **Test locally**: Use `mint dev` to preview how frontmatter affects page appearance

## Common Patterns

### Changelog Pattern

```yaml
---
title: "Changelog"
mode: "center"
rss: true
---
```

### API Reference Pattern

```yaml
---
title: "API Reference"
icon: "square-terminal"
openapi: "openapi.json"
---
```

### Tutorial Pattern

```yaml
---
title: "Step-by-Step Tutorial"
description: "Complete walkthrough with examples"
icon: "graduation-cap"
tag: "TUTORIAL"
---
```

### Internal Documentation Pattern

```yaml
---
title: "Internal Notes"
noindex: true
groups: ["internal"]
---
```
