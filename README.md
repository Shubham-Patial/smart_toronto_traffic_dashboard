# 🚦 Smart Toronto Traffic Dashboard

**Author:** Shubham [Your Last Name]  
**Last Updated:** October 2025  

An interactive Streamlit dashboard analyzing Toronto’s traffic collision data — uncovering how **weather, time, and location** influence road safety and congestion.

---

## 🧭 Overview

This dashboard allows users to explore traffic collision patterns across the City of Toronto.  
You can filter by **day of week, weather condition, vehicle type**, and **neighbourhood**, and visualize:

- Crash counts by hour of day  
- Weather and injury severity impacts  
- Top neighbourhoods by collision frequency  
- Relationship between temperature and crashes  

The dashboard provides a **data-driven understanding of urban traffic safety**, helping planners, policy-makers, and residents identify high-risk conditions and areas.

---

## 🗃️ Data Sources

1. **City of Toronto Open Data Portal** — [Collision Data](https://open.toronto.ca/dataset/collision-data/)  
2. **Environment Canada** — https://openweathermap.org/  

All data were cleaned and combined into `combined.csv` using preprocessing scripts, then optionally stored in an SQLite database (`traffic.db`) for efficient querying.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Data Visualization** | Plotly Express |
| **Data Handling** | Pandas |
| **Database (optional)** | SQLite |
| **Deployment** | Streamlit Cloud |

---

## ⚙️ How to Run the App

### 🪟 Local Setup

1️⃣ Clone or download the project
git clone https://github.com/Shubham-Patial/smart_toronto_traffic_dashboard.git
cd smart_toronto_traffic_dashboard

2️⃣ Install dependencies

Create a virtual environment (optional) and install:

pip install -r requirements.txt

3️⃣ Run Streamlit
streamlit run app/dashboard.py

4️⃣ Open in your browser
http://localhost:8501

🗂️ **Project Structure**

smart_toronto_traffic_dashboard/
├── app/ 📁
│ └── dashboard.py 📝 ← Main Streamlit app
├── Data/ 📁
│ └── combined.csv 📊 ← Cleaned dataset
├── Database/ 📁
│ └── traffic.db 💾 ← SQLite (optional)
├── screenshots/ 📁 ← Optional app images
├── requirements.txt 📄
└── README.md 📄    

📈 Key Insights (Example Findings)

🚗 Peak collisions occur between 8 AM and 6 PM (typical rush hours).

🌧️ Rain and snow conditions increase accident rates by ~25–30 %.

🏙️ Downtown neighbourhoods have the highest collision density.

🌡️ Extreme temperatures (below 0 °C or above 30 °C) correlate with higher injury severity.

Actual insights depend on filter selection and latest data.