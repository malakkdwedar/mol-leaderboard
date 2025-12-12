import streamlit as st
import pandas as pd
import gspread
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🟡", layout="wide")

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="leaderboard_refresh")

# --- Title ---
st.markdown("<h1 style='text-align:center; color: yellow; text-shadow: 2px 2px 10px #FFFF00;'>🟡 Pac-Man Leaderboard 🟡</h1>", unsafe_allow_html=True)

# --- Cached sheet ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # replace with your sheet ID
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

sheet = get_sheet()

# --- Fetch leaderboard ---
def fetch_leaderboard(sheet):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    if df.empty:
        df = pd.DataFrame({
            "team": ["Team A", "Team B", "Team C", "Team D"],
            "score": [0, 0, 0, 0],
            "icon": ["🟡", "👻", "🍒", "⭐"]
        })
    
    df.columns = df.columns.str.lower()
    df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return df

df = fetch_leaderboard(sheet)

# --- Style rows with top 3 highlighting ---
def style_rows(row):
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # gold, silver, bronze
    row_color = colors[row.name] if row.name < 3 else "rgba(0,0,0,0.6)"  # semi-transparent black for others
    return [f'background-color: {row_color}; color: white; font-weight:bold; text-align:center' if col in ["team", "score", "icon"] else '' for col in df.columns]

# --- Video background ---
# Save your video as "pacman_maze.mp4" in the same folder as app.py
st.markdown("""
<style>
.video-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
    opacity: 0.7;  /* adjust for readability */
}
</style>

<video class="video-bg" autoplay muted loop>
  <source src="pacman_maze.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# --- Leaderboard container (semi-transparent) ---
st.markdown("""
<div style="
    background-color: rgba(0, 0, 0, 0.5);  /* semi-transparent overlay */
    padding: 20px;
    border-radius: 15px;
">
""", unsafe_allow_html=True)

# --- Display leaderboard ---
st.markdown("<h3 style='text-align:center; color: white; text-shadow: 1px 1px 5px #00FFFF;'>Current Scores</h3>", unsafe_allow_html=True)
st.dataframe(df.style.apply(style_rows, axis=1), height=400)

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p style='text-align:center; color: white; text-shadow: 1px 1px 5px #FF00FF;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
