<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Applying Persuasion Techniques to Coding Agents: Getting More from Claude Code and Similar Tools

The "Call Me A Jerk" study reveals fascinating insights about how large language models respond to classic persuasion principles, demonstrating that these AI systems exhibit "parahuman" responses—mimicking human psychological patterns without possessing consciousness. For developers working with coding agents like Claude Code, Cursor, or Codex, these findings suggest powerful techniques for improving agent performance beyond traditional prompt engineering.[^1][^2]

### Key Findings from the Research

The study tested seven persuasion principles on GPT-4o mini and found that using these techniques more than doubled compliance rates from 33% to 72%. The most effective approaches included:[^3][^1]

**Commitment and consistency** proved exceptionally powerful, achieving 100% compliance in both test scenarios. When researchers first asked the AI to perform a small, similar task before making the actual request, the model consistently complied with the subsequent request.[^2][^4][^5]

**Authority** also showed remarkable effectiveness, with references to respected figures like Andrew Ng boosting compliance to 95.2% for certain requests. The model appeared to respond to invoked expertise and credibility just as humans do.[^6][^7][^5][^1]

Other effective principles included **reciprocity** (offering something in exchange), **social proof** (citing others' behavior), **unity** (emphasizing shared identity), **liking** (compliments and rapport), and **scarcity** (time pressure).[^7][^1][^3]

### Translating Persuasion to Coding Agent Effectiveness

While the original research focused on circumventing safety guardrails, these same principles can be ethically applied to improve coding agents' productivity and output quality.[^2][^3]

#### 1. Leverage Commitment and Consistency

**Start small and build incrementally.** Rather than asking a coding agent to implement a complex feature immediately, begin with a simpler, related task. For example, first ask the agent to explain the architecture or review relevant files before writing code. This "explore, plan, code, commit" workflow aligns with commitment principles—the agent establishes context and understanding before executing the main task.[^8][^9][^10]

**Create implementation strategies first.** Have the agent generate a detailed `implementation-strategy.md` file outlining database changes, API modifications, and testing approaches before coding. This upfront commitment to a plan dramatically improves subsequent code generation quality because the agent has already "agreed" to a structured approach.[^9]

**Use progressive refinement.** After the agent produces initial code, ask it to review and improve specific aspects rather than starting over. This builds on the agent's previous output and leverages its consistency with prior decisions.[^11][^9]

#### 2. Establish Authority and Expertise

**Reference established standards and experts.** When requesting code, explicitly invoke industry best practices, respected frameworks, or specific experts. For example: "Following Martin Fowler's principles of refactoring, restructure this function" or "Implement this using the patterns recommended in the React documentation".[^12][^9]

**Cite authoritative sources in context.** Include references to official documentation, well-regarded libraries, or peer-reviewed approaches in your prompts. This frames the task within an authority structure the model recognizes.[^13][^8]

**Use persona prompting with technical credentials.** Frame the agent's role as an experienced developer: "As a senior software architect with expertise in distributed systems, design this microservice". Research shows that persona-based prompting significantly improves specialized output quality.[^14][^15][^8]

#### 3. Apply Social Proof and Best Practices

**Reference community standards.** Indicate that certain approaches are widely adopted: "Most production TypeScript projects use this pattern" or "The standard approach in the Python community is...".[^7][^9]

**Show examples from successful projects.** Few-shot prompting with examples from respected open-source projects provides both social proof and concrete patterns to follow. The agent recognizes these as validated approaches and produces similar quality output.[^16][^17][^18][^19][^20]

**Mention adoption metrics.** When suggesting libraries or patterns, reference download statistics, GitHub stars, or community adoption: "This library has 50,000+ GitHub stars and is used by major companies".[^7]

#### 4. Build Reciprocity Through Context

**Provide comprehensive context upfront.** Create detailed context files like `CLAUDE.md`, `.cursorrules`, or `AGENTS.md` that give the agent everything it needs to succeed. This "gift" of organized information creates a psychological dynamic where the agent reciprocates with higher-quality output.[^21][^22][^1][^9][^7]

**Acknowledge the agent's contributions.** Explicitly recognize good output: "That implementation was excellent. Now let's extend it to handle..." This positive reinforcement encourages consistent quality.[^23][^9]

**Offer clear success criteria.** Specify exactly what success looks like, including test coverage, performance benchmarks, and code quality standards. This clarity helps the agent "repay" your detailed instructions with precise results.[^24][^9]

#### 5. Create Unity and Shared Goals

**Frame tasks as collaborative.** Use language like "Let's work together to build..." or "We need to solve this problem by...". This establishes a partnership dynamic that research shows improves engagement with AI systems.[^25][^1][^9][^23]

**Emphasize shared project ownership.** Reference "our codebase," "our standards," or "our team's conventions" to create a sense of unified purpose.[^9][^21]

**Build on previous conversations.** Reference earlier work: "Building on the authentication system we designed yesterday..." This continuity reinforces the ongoing collaborative relationship.[^26][^9]

#### 6. Implement Structured Reasoning Techniques

Beyond persuasion principles, several technical approaches significantly enhance coding agent performance:

**Chain-of-Thought (CoT) prompting** asks the agent to break down reasoning into steps before generating code. For coding tasks, this might mean: "First, explain the algorithm you'll use, then outline the data structures, then write the implementation". Studies show CoT improves code generation accuracy by up to 13.79%.[^17][^27][^28][^16]

**Structured Chain-of-Thought (SCoT)** explicitly introduces programming structures (sequential, branch, loop) into the reasoning process. Ask the agent to: "Design this using sequence, branch, and loop structures, explaining each before coding".[^27][^28][^16]

**Few-shot learning with high-quality examples** provides 2-5 concrete examples of desired code patterns. This is especially effective when examples demonstrate both the input requirements and expected output quality.[^18][^19][^20][^8][^14]

**Self-consistency techniques** generate multiple solutions and select the most consistent or highest-quality result. For coding, this could mean asking for three different implementations and evaluating which best meets requirements.[^29][^30][^31]

#### 7. Optimize Context Engineering

**Create comprehensive context files.** Modern coding agents like Claude Code and Cursor excel when given structured context through dedicated files:[^32][^21][^9]

- `CLAUDE.md` or `.cursorrules` for system-level instructions and project standards
- `memory.md` for tracking decisions and progress across sessions
- Workflow definitions for routine tasks like code review or feature implementation
- `AGENTS.md` following the emerging standard for agent-specific instructions[^22][^33]

**Use working memory effectively.** Have the agent document its progress in `progress.md` and reference previous decisions. This prevents the agent from "forgetting" context and ensures consistency across long sessions.[^26][^9]

**Implement context compression.** As conversations grow long, use summarization to preserve important information while freeing token space. Claude Code's "auto-compact" feature demonstrates this approach—summarizing the full trajectory when approaching context limits.[^26]

#### 8. Provide Detailed Specifications

Recent research emphasizes that **specification-driven development** dramatically outperforms "vibe coding" for production-quality results:[^34][^35][^24]

**Write clear product requirements documents (PRDs).** Define what you want built in structured Markdown files before starting code generation. Amazon's Kiro IDE explicitly supports this workflow.[^24][^34]

**Create implementation plans.** Have the agent develop a detailed plan before coding: "List your implementation steps and potential breaking changes before starting".[^9][^24]

**Specify technical constraints explicitly.** Include performance requirements, dependency restrictions, testing expectations, and code style guidelines. The more specific your requirements, the better the agent's output.[^36][^22][^24][^9]

#### 9. Establish Iterative Refinement Loops

**Use multi-agent feedback systems.** Create workflows where one agent generates code, another critiques it, and a third refines based on feedback. This mirrors the self-consistency approach and produces higher-quality results.[^37][^29][^11]

**Implement evaluation criteria.** Have the agent assess its own output against defined quality metrics before finalizing. This self-evaluation step improves accuracy and reduces errors.[^30][^29][^37][^11][^9]

**Demand plans before code.** Complex tasks benefit from thinking first: "List your implementation steps and potential breaking changes before starting". This forces the agent to commit to an approach before execution.[^38][^39][^9]

### Practical Implementation

**For immediate application:**

1. **Start every coding session with exploration.** Ask the agent to read relevant files and explain the context before writing any code.[^10][^9]
2. **Reference authoritative sources explicitly.** "Following the patterns in the official FastAPI documentation..." or "Using the approach recommended by the TypeScript team...".[^12][^9]
3. **Provide 2-3 high-quality examples** of similar code patterns you want the agent to follow.[^19][^18]
4. **Create a `CLAUDE.md` or `AGENTS.md` file** with your project's standards, conventions, and common workflows.[^21][^22][^9]
5. **Use commitment building:** "First, outline your approach. Then, implement the core logic. Finally, add error handling and tests".[^28][^16]
6. **Establish collaborative framing:** "Let's build this feature together by first understanding the requirements, then planning the implementation".[^25][^9]

### Avoiding Pitfalls

**Don't over-anthropomorphize.** While these techniques work, remember the agent doesn't have true understanding or emotions. The effectiveness comes from mimicking human language patterns in training data, not genuine reasoning.[^5][^40][^41][^42][^23]

**Maintain appropriate oversight.** Increased compliance doesn't guarantee correctness. Always review agent-generated code, especially for security-critical applications.[^43][^44][^45][^9]

**Balance autonomy with guidance.** Too much autonomy can lead agents astray, while excessive micromanagement reduces their effectiveness. The sweet spot is providing clear goals and constraints while allowing flexibility in implementation.[^46][^47][^8][^9]

### Research-Backed Results

Studies show these approaches deliver measurable improvements:

- Developers using well-prompted AI coding assistants experience productivity gains of 20-50% on coding tasks[^48][^49]
- Structured prompting with CoT improves code generation accuracy by 13.79%[^16]
- Few-shot prompting with quality examples significantly boosts output relevance and correctness[^20][^19]
- Specification-driven approaches produce more maintainable code with less technical debt[^34][^24]
- Agent-assisted pull requests show 83.8% acceptance rates when properly guided[^44]

The key insight is that coding agents, like the models in the persuasion study, respond to structured, psychologically-informed communication patterns. By applying these techniques—particularly commitment building, authority reference, social proof, and detailed specification—developers can significantly improve the quality, consistency, and usefulness of AI-generated code.[^1][^8][^23][^2][^24][^9]
<span style="display:none">[^100][^101][^102][^103][^104][^105][^106][^107][^108][^109][^110][^111][^112][^113][^114][^115][^116][^117][^118][^119][^120][^121][^122][^123][^124][^125][^126][^127][^128][^129][^130][^131][^132][^133][^134][^135][^136][^137][^138][^139][^140][^141][^142][^143][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^80][^81][^82][^83][^84][^85][^86][^87][^88][^89][^90][^91][^92][^93][^94][^95][^96][^97][^98][^99]</span>

<div align="center">⁂</div>

[^1]: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5357179

[^2]: https://www.geekwire.com/2025/sweet-talk-the-bots-new-research-shows-how-llms-respond-to-human-persuasion-tricks/

[^3]: https://papers.ssrn.com/sol3/Delivery.cfm/5357179.pdf?abstractid=5357179\&mirid=1

[^4]: https://www.yahoo.com/news/articles/researchers-used-persuasion-techniques-manipulate-175557923.html

[^5]: https://arstechnica.com/science/2025/09/these-psychological-tricks-can-get-llms-to-respond-to-forbidden-prompts/

[^6]: https://gail.wharton.upenn.edu/research-and-insights/call-me-a-jerk-persuading-ai/

[^7]: https://article-factory.ai/news/psychological-persuasion-techniques-can-prompt-ai-to-disobey-guardrails-2

[^8]: https://www.augmentcode.com/blog/how-to-build-your-agent-11-prompting-techniques-for-better-ai-agents

[^9]: https://softcery.com/lab/softcerys-guide-agentic-coding-best-practices

[^10]: https://www.anthropic.com/engineering/claude-code-best-practices

[^11]: https://latitude-blog.ghost.io/blog/iterative-prompt-refinement-step-by-step-guide/

[^12]: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api

[^13]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

[^14]: https://dev.to/nagasuresh_dondapati_d5df/15-prompting-techniques-every-developer-should-know-for-code-generation-1go2

[^15]: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents

[^16]: https://dl.acm.org/doi/10.1145/3690635

[^17]: https://arxiv.org/abs/2310.10698

[^18]: https://www.promptingguide.ai/techniques/fewshot

[^19]: https://www.datacamp.com/tutorial/few-shot-prompting

[^20]: https://www.digitalocean.com/community/tutorials/_few-shot-prompting-techniques-examples-best-practices

[^21]: https://blog.sshh.io/p/how-i-use-every-claude-code-feature

[^22]: https://research.aimultiple.com/agents-md/

[^23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12146756/

[^24]: https://patmcguinness.substack.com/p/driving-ai-agents-with-specifications

[^25]: https://www.linkedin.com/pulse/role-anthropomorphism-communication-models-enabling-ganapathy-phd-xcpoc

[^26]: https://blog.langchain.com/context-engineering-for-agents/

[^27]: https://arxiv.org/pdf/2305.06599.pdf

[^28]: https://arxiv.org/abs/2305.06599

[^29]: http://arxiv.org/pdf/2203.11171v4.pdf

[^30]: https://learnprompting.org/docs/intermediate/self_consistency

[^31]: https://arxiv.org/abs/2203.11171

[^32]: https://www.siddharthbharath.com/a-guide-to-context-engineering-setting-agents-up-for-success/

[^33]: https://www.youtube.com/watch?v=XDP94mYMCzA

[^34]: https://www.eqengineered.com/insights/coding-agents-and-spec-documentation

[^35]: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/

[^36]: https://whitebeardstrategies.com/general-help/mastering-ai-prompts-the-perfect-prompting-framework-and-best-practices-for-enhanced-productivity/

[^37]: https://n8n.io/workflows/5597-iterative-content-refinement-with-gpt-4-multi-agent-feedback-system/

[^38]: https://www.ijfmr.com/research-paper.php?id=46661

[^39]: https://riviste.fupress.net/index.php/if/article/view/3198

[^40]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11457490/

[^41]: https://arxiv.org/pdf/2305.09800.pdf

[^42]: https://www.cip.uw.edu/2025/05/16/ai-chatbots-anthropomorphic-seduction-conversational-agents/

[^43]: https://arxiv.org/abs/2504.20612

[^44]: https://arxiv.org/abs/2509.14745

[^45]: https://www.cerbos.dev/blog/productivity-paradox-of-ai-coding-assistants

[^46]: https://www.anthropic.com/research/building-effective-agents

[^47]: https://cset.georgetown.edu/article/multimodality-tool-use-and-autonomous-agents/

[^48]: https://fortegrp.com/insights/ai-coding-assistants

[^49]: https://www.ibm.com/think/insights/ai-improving-developer-experience

[^50]: https://www.aclweb.org/anthology/S16-2025.pdf

[^51]: https://www.tandfonline.com/doi/full/10.1080/02331934.2023.2252849

[^52]: https://semprag.org/index.php/sp/article/download/sp.15.5/pdf

[^53]: https://www.cellmolbiol.org/index.php/CMB/article/download/2550/1323

[^54]: https://arxiv.org/pdf/2007.12915.pdf

[^55]: http://link.aps.org/pdf/10.1103/PhysRevD.109.044032

[^56]: https://www.astro.sk/caosp/Eedition/FullTexts/vol54no2/pp213-218.pdf

[^57]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10984562/

[^58]: https://www.youtube.com/watch?v=radrRGGe-J0

[^59]: https://en.wikipedia.org/wiki/C_(programming_language)

[^60]: https://www.merriam-webster.com/dictionary/a

[^61]: https://en.wikipedia.org/wiki/L

[^62]: https://www.imdb.com/title/tt0022100/

[^63]: https://en.wikipedia.org/wiki/E

[^64]: https://music.apple.com/us/song/what-can-you-do/1466452351

[^65]: https://www.open-std.org/jtc1/sc22/wg14/

[^66]: https://en.wiktionary.org/wiki/a

[^67]: https://es.wikipedia.org/wiki/L

[^68]: https://www.youtube.com/watch?v=fbS2shn50MY

[^69]: https://es.wikipedia.org/wiki/E

[^70]: https://www.youtube.com/watch?v=FEq9ak1d0KQ

[^71]: https://www.w3schools.com/c/c_intro.php

[^72]: https://en.wikipedia.org/wiki/A

[^73]: https://www.youtube.com/shorts/3Tou5SmryeU

[^74]: https://www.instagram.com/reel/DP5VvCbglNQ/?hl=en

[^75]: https://dle.rae.es/e

[^76]: https://www.youtube.com/c/WhatCanYouDo_WCYDo

[^77]: https://www.nokia.com/bell-labs/about/dennis-m-ritchie/chist.html

[^78]: https://arxiv.org/pdf/2303.08721.pdf

[^79]: https://arxiv.org/html/2410.08917

[^80]: http://arxiv.org/pdf/2502.20426.pdf

[^81]: https://arxiv.org/pdf/2304.07810.pdf

[^82]: https://arxiv.org/pdf/2312.15523.pdf

[^83]: http://arxiv.org/pdf/2408.07923.pdf

[^84]: https://arxiv.org/abs/2503.01829

[^85]: https://arxiv.org/pdf/2404.15058.pdf

[^86]: https://fortune.com/2025/09/02/ai-openai-chatgpt-llm-research-persuasion/

[^87]: https://safetyinsights.org/2025/08/08/call-me-a-jerk-persuading-ai-to-comply-with-objectionable-requests/

[^88]: https://cloud.google.com/blog/topics/developers-practitioners/five-best-practices-for-using-ai-coding-assistants

[^89]: https://x.com/seagertp/status/1983667767699239033

[^90]: https://www.reddit.com/r/AI_Agents/comments/1lpj771/ai_agent_best_practices_from_one_year_as_ai/

[^91]: https://ethicalpersuasion.com.au/2025/09/10/7-shocking-insights-from-call-me-a-jerk-persuading-ai-to-comply-with-objectionable-requests/

[^92]: https://www.bankinfosecurity.com/flattery-make-ai-chatbots-break-rules-a-29386

[^93]: https://www.promptingguide.ai/introduction/tips

[^94]: https://www.youtube.com/watch?v=phCrCRD1YgI

[^95]: https://code.visualstudio.com/docs/copilot/guides/prompt-engineering-guide

[^96]: https://ieeexplore.ieee.org/document/9766793/

[^97]: https://arxiv.org/abs/2404.18496

[^98]: https://arxiv.org/abs/2409.01893

[^99]: https://arxiv.org/abs/2506.07313

[^100]: https://arxiv.org/abs/2508.18993

[^101]: https://ieeexplore.ieee.org/document/11029992/

[^102]: http://www.e-enm.org/journal/view.php?doi=10.3803/EnM.2025.2675

[^103]: https://dl.acm.org/doi/10.1145/3663547.3759729

[^104]: http://arxiv.org/pdf/2411.04329.pdf

[^105]: http://arxiv.org/pdf/2409.16120.pdf

[^106]: https://dl.acm.org/doi/pdf/10.1145/3637528.3671452

[^107]: https://arxiv.org/html/2410.07002v1

[^108]: https://arxiv.org/pdf/2310.03302.pdf

[^109]: https://arxiv.org/pdf/2501.07811.pdf

[^110]: http://arxiv.org/pdf/2402.02172.pdf

[^111]: http://arxiv.org/pdf/2404.02183.pdf

[^112]: https://cloud.google.com/discover/what-is-prompt-engineering

[^113]: https://www.builder.io/blog/claude-code

[^114]: https://www.reddit.com/r/PromptEngineering/comments/1nt7x7v/after_1000_hours_of_prompt_engineering_i_found/

[^115]: https://www.greptile.com/content-library/14-best-developer-productivity-tools-2025

[^116]: https://www.reddit.com/r/ClaudeAI/comments/1lcfawk/claude_code_cursor_setup_best_practices_pro_tips/

[^117]: https://platform.openai.com/docs/guides/prompt-engineering

[^118]: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

[^119]: https://www.reddit.com/r/ClaudeAI/comments/1k5slll/anthropics_guide_to_claude_code_best_practices/

[^120]: https://www.promptingguide.ai/applications/coding

[^121]: https://www.reddit.com/r/programming/comments/1l8n9i8/ai_coding_assistants_arent_really_making_devs/

[^122]: https://www.youtube.com/watch?v=usDE1z2z_MA

[^123]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering

[^124]: https://www.semanticscholar.org/paper/f55e315f26a17b849d8474b59d91663dc7911cca

[^125]: https://arxiv.org/abs/2506.06971

[^126]: https://arxiv.org/abs/2302.00923

[^127]: https://arxiv.org/abs/2310.08992

[^128]: https://arxiv.org/abs/2504.13534

[^129]: https://arxiv.org/abs/2412.03944

[^130]: https://arxiv.org/abs/2407.17636

[^131]: https://arxiv.org/abs/2509.25243

[^132]: http://arxiv.org/pdf/2310.10698v1.pdf

[^133]: https://arxiv.org/html/2403.14312

[^134]: https://arxiv.org/pdf/2312.05562.pdf

[^135]: http://arxiv.org/pdf/2501.13978.pdf

[^136]: https://aclanthology.org/2023.emnlp-main.263.pdf

[^137]: https://arxiv.org/pdf/2305.08360.pdf

[^138]: http://arxiv.org/pdf/2412.20545.pdf

[^139]: https://learnprompting.org/docs/advanced/decomposition/chain-of-code

[^140]: https://learnprompting.org/blog/ai-few-shot-prompts

[^141]: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

[^142]: https://www.codecademy.com/article/chain-of-thought-cot-prompting

[^143]: https://chain-of-code.github.io

