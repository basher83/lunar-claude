---
date: 2026-05-11
status: resolved
tags:
  - hk
  - mise
  - migration
  - validation
---

# hk Custom Syntax Validation for JSON and YAML

## Context

When migrating a repository from the `pre-commit` framework to `hk` via `hk migrate pre-commit`, two of the most common hooks — `check-json` and `check-yaml` — do not map cleanly. The pre-commit hooks of those names perform syntax-only validation: they confirm a file parses without raising an exception. The closest hk builtins are `Builtins.jq` and `Builtins.yamllint`, which do something different.

`Builtins.jq` reformats JSON files and diffs the output against the original, so any cosmetic difference (key ordering, trailing newlines, whitespace) is reported as a failure. `Builtins.yamllint` enforces stylistic rules (line length, indentation, document start markers) on top of syntax validity. Either one will trip on files that the original pre-commit hooks would have passed, which produces false positives during migration and gradually pulls a repository into a stricter style regime that was never an explicit decision.

The hk documentation acknowledges this. From the hk reference packaged with the `repo-forge:mise` skill (`references/hk.md`, under "Known migration mapping issues to review in the generated hk.pkl"):

> `Builtins.yamllint` is a style enforcer (line length, indentation rules), not a syntax validator. The original pre-commit `check-yaml` only validated YAML parses correctly. Replace with a custom syntax check if style enforcement is unwanted.
>
> `Builtins.jq` reformats JSON files and diffs the output. The original `check-json` only validated JSON syntax. Replace with a custom syntax check to avoid unwanted reformatting.

The documented intent is therefore clear: replace these builtins with a custom syntax check. What the docs do not prescribe is *where* the custom check lives. This document records the three valid options and the trade-offs between them.

## The hk `check` field is a shell command

A step in `hk.pkl` declares its check command as a string:

```pkl
["check_json"] {
    glob = "**/*.json"
    check = "<shell command>"
}
```

The shell command can be any executable invocation. Direct binary calls, inline interpreter invocations, paths to script files, and indirections through other task runners all work syntactically. hk does not constrain the shape of `check` beyond it being a runnable shell string. This means at least three implementation styles are valid for a custom JSON or YAML syntax check.

## Three placement options

### Option A: inline in `hk.pkl`

The check command embeds the validator directly in the PKL string:

```pkl
["check_json"] {
    glob = "**/*.json"
    check = "python -c 'import json, sys; [json.load(open(f)) for f in sys.argv[1:]]' {{files}}"
}
```

This keeps all hook logic in a single file. Reading `hk.pkl` tells you everything the pre-commit pipeline does without needing to chase external references. It is the simplest option when the check fits on one line.

The cost is that the embedded program lives inside a PKL string, so it is invisible to language-specific tooling. `shellcheck` cannot lint the shell wrapper, `ruff` cannot lint the Python body, and editors do not get syntax highlighting for the embedded code. Multi-line checks force escape sequences that quickly become unreadable. There is also a known sharp edge with hk 1.36.0's config cache: when a PKL-serialized step round-trips through hk's cache JSON, embedded regex constructions and certain escape patterns can produce `failed to parse cache file: expected regex object, string, or array of strings` warnings. The warnings are non-fatal but persistent.

### Option B: external script in `scripts/`

The check command points at a tracked shell script that wraps the validator:

```pkl
["check_json"] {
    glob = "**/*.json"
    check = "./scripts/check-json.sh"
}
```

```bash
#!/usr/bin/env bash
set -euo pipefail
exec python -c 'import json, sys
for f in sys.argv[1:]:
    json.load(open(f))' "$@"
```

The script is a regular file under version control with the usual affordances. `shellcheck` lints the shell wrapper, the embedded Python is readable without escape soup, and the check can grow to multiple lines without distorting `hk.pkl`.

The cost is one additional file per check and the need to keep `hk.pkl` and the script in sync. The indirection is mild — anyone reading `hk.pkl` sees a path that points at a co-located, similarly-named script — but it is real.

### Option C: mise task

The check command shells out to a `mise.toml`-defined task:

```pkl
["check_json"] {
    glob = "**/*.json"
    check = "mise run check-json -- {{files}}"
}
```

```toml
[tasks."check-json"]
description = "Validate JSON syntax"
run = "python -c 'import json, sys; [json.load(open(f)) for f in sys.argv[1:]]'"
```

