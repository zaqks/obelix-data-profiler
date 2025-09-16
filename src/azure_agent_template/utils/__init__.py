import os

from .azureClient import AzureLLMClient
from .promptManager import PromptManager


pm = PromptManager(prompt_dir=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../prompts"))
client = AzureLLMClient()
