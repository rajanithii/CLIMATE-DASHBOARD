"""ClimatePulse Streamlit application entry point."""

import streamlit as st

from climate_dashboard.components.navigation import nav_bar
from climate_dashboard.data_loader import load_data
from climate_dashboard.styles import inject_css
from climate_dashboard.views import (
    page_co2,
    page_forest,
    page_home,
    page_sea,
    page_temp,
)

st.set_page_config(
    page_title="ClimatePulse",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = "home"

inject_css()
temp_agg, temp_raw, co2, forest, sea = load_data()
nav_bar()

page_renderers = {
    "home": lambda: page_home(temp_agg, co2, forest, sea),
    "co2": lambda: page_co2(co2),
    "temp": lambda: page_temp(temp_agg, temp_raw),
    "sea": lambda: page_sea(sea),
    "forest": lambda: page_forest(forest),
}
page_renderers.get(st.session_state.page, page_renderers["home"])()
