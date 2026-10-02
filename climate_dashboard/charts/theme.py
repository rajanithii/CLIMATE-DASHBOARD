"""Shared Plotly styling for dashboard charts."""

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,24,12,0.85)",
    font=dict(family="'Plus Jakarta Sans', Inter, sans-serif", color="#d1fae5", size=13),
    margin=dict(l=14, r=14, t=62, b=14),
    legend=dict(
        bgcolor="rgba(8,24,12,0.92)",
        bordercolor="rgba(74,222,128,0.18)",
        borderwidth=1,
        font=dict(size=13),
    ),
    xaxis=dict(
        gridcolor="rgba(74,222,128,0.08)",
        linecolor="rgba(74,222,128,0.14)",
        tickfont=dict(size=12),
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(74,222,128,0.08)",
        linecolor="rgba(74,222,128,0.14)",
        tickfont=dict(size=12),
        zeroline=False,
    ),
)

def base(**kw):
    d = dict(_BASE_LAYOUT)
    d.update(kw)
    return d
