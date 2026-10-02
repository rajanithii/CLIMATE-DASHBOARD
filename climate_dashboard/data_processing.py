"""Data cleaning and aggregation for climate datasets."""

import pandas as pd


def prepare_temperature_data(
    temp_raw: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    temp_raw = temp_raw.copy()
    temp_raw["Year"] = pd.to_numeric(temp_raw["Year"], errors="coerce")
    temp_raw["Adjusted Temperature"] = pd.to_numeric(
        temp_raw["Adjusted Temperature"], errors="coerce"
    )
    temp_raw = temp_raw.dropna(subset=["Year", "Adjusted Temperature"])
    temp_agg = (
        temp_raw.groupby("Year")["Adjusted Temperature"]
        .mean()
        .reset_index()
        .rename(columns={"Adjusted Temperature": "temp"})
    )
    temp_agg = temp_agg[temp_agg["Year"] >= 1900].reset_index(drop=True)
    return temp_agg, temp_raw


def prepare_numeric_data(
    frame: pd.DataFrame,
    columns: tuple[str, ...],
    *,
    drop_all_missing: bool = False,
) -> pd.DataFrame:
    frame = frame.copy()
    for column in columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if drop_all_missing:
        return frame.dropna().reset_index(drop=True)
    return frame.dropna(subset=list(columns)).reset_index(drop=True)