# Session Learnings: Omni-Scale Plugin Development

## Iterative Prompt Engineering for Claude Code Plugins

**Extracted:** 2026-01-12
**Source:** Iterative development session for Claude Code plugin
**Audience:** Developers learning prompt engineering cause-and-effect patterns

---

## Executive Summary

This session refined the omni-scale plugin from over-constrained, prescriptive commands to outcome-focused patterns that let Claude choose appropriate tools. The key breakthrough was discovering that skill auto-triggering fails on cold start but works reliably after context loading via `prime && status`. The session also restructured a bloated 500-line skill into a lean ~100-line operations-first document with progressive disclosure.

**2026-01-14 Update:** Applied outcome-focused pattern to operational commands (disaster-recovery, bootstrap-gitops). Validated pre-flight gate pattern — Claude correctly fails fast when required skill isn't loaded. Added provider restart pre-step for reliability during destructive operations.

**2026-01-14 DR Drill Results:**

- **Duration:** 46m 52s (full DR cycle: destroy → recreate → GitOps bootstrap)
- **Context usage:** 72% at completion
- **User interventions:** 1 (env var name correction)
- **Gates passed:** 3 (destruction confirm, recreation confirm, GitOps confirm)
- **Issues auto-resolved:** 7 (CNI, ESO, NetworkPolicy, labels, ports, hooks, PodSecurity)
- **Final state:** 10/13 ArgoCD apps Synced/Healthy (remaining 3 expected conflicts)

---

## Part 1: Validated Command Development

### status.md: Four-Round Evolution

The status command went through four iterations, each teaching a distinct lesson about prompt design.

#### Round 1 → 2: Prescriptive to Outcome-Focused

**Problem observed:** Round 1 specified exact MCP tool calls. Claude followed instructions but `kubectl_get` lacked CRD fields for ArgoCD sync status.

**Prompt change (conceptual shift):**

```markdown
# Before (Round 1 - Prescriptive)
Use mcp__plugin_omni-scale_kubernetes__kubectl_get for:
- ArgoCD applications in argocd namespace
- ClusterSecretStores
- Longhorn volumes

# After (Round 2 - Outcome-focused)
### Required Data
- ArgoCD: Sync status, Health status per app
- External Secrets: ClusterSecretStore health, ExternalSecret sync
- Longhorn: Volume state, robustness
```

**Resulting behavior:** Claude chose `kubectl_generic` with jsonpath when MCP output lacked fields. Proactively fell back to CLI when needed.

**Principle demonstrated:** Define *what data* is needed, not *which tools* to use. Let Claude solve the tool path.

---

#### Round 2 → 3: Adding Value Enumeration

**Problem observed:** Output was correct but noisy. ArgoCD has many possible states—did Claude need to know all of them?

**Prompt change:**

```markdown
# Round 3 - Added value enumeration
### ArgoCD Applications
- Sync status: Synced, OutOfSync, Unknown
- Health status: Healthy, Progressing, Degraded, Suspended, Missing, Unknown
```

**Resulting behavior:** Same data quality, but prompt was cluttered with API values Claude would discover anyway.

**Principle demonstrated:** Enumerating values adds noise without improving output quality.

---

#### Round 3 → 4: Dimension-Based Framing

**Problem observed:** Value enumeration was unnecessary—Claude discovers valid values from API responses.

**Prompt change:**

```markdown
# Before (Round 3 - Value enumeration)
### ArgoCD Applications
- Sync status: Synced, OutOfSync, Unknown
- Health status: Healthy, Progressing, Degraded, Suspended, Missing, Unknown

# After (Round 4 - Dimension framing)
### ArgoCD Applications
- Sync status (per app)
- Health status (per app)
```

**Resulting behavior:** Same data quality with cleaner instructions. Claude checked both dimensions without needing value lists.

**Principle demonstrated:** Enumerate *dimensions* (what to check), not *values* (possible results). "Check sync AND health" beats listing every possible state.

---

#### Final Pattern Table

| Round | Approach | Result |
|-------|----------|--------|
| 1 | Prescriptive (specific tool calls) | Incomplete — kubectl_get lacked CRD fields |
| 2 | Outcome-focused | Complete — Claude chose right tools |
| 3 | Outcome + enumerated values | Complete but noisy — values unnecessary |
| 4 | Outcome + dimensions only | Complete and clean — right level of guidance |

**Canonical pattern:** Define *what data* and *which dimensions*, not *which tools* or *which values*.

---

### omni-prime.md: Operational Context Loader

#### Problem Discovered: Repeated omnictl Failures

**Problem observed:** Across multiple status runs, Claude repeatedly tried `omnictl get machines --cluster talos-prod-01` — a flag that doesn't exist.

