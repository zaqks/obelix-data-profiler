import sys
sys.path.insert(0, "./src/libs/")

# DON"T FORMAT THIS
import json
import datetime
import pandas as pd
from .agents import TimeSeriesAgent, MetaDataAgent, ScoringAgent
from ydata_profiling.config import Settings
from ydata_profiling import ProfileReport



class ObelixProfiler:
    def __init__(self, df: pd.DataFrame, output_folder: str):
        self.df = df
        self.output_folder = output_folder
        self.ts_agent = TimeSeriesAgent()
        self.meta_agent = MetaDataAgent()
        self.scr_agent = ScoringAgent()
        self.report_name = None
        self.score = None
        self.suggestions = None

    def run(self):
        cols = self.df.columns.to_list()

        # Check if timeseries and convert if needed
        ts_mode, ts_col = self.ts_agent.is_timeserie(cols)
        if ts_mode:
            self.df[ts_col] = pd.to_datetime(self.df[ts_col])
            sort_by_col = ts_col
            sort_order = "ascending"
        else:
            sort_by_col = None
            sort_order = None

        # Get metadata descriptions
        meta_cols = self.meta_agent.get_metadata(cols)

        # Setup report settings
        settings = Settings()
        settings.html.inline = False  # separate assets
        settings.html.style.logo = "assets/logo.png"

        # Generate report
        report = ProfileReport(
            self.df,
            title="Obelix Data Quality Report",
            progress_bar=True,
            explorative=True,
            minimal=False,
            sensitive=True,
            sortby=sort_by_col,
            sort=sort_order,
            tsmode=ts_mode,
            variables={"descriptions": meta_cols},
            config=settings
        )

        # Prepare timestamped output file path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_name = f"report_{timestamp}"
        # self.report_name = f"{self.output_folder}/report.html"

        # Save report
        report.to_file(f"{self.output_folder}/{self.report_name}.html")

        # Scoring
        report_json = report.to_json()
        report_json = json.loads(report_json)
        self.score, self.suggestions = self.scr_agent.get_score(
            report_json['alerts'])

        return self.report_name, self.score, self.suggestions
