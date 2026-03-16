# SmartCommit

A 'small' CLI tool that generates commit messages and simple work reports based on your current git diff using a local LLM through Ollama.

The idea is simple: instead of manually writing commit messages for routine changes, you let the model read the diff and suggest a reasonable message.

No external APIs. Everything runs locally.

---

## What it does

SmartCommit reads:

* current **git branch**
* current **git diff (against HEAD)**

Then sends that information to a local model via **Ollama** and generates:

* a commit message
* a short work report
* a git-related AI helper response

All generation is local.

---

## Requirements

You need:

* Python **3.9+**
* **Git**
* **Ollama**

Install Ollama from the official site and make sure it runs in the background.

---

## Installation

Clone the repository:

```
git clone <repo-url>
cd smartcommit
```

Install dependencies:

```
pip install -r requirements.txt
```

Install the CLI tool locally:

```
pip install -e .
```

---

## Model setup

Pull the model you want to use with Ollama.

Example:

```
ollama pull qwen2.5-coder:7b
```

Then open `main.py` and set the model name:

```
MODEL = "qwen2.5-coder:7b"
```

You can use any model supported by Ollama, but coder-oriented models usually work better for diffs.

---

## Usage

SmartCommit works inside a git repository.

Basic usage:

```
smc name
```

This reads your current diff and generates a commit message.

---

### Generate commit message

```
smc name
```

Optional hint:

```
smc -t "refactor auth logic" name
```

The tooltip is just extra context for the model.

---

### Generate work report

```
smc repo
```

Useful if you need a quick description of what changed during the session.

---

### Git helper

```
smc -t "how should I split this commit?" ai
```

This mode ignores the diff and simply lets the model answer git-related questions.

---

## How it works

The tool runs two git commands:

```
git diff HEAD
git branch --show-current
```

The output is passed into prompt templates located in:

```
sc/prompt.py
```

Those prompts are then sent to the Ollama model through the Python API.

---

## Notes

* The tool only analyzes **unstaged changes vs HEAD**.
* Large diffs may produce worse results depending on the model.
* Different models behave very differently — experiment.

---

## Example

```
smc name
```

Output:

```
docs(README.md): update documentation for SmartCommit tool
```

---

## Why this exists

Mostly convenience.

Writing commit messages repeatedly for mechanical changes is boring, and local LLMs are good enough at summarizing diffs to automate most of it.
