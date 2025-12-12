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
    background-color: #1a0028 !important;   /* Dark purple */
    color: white;
}

/* Pixel glowing title */
.glow-title {
    font-family: 'Press Start 2P', cursive;
    font-size: 48px;
    color: #ffea00;
    text-align: center;
    margin-bottom: 10px;
    animation: pulse 2.3s infinite;
}
@keyframes pulse {
    0% { text-shadow: 0 0 6px #ffea00; }
    50% { text-shadow: 0 0 22px #ffea00; }
    100% { text-shadow: 0 0 6px #ffea00; }
}

/* Ghost animations */
.ghost-container {
    text-align: center;
    margin-top: -5px;
    margin-bottom: 15px;
}
.ghost {
    font-size: 60px;
    margin: 0 15px;
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
    margin-bottom: 20px;
    text-shadow: 0 0 10px #9b4bff;
}

/* Pixel-style DataFrame */
[data-testid="stDataFrame"] table {
    font-family: 'Press Start 2P', cursive;
    font-size: 32px !important;
    text-align: center;
}
[data-testid="stDataFrame"] table th {
    text-align: center !important;
    font-size: 36px !important;
}
[data-testid="stDataFrame"] table td {
    text-align: center !important;
    font-size: 32px !important;
}

/* Make table container wider */
[data-testid="stDataFrame"] div.row-widget.stDataFrame {
    width: 100% !important;
}
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

# ---------- TOP-3 ROW COLORS ----------
def style_top3(row):
    if row.name == 0:
        return ['background-color: rgba(255,215,0,0.3); color: #FFD700; font-weight:bold;'] * len(row)
    if row.name == 1:
        return ['background-color: rgba(192,192,192,0.3); color: #C0C0C0; font-weight:bold;'] * len(row)
    if row.name == 2:
        return ['background-color: rgba(205,127,50,0.3); color: #CD7F32; font-weight:bold;'] * len(row)
    return ['background-color: rgba(255,255,255,0.05); color: white;'] * len(row)

styled_df = df.style.apply(style_top3, axis=1)

# ---------- DISPLAY LEADERBOARD ----------
st.dataframe(styled_df, use_container_width=True, height=500)

# ---------- FOOTER ----------
st.markdown('<div class="subtext" style="margin-top:30px;">🍒 Keep scoring! 🍒</div>', unsafe_allow_html=True)
