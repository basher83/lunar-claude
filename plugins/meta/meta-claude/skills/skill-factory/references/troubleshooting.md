# Troubleshooting

## Research Phase Fails

**Symptom:** `/meta-claude:skill:research` command fails with API errors

**Solutions:**

- Verify FIRECRAWL_API_KEY is set: `echo $FIRECRAWL_API_KEY`
- Check network connectivity
- Verify research script permissions: `chmod +x scripts/firecrawl_*.py`
- Try manual research and use Path 1 (skip research phase)

### Content Review Fails Repeatedly

**Symptom:** `/meta-claude:skill:review-content` fails even after applying fixes

**Solutions:**

- Review the specific issues in the quality report
- Check if issues are Tier 3 (complex) - these require manual redesign
- Consider if the skill design matches Claude Code's composition model
- Consult multi-agent-composition skill for architectural guidance

### Compliance Validation Fails

**Symptom:** `/meta-claude:skill:review-compliance` reports frontmatter or naming violations

**Solutions:**

- Run quick_validate.py manually: `scripts/quick_validate.py <skill-path>`
- Check frontmatter YAML syntax (valid YAML, required fields)
- Verify skill name follows hyphen-case convention
- Ensure description is clear and within 1024 characters

### Integration Validation Fails

**Symptom:** `/meta-claude:skill:validate-integration` reports conflicts

**Solutions:**

- Check for duplicate skill names in the plugin
- Review skill description for overlap with existing skills
- Consider renaming or refining scope to avoid conflicts
- Ensure skill complements rather than duplicates existing functionality
