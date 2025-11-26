# Customize Themes, Fonts, Custom Scripts, and React

Customize your Mintlify documentation site's appearance and functionality with themes, fonts, custom CSS/JavaScript, and React components.

## Themes

Choose from seven built-in themes to control your site's layout and visual style.

### Available Themes

Configure your theme in `docs.json`:

```json
{
  "theme": "mint"  // Options: mint, maple, palm, willow, linden, almond, aspen
}
```

**Theme Options**:
- `mint` - Default theme
- `maple`
- `palm`
- `willow`
- `linden`
- `almond`
- `aspen`

Each theme has a unique layout and applies colors differently. Preview themes to find the best fit for your brand.

### Theme-Specific Features

- **Center mode**: Available for Mint and Linden themes only
- **Frame mode**: Available for Aspen and Almond themes only
- **Custom mode**: Available for all themes

## Fonts

Customize typography using Google Fonts, local fonts, or externally hosted fonts.

### Google Fonts

Google Fonts are loaded automatically when you specify a family name:

```json
{
  "fonts": {
    "family": "Open Sans",
    "weight": 400
  }
}
```

### Local Fonts

Place font files in your project and reference them:

```json
{
  "fonts": {
    "family": "Custom Font",
    "source": "/fonts/custom-font.woff2",
    "format": "woff2",
    "weight": 400
  }
}
```

### Separate Heading and Body Fonts

Configure different fonts for headings and body text:

```json
{
  "fonts": {
    "family": "Open Sans",  // Body font
    "weight": 400,
    "heading": {
      "family": "Playfair Display",
      "weight": 700
    },
    "body": {
      "family": "Open Sans",
      "weight": 400
    }
  }
}
```

### Font Configuration Options

- **`family`**: Font family name (Google Fonts supported)
- **`weight`**: Font weight (400, 700, or variable font weights like 550)
- **`source`**: URL or path to font file (not needed for Google Fonts)
- **`format`**: Font format (`woff2`, `woff`, `ttf`, etc.) - required when using `source`

### Complete Font Example

```json
{
  "fonts": {
    "family": "Inter",
    "weight": 400,
    "heading": {
      "family": "Playfair Display",
      "weight": 700,
      "source": "/fonts/playfair-display.woff2",
      "format": "woff2"
    },
    "body": {
      "family": "Inter",
      "weight": 400
    }
  }
}
```

## Custom Scripts

Add custom CSS and JavaScript to fully customize your documentation's appearance and behavior.

### Custom CSS

Create a `style.css` file in your repository root. All CSS classes defined will be available in your MDX files.

**Example `style.css`**:

```css
#navbar {
  background: #fffff2;
  padding: 1rem;
}

footer {
  margin-top: 2rem;
}

.custom-button {
  background-color: #0066ff;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}
```

**Using in MDX**:

```html
<button className="custom-button">Click me</button>
```

### Custom JavaScript

Add a `script.js` file to execute custom JavaScript globally (equivalent to adding a `<script>` tag to every page).

**Example `script.js`**:

```javascript
// Track custom events
document.addEventListener('DOMContentLoaded', () => {
  console.log('Documentation loaded');

  // Add custom behavior
  const buttons = document.querySelectorAll('.custom-button');
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Custom click handler
    });
  });
});
```

### Tailwind CSS

Use Tailwind CSS v3 to style HTML elements. Tailwind classes are available in your MDX files.

**Common Tailwind Classes**:
- `w-full` - Full width
- `aspect-video` - 16:9 aspect ratio
- `rounded-xl` - Large rounded corners
- `block`, `hidden` - Display control
- `dark:hidden`, `dark:block` - Dark mode visibility

**Example**:

```html
<img
  className="block dark:hidden rounded-lg
  src="/images/light-mode.png"
  alt="Light mode"
/>

<img
  className="hidden dark:block"
  src="/images/dark-mode.png"
  alt="Dark mode"
/>
```

**Note**: Tailwind arbitrary values are not supported. Use the `style` prop for custom values:

```html
<img
  style={{ width: '350px', margin: '12px auto' }}
  src="/path/image.jpg"
/>
```

### Using Identifiers and Selectors

Mintlify provides identifiers for UI elements. Use browser inspect element to find specific selectors:

**Common Identifiers**:
- `#navbar` - Navigation bar
- `#sidebar` - Sidebar navigation
- `#footer` - Footer
- `.content-area` - Main content area
- `.code-block` - Code blocks

**Example**:

```css
#navbar {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.sidebar {
  background: #f9fafb;
}
```

## React Components

Build interactive React components directly in your MDX files using React hooks.

### Creating React Components

1. **Create component in `snippets` folder**:

Create `snippets/color-generator.jsx`:

```jsx
import { useState } from 'react';

export const ColorGenerator = () => {
  const [color, setColor] = useState('#0066ff');

  return (
    <div>
      <input
        type="color"
        value={color}
        onChange={(e) => setColor(e.target.value)}
      />
      <p>Selected color: {color}</p>
    </div>
  );
};
```

