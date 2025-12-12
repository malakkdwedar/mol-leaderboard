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
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"
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
    row_color = colors[row.name] if row.name < 3 else "#111111"
    return [f'background-color: {row_color}; color: white; font-weight:bold; text-align:center' if col in ["team", "score", "icon"] else '' for col in df.columns]

# --- CSS for theme & animations ---
st.markdown("""
<style>
body {
    background-color: #000000;
    background-image: url('https://i.imgur.com/Jt2I1Yg.png'); /* Pac-Man maze */
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    color: white;
    overflow-x: hidden;
}

/* Ghosts */
.ghost {
    font-size: 2rem;
    position: absolute;
    animation: ghostMove 8s linear infinite;
}

/* Different ghost colors & heights */
.blinky { color: red; top: 15%; animation-delay: 0s; }
.pinky { color: pink; top: 35%; animation-delay: 1s; }
.inky { color: cyan; top: 55%; animation-delay: 2s; }
.clyde { color: orange; top: 75%; animation-delay: 3s; }

/* Pac-Man */
.pacman {
    font-size: 2.5rem;
    color: yellow;
    text-shadow: 0 0 20px #FFFF00;
    position: absolute;
    top: 45%;
    animation: pacMove 6s linear infinite;
}

/* Moving dots */
.dot {
    font-size: 1rem;
    position: absolute;
    color: white;
    text-shadow: 0 0 10px #FFFF00;
    animation: dotMove 10s linear infinite;
}

/* Animations */
@keyframes ghostMove {
    0% { left: -10%; }
    50% { left: 50%; }
    100% { left: 110%; }
}

@keyframes pacMove {
    0% { left: -10%; }
    50% { left: 50%; }
    100% { left: 110%; }
}

@keyframes dotMove {
    0% { left: -5%; }
    100% { left: 105%; }
}
</style>
""", unsafe_allow_html=True)

# --- Animated overlay ---
st.markdown("""
<div class='pacman'>🟡</div>
<div class='ghost blinky'>👻</div>
<div class='ghost pinky'>👻</div>
<div class='ghost inky'>👻</div>
<div class='ghost clyde'>👻</div>

<!-- Moving dots -->
<div class='dot' style='top:10%; animation-delay:0s;'>•</div>
<div class='dot' style='top:30%; animation-delay:2s;'>•</div>
<div class='dot' style='top:50%; animation-delay:4s;'>•</div>
<div class='dot' style='top:70%; animation-delay:6s;'>•</div>
<div class='dot' style='top:90%; animation-delay:8s;'>•</div>
""", unsafe_allow_html=True)

# --- Display leaderboard ---
st.markdown("<h3 style='text-align:center; color: white; text-shadow: 1px 1px 5px #00FFFF;'>Current Scores</h3>", unsafe_allow_html=True)
st.dataframe(df.style.apply(style_rows, axis=1), height=400)

# --- Footer ---
st.markdown("<p style='text-align:center; color: white; text-shadow: 1px 1px 5px #FF00FF;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
