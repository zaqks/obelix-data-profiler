import pandas as pd

from src.libs.ydata import ProfileReport
from src.libs.ydata.config import Settings

from src.agents import ScoringAgent, TimeSeriesAgent, MetaDataAgent


DATASET = "./data/Steep_cleaned_cleaned.csv"
df = pd.read_csv(DATASET)


# Check if we're dealing with timeseries
ts_agent = TimeSeriesAgent()
ts_mode, ts_col = ts_agent.is_timeserie(df.columns.to_list())

if ts_mode:
    df[ts_col] = pd.to_datetime(df[ts_col])


# Sampling
df = df.sample(frac=0.01, random_state=42)


###
settings = Settings()
settings.html.inline = False  # separate assets instead of inline
settings.html.style.logo = "assets/logo.png"


report = ProfileReport(df,
                       title="Obelix Data Quality Report",
                       progress_bar=True,
                       #
                       explorative=True,
                       minimal=False,
                       sensitive=True,
                       #
                       sortby=ts_col,
                       sort="ascending" if ts_mode else None,
                       tsmode=ts_mode,

                       config=settings)


report.to_file("output/report.html")

# scoring

scr_agent = ScoringAgent()
score, suggs = scr_agent.get_score(report_json['alerts'])

print(score)
print(suggs)
