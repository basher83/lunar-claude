# Configure Site-Wide Settings in docs.json

The `docs.json` file is the blueprint for your Mintlify documentation site. It controls styling, navigation, integrations, and more. All settings apply globally to all pages.

## Quick Start

To get started, you only need four required fields:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Your Documentation",
  "colors": {
    "primary": "#ff0000"
  },
  "navigation": {
    // Your navigation structure
  }
}
```

**Pro Tip**: Include the `$schema` reference at the top for autocomplete, validation, and helpful tooltips in most code editors.

## Required Settings

### Theme

Choose a layout theme for your site:

- `mint` (default)
- `maple`
- `palm`
- `willow`
- `linden`
- `almond`
- `aspen`

```json
{
  "theme": "mint"
}
```

### Name

The name of your project, organization, or product:

```json
{
  "name": "Your Documentation"
}
```

### Colors

Configure your site's color scheme. Colors are applied differently across themes.

**Primary color** (required): Used for emphasis in light mode
```json
{
  "colors": {
    "primary": "#ff0000"
  }
}
```

**Full color configuration** (optional):
```json
{
  "colors": {
    "primary": "#ff0000",  // Light mode emphasis
    "light": "#00ff00",     // Dark mode emphasis
    "dark": "#0000ff"       // Buttons and hover states
  }
}
```

### Navigation

Controls the structure and hierarchy of your documentation. See the Navigation guide for detailed configuration.

```json
{
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "pages": ["introduction", "installation"]
      }
    ]
  }
}
```

## Customization Settings

### Logo

Set logos for light and dark modes:

```json
{
  "logo": {
    "light": "/logo.png",
    "dark": "/logo-dark.png",
    "href": "https://example.com"  // Optional: URL when clicking logo
  }
}
```

### Favicon

Configure favicon for your site:

```json
{
  "favicon": "/favicon.png"
}
```

Or separate favicons for light/dark modes:

```json
{
  "favicon": {
    "light": "/favicon.png",
    "dark": "/favicon-dark.png"
  }
}
```

### Description

Site description for SEO and AI indexing:

```json
{
  "description": "Comprehensive documentation for your product"
}
```

### Thumbnails

Customize social media and page preview thumbnails:

```json
{
  "thumbnails": {
    "appearance": "light"  // or "dark"
  }
}
```

## API Configuration

### OpenAPI Integration

Add OpenAPI specifications to generate API documentation:

```json
{
  "api": {
    "openapi": "openapi.json"  // File path or URL
  }
}
```

Multiple specifications:

```json
{
  "api": {
    "openapi": [
      "openapi/v1.json",
      "openapi/v2.json"
    ]
  }
}
```

### API Playground Settings

Configure the interactive API playground:

```json
{
  "api": {
    "openapi": "openapi.json",
    "display": "all",  // "all", "none", or "endpoint"
    "auth": {
      "method": "bearer",
      "token": "your-token"
    }
  }
}
```

## Integrations

### Analytics

Add analytics integrations (unlimited free integrations):

```json
{
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXX"
    },
    "plausible": {
      "domain": "docs.domain.com"
    },
    "mixpanel": {
      "token": "your-token"
    }
  }
}
```

Supported analytics platforms: Google Analytics 4, Plausible, Mixpanel, Amplitude, PostHog, Segment, Fathom, Pirsch, and more.

### Search

Configure search functionality:

```json
{
  "integrations": {
    "algolia": {
      "appId": "your-app-id",
      "apiKey": "your-api-key",
      "indexName": "your-index"
    }
  }
}
```

### Assistant

Enable AI assistant:

```json
{
  "integrations": {
    "assistant": {
      "enabled": true
    }
  }
}
```

## Styling Options

### Code Blocks

Customize code block themes:

```json
{
  "styling": {
    "codeblocks": {
      "light": "github-light",
      "dark": "github-dark"
    }
  }
}
```

Or use simple themes:

```json
{
  "styling": {
    "codeblocks": "system"  // or "dark"
  }
}
```

### Breadcrumbs

Control breadcrumb display:

```json
{
  "styling": {
    "eyebrows": "breadcrumbs"  // or "section"
  }
}
```

## SEO Settings

### Meta Tags

Add custom meta tags:

```json
{
  "metatags": [
    {
      "property": "og:image",
      "content": "/og-image.png"
    }
  ]
}
```

### Indexing

Control what gets indexed:

```json
{
  "seo": {
    "indexing": "all"  // or "visible" (default)
  }
}
```

## Complete Example

Here's a comprehensive `docs.json` example:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "My Documentation",
  "description": "Complete guide to using our product",
  "colors": {
    "primary": "#0066ff",
    "light": "#00aaff",
    "dark": "#0044cc"
  },
  "logo": {
    "light": "/logo.png",
    "dark": "/logo-dark.png",
    "href": "https://example.com"
  },
  "favicon": "/favicon.png",
  "navigation": {
    "groups": [
      {
        "group": "Getting Started",
        "pages": ["introduction", "installation"]
      },
      {
        "group": "API Reference",
        "openapi": "openapi.json"
      }
    ]
  },
  "api": {
    "openapi": "openapi.json",
    "display": "all"
  },
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXX"
    },
    "assistant": {
      "enabled": true
    }
  },
  "styling": {
    "codeblocks": "system",
    "eyebrows": "breadcrumbs"
  },
  "seo": {
    "indexing": "all"
  }
}
```

## Best Practices

1. **Start minimal**: Begin with required fields (`theme`, `name`, `colors.primary`, `navigation`) and add optional settings as needed
2. **Use schema reference**: Always include `$schema` for better editor support
3. **Validate locally**: Run `mint dev` to test your configuration before deploying
4. **Organize navigation**: Structure your navigation logically for better user experience
5. **Test themes**: Preview different themes to find the best fit for your brand

## Additional Resources

- **Navigation**: See the Navigation guide for detailed navigation configuration
- **Themes**: Explore theme options and customization
- **OpenAPI**: Learn about API documentation setup
- **Analytics**: Configure analytics integrations
- **SEO**: Optimize your documentation for search engines
