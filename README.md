# CHRIST Campus Pulse

**A Smart Campus Monitoring, Crowd Analytics & Prediction Dashboard** built with Python, Streamlit, Pandas and Plotly.

> Academic prototype for MCA Python Programming (MCA411-2). The bundled dataset is synthetic demonstration data. It is not official CHRIST University telemetry and must not be represented as measured university data.

## Dashboard features

- Dark, responsive interface with subtle motion and reduced-motion accessibility support.
- Campus overview KPIs and daily activity trends.
- Crowd-intelligence heatmap, crowd distribution and occupancy analysis.
- Library occupancy, estimated seat availability and weekday/time patterns.
- Cafeteria waiting-time and peak-hour analytics.
- Filter-aware Smart Insights based on transparent historical averages.
- Shared date-range and campus-location filters.
- Bundled CSV dataset; no login, student data-entry forms, external APIs or database required.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

File: `data/christ_campus_pulse_data.csv`

- 1,440 synthetic observations across 30 dates and 8 illustrative campus locations.
- Six daily time slots per location.
- Includes occupancy, assumed capacity, crowd level, estimated waiting time and available seats.

Location names are illustrative dashboard categories. Values are generated for demonstration and do not describe actual campus conditions.

## Run quality checks

Install the development test dependency and run the automated dataset checks:

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m compileall -q app.py
pytest -q
```

GitHub Actions runs syntax and dataset checks on pushes to `main` and pull requests targeting `main`.

## Deploy on Streamlit Community Cloud

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create an app and select this repository.
3. Select branch `main` after merging the reviewed changes.
4. Set the main file path to `app.py`.
5. Deploy.

## Project structure

```text
.
├── app.py
├── data/
│   └── christ_campus_pulse_data.csv
├── tests/
│   └── test_dataset.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── .streamlit/
    └── config.toml
```

## Academic note

The Smart Insights page uses a transparent historical-average baseline, not a trained machine-learning model or live prediction. This keeps the logic explainable for a viva. The application is a dashboard only: there are no student data-entry workflows or user accounts.

The dashboard is an independent academic prototype and is not affiliated with or endorsed by CHRIST University.
