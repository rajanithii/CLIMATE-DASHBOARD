"""Shared page navigation controls."""

import streamlit as st

def go_to(p: str):
    st.session_state.page = p
    st.rerun()

def nav_bar():
    c0, c1, c2, c3, c4, c5 = st.columns([2.6, 1, 1, 1, 1, 1])
    with c0:
        st.markdown(
            '<div style="padding:10px 0;font-size:1.08rem;font-weight:800;'
            'background:linear-gradient(90deg,#4ade80,#a3e635,#2dd4bf,#d1fae5);'
            'background-size:220% auto;-webkit-background-clip:text;'
            '-webkit-text-fill-color:transparent;animation:shimmer 5s linear infinite;">'
            '🌿 ClimatePulse</div>',
            unsafe_allow_html=True,
        )
    for col, (label, page) in zip(
        [c1, c2, c3, c4, c5],
        [("🏠 Home","home"),("🏭 CO₂","co2"),("🌡️ Temp","temp"),("🌊 Sea","sea"),("🌳 Forest","forest")],
    ):
        with col:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                go_to(page)
