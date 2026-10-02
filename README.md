# ClimatePulse

Interactive climate visualization dashboard built with Streamlit, pandas, and Plotly.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```powershell
python -m pip install -r requirements-dev.txt
pytest
```

## Project layout

- `app.py` configures Streamlit and dispatches the selected dashboard view.
- `climate_dashboard/views/` contains the home, CO2, temperature, sea-level, and forest views.
- `climate_dashboard/data_loader.py` loads the source datasets; `data_processing.py` cleans and aggregates them.
- `climate_dashboard/charts/` and `components/` contain shared chart styling and UI elements.
- `assets/styles.css` contains the dashboard stylesheet.
- `data/raw/` contains the source CSV datasets.
- `tests/` contains data-processing tests.