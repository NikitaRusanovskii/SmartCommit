import ollama
import subprocess
import argparse
from sc.prompt import (
    CommitNamePrompt, highlightKeyInformationPrompt,
    finalPrompt
)
MODEL = "qwen2.5-coder:7b"  # model name


def highlightKeyInformation(diff: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "user", "content": f"""{highlightKeyInformationPrompt}{diff}"""}
        ],
    )["message"]["content"]

    # print("Суммаризация разницы коммитов: \n", response)
    return response


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

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": _prompt}],
        options={"num_predict": 100, "temperature": 0.1},
    )["message"]["content"]

    # print('Формирование коммита: \n', response)

    return response


def finalize(commitName: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": finalPrompt + commitName}],
        options={"num_predict": 100, "temperature": 0.1},
    )["message"]["content"]

    # print('Финальная версия: \n', response)

    return response


def main():
    git_diff = subprocess.run(
        ["git", "--no-pager", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    branch_name = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True, check=True
    )

    stripped_diff = git_diff.stdout.strip()
    stripped_name = branch_name.stdout.strip()

    commitName = finalize(generateCommitName(branch_name=stripped_name,
                                             diff=stripped_diff))
    print(commitName)


def run():
    parser = argparse.ArgumentParser(prog="smc")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )
    run_parser = subparsers.add_parser("run", help="Generate commit message")

    args = parser.parse_args()

    if args.command == "run":
        main()


if __name__ == "__main__":
    run()
