import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MOL LGD Live Leaderboard",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- AUTO REFRESH EVERY 3 SECONDS ---
st_autorefresh(interval=3000, key="leaderboard")

# --- GOOGLE SHEETS AUTH ---
# Replace "service_account.json" with your JSON key file name
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("digital-waters-481012-b4-8107df41d97d.json
", scope)
client = gspread.authorize(creds)

# --- LOAD SHEET ---
# Replace "Leaderboard" with the exact name of your Google Sheet
sheet = client.open("Scoreboard").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- SORT BY SCORE DESCENDING ---
df = df.sort_values(by="score", ascending=False)

# --- PAGE TITLE ---
st.markdown(
    "<h1 style='text-align:center; color:#FFCC00; font-family: monospace;'>"
    "🎮 MOL METABOLIC MAZE — LIVE LEADERBOARD 🎮</h1>",
    unsafe_allow_html=True
)

# --- FUNCTION TO CREATE PAC-MAN STYLE ROWS ---
def make_row(team, score, color, icon):
    return f"""
    <div style='
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:12px 20px;
        margin-bottom:10px;
        background-color:#111;
        border-left:8px solid {color};
        border-radius:10px;
        font-family: monospace;
        font-size:24px;
        color:white;
        box-shadow: 0 0 10px {color};
        transition: all 0.3s ease;
    '>
        <span>{icon} {team}</span>
        <span style='color:{color}; font-size:28px;'>{score}</span>
    </div>
    """

# --- BUILD HTML FOR LEADERBOARD ---
html = ""
for _, row in df.iterrows():
    html += make_row(row["team"], row["score"], row["color"], row["icon"])

# --- DISPLAY THE LEADERBOARD ---
st.markdown(html, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(
    "<p style='text-align:center; color:#666; font-family: monospace;'>"
    "Scores update automatically every 3 seconds!</p>",
    unsafe_allow_html=True
)
