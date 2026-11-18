from pathlib import Path

import pandas as pd

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "christ_campus_pulse_data.csv"
)
EXPECTED_COLUMNS = {
    "Date",
    "Time",
    "Day",
    "Location",
    "Crowd_Level",
    "Occupancy",
    "Capacity",
    "Waiting_Time_Min",
    "Available_Seats",
    "Data_Type",
}


def load_dataset():
    return pd.read_csv(DATA_PATH, parse_dates=["Date"])


def test_dataset_has_expected_schema_and_size():
    data = load_dataset()

    assert EXPECTED_COLUMNS.issubset(data.columns)
    assert len(data) == 1440
    assert data["Location"].nunique() == 8
    assert data["Time"].nunique() == 6


def test_each_location_has_one_reading_per_date_and_time():
    data = load_dataset()

    assert not data.duplicated(["Date", "Time", "Location"]).any()


def test_capacity_and_seat_counts_are_consistent():
    data = load_dataset()

    assert (data["Capacity"] > 0).all()
    assert (data["Occupancy"] >= 0).all()
    assert (data["Occupancy"] <= data["Capacity"]).all()
    assert (data["Available_Seats"] >= 0).all()
    assert (
        data["Available_Seats"] == data["Capacity"] - data["Occupancy"]
    ).all()


def test_crowd_labels_and_wait_times_are_valid():
    data = load_dataset()

    assert set(data["Crowd_Level"].unique()) <= {"Low", "Medium", "High"}
    assert (data["Waiting_Time_Min"] >= 0).all()


def test_dates_and_dataset_disclosure_are_consistent():
    data = load_dataset()
    expected_days = data["Date"].dt.day_name()

    assert (data["Day"] == expected_days).all()
    assert data["Data_Type"].eq("Synthetic demonstration data").all()
