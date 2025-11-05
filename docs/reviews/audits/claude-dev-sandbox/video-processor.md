# Audit Report: video-processor

**Skill Path:** `plugins/meta/claude-dev-sandbox/skills/video-processor/SKILL.md`
**Status:** ⚠️ Needs Improvement (73% compliance)
**Compliance:** 73%
**Last Audit:** 2025-11-05
**Auditor:** claude-skill-auditor
**Files Reviewed:** SKILL.md (303 lines), scripts/video_processor.py (433 lines)

---

## Category Breakdown

- [ ] 1. YAML Frontmatter - ❌ (Name has spaces/uppercase, description not third person)
- [x] 2. File Structure - ✓ (303 lines, well organized with scripts/ subdirectory)
- [ ] 3. Description Quality - ❌ (Not third person, uses imperative "Use when")
- [ ] 4. Naming Convention - ❌ (Should use lowercase-hyphen format)
- [~] 5. Content Quality - ⚠️ (Good balance but inconsistent paths, mixed voice in examples)
- [x] 6. Progressive Disclosure - ✓ (Appropriate for complexity level)
- [x] 7. File Paths - ✓ (Uses forward slashes, descriptive names)
- [x] 8. Workflows & Patterns - ✓ (Excellent step-by-step workflows)
- [x] 9. Code & Scripts - ✓ (Excellent error handling, PEP 723 dependencies)
- [ ] 10. MCP Tool References - N/A
- [x] 11. Examples Quality - ✓ (Comprehensive, realistic scenarios)
- [x] 12. Anti-Patterns - ✓ (None present)
- [ ] 13. Testing Coverage - ⚠️ (Test recommendations provided)
- [x] 14. Overall Compliance - 73%

---

## Critical Issues (Must Fix)

**Total:** 2 critical issues

### 1. Invalid YAML frontmatter name format

- **Location:** SKILL.md:2
- **Current:** `name: Video Processor`
- **Required:** Name must use only lowercase letters, numbers, and hyphens (no spaces, no uppercase)
- **Fix:** Change to `name: video-processor` or `name: videoprocessor`
- **Reference:** skills.md - YAML frontmatter requirements

### 2. Description not written in third person

- **Location:** SKILL.md:3
- **Current:** "Use when user mentions..." is second person imperative
- **Required:** Description must be written in third person (no "use when", "you can", "I can")
- **Fix:** Rewrite as: "Processes video files with audio extraction, format conversion (mp4, webm), and Whisper transcription for multimedia content processing. Activated when handling video conversion, audio extraction, transcription, or working with mp4, webm, ffmpeg, and whisper tools."
- **Reference:** agent-skills-best-practices.md - Description quality section

---

## Warnings (Should Fix)

**Total:** 3 warnings

### 1. Description could be more specific about WHEN to use

- **Location:** SKILL.md:3
- **Current:** Lists many trigger words but doesn't explain the use case context
- **Recommended:** Add context about the type of work: "for multimedia content processing and speech-to-text conversion"
- **Impact:** Claude may struggle to determine when this skill is relevant vs other video/audio tools
- **Reference:** agent-skills-best-practices.md - Description should state WHAT and WHEN

### 2. Inconsistent terminology for script paths

- **Location:** SKILL.md:53, 66, 79, 93, etc.
- **Current:** Uses `.claude/skills/video-processor/scripts/video_processor.py` (incorrect path)
- **Recommended:** Should use consistent path relative to skill location: `scripts/video_processor.py` or full path from project root
- **Impact:** Copy-paste commands will fail; creates confusion about actual file location
- **Reference:** agent-skills-best-practices.md - Consistency section

### 3. Examples use second person voice

- **Location:** SKILL.md:180-292 (entire Examples section)
- **Current:** "You would..." throughout all examples
- **Recommended:** Rewrite in instructional/imperative form: "1. Use the to-mp4 command..." or third person: "Claude should use..."
- **Impact:** Inconsistent voice with description requirements; less professional
- **Reference:** agent-skills-best-practices.md - Consistency in voice and tone

