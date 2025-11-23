# claude-skill-auditor Improvements Proposal (Sub-Agent Compatible)

**Date:** 2025-11-10
**Purpose:** Add effectiveness validation to complement technical compliance checking
**Audience:** Sub-agent with zero parent context

---

## Problem Statement

**Current Gap:** Auditor validates technical compliance but not effectiveness for auto-invocation.

**Why This Matters:** A skill can pass all technical requirements (valid YAML, no forbidden files, proper structure) but still fail to be discovered and used by Claude in practice.

**Root Cause:** Technical compliance checks IF features exist, not WHETHER features enable discovery.

**Solution:** Add effectiveness checks that validate discoverability and auto-invocation potential.

---

## Proposed Addition: TIER 1.5 - Critical Effectiveness Checks

**Insert Location:** After TIER 1 (line 247), before TIER 2

**Purpose:** Validate that skills will actually be discovered and auto-invoked by Claude

**Philosophy:** A technically valid skill that never gets used is a failed skill.

---

## TIER 1.5: CRITICAL EFFECTIVENESS CHECKS (Auto-Invocation)

These checks validate whether the skill will be discovered and auto-invoked by Claude.

### 8. Trigger Quality Assessment (CRITICAL for Discovery)

**Why Critical:** The description is the ONLY thing Claude sees before deciding to load a skill. Weak triggers = skill never discovered.

#### 8.1 Concrete vs Abstract Trigger Analysis

**Principle:** Specific, concrete triggers enable discovery. Generic, abstract triggers get lost in noise.

**Check Method:**

1. Extract description field from SKILL.md YAML frontmatter
2. Identify all trigger keywords (nouns, technologies, domains, operations)
3. Classify each trigger as CONCRETE or ABSTRACT:
   - **CONCRETE:** Specific nouns (technology names, domain terms, unique operations)
   - **ABSTRACT:** Generic terms (data, information, work, help, search, find)
4. Calculate ratio: `concrete_triggers / total_triggers`
5. Apply threshold:
   - If <50% concrete: ⚠️ WARNING
   - If <25% concrete: ❌ EFFECTIVENESS-CRITICAL

**Verification:**

```bash
# Extract description from SKILL.md
grep -A 10 "^description:" SKILL.md | grep -v "^---"

# Manual analysis (cannot be automated):
# 1. List all trigger keywords from description
# 2. For each keyword, determine: CONCRETE or ABSTRACT?
# 3. Calculate percentage
```

**Classification Guidelines:**

```text
CONCRETE triggers (high specificity):
✅ Technology names: "PDF", "PostgreSQL", "React", "BigQuery"
✅ Domain terminology: "orderbooks", "invoices", "medical records", "schemas"
✅ Specific operations: "form filling", "text extraction", "rate limiting"
✅ Brand/product names: Tool-specific identifiers
✅ File formats: ".docx", ".xlsx", "JSON", "XML"

ABSTRACT triggers (low specificity):
❌ Generic nouns: "data", "information", "content", "files"
❌ Vague verbs: "help", "assist", "support", "manage"
❌ Common actions: "search", "find", "get", "process"
❌ General concepts: "work", "tasks", "items", "things"
❌ Ambiguous terms: "resources", "tools", "utilities"
```

**Test for Specificity:**

For each trigger, ask: **"How many different tools/skills could this describe?"**
- Answer >10: Too abstract (low specificity)
- Answer 3-5: Moderate specificity
- Answer 1-2: Good specificity (concrete)

**Critical Checks:**

- [ ] >50% of triggers are CONCRETE nouns (not generic terms)
- [ ] Triggers include technology-specific or domain-specific terms
- [ ] Description uses specific terminology, not generic language
- [ ] At least 2 unique identifiers present (see Section 8.3)

**Example Analysis:**

