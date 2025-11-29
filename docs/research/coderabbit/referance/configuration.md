# Configuration reference

> Complete reference for CodeRabbit configuration options with detailed explanations, types, and examples.

<Info>
  This reference is automatically generated from the CodeRabbit configuration
  schema. Last updated: 2025-11-04
</Info>

CodeRabbit's behavior can be customized using a `.coderabbit.yaml` file in your repository root. This reference covers all available configuration options with clear property names and examples.

<CardGroup cols={2}>
  <Card title="Quick Start" icon="rocket" href="/getting-started/configure-coderabbit">
    Get started with basic configuration
  </Card>

  <Card title="YAML config examples" icon="file-code" href="https://github.com/coderabbitai/awesome-coderabbit/tree/main/configs">
    Browse example configurations
  </Card>
</CardGroup>

## Configuration Sections

<CardGroup cols={2}>
  <Card title="Code Reviews" icon="git-pull-request" href="#reviews">
    Configure automatic code reviews, tools, and review behavior
  </Card>

  <Card title="Chat & Integrations" icon="message-circle" href="#chat">
    Set up chat features and third-party integrations
  </Card>

  <Card title="Knowledge Base" icon="brain" href="#knowledge-base">
    Configure learning and knowledge sharing features
  </Card>

  <Card title="Code Generation" icon="code" href="#code-generation">
    Settings for docstrings and unit test generation
  </Card>
</CardGroup>

## Reviews

Settings related to reviews.

### Example Configuration

```yaml .coderabbit.yaml theme={null}
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
reviews:
  profile: chill
  high_level_summary: true
  auto_review:
    enabled: true
    drafts: false
  # update to the tools you use, see full list: https://docs.coderabbit.ai/tools/list
  tools:
    eslint:
      enabled: true
    gitleaks:
      enabled: true

```

### Reference

<ResponseField name="profile" type="enum">
  Set the profile for reviews. Assertive profile yields more feedback, that may be considered nitpicky.

  One of the following: `chill`, `assertive`

  Defaults to `"chill"`.
</ResponseField>

<ResponseField name="request_changes_workflow" type="boolean">
  Approve the review once CodeRabbit’s comments are resolved and no pre-merge checks are in an error state. Note: In GitLab, all discussions must be resolved.

  Defaults to `false`.
</ResponseField>

<ResponseField name="high_level_summary" type="boolean">
  Generate a high level summary of the changes in the PR/MR description.

  Defaults to `true`.
</ResponseField>

<ResponseField name="high_level_summary_placeholder" type="string">
  Placeholder in the PR/MR description that gets replaced with the high level summary.

  Defaults to `"@coderabbitai summary"`.
</ResponseField>

<ResponseField name="high_level_summary_in_walkthrough" type="boolean">
  Include the high level summary in the walkthrough comment.

  Defaults to `false`.
</ResponseField>

<ResponseField name="auto_title_placeholder" type="string">
  Add this keyword in the PR/MR title to auto-generate the title.

  Defaults to `"@coderabbitai"`.
</ResponseField>

<ResponseField name="auto_title_instructions" type="string">
  Auto Title Instructions | Custom instructions for auto-generating the PR/MR title.

  Defaults to `""`.
</ResponseField>

<ResponseField name="review_status" type="boolean">
  Post review details on each review. Additionally, post a review status when a review is skipped in certain cases.

  Defaults to `true`.
</ResponseField>

<ResponseField name="commit_status" type="boolean">
  Set the commit status to 'pending' when the review is in progress and 'success' when it is complete.

  Defaults to `true`.
</ResponseField>

<ResponseField name="fail_commit_status" type="boolean">
  Set the commit status to 'failure' when the PR cannot be reviewed by CodeRabbit for any reason.

  Defaults to `false`.
</ResponseField>

<ResponseField name="collapse_walkthrough" type="boolean">
  Generate walkthrough in a markdown collapsible section.

  Defaults to `false`.
</ResponseField>

<ResponseField name="changed_files_summary" type="boolean">
  Generate a summary of the changed files in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="sequence_diagrams" type="boolean">
  Generate sequence diagrams in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="estimate_code_review_effort" type="boolean">
  Estimate the code review effort in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="assess_linked_issues" type="boolean">
  Generate an assessment of how well the changes address the linked issues in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="related_issues" type="boolean">
  Include possibly related issues in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="related_prs" type="boolean">
  Related PRs | Include possibly related pull requests in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="suggested_labels" type="boolean">
  Suggest labels based on the changes in the pull request in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="labeling_instructions" type="array of object">
  Labeling Instructions | Provide guidelines for suggesting labels for the PR/MR. When specific labels or instructions are provided, only those labels are considered, though previous examples are still used to inform the suggestions. If no such labels are provided, suggestions are based solely on previous PR/MRs.

  Defaults to `[]`.

  <Expandable title="Array Items">
    <ResponseField name="label" type="string">
      Label to suggest for the PR/MR. Example: frontend
    </ResponseField>

    <ResponseField name="instructions" type="string">
      Instructions for the label. Example: Apply when the PR/MR contains changes to the react components.

      <Note>
        Max length: 3000
      </Note>
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="auto_apply_labels" type="boolean">
  Automatically apply the suggested labels to the PR/MR.

  Defaults to `false`.
</ResponseField>

<ResponseField name="suggested_reviewers" type="boolean">
  Suggest reviewers based on the changes in the pull request in the walkthrough.

  Defaults to `true`.
</ResponseField>

<ResponseField name="auto_assign_reviewers" type="boolean">
  Automatically assign suggested reviewers to the pull request

  Defaults to `false`.
</ResponseField>