---

## Suggestions (Consider Improving)

**Total:** 4 suggestions

### 1. Add feedback loop for transcription verification

- **Enhancement:** Add workflow step for quality verification
- **Example:** "4. Preview transcript output and ask user if accuracy is acceptable"
- **Benefit:** Transcription quality is critical; users often need to verify/correct output

### 2. Consider progressive disclosure for long script

- **Enhancement:** 433-line Python script could have its documentation extracted to separate reference file
- **Example:** Move detailed API usage to `reference/script-api.md` and keep only essential usage in SKILL.md
- **Benefit:** Better organization for complex script documentation

### 3. Add troubleshooting section

- **Enhancement:** Add "Common Issues" section covering FFmpeg and Whisper problems
- **Example:** Cover: "FFmpeg not found, Whisper model download failures, permission errors"
- **Benefit:** FFmpeg and Whisper have common installation/permission issues

### 4. Add performance expectations

- **Enhancement:** Document processing time expectations
- **Example:** "Processing time estimates: 1-minute video transcription with base model ~2-3 minutes on typical hardware"
- **Benefit:** Users need to understand processing time expectations

---

## Actionable Items

1. ❌ Change YAML name from `Video Processor` to `video-processor` (CRITICAL)
2. ❌ Rewrite description to third person without "Use when" (CRITICAL)
3. ⚠️ Fix all script path examples (15+ locations) to use correct relative paths
4. ⚠️ Rewrite all examples (lines 180-292) to remove second person "You would"
5. ⚠️ Add context to description about use case type
6. 💡 Consider adding troubleshooting section
7. 💡 Consider adding performance expectations
8. 💡 Consider progressive disclosure for script documentation
9. 💡 Consider adding transcription verification workflow

---

## Positive Observations

- ✅ **Excellent script implementation** - Professional error handling, clear CLI interface, PEP 723 dependencies
- ✅ **Comprehensive examples** - Five detailed examples covering realistic use cases
- ✅ **Clear prerequisites** - Installation instructions for all dependencies across multiple platforms
- ✅ **Good technical depth** - Explains FFmpeg/Whisper integration, audio format requirements, performance
- ✅ **Proper validation** - Script validates input files, checks dependencies, provides helpful error messages
- ✅ **Well-structured workflows** - Step-by-step instructions for all major operations
- ✅ **Appropriate supporting files** - Python script in separate file demonstrates good progressive disclosure
- ✅ **Professional code quality** - Script follows best practices with type hints, docstrings, error handling

---

## Testing Recommendations

- [x] Test with Haiku - Clear structure and examples should work well
- [x] Test with Sonnet - Good balance of guidance without over-explanation
- [x] Test with Opus - Avoids over-explaining basics
- [ ] Create evaluation: Convert AVI to MP4
- [ ] Create evaluation: Extract audio and transcribe with language specification
- [ ] Create evaluation: Batch processing multiple videos
- [ ] Test error handling: FFmpeg not installed scenario
- [ ] Test error handling: Unsupported file format scenario
- [ ] Verify uv run works in Claude Code environment (may need absolute paths)

---

## Compliance Summary

**Official Requirements:** 4/6 requirements met (67%)

- ❌ Name format (must be lowercase-hyphen)
- ❌ Description third person voice
- ✅ YAML structure valid
- ✅ SKILL.md exists
- ✅ Description under 1024 characters
- ✅ Name under 64 characters

**Best Practices:** 18/22 practices followed (82%)

- Strong technical content and examples
- Minor inconsistencies in paths and voice
- Could enhance with troubleshooting section

**Overall Compliance:** 73%

---

## Next Steps

1. Fix the 2 critical YAML frontmatter issues (name format and description voice)
2. Fix inconsistent script paths throughout examples
3. Rewrite examples to use consistent imperative/third person voice
4. Consider implementing the 4 optional suggestions for enhanced usability
5. Re-audit after fixes to verify 90%+ compliance
