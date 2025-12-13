# Secrets Management with Infisical

## Overview

This repository uses **Infisical** for centralized secrets management in Ansible playbooks.
This pattern eliminates hard-coded credentials and provides audit trails for secret access.

## Architecture

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

### The Infisical Lookup Task

**Location:** `ansible/tasks/infisical-secret-lookup.yml`

**Purpose:** Reusable task for secure secret retrieval with validation and fallback.

**Key Features:**

1. **Validates input parameters** - Ensures secret_name and secret_var_name are provided
2. **Checks authentication** - Validates Universal Auth credentials or fallback
3. **Retrieves secret** - Fetches from Infisical with project/env/path context
4. **Validates retrieval** - Ensures secret was actually retrieved
5. **Uses `no_log`** - Prevents secrets from appearing in logs
6. **Supports fallback** - Can fall back to environment variables

### Usage Pattern

**Basic usage:**

```yaml
- name: Retrieve Proxmox password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/doggos-cluster'

# Now use the secret
- name: Create Proxmox user
  community.proxmox.proxmox_user:
    api_password: "{{ proxmox_password }}"
    # ... other config ...
  no_log: true
```

**With fallback to environment variable:**

```yaml
- name: Retrieve database password
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
    fallback_env_var: 'DB_PASSWORD'  # Falls back to $DB_PASSWORD if Infisical fails
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/database'
```

**Allow empty values (optional):**

```yaml
- name: Retrieve optional API key
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'OPTIONAL_API_KEY'
    secret_var_name: 'api_key'
    allow_empty: true  # Won't fail if secret is empty
```

## Required Variables

### Task Parameters

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `secret_name` | Yes | - | Name of secret in Infisical |
| `secret_var_name` | Yes | - | Variable name to store retrieved secret |
| `infisical_project_id` | No | `7b832220-...` | Infisical project ID |
| `infisical_env` | No | `prod` | Environment slug (prod, dev, staging) |
| `infisical_path` | No | `/apollo-13/vault` | Path within Infisical project |
| `fallback_env_var` | No | - | Environment variable to use as fallback |
| `allow_empty` | No | `false` | Whether to allow empty secret values |

### Environment Variables

**Universal Auth (Preferred):**

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="your-client-id"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="your-client-secret"
```

**Fallback (Optional):**

```bash
export PROXMOX_PASSWORD="fallback-password"
```

## Authentication Methods

### Universal Auth (Recommended)

**Setup:**

1. Create service account in Infisical
2. Generate Universal Auth credentials
3. Set environment variables

**Usage:**

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="ua-abc123"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="secret-xyz789"

cd ansible
uv run ansible-playbook playbooks/my-playbook.yml
```

### Fallback to Environment Variables

**When to use:**

- Local development
- CI/CD pipelines without Infisical access
- Emergency fallback

**Usage:**

```yaml
- name: Get API token
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'API_TOKEN'
    secret_var_name: 'api_token'
    fallback_env_var: 'API_TOKEN'  # Falls back to $API_TOKEN
```

## Real-World Examples

### Example 1: Proxmox Template Creation

**From:** `ansible/playbooks/proxmox-build-template.yml`

```yaml
---
- name: Build Proxmox VM template
  hosts: proxmox_nodes
  gather_facts: false

  vars:
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/doggos-cluster'

  tasks:
    - name: Retrieve Proxmox credentials
      ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
      vars:
        secret_name: 'PROXMOX_PASSWORD'
        secret_var_name: 'proxmox_password'
        fallback_env_var: 'PROXMOX_PASSWORD'

    - name: Download cloud image
      ansible.builtin.get_url:
        url: "{{ cloud_image_url }}"
        dest: "/tmp/{{ image_name }}"
        checksum: "{{ cloud_image_checksum }}"
      # ... rest of playbook ...
```

### Example 2: Terraform User Creation

**From:** `ansible/playbooks/proxmox-create-terraform-user.yml`

