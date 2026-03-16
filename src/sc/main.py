import subprocess
import argparse
from .Handler import DiffHandler, QuestionHandler


def getDiff() -> str:
    return subprocess.run(
        ["git", "--no-pager", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def getBranchName() -> str:
    return subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True,
        text=True, check=True
    ).stdout.strip()


def generateName(tooltip: str = None) -> str:
    dh = DiffHandler(getBranchName(), getDiff())
    return dh.generateName(tooltip)


def generateReport(tooltip: str = None) -> str:
    dh = DiffHandler(getBranchName(), getDiff())
    return dh.generateReport(tooltip)


def generateAIHelpGit(tooltip: str = None) -> str:
    qh = QuestionHandler()
    return qh.generateGitHelpAIResponse(tooltip)


def handle(tooltip: str = None, command: str = None):
    funcs = {
        'name': generateName,
        'repo': generateReport,
        'ai': generateAIHelpGit
    }

    result = funcs[command](tooltip)
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
    handle(args.tooltip, args.command)


if __name__ == "__main__":
    main()