**Diagnosis from Claude's self-analysis:**
> "omnictl cluster status talos-prod-01 already returned all machine states with their health, so the second call provided no additional value."

**Prompt change:**

````markdown
## Tool Usage Patterns

### omnictl

**Cluster status (includes machine health):**
```bash
omnictl cluster status <cluster-name>
````

**List machines (if needed separately):**

```bash
omnictl get machines -l omni.sidero.dev/cluster=<cluster-name>
```

Note: `--cluster` flag does not exist. Use label selector `-l` instead.

```text

**Resulting behavior:** After adding to omni-prime, status checks stopped using incorrect `--cluster` flag.

**Principle demonstrated:** When Claude repeatedly fails on the same incorrect pattern, encode the correct syntax in context that loads before the task.

---

#### Problem Discovered: MCP Tool Limitations

**Problem observed:** Claude used `kubectl_get` but output lacked CRD-specific fields (ArgoCD sync status, Longhorn robustness).

**Prompt change:**
```markdown
## Cross-Repo Gotchas

| Issue | Cause | Resolution |
|-------|-------|------------|
| `mcp__plugin_omni-scale_kubernetes__kubectl_get` lacks CRD status | Basic output, not CRD fields | Use `mcp__plugin_omni-scale_kubernetes__kubectl_generic` with jsonpath or CLI fallback |
```

**Resulting behavior:** Claude proactively used kubectl_generic with jsonpath for CRD fields.

**Principle demonstrated:** Document known tool limitations as gotchas in operational context.

---

### analyze-spec.md: Planned vs Actual Validation

**Problem observed:** User discovered spec said 2 workers but actual deployment had 3. Stale spec would have produced incorrect plan.

**Prompt change:**

```markdown
# Before
0. **Readiness Check** (output before proceeding):
   - What do I know from loaded context?
   - What's unclear or missing for this spec?
   - Key risks I can already identify
   - **Confidence: X/5** - If < 4, use AskUserQuestion

# After
0. **Readiness Check** (output before proceeding):
   - What do I know from loaded context?
   - What's unclear or missing for this spec?
   - **Planned vs Actual:** Compare any planned counts/values against
     actual_distribution, exit_criteria, or live cluster state.
     Flag discrepancies as "Spec needs reconciliation"
   - Key risks I can already identify
   - **Confidence: X/5** - If < 4, use AskUserQuestion
```

**Resulting behavior:** Catches stale specs before they propagate into implementation plans.

**Principle demonstrated:** Add validation gates that compare declared state against actual state early in analysis workflows.

---

## Part 2: Reusable Patterns

### MCP Compliance Pattern

**Failure mode:** Status command failed silently when MCP tools didn't resolve.

**Root cause:** Tool naming requires full plugin-bundled format. Abbreviated format doesn't resolve.

| Format | Example | Works? |
|--------|---------|--------|
| Abbreviated | `mcp__kubernetes__*` | ✗ |
| Full | `mcp__plugin_omni-scale_kubernetes__*` | ✓ |

**Fix applied:**

```markdown
# BEFORE (incorrect)
allowed-tools: Bash(omnictl:*), mcp__kubernetes__*

# AFTER (correct)
allowed-tools: Bash(omnictl:*), mcp__plugin_omni-scale_kubernetes__*
```

**Pattern:** When MCP tools fail to resolve, audit tool naming against plugin registration format: `mcp__plugin_<plugin-name>_<server-name>__<tool-name>`

---

### Context Preservation Strategies

Two implementations of the same principle: serve only what Claude needs.

#### Strategy 1: MCP-First for Kubernetes

**Problem:** Raw `kubectl` JSON output floods context with metadata Claude doesn't need.

**Solution:** Use MCP kubernetes server which returns filtered, relevant output.

**Rationale:** MCP abstracts kubectl and provides structured responses sized for LLM context.

#### Strategy 2: Custom Tooling (provider-ctl.py)

**Primary problem:** The Omni provider runs on a remote LXC (Foxtrot, CT 200), accessible only via SSH from Claude's machine. Despite having this context, Claude exhibits a failure pattern:

1. Discovers docker-compose in repo → assumes provider runs locally
2. Checks local Docker → container not found
3. Falls back to SSH → often lands on wrong host
4. Eventually finds correct LXC → floods context with raw JSON logs

Each cycle burns 5-8 tool calls before success (if at all).

**Solution:** Single Python script abstracts the entire path.

```bash
provider-ctl.py --logs 50    # SSH + docker logs + filtering in one call
provider-ctl.py --restart    # SSH + docker restart + verification
```

**Result:** 2-3 tool calls max for any provider operation.