```yaml
---
- name: Create Terraform service user in Proxmox
  hosts: proxmox_nodes
  become: true

  vars:
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/doggos-cluster'

  tasks:
    - name: Retrieve Proxmox API credentials
      ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
      vars:
        secret_name: 'PROXMOX_ROOT_PASSWORD'
        secret_var_name: 'proxmox_root_password'

    - name: Create system user
      ansible.builtin.user:
        name: terraform
        comment: "Terraform automation user"
        shell: /bin/bash
        state: present
      no_log: true

    - name: Create Proxmox API token
      ansible.builtin.command: >
        pveum user token add terraform@pam terraform-token
      register: token_result
      changed_when: "'already exists' not in token_result.stderr"
      failed_when:
        - token_result.rc != 0
        - "'already exists' not in token_result.stderr"
      no_log: true
```

### Example 3: Multiple Secrets

```yaml
---
- name: Deploy application with multiple secrets
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
      vars:
        database_url: "postgres://user:{{ db_password }}@db.example.com/app"
        api_key: "{{ api_key }}"
        redis_url: "redis://:{{ redis_password }}@redis.example.com:6379"
      no_log: true
```

## Security Best Practices

### 1. Always Use `no_log`

**On secret retrieval:**

```yaml
- name: Get secret
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'PASSWORD'
    secret_var_name: 'password'
  # no_log: true (already in included task)
```

**On tasks using secrets:**

```yaml
- name: Use secret in command
  ansible.builtin.command: create-user --password {{ password }}
  no_log: true  # CRITICAL: Prevents password in logs
```

### 2. Never Hard-Code Secrets

**❌ Bad:**

```yaml
- name: Create user
  community.proxmox.proxmox_user:
    api_password: "my-password-123"  # DON'T DO THIS!
```

**✅ Good:**

```yaml
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

The reusable task automatically validates secrets, but you can add additional checks:

```yaml
- name: Get secret
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'

- name: Validate password format
  ansible.builtin.assert:
    that:
      - db_password | length >= 16
      - db_password is regex('^[A-Za-z0-9!@#$%^&*()]+$')
    fail_msg: "Password doesn't meet complexity requirements"
  no_log: true
```

### 4. Use Project/Environment Isolation

**Separate secrets by environment:**

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

### 5. Limit Secret Scope

Only retrieve secrets when needed, not at playbook start:

**✅ Good:**

```yaml
- name: System tasks (no secrets needed)
  ansible.builtin.apt:
    name: nginx
    state: present

# Only retrieve secret when needed
- name: Get credentials
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

## Troubleshooting

### Error: Missing Infisical authentication credentials

**Cause:** Universal Auth environment variables not set

**Solution:**

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="ua-abc123"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="secret-xyz789"
```

### Error: Failed to retrieve secret from Infisical

**Possible causes:**

1. Secret doesn't exist in specified path
2. Wrong project_id/env/path
3. Insufficient permissions

**Debug:**

```yaml
- name: Debug secret retrieval
  ansible.builtin.include_tasks: tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'TEST_SECRET'
    secret_var_name: 'test_secret'
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/test'
  # Check Infisical UI to verify secret exists at this path
```

### Error: Secret validation failed (empty value)

**Cause:** Secret retrieved but value is empty

**Solutions:**

```yaml
# Option 1: Allow empty values
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

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy with Infisical
on: push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Infisical credentials
        env:
          INFISICAL_CLIENT_ID: ${{ secrets.INFISICAL_CLIENT_ID }}
          INFISICAL_CLIENT_SECRET: ${{ secrets.INFISICAL_CLIENT_SECRET }}
        run: |
          echo "INFISICAL_UNIVERSAL_AUTH_CLIENT_ID=$INFISICAL_CLIENT_ID" >> $GITHUB_ENV
          echo "INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET=$INFISICAL_CLIENT_SECRET" >> $GITHUB_ENV

      - name: Run Ansible playbook
        run: |
          cd ansible
          uv run ansible-playbook playbooks/deploy.yml
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  variables:
    INFISICAL_UNIVERSAL_AUTH_CLIENT_ID: $INFISICAL_CLIENT_ID
    INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET: $INFISICAL_CLIENT_SECRET
  script:
    - cd ansible
    - uv run ansible-playbook playbooks/deploy.yml
```

## Further Reading

- [Infisical Documentation](https://infisical.com/docs)
- [Infisical Ansible Collection](https://github.com/Infisical/ansible-collection)
- [Ansible no_log Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/logging.html)
