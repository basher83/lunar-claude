# The Navigation Property in docs.json

The `navigation` property in `docs.json` controls the structure and information hierarchy of your documentation. It organizes your content so users can find what they need.

## Overview

Navigation elements include:
- **Groups**: Organize sidebar navigation into sections
- **Anchors**: Persistent navigation items at the top of the sidebar
- **Tabs**: Create distinct sections with separate URL paths
- **Pages**: Reference MDX files or OpenAPI endpoints
- **External Links**: Link to external resources

## Groups

Groups organize sidebar navigation into sections. They can be nested, labeled with tags, and styled with icons.

### Basic Group Structure

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "pages": ["introduction", "installation", "quickstart"]
      }
    ]
  }
}
```

### Group Properties

- **`group`** (required): The group name
- **`pages`** (required): Array of page paths or nested groups
- **`icon`** (optional): Icon name (Font Awesome, Lucide, or custom SVG)
- **`tag`** (optional): Tag label (e.g., "NEW", "BETA")
- **`expanded`** (optional): Default expanded state (`true`/`false`)

### Nested Groups

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "icon": "play",
        "expanded": true,
        "pages": [
          "introduction",
          {
            "group": "Installation",
            "icon": "download",
            "pages": ["install-linux", "install-mac", "install-windows"]
          }
        ]
      }
    ]
  }
}
```

### Group with Tag and Icon

```json
{
  "navigation": {
    "groups": [
      {
        "group": "New Features",
        "icon": "sparkles",
        "tag": "NEW",
        "pages": ["feature-1", "feature-2"]
      }
    ]
  }
}
```

## Anchors

Anchors add persistent navigation items at the top of your sidebar. Use them to section content, provide quick access to external resources, or create calls to action.

### Basic Anchors

```json
{
  "navigation": {
    "anchors": [
      {
        "anchor": "Documentation",
        "icon": "book-open",
        "pages": ["quickstart", "guides", "api-reference"]
      },
      {
        "anchor": "Blog",
        "icon": "newspaper",
        "href": "https://example.com/blog"
      }
    ]
  }
}
```

### Global Anchors

Global anchors link to external resources only. They must have an `href` field and cannot point to relative paths.

```json
{
  "navigation": {
    "global": {
      "anchors": [
        {
          "anchor": "Community",
          "icon": "users",
          "href": "https://slack.com"
        },
        {
          "anchor": "Support",
          "icon": "headphones",
          "href": "https://support.example.com"
        }
      ]
    },
    "groups": [
      // ... your groups
    ]
  }
}
```

## Tabs

Tabs create distinct sections with separate URL paths. They create a horizontal navigation bar at the top of your documentation.

### Basic Tabs

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "API Reference",
        "icon": "square-terminal",
        "pages": [
          "api-reference/get",
          "api-reference/post",
          "api-reference/delete"
        ]
      },
      {
        "tab": "SDK",
        "icon": "code",
        "pages": ["sdk/javascript", "sdk/python"]
      },
      {
        "tab": "Blog",
        "icon": "newspaper",
        "href": "https://external-link.com/blog"
      }
    ]
  }
}
```

### Hiding Tabs

Hide a tab by adding the `hidden` property:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Hidden Section",
        "hidden": true,
        "pages": ["page1", "page2"]
      }
    ]
  }
}
```

## OpenAPI Integration

Integrate OpenAPI specifications directly into your navigation to automatically generate API documentation.

### Dedicated API Sections

Generate pages for all endpoints in a specification:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "API Reference",
        "openapi": "openapi.json"
      }
    ]
  }
}
```

Or with tabs:

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "API Reference",
        "openapi": "https://petstore3.swagger.io/api/v3/openapi.json"
      }
    ]
  }
}
```

### Selective Endpoints

Reference specific endpoints alongside other pages:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "API Reference",
        "openapi": "openapi.json",
        "pages": [
          "overview",
          "authentication",
          "GET /users",
          "POST /users",
          "GET /users/{id}",
          "advanced-features"
        ]
      }
    ]
  }
}
```

### Multiple OpenAPI Specifications

Organize multiple specifications in separate groups:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Users API",
        "openapi": {
          "source": "/path/to/users-openapi.json",
          "directory": "users-api-reference"
        }
      },
      {
        "group": "Admin API",
        "openapi": {
          "source": "/path/to/admin-openapi.json",
          "directory": "admin-api-reference"
        }
      }
    ]
  }
}
```

### OpenAPI Inheritance

