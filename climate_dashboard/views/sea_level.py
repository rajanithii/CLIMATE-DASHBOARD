"""Sea Level dashboard view."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression

from climate_dashboard.charts.theme import base
from climate_dashboard.components.navigation import go_to


def page_sea(sea):
    acc = "#22d3ee"

    st.markdown(f"""
<div class="dash-wrap">
    <div class="dash-header" style="--bg-glow:rgba(34,211,238,0.16); position:relative; overflow:hidden; padding-bottom:56px;">
        <div class="dash-header-glow"></div>
        <div class="dash-eyebrow" style="color:{acc}">
            <span class="dot" style="background:{acc}"></span>
            Ocean Systems · Coastal Threat
        </div>
        <h1 class="dash-h1">Rising <span style="color:{acc}">Sea Levels</span></h1>
        <p class="dash-desc">
            The ocean is swallowing coastlines. Driven by melting ice sheets and the thermal
            expansion of warming water, sea levels are rising faster than at any point
            in the last 3,000 years — and the rate is <em>accelerating</em>.
            Every millimetre matters for the 680 million people living in low-elevation coastal zones.
        </p>
        <div class="sea-wave-container">
            <div class="sea-wave"></div>
            <div class="sea-wave"></div>
            <div class="sea-wave"></div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_sea"):
        go_to("home")

    sea_s = sea.sort_values("year").copy()
    total_rise  = sea_s["sea_level"].iloc[-1] - sea_s["sea_level"].iloc[0]
    current_lvl = sea_s["sea_level"].iloc[-1]
    rate_mm_yr  = total_rise / (sea_s["year"].iloc[-1] - sea_s["year"].iloc[0])
    recent_rate = (sea_s["sea_level"].iloc[-1] - sea_s["sea_level"].iloc[-6]) / 5

    kpi_data = [
        ("Total Rise (Full Period)", f"{total_rise:.1f} mm",     f"{int(sea_s['year'].min())} → {int(sea_s['year'].max())}", "rise"),
        ("Current Sea Level",         f"{current_lvl:.1f} mm",    "Above 1990 reference baseline",                            "rise"),
        ("Long-Term Rate",            f"{rate_mm_yr:.1f} mm/yr",  "Average pace over full measurement period",                "rise"),
        ("Recent Rate (Last 5 Yrs)", f"{recent_rate:.1f} mm/yr", "⬆ The pace is accelerating",                               "rise"),
    ]
    st.markdown('<div class="kstrip">', unsafe_allow_html=True)
    kpi_cols = st.columns(4)
    for col, (lbl, val, delta, cls) in zip(kpi_cols, kpi_data):
        with col:
            st.markdown(f"""
<div class="kcard" style="--cc:{acc}">
    <div class="kcard-lbl">{lbl}</div>
    <div class="kcard-val">{val}</div>
    <div class="kcard-delta {cls}">{delta}</div>
</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-area">', unsafe_allow_html=True)

    # ── What rising seas actually mean ──
    st.markdown("""
<div class="eyebrow" style="padding:0 0 10px">📍 What Rising Seas Actually Mean for Real People</div>
<div class="impact-strip">
    <div class="impact-card" style="--ic:#a3e635">
        <div class="ic-scenario">Soon — Likely by 2030s</div>
        <div class="ic-level">+10 cm</div>
        <div class="ic-by">First major threshold</div>
        <div class="ic-effect">
            Storm surges reach further inland. Low-lying roads flood at high tide <em>with no storms at all.</em>
            Saltwater contaminates freshwater wells near coasts.
            Miami Beach is already pumping water from streets — this is the present, not the future.
        </div>
    </div>
    <div class="impact-card" style="--ic:#f59e0b">
        <div class="ic-scenario">Mid-Century — 2070 to 2100</div>
        <div class="ic-level">+50 cm</div>
        <div class="ic-by">Moderate scenario</div>
        <div class="ic-effect">
            Tens of millions displaced from river deltas in Bangladesh, Vietnam, and Egypt.
            Pacific island nations like Tuvalu and Kiribati face near-total submergence.
            Sea walls become essential national infrastructure — costing trillions.
        </div>
    </div>
    <div class="impact-card" style="--ic:#ef4444">
        <div class="ic-scenario">End of Century — High Scenario</div>
        <div class="ic-level">+1 m</div>
        <div class="ic-by">If emissions continue unchecked</div>
        <div class="ic-effect">
            150 million people permanently displaced — the largest forced migration in human history.
            Cities including Amsterdam, New Orleans, Jakarta, and Shanghai face existential flooding
            requiring enormous sea defences or full abandonment.
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    # ── Coastal cities at risk tiles ──
    st.markdown("""
<div class="eyebrow" style="padding:0 0 8px">🏙️ Coastal Cities at Risk Right Now</div>
<div class="city-grid">
    <div class="city-tile"><div class="city-risk" style="background:#ef4444"></div><div><div class="city-name">Jakarta, Indonesia</div><div class="city-detail">Sinking 25 cm/yr + sea rise</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#ef4444"></div><div><div class="city-name">Miami, USA</div><div class="city-detail">Regular tidal flooding now</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#f59e0b"></div><div><div class="city-name">Shanghai, China</div><div class="city-detail">Protects 24M people with walls</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#f59e0b"></div><div><div class="city-name">Amsterdam, Netherlands</div><div class="city-detail">1/3 of country below sea level</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#f59e0b"></div><div><div class="city-name">New Orleans, USA</div><div class="city-detail">2.5 m below sea level today</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#a3e635"></div><div><div class="city-name">Venice, Italy</div><div class="city-detail">MOSE barrier now operational</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#ef4444"></div><div><div class="city-name">Dhaka, Bangladesh</div><div class="city-detail">15M residents in flood zones</div></div></div>
    <div class="city-tile"><div class="city-risk" style="background:#f59e0b"></div><div><div class="city-name">Mumbai, India</div><div class="city-detail">18M coastal population at risk</div></div></div>
</div>""", unsafe_allow_html=True)

    # ── Population at Risk — animated progress bars ──
    st.markdown("""
<div class="eyebrow" style="padding:0 0 10px">👥 People at Risk Per Rise Scenario</div>
<div class="rise-bar-wrap">
    <div class="rise-bar-row">
        <div class="rb-label">Today (floods)</div>
        <div class="rb-track"><div class="rb-fill" style="width:3.2%;background:linear-gradient(90deg,#4ade80,#a3e635)"><span class="rb-val" style="color:#0b2010;font-size:0.78rem">11M</span></div></div>
    </div>
    <div class="rise-bar-row">
        <div class="rb-label">+10 cm rise</div>
        <div class="rb-track"><div class="rb-fill" style="width:14%;background:linear-gradient(90deg,#a3e635,#f59e0b)"><span class="rb-val" style="color:#0b2010;font-size:0.78rem">48M</span></div></div>
    </div>
    <div class="rise-bar-row">
        <div class="rb-label">+50 cm rise</div>
        <div class="rb-track"><div class="rb-fill" style="width:29%;background:linear-gradient(90deg,#f59e0b,#f97316)"><span class="rb-val" style="color:#fff;font-size:0.78rem">100M</span></div></div>
    </div>
    <div class="rise-bar-row">
        <div class="rb-label">+1 metre rise</div>
        <div class="rb-track"><div class="rb-fill" style="width:44%;background:linear-gradient(90deg,#f97316,#ef4444)"><span class="rb-val" style="color:#fff;font-size:0.78rem">150M</span></div></div>
    </div>
    <div class="rise-bar-row">
        <div class="rb-label">+2 metres rise</div>
        <div class="rb-track"><div class="rb-fill" style="width:100%;background:linear-gradient(90deg,#ef4444,#dc2626)"><span class="rb-val" style="color:#fff;font-size:0.78rem">340M people</span></div></div>
    </div>
</div>""", unsafe_allow_html=True)

    # ── Main trend chart with projection ──
    X = sea_s[["year"]].values
    y = sea_s["sea_level"].values
    lr = LinearRegression().fit(X, y)
    future_yrs = np.arange(int(sea_s["year"].max()) + 1, 2101)
    proj = lr.predict(future_yrs.reshape(-1, 1))
    resid_std = np.std(y - lr.predict(X))

    fig_main = go.Figure()
    fig_main.add_trace(go.Scatter(
        x=sea_s["year"], y=sea_s["sea_level"],
        mode="none", fill="tozeroy", fillcolor="rgba(34,211,238,0.08)", showlegend=False, hoverinfo="skip",
    ))
    fig_main.add_trace(go.Scatter(
        x=sea_s["year"], y=sea_s["sea_level"], mode="lines+markers",
        marker=dict(size=6, color=acc, line=dict(color="#164e63", width=1.5)),
        line=dict(color=acc, width=3, shape="spline"),
        name="Observed Level",
        hovertemplate="<b>%{x}</b><br>Sea Level: %{y:.1f} mm<extra></extra>",
    ))
    fig_main.add_trace(go.Scatter(
        x=future_yrs, y=proj + 2*resid_std, mode="lines",
        line=dict(color="rgba(34,211,238,0)", width=0), showlegend=False, hoverinfo="skip",
    ))
    fig_main.add_trace(go.Scatter(
        x=future_yrs, y=proj - 2*resid_std, mode="lines",
        fill="tonexty", fillcolor="rgba(34,211,238,0.11)",
        line=dict(color="rgba(34,211,238,0)", width=0), name="Projection Range (±2σ)",
    ))
    fig_main.add_trace(go.Scatter(
        x=future_yrs, y=proj, mode="lines",
        line=dict(color=acc, width=2.4, dash="dot"), name="ML Projection to 2100",
    ))
    fig_main.add_hline(y=current_lvl + 100, line_color="#a3e635", line_width=1.6, line_dash="dash",
                       annotation_text="+10 cm threshold", annotation_font_color="#a3e635", annotation_font_size=11)
    fig_main.add_hline(y=current_lvl + 500, line_color="#f59e0b", line_width=1.6, line_dash="dash",
                       annotation_text="+50 cm threshold", annotation_font_color="#f59e0b", annotation_font_size=11)
    fig_main.update_layout(
        **base(title="Sea Level Rise — Observed Data & Projection to 2100"),
        xaxis_title="Year", yaxis_title="Sea Level (mm above 1990 baseline)",
    )
    st.markdown("""
<div class="ccard" style="--cc:#22d3ee">
    <div class="ccard-title">🌊 The Rising Ocean — Historical Data & Future Projection</div>
    <div class="ccard-sub">Solid line = measured sea level · Dotted line = ML trend projection to 2100 · Shaded zone = uncertainty range · Dashed coloured lines mark key risk thresholds from the impact cards above</div>
    <div class="ccard-explain">💡 <strong>The slope of this curve is getting steeper</strong> — the ocean is rising faster now than 30 years ago. This acceleration is driven by Greenland and Antarctic ice sheets beginning to destabilise, adding meltwater on top of the thermal expansion already occurring.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_main, use_container_width=True, key="sea_main")

    col_a, col_b = st.columns(2)

    with col_a:
        sea_s["period"] = (sea_s["year"] // 5 * 5).astype(int)
        period_data = sea_s.groupby("period").agg(
            start_level=("sea_level","first"), end_level=("sea_level","last")
        ).reset_index()
        period_data["rate"]  = (period_data["end_level"] - period_data["start_level"]) / 5
        period_data["label"] = period_data["period"].astype(str) + "–" + (period_data["period"] + 4).astype(str)
        fig_rate = go.Figure(go.Bar(
            x=period_data["label"], y=period_data["rate"],
            marker=dict(color=period_data["rate"], colorscale=[[0,"#164e63"],[0.5,"#0e7490"],[1,"#22d3ee"]], line=dict(width=0)),
            text=period_data["rate"].apply(lambda v: f"{v:.1f}"),
            textposition="outside", textfont=dict(color="#86efac", size=12),
            hovertemplate="<b>%{x}</b><br>Rate: %{y:.2f} mm/yr<extra></extra>",
        ))
        fig_rate.update_layout(**base(title="Rate of Rise by 5-Year Period (mm/yr)"), xaxis_title="Period", yaxis_title="mm per year", bargap=0.22)
        fig_rate.update_xaxes(tickangle=45)
        st.markdown("""
<div class="ccard" style="--cc:#22d3ee">
    <div class="ccard-title">⚡ Is the Ocean Rising Faster Over Time?</div>
    <div class="ccard-sub">Each bar = how quickly the sea rose during that 5-year window, measured in mm per year · Taller bar = faster rise · This is the acceleration signal scientists fear</div>
    <div class="ccard-explain">💡 <strong>This is the most critical chart on this page.</strong> If bars were the same height, the rate would be stable. Instead, more recent bars are taller — the rise is accelerating. This is the signature of ice sheet meltwater being added on top of thermal expansion.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_rate, use_container_width=True, key="sea_rate")

    with col_b:
        sea_s["cumulative"] = sea_s["sea_level"] - sea_s["sea_level"].iloc[0]
        cum_norm = (sea_s["cumulative"] - sea_s["cumulative"].min()) / (sea_s["cumulative"].max() - sea_s["cumulative"].min() + 1e-9)
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(
            x=sea_s["year"], y=sea_s["cumulative"],
            mode="none", fill="tozeroy", fillcolor="rgba(34,211,238,0.08)", showlegend=False,
        ))
        fig_cum.add_trace(go.Scatter(
            x=sea_s["year"], y=sea_s["cumulative"], mode="markers+lines",
            marker=dict(size=7, color=cum_norm, colorscale=[[0,"#164e63"],[0.5,"#06b6d4"],[1,"#22d3ee"]], line=dict(color="#164e63", width=1)),
            line=dict(color=acc, width=2.5, shape="spline"),
            name="Cumulative Rise",
            hovertemplate="<b>%{x}</b><br>Total rise since start: +%{y:.1f} mm<extra></extra>",
        ))
        fig_cum.update_layout(**base(title="Cumulative Rise from First Measurement"), xaxis_title="Year", yaxis_title="Rise from starting point (mm)")
        st.markdown("""
<div class="ccard" style="--cc:#22d3ee">
    <div class="ccard-title">📈 How Much Has the Sea Risen in Total?</div>
    <div class="ccard-sub">Cumulative rise from the first measurement year — dots coloured from deep blue (small rise) to bright cyan (large rise) · Each point shows total accumulation to that year</div>
    <div class="ccard-explain">💡 Every millimetre of rise equals <strong>361 billion litres</strong> of water added to the global ocean — primarily from melting land ice. This chart shows the total volume added to coastal zones over the measurement period.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_cum, use_container_width=True, key="sea_cum")

    # People at risk chart
    context_data = {
        "Scenario": ["High-tide flood (today)","+10 cm rise","+50 cm rise","+1 metre rise","+2 metre rise"],
        "People at Risk (Millions)": [11, 48, 100, 150, 340],
        "colour": ["#4ade80","#a3e635","#f59e0b","#f97316","#ef4444"],
    }
    df_ctx = pd.DataFrame(context_data)
    fig_ctx = go.Figure(go.Bar(
        x=df_ctx["People at Risk (Millions)"], y=df_ctx["Scenario"],
        orientation="h",
        marker=dict(color=df_ctx["colour"], line=dict(width=0)),
        text=df_ctx["People at Risk (Millions)"].apply(lambda v: f"{v}M people"),
        textposition="outside", textfont=dict(color="#d1fae5", size=13),
        hovertemplate="<b>%{y}</b><br>People at risk: %{x}M<extra></extra>",
    ))
    fig_ctx.update_layout(
        **base(title="How Many People Each Rise Scenario Puts at Flood Risk"),
        xaxis_title="Estimated People at Risk (Millions)", yaxis_title="", bargap=0.28,
    )
    st.markdown("""
<div class="ccard" style="--cc:#22d3ee">
    <div class="ccard-title">🏘️ The Human Cost — People Exposed by Rise Scenario</div>
    <div class="ccard-sub">Estimated global population exposed to regular coastal flooding under different sea level rise scenarios · Based on NASA/IPCC population exposure modelling</div>
    <div class="ccard-explain">💡 Even the current baseline already exposes 11 million people to regular flooding. <strong>Every additional 10 cm of rise roughly doubles the exposed population.</strong> This chart makes the human cost of each degree of warming concrete and legible.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_ctx, use_container_width=True, key="sea_context")

    st.markdown("""
<div class="callout-warn">
    <strong>⚠️ Why the Rate Matters More Than the Total:</strong> Sea levels are currently rising at roughly
    3–4 mm per year — but that rate has roughly <strong>doubled since 1990</strong>. Scientists model this as potentially
    exponential, not linear. If ice sheet destabilisation accelerates, end-of-century projections range
    from 0.5 m to over 2 m. The difference between those scenarios is hundreds of millions of
    displaced people and trillions of dollars in infrastructure loss.
</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