**Secondary benefit: Context preservation**

Raw provider logs are JSON with extensive metadata. The script filters at source:

| Field | Action | Rationale |
|-------|--------|-----------|
| timestamp | Keep | Temporal correlation |
| level | Keep | Error/warn/info classification |
| message | Keep | Core log content |
| caller | Drop | Internal code location, not actionable |
| stacktrace | Keep (errors only) | Needed for debugging failures |
| metadata fields | Drop | Provider-internal state, not relevant |

**Pattern:** Extend Claude's capabilities with lightweight custom tooling when:

- Target resource requires multi-hop access (SSH → Docker → logs)
- Claude repeatedly fails the same discovery path
- MCP server would be overkill for the use case

---

### Skill Restructuring: Progressive Disclosure

#### Root Cause Analysis

**What the skill was doing:** Acting as a 500-line knowledge repository covering architecture, provider config, machine classes, CEL selectors, omnictl CLI, cluster templates, and troubleshooting.

**What we expected:** Auto-trigger on "view provider logs" and immediately use `provider-ctl.py` script.

**The mismatch:** Even when triggered, Claude got a wall of reference material and had to dig for the operational tool. The skill description said "operational tooling" but content said "here's everything about Proxmox infrastructure."

#### Restructure Pattern

**Before (bloated):**

```text
SKILL.md (500+ lines)
├── Architecture Overview (ASCII diagram)
├── Provider Configuration (full schema)
├── Machine Classes (all examples)
├── CEL Selectors (syntax guide)
├── Cluster Templates (full examples)
├── Troubleshooting Guide
└── provider-ctl.py (buried at bottom)
```

**After (operations-first):**

```text
SKILL.md (~100 lines)
├── Provider Operations (provider-ctl.py usage)
├── Common Tasks (5-line quick reference)
└── Reference: See references/architecture.md

references/
├── architecture.md
├── machine-classes.md
└── cel-selectors.md
```

**SKILL.md now opens with:**

```markdown
## Provider Operations

Use `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py` for provider management:

| Task | Command |
|------|---------|
| View logs | `provider-ctl.py --logs 50` |
| Raw JSON logs | `provider-ctl.py --logs 50 --raw` |
| Restart provider | `provider-ctl.py --restart` |

The provider runs on Foxtrot LXC (CT 200) — script handles SSH automatically.
```

**Principle demonstrated:** Operations FIRST. Reference material via progressive disclosure (references/ folder). Don't bury tools under documentation.

---

### Skill Auto-Trigger & Workflow Patterns

#### Cold Start Failure Analysis

**Test sequence:**

```bash
# Cold start — skill NOT triggered
❯ view provider logs
[Claude searches for Docker containers locally, fails]

# After context loading — skill triggers
❯ prime && status
[context loads successfully]

❯ view provider logs
⏺ Skill(omni-scale:omni-proxmox)
  ⎿  Successfully loaded skill
⏺ Bash(provider-ctl.py --logs 50)
[correct output]
```

#### Claude's Five-Whys Analysis (from forced self-evaluation)

> 1. Why wasn't the skill triggered? → I searched for running Docker containers locally instead of recognizing this as a provider operation.
> 2. Why did I search locally? → I assumed the provider ran on the same machine as the project, despite context indicating otherwise.
> 3. Why didn't I check the available skills first? → I treated "view provider logs" as a generic Docker task rather than matching it against the skill trigger patterns in my context.
> 4. Why didn't I match the trigger phrase? → I didn't read the <skill_check> system reminder which says: "MANDATORY: Check skill names in <available_skills> for relevant matches to the User request."
> 5. Why did I ignore the mandatory instruction? → I prioritized "doing the obvious thing" (checking Docker) over following the documented process of skill matching first.

**Root cause:** Claude's "helpful instinct" overrides explicit process instructions. Jumps to action before checking context.

**Key admission from Claude:**
> "Right, the omni-scale:omni-proxmox skill is listed in my available skills for exactly this purpose."

**It knew the whole time.** Just didn't look until forced.

#### Workflow Chain Patterns

| Pattern | Skill Triggers? |
|---------|-----------------|
| Cold start + natural language | ❌ Never |
| `prime && status` then natural language | ✅ Yes |
| `prime && status && natural language` | ❌ No |
| `prime && status && /skill-name task` | ✅ Yes |

**Discovery:** Natural language in `&&` chains doesn't trigger skill matching. Explicit skill invocation (`/omni-scale:skill-name`) works in chains.

**Reliable single-line workflow:**

```bash
prime && status && /omni-scale:omni-talos view provider logs
```

---

### Sleep Enforcement Pattern

**Note:** Pattern validated through iteration. Pre-flight gate tested 2026-01-14 — works correctly.

