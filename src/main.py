import ollama
import subprocess
from prompt import prompt

MODEL = "phi3:3.8b-mini-128k-instruct-q4_K_M"  # Must be pulled, ollama


def generateCommitName(
    branch_name: str = "nothing",
    diff: str = "nothing",
    short_clue: str = "nothing",
) -> str:

    _prompt = f"""{prompt} Analyze the following diff and generate a commit
                  message that accurately describes the change.
                  branch name: {branch_name}, clue :{short_clue}
                  Diff:
                  {diff}
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
        ["git", "diff"], capture_output=True, text=True, check=True
    )
    branch_name = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True, check=True
    )

    commitName = generateCommitName(branch_name=branch_name, diff=git_diff)
    print(commitName["message"]["content"])


if __name__ == "__main__":
    main()
