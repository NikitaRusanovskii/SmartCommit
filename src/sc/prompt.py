commitNamePrompt = """
You generate a single Conventional Commit message from a git diff.

Return ONLY the commit message.
No explanations, no quotes, no markdown, no backticks, no extra text.

Context:
branch name: {branch_name}
hint: {tooltip}

Input:
raw git diff

{difference}

Processing instructions:

1. Analyze the git diff and extract the key changes.

Ignore:

* whitespace-only changes
* formatting-only edits
* comment-only edits
* auto-generated files
* variable renames unless they affect functionality

Focus on:

* added or deleted files
* source code changes
* structural refactors
* dependency updates
* configuration changes
* bug fixes
* new functionality

Internally summarize the diff as phrases in the format:
filename: phrase

Each phrase should:

* describe a meaningful change
* reference the affected file or module
* use a short action phrase

2. From those changes generate a single Conventional Commit message.

Format:
type(scope): subject

Rules:

* output exactly ONE line
* type and subject are required
* scope is optional
* scope must include the path and file name if obvious
* subject must be ≤ 50 characters
* subject must be imperative present tense
* capitalize the first word
* do not end the subject with a period

Allowed types:
feat, fix, docs, style, refactor, perf, test, chore

Type priority:
feat > fix > perf > refactor > docs > style > test > chore

Type definitions:
feat: introduces user-facing functionality
fix: resolves a bug
refactor: code restructuring without behavior change
perf: performance improvement
docs: documentation changes only
style: formatting changes only
test: test-only changes
chore: build system, dependencies, configs, maintenance

Scope rules:

* use a module or directory if obvious (auth, cli, db, ui)
* if unclear, omit the scope

Subject rules:

* summarize ONLY the main change
* do not list multiple changes
* prefer verbs such as add, remove, update, fix, refactor

Atomicity rule:
The commit must represent a single key change composed from the input changes.
If multiple unrelated change types are present, output:

Warning about non-atomic commit. Commit name.

3. Final validation.

Ensure the final commit message length is ≤ 75 characters.

If it exceeds 75 characters:

* compress the wording
* keep the meaning
* keep the Conventional Commit format
* ensure the final message is ≤ 75 characters.

Final output:
Return ONLY the final commit message line.
"""


createReportsPrompt = """

You are an expert technical lead. Your task is to explain the changes in a git diff to a human colleague (e.g., in Slack or during a Stand-up).

Context:
Branch: {branch_name}
User Hint: {tooltip}

Input:
{difference}

Instructions:
1. Summarize the "Big Picture": What is the main goal of these changes? (1-2 sentences).
2. Key Changes: Provide a bulleted list of the most important technical shifts.
3. Impact: Mention if these changes affect other modules, APIs, or user experience.
4. "Why": Based on the diff, infer the reasoning (e.g., "Refactored to improve readability" or "Fixed a race condition in the auth flow").

Constraints:
- Use professional yet conversational tone.
- Avoid technical jargon where a simple word works.
- DO NOT just list files; explain the logic behind the edits.
- Use Markdown for formatting (bolding, lists).
- If the diff is messy, prioritize the most "impactful" code blocks.

Output Format:
### Summary
[Brief overview]

### 🛠 What's changed
- **[Module/File]**: [Action-oriented explanation]
- ...

### Notable details
- [Mention any specific logic, performance wins, or potential side effects]

Final Output:
Return only the Markdown-formatted explanation.
"""

gitAIHelperPrompt = """
You are a Git expert. Your task is to output the exact sequence of Git
commands required to complete the user's request.


IMPORTANT WARNING
Git commands can modify history or permanently delete changes.
The user must review commands before running them.

CONTEXT
Current branch: {branch_name}
User request: {tooltip}

RULES
- Return ONLY the steps required to complete the task.
- Keep explanations extremely short (max 1 line).
- Commands must be ready to copy-paste into a terminal.
- Limit line length to ~70 characters for console readability.
- If a command is longer than 70 characters, split it using '\\'.
- Always place commands inside code blocks.
- Separate steps clearly.
- If the command can rewrite history or lose data
  (reset --hard, push --force, rebase, clean, etc.),
  add a WARNING line before the step.

OUTPUT FORMAT

Step 1 — <short description>
command: [command]
"""