```markdown
WEAK (Too Abstract):
"Search persistent data for past work, findings, and information"

Analysis:
- "persistent data" → Generic (many tools store data)
- "past work" → Vague (what kind of work?)
- "findings" → Abstract (findings from what?)
- "information" → Generic (everything is information)
Concrete: 0/4 = 0% ❌

STRONG (Concrete):
"Extract text from PDF forms, fill PDF fields, and rotate PDF pages"

Analysis:
- "PDF" → Specific technology (appears 3 times)
- "forms" → Domain-specific (PDF forms)
- "fill PDF fields" → Specific operation
- "rotate PDF pages" → Specific operation
Concrete: 4/4 = 100% ✅
```

#### 8.2 Unique Identifier Check

**Principle:** Skills need unique identifiers to differentiate from other tools with similar purposes.

**Why Critical:** Without unique identifiers, triggers are ambiguous and match many tools weakly instead of matching one tool strongly.

**Check Method:**

1. Read description field
2. Search for unique identifiers:
   - System/tool names (brand names, product names, service names)
   - Technology names (programming languages, databases, frameworks)
   - Domain-specific terminology (field-specific jargon)
3. Count unique identifiers
4. Apply threshold:
   - If 0 unique identifiers: ❌ EFFECTIVENESS-CRITICAL
   - If 1 unique identifier: ⚠️ WARNING
   - If ≥2 unique identifiers: ✅ PASS

**Unique Identifier Types:**

```text
✅ SYSTEM/SERVICE NAMES:
- Product names: "BigQuery", "Salesforce", "Jira"
- Tool names: "pdfplumber", "pandas", "React Router"
- Service names: "AWS Lambda", "Cloud Functions"

✅ TECHNOLOGY IDENTIFIERS:
- Programming languages: "Python", "TypeScript", "Go"
- Frameworks: "Django", "Next.js", "FastAPI"
- Databases: "PostgreSQL", "MongoDB", "Redis"
- File formats: "PDF", "DOCX", "XLSX"

✅ DOMAIN-SPECIFIC TERMS:
- Finance: "orderbooks", "market data", "invoices"
- Healthcare: "FHIR", "HL7", "medical records"
- Legal: "contracts", "NDAs", "compliance"
- Engineering: "schemas", "migrations", "deployments"

❌ NOT UNIQUE IDENTIFIERS:
- Generic: "database", "server", "API", "tool"
- Vague: "system", "platform", "service"
- Common: "data", "files", "documents"
```

**Critical Checks:**

- [ ] Description includes ≥2 unique identifiers
- [ ] At least 1 identifier is the skill's primary technology/system/domain
- [ ] Identifiers are searchable keywords (not common words)

**Example Analysis:**

```markdown
WEAK (No Unique Identifiers):
"Search database for stored records and retrieve historical information"

Unique identifiers: 0
- "database" → Generic (which database?)
- "records" → Generic (what kind?)
- "historical information" → Generic
Problem: Could describe dozens of different tools ❌

STRONG (Multiple Unique Identifiers):
"Query BigQuery data warehouse using SQL for business intelligence analytics"

Unique identifiers: 3
- "BigQuery" → Specific Google service ✅
- "SQL" → Specific query language ✅
- "business intelligence" → Domain-specific ✅
Benefit: Clearly identifies what this skill does ✅
```

#### 8.3 Scope Differentiation (For Overlapping Domains)

**Principle:** Skills that operate in domains where Claude has native capabilities must clearly differentiate their scope.

**When to Check:** If skill operates in these common domains:
- Memory/history (Claude has conversation memory)
- Code generation (Claude can write code)
- Text analysis (Claude can analyze text)
- File operations (Claude can read/write files)
- Search/retrieval (Claude can search)

**Check Method:**

1. Identify if skill operates in a domain where Claude has native capabilities
2. Check if description includes scope differentiation keywords:
   - **Temporal:** "previous sessions", "days/weeks/months ago", "before", "already"
   - **Spatial:** "external database", "persistent storage", "API", "service"
   - **Explicit exclusion:** "NOT in current conversation", "outside Claude's knowledge"
   - **System-specific:** "stored in [system]", "managed by [service]"
3. Count differentiation keywords
4. Apply threshold:
   - If overlapping domain + 0 differentiation keywords: ⚠️ WARNING
   - If overlapping domain + <2 differentiation keywords: ⚠️ WARNING
   - If overlapping domain + ≥3 differentiation keywords: ✅ PASS

