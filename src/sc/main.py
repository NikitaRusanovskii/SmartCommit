import ollama
import subprocess
import argparse
from sc.prompt import combinedPrompt
MODEL = "qwen2.5-coder:7b"  # model name


class PromptGenerator:
    def __init__(self,
                 branch_name: str,
                 difference: str,
                 tooltip: str):
        self.branch_name = branch_name
        self.diff = difference
        self.tooltip = tooltip

    def generatePrompt(self):
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": combinedPrompt.format(
                branch_name=self.branch_name,
                difference=self.diff,
                tooltip=self.tooltip
            )}],
            options={"num_predict": 100,
                     "temperature": 0.1})["message"]["content"]
        return response


def main(tooltip: str = 'nothing'):
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

    promptGen = PromptGenerator(
        stripped_name,
        stripped_diff,
        tooltip
    )

    print(promptGen.generatePrompt())


def run():
    parser = argparse.ArgumentParser(prog="smc")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )
    subparsers.add_parser("run", help="Generate commit message")
    parser.add_argument('-t', '--tooltip')

    args = parser.parse_args()

    if args.command == "run":
        main(args.tooltip)


if __name__ == "__main__":
    run()
