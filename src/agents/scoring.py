import json
from src.libs.azure_agent_template import AzureAgentTemplate


class ScoringAgent(AzureAgentTemplate):
    def __init__(self):
        super().__init__("scoring")

    def get_score(self, alerts: list[str]) -> dict:
        """
        returns {
            score: int,
            suggs: list[str]
        }
        """

        result = self.think({"ALERTS": alerts})
        result = json.loads(result)

        return result
