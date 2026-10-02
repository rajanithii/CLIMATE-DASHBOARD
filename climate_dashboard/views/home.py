"""Home dashboard view."""

import streamlit as st
from climate_dashboard.components.navigation import go_to


def page_home(temp_agg, co2, forest, sea):
    latest_temp  = temp_agg["temp"].iloc[-1]
    latest_sea   = sea.sort_values("year")["sea_level"].iloc[-1]
    co2_peak     = co2["co2"].max()
    forest_total = forest["forest_loss"].sum()

    # Floating leaf decorations
    leaves_html = "".join([
        f'<div class="leaf-deco" style="left:{pos}%;animation-duration:{dur}s;animation-delay:{delay}s;">{emoji}</div>'
        for pos, dur, delay, emoji in [
            (8,  7, 0,   "🍃"), (22, 9, 2,  "🌿"), (38, 6, 1,  "🍃"),
            (55, 8, 3,   "🌱"), (70, 7, 0.5,"🍃"), (85, 9, 1.5,"🌿"),
        ]
    ])

    st.markdown(f"""
<div class="hero">
    {leaves_html}
    <div class="badge">🌿&nbsp; LIVE CLIMATE INTELLIGENCE DASHBOARD</div>
    <h1 class="hero-title">Our Planet<br>Is Changing</h1>
    <p class="hero-sub">
        An interactive deep-dive into the four most urgent climate crises —
        powered by real data, striking visuals, and the science behind them.
        Understanding the problem is the first step to solving it.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hs-val" style="color:#f87171">+{latest_temp:.2f}°C</div>
            <div class="hs-lbl">Temperature Rise</div>
        </div>
        <div class="hs-sep"></div>
        <div>
            <div class="hs-val" style="color:#fb923c">{co2_peak:.0f} Mt</div>
            <div class="hs-lbl">Peak CO₂ Output</div>
        </div>
        <div class="hs-sep"></div>
        <div>
            <div class="hs-val" style="color:#22d3ee">{latest_sea:.0f} mm</div>
            <div class="hs-lbl">Sea Level Rise</div>
        </div>
        <div class="hs-sep"></div>
        <div>
            <div class="hs-val" style="color:#4ade80">{forest_total/1000:.0f}K km²</div>
            <div class="hs-lbl">Forest Destroyed</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    qc1, qc2, qc3, qc4 = st.columns(4)
    for col, (label, page) in zip([qc1, qc2, qc3, qc4], [
        ("🏭 Explore CO₂","co2"),("🌡️ Temperature","temp"),("🌊 Sea Level","sea"),("🌳 Forest Loss","forest"),
    ]):
        with col:
            if st.button(label, key=f"qnav_{page}", use_container_width=True):
                go_to(page)

    st.markdown("""
<div class="section" style="padding-top:40px;padding-bottom:26px">
    <div class="eyebrow">Four Critical Crises</div>
    <h2 class="sh2">The Numbers Don't Lie</h2>
    <p class="sp">Each crisis amplifies the others. Together they define humanity's greatest challenge. Explore any dashboard for the complete data story.</p>
</div>""", unsafe_allow_html=True)

    CARDS = [
        {"page":"co2",   "cc":"#f97316","icon":"🏭","cat":"Atmosphere",
         "name":"CO₂ Emissions","num":f"{co2_peak:.0f}","unit":"Million Tonnes — Peak Annual Output",
         "text":"Carbon dioxide from fossil fuels has reached record concentrations, trapping heat and accelerating every other crisis on this list.",
         "pills":["Fossil Fuels","Industry","Transport","Power Generation"]},
        {"page":"temp",  "cc":"#ef4444","icon":"🌡️","cat":"Global Warming",
         "name":"Temperature Rise","num":f"+{latest_temp:.2f}","unit":"°C Above Historical Baseline",
         "text":"Earth's average temperature has risen dramatically since industrialisation. At current trajectories we will breach the 1.5°C Paris threshold within years.",
         "pills":["Heat Waves","Droughts","Crop Failure","Permafrost Melt"]},
        {"page":"sea",   "cc":"#22d3ee","icon":"🌊","cat":"Ocean Systems",
         "name":"Sea Level Rise","num":f"{latest_sea:.0f}","unit":"mm Above 1990 Reference Level",
         "text":"Thermal expansion and accelerating ice-sheet collapse are raising sea levels. Hundreds of millions of coastal residents face displacement by 2100.",
         "pills":["Glacier Melt","Ice Sheets","Coastal Flooding","Migration"]},
        {"page":"forest","cc":"#4ade80","icon":"🌳","cat":"Biosphere",
         "name":"Deforestation","num":f"{forest['forest_loss'].max():.0f}","unit":"km² — Peak Annual Loss (Single Country)",
         "text":"Forests absorb a third of all CO₂ emissions. Their destruction releases stored carbon, collapses biodiversity, and disrupts rainfall across continents.",
         "pills":["Biodiversity","Carbon Sink","Rainfall","Agriculture"]},
    ]
    card_cols = st.columns(4)
    for col, card in zip(card_cols, CARDS):
        with col:
            pills_html = "".join(f'<span class="pill">{p}</span>' for p in card["pills"])
            st.markdown(f"""
<div class="dcard" style="--cc:{card['cc']}">
    <div class="dcard-glow"></div>
    <span class="dcard-icon">{card['icon']}</span>
    <div class="dcard-cat">{card['cat']}</div>
    <div class="dcard-name">{card['name']}</div>
    <div class="dcard-num">{card['num']}</div>
    <div class="dcard-unit">{card['unit']}</div>
    <div class="dcard-text">{card['text']}</div>
    <div class="dcard-hr"></div>
    <div class="pills">{pills_html}</div>
</div>""", unsafe_allow_html=True)
            if st.button("Open Dashboard →", key=f"card_{card['page']}", use_container_width=True):
                go_to(card["page"])

    st.markdown("""
<div class="prev-section">
    <div class="eyebrow">What We Can Do</div>
    <h2 class="sh2" style="margin-bottom:8px">Prevention &amp; Action</h2>
    <p class="sp">Collective action can still prevent the worst outcomes. These four levers have the greatest scientific consensus for impact.</p>
</div>""", unsafe_allow_html=True)

    PREV = [
        {"icon":"⚡","head":"Clean Energy Transition","sub":"Replace fossil fuels at every scale",
         "items":["Accelerate solar and wind power deployment","Phase out coal-fired plants by 2035","Invest in long-duration energy storage","Electrify heating, transport, and industry","Support community renewable microgrids"]},
        {"icon":"🌿","head":"Nature-Based Solutions","sub":"Restore the ecosystems that protect us",
         "items":["Halt and reverse deforestation now","Restore coastal mangroves and wetlands","Protect 30% of land and ocean by 2030","Scale regenerative agriculture globally","Rewild degraded landscapes worldwide"]},
        {"icon":"🏙️","head":"Urban & Industrial Reform","sub":"Transform how cities and industry operate",
         "items":["Build net-zero carbon cities","Retrofit buildings for energy efficiency","Decarbonise steel, cement, and chemicals","Expand public and active transport","Adopt circular economy models"]},
        {"icon":"🌐","head":"Policy & Global Cooperation","sub":"Systems-level change through governance",
         "items":["Implement meaningful carbon pricing","End fossil fuel subsidies worldwide","Fund climate adaptation in the Global South","Strengthen Paris Agreement NDCs","Align financial flows with net-zero pathways"]},
    ]
    prev_cols = st.columns(4)
    for col, pr in zip(prev_cols, PREV):
        with col:
            items_html = "".join(f'<li><span class="arr">→</span>{item}</li>' for item in pr["items"])
            st.markdown(f"""
<div class="pcard">
    <div class="pcard-head">{pr['icon']}&nbsp; {pr['head']}</div>
    <div class="pcard-sub">{pr['sub']}</div>
    <ul class="pcard-list">{items_html}</ul>
</div>""", unsafe_allow_html=True)
