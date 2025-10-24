# Docker Deployment with Infisical Secrets

**Learning objective:** See best practices in action - secrets management, error handling, and idempotency.

## What This Example Demonstrates

This playbook showcases **production-ready Ansible patterns** from Virgo-Core:

✅ **Secrets Management:**
- Infisical integration using reusable task
- Fallback to environment variables
- `no_log: true` on sensitive tasks

✅ **Error Handling:**
- Pre-flight checks with `assert`
- `changed_when` for idempotency
- `failed_when` for graceful failures
- Block/rescue for rollback

✅ **Best Practices:**
- Fully qualified module names (FQCN)
- Task organization with blocks
- Handlers for service restarts
- Verification steps

✅ **Docker Operations:**
- Idempotent container management
- Health checks with retries
- Proper logging on failures

## Prerequisites

### 1. Infisical Setup

**Universal Auth credentials:**

```bash
export INFISICAL_UNIVERSAL_AUTH_CLIENT_ID="ua-abc123"
export INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET="secret-xyz789"
```

**OR fallback environment variables:**

```bash
export DB_PASSWORD="fallback-db-password"
export API_KEY="fallback-api-key"
export REDIS_PASSWORD="fallback-redis-password"
```

### 2. Ansible Collections

```bash
# Install required collections
cd ../../..  # Back to ansible directory
uv run ansible-galaxy collection install -r requirements.yml
```

### 3. Target Hosts

Update inventory with Docker hosts:

```ini
# inventory/hosts
[docker_hosts]
docker-01-nexus.spaceships.work
```

### 4. Templates (create these)

The playbook references templates you need to create:

**`templates/app-config.yml.j2`:**
```yaml
database:
  host: db.spaceships.work
  password: "{{ db_password }}"

api:
  key: "{{ api_key }}"

redis:
  host: redis.spaceships.work
  password: "{{ redis_password }}"
```

**`templates/docker-compose.yml.j2`:**
```yaml
version: '3.8'
services:
  app:
    image: your-app:latest
    environment:
      - CONFIG_FILE=/config/config.yml
    volumes:
      - {{ app_dir }}/config.yml:/config/config.yml:ro
    ports:
      - "8080:8080"
```

## Quick Start

### 1. Validate Playbook

**Syntax check:**
```bash
ansible-playbook docker-deployment.yml --syntax-check
```

**Lint check:**
```bash
ansible-lint docker-deployment.yml
```

**Dry run:**
```bash
ansible-playbook docker-deployment.yml --check
```

### 2. Run Playbook

```bash
# Full deployment
ansible-playbook -i ../../inventory/hosts docker-deployment.yml

# Specific tags
ansible-playbook -i ../../inventory/hosts docker-deployment.yml --tags secrets
ansible-playbook -i ../../inventory/hosts docker-deployment.yml --tags deploy
ansible-playbook -i ../../inventory/hosts docker-deployment.yml --tags verify
```

### 3. Verify Deployment

```bash
# Check application health
curl http://docker-01-nexus.spaceships.work:8080/health

# Check Docker containers
ssh ansible@docker-01-nexus.spaceships.work "docker ps"
```

## Understanding the Patterns

### Pattern 1: Infisical Secret Lookup

**The Pattern:**
```yaml
- name: Retrieve database password from Infisical
  ansible.builtin.include_tasks: ../../tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'DB_PASSWORD'
    secret_var_name: 'db_password'
    fallback_env_var: 'DB_PASSWORD'
```

**Why it works:**
- Reusable task (DRY principle)
- Validates authentication before retrieving
- Fallback to environment for local dev
- No secrets in logs
- Clear error messages

**Learn more:** [../../patterns/secrets-management.md](../../patterns/secrets-management.md)

### Pattern 2: Pre-flight Validation

**The Pattern:**
```yaml
pre_tasks:
  - name: Validate required variables
    ansible.builtin.assert:
      that:
        - app_name is defined
      fail_msg: "Required variables not set"

  - name: Check if Docker is installed
    ansible.builtin.command: which docker
    register: docker_check
    changed_when: false  # Check doesn't change state
    failed_when: false   # Don't fail yet
```

**Why it works:**
- Fails fast with clear messages
- Prevents partial deployments
- Uses `changed_when: false` for checks
- Uses `failed_when: false` to check result later

### Pattern 3: Idempotent Docker Operations

**The Pattern:**
```yaml
- name: Check if container is already running
  ansible.builtin.command: docker ps --filter name={{ app_name }}
  register: container_check
  changed_when: false

- name: Start Docker containers
  ansible.builtin.command: docker-compose up -d
  register: compose_up
  changed_when: "'Creating' in compose_up.stderr or 'Starting' in compose_up.stderr"
  when: container_check.stdout != app_name
```

**Why it works:**
- Check first, then create
- Only reports "changed" if actually started something
- Conditional execution with `when:`
- True idempotency

### Pattern 4: Block/Rescue Error Handling

**The Pattern:**
```yaml
- name: Docker Management Block
  block:
    - name: Pull images
      # ... tasks ...

  rescue:
    - name: Show container logs on failure
      ansible.builtin.command: docker-compose logs --tail=50
      register: container_logs

    - name: Report failure
      ansible.builtin.fail:
        msg: "Deployment failed: {{ container_logs.stdout }}"
```

