# mise: Rust Ecosystem

Rust toolchain management and common task patterns for Rust projects.

## Rust Toolchain Management

mise manages Rust through rustup. Installations live in rustup's directory structure, not mise's. mise sets `RUSTUP_TOOLCHAIN` to activate the correct version.

```toml
[tools]
rust = "stable"               # Most common
```

Other channel options:

```toml
[tools]
rust = "1.83"                 # Pinned version
# or
rust = "nightly"              # Nightly channel
```

### Components and profiles

```toml
[tools]
rust = {
  version = "stable",
  components = "clippy,rustfmt,rust-src",
  profile = "default"
}
```

Profile options: `minimal` (compiler only), `default` (plus docs, rustfmt, clippy), `complete` (all components).

### Cross-compilation targets

```toml
[tools]
rust = {
  version = "stable",
  targets = "wasm32-unknown-unknown,aarch64-unknown-linux-gnu"
}
```

### When to use mise vs rustup directly

Use mise for version pinning in `mise.toml` — the project declares which Rust version it needs, and mise activates it. Rustup handles the underlying installation, component management, and target configuration. The two work together: mise selects, rustup provides.

### Rust settings

```toml
[settings]
rust.cargo_home = "~/.cargo"
rust.rustup_home = "~/.rustup"
```

These isolate mise's Rust installation from other rustup setups on the system when needed.

## Task Patterns

### Building

```toml
[tasks.build]
description = "Build in debug mode"
run = "cargo build"

[tasks."build:release"]
description = "Build optimized release binary"
run = "cargo build --release"
sources = ["src/**/*.rs", "Cargo.toml", "Cargo.lock"]
outputs = ["target/release/{{env.CARGO_BIN_NAME}}"]
```

### Testing

```toml
[tasks.test]
description = "Run test suite"
run = "cargo test"

[tasks."test:verbose"]
description = "Run tests with output"
run = "cargo test -- --nocapture"

[tasks."test:doc"]
description = "Run documentation tests"
run = "cargo test --doc"
```

### Linting and Formatting

```toml
[tasks.lint]
description = "Run clippy with strict warnings"
run = "cargo clippy -- -D warnings"

[tasks.format]
description = "Format code"
run = "cargo fmt"

[tasks."format:check"]
description = "Check formatting without changes"
run = "cargo fmt -- --check"
```

### Quality Gate

```toml
[tasks.check]
description = "Full quality gate"
depends = ["format:check", "lint", "test"]
```

### Documentation

```toml
[tasks.doc]
description = "Build and open docs"
run = "cargo doc --open --no-deps"

[tasks."doc:check"]
description = "Check doc warnings"
run = "RUSTDOCFLAGS='-D warnings' cargo doc --no-deps"
```

### Development Workflow

```toml
[tasks.watch]
description = "Rebuild on file changes"
run = "cargo watch -x build"

[tasks.run]
description = "Run the binary"
depends = ["build"]
run = "cargo run"

[tasks.install]
description = "Install binary locally"
run = "cargo install --path ."
```

### Workspace Tasks

For Cargo workspaces with multiple crates:

```toml
[tasks."ws:test"]
description = "Test all workspace members"
run = "cargo test --workspace"

[tasks."ws:check"]
description = "Check all workspace members"
run = "cargo check --workspace"
```

## Cross-Compilation

Set target-specific environment variables through `[env]`:

```toml
[env]
CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER = "aarch64-linux-gnu-gcc"

[tasks."build:arm64"]
description = "Cross-compile for ARM64 Linux"
run = "cargo build --release --target aarch64-unknown-linux-gnu"
```

For WASM targets:

```toml
[tasks."build:wasm"]
description = "Build for WASM"
run = "cargo build --release --target wasm32-unknown-unknown"
```

## Cargo Tool Extensions

Install additional Cargo tools through mise backends:

```toml
[tools]
"cargo:cargo-watch" = "latest"
"cargo:cargo-nextest" = "latest"
"cargo:cargo-audit" = "latest"
```

These install as mise-managed tools, separate from the project's `Cargo.toml` dependencies.
