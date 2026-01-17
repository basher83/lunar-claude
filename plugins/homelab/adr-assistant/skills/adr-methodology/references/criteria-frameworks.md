# Assessment Criteria Frameworks

## Salesforce Well-Architected Framework

Use for enterprise decisions involving security, user experience, and organizational scale.

### Trusted Pillar

Criteria focused on security, compliance, and governance.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Data Security | Protection of sensitive data at rest and in transit | Encryption standards met, access logged |
| Compliance | Regulatory and policy adherence | Audit trails, certifications maintained |
| Access Control | Authorization complexity and management | RBAC/ABAC implemented, least privilege |
| Audit & Governance | Traceability and oversight capabilities | Complete audit logs, change tracking |
| Data Privacy | PII handling and user consent | GDPR/CCPA compliant, consent managed |
| Identity Management | Authentication and identity federation | SSO support, MFA capability |

### Easy Pillar

Criteria focused on usability, deployment, and maintenance.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| User Experience | Impact on end-user workflows | Minimal friction, intuitive interfaces |
| Deployment Complexity | Effort to deploy and configure | Automated pipelines, IaC support |
| Integration Effort | Work to connect with existing systems | Standard APIs, documented contracts |
| Maintenance Burden | Ongoing operational overhead | Self-healing, minimal manual intervention |
| Documentation | Quality and completeness of docs | Up-to-date, example-rich, searchable |
| Onboarding | Time for new team members to contribute | Clear guides, sandbox environments |

### Adaptable Pillar

Criteria focused on scalability, flexibility, and future-proofing.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Scalability Path | Ability to handle growth | Horizontal scaling, load tested |
| Future Flexibility | Adaptability to changing requirements | Modular design, extension points |
| Cost Trajectory | Long-term cost predictability | Linear scaling, no cliff pricing |
| Team Skill Alignment | Match with team capabilities | Existing expertise, training available |
| Vendor Independence | Ability to switch providers | Standard interfaces, data portability |
| Technology Longevity | Expected lifespan and support | Active community, vendor commitment |

## Technical Trade-off Framework

Use for infrastructure, tooling, and technology selection decisions.

### Operational Pillar

Criteria focused on running and maintaining systems.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Setup Complexity | Initial configuration effort | Single command setup, sensible defaults |
| Maintenance Burden | Ongoing operational work | Auto-updates, self-tuning |
| Monitoring & Observability | Visibility into system behavior | Built-in metrics, tracing support |
| Failure Modes | How system fails and recovers | Graceful degradation, auto-recovery |
| Backup & Recovery | Data protection capabilities | Point-in-time recovery, tested restores |
| Resource Efficiency | Compute/memory/storage usage | Right-sized, efficient algorithms |

### Development Pillar

Criteria focused on building and evolving systems.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Learning Curve | Time to productive usage | Good tutorials, familiar patterns |
| Development Velocity | Speed of feature delivery | Fast iteration, good tooling |
| Testing Approach | Ease of testing and validation | Test frameworks, mocking support |
| Documentation Quality | Usefulness of available docs | Complete API docs, examples |
| Debugging Experience | Ease of troubleshooting | Clear errors, debugging tools |
| Local Development | Ability to develop locally | Docker support, lightweight mode |

### Integration Pillar

Criteria focused on system interoperability.

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Ecosystem Compatibility | Fit with existing stack | Standard protocols, adapters exist |
| Migration Path | Effort to adopt or leave | Import/export tools, gradual migration |
| Dependency Management | Third-party dependency burden | Few dependencies, stable versions |
| Lock-in Risk | Difficulty switching away | Open standards, data export |
| API Stability | Breaking change frequency | Semantic versioning, deprecation policy |
| Extensibility | Ability to customize behavior | Plugin system, hooks available |

## Custom Framework Construction

When neither standard framework fits, construct criteria from decision drivers.

### Process

1. **Extract drivers**: List 3-5 key factors from context
2. **Create measurable criteria**: Each driver becomes 1-2 criteria
3. **Define "good"**: Specify what success looks like for each
4. **Include reversibility**: Add at least one criterion about switching costs

### Example: Build vs Buy Decision

Drivers: Time to market, customization needs, long-term cost

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Time to Value | How quickly can we deliver | Production in weeks, not months |
| Customization Depth | Ability to modify for our needs | Core workflows adjustable |
| Total Cost of Ownership | 5-year cost projection | Predictable, within budget |
| Exit Strategy | Ability to switch later | Data exportable, alternatives exist |

### Example: Monolith vs Microservices

Drivers: Team structure, deployment frequency, failure isolation

| Criterion | Description | Good Looks Like |
|-----------|-------------|-----------------|
| Team Autonomy | Independent team delivery | Deploy without coordination |
| Deployment Frequency | Release cadence capability | Multiple deploys per day |
| Blast Radius | Impact of component failure | Failures contained, graceful degradation |
| Operational Complexity | Infrastructure overhead | Manageable with current team |
| Data Consistency | Transaction handling | Acceptable consistency model |

## Framework Selection Guide

| Decision Type | Recommended Framework |
|---------------|----------------------|
| Enterprise system selection | Salesforce Well-Architected |
| Security-sensitive choices | Salesforce Well-Architected (Trusted focus) |
| User-facing applications | Salesforce Well-Architected (Easy focus) |
| Infrastructure tooling | Technical Trade-off |
| Database selection | Technical Trade-off |
| CI/CD pipeline choices | Technical Trade-off (Development focus) |
| Build vs buy | Custom |
| Architecture style | Custom |