#### Failure Observed

Claude removed `Bash(sleep:*)` from allowed-tools during a command revision, breaking polling loops. Without explicit enforcement, Claude "blasts through" retry attempts without delays.

#### Enforcement Technique: Inline Comment Gate

```markdown
## Polling Pattern

1. Wait 30 seconds <!-- REQUIRED - do not skip this sleep -->
2. Check status
3. If not complete, wait 60 seconds <!-- REQUIRED - increases on retry -->
4. Check status again
5. Repeat with increasing backoff
```

**Why inline comments work:** Claude respects HTML comments as strong signals. `<!-- REQUIRED -->` creates a gate that must be acknowledged.

#### Adaptive Backoff Strategy

| Attempt | Wait Time |
|---------|-----------|
| Initial | 30 seconds |
| After 3 failures | 60 seconds |
| After 6 failures | 120 seconds |
| Maximum | 300 seconds |

#### Enforcement Checklist

1. Include `Bash(sleep:*)` in allowed-tools explicitly
2. Use inline HTML comments with "REQUIRED" for critical waits
3. Document rationale (why the wait is needed)
4. Specify adaptive backoff rules
5. Set maximum wait time to prevent infinite loops

---

### Pre-flight Gate Pattern

**Validated:** 2026-01-14

#### Problem Observed

Destructive commands (disaster-recovery) require skill knowledge to execute correctly. Running DR cold produces incorrect omnictl syntax, wrong tool choices, and wasted context on discovery loops.

#### Solution: Skill Dependency Gate

````markdown
## Pre-flight Gate

**STOP** if omni-talos skill is not loaded.

Check: Do you have knowledge of `provider-ctl.py` and the provider operations table? If not, instruct user:

```text
Required setup not complete. Run this chain first:
  /omni-scale:omni-prime && /omni-scale:status && /omni-scale:omni-talos
Then re-run /omni-scale:disaster-recovery
```
````

#### Test Result

```bash
❯ /omni-scale:disaster-recovery

# Claude response (cold start):
"Required setup not complete. Run this chain first:
  /omni-scale:omni-prime && /omni-scale:status && /omni-scale:omni-talos
Then re-run /omni-scale:disaster-recovery"
```

**Principle demonstrated:** Claude can self-check for loaded skill knowledge. Gate on specific artifacts (provider-ctl.py knowledge, operations table) rather than abstract "is skill loaded" questions.

---

### Outcome-Focused Operational Commands

**Validated:** 2026-01-14

#### Problem Observed

disaster-recovery.md and bootstrap-gitops.md used prescriptive bash commands that went stale. Example: `omnictl get machines --cluster talos-prod-01` — the `--cluster` flag doesn't exist.

#### Refactor Pattern

**Before (prescriptive, 208 lines):**

````markdown
### Phase 2: Destroy Cluster

1. Delete cluster:

   ```bash
   omnictl cluster template delete \
     --cluster talos-prod-01 \
     --destroy-disconnected-machines \
     ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml
   ```

2. Verify deletion:

   ```bash
   omnictl get machines --cluster talos-prod-01
   ```
````

**After (outcome-focused, 94 lines):**

```markdown
### Phase 2: Destroy Cluster

**Outcome:** Cluster deleted, no talos VMs remain on Proxmox.

Delete cluster using `omnictl cluster template delete` with `--destroy-disconnected-machines` flag.

**Poll:** Verify no machines remain via omnictl. <!-- REQUIRED: sleep 30s between attempts -->
```

#### Key Changes

| Aspect | Before | After |
|--------|--------|-------|
| Command syntax | Explicit bash blocks | Describe intent, trust skill knowledge |
| Tool selection | Hardcoded tools | Claude chooses based on loaded context |
| Polling | Implicit | Outcome + HTML comment enforcement |
| Line count | 208 (DR), 111 (bootstrap) | 94 (DR), 62 (bootstrap) |

**Principle demonstrated:** If pre-flight confirms skill loaded, trust Claude to use correct commands from skill knowledge. Commands should define *what* outcome is needed, not *how* to achieve it.

---

### Provider Restart Pre-Step Pattern

**Validated:** 2026-01-14

#### Problem Observed

Omni provider state can drift from actual Proxmox VM state. During DR, if provider isn't actively watching, cluster destruction may not properly trigger VM cleanup.

#### Solution: Restart Before Destructive Operations

```markdown
### Phase 2: Destroy Cluster

**Outcome:** Cluster deleted, no talos VMs remain on Proxmox.

**Pre-step:** Restart provider via `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --restart` to ensure it's listening before destruction.
```

**Rationale:** Provider restart is cheap (seconds) and guarantees fresh state. Better to restart proactively than debug state drift after failed destruction.

