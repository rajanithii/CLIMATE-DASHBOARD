"""Temperature warming-stripe chart markup."""

import pandas as pd

def _temp_to_hex(t: float) -> str:
    t = max(0.0, min(1.0, t))
    stops = [
        (0.00, (  5,  48,  97)),
        (0.20, ( 33, 102, 172)),
        (0.40, (146, 197, 222)),
        (0.50, (247, 247, 247)),
        (0.60, (253, 219, 199)),
        (0.80, (214,  96,  77)),
        (1.00, (103,   0,  31)),
    ]
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return "#{:02x}{:02x}{:02x}".format(
                int(c0[0] + f * (c1[0] - c0[0])),
                int(c0[1] + f * (c1[1] - c0[1])),
                int(c0[2] + f * (c1[2] - c0[2])),
            )
    return "#5e0d0d"

def warming_stripes_html(df: pd.DataFrame) -> str:
    vmin, vmax = df["temp"].min(), df["temp"].max()
    bars = "".join(
        f'<div class="stripe" title="{int(r.Year)}: {r.temp:.2f}°C" '
        f'style="background:{_temp_to_hex((r.temp - vmin) / (vmax - vmin))}"></div>'
        for r in df.itertuples()
    )
    y0, y1 = int(df["Year"].min()), int(df["Year"].max())
    return (
        f'<div class="stripes-outer">{bars}</div>'
        f'<div class="stripe-lbl"><span>{y0}</span>'
        f'<span style="letter-spacing:1px">← COOLER &nbsp;·&nbsp; WARMER →</span>'
        f'<span>{y1}</span></div>'
    )
