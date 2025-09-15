import sys
sys.path.insert(0, "./src/libs/")


# DON"T FORMAT THIS
from ydata_profiling import ProfileReport
from ydata_profiling.config import Settings
from src.agents import TimeSeriesAgent, MetaDataAgent, ScoringAgent