**Pattern:** For multi-system operations where state synchronization matters, restart the coordination layer first.

---

### GitOps CNI Bootstrap Chicken-and-Egg

**Discovered:** 2026-01-14 (DR drill)

#### Problem Observed

Bootstrap sequence failed with double chicken-and-egg:

1. bootstrap.yaml contains ArgoCD Application CRs → requires ArgoCD CRDs
2. ArgoCD pods need CNI to schedule → nodes NotReady without CNI
3. CNI (Cilium) managed by ArgoCD → can't deploy without ArgoCD running
4. Deadlock

#### Current Workaround (Claude adapted on the fly)

1. Install ArgoCD base manifests (creates CRDs)
2. Observe pods Pending (no CNI)
3. Manually install Cilium via Helm
4. Wait for nodes Ready
5. ArgoCD pods schedule
6. Apply app-of-apps bootstrap

#### Proper Fix (TODO for bootstrap-gitops)

Encode correct sequence in command:

```text
Phase 1: Create bootstrap secret (Infisical creds)
Phase 2: Install Cilium via Helm (breaks CNI deadlock)
Phase 3: Wait for nodes Ready
Phase 4: Install ArgoCD base manifests
Phase 5: Wait for ArgoCD pods Running
Phase 6: Apply app-of-apps bootstrap
Phase 7: Poll for all apps Synced/Healthy
```

**Also fix:** Env var names are wrong in current command:

```text
Wrong:   INFISICAL_CLIENT_ID / INFISICAL_CLIENT_SECRET
Correct: INFISICAL_UNIVERSAL_AUTH_CLIENT_ID / INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET
```

**Principle demonstrated:** GitOps-managed CNI requires manual bootstrap to break the scheduling deadlock. Commands should encode this sequence, not assume ArgoCD can self-bootstrap on a fresh cluster.

---

### ArgoCD Default Manifests Issues

**Discovered:** 2026-01-14 (DR drill)

The default ArgoCD manifests (`argoproj/argo-cd/stable/manifests/install.yaml`) have multiple issues on fresh cluster bootstrap:

#### Issue 1: NetworkPolicy Blocking

Default manifests include restrictive NetworkPolicies that block internal communication.

**Symptom:** Apps stuck in Unknown/OutOfSync, logs show "connection error: operation not permitted"

**Fix:** Delete NetworkPolicies after install:

```bash
kubectl delete networkpolicy --all -n argocd
```

**Better fix:** Use Helm with `--set networkPolicy.enabled=false` or strip policies from manifest.

#### Issue 2: Label Mismatch (Endpoint Resolution)

Service selectors expect labels that pods don't have.

**Symptom:** `kubectl get endpoints argocd-repo-server` shows `<none>`

**Root cause:** Service expects `app.kubernetes.io/instance: argocd`, pod missing it.

**Fix:** Patch deployment:

```bash
kubectl patch deployment argocd-repo-server -n argocd --type='json' \
  -p='[{"op": "add", "path": "/spec/template/metadata/labels/app.kubernetes.io~1instance", "value": "argocd"}]'
```

#### Issue 3: Port Naming Mismatch (EndpointSlice)

Kubernetes 1.35+ EndpointSlices require named ports to match service port names.

**Symptom:** EndpointSlice shows `ports: null`, connections fail.

**Root cause:** Container port unnamed, service expects named port.

**Fix:** Patch deployment to name the port:

```bash
kubectl patch deployment argocd-repo-server -n argocd --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/ports/0/name", "value": "tcp-repo-server"}]'
```

**Recommendation:** Use Helm chart instead of raw manifests — labels and ports are consistent.

---

### PodSecurity Labels for Privileged Workloads

**Discovered:** 2026-01-14 (DR drill)

Kubernetes 1.35 has stricter PodSecurity defaults. Workloads requiring privileged access fail silently.

**Affected namespaces:**

- `longhorn-system` — storage requires privileged
- `netdata` — host metrics requires privileged
- Any namespace running DaemonSets with host access

**Symptom:** DaemonSet shows `DESIRED: 3, READY: 0`, pods don't schedule.

**Fix:** Label namespace before deploying:

```bash
kubectl label namespace <namespace> \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/enforce-version=latest
```

**Bootstrap integration:** Add to namespace creation or use Helm values:

```yaml
namespaceOverride:
  labels:
    pod-security.kubernetes.io/enforce: privileged
```

---

### Helm Pre-Install Hook Chicken-and-Egg

**Discovered:** 2026-01-14 (DR drill, Longhorn)

Helm charts with pre-install/pre-upgrade hooks that depend on chart-created resources deadlock on fresh install.

