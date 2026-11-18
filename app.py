import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Campus Pulse | CHRIST University",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_PATH = Path(__file__).parent / "data" / "christ_campus_pulse_data.csv"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#111a29;--panel:#1a2940;--line:rgba(148,163,184,.14);--muted:#91a2bd;--text:#edf4ff;--cyan:#54d8f5;--violet:#9a8cff}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.stApp{background:radial-gradient(ellipse at 10% 0%,rgba(79,112,190,.19),transparent 34%),radial-gradient(ellipse at 90% 8%,rgba(139,94,198,.15),transparent 30%),var(--bg);color:var(--text)}
[data-testid="stHeader"]{background:rgba(17,26,41,.82)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1b2a40,#142136);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:#dce7fa}
.block-container{padding-top:1.5rem;padding-bottom:2.5rem;max-width:1440px}
h1,h2,h3{color:var(--text)!important;letter-spacing:-.035em}
p,label,.stMarkdown{color:#c4d0e3}
.brand{font:500 .7rem 'DM Mono',monospace;letter-spacing:.18em;color:var(--cyan);text-transform:uppercase}
.hero{padding:1.35rem 1.6rem;border:1px solid rgba(127,155,210,.2);border-radius:20px;background:linear-gradient(115deg,rgba(38,57,88,.96),rgba(29,43,67,.92) 58%,rgba(66,48,91,.78));position:relative;overflow:hidden;animation:rise .5s ease both}
.hero:after{content:'';position:absolute;width:220px;height:220px;right:-75px;top:-135px;border-radius:50%;border:1px solid rgba(84,216,245,.22);box-shadow:0 0 0 28px rgba(84,216,245,.025),0 0 0 58px rgba(154,140,255,.025)}
.hero h1{font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:800;margin:.25rem 0}
.hero p{color:#b9c8df;max-width:760px;margin:0;font-size:.94rem}
.hero-meta{margin-top:13px;font: .68rem 'DM Mono',monospace;color:#8fa5c5;letter-spacing:.07em}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#4ce0a0;margin-right:8px;box-shadow:0 0 0 0 rgba(76,224,160,.55);animation:pulse 1.8s infinite}
.kpi{background:linear-gradient(145deg,rgba(34,50,75,.97),rgba(25,39,61,.97));border:1px solid var(--line);border-radius:15px;padding:14px 16px;min-height:105px;transition:transform .2s ease,border-color .2s ease}
.kpi{animation:softIn .55s ease both}
.kpi:hover{transform:translateY(-3px);border-color:rgba(84,216,245,.4);box-shadow:0 10px 26px rgba(0,0,0,.10)}
.stTabs [data-baseweb="tab"]{transition:background .22s ease,color .22s ease,transform .22s ease}
.stTabs [data-baseweb="tab"]:hover{transform:translateY(-2px)}
[data-testid="stPlotlyChart"]{animation:softIn .65s ease both}
.stButton button,.stDownloadButton button{transition:transform .2s ease,box-shadow .2s ease}
.stButton button:hover,.stDownloadButton button:hover{transform:translateY(-1px);box-shadow:0 7px 18px rgba(84,216,245,.12)}
.kpi-label{color:#9eb0ca;font-size:.69rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.kpi-value{color:#f4f8ff;font-size:1.8rem;font-weight:800;letter-spacing:-.05em;margin:.28rem 0}
.kpi-foot{color:#8295b3;font-size:.68rem}
.section-title{font-size:1.02rem;font-weight:800;color:#edf4ff;margin:1.2rem 0 .2rem}
.section-note{font-size:.78rem;color:#8295b3;margin-bottom:.55rem}
.insight{background:linear-gradient(110deg,rgba(84,216,245,.09),rgba(154,140,255,.09));border:1px solid rgba(128,158,221,.2);border-radius:13px;padding:13px 16px;color:#dce8fa;font-size:.88rem}
.small-muted{color:#8295b3;font-size:.73rem}
.stTabs [data-baseweb="tab-list"]{gap:7px;border-bottom:1px solid var(--line)}
.stTabs [data-baseweb="tab"]{background:#111d30;border-radius:9px 9px 0 0;padding:9px 15px}
.stTabs [aria-selected="true"]{background:#1b2c46!important}
div[data-testid="stMetric"]{background:rgba(29,44,66,.88);border:1px solid var(--line);padding:12px 14px;border-radius:13px}
div[data-testid="stMetricLabel"] p{color:#9eb0ca!important}
div[data-testid="stMetricValue"]{color:#f4f8ff!important}
hr{border-color:var(--line)}
@keyframes rise{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
@keyframes softIn{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(76,224,160,.5)}70%{box-shadow:0 0 0 7px rgba(76,224,160,0)}100%{box-shadow:0 0 0 0 rgba(76,224,160,0)}}
@media(max-width:700px){.hero{padding:1.1rem}.kpi-value{font-size:1.5rem}.block-container{padding-left:1rem;padding-right:1rem}}

/* Layout refinement */
.block-container{padding-top:4.6rem !important;padding-bottom:3rem;max-width:1360px;padding-left:2.2rem;padding-right:2.2rem}
[data-testid="stAppViewContainer"] > .main .block-container{padding-top:4.6rem !important}
[data-testid="stHeader"]{height:3.5rem;background:rgba(17,26,41,.98);z-index:1000}
[data-testid="stToolbar"]{right:1rem;top:.45rem}
[data-testid="stSidebar"] .block-container{padding:1.5rem 1rem}
[data-testid="stSidebar"] [data-testid="stExpander"]{background:rgba(12,22,37,.24);border:1px solid rgba(148,163,184,.14);border-radius:13px}
.hero{padding:1.55rem 1.8rem;margin:0 0 1.1rem;border-radius:22px;box-shadow:0 16px 42px rgba(0,0,0,.12)}
.hero p{color:#c3d0e3;line-height:1.65}
.kpi{border-color:rgba(148,163,184,.17);border-radius:16px;padding:16px 17px;min-height:116px;display:flex;flex-direction:column;justify-content:center}
.section-title{margin:1.55rem 0 .28rem;padding-left:11px;border-left:3px solid rgba(84,216,245,.72)}
.section-note{color:#91a3bd;margin:0 0 .75rem 14px;line-height:1.55}
.stTabs [data-baseweb="tab-list"]{gap:8px;border-bottom:1px solid var(--line);padding:0 0 10px;margin:0 0 1.2rem;flex-wrap:wrap}
.stTabs [data-baseweb="tab"]{background:rgba(26,41,64,.78);border:1px solid rgba(148,163,184,.13);border-radius:11px;padding:10px 17px;margin:0 2px}
.stTabs [aria-selected="true"]{background:linear-gradient(120deg,#24405a,#302e55)!important;border-color:rgba(84,216,245,.36)!important;color:#f5f8ff!important;box-shadow:0 5px 18px rgba(0,0,0,.12)}
[data-testid="stPlotlyChart"]{background:rgba(18,29,46,.42);border:1px solid rgba(148,163,184,.10);border-radius:16px;padding:7px 8px 2px;margin:.25rem 0 .75rem;overflow:hidden}
.masthead{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.2rem 0 1.1rem;margin-bottom:.7rem;border-bottom:1px solid var(--line)}
.masthead-title{font-size:clamp(2rem,4vw,2.8rem);font-weight:800;letter-spacing:-.06em;color:#f4f8ff;line-height:1.12;margin:.3rem 0}
.masthead-subtitle{font-size:.88rem;color:#a8b9d1}
.masthead-status{white-space:nowrap;border:1px solid rgba(76,224,160,.2);background:rgba(76,224,160,.07);padding:9px 13px;border-radius:999px;color:#bcebd7;font:500 .65rem monospace;letter-spacing:.07em}
.filter-strip{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 13px;margin:0 0 1.15rem;background:rgba(25,39,61,.7);border:1px solid var(--line);border-radius:13px;color:#c4d0e3;font-size:.73rem}
.filter-strip span{padding:3px 8px;border-right:1px solid rgba(148,163,184,.16)}
.filter-strip span:last-child{border:0}
.filter-strip b{color:#8fa5c5;font:500 .62rem monospace;letter-spacing:.08em;margin-right:6px}
.filter-strip .filter-hint{margin-left:auto;color:#8295b3}
@media(max-width:900px){.block-container{padding-left:1.2rem;padding-right:1.2rem}.hero{padding:1.25rem}}
@media(max-width:700px){.masthead{align-items:flex-start;flex-direction:column}.masthead-status{align-self:flex-start}.filter-strip .filter-hint{margin-left:0}.hero{padding:1.1rem}.kpi-value{font-size:1.5rem}.block-container{padding-left:1rem;padding-right:1rem}.stTabs [data-baseweb="tab"]{padding:8px 11px;font-size:.82rem}}
:focus-visible{outline:2px solid var(--cyan)!important;outline-offset:3px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    data["Occupancy_Rate"] = (data["Occupancy"] / data["Capacity"] * 100).clip(0, 100)
    data["Time_Slot"] = data["Time"].str.slice(0, 5)
    data["Day_Name"] = data["Date"].dt.day_name()
    return data

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load the bundled dataset: {exc}")
    st.stop()

COLORS = {"Low": "#43d6a0", "Medium": "#f5bd62", "High": "#fa718c"}

def chart_layout(fig, height=330):
    fig.update_layout(
        template="plotly_dark", height=height, margin=dict(l=14, r=14, t=48, b=14),
        transition=dict(duration=650, easing="cubic-in-out"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope", color="#c5d2e5", size=12),
        title_font=dict(color="#f1f5ff", size=15),
        legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1, font=dict(size=10)),
        hoverlabel=dict(bgcolor="#1a2a42", bordercolor="#526783", font_color="#f8fbff", font=dict(size=12)),
        hovermode="closest",
        uirevision="campus-pulse",
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(148,163,184,.22)", tickfont=dict(color="#aebed4"))
    fig.update_yaxes(gridcolor="rgba(148,163,184,.13)", zeroline=False, tickfont=dict(color="#aebed4"))
    return fig

def hero(kicker, title, subtitle, start_date, end_date):
    st.markdown(f"""
    <div class="hero">
      <div class="brand">{kicker}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
      <div class="hero-meta"><span class="dot"></span>SELECTED PERIOD &nbsp;·&nbsp; {start_date:%d %b %Y} — {end_date:%d %b %Y}</div>
    </div>
    """, unsafe_allow_html=True)

def kpi(label, value, foot):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-foot">{foot}</div></div>', unsafe_allow_html=True)

def section(title, note=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="section-note">{note}</div>', unsafe_allow_html=True)

# Global filters live in one compact sidebar expander; page navigation stays in the main canvas.
with st.sidebar:
    st.markdown('<div class="brand">CHRIST UNIVERSITY · MCA 411-2</div>', unsafe_allow_html=True)
    st.markdown("## 🟣 Campus Pulse")
    st.caption("Campus intelligence dashboard")
    st.markdown("---")
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    with st.expander("⚙️ Dashboard filters", expanded=True):
        date_range = st.date_input("Observation period", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        all_locations = sorted(df["Location"].unique())
        locations = st.multiselect("Campus locations", all_locations, default=all_locations)
    st.markdown("---")
    st.markdown('<div class="small-muted">DATASET STATUS</div><div style="margin-top:8px"><span class="dot"></span><b>Bundled dataset ready</b></div>', unsafe_allow_html=True)
    st.caption(f"{len(df):,} observations · {df['Location'].nunique()} illustrative locations")
    st.caption("Synthetic demonstration data — not live university telemetry.")


if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range if isinstance(date_range, date) else min_date

filtered = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Location"].isin(locations))
].copy()

if filtered.empty:
    st.warning("No observations match these filters. Widen the date range or include more locations.")
    st.stop()

avg_occ = filtered["Occupancy_Rate"].mean()
high_share = filtered["Crowd_Level"].eq("High").mean() * 100
busiest = filtered.groupby("Location")["Occupancy_Rate"].mean().idxmax()
total_observations = len(filtered)
selected_location_count = filtered["Location"].nunique()

st.markdown("""
<div class="masthead">
  <div>
    <div class="brand">CHRIST CAMPUS INTELLIGENCE · MCA 411-2</div>
    <div class="masthead-title">Campus Pulse</div>
    <div class="masthead-subtitle">A focused view of campus activity, crowd patterns and shared spaces.</div>
  </div>
  <div class="masthead-status"><span class="dot"></span>DEMO DATASET READY</div>
</div>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class="filter-strip">
  <span><b>PERIOD</b> {start_date:%d %b %Y} — {end_date:%d %b %Y}</span>
  <span><b>LOCATIONS</b> {selected_location_count} selected</span>
  <span><b>READINGS</b> {total_observations:,}</span>
  <span class="filter-hint">Filters available in the sidebar</span>
</div>
""", unsafe_allow_html=True)

pages = st.tabs(["Overview", "Crowd intelligence", "Library", "Cafeteria", "Smart insights"])

# OVERVIEW
with pages[0]:
    hero("CAMPUS INTELLIGENCE / OVERVIEW", "See the pulse of campus.", "A concise snapshot of activity patterns across the selected campus spaces.", start_date, end_date)
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Average occupancy", f"{avg_occ:.2f}%", "Mean capacity utilization")
    with c2: kpi("High-crowd readings", f"{high_share:.2f}%", "Share of selected observations")
    with c3: kpi("Busiest location", busiest, "Highest average utilization")
    with c4: kpi("Locations included", f"{filtered['Location'].nunique()}", "In the current filter")
    section("Activity over time", "Daily average occupancy. Use the legend to focus on individual locations.")
    daily = filtered.groupby(["Date", "Location"], as_index=False)["Occupancy_Rate"].mean()
    fig = px.line(daily, x="Date", y="Occupancy_Rate", color="Location", markers=True)
    fig.update_traces(line=dict(width=2.2), marker=dict(size=4), hovertemplate="%{x|%b %d, %Y}<br>%{fullData.name}: %{y:.2f}%<extra></extra>")
    chart_layout(fig, 350)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with st.expander("Explore the supporting breakdowns"):
        left, right = st.columns(2)
        with left:
            loc = filtered.groupby("Location", as_index=False)["Occupancy_Rate"].mean().sort_values("Occupancy_Rate")
            fig2 = px.bar(loc, x="Occupancy_Rate", y="Location", orientation="h", color="Occupancy_Rate",
                          color_continuous_scale=["#43d6a0", "#54d8f5", "#9a8cff"])
            fig2.update_layout(coloraxis_showscale=False, title="Average capacity utilization")
            fig2.update_traces(hovertemplate="%{y}<br>Average occupancy: %{x:.2f}%<extra></extra>")
            chart_layout(fig2, 300)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        with right:
            mix = filtered["Crowd_Level"].value_counts().reindex(["Low", "Medium", "High"], fill_value=0).rename_axis("Crowd level").reset_index(name="Readings")
            fig3 = px.pie(mix, names="Crowd level", values="Readings", hole=.68, color="Crowd level", color_discrete_map=COLORS)
            fig3.update_traces(textinfo="percent+label", texttemplate="%{label}<br>%{percent:.1%}", hovertemplate="%{label}<br>Readings: %{value:,}<br>Share: %{percent:.1%}<extra></extra>")
            fig3.update_layout(title="Crowd condition mix")
            chart_layout(fig3, 300)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    busiest_value = filtered.loc[filtered["Location"] == busiest, "Occupancy_Rate"].mean()
    st.markdown(f'<div class="insight"><b>Key observation</b> · {busiest} records the highest average utilization in this selection ({busiest_value:.2f}% of its assumed capacity).</div>', unsafe_allow_html=True)

# CROWD INTELLIGENCE
with pages[1]:
    hero("CAMPUS INTELLIGENCE / CROWD", "Understand the movement.", "Compare crowd intensity by place and time without stacking every chart on one screen.", start_date, end_date)
    c1, c2, c3 = st.columns(3)
    with c1: kpi("Average occupancy", f"{avg_occ:.2f}%", "Across selected spaces")
    with c2: kpi("High-crowd readings", f"{high_share:.2f}%", "Of selected observations")
    with c3: kpi("Busiest location", busiest, "Highest mean utilization")
    section("Crowd intensity map", "Average occupancy by location and time slot. Brighter cells indicate fuller spaces.")
    heat = filtered.pivot_table(index="Location", columns="Time_Slot", values="Occupancy_Rate", aggfunc="mean")
    heat = heat.reindex(columns=sorted(heat.columns))
    fig = go.Figure(go.Heatmap(z=heat.values, x=heat.columns, y=heat.index,
        colorscale=[[0, "#163d4b"], [.5, "#4b78a8"], [1, "#c17de2"]],
        colorbar=dict(title="Occupancy %"), hovertemplate="%{y}<br>%{x}<br>Occupancy: %{z:.2f}%<extra></extra>"))
    chart_layout(fig, 370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with st.expander("View crowd-level and occupancy distributions"):
        left, right = st.columns(2)
        with left:
            counts = filtered.groupby(["Location", "Crowd_Level"]).size().reset_index(name="Readings")
            fig2 = px.bar(counts, x="Location", y="Readings", color="Crowd_Level", barmode="stack", color_discrete_map=COLORS)
            fig2.update_layout(title="Crowd-level readings by location", xaxis_tickangle=-20)
            fig2.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y:,} readings<extra></extra>")
            chart_layout(fig2, 310)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        with right:
            fig3 = px.box(filtered, x="Location", y="Occupancy_Rate", color="Location", points="outliers")
            fig3.update_layout(title="Occupancy spread", showlegend=False)
            fig3.update_traces(hovertemplate="%{x}<br>Occupancy: %{y:.2f}%<extra></extra>")
            chart_layout(fig3, 310)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# LIBRARY — dedicated analytics workspace
with pages[2]:
    hero("CAMPUS INTELLIGENCE / LIBRARY", "A better view of study spaces.", "Understand when the library is busiest, how seating changes, and which periods tend to be quieter.", start_date, end_date)
    library = filtered[filtered["Location"] == "Central Library"].copy()
    if library.empty:
        st.warning("Central Library is excluded by the current location filter. Add it in Dashboard filters to view library analytics.")
    else:
        avg_library = library["Occupancy_Rate"].mean()
        mean_seats = library["Available_Seats"].mean()
        peak_row = library.loc[library["Occupancy_Rate"].idxmax()]
        capacity = library["Capacity"].iloc[0]
        peak_slot = peak_row["Time_Slot"]
        k1, k2, k3, k4 = st.columns(4)
        with k1: kpi("Average occupancy", f"{avg_library:.2f}%", "Of assumed library capacity")
        with k2: kpi("Average seats free", f"{mean_seats:.1f}", "Estimated seats per reading")
        with k3: kpi("Peak occupancy", f"{library['Occupancy_Rate'].max():.2f}%", f"Highest reading · {peak_slot}")
        with k4: kpi("Assumed capacity", f"{capacity:,}", "Illustrative dataset value")

        usage_tab, seats_tab, detail_tab = st.tabs(["Study-hour patterns", "Seating & capacity", "Daily breakdown"])

        with usage_tab:
            section("When is the library busiest?", "Average occupancy for each time slot across the selected dates.")
            by_time = library.groupby("Time_Slot", as_index=False).agg(
                Occupancy=("Occupancy_Rate", "mean"),
                Free_Seats=("Available_Seats", "mean"),
            )
            peak_time = by_time.loc[by_time["Occupancy"].idxmax()]
            quiet_time = by_time.loc[by_time["Occupancy"].idxmin()]
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f'<div class="insight"><b>Busiest average slot</b><br>{peak_time["Time_Slot"]} · {peak_time["Occupancy"]:.2f}% occupancy</div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="insight"><b>Quietest average slot</b><br>{quiet_time["Time_Slot"]} · {quiet_time["Occupancy"]:.2f}% occupancy</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=by_time["Time_Slot"], y=by_time["Occupancy"], mode="lines+markers",
                line=dict(color="#54d8f5", width=3), marker=dict(size=9, color="#9a8cff"),
                fill="tozeroy", fillcolor="rgba(84,216,245,.10)", name="Average occupancy",
                hovertemplate="%{x}<br>Average occupancy: %{y:.2f}%<extra></extra>"))
            fig.update_layout(yaxis_title="Occupancy (%)", xaxis_title="Time slot", yaxis_range=[0, 100], yaxis_tickformat=".2f")
            chart_layout(fig, 330)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            section("Weekly rhythm", "This heatmap compares the average library occupancy across weekdays and time slots.")
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekly = library.pivot_table(index="Day_Name", columns="Time_Slot", values="Occupancy_Rate", aggfunc="mean")
            weekly = weekly.reindex(index=[d for d in weekday_order if d in weekly.index], columns=sorted(weekly.columns))
            fig_week = go.Figure(go.Heatmap(z=weekly.values, x=weekly.columns, y=weekly.index,
                colorscale=[[0, "#163d4b"], [.5, "#4b78a8"], [1, "#c17de2"]],
                colorbar=dict(title="Occupancy %"), hovertemplate="%{y}<br>%{x}<br>Occupancy: %{z:.2f}%<extra></extra>"))
            chart_layout(fig_week, 300)
            st.plotly_chart(fig_week, use_container_width=True, config={"displayModeBar": False})

        with seats_tab:
            section("Are seats available?", "Track estimated free seats and the proportion of capacity currently in use.")
            daily_seats = library.groupby("Date", as_index=False).agg(
                Free_Seats=("Available_Seats", "mean"),
                Occupancy=("Occupancy_Rate", "mean"),
            )
            left, right = st.columns(2)
            with left:
                fig_seats = px.area(daily_seats, x="Date", y="Free_Seats")
                fig_seats.update_traces(line_color="#54d8f5", fillcolor="rgba(84,216,245,.14)", hovertemplate="Date=%{x|%b %d, %Y}<br>Estimated free seats: %{y:.1f}<extra></extra>")
                fig_seats.update_layout(title="Average available seats per day", yaxis_title="Available seats")
                chart_layout(fig_seats, 320)
                st.plotly_chart(fig_seats, use_container_width=True, config={"displayModeBar": False})
            with right:
                fig_occ = px.line(daily_seats, x="Date", y="Occupancy", markers=True)
                fig_occ.update_traces(line_color="#9a8cff", line_width=3, hovertemplate="Date=%{x|%b %d, %Y}<br>Occupancy: %{y:.2f}%<extra></extra>")
                fig_occ.update_layout(title="Daily capacity utilization", yaxis_title="Occupancy (%)", yaxis_range=[0, 100])
                chart_layout(fig_occ, 320)
                st.plotly_chart(fig_occ, use_container_width=True, config={"displayModeBar": False})
            st.caption("Seat counts and capacity are illustrative estimates from the bundled synthetic dataset.")

        with detail_tab:
            section("Daily library readings", "A compact table for reviewing each date and time slot.")
            detail = library.groupby(["Date", "Day_Name", "Time_Slot"], as_index=False).agg(
                Occupancy=("Occupancy_Rate", "mean"),
                Available_Seats=("Available_Seats", "mean"),
                Crowd_Level=("Crowd_Level", lambda s: s.mode().iloc[0]),
            )
            detail = detail.rename(columns={"Date": "Date", "Day_Name": "Day", "Time_Slot": "Time",
                "Occupancy": "Occupancy (%)", "Available_Seats": "Estimated free seats", "Crowd_Level": "Typical crowd level"})
            st.dataframe(detail.round({"Occupancy (%)": 2, "Estimated free seats": 2}),
                use_container_width=True, hide_index=True)
            st.download_button("Download library summary (CSV)", detail.to_csv(index=False).encode("utf-8"),
                file_name="campus_pulse_library_summary.csv", mime="text/csv")

# CAFETERIA
with pages[3]:
    hero("CAMPUS INTELLIGENCE / CAFETERIA", "Find a calmer queue.", "Review estimated waiting times and identify recurring cafeteria rush periods.", start_date, end_date)
    cafe = filtered[filtered["Location"] == "Cafeteria"].copy()
    if cafe.empty:
        st.warning("Cafeteria is excluded by the current location filter. Add it in Dashboard filters to view cafeteria analytics.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1: kpi("Average wait", f"{cafe['Waiting_Time_Min'].mean():.1f} min", "Estimated queue duration")
        with c2: kpi("Peak wait", f"{cafe['Waiting_Time_Min'].max():.1f} min", "Maximum estimated wait")
        with c3: kpi("Average occupancy", f"{cafe['Occupancy_Rate'].mean():.2f}%", "Of assumed cafeteria capacity")
        section("Queue pattern by time", "Compare average waiting time with occupancy for each time slot.")
        wait = cafe.groupby("Time_Slot", as_index=False).agg(Wait=("Waiting_Time_Min", "mean"), Occupancy=("Occupancy_Rate", "mean"))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=wait["Time_Slot"], y=wait["Wait"], name="Wait (minutes)", marker_color="#9a8cff"))
        fig.add_trace(go.Scatter(x=wait["Time_Slot"], y=wait["Occupancy"], name="Occupancy (%)", mode="lines+markers",
            yaxis="y2", line=dict(color="#54d8f5", width=3)))
        fig.update_layout(yaxis=dict(title="Wait (min)", tickformat=".1f"), yaxis2=dict(title="Occupancy (%)", overlaying="y", side="right", showgrid=False, tickformat=".2f"))
        fig.update_traces(hovertemplate="%{x}<br>Average wait: %{y:.1f} min<extra></extra>", selector=dict(type="bar"))
        fig.update_traces(hovertemplate="%{x}<br>Average occupancy: %{y:.2f}%<extra></extra>", selector=dict(type="scatter"))
        chart_layout(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with st.expander("View daily waiting-time trend"):
            daily_wait = cafe.groupby("Date", as_index=False)["Waiting_Time_Min"].mean()
            fig2 = px.area(daily_wait, x="Date", y="Waiting_Time_Min")
            fig2.update_traces(line_color="#ec83d2", fillcolor="rgba(236,131,210,.14)", hovertemplate="Date=%{x|%b %d, %Y}<br>Waiting_Time_Min=%{y:.1f}<extra></extra>")
            fig2.update_layout(title="Average estimated wait by day")
            fig2.update_yaxes(tickformat=".1f")
            chart_layout(fig2, 300)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# SMART INSIGHTS
with pages[4]:
    hero("CAMPUS INTELLIGENCE / HISTORICAL BASELINE", "Anticipate busy windows.", "A transparent estimate of typical occupancy by location and time slot, based on the selected historical period.", start_date, end_date)
    st.markdown('<div class="insight"><b>Method note</b> · These are historical averages, not a trained machine-learning model or a live prediction. Treat them as an exploratory baseline.</div>', unsafe_allow_html=True)
    forecast = filtered.groupby(["Location", "Time_Slot"], as_index=False).agg(
        Expected_Occupancy=("Occupancy_Rate", "mean"),
        Expected_Wait=("Waiting_Time_Min", "mean"))
    forecast = forecast.sort_values("Expected_Occupancy", ascending=False)

    # Compact, filter-aware findings make the baseline useful before reading the chart.
    busiest_combo = forecast.loc[forecast["Expected_Occupancy"].idxmax()]
    longest_wait = forecast.loc[forecast["Expected_Wait"].idxmax()]
    busiest_slot = (forecast.groupby("Time_Slot")["Expected_Occupancy"].mean()
                    .sort_values(ascending=False).index[0])
    insight_cols = st.columns(3)
    with insight_cols[0]:
        kpi("Busiest combination", busiest_combo["Location"], f"{busiest_combo['Time_Slot']} · {busiest_combo['Expected_Occupancy']:.2f}%")
    with insight_cols[1]:
        kpi("Longest estimated wait", f"{longest_wait['Expected_Wait']:.1f} min", f"{longest_wait['Location']} · {longest_wait['Time_Slot']}")
    with insight_cols[2]:
        slot_mean = forecast.loc[forecast["Time_Slot"] == busiest_slot, "Expected_Occupancy"].mean()
        kpi("Busiest average time", busiest_slot, f"{slot_mean:.2f}% mean occupancy")

    section("Highest-occupancy location and time combinations", "Only time slots represented in the displayed results are shown, in chronological order.")
    top = forecast.head(10).sort_values("Expected_Occupancy")
    # Build the facet order from the displayed rows only: omit absent time slots
    # and keep the remaining HH:MM values in true clock order.
    time_slot_order = sorted(top["Time_Slot"].dropna().unique(), key=lambda value: pd.to_datetime(value, format="%H:%M").time())
    fig = px.bar(top, x="Expected_Occupancy", y="Location", color="Expected_Occupancy", orientation="h",
        facet_col="Time_Slot", facet_col_wrap=3, category_orders={"Time_Slot": time_slot_order},
        color_continuous_scale=["#43d6a0", "#54d8f5", "#9a8cff"], custom_data=["Expected_Wait"])
    fig.update_layout(coloraxis_showscale=False)
    fig.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.replace("Time_Slot=", "")))
    fig.update_traces(hovertemplate="%{y}<br>Average occupancy: %{x:.2f}%<br>Average wait: %{customdata[0]:.1f} min<extra></extra>")
    chart_layout(fig, 490)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with st.expander("Open the complete historical baseline table"):
        display = forecast.rename(columns={"Location": "Campus location", "Time_Slot": "Time",
            "Expected_Occupancy": "Average occupancy (%)", "Expected_Wait": "Average wait (min)"})
        st.dataframe(display.round(2), use_container_width=True, hide_index=True)

st.markdown("---")
left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="small-muted">CHRIST CAMPUS PULSE · MCA PYTHON PROGRAMMING · MCA411-2</div>', unsafe_allow_html=True)
    st.caption("Independent academic prototype using synthetic demonstration data. Not affiliated with or endorsed by CHRIST University.")
with right:
    st.caption(f"{total_observations:,} filtered observations")