**Differentiation Keyword Categories:**

```text
TEMPORAL (For historical/past data skills):
✅ Time distance: "days ago", "weeks ago", "months ago", "last year"
✅ Session differentiation: "previous sessions", "past conversations"
✅ Temporal adverbs: "already", "before", "previously", "earlier"
✅ Historical: "history of", "when did", "timeline"

SPATIAL (For external data skills):
✅ Storage location: "external database", "API", "cloud storage"
✅ System names: "stored in [X]", "managed by [Y]"
✅ Persistence: "persistent storage", "permanent records"

EXPLICIT EXCLUSION (For clarity):
✅ Negation: "NOT in current conversation", "outside current context"
✅ Boundary: "beyond Claude's knowledge", "external to session"

CAPABILITY EXTENSION (For augmentation):
✅ Beyond native: "specialized analysis Claude can't do"
✅ Tools required: "requires [tool] which Claude doesn't have"
```

**Example Analysis:**

```markdown
OVERLAPPING DOMAIN WITHOUT DIFFERENTIATION:
"Search for bugs, features, and code changes"

Problem:
- Domain: Code/development (Claude already discusses code)
- Differentiation keywords: 0
- User asks: "What bugs did we fix?"
- Claude behavior: Answers from current conversation (doesn't invoke skill) ❌

OVERLAPPING DOMAIN WITH DIFFERENTIATION:
"Search external database for bugs and features from previous sessions days/weeks/months ago, NOT in current conversation"

Differentiation:
- "external database" → Spatial (not current context) ✅
- "previous sessions" → Temporal (not current session) ✅
- "days/weeks/months ago" → Temporal (specific time distance) ✅
- "NOT in current conversation" → Explicit exclusion ✅
Count: 4 keywords ✅
User asks: "What bugs did we fix?"
Claude behavior: "days/weeks/months ago" → Invoke skill ✅
```

**Critical Checks:**

- [ ] If skill overlaps with Claude's native capabilities:
  - [ ] Description includes ≥3 differentiation keywords
  - [ ] Keywords clearly define scope boundaries
  - [ ] Temporal keywords present (for historical data)
  - [ ] Spatial keywords present (for external data)

#### 8.4 Domain Overlap Analysis

**Principle:** Triggers that Claude can answer natively will rarely trigger skill invocation.

**Check Method:**

1. Extract primary triggers from description
2. For each trigger, ask: **"Can Claude answer questions about this using only current conversation context?"**
3. Count triggers where answer is YES (overlapping)
4. Count triggers where answer is NO (unique to skill)
5. Calculate overlap ratio: `overlapping_triggers / total_triggers`
6. Apply threshold:
   - If >80% overlap: ❌ EFFECTIVENESS-CRITICAL
   - If 50-80% overlap: ⚠️ WARNING
   - If <50% overlap: ✅ PASS

**Claude's Native Capabilities (Common Overlaps):**

```text
Claude CAN do from current conversation:
❌ "code in this conversation" (remembers code discussed)
❌ "bugs mentioned today" (remembers bugs from current session)
❌ "files we modified now" (remembers current file operations)
❌ "decisions made in this chat" (remembers current conversation)
❌ "ideas discussed earlier" (remembers conversation history)
❌ "text analysis" (native capability)
❌ "summarization" (native capability)

Claude CANNOT do without skill:
✅ "data from external API" (requires API access)
✅ "database queries" (requires database connection)
✅ "work from sessions last month" (no cross-session memory)
✅ "specialized domain analysis" (requires domain tools)
✅ "file format manipulation" (PDF, DOCX internals)
✅ "system automation" (requires system access)
```

**Test for Each Trigger:**

Question: **"If user asks about [trigger], can Claude answer from current conversation alone?"**