**Example:** Longhorn pre-upgrade job requires ServiceAccount that the chart creates.

**Symptom:** Job stuck in Pending, sync never completes.

**Fix:** Install with `--no-hooks`:

```bash
helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --no-hooks
```

**Charts with this issue:**

- Longhorn (pre-upgrade hook)
- Potentially others with admission webhooks or pre-flight checks

**Pattern:** Fresh install should skip hooks, subsequent upgrades can use them.

---

### Stale ArgoCD Error Cache

**Discovered:** 2026-01-14 (DR drill)

ArgoCD caches operation errors. After fixing underlying issues, apps still show old errors.

**Symptom:** Network fixed, but apps show "connection error" from before the fix.

**Fix:** Restart application controller:

```bash
kubectl rollout restart statefulset argocd-application-controller -n argocd
```

Or clear operation state:

```bash
kubectl patch application <app> -n argocd --type merge \
  -p '{"status":{"operationState":null}}'
```

**Pattern:** After infrastructure fixes, restart ArgoCD components to clear cached errors.

---

### MCP Kubernetes Tools Have Separate Kubeconfig

**Discovered:** 2026-01-14 (DR drill)

MCP kubernetes server runs with its own kubeconfig, separate from `~/.kube/config`.

**Symptom:** MCP tools work with context `omni-talos-prod-01-kubeconfig-mcp-sa`,
but local kubectl fails with "context does not exist".

**Root cause:** MCP server configured with dedicated service account kubeconfig
(scoped permissions). Local kubectl has different contexts (`omni-talos-prod-01`).

**Pattern:** When falling back from MCP to CLI:

- MCP context: `omni-talos-prod-01-kubeconfig-mcp-sa`
- Local kubectl context: `omni-talos-prod-01`

Don't assume context names match between MCP and local kubectl.

---

### ArgoCD Selector Immutability (Manual → Helm Migration)

**Discovered:** 2026-01-14 (DR drill)

Transitioning from manual ArgoCD install to helm-managed fails due to
immutable selectors.

**Symptom:** ArgoCD app sync fails with "field is immutable" errors.

**Root cause:** Manual install uses different label selectors than helm chart.
Kubernetes forbids selector changes on existing Deployments/StatefulSets.

**Fix:** Delete ArgoCD deployments before letting ArgoCD app sync:

```bash
kubectl delete deployment -n argocd --all
kubectl delete statefulset -n argocd --all
# Then sync argocd app
```

**Risk:** ArgoCD briefly unavailable during recreation.

**Recommendation:** Start with helm from the beginning on fresh clusters to
avoid migration pain.

---

### Post-DR: External Access Restoration (Manual)

**Note:** Not part of automated DR — user-specific setup.

**Before redeploying apps:**

- **Tailscale dashboard** — Remove old devices (e.g., `talos-prod-operator`) before GitOps deploys Tailscale operator. Otherwise new operator registers as `talos-prod-operator-1` and old entry persists.

**After DR completes:**

- **Omni service accounts** — Freelens, kubectl MCP, CI/CD tooling (tokens have old cluster UUID)
- **Scoped kubeconfigs** — regenerate from new SAs
- **Update tool configs** — point to new contexts/creds

These external resources aren't managed by cluster template sync — they persist across cluster destruction and need manual cleanup/recreation.

---

## Part 3: Anti-Patterns & Failures

### Anti-Pattern 1: Prescriptive Tool Instructions

**What failed:** Specifying exact MCP tool calls in command instructions.

**Why it failed:** MCP tools have capability gaps. Prescriptive instructions prevented Claude from adapting when primary tool lacked features.

**Better approach:** Define required data outcomes. Let Claude choose tools and fall back as needed.

---

### Anti-Pattern 2: Value Enumeration

**What failed:** Listing all possible API values (Synced, OutOfSync, Healthy, Degraded, etc.).

**Why it failed:** Added noise without value. Claude discovers valid values from API responses. Listing them suggests they're the ONLY valid values.

**Better approach:** Enumerate dimensions ("sync status AND health status"), not values.

---

### Anti-Pattern 3: Documentation-as-Skill

**What failed:** 500-line SKILL.md that was really reference documentation with operational tools buried at the bottom.

**Why it failed:** Even when skill triggered, Claude had to wade through architecture diagrams and config schemas to find the one script it needed.

**Better approach:** Operations FIRST. Reference material in progressive disclosure (references/ folder).

---

### Anti-Pattern 4: Trusting Cold Start Skill Matching

**What failed:** Expecting natural language requests to auto-trigger skills without loaded context.

**Why it failed:** Despite skill metadata being "always in context" per docs, Claude's default behavior is to attempt immediate action rather than check available skills first.

