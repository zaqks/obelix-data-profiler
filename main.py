from ydata_profiling import ProfileReport
from ydata_profiling.config import Settings


import pandas as pd

DATASET = "./data/Steep_cleaned_cleaned.csv"
df = pd.read_csv(DATASET)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.sample(frac=0.01, random_state=42)


###
settings = Settings()
settings.html.inline = False  # separate assets instead of inline
settings.html.style.logo = "assets/logo.png"
settings.html.style.primary_colors = ["#aaaaaa"]


report = ProfileReport(df,
                       title="Teknor Data Quality Report",
                       progress_bar=True,
                       #
                       explorative=True,
                       minimal=False,
                       sensitive=True,
                       #
                       sortby="Timestamp",
                       sort="ascending",
                       tsmode=True,

                       config=settings)


report.to_file("output/report.html")