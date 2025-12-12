import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MOL LGD Live Leaderboard",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- TITLE ---
st.markdown(
    "<h1 style='text-align: center; color: #FFCC00; font-family: monospace;'>"
    "🎮 MOL METABOLIC MAZE — LIVE LEADERBOARD 🎮</h1>",
    unsafe_allow_html=True
)

# --- AUTO REFRESH EVERY 3 SECONDS ---
st_autorefresh = st.experimental_rerun

# --- LOAD GOOGLE SHEET ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXL1MUBynMkoACJNX5O1aXJznbUP36M6RWunBPWI78tRyLq13tXNnSkAqkhz0pHOzcs6yDfnBcnp_l/pub?output=csv"
df = pd.read_csv(sheet_url)

# --- SORT BY SCORE ---
df = df.sort_values(by="score", ascending=False)

# --- STYLE THE TABLE ---
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
         color:white;'
    >
        <span>{icon} {team}</span>
        <span style='color:{color}; font-size:28px;'>{score}</span>
    </div>
    """

html = ""
for _, row in df.iterrows():
    html += make_row(row["team"], row["score"], row["color"], row["icon"])

st.markdown(html, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(
    "<p style='text-align:center; color:#666; font-family: monospace;'>"
    "Scores update automatically every few seconds."
    "</p>",
    unsafe_allow_html=True
)
