# CHRIST Campus Pulse

**A Smart Campus Monitoring, Crowd Analytics & Prediction Dashboard** built with Python, Streamlit, Pandas and Plotly.

> Academic prototype for MCA Python Programming (MCA411-2). The bundled dataset is synthetic demonstration data. It is not official CHRIST University telemetry and should not be represented as measured university data.

## Features

- Premium dark dashboard with custom CSS, responsive layout and subtle motion effects.
- Campus overview KPIs and daily activity trends.
- Crowd intelligence heatmap, crowd distribution and occupancy analysis.
- Library occupancy and estimated seat-availability analytics.
- Cafeteria waiting-time and peak-hour analytics.
- Transparent baseline crowd-pattern estimates using historical averages.
- Sidebar filters for date range and campus locations.
- Bundled CSV dataset; no login, forms, external APIs or database required.

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

## Run quality checks\n\nInstall the development test dependency and run the automated dataset checks:\n\n```bash\npip install -r requirements.txt\npip install -r requirements-dev.txt\npython -m compileall -q app.py\npytest -q\n```\n\nGitHub Actions runs the same syntax and dataset checks on pushes to `main` and pull requests targeting `main`.\n\n## Deploy on Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/.
2. Create an app and select this repository.
3. Select branch `main` after merging the project PR.
4. Set the main file path to `app.py`.
5. Deploy.

## Project structure

```text
.
├── app.py
├── data/christ_campus_pulse_data.csv
├── requirements.txt
├── README.md
└── .streamlit/config.toml
```

## Academic note

The Smart Insights page uses a transparent historical-average baseline, not a trained predictive model. This keeps the logic explainable for a viva. The application is a dashboard only: there are no student data-entry workflows or user accounts.

The dashboard is an independent academic prototype and is not affiliated with or endorsed by CHRIST University.