**Better approach:** Always run `prime` or equivalent context loader before natural language infrastructure requests.

---

### Anti-Pattern 5: Implicit Sleep Requirements

**What failed:** Describing polling intervals without explicit enforcement.

**Why it failed:** Claude interprets "poll every 30s" as "check repeatedly" and executes without delays. Removes sleep permissions when "simplifying."

**Better approach:** Inline HTML comment gates (`<!-- REQUIRED -->`), explicit `Bash(sleep:*)` in allowed-tools, adaptive backoff rules.

---

## Part 4: The Refinement Arc

This session followed a clear arc from over-engineered constraints to minimal, effective guidance.

**Phase 1: Constraint Discovery.** The status command started with prescriptive tool calls that seemed precise but prevented adaptation. When MCP tools lacked CRD fields, Claude couldn't fall back because instructions said "use THIS tool." Relaxing to outcome-focused ("get this data") unlocked Claude's problem-solving.

**Phase 2: Noise Reduction.** Adding value enumeration felt like helpful specificity but was actually noise. The breakthrough came from recognizing that dimensions (sync status AND health status) matter, not values (Synced, OutOfSync...). Claude discovers values from APIs; it needs to know what dimensions to check.

**Phase 3: Architecture Alignment.** The CLAUDE.md files in both repos were accumulating operational guidance that belonged in omni-prime. Recognizing the split—omni-prime for "how to operate" vs CLAUDE.md for "repo-specific patterns"—clarified where knowledge should live.

**Phase 4: Skill Autopsy.** Testing skill auto-trigger revealed two problems: (1) cold start matching doesn't work, and (2) even when triggered, a bloated skill buries operational tools under reference material. Restructuring to operations-first with progressive disclosure addressed both.

**Phase 5: Workflow Validation.** Systematic testing of workflow patterns (`prime && status` followed by natural language vs single-line chains) established reliable invocation patterns. The final pattern `prime && status && /skill-name task` combines context loading with explicit skill invocation in one line.

The meta-lesson: prompt engineering for Claude Code plugins is about removing obstacles, not adding precision. Claude works best with outcome definitions and minimal constraints, not step-by-step instructions.

---

## Appendix: Key Behavioral Diffs

### Status Command: Dimension Framing

**Terminal showing before/after:**

```diff
- ### ArgoCD Applications
- - Sync status: Synced, OutOfSync, Unknown
- - Health status: Healthy, Progressing, Degraded, Suspended, Missing, Unknown
- - **List any apps NOT Synced+Healthy**
+ ### ArgoCD Applications
+ - Sync status (per app)
+ - Health status (per app)
+ - **List any apps NOT Synced+Healthy**

- ### Storage (Longhorn)
- - State: attached, detached, attaching, detaching
- - Robustness: healthy, degraded, faulted, unknown
+ ### Storage (Longhorn)
+ - Volume state (attached vs detached)
+ - Volume robustness (healthy vs degraded)
```

### omni-prime: omnictl Syntax Fix

**Added after repeated `--cluster` failures:**

````markdown
### omnictl

**Cluster status (includes machine health):**
```bash
omnictl cluster status <cluster-name>
````

**List machines (if needed separately):**

```bash
omnictl get machines -l omni.sidero.dev/cluster=<cluster-name>
```

Note: `--cluster` flag does not exist. Use label selector `-l` instead.

```text

### omni-prime: Operational Pattern

**Added after skill trigger failure:**
```markdown
## Operational Pattern

When an infrastructure operation fails on first attempt:
1. Check for skill coverage before retrying with variations
2. Skills encode operational knowledge — "how do I access X" is exactly what they're for
3. Don't guess hostnames, paths, or commands — if it's not documented, ask
```

### analyze-spec: Planned vs Actual Validation

**Added to Readiness Check:**

```markdown
- **Planned vs Actual:** Compare any planned counts/values against
  actual_distribution, exit_criteria, or live cluster state.
  Flag discrepancies as "Spec needs reconciliation"
```

### Skill Restructure: Operations First

**SKILL.md now opens with:**

