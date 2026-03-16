import subprocess
import argparse
from .Handler import DiffHandler


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
