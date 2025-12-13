st.markdown("""
<style>
/* Remove Streamlit default padding */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Hide Streamlit menu & footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import gspread
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🕹️", layout="wide")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# --- Cached Google Sheet connection ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"
    return client.open_by_key(SHEET_KEY).sheet1

try:
    sheet = get_sheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except Exception:
    # Fallback data if sheet fails
    df = pd.DataFrame({
        "team": ["Team A", "Team B", "Team C"],
        "score": [120, 95, 80],
        "icon": ["🟡", "👻", "🍒"]
    })

# Normalize + sort
df.columns = df.columns.str.lower()
if "score" in df.columns:
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.stApp {
    background-color: #1a0028 !important;
    color: white;
}

/* Pixel glowing title */
.glow-title {
    font-family: 'Press Start 2P', cursive;
    font-size: 50px;
    color: #ffea00;
    text-align: center;
    margin-bottom: 20px;
    animation: pulse 2.3s infinite;
}
@keyframes pulse {
    0% { text-shadow: 0 0 6px #ffea00; }
    50% { text-shadow: 0 0 32px #ffea00; }
    100% { text-shadow: 0 0 6px #ffea00; }
}

/* Ghost animations */
.ghost-container {
    text-align: center;
    margin-top: -5px;
    margin-bottom: 20px;
}
.ghost {
    font-size: 50px;
    margin: 0 20px;
    display: inline-block;
    animation: floaty 3s ease-in-out infinite;
}
.ghost:nth-child(2) { animation-delay: 0.4s; }
.ghost:nth-child(3) { animation-delay: 0.8s; }
.ghost:nth-child(4) { animation-delay: 1.2s; }

@keyframes floaty {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

/* Pixel subtext */
.subtext {
    font-family: 'Press Start 2P', cursive;
    text-align: center;
    font-size: 24px;
    color: #ffb7ff;
    margin-bottom: 25px;
    text-shadow: 0 0 12px #9b4bff;
}

/* Pixel-style table */
.pixel-table {
    font-family: 'Press Start 2P', cursive;
    font-size: 30px;
    text-align: center;
    width: 100%;
    border-collapse: collapse;
}
.pixel-table th, .pixel-table td {
    padding: 14px;
    border: 3px solid #ffea00;
}
.pixel-table th {
    background-color: #ffea00;
    color: #1a0028;
}
.pixel-table td {
    color: #ffffff;
}

/* Top 3 row colors */
.top1 { background-color: rgba(255,215,0,0.5); color: #FFD700; font-weight:bold; }
.top2 { background-color: rgba(192,192,192,0.5); color: #C0C0C0; font-weight:bold; }
.top3 { background-color: rgba(205,127,50,0.5); color: #CD7F32; font-weight:bold; }

</style>
""", unsafe_allow_html=True)

# ---------- TITLE & GHOSTS & SUBTEXT ----------
st.markdown('<div class="glow-title">🕹️👾 Pac-Man Leaderboard 🕹️👾</div>', unsafe_allow_html=True)
st.markdown("""
<div class='ghost-container'>
    <span class='ghost'>👻</span>
    <span class='ghost'>👻</span>
    <span class='ghost'>👻</span>
    <span class='ghost'>👻</span>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtext">TOP TEAMS UPDATED LIVE DURING THE LGD!</div>', unsafe_allow_html=True)

# ---------- BUILD HTML TABLE ----------
table_html = "<table class='pixel-table'><thead><tr><th>Rank</th><th>Team</th><th>Score</th><th>Icon</th></tr></thead><tbody>"
for i, row in df.iterrows():
    cls = ""
    if i == 0: cls = "top1"
    elif i == 1: cls = "top2"
    elif i == 2: cls = "top3"
    table_html += f"<tr class='{cls}'><td>{i+1}</td><td>{row['team']}</td><td>{row['score']}</td><td>{row['icon']}</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown('<div class="subtext">🍒 Keep scoring! 🍒</div>', unsafe_allow_html=True)
