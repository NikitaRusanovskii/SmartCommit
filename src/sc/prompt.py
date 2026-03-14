combinedPrompt = """
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