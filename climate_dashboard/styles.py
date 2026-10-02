"""Load and apply the dashboard stylesheet."""

from pathlib import Path

import streamlit as st


_STYLESHEET = Path(__file__).resolve().parent.parent / "assets" / "styles.css"


def inject_css() -> None:
    css = _STYLESHEET.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
