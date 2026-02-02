# DeepWiki vs context7: MCP Documentation Tools

Head-to-head comparison using `jdx/mise` and `jdx/fnox` as test subjects.

## Summary

Both are MCP servers for fetching library/project documentation. They serve
different purposes and are complementary.

| Aspect | DeepWiki | context7 |
|--------|----------|---------|
| **Strength** | High-level understanding | Concrete implementation details |
| **Output style** | Wiki-like explanations with architecture context | Code snippets with source links |
| **Best question** | "What does this tool do?" | "How do I configure this?" |
| **Depth** | Broad — covers features, architecture, relationships | Narrow — specific configs, APIs, usage patterns |
| **Source** | GitHub repo analysis (AI-generated wiki) | Library documentation + code examples |

## Test: jdx/mise

- **DeepWiki**: Returned comprehensive overview of env plugins, hooks system,
  sops integration, all `mise.toml` config options. Good for understanding the
  plugin architecture and how secret managers integrate via `env._.<plugin>`.
- **context7**: Returned actual `mise.toml` snippets, env plugin development
  patterns, vault-secrets config example. More directly copy-pasteable.

## Test: jdx/fnox

- **DeepWiki**: Full feature overview, all supported providers listed
  (encryption, cloud, password managers, local), architecture explanation,
  profile system, hierarchical config loading.
- **context7**: Exact `fnox.toml` configs for infisical provider, CI/CD GitHub
  Actions workflow, `fnox exec` usage with profiles, `fnox get` commands.

## Recommendation

Use both together:

1. **DeepWiki first** — understand what a tool does, its architecture, and how
   components relate
2. **context7 second** — get the specific configuration snippets and usage
   patterns for implementation

For building Claude Code skills/plugins about external tools, this two-pass
approach gives the best coverage: deepwiki for the knowledge sections, context7
for the concrete examples and reference material.