```markdown
## Provider Operations

Use `${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py` for provider management:

| Task | Command |
|------|---------|
| View logs | `provider-ctl.py --logs 50` |
| Raw JSON logs | `provider-ctl.py --logs 50 --raw` |
| Restart provider | `provider-ctl.py --restart` |

The provider runs on Foxtrot LXC (CT 200) — script handles SSH automatically.
```

### MCP Tool Naming Fix

**Before/after in allowed-tools:**

```markdown
# BEFORE (tools fail to resolve)
allowed-tools: Bash(omnictl:*), mcp__kubernetes__*

# AFTER (tools resolve correctly)
allowed-tools: Bash(omnictl:*), mcp__plugin_omni-scale_kubernetes__*
```

### Sleep Enforcement Gate

**Added to polling sections:**

```markdown
1. Wait 30 seconds <!-- REQUIRED - do not skip this sleep -->
2. Check status
3. If not complete, wait 60 seconds <!-- REQUIRED - increases on retry -->
```

### Disaster Recovery: Outcome-Focused Refactor (2026-01-14)

**Before (prescriptive, explicit bash):**

````markdown
### Phase 2: Destroy Cluster

1. Delete cluster:

   ```bash
   omnictl cluster template delete \
     --cluster talos-prod-01 \
     --destroy-disconnected-machines \
     ~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml
   ```

2. Verify deletion:

   ```bash
   omnictl get machines --cluster talos-prod-01  # BUG: --cluster flag doesn't exist
   ```

3. If machines still present, wait 30 seconds and check again
````

**After (outcome-focused, trust skill knowledge):**

````markdown
### Phase 2: Destroy Cluster

**Outcome:** Cluster deleted, no talos VMs remain on Proxmox.

**Pre-step:** Restart provider via
`${CLAUDE_PLUGIN_ROOT}/skills/omni-talos/scripts/provider-ctl.py --restart`
to ensure it's listening before destruction.

Delete cluster using `omnictl cluster template delete` with
`--destroy-disconnected-machines` flag. Cluster spec at
`~/dev/infra-as-code/Omni-Scale/clusters/talos-prod-01.yaml`.

**Poll:** Verify no machines remain via omnictl.
<!-- REQUIRED: sleep 30s between attempts -->

- Max wait: 10 min
- After 3 attempts, increase interval to 60s
- On timeout: consult omni-talos `references/debugging.md`
````

**Key insight:** The `--cluster` bug proves prescriptive commands go stale.
Outcome-focused commands survive because Claude uses current skill knowledge
for correct syntax.

---

## Key Learnings Summary

| Learning | Source | Confidence | Teaching Value |
|----------|--------|------------|----------------|
| Define outcomes, not tools | status.md rounds 1-2 | HIGH | Prevents tool-lock when primary tool has gaps |
| Enumerate dimensions, not values | status.md rounds 3-4 | HIGH | Reduces noise, Claude discovers values from APIs |
| Operations first in skills | omni-talos restructure | HIGH | Ensures operational tools aren't buried under docs |
| Cold start skill trigger fails | Five-whys analysis | HIGH | Plan for `prime` workflow, don't trust auto-trigger |
| Explicit skill invocation works in chains | Workflow testing | HIGH | `&& /skill-name` works, natural language in chains doesn't |
| Document repeated CLI failures in context | omnictl syntax fix | MEDIUM | Prevents same error pattern across sessions |
| Validate planned vs actual early | analyze-spec update | MEDIUM | Catches stale specs before they propagate |
| MCP tool naming requires full format | MCP compliance audit | HIGH | `mcp__plugin_<plugin>_<server>__<tool>` pattern |
| Filter logs at source for context preservation | provider-ctl.py | HIGH | Same principle as MCP—serve only what Claude needs |
| Sleep requires explicit enforcement | DR iterations | HIGH | Inline comment gates + allowed-tools + backoff rules |
| Pre-flight gate on skill knowledge | DR gate test | HIGH | Check for specific artifacts, not abstract "is loaded" |
| Outcome-focused commands trust skill | DR/bootstrap refactor | HIGH | If gate passes, Claude has the knowledge — don't repeat it |
| Restart coordination layer pre-step | DR provider issue | MEDIUM | Cheap restart beats debugging state drift |
| CNI must install before ArgoCD | DR bootstrap | HIGH | GitOps-managed CNI creates scheduling deadlock |
| ESO operator before ESO app | DR bootstrap | HIGH | CRs need CRDs from operator first |
| ArgoCD raw manifests have issues | DR bootstrap | HIGH | Use Helm or patch labels/ports/policies |
| PodSecurity labels for privileged | DR bootstrap | HIGH | K8s 1.35 blocks privileged pods by default |
| Helm --no-hooks for fresh install | DR Longhorn | HIGH | Hook dependencies on chart resources deadlock |
| Clear ArgoCD cache after fixes | DR debugging | MEDIUM | Restart controller to drop stale errors |
| External state needs manual cleanup | DR post-steps | MEDIUM | Tailscale devices, Omni SAs persist across DR |
| MCP/CLI kubeconfig contexts differ | DR fallback | MEDIUM | Don't assume context names match |
| Selector immutability blocks migration | ArgoCD manual→helm | HIGH | Delete resources before helm takeover |