<ResponseField name="in_progress_fortune" type="boolean">
  Post an in-progress fortune message while the review is in progress.

  Defaults to `true`.
</ResponseField>

<ResponseField name="poem" type="boolean">
  Generate a poem in the walkthrough comment.

  Defaults to `true`.
</ResponseField>

<ResponseField name="path_filters" type="array of string">
  Specify file patterns to include or exclude in a review using glob patterns (e.g., !dist/**, src/**). These patterns also apply to 'git sparse-checkout', including specified patterns and ignoring excluded ones (starting with '!') when cloning the repository.

  Defaults to `[]`.
</ResponseField>

<ResponseField name="path_instructions" type="array of object">
  Path Instructions | Provide specific additional guidelines for code review based on file paths.

  Defaults to `[]`.

  <Expandable title="Array Items">
    <ResponseField name="path" type="string">
      File path glob pattern. Example: \*\*/\*.js
    </ResponseField>

    <ResponseField name="instructions" type="string">
      Provides specific additional guidelines for code review based on file paths.

      <Note>
        Max length: 20000
      </Note>
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="abort_on_close" type="boolean">
  Abort the in-progress review if the pull request is closed or merged.

  Defaults to `true`.
</ResponseField>

<ResponseField name="disable_cache" type="boolean">
  Disable caching of code and dependencies. This will force CodeRabbit to download the code and dependencies fresh from the repository each time.

  Defaults to `false`.
</ResponseField>

<ResponseField name="auto_review" type="object">
  Configuration for auto review

  Defaults to `{}`.

  <Expandable title="Auto review">
    <ResponseField name="enabled" type="boolean">
      Automatic Review | Automatic code review

      Defaults to `true`.
    </ResponseField>

    <ResponseField name="auto_incremental_review" type="boolean">
      Automatic Incremental Review | Automatic incremental code review on each push

      Defaults to `true`.
    </ResponseField>

    <ResponseField name="ignore_title_keywords" type="array of string">
      Ignore reviewing if the title of the pull request contains any of these keywords (case-insensitive).

      Defaults to `[]`.
    </ResponseField>

    <ResponseField name="labels" type="array of string">
      List of labels to control which PRs/MRs to review. Labels starting with '!' are negative matches. Examples: \['bug', 'feature'] - reviews PRs with 'bug' OR 'feature' label. \['!wip'] - reviews all PRs except those with 'wip' label. \['bug', '!wip'] - reviews PRs with 'bug' label but not if they have 'wip' label.

      Defaults to `[]`.
    </ResponseField>

    <ResponseField name="drafts" type="boolean">
      Review draft PRs/MRs.

      Defaults to `false`.
    </ResponseField>

    <ResponseField name="base_branches" type="array of string">
      Base branches (other than the default branch) to review. Accepts regex patterns. Use '.\*' to match all branches.

      Defaults to `[]`.
    </ResponseField>

    <ResponseField name="ignore_usernames" type="array of string">
      Ignore reviewing pull requests by these usernames. These should match the Git platform usernames exactly, not the email addresses.

      Defaults to `[]`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="finishing_touches" type="object">
  Configuration for finishing touches

  Defaults to `{}`.

  <Expandable title="Finishing touches">
    <ResponseField name="docstrings" type="object">
      Docstrings | Options for generating Docstrings for your PRs/MRs.

      Defaults to `{}`.

      <Expandable title="Docstrings">
        <ResponseField name="enabled" type="boolean">
          Docstrings | Allow CodeRabbit to generate docstrings for PRs/MRs.

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="unit_tests" type="object">
      Unit Tests | Options for generating unit tests for your PRs/MRs.

      Defaults to `{}`.

      <Expandable title="Unit tests">
        <ResponseField name="enabled" type="boolean">
          Unit Tests | Allow CodeRabbit to generate unit tests for PRs/MRs.

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="pre_merge_checks" type="object">
  Configuration for pre merge checks

  Defaults to `{}`.

  <Expandable title="Pre merge checks">
    <ResponseField name="docstrings" type="object">
      Docstring Coverage | Checks if the code has sufficient docstrings.

      Defaults to `{}`.

      <Expandable title="Docstrings">
        <ResponseField name="mode" type="enum">
          Mode | Determines how strictly the docstring coverage check is enforced. Warning will only generate a warning and does not require the user to resolve the check. Error requires the user to resolve issues before merging the pull request. If set to error and the request changes workflow is enabled, the pull request will be blocked until the issues are resolved.

          One of the following: `off`, `warning`, `error`

          Defaults to `"warning"`.
        </ResponseField>

        <ResponseField name="threshold" type="number">
          Percentage threshold for docstring coverage check.

          Defaults to `80`.

          <Note>
            Min: 0, Max: 100
          </Note>
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="title" type="object">
      Title Check | Checks if the pull request title is appropriate and follows best practices.

      Defaults to `{}`.

      <Expandable title="Title">
        <ResponseField name="mode" type="enum">
          Mode | Determines how strictly the title check is enforced. Warning will only generate a warning and does not require the user to resolve the check. Error requires the user to resolve issues before merging the pull request. If set to error and the request changes workflow is enabled, the pull request will be blocked until the issues are resolved.

          One of the following: `off`, `warning`, `error`

          Defaults to `"warning"`.
        </ResponseField>

        <ResponseField name="requirements" type="string">
          Requirements | Requirements for the pull request title. Example: 'Title should be concise and descriptive, ideally under 50 characters.'

          Defaults to `""`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="description" type="object">
      Description Check | Checks if the pull request description is appropriate and follows best practices.

      Defaults to `{}`.

      <Expandable title="Description">
        <ResponseField name="mode" type="enum">
          Mode | Determines how strictly the description check is enforced. Warning will only generate a warning and does not require the user to resolve the check. Error requires the user to resolve issues before merging the pull request. If set to error and the request changes workflow is enabled, the pull request will be blocked until the issues are resolved.

          One of the following: `off`, `warning`, `error`

          Defaults to `"warning"`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="issue_assessment" type="object">
      Linked Issue Assessment | Checks if the pull request addresses the linked issues. Generate an assessment of how well the changes address the linked issues.

      Defaults to `{}`.

      <Expandable title="Issue assessment">
        <ResponseField name="mode" type="enum">
          Mode | Determines how strictly the issue assessment check is enforced. Warning will only generate a warning and does not require the user to resolve the check. Error requires the user to resolve issues before merging the pull request. If set to error and the request changes workflow is enabled, the pull request will be blocked until the issues are resolved.

          One of the following: `off`, `warning`, `error`

          Defaults to `"warning"`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="custom_checks" type="array of object">
      Custom Pre-merge Checks | Add unique checks to enforce your team's standards before merging a pull request. Each check must have a unique name (up to 50 characters) and clear instructions (up to 10000 characters). Use these to automatically verify coding, security, documentation, or business rules and maintain code quality.

      Defaults to `[]`.

      <Expandable title="Array Items">
        <ResponseField name="mode" type="enum">
          Mode | Determines how strictly the custom check is enforced. Warning will only generate a warning and does not require the user to resolve the check. Error requires the user to resolve issues before merging the pull request. If set to error and the request changes workflow is enabled, the pull request will be blocked until the issues are resolved.

          One of the following: `off`, `warning`, `error`

          Defaults to `"warning"`.
        </ResponseField>

        <ResponseField name="name" type="string">
          Name | Name of the custom check. Maximum length is 50 characters.

          Defaults to `""`.

          <Note>
            Min length: 1, Max length: 50
          </Note>
        </ResponseField>

        <ResponseField name="instructions" type="string">
          Instructions | Please ensure that the instructions specify conditions that deterministically result in a clear pass or fail outcome. The maximum length for this field is 10,000 characters.

          Defaults to `""`.

          <Note>
            Min length: 1, Max length: 10000
          </Note>
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="tools" type="object">
  Tools that provide additional context to code reviews.

  Defaults to `{}`.

  <Expandable title="Tools">
    <ResponseField name="ast-grep" type="object">
      Enable ast-grep | ast-grep is a code analysis tool that helps you to find patterns in your codebase using abstract syntax trees patterns. | v0.39.7

      Defaults to `{}`.

      <Expandable title="Ast-grep">
        <ResponseField name="rule_dirs" type="array of string">
          List of rules directories.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="util_dirs" type="array of string">
          List of utils directories.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="essential_rules" type="boolean">
          Use ast-grep essentials package.

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="packages" type="array of string">
          Predefined packages to be used.

          Defaults to `[]`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="shellcheck" type="object">
      ShellCheck is a static analysis tool that finds bugs in your shell scripts.

      Defaults to `{}`.

      <Expandable title="Shellcheck">
        <ResponseField name="enabled" type="boolean">
          Enable ShellCheck | ShellCheck is a static analysis tool that finds bugs in your shell. | Enable ShellCheck integration. | v0.11.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="ruff" type="object">
      Ruff is a Python linter and code formatter.

      Defaults to `{}`.

      <Expandable title="Ruff">
        <ResponseField name="enabled" type="boolean">
          Enable Ruff | Ruff is a Python linter and code formatter. |  Enable Ruff integration. | v0.14.3

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="markdownlint" type="object">
      markdownlint-cli2 is a static analysis tool to enforce standards and consistency for Markdown files.

      Defaults to `{}`.

      <Expandable title="Markdownlint">
        <ResponseField name="enabled" type="boolean">
          Enable markdownlint | markdownlint-cli2 is a static analysis tool to enforce standards and consistency for Markdown files. | Enable markdownlint integration. | v0.18.1

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="github-checks" type="object">
      GitHub Checks integration configuration.

      Defaults to `{}`.

      <Expandable title="Github-checks">
        <ResponseField name="enabled" type="boolean">
          Enable GitHub Checks
          \| Enable integration, defaults to true
          \| Enable GitHub Checks integration.

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="timeout_ms" type="number">
          Time in milliseconds to wait for all GitHub Checks to conclude. Default 90 seconds, max 15 minutes (900000ms).

          Defaults to `90000`.

          <Note>
            Min: 0, Max: 900000
          </Note>
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="languagetool" type="object">
      LanguageTool is a style and grammar checker for 30+ languages.

      Defaults to `{}`.

      <Expandable title="Languagetool">
        <ResponseField name="enabled" type="boolean">
          Enable LanguageTool | Enable LanguageTool integration.

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="enabled_rules" type="array of string">
          IDs of rules to be enabled. The rule won't run unless 'level' is set to a level that activates the rule.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="disabled_rules" type="array of string">
          IDs of rules to be disabled. Note: EN\_UNPAIRED\_BRACKETS, and EN\_UNPAIRED\_QUOTES are always disabled.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="enabled_categories" type="array of string">
          IDs of categories to be enabled.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="disabled_categories" type="array of string">
          IDs of categories to be disabled. Note: TYPOS, TYPOGRAPHY, and CASING are always disabled.

          Defaults to `[]`.
        </ResponseField>

        <ResponseField name="enabled_only" type="boolean">
          Only the rules and categories whose IDs are specified with 'enabledRules' or 'enabledCategories' are enabled.

          Defaults to `false`.
        </ResponseField>

        <ResponseField name="level" type="enum">
          If set to 'picky', additional rules will be activated, i.e. rules that you might only find useful when checking formal text.

          One of the following: `default`, `picky`

          Defaults to `"default"`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="biome" type="object">
      Biome is a fast formatter, linter, and analyzer for web projects.

      Defaults to `{}`.

      <Expandable title="Biome">
        <ResponseField name="enabled" type="boolean">
          Enable Biome | Biome is a fast formatter, linter, and analyzer for web projects. | Enable Biome integration. | v2.1.2

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="hadolint" type="object">
      Hadolint is a Dockerfile linter.

      Defaults to `{}`.

      <Expandable title="Hadolint">
        <ResponseField name="enabled" type="boolean">
          Enable Hadolint | Hadolint is a Dockerfile linter. | Enable Hadolint integration. | v2.14.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="swiftlint" type="object">
      SwiftLint integration configuration object.

      Defaults to `{}`.

      <Expandable title="Swiftlint">
        <ResponseField name="enabled" type="boolean">
          Enable SwiftLint | SwiftLint is a Swift linter. | Enable SwiftLint integration. | v0.57.0

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="config_file" type="string">
          Optional path to the SwiftLint configuration file relative to the repository. This is useful when the configuration file is named differently than the default '.swiftlint.yml' or '.swiftlint.yaml'.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="phpstan" type="object">
      PHPStan is a tool to analyze PHP code.

      Defaults to `{}`.

      <Expandable title="Phpstan">
        <ResponseField name="enabled" type="boolean">
          Enable PHPStan | PHPStan requires [config file](https://phpstan.org/config-reference#config-file) in your repository root. Please ensure that this file contains the `paths:` parameter. | v2.1.31

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="level" type="enum">
          Level | Specify the [rule level](https://phpstan.org/user-guide/rule-levels) to run. This setting is ignored if your configuration file already has a `level:` parameter.

          One of the following: `default`, `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `max`

          Defaults to `"default"`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="phpmd" type="object">
      PHPMD is a tool to find potential problems in PHP code.

      Defaults to `{}`.

      <Expandable title="Phpmd">
        <ResponseField name="enabled" type="boolean">
          Enable PHPMD | PHPMD is a tool to find potential problems in PHP code. | v2.15.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="phpcs" type="object">
      PHP CodeSniffer is a PHP linter and coding standard checker.

      Defaults to `{}`.

      <Expandable title="Phpcs">
        <ResponseField name="enabled" type="boolean">
          Enable PHP CodeSniffer | PHP CodeSniffer is a PHP linter and coding standard checker. | v3.7.2

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="golangci-lint" type="object">
      golangci-lint is a fast linters runner for Go.

      Defaults to `{}`.

      <Expandable title="Golangci-lint">
        <ResponseField name="enabled" type="boolean">
          Enable golangci-lint | golangci-lint is a fast linters runner for Go. | Enable golangci-lint integration. | v2.5.0

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="config_file" type="string">
          Optional path to the golangci-lint configuration file relative to the repository. Useful when the configuration file is named differently than the default '.golangci.yml', '.golangci.yaml', '.golangci.toml', '.golangci.json'.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="yamllint" type="object">
      YAMLlint is a linter for YAML files.

      Defaults to `{}`.

      <Expandable title="Yamllint">
        <ResponseField name="enabled" type="boolean">
          Enable YAMLlint | YAMLlint is a linter for YAML files. | Enable YAMLlint integration. | v1.37.1

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="gitleaks" type="object">
      Gitleaks is a secret scanner.

      Defaults to `{}`.

      <Expandable title="Gitleaks">
        <ResponseField name="enabled" type="boolean">
          Enable Gitleaks | Gitleaks is a secret scanner. | Enable Gitleaks integration. | v8.28.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="checkov" type="object">
      Checkov is a static code analysis tool for infrastructure-as-code files.

      Defaults to `{}`.

      <Expandable title="Checkov">
        <ResponseField name="enabled" type="boolean">
          Enable Checkov | Checkov is a static code analysis tool for infrastructure-as-code files. | v3.2.334

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="detekt" type="object">
      Detekt is a static code analysis tool for Kotlin files.

      Defaults to `{}`.

      <Expandable title="Detekt">
        <ResponseField name="enabled" type="boolean">
          Enable detekt | detekt is a static code analysis tool for Kotlin files. | v1.23.8

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="config_file" type="string">
          Optional path to the detekt configuration file relative to the repository.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="eslint" type="object">
      ESLint is a static code analysis tool for JavaScript files.

      Defaults to `{}`.

      <Expandable title="Eslint">
        <ResponseField name="enabled" type="boolean">
          Enable ESLint | ESLint is a static code analysis tool for JavaScript files.

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="flake8" type="object">
      Flake8 is a Python linter that wraps PyFlakes, pycodestyle and Ned Batchelder's McCabe script.

      Defaults to `{}`.

      <Expandable title="Flake8">
        <ResponseField name="enabled" type="boolean">
          Enable Flake8 | Flake8 is a Python linter that wraps PyFlakes, pycodestyle and Ned Batchelder's McCabe script. | v7.3.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="rubocop" type="object">
      RuboCop is a Ruby static code analyzer (a.k.a. linter ) and code formatter.

      Defaults to `{}`.

      <Expandable title="Rubocop">
        <ResponseField name="enabled" type="boolean">
          Enable RuboCop | RuboCop is a Ruby static code analyzer (a.k.a. linter ) and code formatter. | v1.81.7

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="buf" type="object">
      Buf offers linting for Protobuf files.

      Defaults to `{}`.

      <Expandable title="Buf">
        <ResponseField name="enabled" type="boolean">
          Enable Buf | Buf offers linting for Protobuf files. | v1.59.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="regal" type="object">
      Regal is a linter and language server for Rego.

      Defaults to `{}`.

      <Expandable title="Regal">
        <ResponseField name="enabled" type="boolean">
          Enable Regal | Regal is a linter and language server for Rego. | v0.36.1

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="actionlint" type="object">
      actionlint is a static checker for GitHub Actions workflow files.

      Defaults to `{}`.

      <Expandable title="Actionlint">
        <ResponseField name="enabled" type="boolean">
          Enable actionlint | is a static checker for GitHub Actions workflow files. | v1.7.8

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="pmd" type="object">
      PMD is an extensible multilanguage static code analyzer. It’s mainly concerned with Java.

      Defaults to `{}`.

      <Expandable title="Pmd">
        <ResponseField name="enabled" type="boolean">
          Enable PMD | PMD is an extensible multilanguage static code analyzer. It’s mainly concerned with Java. | v7.18.0

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="config_file" type="string">
          Optional path to the PMD configuration file relative to the repository.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="clang" type="object">
      Configuration for Clang to perform static analysis on C and C++ code

      Defaults to `{}`.

      <Expandable title="Clang">
        <ResponseField name="enabled" type="boolean">
          Enable Clang for C/C++ static analysis and code quality checks | v14.0.6

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="cppcheck" type="object">
      Cppcheck is a static code analysis tool for the C and C++ programming languages.

      Defaults to `{}`.

      <Expandable title="Cppcheck">
        <ResponseField name="enabled" type="boolean">
          Enable Cppcheck | Cppcheck is a static code analysis tool for the C and C++ programming languages. | v2.18.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="semgrep" type="object">
      Semgrep is a static analysis tool designed to scan code for security vulnerabilities and code quality issues.

      Defaults to `{}`.

      <Expandable title="Semgrep">
        <ResponseField name="enabled" type="boolean">
          Enable Semgrep | Semgrep is a static analysis tool designed to scan code for security vulnerabilities and code quality issues. | Enable Semgrep integration. | v1.142.0

          Defaults to `true`.
        </ResponseField>

        <ResponseField name="config_file" type="string">
          Optional path to the Semgrep configuration file relative to the repository.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="circleci" type="object">
      CircleCI tool is a static checker for CircleCI config files.

      Defaults to `{}`.

      <Expandable title="Circleci">
        <ResponseField name="enabled" type="boolean">
          Enable CircleCI | CircleCI tool is a static checker for CircleCI config files. | v0.1.33494

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="clippy" type="object">
      Clippy is a collection of lints to catch common mistakes and improve your Rust code.

      Defaults to `{}`.

      <Expandable title="Clippy">
        <ResponseField name="enabled" type="boolean">
          Enable Clippy | Clippy is a collection of lints to catch common mistakes and improve your Rust code. | Enable Clippy integration.

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="sqlfluff" type="object">
      SQLFluff is an open source, dialect-flexible and configurable SQL linter.

      Defaults to `{}`.

      <Expandable title="Sqlfluff">
        <ResponseField name="enabled" type="boolean">
          Enable SQLFluff | SQLFluff is an open source, dialect-flexible and configurable SQL linter. | v3.5.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="prismaLint" type="object">
      Configuration for Prisma Schema linting to ensure schema file quality

      Defaults to `{}`.

      <Expandable title="Prisma Lint">
        <ResponseField name="enabled" type="boolean">
          Enable Prisma Schema linting | Prisma Schema linting helps maintain consistent and error-free schema files | v0.10.3

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="pylint" type="object">
      Pylint is a Python static code analysis tool.

      Defaults to `{}`.

      <Expandable title="Pylint">
        <ResponseField name="enabled" type="boolean">
          Enable Pylint | Pylint is a Python static code analysis tool. | v4.0.2

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="oxc" type="object">
      Oxlint is a JavaScript/TypeScript linter for OXC written in Rust.

      Defaults to `{}`.

      <Expandable title="Oxc">
        <ResponseField name="enabled" type="boolean">
          Enable Oxlint | Oxlint is a JavaScript/TypeScript linter for OXC written in Rust. | v1.25.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="shopifyThemeCheck" type="object">
      Configuration for Shopify Theme Check to ensure theme quality and best practices

      Defaults to `{}`.

      <Expandable title="Shopify Theme Check">
        <ResponseField name="enabled" type="boolean">
          Enable Shopify Theme Check | A linter for Shopify themes that helps you follow Shopify theme & Liquid best practices | cli 3.84.2 | theme 3.58.2

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="luacheck" type="object">
      Configuration for Lua code linting to ensure code quality

      Defaults to `{}`.

      <Expandable title="Luacheck">
        <ResponseField name="enabled" type="boolean">
          Enable Lua code linting | Luacheck helps maintain consistent and error-free Lua code | v1.2.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="brakeman" type="object">
      Brakeman is a static analysis security vulnerability scanner for Ruby on Rails applications. | v7.1.0

      Defaults to `{}`.

      <Expandable title="Brakeman">
        <ResponseField name="enabled" type="boolean">
          Enable Brakeman | Brakeman is a static analysis security vulnerability scanner for Ruby on Rails applications. | v7.1.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="dotenvLint" type="object">
      dotenv-linter is a tool for checking and fixing .env files for problems and best practices

      Defaults to `{}`.

      <Expandable title="Dotenv Lint">
        <ResponseField name="enabled" type="boolean">
          Enable dotenv-linter | dotenv-linter is a tool for checking and fixing .env files for problems and best practices | v4.0.0

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="htmlhint" type="object">
      HTMLHint is a static code analysis tool for HTML files.

      Defaults to `{}`.

      <Expandable title="Htmlhint">
        <ResponseField name="enabled" type="boolean">
          Enable HTMLHint | HTMLHint is a static code analysis tool for HTML files. | Enable HTMLHint integration. | v1.7.1

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="checkmake" type="object">
      checkmake is a linter for Makefiles.

      Defaults to `{}`.

      <Expandable title="Checkmake">
        <ResponseField name="enabled" type="boolean">
          Enable checkmake | checkmake is a linter for Makefiles. | v0.2.2

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="osvScanner" type="object">
      OSV Scanner is a tool for vulnerability package scanning.

      Defaults to `{}`.

      <Expandable title="Osv Scanner">
        <ResponseField name="enabled" type="boolean">
          Enable OSV Scanner | OSV Scanner is a tool for vulnerability package scanning | v2.2.4

          Defaults to `true`.
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

## Chat

Configuration for chat

### Example Configuration

```yaml .coderabbit.yaml theme={null}
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
chat:
  auto_reply: true
  integrations:
    jira:
      usage: enabled

```

### Reference

<ResponseField name="art" type="boolean">
  Generate art in response to chat messages. CodeRabbit expresses emotions as either ASCII or Emoji art.

  Defaults to `true`.
</ResponseField>

<ResponseField name="auto_reply" type="boolean">
  Enable the bot to reply automatically without requiring the user to tag it.

  Defaults to `true`.
</ResponseField>

<ResponseField name="integrations" type="object">
  Configuration for integrations

  Defaults to `{}`.

  <Expandable title="Integrations">
    <ResponseField name="jira" type="object">
      Configuration for jira

      Defaults to `{}`.

      <Expandable title="Jira">
        <ResponseField name="usage" type="enum">
          Jira | Enable the Jira integration for opening issues, etc. 'auto' disables the integration for public repositories.

          One of the following: `auto`, `enabled`, `disabled`

          Defaults to `"auto"`.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="linear" type="object">
      Configuration for linear

      Defaults to `{}`.

      <Expandable title="Linear">
        <ResponseField name="usage" type="enum">
          Linear | Enable the Linear integration for opening issues, etc. 'auto' disables the integration for public repositories.

          One of the following: `auto`, `enabled`, `disabled`

          Defaults to `"auto"`.
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

## Knowledge base

Configuration for knowledge base

### Example Configuration

```yaml .coderabbit.yaml theme={null}
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
knowledge_base:
  opt_out: false
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/.cursorrules"
      - "**/CODING_STANDARDS.md"

```

### Reference

<ResponseField name="opt_out" type="boolean">
  Opt Out | Disable all knowledge base features that require data retention. If you opt out after opting in, all of your existing knowledge base data will be removed from the system.

  Defaults to `false`.
</ResponseField>

<ResponseField name="web_search" type="object">
  Configuration for web search

  Defaults to `{}`.

  <Expandable title="Web search">
    <ResponseField name="enabled" type="boolean">
      Web Search | Enable the web search integration.

      Defaults to `true`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="code_guidelines" type="object">
  CodeRabbit will analyse and learn from your organization's code guidelines, which you can mention in the file patterns section. These guidelines will then be used to conduct thorough code reviews.

  Defaults to `{}`.

  <Expandable title="Code guidelines">
    <ResponseField name="enabled" type="boolean">
      Enabled | Enable CodeRabbit to enforce your organization's coding standards during reviews.

      Defaults to `true`.
    </ResponseField>

    <ResponseField name="filePatterns" type="array of string">
      File Patterns | Specify files for your coding guideline documents in this section. CodeRabbit will scan these files to understand your team's standards and apply them during code reviews. Multiple files supported. File names are case-sensitive. Common files like: (\*\*/.cursorrules, .github/copilot-instructions.md, .github/instructions/*.instructions.md, \*\*/CLAUDE.md, \*\*/GEMINI.md, \*\*/.cursor/rules/*, \*\*/.windsurfrules, \*\*/.clinerules/*, \*\*/.rules/*, \*\*/AGENT.md, \*\*/AGENTS.md) are included by default.

      Defaults to `[]`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="learnings" type="object">
  Configuration for learnings

  Defaults to `{}`.

  <Expandable title="Learnings">
    <ResponseField name="scope" type="enum">
      Learnings | Specify the scope of learnings to use for the knowledge base. 'local' uses the repository's learnings, 'global' uses the organization's learnings, and 'auto' uses repository's learnings for public repositories and organization's learnings for private repositories.

      One of the following: `local`, `global`, `auto`

      Defaults to `"auto"`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="issues" type="object">
  Configuration for issues

  Defaults to `{}`.

  <Expandable title="Issues">
    <ResponseField name="scope" type="enum">
      Issues | Specify the scope of git platform (GitHub/GitLab) issues to use for the knowledge base. 'local' uses the repository's issues, 'global' uses the organization's issues, and 'auto' uses repository's issues for public repositories and organization's issues for private repositories.

      One of the following: `local`, `global`, `auto`

      Defaults to `"auto"`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="jira" type="object">
  Configuration for jira

  Defaults to `{}`.

  <Expandable title="Jira">
    <ResponseField name="usage" type="enum">
      Jira | Enable the Jira knowledge base integration. 'auto' disables the integration for public repositories.

      One of the following: `auto`, `enabled`, `disabled`

      Defaults to `"auto"`.
    </ResponseField>

    <ResponseField name="project_keys" type="array of string">
      Jira Project Keys | Specify the Jira project keys to use for the knowledge base.

      Defaults to `[]`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="linear" type="object">
  Configuration for linear

  Defaults to `{}`.

  <Expandable title="Linear">
    <ResponseField name="usage" type="enum">
      Linear | Enable the Linear knowledge base integration. 'auto' disables the integration for public repositories.

      One of the following: `auto`, `enabled`, `disabled`

      Defaults to `"auto"`.
    </ResponseField>

    <ResponseField name="team_keys" type="array of string">
      Linear Team Keys | Specify the Linear team keys (identifiers) to use for the knowledge base. E.g. 'ENG'

      Defaults to `[]`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="pull_requests" type="object">
  Configuration for pull requests

  Defaults to `{}`.

  <Expandable title="Pull requests">
    <ResponseField name="scope" type="enum">
      Pull Requests | Specify the scope of pull requests to use for the knowledge base. 'local' uses the repository's pull requests, 'global' uses the organization's pull requests, and 'auto' uses repository's pull requests for public repositories and organization's pull requests for private repositories.

      One of the following: `local`, `global`, `auto`

      Defaults to `"auto"`.
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="mcp" type="object">
  Configuration for mcp

  Defaults to `{}`.

  <Expandable title="Mcp">
    <ResponseField name="usage" type="enum">
      MCP | Enable the MCP knowledge base integration. 'auto' disables the integration for public repositories.

      One of the following: `auto`, `enabled`, `disabled`

      Defaults to `"auto"`.
    </ResponseField>

    <ResponseField name="disabled_servers" type="array of string">
      MCP Disabled Servers | Specify MCP server labels to disable (case-insensitive). These servers will be excluded from reviews and knowledge base queries.

      Defaults to `[]`.
    </ResponseField>
  </Expandable>
</ResponseField>

## Code generation

Configuration for code generation

### Example Configuration

```yaml .coderabbit.yaml theme={null}
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
code_generation:
  docstrings:
    language: en-US
  unit_tests:
    path_instructions: []

```

### Reference

<ResponseField name="docstrings" type="object">
  Settings related to the generation of docstrings.

  Defaults to `{"path_instructions":[]}`.

  <Expandable title="Docstrings">
    <ResponseField name="language" type="enum">
      Set the language for docstrings by using the corresponding ISO language code.

      One of the following: `de`, `de-DE`, `de-AT`, `de-CH`, `en`, `en-US`, `en-AU`, `en-GB`, `en-CA`, `en-NZ`, `en-ZA`, `es`, `es-AR`, `fr`, `fr-CA`, `fr-CH`, `fr-BE`, `nl`, `nl-BE`, `pt-AO`, `pt`, `pt-BR`, `pt-MZ`, `pt-PT`, `ar`, `ast-ES`, `ast`, `be-BY`, `be`, `br-FR`, `br`, `ca-ES`, `ca`, `ca-ES-valencia`, `ca-ES-balear`, `da-DK`, `da`, `de-DE-x-simple-language`, `el-GR`, `el`, `eo`, `fa`, `ga-IE`, `ga`, `gl-ES`, `gl`, `it`, `ja-JP`, `ja`, `km-KH`, `km`, `ko-KR`, `ko`, `pl-PL`, `pl`, `ro-RO`, `ro`, `ru-RU`, `ru`, `sk-SK`, `sk`, `sl-SI`, `sl`, `sv`, `ta-IN`, `ta`, `tl-PH`, `tl`, `tr`, `uk-UA`, `uk`, `zh-CN`, `zh`, `crh-UA`, `crh`, `cs-CZ`, `cs`, `nb`, `no`, `nl-NL`, `de-DE-x-simple-language-DE`, `es-ES`, `it-IT`, `fa-IR`, `sv-SE`, `de-LU`, `fr-FR`, `bg-BG`, `bg`, `he-IL`, `he`, `hi-IN`, `hi`, `vi-VN`, `vi`, `th-TH`, `th`, `bn-BD`, `bn`

      Defaults to `"en-US"`.
    </ResponseField>

    <ResponseField name="path_instructions" type="array of object">
      Path Instructions | Provide additional guidelines for docstring generation based on file paths.

      Defaults to `[]`.

      <Expandable title="Array Items">
        <ResponseField name="path" type="string">
          File path glob pattern. Example: \*\*/\*.js
        </ResponseField>

        <ResponseField name="instructions" type="string">
          Provides additional guidelines for docstring generation based on file paths.

          <Note>
            Max length: 20000
          </Note>
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

<ResponseField name="unit_tests" type="object">
  Settings related to the generation of unit tests.

  Defaults to `{"path_instructions":[]}`.

  <Expandable title="Unit tests">
    <ResponseField name="path_instructions" type="array of object">
      Unit Test Generation | Provide additional guidelines for unit test generation based on file paths.

      Defaults to `[]`.

      <Expandable title="Array Items">
        <ResponseField name="path" type="string">
          File path glob pattern. Example: \*\*/\*.js
        </ResponseField>

        <ResponseField name="instructions" type="string">
          Provides additional guidelines for unit test generation based on file paths.

          <Note>
            Max length: 20000
          </Note>
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Expandable>
</ResponseField>

## Global Settings

<Info>
  These settings apply to your entire CodeRabbit configuration across all
  repositories.
</Info>

### Example Configuration

```yaml .coderabbit.yaml theme={null}
# yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
language: en-US
tone_instructions: "Be concise and focus on critical issues only"
early_access: false

```

### Reference

<ResponseField name="language" type="enum">
  Set the language for reviews by using the corresponding ISO language code.

  One of the following: `de`, `de-DE`, `de-AT`, `de-CH`, `en`, `en-US`, `en-AU`, `en-GB`, `en-CA`, `en-NZ`, `en-ZA`, `es`, `es-AR`, `fr`, `fr-CA`, `fr-CH`, `fr-BE`, `nl`, `nl-BE`, `pt-AO`, `pt`, `pt-BR`, `pt-MZ`, `pt-PT`, `ar`, `ast-ES`, `ast`, `be-BY`, `be`, `br-FR`, `br`, `ca-ES`, `ca`, `ca-ES-valencia`, `ca-ES-balear`, `da-DK`, `da`, `de-DE-x-simple-language`, `el-GR`, `el`, `eo`, `fa`, `ga-IE`, `ga`, `gl-ES`, `gl`, `it`, `ja-JP`, `ja`, `km-KH`, `km`, `ko-KR`, `ko`, `pl-PL`, `pl`, `ro-RO`, `ro`, `ru-RU`, `ru`, `sk-SK`, `sk`, `sl-SI`, `sl`, `sv`, `ta-IN`, `ta`, `tl-PH`, `tl`, `tr`, `uk-UA`, `uk`, `zh-CN`, `zh`, `crh-UA`, `crh`, `cs-CZ`, `cs`, `nb`, `no`, `nl-NL`, `de-DE-x-simple-language-DE`, `es-ES`, `it-IT`, `fa-IR`, `sv-SE`, `de-LU`, `fr-FR`, `bg-BG`, `bg`, `he-IL`, `he`, `hi-IN`, `hi`, `vi-VN`, `vi`, `th-TH`, `th`, `bn-BD`, `bn`

  Defaults to `"en-US"`.
</ResponseField>

<ResponseField name="tone_instructions" type="string">
  Set the tone of reviews and chat. Example: 'You must use talk like Mr. T. I pity the fool who doesn't!'

  Defaults to `""`.

  <Note>Max length: 250</Note>
</ResponseField>

<ResponseField name="early_access" type="boolean">
  Enable early-access features.

  Defaults to `false`.
</ResponseField>

<ResponseField name="enable_free_tier" type="boolean">
  Enable free tier features for users not on a paid plan.

  Defaults to `true`.
</ResponseField>

## Configuration Examples

<Tabs>
  <Tab title="Basic Setup" icon="rocket">
    Perfect for getting started with CodeRabbit.

    ```yaml .coderabbit.yaml theme={null}
    # yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
    language: en-US
    reviews:
      profile: assertive
      high_level_summary: true
      high_level_summary_in_walkthrough: true
      auto_review:
        enabled: true
        drafts: false
      #to auto generate the title of your pull request, put the placeholder when creating it: @coderabbitai, it then follows the auto_title_instructions below:
      auto_title_instructions: "use conventional commits structure: <type>[optional scope]: <description>"
      collapse_walkthrough: true
      suggested_labels: false
      poem: false
      # add linters and other tools, CodeRabbit will run and check these as part of its review process. See a list of supported tools: https://docs.coderabbit.ai/tools/list
      tools:
        eslint:
          enabled: true
    ```

  </Tab>

  <Tab title="Advanced Setup" icon="settings">
    Comprehensive configuration with multiple tools and custom settings.

    ```yaml .coderabbit.yaml theme={null}
    # yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
    language: en-US
    tone_instructions: "You are a principal engineer with natural teaching abilities. You detect issues and clearly explain why."
    reviews:
      profile: assertive
      high_level_summary: true
      #paths to ignore, customize for your stack
      path_filters:
        - "!node_modules/**"
        - "!dist/**"
        - "src/**"
    # add linters and other tools, CodeRabbit will run and check these as part of its review process. See a list of supported tools: https://docs.coderabbit.ai/tools/list
      tools:
        eslint:
          enabled: true
        ruff:
          enabled: true
        gitleaks:
          enabled: true
      auto_review:
        enabled: true
        drafts: false
        ignore_title_keywords:
          - "wip"
          - "draft"
    knowledge_base:
      # Coding guidelines automatically detects major coding agents, Cursor, Claude Code, Gemini, et. al. If you keep custom coding standards or other documents, say architectural patterns, add them as file patterns.
      code_guidelines:
        enabled: true
        filePatterns:
          - "**/architecture-pattern.md"
          - "**/technology-stack-and-usage.md"
          - "**/CODING_STANDARDS.md"
    ```

  </Tab>

  <Tab title="Team Setup" icon="users">
    Configuration optimized for team collaboration.

    ```yaml .coderabbit.yaml theme={null}
    # yaml-language-server: $schema=https://coderabbit.ai/integrations/schema.v2.json
    language: en-US
    reviews:
      profile: chill
      high_level_summary: true
      suggested_reviewers: true
      auto_assign_reviewers: true
      # Automatically generate docstrings and unit tests for your PRs
      finishing_touches:
        docstrings:
          enabled: true
        unit_tests:
          enabled: true
      # Quality gates that run before merging. Set mode to 'error' to block PRs that don't meet requirements
      pre_merge_checks:
        title:
          mode: error
          requirements: "Title should follow conventional commit structure"
        description:
          mode: warning
    chat:
      art: false
      auto_reply: true
      # Enable integrations with issue tracking systems like Linear, Jira, etc.
      integrations:
        linear:
          usage: enabled
    knowledge_base:
      # Enable web search for additional context during reviews
      web_search:
        enabled: true
      # Use 'auto' if you have both public and private repos: uses repository-specific for public, organization-wide for private
      learnings:
        scope: global
      # Use 'auto' if you have both public and private repos: uses repository-specific for public, organization-wide for private
      issues:
        scope: global
    ```

  </Tab>
</Tabs>

## Related Resources

<CardGroup cols={3}>
  <Card title="Review Commands" icon="terminal" href="/reference/review-commands">
    Learn about @coderabbitai commands
  </Card>

  <Card title="Supported Tools" icon="wrench" href="/reference/tools-reference">
    Browse all supported linters and analyzers
  </Card>

  <Card title="Best Practices" icon="star" href="/guides/setup-best-practices">
    Configuration tips and recommendations
  </Card>
</CardGroup>
