import json

from .utils import pm, client


class AzureAgentTemplate:
    def __init__(self, prompt_name: str):
        self.prompt_name = prompt_name

    def think(self, tokens: dict) -> str:
        prompt = pm.fill_prompt(self.prompt_name, tokens)
        result = client.generate(prompt)

        return result