The validator becomes invocable from the CLI (`mise run check-json path.json`) and shows up in `mise tasks` alongside the rest of the project's operational surface. The same task can be reused outside the hook context — from CI, from ad hoc shell sessions, from other mise tasks via `depends`.

The cost is that mise is now a runtime dependency of the git hook itself. When the hook fires during a commit, `mise` must be on PATH and the project's `mise.toml` must resolve cleanly. The `HK_MISE=1` integration mode wraps hooks in `mise x`, which makes this dependable when configured, but it still expands the surface area of "what must work for a commit to succeed" beyond a self-contained shell script. There is also a small layering oddity: mise tasks are conventionally developer-facing automation, and using them as the implementation of a hook rather than as a convenience wrapper around the hook can blur that boundary.

## Trade-off summary

| Concern | Inline in `hk.pkl` | External `scripts/` file | `mise run` task |
|---------|-------------------|--------------------------|-----------------|
| Files to maintain | 1 | 2 | 2 |
| Linter coverage of validator body | none | shellcheck + native linter | native linter |
| Readability of multi-line checks | poor | good | good |
| Reusable from CLI | no | yes (run script directly) | yes (`mise run`) |
| Cache-serialization sharp edge in hk 1.36.0 | observed | untested | untested |
| Runtime dependency surface during commit | hk only | hk + shell | hk + shell + mise |
| Discoverability in `mise tasks` | no | no | yes |

## Decision criteria

One repo-specific factor weighs heavily across the trade-offs above: how often the validator needs to be invoked outside the git hook context. When it is purely a hook implementation that no one runs by hand, the simplest placement wins. When the same syntax check is wanted from CI scripts, ad hoc shell sessions, or other tasks in the project, the placements that expose a stable CLI surface (options B and C) earn their indirection.

## Documentation gap

The hk migration documentation prescribes the *intent* (replace `Builtins.jq` and `Builtins.yamllint` with custom syntax checks) but not the *placement* (inline, external script, or task indirection). For a project standardizing on `repo-forge`-style scaffolding, this is the kind of decision that benefits from being made once at the preset level rather than rediscovered per repository. A future iteration of the `repo-forge:mise` skill could express an opinion here, either by emitting a specific placement during `hk init --mise` or by documenting the recommended placement alongside the migration warnings.

## Open questions

Load-bearing claims and decisions that need to be verified against authoritative sources before this document's conclusions can be trusted. Status markers reflect the state recorded in the research log; questions are added as the work surfaces them rather than fixed up front.

