import pandas as pd

from climate_dashboard.data_processing import (
    prepare_numeric_data,
    prepare_temperature_data,
)


def test_prepare_temperature_data_cleans_and_aggregates_without_mutating_input():
    source = pd.DataFrame(
        {
            "Year": ["1899", "1900", "1900", "bad"],
            "Adjusted Temperature": ["0.5", "1.0", "3.0", "2.0"],
            "Country": ["A", "A", "B", "C"],
        }
    )

    aggregated, cleaned = prepare_temperature_data(source)

    assert len(source) == 4
    assert cleaned["Year"].tolist() == [1899, 1900, 1900]
    assert aggregated.to_dict("records") == [{"Year": 1900, "temp": 2.0}]


def test_prepare_numeric_data_converts_values_and_drops_invalid_rows():
    source = pd.DataFrame({"year": ["2000", "bad"], "value": ["1.5", "2.0"]})

    cleaned = prepare_numeric_data(source, ("year", "value"))

    assert cleaned.to_dict("records") == [{"year": 2000, "value": 1.5}]


def test_prepare_numeric_data_can_drop_rows_with_any_missing_value():
    source = pd.DataFrame(
        {"year": ["2000", "2001"], "value": ["1.5", "2.0"], "country": ["A", None]}
    )

    cleaned = prepare_numeric_data(
        source, ("year", "value"), drop_all_missing=True
    )

    assert cleaned["year"].tolist() == [2000]