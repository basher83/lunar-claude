# New Project Setup

## Install mise-en-place for Zsh

`curl https://mise.run/zsh | sh`

## Source the .zshrc to apply changes

`source /home/codespace/.zshrc`

## Trust and install mise-en-place

`mise trust` and `mise install`

## Install Claude Code

`npm install -g @anthropic-ai/claude-code`

## Running Claude Code

`claude` for regular mode

`claude --dangerously-skip-permissions` for unrestricted mode

## Claude settings

- Launch claude code
- Add plugin marketplace for superpowers: `/plugin marketplace add obra/superpowers-marketplace`
- Add plugin for offical anthropic claude code: `/plugin marketplace add anthropics/claude-code`
- Install agent-sdk-dev: `/plugin install agent-sdk-dev@anthropics/claude-code`
- Install superpowers: `/plugin install superpowers@superpowers-marketplace`
- Install elements-of-style: `/plugin install elements-of-style@superpowers-marketplace`
- Restart claude code to apply changes

## VS Code Extensions

- tamasfe.even-better-toml
- davidanson.vscode-markdownlint
