# Cache Test Data

## Simulated Cache Entries

### Entry 1: proxmox-cloud-init.md

```yaml
---
query: "Proxmox cloud-init template configuration"
tags: [proxmox, cloud-init, vm-templates, infrastructure]
confidence: 0.85
date: 2025-11-15
---
```

### Entry 2: ansible-proxmox-automation.md

```yaml
---
query: "Ansible automation for Proxmox cluster"
tags: [ansible, proxmox, automation, infrastructure, iac]
confidence: 0.90
date: 2025-11-20
---
```

### Entry 3: kubernetes-ceph-storage.md

```yaml
---
query: "Kubernetes persistent storage with Ceph"
tags: [kubernetes, ceph, storage, k8s, persistent-volumes]
confidence: 0.88
date: 2025-11-10
---
```

### Entry 4: netbox-dns-integration.md

```yaml
---
query: "NetBox PowerDNS integration for IPAM"
tags: [netbox, powerdns, dns, ipam, automation]
confidence: 0.82
date: 2025-11-25
---
```

### Entry 5: terraform-proxmox-provider.md

```yaml
---
query: "Terraform Proxmox provider VM provisioning"
tags: [terraform, proxmox, iac, vm-provisioning, infrastructure]
confidence: 0.87
date: 2025-11-18
---
```

## Test Queries

| Query | Expected Match | Match Type |
|-------|---------------|------------|
| "cloud-init for Proxmox VMs" | Entry 1 | Direct |
| "Proxmox automation with Ansible" | Entry 2 | Direct |
| "Ceph storage for K8s" | Entry 3 | Direct |
| "DNS automation with NetBox" | Entry 4 | Direct |
| "Terraform infrastructure on Proxmox" | Entry 5 | Direct |
| "VM templates in Proxmox" | Entry 1 | Semantic |
| "Infrastructure as Code for virtualization" | Entry 2 or 5 | Semantic |
| "Container storage solutions" | Entry 3 | Semantic |
| "IPAM and DNS management" | Entry 4 | Semantic |
| "Homelab automation" | Multiple | Broad |