```text
Examples:

Trigger: "bugs fixed"
Q: Can Claude list bugs from current conversation?
A: YES ❌ → Overlaps with native capability

Trigger: "bugs fixed last month in external tracking system"
Q: Can Claude access tracking system from last month?
A: NO ✅ → Requires skill

Trigger: "analyze text sentiment"
Q: Can Claude analyze sentiment natively?
A: YES ❌ → Overlaps with native capability

Trigger: "extract structured data from PDF forms"
Q: Can Claude parse PDF form fields natively?
A: NO ✅ → Requires specialized tool
```

**Critical Checks:**

- [ ] <50% of triggers overlap with Claude's native capabilities
- [ ] Primary use cases require external data/tools/systems
- [ ] Description emphasizes what Claude cannot do alone

---

### 9. Capability Visibility Assessment (Navigation Complexity)

**Why Critical:** If Claude must read additional files to understand what the skill can do, discovery and correct usage suffer.

#### 9.1 Navigation Depth Analysis

**Principle:** Capabilities should be visible in SKILL.md (1-hop). Implementation details should be in reference files (2-hop).

**Check Method:**

1. Read SKILL.md completely
2. Locate "Available Operations" or "Capabilities" or "Features" section
3. For each operation/capability listed:
   - **PURPOSE visible in SKILL.md?** → 1-hop (good)
   - **Only NAME/LINK visible, must read file to understand?** → 2-hop (bad)
4. Calculate visibility ratio: `capabilities_with_visible_purpose / total_capabilities`
5. Apply threshold:
   - If <40% visible: ❌ EFFECTIVENESS-CRITICAL
   - If 40-60% visible: ⚠️ WARNING
   - If >60% visible: ✅ PASS

**What to Show vs Hide:**

```text
SHOW in SKILL.md (1-hop, enables discovery):
✅ Operation/capability names
✅ Purpose of each operation (what it does)
✅ When to use each operation (trigger conditions)
✅ Key parameters (what inputs are needed)
✅ Brief examples

HIDE in reference files (2-hop, implementation details):
✅ Detailed API documentation
✅ All parameter options and combinations
✅ Edge cases and error handling
✅ Advanced usage patterns
✅ Troubleshooting guides
```

**Navigation Patterns:**

```markdown
❌ BAD (2-hop, hidden capabilities):
## Available Operations

1. [Process Documents](operations/process.md)
2. [Extract Data](operations/extract.md)
3. [Transform Output](operations/transform.md)

Analysis:
- Capability names: Yes (process, extract, transform)
- Purposes: No (what do they process? extract from what?)
- When to use: No (must read files to know)
- Navigation: 2-hop (SKILL.md → operations/ → understand)
- Problem: Claude sees links, doesn't know which operation to use ❌

✅ GOOD (1-hop, visible capabilities):
## Available Operations

### Document Processing
- **process-pdf** - Extract text and tables from PDF documents
  - Use when: User provides PDF file and needs text/data extraction
  - Key params: filepath, extract_tables=true/false
  - Example: "Extract all tables from invoice.pdf"

- **process-docx** - Read and modify Word documents with tracked changes
  - Use when: User needs to edit .docx files or review tracked changes
  - Key params: filepath, track_changes=true/false
  - Example: "Add comment to contract.docx section 3"

For detailed API reference, see [operations/](operations/)

Analysis:
- Capability names: Yes
- Purposes: Yes (inline, clear)
- When to use: Yes (inline with examples)
- Navigation: 1-hop (SKILL.md has all info to choose)
- Benefit: Claude knows which operation to use without reading files ✅
```

**Critical Checks:**

- [ ] >60% of capabilities have PURPOSE visible in SKILL.md
- [ ] Operations include "Use when" guidance inline (not only in linked files)
- [ ] Claude can select correct operation from SKILL.md alone
- [ ] Implementation details are in reference files (correct progressive disclosure)

**Verification Method:**

```bash
# Extract operations section
sed -n '/## Available Operations/,/##/p' SKILL.md

# For each operation listed, check:
# 1. Is purpose shown inline? (not just link text)
# 2. Is "Use when" example shown inline?
# 3. Or is it just: "[Operation Name](link)" ?
```

#### 9.2 Decision Complexity Assessment

**Principle:** If skill has many operations, provide a simplified decision guide to reduce cognitive load.

