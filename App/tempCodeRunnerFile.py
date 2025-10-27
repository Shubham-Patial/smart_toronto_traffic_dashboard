import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- File path ---
DATA_PATH = "C:/Users/shubh/Desktop/smart_toronto_traffic_dashboard/Data/combined.csv"

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # --- Fix datetime ---
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # --- Fix AUTOMOBILE column ---
    if "AUTOMOBILE" in df.columns:
        df["AUTOMOBILE"] = pd.to_numeric(df["AUTOMOBILE"], errors="coerce")
        if df["AUTOMOBILE"].isna().all():
            df["AUTOMOBILE"] = (
                df["AUTOMOBILE"]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "yes": 1, "y": 1, "true": 1, "1": 1,
                    "no": 0, "n": 0, "false": 0, "0": 0
                })
                .fillna(0)
            )

    # --- Create hour & day_of_week if missing ---
    if "hour" not in df.columns and "datetime" in df.columns:
        df["hour"] = df["datetime"].dt.hour
    if "day_of_week" not in df.columns and "datetime" in df.columns:
        df["day_of_week"] = df["datetime"].dt.day_name()

    # Fill missing categorical columns to avoid issues
    for col in ["weather_condition", "NEIGHBOURHOOD_140", "injury_severity", "vehicle_category"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


# --- Load ---
data = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

# Date range filter
if "datetime" in data.columns:
    min_date, max_date = data["datetime"].min().date(), data["datetime"].max().date()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
else:
    date_range = []

# Dropdown filters
day_options = sorted(data["day_of_week"].dropna().unique()) if "day_of_week" in data.columns else []
weather_options = sorted(data["weather_condition"].dropna().unique()) if "weather_condition" in data.columns else []
vehicle_options = sorted(data["vehicle_category"].dropna().unique()) if "vehicle_category" in data.columns else []
hood_options = sorted(data["NEIGHBOURHOOD_140"].dropna().unique()) if "NEIGHBOURHOOD_140" in data.columns else []

selected_days = st.sidebar.multiselect("Select Day(s) of Week", day_options)
selected_weather = st.sidebar.multiselect("Select Weather Condition(s)", weather_options)
selected_vehicle = st.sidebar.multiselect("Select Vehicle Category", vehicle_options)
selected_hood = st.sidebar.multiselect("Select Neighbourhood(s)", hood_options)

# --- Filtering logic ---
filtered = data.copy()

if len(date_range) == 2 and "datetime" in filtered.columns:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["datetime"].dt.date >= start_date)
        & (filtered["datetime"].dt.date <= end_date)
    ]

if selected_days:
    filtered = filtered[filtered["day_of_week"].isin(selected_days)]

if selected_weather:
    filtered = filtered[filtered["weather_condition"].isin(selected_weather)]

if selected_vehicle:
    filtered = filtered[filtered["vehicle_category"].isin(selected_vehicle)]

if selected_hood:
    filtered = filtered[filtered["NEIGHBOURHOOD_140"].isin(selected_hood)]

# --- Dashboard Header ---
st.title("🚦 Smart Toronto Traffic Dashboard")

# --- Check filtered data ---
if filtered.empty:
    st.warning("⚠️ No records match your selected filters. Try clearing one or more filters.")
    st.stop()
else:
    st.success(f"✅ Showing {len(filtered)} records after filtering.")

# --- KPIs ---
total_records = len(filtered)
unique_neighbourhoods = filtered["NEIGHBOURHOOD_140"].nunique() if "NEIGHBOURHOOD_140" in filtered.columns else 0
peak_hour = int(filtered["hour"].mode()[0]) if not filtered.empty and "hour" in filtered.columns else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", total_records)
col2.metric("Peak Hour", peak_hour)
col3.metric("Unique Neighbourhoods", unique_neighbourhoods)

# --- Charts ---

# 1️⃣ Crashes by Hour
if "hour" in filtered.columns:
    hourly = filtered.groupby("hour").size().reset_index(name="count")
    fig1 = px.line(hourly, x="hour", y="count", title="Crashes by Hour of Day")
    st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Injury Severity Distribution
if "injury_severity" in filtered.columns:
    injury_counts = filtered["injury_severity"].value_counts().reset_index()
    injury_counts.columns = ["Injury Severity", "Count"]
    fig2 = px.bar(injury_counts, x="Injury Severity", y="Count", title="Injury Severity Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Crashes by Weather
if "weather_condition" in filtered.columns:
    weather_counts = filtered["weather_condition"].value_counts().reset_index()
    weather_counts.columns = ["Weather Condition", "Count"]
    fig3 = px.bar(weather_counts, x="Weather Condition", y="Count", title="Crashes by Weather Condition")
    st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Top Neighbourhoods
if "NEIGHBOURHOOD_140" in filtered.columns:
    top_hoods = filtered["NEIGHBOURHOOD_140"].value_counts().reset_index().head(15)
    top_hoods.columns = ["Neighbourhood", "Count"]
    fig4 = px.bar(top_hoods, x="Neighbourhood", y="Count", title="Top 15 Neighbourhoods by Collisions")
    st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Temperature vs Crashes
if "temperature" in filtered.columns:
    temp_group = filtered.groupby("temperature").size().reset_index(name="count")
    fig5 = px.line(temp_group, x="temperature", y="count", title="Temperature vs Collision Count")
    st.plotly_chart(fig5, use_container_width=True)

# 6️⃣ Accident Map (optional)
if {"latitude", "longitude"}.issubset(filtered.columns):
    map_df = filtered.dropna(subset=["latitude", "longitude"])
    if not map_df.empty:
        fig6 = px.scatter_mapbox(
            map_df,
            lat="latitude",
            lon="longitude",
            color="weather_condition" if "weather_condition" in map_df.columns else None,
            hover_data=["NEIGHBOURHOOD_140", "datetime"],
            title="📍 Accident Locations Map",
            zoom=9,
            height=500,
        )
        fig6.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig6, use_container_width=True)

# --- Insights ---
st.markdown("### 💡 Key Insights")

insights = []

if "hour" in filtered.columns:
    insights.append(f"🕒 Peak traffic occurs around **{peak_hour}:00** hours.")
if "weather_condition" in filtered.columns:
    rainy = filtered[filtered["weather_condition"].str.contains("rain", case=False, na=False)]
    if not rainy.empty:
        rain_ratio = len(rainy) / len(filtered) * 100
        insights.append(f"🌧️ About **{rain_ratio:.1f}%** of accidents occur during rainy weather.")
if "temperature" in filtered.columns:
    avg_temp = filtered["temperature"].mean()
    insights.append(f"🌡️ The average temperature during incidents is **{avg_temp:.1f}°C**.")

if not insights:
    st.info("No insights available for the current filters.")
else:
    for item in insights:
        st.markdown(item)

# --- Footer ---
st.markdown("---")
st.caption(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("📘 Data Source: City of Toronto Traffic / Weather Data")
