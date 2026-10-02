"""Temperature dashboard view."""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression

from climate_dashboard.charts.theme import base
from climate_dashboard.components.navigation import go_to
from climate_dashboard.components.warming_stripes import warming_stripes_html


def page_temp(temp_agg, temp_raw):
    acc = "#f87171"
    st.markdown(f"""
<div class="dash-wrap">
    <div class="dash-header" style="--bg-glow:rgba(239,68,68,0.18)">
        <div class="dash-header-glow"></div>
        <div class="dash-eyebrow" style="color:{acc}">
            <span class="dot" style="background:{acc}"></span>
            Climate System · Global Warming
        </div>
        <h1 class="dash-h1">Global <span style="color:{acc}">Temperature</span> Rise</h1>
        <p class="dash-desc">
            Earth's average surface temperature has risen ~1.1°C since pre-industrial times.
            That sounds small — but it represents an enormous amount of trapped energy
            that is reshaping weather patterns, ecosystems, and coastlines worldwide.
        </p>
    </div>
</div>""", unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_temp"):
        go_to("home")

    baseline   = temp_agg[temp_agg["Year"] <= 1950]["temp"].mean()
    latest_t   = temp_agg["temp"].iloc[-1]
    anomaly    = latest_t - baseline
    warmest_yr = int(temp_agg.loc[temp_agg["temp"].idxmax(), "Year"])
    max_temp   = temp_agg["temp"].max()
    decade_avg = temp_agg[temp_agg["Year"] >= 2010]["temp"].mean()
    early_avg  = temp_agg[temp_agg["Year"] < 1960]["temp"].mean()
    decade_rise = decade_avg - early_avg

    kpi_data = [
        ("Latest Temperature",      f"{latest_t:.2f}°C",     "Most recent annual mean",                    "rise"),
        ("Anomaly vs Baseline",     f"+{anomaly:.2f}°C",      "Above 1900–1950 pre-industrial average",      "rise"),
        ("Hottest Year on Record",  str(warmest_yr),          f"Peaked at {max_temp:.2f}°C",                 "rise"),
        ("Long-Term Rise",          f"+{decade_rise:.2f}°C",  "2010s average vs pre-1960 average",           "rise"),
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

    st.markdown("""
<div class="ccard" style="--cc:#f87171">
    <div class="ccard-title">🌡️ Warming Stripes — 120 Years of Temperature in One Glance</div>
    <div class="ccard-sub">Each stripe = one year · Blue = cooler than average · Red = warmer than average · The dramatic shift from left to right tells the whole story</div>
    <div class="ccard-explain">💡 <strong>This visualisation was created by climate scientist Ed Hawkins.</strong> No numbers, no axes — just colour. The shift from a sea of blue to a wall of red is impossible to dismiss. Hover any stripe to see the exact year and temperature.</div>
</div>""", unsafe_allow_html=True)
    st.markdown(warming_stripes_html(temp_agg), unsafe_allow_html=True)

    X = temp_agg[["Year"]].values
    y = temp_agg["temp"].values
    lr = LinearRegression().fit(X, y)
    future_yrs = np.arange(int(temp_agg["Year"].max()) + 1, 2061)
    proj = lr.predict(future_yrs.reshape(-1, 1))
    resid_std = np.std(y - lr.predict(X))
    norm = (y - y.min()) / (y.max() - y.min())

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=temp_agg["Year"], y=temp_agg["temp"],
        mode="none", fill="tozeroy", fillcolor="rgba(239,68,68,0.07)", showlegend=False,
    ))
    fig_trend.add_trace(go.Scatter(
        x=temp_agg["Year"], y=temp_agg["temp"], mode="markers",
        marker=dict(size=5, color=norm, colorscale=[[0,"#1e40af"],[0.35,"#7c3aed"],[0.65,"#f97316"],[1,"#dc2626"]]),
        name="Annual Mean", hovertemplate="<b>%{x}</b> → %{y:.2f}°C<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=temp_agg["Year"], y=temp_agg["temp"].rolling(10, center=True).mean(),
        mode="lines", line=dict(color="#f87171", width=3, shape="spline"), name="10-yr Smooth",
    ))
    fig_trend.add_trace(go.Scatter(
        x=future_yrs, y=proj + 2*resid_std, mode="lines",
        line=dict(color="rgba(239,68,68,0)", width=0), showlegend=False, hoverinfo="skip",
    ))
    fig_trend.add_trace(go.Scatter(
        x=future_yrs, y=proj - 2*resid_std, mode="lines",
        fill="tonexty", fillcolor="rgba(239,68,68,0.13)",
        line=dict(color="rgba(239,68,68,0)", width=0), name="±2σ Projection Range",
    ))
    fig_trend.add_trace(go.Scatter(
        x=future_yrs, y=proj, mode="lines",
        line=dict(color="#f87171", width=2.4, dash="dot"), name="ML Projection",
    ))
    fig_trend.add_hline(y=baseline + 1.5, line_color="#fbbf24", line_width=1.8, line_dash="dash",
                        annotation_text="Paris 1.5°C limit", annotation_font_color="#fbbf24", annotation_font_size=12)
    fig_trend.update_layout(
        **base(title="Surface Temperature 1900–Present + Projection to 2060"),
        xaxis_title="Year", yaxis_title="Temperature (°C)",
    )
    st.markdown("""
<div class="ccard" style="--cc:#f87171">
    <div class="ccard-title">📉 The Temperature Trend — Past, Present &amp; Projected Future</div>
    <div class="ccard-sub">Dots coloured blue (cool) to red (hot) · Smooth line = 10-year rolling average · Shaded zone = ML projection range to 2060 · Yellow dashed = Paris 1.5°C limit</div>
    <div class="ccard-explain">💡 <strong>The dashed yellow line is the Paris Agreement's 1.5°C limit</strong> — the threshold beyond which scientists warn of irreversible and cascading impacts. The projection shows we could breach it within decades if current trends continue unabated.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True, key="temp_trend")

    col_a, col_b = st.columns(2)
    with col_a:
        temp_agg["decade"] = (temp_agg["Year"] // 10 * 10).astype(int)
        d_avg = temp_agg.groupby("decade")["temp"].mean().reset_index()
        d_norm = (d_avg["temp"] - d_avg["temp"].min()) / (d_avg["temp"].max() - d_avg["temp"].min())
        fig_dec = go.Figure(go.Bar(
            x=d_avg["decade"].astype(str) + "s",
            y=d_avg["temp"],
            marker=dict(color=d_norm, colorscale=[[0,"#1e3a5f"],[0.4,"#3b82f6"],[0.7,"#f97316"],[1,"#dc2626"]], line=dict(width=0)),
            text=d_avg["temp"].apply(lambda v: f"{v:.2f}°C"),
            textposition="outside", textfont=dict(color="#d1fae5", size=12),
            hovertemplate="<b>%{x}</b><br>Avg: %{y:.2f}°C<extra></extra>",
        ))
        fig_dec.update_layout(**base(title="Decade-by-Decade Average Temperature"), xaxis_title="Decade", yaxis_title="°C", bargap=0.22)
        st.markdown("""
<div class="ccard" style="--cc:#f87171">
    <div class="ccard-title">📊 The Warming Ladder — Every Decade Gets Hotter</div>
    <div class="ccard-sub">Each bar is one decade's average temperature · Blue = cooler decades · Red = hotter decades · The direction is unmistakable</div>
    <div class="ccard-explain">💡 Every decade since the 1970s has been warmer than the one before it. This consistent, accelerating pattern is the fingerprint of accumulated greenhouse gases — not natural variation.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_dec, use_container_width=True, key="temp_decade")

    with col_b:
        cur_anom = latest_t - baseline
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=cur_anom,
            delta=dict(reference=0, valueformat=".2f", suffix="°C vs baseline", increasing=dict(color="#f87171")),
            number=dict(suffix="°C", font=dict(size=40, color="#f0fdf4")),
            gauge=dict(
                axis=dict(range=[-0.5, 2.5], tickwidth=1, tickcolor="#4d7a5c", tickfont=dict(size=12, color="#86efac")),
                bar=dict(color="#ef4444", thickness=0.30),
                bgcolor="rgba(5,18,9,0)",
                steps=[
                    dict(range=[-0.5, 0],  color="rgba(30,64,175,0.35)"),
                    dict(range=[0,    1.5], color="rgba(74,222,128,0.09)"),
                    dict(range=[1.5,  2.0], color="rgba(251,191,36,0.18)"),
                    dict(range=[2.0,  2.5], color="rgba(239,68,68,0.22)"),
                ],
                threshold=dict(line=dict(color="#fbbf24", width=3.5), thickness=0.8, value=1.5),
            ),
            title=dict(text="Current Warming vs Pre-industrial<br><sub>Yellow marker = Paris 1.5°C danger threshold</sub>", font=dict(size=14, color="#86efac")),
        ))
        fig_gauge.update_layout(**base(height=380))
        st.markdown("""
<div class="ccard" style="--cc:#f87171">
    <div class="ccard-title">🌡️ How Close Are We to the Danger Zone?</div>
    <div class="ccard-sub">Needle = current warming above pre-industrial baseline · Yellow threshold = Paris 1.5°C limit · Red zone = catastrophic warming territory</div>
    <div class="ccard-explain">💡 The difference between 1.5°C and 2°C of warming may sound small, but it means hundreds of millions more people exposed to extreme heat, severe water stress, and sea level rise that could submerge entire coastal nations.</div>
</div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, key="temp_gauge")

    country_avg = (
        temp_raw[temp_raw["Year"] >= 1980]
        .groupby("Country")["Adjusted Temperature"].mean()
        .reset_index()
        .rename(columns={"Country":"country","Adjusted Temperature":"avg_temp"})
    )
    fig_geo = px.choropleth(
        country_avg, locations="country", locationmode="country names",
        color="avg_temp",
        color_continuous_scale=[[0,"#1e3a5f"],[0.3,"#3b82f6"],[0.6,"#fb923c"],[1,"#dc2626"]],
        labels={"avg_temp":"°C"}, hover_name="country",
    )
    fig_geo.update_layout(
        **base(title="Average Surface Temperature by Country (1980–Present)"),
        geo=dict(
            bgcolor="rgba(0,0,0,0)", showframe=False,
            showcoastlines=True, coastlinecolor="rgba(74,222,128,0.18)",
            landcolor="rgba(10,28,12,0.88)",
            showocean=True, oceancolor="rgba(5,18,9,1)",
        ),
        coloraxis_colorbar=dict(
            bgcolor="rgba(0,0,0,0.55)", bordercolor="rgba(74,222,128,0.10)",
            tickfont=dict(color="#86efac", size=11),
            title=dict(text="°C", font=dict(color="#86efac", size=12)),
            thickness=14, len=0.7,
        ),
    )
    st.markdown("""
<div class="ccard" style="--cc:#f87171">
    <div class="ccard-title">🗺️ Where Is Earth Warming the Fastest?</div>
    <div class="ccard-sub">Average surface temperature by country since 1980 — deeper red = hotter average climate · Reveals which regions face the harshest conditions</div>
    <div class="ccard-explain">💡 The Arctic and northern latitudes are warming 2–4× faster than the global average — a phenomenon called Arctic Amplification. Equatorial regions may already be too hot for safe outdoor labour during summer months.</div>
</div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_geo, use_container_width=True, key="temp_geo")
    st.markdown("</div>", unsafe_allow_html=True)
