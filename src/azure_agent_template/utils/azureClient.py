import os
import logging
import openai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AzureLLMClient:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_MODEL")

        if not all([self.api_key, self.api_base, self.api_version, self.deployment_name]):
            logger.error(
                "One or more Azure OpenAI environment variables are missing")
            raise ValueError("Missing Azure OpenAI environment variables")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        openai.api_type = "azure"
        openai.api_version = self.api_version

    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response['choices'][0]['message']['content'].strip()
        except KeyError as ke:
            logger.error(f"KeyError accessing response content: {
                         ke}, full response: {response}")
            return ""
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            return ""