**When to Check:** If skill has ≥5 operations/capabilities

**Check Method:**

1. Count total operations/capabilities in skill
2. If ≥5 operations:
   - Check if SKILL.md includes a "Decision Guide" or "Quick Decision Guide" or "What to Use When" section
   - Check if guide reduces options to 3-5 common cases
   - Check if guide covers 80%+ of expected use cases
3. Apply threshold:
   - If ≥5 operations + NO decision guide: ⚠️ WARNING
   - If ≥8 operations + NO decision guide: ❌ EFFECTIVENESS-CRITICAL
   - If decision guide exists: ✅ PASS

**Decision Guide Patterns:**

```markdown
❌ BAD (No decision guide with 10 operations):
## Available Operations

1. Search Documents
2. Search by Date
3. Search by Author
4. Search by Tags
5. Search by Type
6. Search by Content
7. Search by Metadata
8. Search by Location
9. Search Recent
10. Search All

[No guidance on which to use when]

Problem:
- 10 choices presented equally
- No routing logic
- Claude must evaluate all 10 for every user query
- High cognitive load → Slower, error-prone ❌

✅ GOOD (Decision guide for 10 operations):
## Quick Decision Guide

**What is the user searching for?**

1. **Recent items** (last 3-5 items) → Use "Search Recent"
2. **Specific content/keywords** → Use "Search by Content"
3. **Specific author/person** → Use "Search by Author"
4. **Time-based** (last week, specific date) → Use "Search by Date"
5. **Don't know** / Complex query → Use "Search All"

**Most common:** Use "Search by Content" for keyword searches.

[10 operations still listed below with full details]

Benefit:
- 10 options reduced to 5 common patterns
- Clear routing: user need → operation
- Covers 80%+ of queries
- Low cognitive load → Fast, accurate selection ✅
```

**Critical Checks:**

- [ ] If ≥5 operations: Decision guide exists
- [ ] If ≥8 operations: Decision guide is MANDATORY
- [ ] Decision guide reduces to 3-5 common cases
- [ ] Guide includes "most common" or "default" recommendation

---

### 10. Report Format Updates

**Add to Executive Summary:**

```markdown
**Breakdown:**
- Critical Issues: [count] ❌ (Violates official requirements)
- Effectiveness Issues: [count] ⚠️⚠️ (Prevents auto-invocation)
- Warnings: [count] ⚠️ (Violates best practices)
- Suggestions: [count] 💡 (Optional improvements)
```

**Add new section after "Critical Issues":**

```markdown
## Effectiveness Issues ⚠️⚠️

[If none: "✅ None identified - triggers are strong and capabilities are visible"]

### Effectiveness Issue [#]: [Brief Title]

**Severity:** EFFECTIVENESS-CRITICAL
**Category:** [Trigger Quality / Navigation Complexity]
**Impact:** [How this prevents auto-invocation]
**Location:** SKILL.md:[line] (description or section)

**Current State:**
[Quote actual content from skill]

**Problem:**
[Why this prevents effective discovery/usage]

**Analysis:**
[Show the calculation/measurement that triggered this issue]
- Concrete triggers: X/Y = Z%
- Unique identifiers: X
- Domain overlap: X%
- Capability visibility: X%

**Fix:**
[Specific improvements needed]

**Expected Improvement:**
[What this fix should achieve - more specific triggers, reduced navigation depth, etc.]

**Examples:**
[Show before/after if helpful]
```

**Update Category Breakdown:**

Add after "Official Requirements Compliance":

```markdown
### ✓ Effectiveness Compliance (Auto-Invocation Potential)

**Trigger Quality:**
- [✅/❌] Concrete triggers: >50%
- [✅/❌] Unique identifiers: ≥2
- [✅/❌] Scope differentiation: ≥3 keywords (if applicable)
- [✅/❌] Domain overlap: <50%

**Capability Visibility:**
- [✅/❌] Purpose visibility: >60%
- [✅/❌] Decision guide: Present (if ≥5 operations)
```

**Update Status Determination:**

