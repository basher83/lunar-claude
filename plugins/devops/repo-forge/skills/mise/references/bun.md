# mise: Bun + TypeScript Ecosystem

Bun toolchain management and task patterns for Bun/TypeScript projects. Models the pi-until-done toolchain: bun as runtime, package manager, and test runner; node (LTS) for tooling that expects a node binary; biome for lint + format; tsc for type-checking only.

## Toolchain

```toml
[tools]
bun = "1.3.14"          # runtime, package manager, test runner
node = "24.16.0"        # LTS — pinned for tooling that assumes node on PATH
biome = "2.4.16"        # lint + format for JS/TS/JSON
shellcheck = "0.11.0"   # shell scripts (preset/CI helpers)
```

Install these resolve-then-pin: `mise use --pin bun node@lts biome shellcheck` writes the exact resolved versions (see the Tool Version Management policy in `SKILL.md` — never the bare `latest`/`@lts` channel form). `tsc` is deliberately not a mise tool: it runs through bun (`bun x tsc`), versioned by the project's `typescript` devDependency so the type-checker tracks the codebase, not a global pin.

### Why both bun and node

bun is the runtime, installer, and test runner — most project commands go through it. node (LTS) is still pinned because some build tools, language servers, and libraries assume a `node` binary on PATH even in a bun-first project. Pinning node@lts (resolved to an exact version) keeps that compatibility deterministic.

## biome (lint + format)

biome replaces eslint + prettier with a single fast binary covering JS, TS, and JSON. Let biome generate its own config rather than hand-writing one — this avoids pinning a schema/ruleset from memory:

```bash
biome init   # writes biome.json with a version-correct schema + ruleset
```

Create it only when absent so an existing project's biome config is never clobbered. Because biome also formats JSON, any scaffolded JSON (including base's `renovate.json`) must be normalized through `biome format --write` once biome is in the pre-commit gate — otherwise the first `hk check` on a freshly onboarded repo fails on the scaffolder's own output.

## TypeScript config

`tsconfig.json` defines compilation semantics, so write it only when absent. A strict, no-emit baseline fits a bun project (bun handles execution and bundling; tsc is type-check only):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2022", "DOM"],
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "isolatedModules": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist", "build"]
}
```

## Task Patterns

```toml
[tasks.install-deps]
description = "Install dependencies"
run = "bun install"

[tasks.test]
description = "Run tests"
run = "bun test"

[tasks.typecheck]
description = "Type-check (no emit)"
run = "bun x tsc --noEmit"

[tasks.format]
description = "Format code"
run = "biome format --write ."

[tasks.lint]
description = "Run all checks"
run = "hk check"        # biome + shellcheck run inside hk's hooks

[tasks.ci]
description = "Full CI gate"
depends = ["lint", "typecheck", "test"]
```

## hk Integration

The bun preset writes `hk.pkl` with `Builtins.biome` (lint + format for JS/TS/JSON) and `Builtins.shellcheck`, plus the base file-hygiene steps and a `check_conventional_commit` commit-msg hook. biome resolves through mise, so no version is pinned in `hk.pkl` itself — the `[tools]` pin in `mise.toml` is the single source of truth. See `references/hk.md` for step configuration and the `Regex`-vs-`List` exclude caveat.

## Bun Specifics

- `bun install` — fast installer; writes `bun.lock` (text) or `bun.lockb` (binary). Commit the lockfile.
- `bun test` — built-in test runner; no jest/vitest dependency needed.
- `bun x <tool>` — runs a package binary (like `npx`), e.g. `bun x tsc --noEmit`.
- `bun run <script>` — runs a `package.json` script.

Run `bun init` first if the project has no `package.json` yet — the preset configures tooling but does not create the package manifest.
