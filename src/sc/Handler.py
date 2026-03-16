import ollama
from .Prompt import (
    commitNamePrompt,
    createReportsPrompt,
    gitAIHelperPrompt
)
from .ModelConfig import (
    MODEL,
    genNameNumPredict,
    genNameTemp,
    genRepNumPredict,
    genRepTemp,
    genGitHelpNumPredict,
    genGitHelpTemp
)


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
            options={"num_predict": genNameNumPredict,
                     "temperature": genNameTemp})["message"]["content"]
        return response

    def generateReport(self, tooltip: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": createReportsPrompt.format(
                branch_name=self.branch_name,
                difference=self.diff,
                tooltip=tooltip
            )}],
            options={"num_predict": genRepNumPredict,
                     "temperature": genRepTemp})["message"]["content"]
        return response

    def generateGitHelpAIResponse(self, tooltip: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": gitAIHelperPrompt.format(
                branch_name=self.branch_name,
                tooltip=tooltip
            )}],
            options={"num_predict": genGitHelpNumPredict,
                     "temperature": genGitHelpTemp})["message"]["content"]
        return response
