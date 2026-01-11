# Homelab Kernel (L0)

**Purpose:** Immutable context for AI collaboration. Upload at start of every Strategic session.
**Last Updated:** 2026-01-03

---

## Infrastructure Overview

### Clusters

| Cluster | Nodes | Purpose | Storage | Network |
|---------|-------|---------|---------|---------|
| **Matrix** | 3 (Foxtrot, Golf, Hotel) | Production workloads | CEPH (24TB raw, 12TB usable) + Local LVM-thin (1TB/node) | 192.168.3.0/24 (mgmt), 192.168.5.0/24 (CEPH public), 192.168.7.0/24 (CEPH private) |
| **Nexus** | 2 (Alpha, Bravo) | Mixed workloads, legacy | Local LVM-thin + NFS | 192.168.30.0/24 |
| **Quantum** | 3 (Holly, Lloyd, Mable) | Management plane (Omni Hub on Holly) | Local LVM-thin + NFS | 192.168.10.0/24 |

### Shared Infrastructure

- **TrueNAS:** 192.168.30.6 (NFS exports to Nexus, Quantum)
- **PBS:** 192.168.30.200 (currently unreachable—pending resolution)
- **Domain:** spaceships.work
- **Network Overlay:** Tailscale (all clusters connected)

### Hardware Summary

| Cluster | Per-Node Specs |
|---------|----------------|
| Matrix | AMD Ryzen 9 9955HX (16c/32t), 64GB DDR5, 1TB boot + 8TB CEPH NVMe, 10GbE |
| Nexus | Mixed: Alpha (i3, 64GB), Bravo (Dual Xeon, 256GB) |
| Quantum | Intel i9-13900H (14c/20t), 32GB, 1TB NVMe, 10GbE |

---

## Technology Stack

### Preferred Tools

| Domain | Tool | Notes |
|--------|------|-------|
| IaC | OpenTofu (`tofu` not `terraform`) | Remote state required |
| Config Management | Ansible (via `uv run`) | Roles over playbooks for reusable logic |
| Containers | Docker, Podman | Context-dependent |
| Kubernetes | Talos Linux + Sidero Omni | Management via Omni on Quantum |
| Secrets | Infisical | Per-cluster paths: `/matrix`, `/nexus`, `/quantum` |
| DNS | PowerDNS + NetBox sync | Automatic record management |
| Network Overlay | Tailscale | OIDC via Auth0, MagicDNS for internal resolution |
| Reverse Proxy | Caddy | For services needing custom domains |

### Languages (in order of preference)

1. **Python** — scripting, automation
2. **Go** — when performance or single-binary matters
3. **Bash** — glue, one-liners (not complex logic)

---

## Global Standards

### Infrastructure

- All Terraform/OpenTofu must use remote state
- No secrets in plaintext (use Infisical or environment files)
- All VMs must have backup tags
- Prefer Tailscale HTTPS over DNS-01 for internal services
- Omni Hub on Quantum (Holly), Omni Provider on Matrix (Foxtrot LXC) for L2 adjacency to Talos VMs
- **Split-Horizon DNS required** when services need both Tailscale and LAN access (see Omni deployment war story)

### Code & Config

- Ansible: `uv run ansible-playbook` (always via uv)
- OpenTofu: `tofu` command (not `terraform`)
- Task runner: `mise run <task>`
- Commit messages: imperative mood, reference initiative if applicable
- Automation over documentation: if you'll do it twice, script it

### Documentation

- ADRs for cross-initiative architectural decisions (`docs/decisions/NNN-title.md`)
- Specs in YAML for initiative handoff (`specs/project.yaml`)
- ADRs: Decisions affecting multiple initiatives or overall architecture
- Specs: Initiative-specific decisions in `locked_decisions` section (no duplication needed)
- Specs are living documents during active initiatives; freeze when DoD is met
- Strategic context (ARCHITECTURE.md, domain references) lives in Notion—not in-repo
- Explicit over implicit: state assumptions, capture "I don't know yet" rather than guessing

---

## Operational Constraints

### Single Admin Reality

- Recovery procedures must be executable solo
- Documentation matters—future-you is the on-call engineer
- Avoid architectures requiring simultaneous action on multiple systems

### Acceptable Risk Profile

- Hours of downtime tolerable (not enterprise SLA)
- Optimize for recoverability over high availability
- HA is a learning goal, not a hard requirement

### Complexity Budget

- Each dependency is a failure mode
- "Good enough" beats "ideal" when ideal adds significant complexity
- Prefer fewer moving parts; consolidate where possible

### Resource Priorities

- Budget-conscious, not cheap: spend for meaningful capability gains
- Avoid recurring costs where one-time investments work
- Hardware already owned > new purchase when capability is comparable
- Learning value is valid justification—novel tech exposure has worth
- But: learning value alone doesn't justify complexity that undermines operations

### Decision Quality

- Prefer reversible decisions; deliberate more on irreversible ones
- Prototype before production where feasible
- "I don't know yet" is valid—capture uncertainty rather than guessing
- Future decisions reference past constraints—make them findable

---

## AI Collaboration Conventions

### Process Selection

| Type | Criteria | Process |
|------|----------|---------|
| **Initiative** | Multi-day, new system, high blast radius | Full Flow (Research → Plan → Design → Implement) |
| **Task** | Single sitting, reversible, modifies existing | Fast Path (Define → Do) |

### Task → Initiative Escalation

**Trigger:** About to touch a system outside original scope.
**Test:** "Am I about to modify something I didn't mention in my opening prompt?"
**Action:** Commit current work, switch to Web UI, draft ADR for scope expansion.

### Strategic Session Continuity

Each Web UI session: Re-upload `kernel.md` + relevant L1 artifacts (ADRs, specs).
ADRs capture "why", specs capture "what"—that's sufficient context to resume.

### Escalation from Execution

**Trigger:** Constraint error (hardware/infra limitation, not logic bug).
**Action:** Commit state, return to Web UI with kernel + specs + error description.
**Output:** Updated ADR or spec reflecting the constraint.

### Spec Completeness Test

Spec is ready when it answers **What, Where, Which**—not **How**.
If Execution AI must decide naming, sizing, or networking, the spec is incomplete.

### Context Loading by Mode

| Mode | Load | Source |
|------|------|--------|
| Strategic (Web UI) | `kernel.md` + specs + ADRs + strategic context | Repo + Notion (via connector) |
| Execution (CLI) | `kernel.md` + `spec.yaml` for active initiative | Repo only |

---

## Active Initiatives

<!-- Update this section as initiatives open/close -->

| Initiative | Status | Spec Location |
|------------|--------|---------------|
| Omni Deployment | Infrastructure Operational | `specs/omni.yaml` |
