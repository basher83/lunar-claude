# Test Scenarios

Reference catalog for plugin evaluation. **Do NOT load this document during sessions.**

Memorize the command and requirements, run session, evaluate after.

## Invocation Method

All scenarios use **slash commands** to properly initialize the pipeline:

```text
/ansible-workflows:create-playbook <name> [--hosts <target>]
/ansible-workflows:create-role <name>
```

After the command scaffolds the structure, provide requirements as a follow-up message
to guide the generator agent.

## Simple Complexity

### S01: Docker Installation

**Command:**

```text
/ansible-workflows:create-playbook setup-docker
```

**Follow-up requirements:**

```text
Install Docker CE on Ubuntu 22.04 hosts with proper GPG key verification and HTTPS transport
```

**Expected patterns:**

- apt_key or get_url for GPG key
- apt_repository for Docker repo
- apt for docker-ce package
- service/systemd for docker daemon
- User added to docker group (optional)

**Quality signals:**

- FQCN throughout
- Handlers for service restart
- Idempotent key/repo addition

### S02: UFW Firewall

**Command:**

```text
/ansible-workflows:create-playbook configure-firewall
```

**Follow-up requirements:**

```text
Configure UFW firewall with SSH, HTTP, HTTPS, and Proxmox cluster ports (8006, 5900-5999)
```

**Expected patterns:**

- community.general.ufw module
- Default deny incoming
- Allow specific ports
- Enable firewall
- State-based (present/absent for rules)

**Quality signals:**

- Port ranges handled correctly
- Order matters (enable last)
- Idempotent rule addition

## Medium Complexity

### M01: Proxmox Cloud-Init

**Command:**

```text
/ansible-workflows:create-role proxmox_cloudinit
```

**Follow-up requirements:**

```text
Configure Proxmox cloud-init templates with custom user-data for Ubuntu VMs
```

**Expected patterns:**

- community.proxmox.proxmox_kvm for VM/template
- template module for user-data
- Cloud-init disk configuration
- Variable-driven (template name, storage, etc.)

**Quality signals:**

- Role structure (defaults, tasks, handlers)
- Proxmox API auth via variables
- no_log on credentials

### M02: VLAN Bridges

**Command:**

```text
/ansible-workflows:create-playbook configure-vlans --hosts proxmox
```

**Follow-up requirements:**

```text
Configure VLAN-aware network bridges on Proxmox hosts for isolated VM networks
```

**Expected patterns:**

- Network interface configuration
- Bridge with vlan-aware flag
- /etc/network/interfaces.d/ files
- Template for bridge config
- Handler to restart networking

**Quality signals:**

- Backup of original config
- Validation of network state
- Careful with networking restarts

### M03: System Users

**Command:**

```text
/ansible-workflows:create-role system_users
```

**Follow-up requirements:**

```text
Manage system users with SSH key authentication and sudo access via /etc/sudoers.d
```

**Expected patterns:**

- ansible.builtin.user module
- ansible.posix.authorized_key module
- Template for sudoers file
- visudo validation

**Quality signals:**

- no_log on any password hashes
- Validate sudoers syntax before applying
- State-based (present/absent)

## Complex

### C01: Nginx with SSL

**Command:**

```text
/ansible-workflows:create-playbook deploy-nginx-ssl
```

**Follow-up requirements:**

```text
Deploy Nginx with Let's Encrypt SSL certificates using certbot
```

**Expected patterns:**

- apt for nginx and certbot
- Template for nginx site config
- certbot command for certificate
- Handler chain (certbot -> nginx reload)
- Cron/timer for renewal

**Quality signals:**

- HTTP->HTTPS redirect
- Strong SSL configuration
- changed_when on certbot (idempotent cert check)
- Proper ordering (nginx config before cert)

### C02: Multi-Service Stack

**Command:**

```text
/ansible-workflows:create-playbook monitoring-stack
```

**Follow-up requirements:**

```text
Provision a complete monitoring stack: install Docker, deploy Prometheus container, deploy Grafana container, configure firewall rules for ports 3000 and 9090
```

**Expected patterns:**

- Docker installation tasks or role dependency
- community.docker.docker_container for services
- UFW or iptables rules
- Service dependencies (Docker before containers)

**Quality signals:**

- Proper task ordering and dependencies
- Container health checks
- Idempotent container deployment

## Edge Cases

These expose specific plugin behaviors:

### E01: Validation Failure Path

**Command:**

```text
/ansible-workflows:create-playbook run-migrations
```

**Follow-up requirements:**

```text
Run database migrations using a custom script at /opt/app/migrate.sh
```

**Why:** Forces command module usage, tests whether generator adds changed_when and whether validator catches missing idempotency controls.

### E02: Secret Handling

**Command:**

```text
/ansible-workflows:create-playbook proxmox-api-setup
```

**Follow-up requirements:**

```text
Configure Proxmox API access using credentials stored in environment variables
```

**Why:** Tests secret management patterns without explicit instruction. Should use no_log and avoid hardcoding.

## Pipeline Expectations

For each test, verify the full pipeline executes:

1. Command initializes state file (`.claude/ansible-workflows.local.md`)
2. Generator creates code and writes `.generating.bundle.md`
3. Validator runs lint and writes `.validating.bundle.md`
4. On PASS: Reviewer evaluates and writes `.reviewing.bundle.md`
5. On FAIL: Debugger fixes and loops back to validator

## Usage Notes

1. Pick one scenario per session
2. Memorize the command AND follow-up requirements
3. Do not reference this document during session
4. Verify pipeline state files were created
5. Record results in `results/` directory after session ends

## Future: Natural Language Invocation

Once slash command workflows are validated, we will test natural language triggers
(e.g., "Create a playbook to install Docker...") and document expected behavior
for ad-hoc agent dispatch vs pipeline orchestration.
