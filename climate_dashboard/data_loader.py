"""Read and clean the climate datasets."""

from pathlib import Path

import pandas as pd
import streamlit as st

from climate_dashboard.data_processing import prepare_numeric_data, prepare_temperature_data


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


@st.cache_data
def load_data():
    temp_raw = pd.read_csv(DATA_DIR / "data_test.csv")
    temp_agg, temp_raw = prepare_temperature_data(temp_raw)

    co2 = prepare_numeric_data(
        pd.read_csv(DATA_DIR / "co2_sample_dataset.csv"), ("year", "co2")
    )
    forest = prepare_numeric_data(
        pd.read_csv(DATA_DIR / "forest_large.csv"),
        ("year", "forest_loss"),
        drop_all_missing=True,
    )
    sea = prepare_numeric_data(
        pd.read_csv(DATA_DIR / "sea_level_large.csv"), ("year", "sea_level")
    )

    return temp_agg, temp_raw, co2, forest, sea
