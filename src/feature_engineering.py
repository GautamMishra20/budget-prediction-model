import pandas as pd
from src.config import GROUP_COLUMNS

def create_features(df):
    df = df.sort_values(GROUP_COLUMNS + ["date"])

    # Previous month budget
    df["lag_1"] = df.groupby(GROUP_COLUMNS)["allocated_budget"].shift(1)

    # Growth rate (month-over-month)
    df["growth_rate"] = (
        (df["allocated_budget"] - df["lag_1"]) / df["lag_1"]
    )

    # Lag growth features
    df["growth_lag_1"] = df.groupby(GROUP_COLUMNS)["growth_rate"].shift(1)
    df["growth_lag_3"] = df.groupby(GROUP_COLUMNS)["growth_rate"].shift(3)

    # Rolling average of growth
    df["rolling_growth_3"] = (
        df.groupby(GROUP_COLUMNS)["growth_rate"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    df = df.dropna()
    return df