**Why it works:**
- Groups related tasks
- Automatic rollback on failure
- Provides debugging info
- Clean error reporting

**Learn more:** [../../patterns/error-handling.md](../../patterns/error-handling.md)

### Pattern 5: Health Checks with Retries

**The Pattern:**
```yaml
- name: Wait for application to be healthy
  ansible.builtin.uri:
    url: "http://localhost:8080/health"
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 30
  delay: 10
```

**Why it works:**
- Automatic retries for transient failures
- Configurable timeout (30 × 10s = 5 minutes)
- Fails clearly if never becomes healthy

## Common Mistakes Avoided

This playbook avoids common anti-patterns:

### ❌ Anti-pattern 1: Hard-coded Secrets

```yaml
# DON'T DO THIS!
- name: Deploy config
  ansible.builtin.template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    db_password: "MyPassword123"  # NEVER!
```

✅ **This playbook:** Uses Infisical with fallback to environment

### ❌ Anti-pattern 2: Missing changed_when

```yaml
# DON'T DO THIS!
- name: Start container
  ansible.builtin.command: docker start myapp
  # Always reports "changed" even if already running
```

✅ **This playbook:** Checks first, uses `changed_when` to detect actual changes

### ❌ Anti-pattern 3: No Error Handling

```yaml
# DON'T DO THIS!
- name: Deploy app
  ansible.builtin.command: deploy.sh
  # No check if it worked, no cleanup on failure
```

✅ **This playbook:** Uses block/rescue, verifies success

### ❌ Anti-pattern 4: Secrets in Logs

```yaml
# DON'T DO THIS!
- name: Set password
  ansible.builtin.command: set-password {{ password }}
  # Password visible in Ansible output!
```

✅ **This playbook:** Uses `no_log: true` on sensitive tasks

## Customization

### Different Application

Change variables:

```yaml
vars:
  app_name: "my-other-app"
  app_dir: "/opt/my-other-app"
```

### Different Secrets

Add more secret retrievals:

```yaml
- name: Retrieve JWT secret
  ansible.builtin.include_tasks: ../../tasks/infisical-secret-lookup.yml
  vars:
    secret_name: 'JWT_SECRET'
    secret_var_name: 'jwt_secret'
```

### Skip Health Check

```bash
ansible-playbook docker-deployment.yml --skip-tags verify
```

## Troubleshooting

### Infisical Authentication Failed

**Error:** `Missing Infisical authentication credentials`

**Solution:**
```bash
# Check environment variables
echo $INFISICAL_UNIVERSAL_AUTH_CLIENT_ID
echo $INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET

# OR use fallback
export DB_PASSWORD="fallback-password"
```

### Docker Not Installed

**Error:** `Docker is not installed`

**Solution:**
```bash
# Install Docker on target host
ssh ansible@docker-host
sudo apt update
sudo apt install docker.io docker-compose
```

### Container Won't Start

**Error:** `Docker deployment failed`

**Solution:** Playbook shows logs automatically in rescue block. Review output for errors.

**Manual check:**
```bash
ssh ansible@docker-host
cd /opt/my-application
docker-compose logs
```

### Health Check Timeout

**Error:** `Wait for application to be healthy` times out

**Solution:**
```yaml
# Increase retries/delay
retries: 60  # 10 minutes
delay: 10
```

## Testing the Playbook

### Check Idempotency

```bash
# Run twice - second run should show no changes
ansible-playbook docker-deployment.yml
ansible-playbook docker-deployment.yml  # Should be all "ok", no "changed"
```

### Run Linters

```bash
# Ansible lint
ansible-lint docker-deployment.yml

# Custom idempotency check
../../tools/check_idempotency.py docker-deployment.yml

# Full lint suite
../../tools/lint-all.sh
```

## Next Steps

### Learn More Patterns

- **Error Handling:** [../../patterns/error-handling.md](../../patterns/error-handling.md)
- **Secrets Management:** [../../patterns/secrets-management.md](../../patterns/secrets-management.md)
- **Common Mistakes:** [../../anti-patterns/common-mistakes.md](../../anti-patterns/common-mistakes.md)

### Additional Examples

- **Basic Playbook:** `../01-basic-playbook/` - Simpler starting point
- **Repository Playbooks:** `../../../ansible/playbooks/` - Real production playbooks

### Best Practices

Review the main skill:
- [../../SKILL.md](../../SKILL.md) - Complete best practices guide

## Why These Patterns Matter

**In Production:**
- ✅ Secrets never in version control
- ✅ Playbooks are truly idempotent
- ✅ Clear error messages for troubleshooting
- ✅ Audit trail for all operations
- ✅ Rollback on failures

**For Teams:**
- ✅ Consistent patterns across playbooks
- ✅ Easy to understand and maintain
- ✅ Self-documenting code
- ✅ Reduced bus factor

**For You:**
- ✅ Confidence in deployments
- ✅ Less time debugging
- ✅ Better sleep at night!
