import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import date

# ------------------------------------------------------------
# CHRIST CAMPUS PULSE | Smart campus crowd analytics dashboard
# All values are synthetic demonstration data from the bundled CSV.
# ------------------------------------------------------------
st.set_page_config(
    page_title="Campus Pulse | CHRIST University",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "data" / "christ_campus_pulse_data.csv"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --bg:#080d19; --panel:#101a2b; --panel2:#142238; --line:rgba(148,163,184,.15); --muted:#91a2bd; --text:#edf4ff; --cyan:#54d8f5; --violet:#9a8cff; --pink:#ec83d2; }
html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
.stApp { background: radial-gradient(ellipse at 12% 0%, rgba(65,91,180,.18), transparent 34%), radial-gradient(ellipse at 90% 12%, rgba(127,77,194,.14), transparent 30%), var(--bg); color:var(--text); }
[data-testid="stHeader"] { background:rgba(8,13,25,.72); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101a2b,#0b1322); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#dce7fa; }
.block-container { padding-top:1.6rem; padding-bottom:3rem; max-width:1500px; }
h1,h2,h3 { color:var(--text)!important; letter-spacing:-.035em; }
p, label, .stMarkdown { color:#c4d0e3; }
.pulse-eyebrow { color:var(--cyan); font:500 .72rem 'DM Mono',monospace; letter-spacing:.19em; text-transform:uppercase; }
.hero { padding:1.55rem 1.7rem; border:1px solid rgba(127,155,210,.22); border-radius:22px; background:linear-gradient(115deg,rgba(26,43,72,.94),rgba(19,27,49,.82) 55%,rgba(55,36,81,.72)); box-shadow:0 18px 55px rgba(0,0,0,.22); position:relative; overflow:hidden; animation:rise .65s ease both; }
.hero:after { content:''; position:absolute; width:260px;height:260px;right:-65px;top:-145px;border-radius:50%;border:1px solid rgba(84,216,245,.25);box-shadow:0 0 0 28px rgba(84,216,245,.025),0 0 0 58px rgba(154,140,255,.025); }
.hero h1 { font-size:clamp(2rem,4vw,3.35rem); font-weight:800; margin:.25rem 0 .35rem; }
.hero p { color:#b9c8df; max-width:760px; margin:0; }
.live-dot { display:inline-block;width:8px;height:8px;border-radius:50%;background:#4ce0a0;margin-right:8px;box-shadow:0 0 0 0 rgba(76,224,160,.65);animation:pulse 1.8s infinite; }
.kpi { background:linear-gradient(145deg,rgba(22,36,59,.96),rgba(15,25,43,.96)); border:1px solid var(--line); border-radius:17px; padding:17px 18px 15px; min-height:124px; position:relative; overflow:hidden; animation:rise .55s ease both; transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease; }
.kpi:hover { transform:translateY(-4px); border-color:rgba(84,216,245,.42); box-shadow:0 12px 30px rgba(0,0,0,.22); }
.kpi:before { content:'';position:absolute;inset:0 auto 0 0;width:3px;background:linear-gradient(180deg,var(--cyan),var(--violet)); }
.kpi-label { color:#9eb0ca;font-size:.75rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase; }
.kpi-value { color:#f4f8ff;font-size:2rem;font-weight:800;letter-spacing:-.06em;margin:.35rem 0 .1rem; }
.kpi-foot { color:#8295b3;font-size:.72rem; }
.section-head { display:flex;align-items:center;gap:10px;margin:1.25rem 0 .7rem;color:#eef4ff;font-weight:800;font-size:1.12rem; }
.section-head:before { content:'';width:4px;height:19px;border-radius:9px;background:linear-gradient(var(--cyan),var(--violet)); }
.panel { background:rgba(16,26,43,.78);border:1px solid var(--line);border-radius:18px;padding:16px 18px; }
.insight { background:linear-gradient(110deg,rgba(84,216,245,.10),rgba(154,140,255,.10));border:1px solid rgba(128,158,221,.22);border-radius:15px;padding:15px 17px;color:#dce8fa; }
.small-muted { color:#8295b3;font-size:.78rem; }
div[data-testid="stMetric"] { background:rgba(16,26,43,.78);border:1px solid var(--line);padding:14px 16px;border-radius:15px; }
div[data-testid="stMetricLabel"] p { color:#9eb0ca!important; }
div[data-testid="stMetricValue"] { color:#f4f8ff!important; }
.stSelectbox label,.stMultiSelect label,.stDateInput label { color:#b9c8df!important;font-weight:700; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#121e31;border-radius:10px 10px 0 0;padding:9px 15px; }
hr { border-color:var(--line); }
@keyframes rise { from { opacity:0;transform:translateY(12px) } to { opacity:1;transform:translateY(0) } }
@keyframes pulse { 0% { box-shadow:0 0 0 0 rgba(76,224,160,.55) } 70% { box-shadow:0 0 0 8px rgba(76,224,160,0) } 100% { box-shadow:0 0 0 0 rgba(76,224,160,0) } }
@media(max-width:700px){.hero{padding:1.2rem}.kpi-value{font-size:1.6rem}.block-container{padding-left:1rem;padding-right:1rem}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    data["Occupancy_Rate"] = (data["Occupancy"] / data["Capacity"] * 100).clip(0, 100)
    data["Hour"] = data["Time"].str.slice(0, 2).astype(int)
    data["Time_Slot"] = data["Time"].str.slice(0, 5)
    return data

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load the bundled dataset: {exc}")
    st.stop()

COLORS = {"Low":"#43d6a0","Medium":"#f5bd62","High":"#fa718c"}
CHART_TEMPLATE = "plotly_dark"

def chart_layout(fig, height=340):
    fig.update_layout(
        template=CHART_TEMPLATE, height=height, margin=dict(l=8,r=8,t=34,b=8),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope", color="#b9c8df", size=11),
        title_font=dict(color="#edf4ff", size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="#142238", bordercolor="#526783", font_color="#fff"),
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(148,163,184,.12)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.10)", zeroline=False)
    return fig

# Sidebar controls
with st.sidebar:
    st.markdown('<div class="pulse-eyebrow">CHRIST UNIVERSITY · MCA 411-2</div>', unsafe_allow_html=True)
    st.markdown("## 🟣 Campus Pulse")
    st.caption("Smart campus intelligence")
    page = st.radio("NAVIGATION", ["Campus Overview","Crowd Intelligence","Library Analytics","Cafeteria Analytics","Smart Insights"], label_visibility="visible")
    st.markdown("---")
    st.markdown("### FILTER DATA")
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input("Observation period", value=(min_date,max_date), min_value=min_date, max_value=max_date)
    locations = st.multiselect("Campus locations", sorted(df["Location"].unique()), default=sorted(df["Location"].unique()))
    st.markdown("---")
    st.markdown('<div class="small-muted">DATASET STATUS</div><div style="margin-top:8px"><span class="live-dot"></span><b>Local dataset loaded</b></div>', unsafe_allow_html=True)
    st.caption(f"{len(df):,} observations · {df['Location'].nunique()} locations")
    st.caption("Synthetic demonstration dataset · Not official university telemetry")

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range if isinstance(date_range, date) else min_date

filtered = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date) &
    (df["Location"].isin(locations))
].copy()

if filtered.empty:
    st.warning("No observations match these filters. Select a wider date range or more locations.")
    st.stop()

avg_occ = filtered["Occupancy_Rate"].mean()
avg_wait = filtered.loc[filtered["Location"]=="Cafeteria","Waiting_Time_Min"].mean()
avg_wait = 0 if pd.isna(avg_wait) else avg_wait
high_share = (filtered["Crowd_Level"].eq("High").mean() * 100)
total_observations = len(filtered)
busiest = filtered.groupby("Location")["Occupancy_Rate"].mean().idxmax()
free_seats = int(filtered.groupby(["Date","Time","Location"])["Available_Seats"].sum().mean())

def hero(kicker, title, subtitle):
    st.markdown(f"""
    <div class="hero">
      <div class="pulse-eyebrow">{kicker}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
      <div style="margin-top:17px;font-size:.75rem;color:#8fa5c5"><span class="live-dot"></span>ANALYTICS VIEW &nbsp;·&nbsp; {start_date:%d %b %Y} — {end_date:%d %b %Y}</div>
    </div>""", unsafe_allow_html=True)

def kpi(label, value, foot, symbol):
    st.markdown(f"""<div class="kpi"><div class="kpi-label">{symbol} &nbsp; {label}</div><div class="kpi-value">{value}</div><div class="kpi-foot">{foot}</div></div>""", unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-head">{text}</div>', unsafe_allow_html=True)

def empty_note(text):
    st.info(text)

if page == "Campus Overview":
    hero("CAMPUS INTELLIGENCE / OVERVIEW", "See the pulse of campus.", "A consolidated view of activity patterns across campus spaces, built from a curated demonstration dataset.")
    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Avg. occupancy", f"{avg_occ:.0f}%", "Mean capacity utilization", "◉")
    with c2: kpi("High-crowd readings", f"{high_share:.0f}%", "Share of observations marked high", "↗")
    with c3: kpi("Cafeteria wait", f"{avg_wait:.0f} min", "Average estimated queue time", "◷")
    with c4: kpi("Locations tracked", f"{filtered['Location'].nunique()}", "Campus zones in this view", "⌖")
    section("Campus activity timeline")
    daily = filtered.groupby(["Date","Location"],as_index=False)["Occupancy_Rate"].mean()
    fig = px.line(daily,x="Date",y="Occupancy_Rate",color="Location",markers=True,title="Average occupancy by location · daily trend")
    fig.update_traces(line=dict(width=2.5),marker=dict(size=5))
    chart_layout(fig,370)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    left,right = st.columns([1.05,.95])
    with left:
        section("Where activity concentrates")
        loc = filtered.groupby("Location",as_index=False).agg(Occupancy=("Occupancy_Rate","mean"),People=("Occupancy","mean"))
        fig2 = px.bar(loc.sort_values("Occupancy"),x="Occupancy",y="Location",orientation="h",color="Occupancy",color_continuous_scale=["#43d6a0","#54d8f5","#9a8cff"],text=loc.sort_values("Occupancy")["Occupancy"].map(lambda x:f"{x:.0f}%"),title="Average capacity utilization")
        chart_layout(fig2,320); fig2.update_layout(coloraxis_showscale=False); fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
    with right:
        section("Crowd mix")
        mix = filtered["Crowd_Level"].value_counts().reindex(["Low","Medium","High"],fill_value=0).reset_index()
        mix.columns=["Crowd level","Readings"]
        fig3 = px.pie(mix,names="Crowd level",values="Readings",hole=.68,color="Crowd level",color_discrete_map=COLORS,title="Distribution of crowd conditions")
        fig3.update_traces(textposition="outside",textinfo="percent+label")
        chart_layout(fig3,320)
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})
    st.markdown(f'<div class="insight"><b>Pulse insight</b> · {busiest} has the highest average occupancy in the selected period at {filtered[filtered["Location"]==busiest]["Occupancy_Rate"].mean():.0f}% of assumed capacity.</div>',unsafe_allow_html=True)

elif page == "Crowd Intelligence":
    hero("CAMPUS INTELLIGENCE / CROWD", "Understand the movement.", "Compare crowd intensity across campus zones and discover when spaces are most active.")
    c1,c2,c3 = st.columns(3)
    with c1: kpi("Avg. occupancy",f"{avg_occ:.0f}%","Across selected locations","◉")
    with c2: kpi("High crowd",f"{high_share:.0f}%","Of all selected readings","↗")
    with c3: kpi("Busiest location",busiest,"Highest mean utilization","⌖")
    section("Crowd intensity heatmap")
    heat = filtered.pivot_table(index="Location",columns="Time_Slot",values="Occupancy_Rate",aggfunc="mean").reindex(columns=sorted(filtered["Time_Slot"].unique()))
    fig = go.Figure(data=go.Heatmap(z=heat.values,x=heat.columns,y=heat.index,colorscale=[[0,"#163d4b"],[.5,"#4b78a8"],[1,"#c17de2"]],colorbar=dict(title="Occupancy %"),hovertemplate="%{y}<br>%{x}<br>%{z:.1f}%<extra></extra>"))
    fig.update_layout(title="Average occupancy by location and time slot")
    chart_layout(fig,390)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    left,right = st.columns(2)
    with left:
        section("Crowd level by location")
        counts = filtered.groupby(["Location","Crowd_Level"]).size().reset_index(name="Readings")
        fig2=px.bar(counts,x="Location",y="Readings",color="Crowd_Level",barmode="stack",color_discrete_map=COLORS,title="Reading distribution")
        chart_layout(fig2,330); fig2.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
    with right:
        section("Occupancy distribution")
        fig3=px.box(filtered,x="Location",y="Occupancy_Rate",color="Location",points="outliers",title="Spread of capacity utilization")
        chart_layout(fig3,330); fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

elif page == "Library Analytics":
    hero("CAMPUS INTELLIGENCE / LIBRARY", "Make room for focus.", "Explore estimated library utilization, available seating and recurring study-hour patterns.")
    library = filtered[filtered["Location"]=="Central Library"].copy()
    if library.empty:
        empty_note("Central Library is not included in the selected locations. Add it using the sidebar filter.")
    else:
        lc1,lc2,lc3=st.columns(3)
        with lc1: kpi("Avg. occupancy",f"{library['Occupancy_Rate'].mean():.0f}%","Estimated capacity utilization","◉")
        with lc2: kpi("Avg. free seats",f"{library['Available_Seats'].mean():.0f}","Estimated seats available per reading","▦")
        with lc3: kpi("Peak observed",f"{library['Occupancy_Rate'].max():.0f}%","Highest single occupancy reading","↗")
        section("Library occupancy through the day")
        hourly=library.groupby(["Time_Slot","Date"],as_index=False)["Occupancy_Rate"].mean()
        fig=px.line(hourly,x="Time_Slot",y="Occupancy_Rate",color="Date",line_group="Date",title="Daily occupancy profiles · select a date in the legend")
        fig.update_traces(line=dict(width=1.4),opacity=.45)
        chart_layout(fig,350)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        section("Seat availability trend")
        seats=library.groupby("Date",as_index=False)["Available_Seats"].mean()
        fig2=px.area(seats,x="Date",y="Available_Seats",title="Estimated average available seats by day")
        fig2.update_traces(line_color="#54d8f5",fillcolor="rgba(84,216,245,.16)")
        chart_layout(fig2,300)
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

elif page == "Cafeteria Analytics":
    hero("CAMPUS INTELLIGENCE / FOOD & BEVERAGE", "Beat the lunch rush.", "Review estimated cafeteria queues, waiting times and recurring peak periods.")
    cafe=filtered[filtered["Location"]=="Cafeteria"].copy()
    if cafe.empty:
        empty_note("Cafeteria is not included in the selected locations. Add it using the sidebar filter.")
    else:
        cc1,cc2,cc3=st.columns(3)
        with cc1: kpi("Avg. wait",f"{cafe['Waiting_Time_Min'].mean():.0f} min","Estimated queue duration","◷")
        with cc2: kpi("Peak wait",f"{cafe['Waiting_Time_Min'].max():.0f} min","Maximum in selected period","↗")
        with cc3: kpi("Avg. occupancy",f"{cafe['Occupancy_Rate'].mean():.0f}%","Estimated cafeteria utilization","◉")
        section("Queue pattern by time")
        wait=cafe.groupby("Time_Slot",as_index=False).agg(Wait=("Waiting_Time_Min","mean"),Occupancy=("Occupancy_Rate","mean"))
        fig=go.Figure()
        fig.add_trace(go.Bar(x=wait["Time_Slot"],y=wait["Wait"],name="Wait (minutes)",marker_color="#9a8cff"))
        fig.add_trace(go.Scatter(x=wait["Time_Slot"],y=wait["Occupancy"],name="Occupancy (%)",mode="lines+markers",yaxis="y2",line=dict(color="#54d8f5",width=3)))
        fig.update_layout(title="Average queue time and occupancy by time slot",yaxis=dict(title="Wait (min)"),yaxis2=dict(title="Occupancy (%)",overlaying="y",side="right",showgrid=False))
        chart_layout(fig,360)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        section("Daily waiting-time movement")
        daily_wait=cafe.groupby("Date",as_index=False)["Waiting_Time_Min"].mean()
        fig2=px.area(daily_wait,x="Date",y="Waiting_Time_Min",title="Average estimated wait by day")
        fig2.update_traces(line_color="#ec83d2",fillcolor="rgba(236,131,210,.14)")
        chart_layout(fig2,300)
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

elif page == "Smart Insights":
    hero("CAMPUS INTELLIGENCE / FORECAST", "See the next busy window.", "A transparent baseline forecast derived from historical average occupancy by location and time slot.")
    st.markdown('<div class="insight"><b>How this works</b> · This is a historical-pattern estimate, not a trained machine-learning model or a live forecast. It averages the selected period by location and time slot.</div>',unsafe_allow_html=True)
    section("Expected busy windows")
    forecast=filtered.groupby(["Location","Time_Slot"],as_index=False).agg(Expected_Occupancy=("Occupancy_Rate","mean"),Expected_Wait=("Waiting_Time_Min","mean"))
    forecast=forecast.sort_values("Expected_Occupancy",ascending=False)
    top=forecast.head(12)
    fig=px.bar(top.sort_values("Expected_Occupancy"),x="Expected_Occupancy",y="Location",color="Expected_Occupancy",orientation="h",facet_col="Time_Slot",facet_col_wrap=3,color_continuous_scale=["#43d6a0","#54d8f5","#9a8cff"],title="Highest historical occupancy windows")
    fig.update_layout(height=560,coloraxis_showscale=False)
    chart_layout(fig,560)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    section("Time-slot ranking")
    ranked=forecast.groupby("Time_Slot",as_index=False)["Expected_Occupancy"].mean().sort_values("Expected_Occupancy",ascending=False)
    fig2=px.bar(ranked,x="Time_Slot",y="Expected_Occupancy",color="Expected_Occupancy",color_continuous_scale=["#163d4b","#54d8f5","#9a8cff"],title="Campus-wide average utilization by time")
    chart_layout(fig2,300); fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
    st.dataframe(forecast.rename(columns={"Location":"Campus location","Time_Slot":"Time","Expected_Occupancy":"Expected occupancy (%)","Expected_Wait":"Expected wait (min)"}).round(1),use_container_width=True,hide_index=True)

st.markdown("---")
left,right=st.columns([3,1])
with left:
    st.markdown('<div class="small-muted">CHRIST CAMPUS PULSE · MCA PYTHON PROGRAMMING · MCA411-2</div>',unsafe_allow_html=True)
    st.caption("Academic prototype using synthetic demonstration data. Not affiliated with or endorsed by CHRIST University.")
with right:
    st.caption(f"Showing {total_observations:,} filtered observations")
