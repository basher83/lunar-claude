---
name: ansible-secrets
description: >
  This skill should be used when working with secrets in Ansible playbooks, integrating
  Infisical vault, using no_log directive, retrieving credentials securely, or
  implementing fallback patterns for secrets. Covers the reusable Infisical lookup task.
---

# Ansible Secrets Management

Secure secrets handling with Infisical integration and proper security practices.

## Architecture Overview

```text
┌──────────────┐
│   Ansible    │
│   Playbook   │
└──────┬───────┘
       │
       │ include_tasks: infisical-secret-lookup.yml
       │
       ▼
┌──────────────────┐
│ Infisical Lookup │
│      Task        │
└──────┬───────────┘
       │
       ├─> Try Universal Auth (preferred)
       │   - INFISICAL_UNIVERSAL_AUTH_CLIENT_ID
       │   - INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET
       │
       ├─> Fallback to Environment Variable (optional)
       │   - Uses specified fallback_env_var
       │
       ▼
┌──────────────┐
│  Infisical   │ (Vault)
│     API      │
└──────────────┘
```

## Reusable Task Pattern

The repository provides a reusable task for secret retrieval at `ansible/tasks/infisical-secret-lookup.yml`.

### Basic Usage

```yaml
- name: Retrieve Proxmox password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/proxmox-cluster'

# Now use the secret
- name: Create Proxmox user
  community.proxmox.proxmox_user:
    api_password: "{{ proxmox_password }}"
    # ... other config ...
  no_log: true
```

### With Fallback

```yaml
- name: Retrieve database password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
    fallback_env_var: 'DB_PASSWORD'  # Falls back to $DB_PASSWORD
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/database'
```

### Task Parameters

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `secret_name` | Yes | - | Name of secret in Infisical |
| `secret_var_name` | Yes | - | Variable name to store secret |
| `infisical_project_id` | No | (repo default) | Infisical project ID |
| `infisical_env` | No | `prod` | Environment (prod, dev, staging) |
| `infisical_path` | No | `/apollo-13/vault` | Path within project |
| `fallback_env_var` | No | - | Env var to use as fallback |
| `allow_empty` | No | `false` | Allow empty secret values |

## Authentication

### Universal Auth (Recommended)

Set environment variables before running playbooks:

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="ua-abc123"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="secret-xyz789"

cd ansible
uv run ansible-playbook playbooks/my-playbook.yml
```

### Environment Fallback

For local development or CI without Infisical:

```bash
export PROXMOX_PASSWORD="local-dev-password"

cd ansible
uv run ansible-playbook playbooks/my-playbook.yml
```

## Security Best Practices

### 1. Use no_log

On tasks that handle secrets:

```yaml
- name: Set database password
  ansible.builtin.command: set-password {{ password }}
  no_log: true

- name: Deploy config with secrets
  ansible.builtin.template:
    src: config.j2
    dest: /etc/app/config.yml
  no_log: true
```

### 2. Avoid Hard-Coded Secrets

```yaml
# BAD - Exposes secrets
- name: Create user
  community.proxmox.proxmox_user:
    api_password: "my-password-123"  # EXPOSED!

# GOOD
- name: Retrieve password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'

- name: Create user
  community.proxmox.proxmox_user:
    api_password: "{{ proxmox_password }}"
  no_log: true
```

### 3. Validate Secret Retrieval

Add validation for critical secrets:

```yaml
- name: Get database password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'

- name: Validate password complexity
  ansible.builtin.assert:
    that:
      - db_password | length >= 16
    fail_msg: "Password doesn't meet complexity requirements"
  no_log: true
```

### 4. Limit Secret Scope

Retrieve secrets only when needed:

```yaml
# GOOD - Retrieve only when needed
- name: System tasks (no secrets)
  ansible.builtin.apt:
    name: nginx
    state: present

- name: Get credentials (only when needed)
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'

- name: Configure database connection
  ansible.builtin.template:
    src: db-config.j2
    dest: /etc/app/db.yml
  no_log: true
```

### 5. Use Environment Isolation

Separate secrets by environment:

```yaml
# Production
- name: Get prod secret
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
    infisical_env: 'prod'
    infisical_path: '/production/database'

# Development
- name: Get dev secret
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
    infisical_env: 'dev'
    infisical_path: '/development/database'
```

## Multiple Secrets Pattern

```yaml
---
- name: Deploy application with secrets
  hosts: app_servers
  become: true

  vars:
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/app-config'

  tasks:
    - name: Retrieve database password
      ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
      vars:
        secret_name: 'DB_PASSWORD'
        secret_var_name: 'db_password'

    - name: Retrieve API key
      ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
      vars:
        secret_name: 'API_KEY'
        secret_var_name: 'api_key'

    - name: Retrieve Redis password
      ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
      vars:
        secret_name: 'REDIS_PASSWORD'
        secret_var_name: 'redis_password'

    - name: Deploy application config
      ansible.builtin.template:
        src: app-config.j2
        dest: /etc/app/config.yml
        owner: app
        group: app
        mode: '0600'
      no_log: true
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy
on: push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Infisical
        env:
          INFISICAL_CLIENT_ID: ${{ secrets.INFISICAL_CLIENT_ID }}
          INFISICAL_CLIENT_SECRET: ${{ secrets.INFISICAL_CLIENT_SECRET }}
        run: |
          echo "INFISICAL_UNIVERSAL_AUTH_CLIENT_ID=$INFISICAL_CLIENT_ID" >> $GITHUB_ENV
          echo "INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET=$INFISICAL_CLIENT_SECRET" >> $GITHUB_ENV

      - name: Run Ansible
        run: |
          cd ansible
          uv run ansible-playbook playbooks/deploy.yml
```

## Troubleshooting

### Missing Authentication

**Error**: Missing Infisical authentication credentials

**Solution**:

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="ua-abc123"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="secret-xyz789"
```

### Secret Not Found

**Error**: Failed to retrieve secret from Infisical

**Check**:

1. Secret exists at specified path in Infisical
2. Correct project_id/env/path
3. Service account has read permission

### Empty Secret Value

**Error**: Secret validation failed (empty value)

**Solutions**:

```yaml
# Option 1: Allow empty (not recommended for required secrets)
- name: Get optional secret
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'OPTIONAL_KEY'
    secret_var_name: 'optional_key'
    allow_empty: true

# Option 2: Use fallback
- name: Get secret with fallback
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'API_KEY'
    secret_var_name: 'api_key'
    fallback_env_var: 'DEFAULT_API_KEY'
```

## Additional Resources

For detailed secrets management patterns, consult:

- **`references/secrets-management.md`** - Infisical integration patterns, no_log best practices, credential security

## Related Skills

- **ansible-fundamentals** - Core Ansible patterns
- **ansible-error-handling** - Error handling for secret retrieval failures
