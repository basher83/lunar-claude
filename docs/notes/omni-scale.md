Repo Classification:
  Repo: Omni-Scale
  Function: Infrastructure provisioning
  Reviews: Cluster templates, machine classes, provider configs, Omni compose
  ────────────────────────────────────────
  Repo: mothership-gitops
  Function: Workload deployment
  Reviews: ArgoCD Applications, Helm values, K8s manifests, ESO configs
  Reviewer Agent Split:
  Agent: Omni Reviewer
  Scope: Omni-Scale repo
  Validates: Machine class schema, cluster template syntax, CEL selectors,
    provider config, spec consistency
  ────────────────────────────────────────
  Agent: GitOps Reviewer
  Scope: mothership-gitops
  Validates: Sync waves order, Application structure, Helm values, Ingress
    patterns, ESO mappings, namespace labels
  Matches the locked decision you already have:

- Omni-Scale = how cluster exists
- mothership-gitops = what runs on cluster

  Two agents, clean separation. The Omni reviewer doesn't need to know ArgoCD,
  the GitOps reviewer doesn't need to know machine classes.

  Want me to sketch out what each reviewer would check for?

❯ yeah that would be a huge help

⏺ Omni Reviewer (Omni-Scale repo)

  Machine Classes (machine-classes/*.yaml)
  Check: Required fields
  Rule: spec.autoprovision.providerid, providerdata present
  ────────────────────────────────────────
  Check: Providerdata schema
  Rule: Valid fields: cores, memory, disk_size, network_bridge, storage_selector
  ────────────────────────────────────────
  Check: CEL selector syntax
  Rule: No reserved keywords (type → use name)
  ────────────────────────────────────────
  Check: Storage selector
  Rule: References valid pool (e.g., name == "vm_ssd")
  ────────────────────────────────────────
  Check: Provider ID
  Rule: Matches registered provider in Omni
  ────────────────────────────────────────
  Check: Naming convention
  Rule: <cluster>-<role>-<host>.yaml pattern
  Cluster Templates (clusters/*.yaml)
  ┌─────────────────────┬──────────────────────────────────────────────────┐
  │        Check        │                       Rule                       │
  ├─────────────────────┼──────────────────────────────────────────────────┤
  │ Multi-doc structure │ Separate docs for Cluster, ControlPlane, Workers │
  ├─────────────────────┼──────────────────────────────────────────────────┤
  │ Machine class refs  │ Referenced classes exist in machine-classes/     │
  ├─────────────────────┼──────────────────────────────────────────────────┤
  │ Version format      │ kubernetes: v1.x.x, talos: v1.x.x                │
  ├─────────────────────┼──────────────────────────────────────────────────┤
  │ CNI setting         │ none if using Cilium post-bootstrap              │
  ├─────────────────────┼──────────────────────────────────────────────────┤
  │ Control plane count │ Odd number (1, 3, 5) for etcd quorum             │
  └─────────────────────┴──────────────────────────────────────────────────┘
  Provider Config (proxmox-provider/)
  ┌───────────────────┬───────────────────────────────────────────┐
  │       Check       │                   Rule                    │
  ├───────────────────┼───────────────────────────────────────────┤
  │ Required env vars │ OMNI_ENDPOINT, PROXMOX_API, PROXMOX_TOKEN │
  ├───────────────────┼───────────────────────────────────────────┤
  │ Image tag         │ :local-fix not :latest (hostname bug)     │
  ├───────────────────┼───────────────────────────────────────────┤
  │ Provider ID       │ Consistent with machine classes           │
  └───────────────────┴───────────────────────────────────────────┘
  Specs (specs/*.yaml)
  ┌────────────────────┬────────────────────────────────────────────────────┐
  │       Check        │                        Rule                        │
  ├────────────────────┼────────────────────────────────────────────────────┤
  │ Phase progression  │ Status flows: not-started → in-progress → complete │
  ├────────────────────┼────────────────────────────────────────────────────┤
  │ Definition of done │ All items have corresponding phase work            │
  ├────────────────────┼────────────────────────────────────────────────────┤
  │ Locked decisions   │ Each has rationale field                           │
  ├────────────────────┼────────────────────────────────────────────────────┤
  │ Constraints        │ Each has description and resolution                │
  └────────────────────┴────────────────────────────────────────────────────┘
  ---
  GitOps Reviewer (mothership-gitops repo)

  ArgoCD Applications (apps/*/)
  Check: Sync wave annotation
  Rule: argocd.argoproj.io/sync-wave present
  ────────────────────────────────────────
  Check: Wave ordering
  Rule: Respects dependencies (ESO < consumers, Longhorn < PVC users)
  ────────────────────────────────────────
  Check: Destination
  Rule: Namespace exists OR CreateNamespace=true in syncOptions
  ────────────────────────────────────────
  Check: Source
  Rule: repoURL, chart, targetRevision all present
  ────────────────────────────────────────
  Check: Finalizers
  Rule: resources-finalizer.argocd.argoproj.io for cleanup
  Helm Values
  Check: No hardcoded secrets
  Rule: Secrets via ESO, never inline
  ────────────────────────────────────────
  Check: Resource requests
  Rule: Present for production workloads
  ────────────────────────────────────────
  Check: Replicas
  Rule: Match available nodes (e.g., Redis HA needs 3 schedulable)
  Web UI Exposure (HARD REQUIREMENT)
  Check: UI detection
  Rule: App has -frontend, -ui, -server service → needs Ingress
  ────────────────────────────────────────
  Check: Ingress present
  Rule: ingressClassName: tailscale
  ────────────────────────────────────────
  Check: Naming
  Rule: <app>-tailscale
  ────────────────────────────────────────
  Check: No cluster-internal UIs
  Rule: Fail if web UI has no Ingress
  External Secrets
  ┌─────────────────┬───────────────────────────────────────────────────┐
  │      Check      │                       Rule                        │
  ├─────────────────┼───────────────────────────────────────────────────┤
  │ Store reference │ secretStoreRef points to valid ClusterSecretStore │
  ├─────────────────┼───────────────────────────────────────────────────┤
  │ Infisical path  │ Matches store's secretsPath                       │
  ├─────────────────┼───────────────────────────────────────────────────┤
  │ Target secret   │ Name/namespace match consumer expectations        │
  └─────────────────┴───────────────────────────────────────────────────┘
  Namespace Labels
  Check: Privileged namespaces
  Rule: longhorn-system, netdata, tailscale-operator have
    pod-security.kubernetes.io/enforce=privileged
  Sync Wave Reference

  Wave 0-1: Networking (Cilium if managed)
  Wave 2:   Secrets (ESO + ClusterSecretStores)
  Wave 3-4: Storage (Longhorn)
  Wave 5:   Platform services (Tailscale, Netdata, etc.)
  Wave 99:  ArgoCD HA (manual sync)
