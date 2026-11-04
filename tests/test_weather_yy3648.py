"""Tests for the weather_yy3648 package."""


import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_yy3648 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32),             # Water freezes
        (100, 212),          # Water boils
        (-40, -40),          # The two scales meet
        (37, 98.6),          # Body temperature
        (-273.15, -459.67),  # Absolute zero is allowed
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Convert five Celsius temperatures, including boundary values."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)
@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("ten", TypeError),
        (None, TypeError),
        (True, TypeError),
        (-273.16, ValueError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Reject invalid inputs and temperatures below absolute zero."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Ignore one missing reading and check all four summary values."""
    # Arrange
    temps = [10.0, float("nan"), 20.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert set(result) == {"mean", "min", "max", "n_missing"}
    assert result["mean"] == pytest.approx(15.0)
    assert result["min"] == pytest.approx(10.0)
    assert result["max"] == pytest.approx(20.0)
    assert result["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Provide unsorted station readings with one missing and one invalid value."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": [
            "2026-07-02",
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-01",
        ],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Check the sample's columns, row count, and missing temperature."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1
# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Remove bad readings, convert temperatures, and sort the rows."""
    # Arrange: write the expected result by hand
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    # Act
    actual = clean_readings(raw_readings)

    # Assert
    assert_frame_equal(actual, expected)

def test_summarize_temperatures_all_missing():
    """Reject a list that has no valid readings."""
    with pytest.raises(ValueError, match="no valid temperature readings"):
        summarize_temperatures([float("nan"), float("nan")])