Set a default OpenAPI specification at any level. Child elements inherit it unless they define their own:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "API Reference",
        "openapi": "/path/to/openapi-v1.json",
        "pages": [
          "overview",
          "GET /users",
          {
            "group": "Products",
            "openapi": "/path/to/openapi-v2.json",
            "pages": ["GET /products", "POST /products"]
          }
        ]
      }
    ]
  }
}
```

## External Links

### In Navigation

Link to external sites directly from navigation:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Resources",
        "pages": [
          "documentation",
          {
            "title": "npm Package",
            "href": "https://www.npmjs.com/package/example"
          }
        ]
      }
    ]
  }
}
```

### In Page Frontmatter

Use the `url` metadata in page frontmatter:

```yaml
---
title: "npm Package"
url: "https://www.npmjs.com/package/example"
---
```

## Navbar Links

Add external links to the top navigation bar:

```json
{
  "navbar": {
    "links": [
      {
        "label": "Blog",
        "href": "https://example.com/blog",
        "icon": "newspaper"
      },
      {
        "label": "GitHub",
        "href": "https://github.com/example",
        "icon": "github"
      }
    ],
    "primary": {
      "type": "button",
      "label": "Get Started",
      "href": "https://example.com/signup"
    }
  }
}
```

## Hiding Pages and Groups

### Hide a Group

Set `hidden: true` to hide an entire group:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Internal Docs",
        "hidden": true,
        "pages": ["internal-page-1", "internal-page-2"]
      }
    ]
  }
}
```

### Hide a Tab

```json
{
  "navigation": {
    "tabs": [
      {
        "tab": "Hidden Tab",
        "hidden": true,
        "pages": ["page1", "page2"]
      }
    ]
  }
}
```

**Note**: Hidden pages are excluded from search and SEO by default. To include them, add `"seo": { "indexing": "all" }` to your `docs.json`.

## Icons

Icons can be specified using:
- **Font Awesome icon name**: `"icon": "book"`
- **Lucide icon name**: `"icon": "book-open"`
- **Custom SVG**: `"icon": {<svg>...</svg>}`
- **URL**: `"icon": "https://example.com/icon.svg"`
- **File path**: `"icon": "/icons/custom-icon.svg"`

For Font Awesome icons, specify the style:

```json
{
  "icon": "book",
  "iconType": "solid"  // Options: regular, solid, light, thin, sharp-solid, duotone, brands
}
```

## Expanded State

Control the default expanded state:

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Important Section",
        "expanded": true,  // Expanded by default
        "pages": ["page1", "page2"]
      },
      {
        "group": "Other Section",
        "expanded": false,  // Collapsed by default
        "pages": ["page3", "page4"]
      }
    ]
  }
}
```

## Complete Example

Here's a comprehensive navigation example:

```json
{
  "navigation": {
    "global": {
      "anchors": [
        {
          "anchor": "Community",
          "icon": "users",
          "href": "https://slack.com"
        }
      ]
    },
    "tabs": [
      {
        "tab": "Documentation",
        "icon": "book",
        "groups": [
          {
            "group": "Getting Started",
            "icon": "play",
            "expanded": true,
            "pages": [
              "introduction",
              "installation",
              {
                "group": "Quick Start",
                "pages": ["quickstart-guide"]
              }
            ]
          },
          {
            "group": "API Reference",
            "icon": "square-terminal",
            "tag": "NEW",
            "openapi": "openapi.json",
            "pages": [
              "overview",
              "authentication",
              "GET /users",
              "POST /users"
            ]
          }
        ]
      },
      {
        "tab": "SDK",
        "icon": "code",
        "pages": ["sdk/javascript", "sdk/python"]
      }
    ]
  }
}
```

## Best Practices

1. **Start simple**: Begin with basic groups and add complexity as needed
2. **Logical hierarchy**: Organize content in a way that matches user mental models
3. **Use icons**: Icons improve visual scanning and navigation
4. **Expand important sections**: Use `expanded: true` for frequently accessed content
5. **Limit top-level items**: Avoid overwhelming users with too many top-level sections
6. **Consistent naming**: Use clear, intuitive labels that align with user terminology
7. **Test navigation**: Use `mint dev` to preview and test your navigation structure

## Troubleshooting

- **Pages not appearing**: Ensure file paths match exactly (case-sensitive)
- **OpenAPI endpoints not generating**: Verify OpenAPI spec is valid using `mint openapi-check`
- **Hidden pages still indexed**: Add `"seo": { "indexing": "visible" }` to exclude hidden pages
- **Mixed navigation issues**: Don't reference both MDX files and OpenAPI endpoints for the same operation