**Important**: Use arrow function syntax (`=>`) rather than `function` declarations.

2. **Import and use in MDX**:

```mdx
---
title: "Color Picker"
---

import { ColorGenerator } from "/snippets/color-generator.jsx";

<ColorGenerator />
```

### React Hooks

You can use all React hooks in your components:

```jsx
import { useState, useEffect } from 'react';

export const Counter = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};
```

### Using CodeBlock Component

Use the `<CodeBlock>` component in custom React components:

```jsx
import { CodeBlock } from '@mintlify/components';

export const CustomCodeBlock = ({ filename, icon, language, highlight, children }) => {
  return (
    <CodeBlock
      filename={filename}
      icon={icon}
      language={language}
      lines
      highlight={highlight}
    >
      {children}
    </CodeBlock>
  );
};
```

### Component Example

**`snippets/interactive-demo.jsx`**:

```jsx
import { useState } from 'react';

export const InteractiveDemo = () => {
  const [activeTab, setActiveTab] = useState('tab1');

  return (
    <div>
      <div>
        <button onClick={() => setActiveTab('tab1')}>Tab 1</button>
        <button onClick={() => setActiveTab('tab2')}>Tab 2</button>
      </div>
      {activeTab === 'tab1' && <div>Content for Tab 1</div>}
      {activeTab === 'tab2' && <div>Content for Tab 2</div>}
    </div>
  );
};
```

## Code Block Themes

Customize syntax highlighting themes for code blocks.

### Simple Themes

```json
{
  "styling": {
    "codeblocks": "system"  // or "dark"
  }
}
```

- `"system"` - Matches current site mode (light or dark)
- `"dark"` - Always uses dark mode

### Custom Shiki Themes

Use Shiki themes for light and dark modes:

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

Or use a single theme for both modes:

```json
{
  "styling": {
    "codeblocks": "monokai"
  }
}
```

### CSS Variables Theme

For complete control, use CSS variables:

1. Set theme to `"css-variables"`:

```json
{
  "theme": "css-variables",
  "styling": {
    "codeblocks": "css-variables"
  }
}
```

2. Override colors in your CSS:

```css
:root {
  --mint-color-text: #333333;
  --mint-color-background: #ffffff;
  --mint-token-keyword: #0066ff;
  --mint-token-string: #00aa00;
  --mint-token-comment: #888888;
  --mint-token-function: #ff6600;
}
```

**Available CSS Variables**:
- `--mint-color-text` - Default text color
- `--mint-color-background` - Background color
- `--mint-token-constant` - Constants and literals
- `--mint-token-string` - String values
- `--mint-token-comment` - Comments
- `--mint-token-keyword` - Keywords
- `--mint-token-parameter` - Function parameters
- `--mint-token-function` - Function names
- Plus ANSI color variables for terminal output

## Complete Customization Example

Here's a comprehensive `docs.json` example:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "My Documentation",
  "colors": {
    "primary": "#0066ff",
    "light": "#00aaff",
    "dark": "#0044cc"
  },
  "fonts": {
    "family": "Inter",
    "weight": 400,
    "heading": {
      "family": "Playfair Display",
      "weight": 700
    }
  },
  "styling": {
    "codeblocks": {
      "light": "github-light",
      "dark": "github-dark"
    },
    "eyebrows": "breadcrumbs"
  },
  "icons": {
    "library": "fontawesome"
  }
}
```

## Best Practices

1. **Start with themes**: Choose a theme that matches your brand before extensive customization
2. **Use Google Fonts**: Prefer Google Fonts for better performance and reliability
3. **Organize snippets**: Keep React components in the `snippets` folder organized by feature
4. **Test locally**: Use `mint dev` to preview all customizations
5. **Use Tailwind**: Leverage Tailwind CSS for responsive design
6. **Component reusability**: Create reusable React components for common patterns
7. **CSS organization**: Keep custom CSS organized and commented
8. **Performance**: Minimize custom JavaScript and CSS for faster page loads
9. **Dark mode**: Always test customizations in both light and dark modes
10. **Accessibility**: Ensure custom components meet accessibility standards

## File Structure

```
your-project/
├── docs.json
├── style.css          # Custom CSS
├── script.js           # Custom JavaScript
├── snippets/           # React components
│   ├── color-generator.jsx
│   └── interactive-demo.jsx
└── fonts/              # Local fonts (optional)
    └── custom-font.woff2
```

## Troubleshooting

**Fonts not loading**:
- Verify font file paths are correct
- Check font format is supported
- Ensure Google Fonts name is spelled correctly

**React components not rendering**:
- Verify component is in `snippets` folder
- Check import path uses `/snippets/` prefix
- Ensure arrow function syntax is used

**Custom CSS not applying**:
- Check CSS file is in repository root
- Verify class names match exactly
- Use browser inspector to check specificity

**Tailwind classes not working**:
- Ensure you're using Tailwind v3 syntax
- Avoid arbitrary values (use `style` prop instead)
- Check for typos in class names