1. **(closed; see research-log Q1 Round 2)** Does `hk migrate pre-commit` actually produce the `Builtins.yamllint` and `Builtins.jq` mappings described in the Context section? Resolved by running `hk migrate pre-commit` against a fixture against hk 1.36.0 and reading the literal emitted hk.pkl: yes, it emits `Builtins.jq` and `Builtins.yamllint`. Deepwiki's source-map claim was wrong.
2. **(closed; see research-log Q2)** Is the skill's `references/hk.md` accurate against upstream `hk.jdx.dev`? Specifically the described behaviors of `Builtins.jq`, `Builtins.yamllint`, and the `check` field semantics.
3. **(closed; see research-log Q3)** Is the hk 1.36.0 cache-serialization issue real, and what specifically triggers it? Session evidence in this repo confirms `exclude = Regex(...)` triggers the `failed to parse cache file: expected regex object, string, or array of strings` warning. The option A hypothesis that embedded escape patterns in `check` strings can also trigger it was never isolated, because externalization happened before the Regex root cause was found. Is the issue filed or fixed upstream?
4. **(closed; see research-log Q4 Round 2)** Does `mise run check-json -- {{files}}` work end-to-end as a `check` value? Resolved by fixture: composition works without `HK_MISE=1`, `{{files}}` is shell-safe through the `mise run -- ...` boundary, and a space-containing filename round-tripped to Python's `sys.argv` intact.
5. **(closed; see research-log Q5)** What does hk substitute for `{{files}}` — space-separated unquoted paths, properly quoted, newline-delimited? If a tracked file's path contains a space or shell-special character, do the three options each handle it correctly? Option B's script body uses `"$@"` which is safe regardless of how arguments arrive; options A and C depend on the expansion being shell-safe at the `check` string boundary. Round 2 fixture (under Q4) reinforces this: hk emitted `bad' name.json' valid.json` — single-quoted shell escaping around the space-containing token.
6. **(closed; see research-log Q6)** Do `Builtins.check_yaml` and `Builtins.check_json` exist in the upstream `Builtins.pkl`? Direct inspection of `Builtins.pkl` from the hk 1.36.0 release artifact: no. The document's central premise holds.
7. **(closed; see research-log Q7 and Round 2 mechanism question)** Does `HK_MISE=1` wrapping interact cleanly with `check = "mise run X"` patterns? Round 2 fixture exercised the composition without `HK_MISE=1` and observed no deadlock, no environment rebuild between hk steps. The `mise trust` prompt observed during fixture setup is governed by the documented `trusted_config_paths` / `MISE_TRUSTED_CONFIG_PATHS` setting (and the `mise trust --all` non-interactive command); it is not an immutable cost of Option C. The doc body's recommendation should reflect this rather than warn of an unsolvable onboarding cost.
8. **(open; surfaced by Q3 research; low priority)** Was the cache-serialization bug at hk 1.36.0 triggered specifically by `glob = Regex(...)` or `exclude = Regex(...)`? The regression test in `test/regex_patterns.bats` is named "regex glob pattern cache roundtrip", suggesting `glob`; the local session evidence shows the trigger was `exclude = Regex(...)`. Practically moot since the fix is in hk 1.40.0; left unresolved.
9. **(closed; see Round 2 mechanism question)** Does mise have a built-in auto-update mechanism for tools pinned to `"latest"`, or auto-trust mechanism that avoids the per-clone `mise trust` step? Auto-update: mise itself does not currently provide one (`plugin_autoupdate_last_check_duration` is documented as "not currently implemented"); but the question was asked at the wrong layer — this repository's renovate preset (`local>basher83/renovate-config//presets/mise.json`) auto-merges mise tool bumps, so the auto-update mechanism exists at the repo layer, and `"latest"` is invisible to it. Auto-trust: yes, via `trusted_config_paths` / `MISE_TRUSTED_CONFIG_PATHS` and `mise trust --all`. Residual ambiguity: whether `mise install` ever re-resolves `"latest"` independently of `mise upgrade` is not stated by the consulted mise docs, and is practically irrelevant given the renovate-layer answer.
10. **(closed; surfaced by Round 2 layer-correction)** Why is `version = "latest"` an anti-pattern for mise-managed tools wherever `basher83/renovate-config` is extended? Load-bearing reason: it defeats the operator-configured auto-update mechanism. Renovate's mise manager (`https://docs.renovatebot.com/modules/manager/mise/`) bumps concrete pinned versions; `"latest"` is not a version it resolves against. The preset auto-merges mise tool bumps (`presets/mise.json` in `basher83/renovate-config`: `matchManagers: ["mise"]`, `automerge: true`), so semver-pinned mise tools flow through CI to merge with no human in the loop. Scope of the conclusion: the cause is at the renovate-preset layer, which the operator confirms is extended by all repositories in their system, so the anti-pattern is global to the operator's repos rather than specific to repo-forge. The Q3 cache-serialization observation (hk 1.36.0 persisting in repo-forge long past hk 1.40.0's fix) is one empirical instance of the cost; the same anti-pattern is expected to produce similar drift wherever it appears in the operator's other repos. Recommendation that follows: pin mise tools (hk, and any other entry currently set to `"latest"`) to concrete semvers across the operator's repos. The `repo-forge:mise` skill scaffolding and the `mise-hk-integration.md` doc should encode this opinion so new repos created with that scaffolding inherit semver pins by default rather than re-introducing the anti-pattern.

## Research log

This section records factual data gathered for each open question. It does not draw conclusions or recommend doc revisions — those are the next step. Where a finding comes from a Deepwiki summary rather than direct file inspection, the underlying file path is included so the claim can be verified independently. Contradictions in the gathered evidence are recorded as data, not resolved.

### Q1 findings

The CLI surface of `hk migrate pre-commit` is documented at `https://github.com/jdx/hk/blob/main/docs/cli/migrate/pre-commit.md`. It reads `.pre-commit-config.yaml` (default path; overridable with `--config`) and writes `hk.pkl` (default path; overridable with `--output`).

Per Deepwiki's reading of `src/cli/migrate/pre_commit.rs` in jdx/hk, the migration uses a `builtin_map` lookup and a `convert_known_hook` function to convert known pre-commit hook IDs into Step entries that reference the `Builtins` module. Deepwiki reports that the map entries for `check-json` and `check-yaml` resolve to `Builtins.check_json` and `Builtins.check_yaml` respectively, producing entries of the form `["check-json"] = Builtins.check_json`.

Per Deepwiki's separate search of the same repository (driven by `bin/generate_docs.rs`, which iterates the Builtins module to generate `docs/builtins.md`), `Builtins.check_json` and `Builtins.check_yaml` are not present in the current `Builtins.pkl` among the 90+ defined builtins.

Per Deepwiki's reading of `test/migrate_precommit.bats` (the "apache airflow real-world config" case), the asserted hk.pkl output for that test contains a reference to `Builtins.yamllint`.

**Contradiction logged:** Deepwiki claims both that the migrate source maps `check-yaml` to `Builtins.check_yaml` and that `Builtins.check_yaml` is not defined in Builtins.pkl. The cited test evidence for migrate output references `Builtins.yamllint` rather than `Builtins.check_yaml`. The three statements have not been reconciled by inspecting the migrate source, the Builtins module, or the test files directly.

Verifiable references:

- `https://github.com/jdx/hk/blob/main/docs/cli/migrate/pre-commit.md`
- `src/cli/migrate/pre_commit.rs` (in jdx/hk; not directly inspected this session)
- `bin/generate_docs.rs` (in jdx/hk; not directly inspected this session)
- `test/migrate_precommit.bats`, "apache airflow real-world config" case (in jdx/hk; not directly inspected this session)

Not yet done: running `hk migrate pre-commit` against a fixture `.pre-commit-config.yaml` containing `check-json` and `check-yaml` and observing the literal emitted hk.pkl.

### Q2 findings

The `Builtins.jq` check command, as published at `https://hk.jdx.dev/builtins.html`:

```shell
failed=0
for f in {{ files }};
  do jq . "$f" | diff -u "$f" - || failed=1
done
exit $failed
```

The `Builtins.jq` fix command from the same source:

```shell
for f in {{ files }};
  do tmp=$(mktemp) && jq -S . "$f" > "$tmp" && mv "$tmp" "$f"
done
```

The `Builtins.yamllint` check command, as published at the same URL, is `yamllint --strict {{ files }}`.

The `check` field semantics are described at `https://hk.jdx.dev/configuration.html` as "a command that performs validation without modifying files, such as running a linter in check mode... supports template variables like `{{files}}` to receive the list of target files, and can be configured as a Script to provide platform-specific command variations for Linux, macOS, and Windows."

Verifiable references:

- `https://hk.jdx.dev/builtins.html`
- `https://hk.jdx.dev/configuration.html`
- `https://hk.jdx.dev/hooks.html`

### Q3 findings

Test file `test/regex_patterns.bats` in jdx/hk contains a case named "regex glob pattern cache roundtrip" that runs `hk check` twice and asserts that the second run produces no `failed to parse cache file` warning.

Per Deepwiki, the regression and corresponding fix are attributed to commit `849824df` in jdx/hk, claimed to be authored 2024-03-20 and released in hk `1.40.0`. The commit was not fetched directly this session.

Session `9a56b75d` in this repository (transcript captured 2026-05-10 in checkpoint `7265ecb41802`) observed the warning `failed to parse cache file: ... expected regex object, string, or array of strings at line 1 column 18705` on `mise install` against hk `1.36.0`. The warning was cleared in that session by replacing `exclude = Regex(#"(examples/.*\\.yaml$|specs/.*\\.yaml$)"#)` with `exclude = List("examples/**/*.yaml", "specs/**/*.yaml")` in `hk.pkl`.

This repository's `mise.toml:31` pins `hk = "latest"`. Context7-retrieved examples of hk.pkl from `https://hk.jdx.dev/configuration.html` cite hk releases at `v1.38.0` and `v1.43.0`.

Verifiable references:

- `test/regex_patterns.bats` (in jdx/hk; not directly inspected this session)
- Commit `849824df` (in jdx/hk; not directly inspected this session)
- `/Users/basher8383/3I/workshop/lunar-claude/mise.toml:31`
- Entire checkpoint `7265ecb41802` (session `9a56b75d-bcf5-4156-98f9-92f9b796ee33`)

### Q4 findings

Per Deepwiki's reading of `src/cli/mod.rs` in jdx/mise, an `escape_task_args` function preprocesses arguments after a task name by prefixing flag-like tokens with a `TASK_ARG_ESCAPE_PREFIX` constant, preventing clap from interpreting them as flags to `mise` itself. Arguments after `--` bypass this escaping. An `unescape_task_args` function reverses the prefix before passing arguments to the task command.

Per Deepwiki, the test `e2e/tasks/test_task_double_dash_behavior` in jdx/mise asserts that multiple arguments after `--` are passed as separate arguments to the task's command.

The `Run` struct in `src/cli/run.rs` (per Deepwiki) defines fields `args` and `args_last` for handling task arguments. The CLI usage definition lives at `docs/mise.usage.kdl`.

The mise documentation describes `raw_args = true` as a task-level option that "prevents `mise` from parsing any arguments to the task, forwarding them verbatim, including `--help`."

The mise documentation describes `mise run` as setting up "the mise environment (tools in PATH and environment variables from `mise.toml`) before running the task."

Verifiable references:

- `src/cli/mod.rs` (in jdx/mise; not directly inspected this session)
- `src/cli/run.rs` (in jdx/mise; not directly inspected this session)
- `e2e/tasks/test_task_double_dash_behavior` (in jdx/mise; not directly inspected this session)
- `docs/mise.usage.kdl` (in jdx/mise; not directly inspected this session)

Not yet done: setting up a fixture where hk invokes `mise run check-json -- {{files}}` as a `check` value, executing it, and confirming the validator receives the expected file list.

### Q5 findings

Per Deepwiki's reading of `test/git.bats` in jdx/hk, an expansion test asserts that `{{files}}` resolves to a space-separated list, with the example `echo 'feature.txt main.txt'` shown as the executed command. A similar expansion is shown in `test/regex_patterns.bats` as `files=config.yaml settings.yaml`.

Per Deepwiki, the Windows e2e test file `e2e-win/check.Tests.ps1` includes a case asserting that `{{files}}` "passes clean arguments on Windows (no literal quotes)" and explicitly tests a filename with embedded spaces (`"hello world.txt"`).

The `check` field description at `https://hk.jdx.dev/configuration.html` says `{{files}}` receives "the list of target files" without further elaborating on shell-quoting behavior in prose. The behavior described above is sourced from the test files rather than narrative documentation.

Verifiable references:

- `test/git.bats` (in jdx/hk; not directly inspected this session)
- `test/regex_patterns.bats` (in jdx/hk; not directly inspected this session)
- `e2e-win/check.Tests.ps1` (in jdx/hk; not directly inspected this session)
- `https://hk.jdx.dev/configuration.html`

### Round 2 — closure pass

A second research pass exercised fixtures against the locally-installed hk and inspected the hk release artifact directly. Status changes recorded in the Open questions section above; raw findings below.

Two observations from the fixture work each pose the same shape of question — *does mise have a built-in mechanism for this, or is it on the operator?* — and answering them jointly is more useful than treating them as separate footnotes.

**Does mise have an auto-update mechanism for tools pinned to `"latest"`?**

This question was initially asked at the wrong layer. Auto-update of dev tools is not mise's responsibility in this repository; it is renovate's. The mise-layer answer and the actual-mechanism answer are recorded separately to avoid conflating them.

*Mise-layer answer (the literal question):*

- `https://mise.jdx.dev/configuration/settings.html` lists `plugin_autoupdate_last_check_duration` (env: `MISE_PLUGIN_AUTOUPDATE_LAST_CHECK_DURATION`, default `7d`), and the documentation entry says verbatim: *"this isn't currently implemented."*
- `https://mise.jdx.dev/cli/upgrade.html` documents `mise upgrade` as the explicit command for moving installed tools forward. Default behavior keeps the constraint range in `mise.toml`; `mise upgrade --bump` rewrites the constraint to the absolute latest version.
- Documented: mise has no automatic mechanism at present. Refreshing a `"latest"` pin via mise alone is an explicit `mise upgrade` (or `mise upgrade --bump`) action.

*Actual-mechanism answer (the question that matters for this repo):*

- This repository's `renovate.json` extends `local>basher83/renovate-config`, whose `default.json` includes `presets/mise.json` from the same preset repo. That mise preset (fetched via `gh api repos/basher83/renovate-config/contents/presets/mise.json`) sets `matchManagers: ["mise"]` with `automerge: true` and `groupName: "mise tools"`. Renovate is therefore the configured auto-update mechanism for mise-managed tools in this repo; updates are auto-merged.
- Renovate's mise manager (`https://docs.renovatebot.com/modules/manager/mise/`) updates the primary (first-listed) version per tool entry. It operates on concrete pinned versions; the `"latest"` keyword is not a version renovate's datasources resolve against and is not bumped by the manager.
- Git history confirms the renovate pipeline runs: commits `973dd25 chore(deps): update mise tools (#73)`, `8c03772 chore(deps): update mise tools (#69)`, and several earlier `renovate/mise-tools` PR merges show the loop closing in practice for semver-pinned mise tools.
- Documented answer at the right layer: yes, this repo has an active auto-update mechanism for mise tools. Semver-pinned entries flow through it. `hk = "latest"` does not.

*Consequence for the doc body.* `"latest"` is an anti-pattern in any repository that extends `basher83/renovate-config` (per operator statement in this session: the operator's whole system of repos), and the load-bearing reason is not mise's behavior in isolation — it is that `"latest"` is invisible to the renovate mise manager that would otherwise be bumping the pin. Semver-pinning (e.g., `hk = "1.43.0"`) is what enables the configured auto-update path. Observed downstream effect of the `"latest"` anti-pattern in this env: hk 1.36.0 persisted long enough for the Q3 cache-serialization warning to bite. Renovate would have moved past 1.40.0 on its own had the pin been semver. The scope of the recommendation that follows is therefore global to the operator's repos (anywhere this preset is extended), not local to repo-forge.

**Does mise have an auto-trust mechanism that would avoid the `mise trust` step Q7 surfaced for Option C?**

- `https://mise.jdx.dev/configuration/settings.html` documents `trusted_config_paths` (env: `MISE_TRUSTED_CONFIG_PATHS`, default `[]`): *"any config files under these paths will be trusted without prompting."* The same entry notes that setting it to `["/"]` effectively disables the trust prompt entirely.
- `https://mise.jdx.dev/cli/trust.html` documents `mise trust --all` (trust the config plus its parent-chain in one command) and the inverse `--untrust` / `--ignore`.
- Documented answer: yes. A contributor (or onboarding script) can populate `MISE_TRUSTED_CONFIG_PATHS` to cover the repository tree once, after which the per-clone interactive `mise trust` step is no longer required. `mise trust --all` is the per-repo non-interactive alternative.
- This is load-bearing for Option C's onboarding story: the prompt observed in the Q7 fixture is not an immutable property of the choice to invoke `mise run` from a hook; it is governed by a mise setting with a documented env-var override.

The residual ambiguity below the documented answer: whether `mise install` (as opposed to `mise upgrade`) ever re-resolves a `"latest"` pin against upstream — for example after the on-disk cache for the tool's available versions expires — is not explicitly stated by the consulted docs. Practically irrelevant given the documented answer (refresh is operator-driven), but recorded as a residual question rather than silently assumed. See Open question 9.

#### Q1 Round 2

A fixture `.pre-commit-config.yaml` containing entries for `check-json`, `check-yaml`, and `trailing-whitespace` was passed to `hk migrate pre-commit` against hk 1.36.0. The literal emitted `hk.pkl` was:

```pkl
local linters = new Mapping<String, Step> {
    ["check-json"] = (Builtins.jq) {
        exclude = Regex(#"^\.hk/"#)
    }
    ["check-yaml"] = (Builtins.yamllint) {
        exclude = Regex(#"^\.hk/"#)
    }
    ["trailing-whitespace"] = (Builtins.trailing_whitespace) {
        exclude = Regex(#"^\.hk/"#)
    }
}
```

The Deepwiki-mediated claim in Q1 findings (that the migrate source map points at `Builtins.check_json` / `Builtins.check_yaml`) is empirically contradicted by the migrate tool's actual output. The Q1 entry's third Deepwiki claim — that the apache-airflow migrate test asserts `Builtins.yamllint` in the output — is consistent with this fixture run.

Verifiable references:

- Local hk 1.36.0 binary, invocation `hk migrate pre-commit --config <fixture>.yaml --output <fixture>.pkl`
- Fixture artifacts captured in the session's working directory at the time of the run

#### Q6 Round 2

The `Builtins.pkl` shipped inside `~/.pkl/cache/.../hk@1.36.0.zip` was inspected directly. It defines 115 builtins. The `check_*` entries present are: `check_added_large_files`, `check_byte_order_marker`, `check_case_conflict`, `check_conventional_commit`, `check_executables_have_shebangs`, `check_merge_conflict`. Neither `check_json` nor `check_yaml` is defined. The `jq` and `yamllint` builtins are present and their check commands match the Q2 findings from `hk.jdx.dev/builtins.html`.

The doc's central premise (migration produces style-enforcing mappings which must be replaced with custom checks) holds for hk 1.36.0. Whether a later hk release introduces `Builtins.check_json` / `Builtins.check_yaml` would need to be re-verified by inspecting that release's `Builtins.pkl` directly.

Verifiable references:

- `~/.pkl/cache/.../hk@1.36.0.zip` (local pkl cache)

#### Q4 Round 2

A fixture repository was constructed with a step declared as:

```pkl
check = "mise run check-json-task -- {{files}}"
```

and a `mise.toml` task `check-json-task` that invokes Python and prints `sys.argv[1:]`. Two staged files were used: `valid.json` and `bad name.json` (the latter chosen to exercise the shell-escaping question from Q5). After `mise trust`, `hk check` ran the step and the captured output was:

```text
[check-json-task] $ uv run --with pyyaml python -c '...'
OK got files: ['bad name.json', 'valid.json']
```

The composition `hk check → mise run X -- {{files}}` works end-to-end. `mise run` accepts `--` passthrough cleanly. Both filenames arrived intact in `sys.argv`, including the space-containing one.

The hk command logged for that step prior to mise's own re-quoting was `mise run check-json-task -- bad' name.json' valid.json`, which is the empirical answer to Q5: hk single-quotes shell-special segments at the `{{files}}` substitution boundary, preserving the shell-safety property described there.

Verifiable references:

- Fixture repository constructed during the session; hk 1.36.0 + mise local install

#### Q7 Round 2

The Q4 fixture exercised the composition without setting `HK_MISE=1`. No deadlock occurred. No observable environment rebuild happened between hk steps within a single `hk check` invocation. The full `mise x → hk → mise run` three-layer composition described in the Q7 open-questions text was not exercised in this round; the worry that prompted Q7 (deadlock, rebuild) was not observed in the simpler two-layer composition either.

A separate observation surfaced during the same fixture work: `mise` refuses to load an untrusted config file. The first attempt to run the fixture produced `mise ERROR ... are not trusted` until `mise trust` was run in the fixture directory. For Option C, this means a fresh clone of a repo using `check = "mise run X"` will fail at the first commit until the contributor runs `mise trust`. This is independent of `HK_MISE=1`.

Verifiable references:

- Fixture repository constructed during the session
- mise CLI behavior at hk 1.36.0 / locally installed mise

#### Q8

Not exercised this round. Practically moot — the cache-serialization fix is in hk 1.40.0 — but the specific `glob` vs `exclude` trigger remains unresolved.

---

## Resolution (2026-06-09)

The steering decision was made and the load-bearing conclusions (Q3, Q10) were actioned. The cache-serialization warning that motivated this research has two layers, both addressed:

- **Root cause — the `"latest"` pin (Q10).** `hk = "latest"` defeated the renovate mise manager, stranding hk at 1.36.0 long past the 1.40.0 fix (Q3). Fixed in `lunar-claude/mise.toml` by pinning all eight `"latest"` tools to concrete semvers (`hk = "1.47.0"`, etc.); renovate now maintains them. The `repo-forge:mise` skill (`SKILL.md` Tool Version Management) and this doc's sibling `mise-hk-integration.md` now encode the semver-pin policy so scaffolded repos inherit it rather than re-introducing the anti-pattern.
- **Trigger — the `Regex(...)` step field.** `lunar-claude/hk.pkl` was switched from `exclude = Regex(...)` to an equivalent `List(...)` of globs (version-independent; verified `check_yaml` matches the same 4 files), and `hk.pkl`'s schema bumped to 1.47.0. `references/hk.md` now warns that `hk migrate pre-commit` emits `Regex` excludes and recommends glob excludes plus hk ≥ 1.40.0.

Q8 (whether `glob` vs `exclude` Regex was the trigger) remains the only open item and is moot — both round-trip cleanly on hk ≥ 1.40.0. The doc-body documentation gap (§Documentation gap: which placement `hk init --mise` should emit for custom JSON/YAML checks) is unrelated to the cache bug and is left as a separate future enhancement to the skill.
