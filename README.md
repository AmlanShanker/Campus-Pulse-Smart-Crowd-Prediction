# CHRIST Campus Pulse

**A Smart Campus Monitoring, Crowd Analytics & Prediction Dashboard**  
An academic dashboard built with **Python, Streamlit, Pandas and Plotly** for the MCA Python Programming course (MCA411-2).

## Live dashboard

Explore the deployed application: **[CHRIST Campus Pulse – Open Dashboard](https://campus-pulse-smart-crowd-prediction.streamlit.app/)**

> **Data notice:** This project uses a bundled synthetic dataset for demonstration. It does not use live student data, official CHRIST University telemetry, or real-time campus sensors. Location names and capacity figures are illustrative.

## What the dashboard does

Campus Pulse presents campus-space activity through five focused views. Use the shared sidebar filters to select an observation date range and one or more locations; the charts and summary metrics update to reflect that selection.

| Dashboard view | What you can explore |
| --- | --- |
| **Overview** | Campus-wide occupancy KPIs, daily activity trends, average utilization by location and crowd-level distribution. |
| **Crowd intelligence** | Location-by-time occupancy heatmap, crowd-level readings by location and occupancy spread. |
| **Library** | Average occupancy, estimated free seats, peak and quiet study periods, weekday patterns, daily breakdown and CSV export. |
| **Cafeteria** | Average and peak estimated waiting times, occupancy by time slot and daily waiting-time trends. |
| **Smart insights** | Highest-occupancy location/time combinations, estimated waiting-time highlights and a historical-average baseline. |

The interface uses a dark theme, responsive layouts, subtle transitions and reduced-motion support. It is a dashboard only: there are no student accounts, login screens or data-entry forms.

## Smart Insights: how the estimates work

Smart Insights groups the selected historical observations by **location** and **time slot**, then calculates average occupancy and average waiting time for each group. It highlights the busiest combinations and displays the highest-occupancy results.

This is a **historical-average baseline**, not a trained machine-learning model, predictive AI system or live forecast. The estimates describe patterns in the selected synthetic demonstration data only.

## Dataset

Bundled file: `data/christ_campus_pulse_data.csv`

The dataset contains **1,440 synthetic observations** across **30 dates** (19 October–17 November 2026), **8 illustrative campus locations** and **6 daily time slots**.

The records include:

- Observation date, time, weekday and location
- Crowd-level category
- Occupancy and assumed capacity
- Estimated waiting time in minutes
- Estimated available seats
- Data-type label

Occupancy percentages and summary values are calculated by the dashboard from these fields. Capacity, seat availability and waiting times are illustrative values—not measurements of actual campus facilities.

## Run locally

Python 3.10 or later is recommended.

1. Clone the repository and open its folder:

   ```bash
   git clone https://github.com/AmlanShanker/Campus-Pulse-Smart-Crowd-Prediction.git
   cd Campus-Pulse-Smart-Crowd-Prediction
   ```

2. (Optional) Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the application dependencies and launch Streamlit:

   ```bash
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

Streamlit will print a local URL (usually `http://localhost:8501`) to open in your browser.

## Quality checks

The repository includes automated dataset tests and a GitHub Actions quality-check workflow. To run the checks locally:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m compileall -q app.py
pytest -q
```

## Deploy with Streamlit Community Cloud

1. Push or merge the reviewed project changes to the repository's `main` branch.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in.
3. Create a new app and select this GitHub repository.
4. Choose branch `main` and set the main file path to `app.py`.
5. Deploy the app.

The app reads its CSV from the repository's `data/` directory, so keep the bundled dataset in place when deploying. No secrets, external API keys or database configuration are required by the current implementation.

## Project structure

```text
.
├── app.py
├── data/
│   └── christ_campus_pulse_data.csv
├── tests/
│   └── test_dataset.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Academic scope and disclaimer

CHRIST Campus Pulse is an independent academic prototype created for MCA411-2. It demonstrates dashboard design, data filtering, exploratory analysis and clear presentation of historical averages using Python.

It is **not** an official CHRIST University system, is not affiliated with or endorsed by the University, and must not be used to infer actual campus occupancy or operational conditions.
