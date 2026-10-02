"""Co2 dashboard view."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from climate_dashboard.charts.theme import base
from climate_dashboard.components.navigation import go_to


def page_co2(co2):
    acc = "#fb923c"
    st.markdown(f"""
<div class="dash-wrap">
    <div class="dash-header" style="--bg-glow:rgba(249,115,22,0.20)">
        <div class="dash-header-glow"></div>
        <div class="dash-eyebrow" style="color:{acc}">
            <span class="dot" style="background:{acc}"></span>
            Atmosphere · Carbon Emissions
        </div>
        <h1 class="dash-h1">Global <span style="color:{acc}">CO₂</span> Emissions</h1>
        <p class="dash-desc">
            Carbon dioxide is the primary heat-trapping gas from human activity.
            Every tonne emitted stays in the atmosphere for centuries — meaning today's
            decisions lock in tomorrow's temperatures for generations.
        </p>
    </div>
</div>""", unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_co2"):
        go_to("home")

    total_co2      = co2["co2"].sum()
    max_co2        = co2["co2"].max()
    top_country    = co2.groupby("country")["co2"].sum().idxmax()
    latest_total   = co2[co2["year"] == co2["year"].max()]["co2"].sum()
    earliest_total = co2[co2["year"] == co2["year"].min()]["co2"].sum()
    growth_pct     = (latest_total - earliest_total) / earliest_total * 100

    kpi_data = [
        ("Total Emissions Tracked",  f"{total_co2/1e6:.2f}B Mt", "All countries, all years",                       "neutral"),
        ("Single Highest Record",     f"{max_co2:.0f} Mt",         "Peak single-country output",                     "rise"),
        ("Top Cumulative Emitter",    top_country,                  "By all-time total output",                       "neutral"),
        ("Emission Growth",           f"+{growth_pct:.0f}%",        f"{int(co2.year.min())} → {int(co2.year.max())}","rise"),
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

    fig_map = px.choropleth(
        co2.dropna(subset=["co2"]),
        locations="country", locationmode="country names", color="co2",
        animation_frame="year",
        color_continuous_scale=[[0,"#0f0500"],[0.2,"#7c2d12"],[0.5,"#c2410c"],[0.8,"#f97316"],[1,"#fed7aa"]],
        labels={"co2":"Mt CO₂"}, hover_name="country",
    )
    fig_map.update_layout(
        **base(title="CO₂ Emissions by Country — Animated Year by Year", title_font_size=14),
        geo=dict(
            bgcolor="rgba(0,0,0,0)", showframe=False,
            showcoastlines=True, coastlinecolor="rgba(74,222,128,0.18)",
            landcolor="rgba(10,28,12,0.88)",
            showocean=True, oceancolor="rgba(5,18,9,1)",
            lakecolor="rgba(5,18,9,0.8)",
        ),
        coloraxis_colorbar=dict(
            bgcolor="rgba(0,0,0,0.55)", bordercolor="rgba(74,222,128,0.10)",
            tickfont=dict(color="#86efac", size=11),
            title=dict(text="Mt CO₂", font=dict(color="#86efac", size=12)),
            thickness=14, len=0.7,
        ),
    )
    st.markdown("""
