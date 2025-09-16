import json
from src.azure_agent_template import AzureAgentTemplate


class TimeSeriesAgent(AzureAgentTemplate):
    def __init__(self):
        super().__init__("timeseries")

    def is_timeserie(self, columns: list[str]) -> dict:
        """
        returns (
            ts_mode: bool,
            timestamp_col: str
        )
        """
        
        result = self.think({"COLUMNS": columns})
        print(result)
        result = json.loads(result)

        return result.values()