import ollama
import subprocess
import argparse
from sc.prompt import (
    commitNamePrompt,
    createReportsPrompt,
    gitAIHelperPrompt
)
MODEL = "qwen2.5-coder:7b"  # model name


class DiffHandler:
    def __init__(self,
                 branch_name: str,
                 difference: str,
                 ):
        self.branch_name = branch_name
        self.diff = difference

    def generateName(self, tooltip: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": commitNamePrompt.format(
                branch_name=self.branch_name,
                difference=self.diff,
                tooltip=tooltip
            )}],
            options={"num_predict": 100,
                     "temperature": 0.1})["message"]["content"]
        return response

    def generateReport(self, tooltip: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": createReportsPrompt.format(
                branch_name=self.branch_name,
                difference=self.diff,
                tooltip=tooltip
            )}],
            options={"num_predict": 200,
                     "temperature": 0.1})["message"]["content"]
        return response

    def generateGitHelpAIResponse(self, tooltip: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": gitAIHelperPrompt.format(
                branch_name=self.branch_name,
                tooltip=tooltip
            )}],
            options={"num_predict": 200,
                     "temperature": 0.1})["message"]["content"]
        return response


def generateName(df: DiffHandler, tooltip: str = None) -> str:
    return df.generateName(tooltip)


def generateReport(df: DiffHandler, tooltip: str = None) -> str:
    return df.generateReport(tooltip)


def generateAIHelpGit(df: DiffHandler, tooltip: str = None) -> str:
    return df.generateGitHelpAIResponse(tooltip)


def run(tooltip: str = None, command: str = None):
    git_diff = subprocess.run(
        ["git", "--no-pager", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    branch_name = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True,
        text=True, check=True
    )

    stripped_diff = git_diff.stdout.strip()
    stripped_name = branch_name.stdout.strip()

    diffHandler = DiffHandler(
        stripped_name,
        stripped_diff,
    )

    funcs = {
        'name': generateName,
        'repo': generateReport,
        'ai': generateAIHelpGit
    }

    result = funcs[command](diffHandler, tooltip)
    print(result)


def main():
    parser = argparse.ArgumentParser(prog="smc")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )
    subparsers.add_parser("name", help="Generate commit message")
    subparsers.add_parser("repo", help="Generate work-report message")
    subparsers.add_parser("ai", help="Generate ai-help message for git")
    parser.add_argument('-t', '--tooltip')

    args = parser.parse_args()
    run(args.tooltip, args.command)


if __name__ == "__main__":
    main()
