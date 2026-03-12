import streamlit as st
from pymongo import MongoClient
import pandas as pd
import time
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Industrial Monitor",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- CUSTOM UI STYLE ----------------
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

.main-title{
text-align:center;
font-size:45px;
font-weight:bold;
color:#00e5ff;
margin-bottom:5px;
}

.sub-title{
text-align:center;
font-size:18px;
color:#d0d0d0;
margin-bottom:30px;
}

.metric-card{
background:rgba(255,255,255,0.05);
backdrop-filter: blur(8px);
padding:25px;
border-radius:12px;
border:1px solid rgba(255,255,255,0.1);
text-align:center;
box-shadow:0px 0px 15px rgba(0,255,255,0.2);
}

.metric-value{
font-size:35px;
font-weight:bold;
color:#00ffff;
}

.metric-label{
font-size:16px;
color:#cccccc;
}

.status-normal{
background:linear-gradient(90deg,#00b09b,#96c93d);
padding:18px;
border-radius:10px;
text-align:center;
font-size:22px;
font-weight:bold;
color:white;
box-shadow:0px 0px 15px rgba(0,255,100,0.5);
}

.status-fault{
background:linear-gradient(90deg,#ff416c,#ff4b2b);
padding:18px;
border-radius:10px;
text-align:center;
font-size:22px;
font-weight:bold;
color:white;
box-shadow:0px 0px 15px rgba(255,0,0,0.5);
}

.section-title{
font-size:24px;
margin-top:25px;
margin-bottom:10px;
color:#00e5ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>⚙ AI MACHINE HEALTH MONITOR</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Real-Time Industrial Predictive Maintenance System</div>", unsafe_allow_html=True)

# ---------------- DATABASE CONNECTION ----------------
# Replace 'atlas-xxxx-shard-0' with your actual replica set name from MongoDB Atlas
client = MongoClient(
    "mongodb://Vomkar:vomkar123@cluster0-shard-00-00.s58phda.mongodb.net:27017,"
    "cluster0-shard-00-01.s58phda.mongodb.net:27017,"
    "cluster0-shard-00-02.s58phda.mongodb.net:27017/"
    "peditrix?ssl=true&replicaSet=atlas-0abcde-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = client["ai_machine"]
collection = db["sensor_data"]

data = list(collection.find().sort("timestamp",-1).limit(100))

# ---------------- DASHBOARD ----------------
if len(data) > 0:

    df = pd.DataFrame(data)
    latest = df.iloc[0]

    st.markdown("<div class='section-title'>📊 Machine Metrics</div>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-value">{latest['temperature']} °C</div>
        <div class="metric-label">Temperature</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-value">{latest['vibration']}</div>
        <div class="metric-label">Vibration</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-value">{latest['health_score']}%</div>
        <div class="metric-label">Health Score</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- STATUS ----------------
    st.markdown("<div class='section-title'>🔍 Machine Status</div>", unsafe_allow_html=True)

    if latest["status"] == "FAULT":
        st.markdown("<div class='status-fault'>⚠ MACHINE FAULT DETECTED</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-normal'>✅ MACHINE OPERATING NORMALLY</div>", unsafe_allow_html=True)

    # ---------------- ATTRACTIVE PLOTS ----------------
    st.markdown("<div class='section-title'>📈 Sensor Analytics</div>", unsafe_allow_html=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Temperature Chart
    temp_fig = px.line(
        df,
        x="timestamp",
        y="temperature",
        title="Temperature Monitoring",
        markers=True
    )

    temp_fig.update_layout(
        template="plotly_dark",
        title_font_size=22,
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        plot_bgcolor="#0f2027",
        paper_bgcolor="#0f2027"
    )

    st.plotly_chart(temp_fig, use_container_width=True)

    # Vibration Chart
    vib_fig = px.line(
        df,
        x="timestamp",
        y="vibration",
        title="Vibration Monitoring",
        markers=True
    )

    vib_fig.update_layout(
        template="plotly_dark",
        title_font_size=22,
        xaxis_title="Time",
        yaxis_title="Vibration Level",
        plot_bgcolor="#0f2027",
        paper_bgcolor="#0f2027"
    )

    st.plotly_chart(vib_fig, use_container_width=True)

    # Health Score Chart
    health_fig = px.area(
        df,
        x="timestamp",
        y="health_score",
        title="Machine Health Score"
    )

    health_fig.update_layout(
        template="plotly_dark",
        title_font_size=22,
        xaxis_title="Time",
        yaxis_title="Health %",
        plot_bgcolor="#0f2027",
        paper_bgcolor="#0f2027"
    )

    st.plotly_chart(health_fig, use_container_width=True)

    # ---------------- LOG TABLE ----------------
    st.markdown("<div class='section-title'>📄 Machine Logs</div>", unsafe_allow_html=True)

    st.dataframe(
        df[["temperature","vibration","status","health_score","timestamp"]],
        use_container_width=True
    )

else:

    st.warning("Waiting for ESP32 sensor data...")

    col1,col2,col3 = st.columns(3)

    col1.metric("Temperature","0 °C")
    col2.metric("Vibration","0")
    col3.metric("Health Score","0 %")

# ---------------- AUTO REFRESH ----------------
time.sleep(5)
st.rerun()
