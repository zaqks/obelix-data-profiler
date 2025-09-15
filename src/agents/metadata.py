import json
from src.libs.azure_agent_template import AzureAgentTemplate


class MetaDataAgent(AzureAgentTemplate):
    def __init__(self):
        super().__init__("metadata")

    def get_metadata(self, columns: list[str]) -> dict:
        """
        returns (
            ts_mode: bool,
            timestamp_col: str
        )
        """

        result = self.think({"COLUMNS": columns})
        result = json.loads(result)

        print(result)

        return result
