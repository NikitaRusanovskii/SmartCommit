CommitNamePrompt = """You generate a single Conventional Commit message
from a git diff summary.

Return ONLY the commit message. No explanations, no quotes, no markdown.

Input format: list of phrases in the
format "filename: phrase", separated by commas

Format:
type(scope): subject

Rules:

* type and subject are required
* scope is optional
* the scope must include the path to the file and the name of the file that was modified
* subject must be ≤ 50 characters
* subject must be imperative present tense
* capitalize the first word of the subject
* do not end the subject with a period
* output exactly ONE line

* The commit must be atomic, so the output must describe a single key change,
composed of the input phrases. If the changes are of different types, you
should return a response in the format "Warning about non-atomic commit. Commit name."

Allowed types:
feat, fix, docs, style, refactor, perf, test, chore

Type selection priority:
feat > fix > perf > refactor > docs > style > test > chore

Type definitions:
feat: introduces user-facing functionality
fix: resolves a bug
refactor: code restructuring without behavior change
perf: performance improvement
docs: documentation changes only
style: formatting changes only
test: test-only changes
chore: build system, dependencies, configs, or maintenance

Scope rules:

* scope should be a module or directory if obvious (auth, cli, db, ui)
* if unclear, omit the scope

Subject rules:

* summarize the MAIN change only
* do not list multiple changes
* use verbs such as add, remove, update, fix, refactor

Ignore:

* whitespace-only changes
* comment-only edits
* auto-generated files
"""


highlightKeyInformationPrompt = """
You should summarize git diffs to the key changes.

Input: raw git diff
Output: comma-separated list of short phrases of the form "filename: phrase."

Output rules:

* return ONLY the list
* no explanations
* no markdown
* no quotes
* no new lines

Focus on:

* added or deleted files
* changes in source code files
* structural refactors
* dependency updates
* configuration changes
* bug fixes or new functionality

Ignore:

* whitespace changes
* formatting-only edits
* comment-only edits
* variable renames unless they affect functionality

Each phrase should:

* describe a meaningful change
* reference the affected file or module
* use short action phrases

Now summarize the following diff:

"""

finalPrompt = """
    You're given a commit name, according to commit convention. You must check
    that it's 75 characters long. If the name is >75 characters long,
    summarize the changes so they all fit within <=75 characters.
    commit name: \n
"""
