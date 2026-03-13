import ollama
import subprocess
import argparse
from sc.prompt import CommitNamePrompt, highlightKeyInformationPrompt

MODEL = "codellama:7b-instruct"  # Must be pulled, ollama


def highlightKeyInformation(diff: str) -> str:
    return ollama.chat(model=MODEL, messages=[
        {'role': 'user', 'content': f"""{highlightKeyInformationPrompt}{diff}"""}
    ])


def generateCommitName(
    branch_name: str = "nothing",
    diff: str = "nothing",
    short_clue: str = "nothing",
) -> str:

    _prompt = f"""{CommitNamePrompt} Analyze the following diff and generate a commit
                  message that accurately describes the change.
                  branch name: {branch_name}, clue :{short_clue}
                  Key changes:
                  {highlightKeyInformation(diff)}
                  Output ONLY the commit message line. Do not include any
                  explanations, extra text, markdown, or backticks.
               """

    return ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": _prompt}],
        options={"num_predict": 100, "temperature": 0.3},
    )


def main():
    git_diff = subprocess.run(
        ["git", "--no-pager", "diff", "HEAD"], capture_output=True, text=True, check=True
    )

    branch_name = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True,
        check=True
    )

    stripped_diff = git_diff.stdout.strip()
    stripped_name = branch_name.stdout.strip()

    commitName = generateCommitName(branch_name=stripped_name,
                                    diff=stripped_diff)
    print(commitName["message"]["content"])


def run():
    parser = argparse.ArgumentParser(prog="sc")
    args = parser.parse_args()

    subparsers = parser.add_subparsers(dest="command", required=True,
                                       help="Available commands")
    run_parser = subparsers.add_parser("run", help="Generate commit message")

    args = parser.parse_args()

    if args.command == "run":
        main()


if __name__ == "__main__":
    run()