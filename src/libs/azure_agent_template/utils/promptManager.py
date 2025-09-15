import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List


class MissingTokensError(Exception):
    pass


class UnknownTokensError(Exception):
    pass


@dataclass(frozen=True)
class Prompt:
    text: str
    tokens: List[str]
    replacements: Dict[str, str] = field(default_factory=dict)

    def with_replacements(self, replacements: Dict) -> 'Prompt':
        # Convert keys and values to strings
        replacements = {str(k): str(v) for k, v in replacements.items()}

        # Check for unknown tokens in replacements keys
        unknown_tokens = set(replacements) - set(self.tokens)
        if unknown_tokens:
            raise UnknownTokensError(
                f"Unknown tokens in replacements: {unknown_tokens}")

        combined = {token: "" for token in self.tokens}
        combined.update(replacements)

        # Check for missing replacements (empty or None)
        missing_tokens = [t for t, v in combined.items() if not v]
        if missing_tokens:
            raise MissingTokensError(
                f"Missing replacements for tokens: {missing_tokens}")

        return Prompt(self.text, self.tokens, combined)

    def get_filled_prompt(self) -> str:
        result = self.text
        for token, replacement in self.replacements.items():
            result = result.replace(f"%% {token} %%", replacement)
        return result


class PromptManager:
    def __init__(self, prompt_dir: str):
        self.prompt_dir = Path(prompt_dir)

    def load_prompt(self, name: str) -> Prompt:
        prompt_path = self.prompt_dir / f"{name}.txt"
        text = prompt_path.read_text()
        tokens = re.findall(r"%%\s*(.*?)\s*%%", text)
        return Prompt(text, tokens)

    def fill_prompt(self, name: str, replacements: Dict[str, str]) -> str:
        prompt = self.load_prompt(name).with_replacements(replacements)
        return prompt.get_filled_prompt()