<div class="ccard" style="--cc:#fb923c">
    <div class="ccard-title">🌍 CO₂ Emissions World Map — Press ▶ to Play</div>
    <div class="ccard-sub">Each country is shaded by its annual CO₂ output · Deeper orange = higher emissions · Hover any country for exact figures</div>
    <div class="ccard-explain">💡 <strong>What to look for:</strong> Watch China (light in 1960) turn deep orange by 2020. The USA stays dark orange throughout. Most developing nations remain light — yet they will bear the worst consequences of emissions they barely contributed to. This is the core injustice of climate change.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True, key="co2_map")

    col_a, col_b = st.columns(2)
    with col_a:
        latest_yr = int(co2["year"].max())
        top10 = co2[co2["year"] == latest_yr].nlargest(10, "co2").sort_values("co2")
        fig_bar = go.Figure(go.Bar(
            x=top10["co2"], y=top10["country"], orientation="h",
            marker=dict(color=top10["co2"], colorscale=[[0,"#7c2d12"],[0.5,"#c2410c"],[1,"#fb923c"]], line=dict(width=0)),
            text=top10["co2"].apply(lambda v: f"{v:,.0f} Mt"),
            textposition="outside", textfont=dict(color="#86efac", size=12),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f} Mt CO₂<extra></extra>",
        ))
        fig_bar.update_layout(**base(title=f"Top 10 Biggest Emitters — {latest_yr}"), xaxis_title="Million Tonnes CO₂", yaxis_title="", bargap=0.25)
        st.markdown(f"""
<div class="ccard" style="--cc:#fb923c">
    <div class="ccard-title">📊 Who Emits the Most Right Now?</div>
    <div class="ccard-sub">Top 10 CO₂-producing countries in {latest_yr} — these nations together account for the majority of all global emissions</div>
    <div class="ccard-explain">💡 Changes in the energy policy of these 10 countries have an outsized effect on the entire planet's climate trajectory. A single policy shift in any of them can move the global needle more than decades of individual action combined.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, key="co2_bar")

    with col_b:
        global_co2 = co2.groupby("year")["co2"].sum().reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=global_co2["year"], y=global_co2["co2"],
            mode="none", fill="tozeroy", fillcolor="rgba(249,115,22,0.09)", showlegend=False,
        ))
        fig_trend.add_trace(go.Scatter(
            x=global_co2["year"], y=global_co2["co2"],
            mode="lines+markers",
            marker=dict(size=5, color=acc, line=dict(color="#7c2d12", width=1.5)),
            line=dict(color=acc, width=2.8, shape="spline"),
            name="Global Total",
            hovertemplate="<b>%{x}</b><br>Global Total: %{y:,.0f} Mt<extra></extra>",
        ))
        fig_trend.update_layout(**base(title="Global CO₂ — 60 Years of Unbroken Rise"), xaxis_title="Year", yaxis_title="Total Mt CO₂")
        st.markdown("""
<div class="ccard" style="--cc:#fb923c">
    <div class="ccard-title">📈 The Relentless Rise — Global CO₂ Since 1960</div>
    <div class="ccard-sub">Combined annual emissions from all tracked countries — an unbroken upward trend across six decades of industrial growth</div>
    <div class="ccard-explain">💡 The small dip around 2020 is the COVID-19 lockdown — the largest single-year emissions drop in modern history. Yet emissions bounced back within two years, proving that crisis disruption alone cannot solve a structural problem. Only systemic change will.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_trend, use_container_width=True, key="co2_trend")

    top5_c = co2.groupby("country")["co2"].sum().nlargest(5).index.tolist()
    WARM5 = ["#fed7aa","#fb923c","#f97316","#ea580c","#c2410c"]
    fig_lines = go.Figure()
    for country, clr in zip(top5_c, WARM5):
        df_c = co2[co2["country"] == country].sort_values("year")
        fig_lines.add_trace(go.Scatter(
            x=df_c["year"], y=df_c["co2"], mode="lines+markers",
            marker=dict(size=4, color=clr), line=dict(color=clr, width=2.4, shape="spline"),
            name=country, hovertemplate=f"<b>{country}</b> %{{x}}: %{{y:,.0f}} Mt<extra></extra>",
        ))
    fig_lines.update_layout(**base(title="Top 5 Emitters — How Their Output Has Evolved"), xaxis_title="Year", yaxis_title="Mt CO₂")
    st.markdown("""
<div class="ccard" style="--cc:#fb923c">
    <div class="ccard-title">🏁 Top 5 Emitters — Side-by-Side Over Time</div>
    <div class="ccard-sub">Each line tracks one country's annual emissions · Lines levelling off = energy transition underway · Lines still climbing = fossil fuel dependence continues</div>
    <div class="ccard-explain">💡 The gap between countries with declining emissions and those still rising is widening. This chart shows that decarbonisation is possible — the question is whether it is happening fast enough to matter for the climate.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_lines, use_container_width=True, key="co2_lines")
    st.markdown("</div>", unsafe_allow_html=True)
