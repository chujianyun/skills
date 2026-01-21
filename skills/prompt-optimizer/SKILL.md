---
name: prompt-optimizer
description: Prompt engineering expert that helps users craft optimized prompts using 57 proven frameworks. Use when users want to optimize prompts, improve AI instructions, create better prompts for specific tasks, or need help selecting the best prompt framework for their use case.
license: LICENSE-CC-BY-NC-SA 4.0 in LICENSE.txt
anthor: 悟鸣
---

# Prompt Optimizer

A comprehensive prompt engineering skill that helps users craft high-quality, effective prompts using proven frameworks.

## Workflow

Copy this checklist and track your progress:
- [ ] Step 1: Analyze User Input
- [ ] Step 2: Match Scenario and Select Framework
- [ ] Step 3: Load Framework Details
- [ ] Step 4: Clarify Ambiguities
- [ ] Step 5: Generate Optimized Prompt
- [ ] Step 6: Present and Iterate

When a user requests create or prompt optimization, follow these steps:

### Step 1: Analyze User Input

Receive the user's request, which may be:
- A raw prompt that needs optimization
- A task description or requirement
- A vague idea that needs to be turned into a prompt

### Step 2: Match Scenario and Select Framework

Read the [references/Frameworks_Summary.md](references/Frameworks_Summary.md) file to:
1. Identify the user's scenario from the application scenarios listed
2. Match the most suitable framework(s) based on:
   - Application scenario alignment
   - Task complexity (simple/medium/complex)
   - Domain category (marketing, decision analysis, education, etc.)

**Framework Selection Guide by Complexity:**

| Complexity | Recommended Frameworks |
|------------|----------------------|
| Simple (≤3 elements) | APE, ERA, TAG, RTF, BAB, PEE, ELI5 |
| Medium (4-5 elements) | RACE, CIDI, SPEAR, SPAR, FOCUS, SMART, GOPA, ORID, CARE, ROSE, PAUSE, TRACE, GRADE, TRACI, RODES |
| Complex (6+ elements) | RACEF, CRISPE, SCAMPER, Six Thinking Hats, ROSES, PROMPT, RISEN, RASCEF, Atomic Prompting |

**Framework Selection Guide by Domain:**

| Domain | Recommended Frameworks |
|--------|----------------------|
| Marketing Content | BAB, SPEAR, Challenge-Solution-Benefit, BLOG, PROMPT, RHODES |
| Decision Analysis | RICE, Pros and Cons, Six Thinking Hats, Tree of Thought, PAUSE, What If |
| Education & Training | Bloom's Taxonomy, ELI5, Socratic Method, PEE, Hamburger Model |
| Product Development | SCAMPER, HMW, CIDI, RELIC, 3Cs Model |
| AI Dialogue/Assistant | COAST, ROSES, TRACE, RACE, RASCEF |
| Writing & Creation | BLOG, 4S Method, Hamburger Model, Few-shot, RHODES, Chain of Destiny |
| Image Generation | Atomic Prompting |
| Quick Simple Tasks | Zero-shot, ERA, TAG, APE, RTF |
| Complex Reasoning | Chain of Thought, Tree of Thought |

### Step 3: Load Framework Details

Once the best framework is identified, read the corresponding framework file from the `references/frameworks/` directory:
- File naming pattern: `XX_FrameworkName_Framework.md`
- Example: For RACEF framework, read `references/frameworks/01_RACEF_Framework.md`

The framework file contains:
- Framework overview and components
- Detailed explanation of each element
- Pros and cons
- Best practice examples

### Step 4: Clarify Ambiguities

Before generating the final prompt, verify with the user:

1. **Goal Clarity**: Is the intended outcome clear?
2. **Target Audience**: Who will receive the AI's response?
3. **Context Completeness**: Is sufficient background information provided?
4. **Format Requirements**: Are there specific output format needs?
5. **Constraints**: Are there any limitations or restrictions?

Ask clarifying questions if any information is:
- Missing
- Ambiguous
- Incomplete
- Contradictory

Example clarifying questions:
- "What specific outcome are you hoping to achieve?"
- "Who is the target audience for this content?"
- "Are there any format or length requirements?"
- "What context should the AI consider?"

### Step 5: Generate Optimized Prompt

Apply the selected framework to create the final prompt:

1. Structure the prompt according to framework components
2. Incorporate all clarified information
3. Ensure clarity and specificity
4. Include relevant examples if the framework requires
5. Add any necessary constraints or guidelines

### Step 6: Present and Iterate

Present the optimized prompt to the user with:
1. The selected framework name and why it was chosen
2. The complete optimized prompt
3. Explanation of how each framework element was applied
4. Suggestions for potential variations or improvements

If the user requests changes, iterate on the prompt while maintaining framework structure.

## Framework Reference Files

All framework details are stored in the `references/frameworks/` directory. Each file contains:
- Application scenarios
- Framework components with explanations
- Advantages and disadvantages
- Multiple practical examples

## Quick Framework Selection

For users unsure which framework to use:

| User Says | Recommended Framework |
|-----------|----------------------|
| "I need a simple prompt" | APE, ERA, TAG |
| "I want to persuade/sell" | BAB, SPEAR, Challenge-Solution-Benefit |
| "I need to analyze/decide" | RICE, Pros and Cons, Chain of Thought |
| "I want to teach/explain" | ELI5, Bloom's Taxonomy, Socratic Method |
| "I need creative ideas" | SCAMPER, HMW, SPARK, Imagine |
| "I want structured writing" | BLOG, 4S Method, Hamburger Model |
| "I need step-by-step reasoning" | Chain of Thought, Tree of Thought |
| "I'm generating images" | Atomic Prompting |
| "I need a detailed plan" | RISEN, RASCEF, CRISPE |