```markdown
**Status Determination:**

- ✅ PASS: 100% official requirements + ≥60% effectiveness + 80%+ best practices
- ⚠️ NEEDS IMPROVEMENT: 100% official + effectiveness issues + <80% best practices
- ⚠️⚠️ EFFECTIVENESS FAIL: 100% official + <60% effectiveness metrics
- ❌ FAIL: <100% official requirements

**Effectiveness Scoring:**
- Trigger quality: 4 checks (Section 8)
- Capability visibility: 2 checks (Section 9)
- Total: 6 effectiveness checks
- Pass rate: (passed checks / 6) * 100%
```

---

## Implementation Checklist

To add TIER 1.5 to claude-skill-auditor.md:

- [ ] Insert TIER 1.5 header after line 247 (after TIER 1, before TIER 2)
- [ ] Add Section 8: Trigger Quality Assessment
  - [ ] Add Section 8.1: Concrete vs Abstract Trigger Analysis
  - [ ] Add Section 8.2: Unique Identifier Check
  - [ ] Add Section 8.3: Scope Differentiation
  - [ ] Add Section 8.4: Domain Overlap Analysis
- [ ] Add Section 9: Capability Visibility Assessment
  - [ ] Add Section 9.1: Navigation Depth Analysis
  - [ ] Add Section 9.2: Decision Complexity Assessment
- [ ] Add Section 10: Report Format Updates
- [ ] Update "Review Workflow" to include effectiveness checks in Step 3
- [ ] Update "Standardized Output Format" to include Effectiveness Issues section
- [ ] Update "Category Breakdown" to include Effectiveness Compliance
- [ ] Update "Status Determination" to include effectiveness scoring
- [ ] Add effectiveness verification commands to "Execution Guidelines"
- [ ] Update "Important Reminders" to include effectiveness checks

---

## Verification Commands for Effectiveness Checks

Add to "Verification Commands Reference" section:

```bash
## Effectiveness Checks (TIER 1.5)

# Extract description for trigger analysis
echo "=== TRIGGER ANALYSIS ==="
grep -A 10 "^description:" SKILL.md | grep -v "^---"

# Extract operations section for capability visibility
echo "=== CAPABILITY VISIBILITY ==="
sed -n '/## Available Operations/,/##/p' SKILL.md

# Check for decision guide (if many operations)
echo "=== DECISION GUIDE CHECK ==="
grep -i "decision\|quick guide\|what to use" SKILL.md

# Count operations/capabilities
echo "=== OPERATION COUNT ==="
grep -E "^[#]{2,3}|^[-*]|^\d+\." SKILL.md | wc -l
```

---

## Expected Impact

**Before TIER 1.5:**
- Catches: Technical violations (forbidden files, YAML errors, structure issues)
- Misses: Weak triggers, hidden capabilities, poor discoverability
- Result: Skills pass audit but fail in practice

**After TIER 1.5:**
- Catches: Technical violations + effectiveness issues
- Identifies: Weak triggers, poor navigation, domain overlap
- Result: Skills that pass audit are more likely to be auto-invoked

**Key Improvements:**
- ✅ Detects abstract/generic triggers
- ✅ Identifies missing unique identifiers
- ✅ Catches scope ambiguity in overlapping domains
- ✅ Measures capability visibility
- ✅ Assesses decision complexity
- ✅ Provides actionable fixes for effectiveness

---

## Notes for Auditor Sub-Agents

When you (the sub-agent) run these checks:

1. **Manual analysis required:** Many effectiveness checks cannot be fully automated. You must read and analyze the description and structure.

2. **No external references:** You cannot reference other skills or conversations. Use the generic principles and examples provided here.

3. **Observable patterns only:** Check what you can observe in the skill files, not what you assume about effectiveness.

4. **Be specific in reports:** When you find effectiveness issues, quote the actual content and show your analysis (percentages, counts).

5. **Balanced feedback:** If triggers are weak, acknowledge what's technically correct while explaining the effectiveness gap.

6. **Actionable recommendations:** Provide specific examples of stronger triggers using the categories in this document.

---

**This proposal is self-contained and requires no parent session context.**
