# Risk Ratings

## Definitions

| Rating | Definition | Governance Required |
|--------|------------|---------------------|
| **Low** | Minimal risk to current or future requirements, performance, or scale | Standard review |
| **Medium** | Manageable risk with proper governance in place | Documented mitigation |
| **High** | Significant risk without active mitigation; may block requirements | Explicit acceptance |

## Detailed Rating Criteria

### Low Risk

Assign Low when the option:

- Aligns naturally with stated constraints
- Has no significant trade-offs identified
- Matches team's proven experience
- Is reversible if the decision proves wrong
- Has successful precedent in similar contexts
- Requires no special handling or monitoring

**Governance**: Standard review process. No additional documentation beyond the ADR.

**Example rationale**: "Low risk. Team has 3 years PostgreSQL experience, matches existing stack, well-understood failure modes."

### Medium Risk

Assign Medium when the option:

- Has trade-offs that exist but are manageable
- Requires discipline to avoid known pitfalls
- Involves some learning curve for the team
- Is partially reversible (migration possible but costly)
- Has known limitations that need monitoring
- Requires specific practices to succeed

**Governance**: Document mitigation strategy. Identify owner responsible for monitoring.

**Example rationale**: "Medium risk. Requires team training on event sourcing patterns. Mitigation: allocate 2 weeks for team workshops before implementation."

### High Risk

Assign High when the option:

- Directly conflicts with a stated requirement
- Requires significant mitigation effort to be viable
- Team lacks experience in the domain
- Is difficult or expensive to reverse
- Has known failure modes that could be severe
- Introduces significant technical debt

**Governance**: Explicit acceptance required from stakeholders. Document accepted risks and contingency plans.

**Example rationale**: "High risk. No team experience with Cassandra's eventual consistency model. Accepted because: global scale requirement has no alternatives. Mitigation: hire consultant for first 6 months."

## Rating Consistency Guidelines

### Within a Single Criterion

When rating the same criterion across options:

1. **At least one option should be Low or Medium**
   - If all options are High, the criterion may be a blocker, not a trade-off
   - Consider whether the criterion is actually relevant to this decision

2. **Ratings are relative to this decision's context**
   - "High complexity" for a 3-person team might be "Low" for a 50-person team
   - Consider the specific constraints and capabilities

3. **Differentiate between options**
   - If all options have the same rating, the criterion doesn't help discriminate
   - Either refine the criterion or acknowledge it's not a differentiator

### Across the Matrix

1. **No option should be all Low**
   - If an option has no trade-offs, the analysis may be incomplete
   - Ensure you've considered operational, development, and business impacts

2. **No option should be all High**
   - If an option has no strengths, why is it being considered?
   - Either drop the option or reconsider the criteria

3. **Balance the matrix**
   - Each option should have a mix of ratings
   - This reflects real-world trade-offs

## Writing Effective Rationales

### Structure

Each rating should include:
1. The risk level (Low/Medium/High)
2. Brief rationale (1-2 sentences)
3. Mitigation if Medium/High

### Good Rationale Examples

**Low**:
> "Low. Native Kubernetes support with mature Helm charts. Team deployed similar stacks in last 3 projects."

**Medium**:
> "Medium. GraphQL requires schema management discipline. Mitigation: implement schema registry from day one."

**High**:
> "High. Real-time sync conflicts with offline-first requirement. Accepted trade-off: limited offline capability for initial release."

### Poor Rationale Examples

Avoid vague or unjustified rationales:

- ❌ "Medium. Some concerns." (What concerns?)
- ❌ "Low. Should be fine." (Why?)
- ❌ "High. Complex." (What makes it complex?)

## Aggregating Ratings

### Weighted Approach

Not all criteria are equally important. Consider weighting:

| Weight | When to Apply |
|--------|---------------|
| **Critical** | Requirement is non-negotiable |
| **Important** | Significant impact on success |
| **Nice-to-have** | Beneficial but not essential |

A single High rating on a Critical criterion may outweigh multiple Low ratings on Nice-to-have criteria.

### Decision Heuristics

1. **No High on Critical criteria**: Option may be blocked
2. **Multiple High ratings**: Option needs strong justification
3. **Mostly Medium**: Viable with governance
4. **Mostly Low**: Strong candidate, verify nothing is missed

## Common Rating Mistakes

### Mistake 1: Rating Optimistically

**Problem**: Underestimating risks due to enthusiasm for an option.

**Fix**: Ask "What would make this fail?" before rating.

### Mistake 2: Rating Without Context

**Problem**: Using absolute judgments instead of relative to constraints.

**Fix**: Always reference specific project constraints in rationale.

### Mistake 3: Inconsistent Criteria Interpretation

**Problem**: Applying different standards to different options.

**Fix**: Rate all options for one criterion before moving to the next.

### Mistake 4: Missing Mitigations

**Problem**: Assigning Medium/High without explaining how to address the risk.

**Fix**: Every Medium/High rating needs a mitigation strategy or explicit acceptance.

## Rating Review Checklist

Before finalizing ratings:

- [ ] Each rating has a specific rationale
- [ ] Medium/High ratings have mitigations or explicit acceptance
- [ ] No criterion has all options rated the same
- [ ] No option is rated all Low or all High
- [ ] Ratings reflect this project's specific constraints
- [ ] Critical criteria are identified and weighted appropriately
- [ ] Stakeholders can understand and challenge the ratings
