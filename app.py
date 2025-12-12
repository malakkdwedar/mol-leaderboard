import streamlit as st
import pandas as pd
import gspread
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🟡", layout="wide")

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="leaderboard_refresh")

# --- Floating leaderboard container with Pac-Man maze background ---
st.markdown("""
<div style="
    background-image: url('https://i.pinimg.com/1200x/9f/c9/93/9fc99302c35961da24f02dcf74fc854d.jpg');
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    padding: 40px;
    width: 70%;
    margin: 50px auto;
    text-align: center;
    box-shadow: 0 0 40px rgba(255,255,0,0.8);
">
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='color: yellow; text-shadow: 3px 3px 15px #FFFF00;'>🟡 Pac-Man Leaderboard 🟡</h1>", unsafe_allow_html=True)

# --- Google Sheet connection ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # Replace with your Sheet ID
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

sheet = get_sheet()

# --- Fetch leaderboard data ---
def fetch_leaderboard(sheet):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    if df.empty:
        # Placeholder if sheet is empty
        df = pd.DataFrame({
            "team": ["Team A", "Team B", "Team C", "Team D"],
            "score": [0, 0, 0, 0],
            "icon": ["🟡", "👻", "🍒", "⭐"]
        })
    
    # Normalize column names
    df.columns = df.columns.str.lower()
    df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return df

df = fetch_leaderboard(sheet)

# --- Style leaderboard rows ---
def style_rows(row):
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
    row_color = colors[row.name] if row.name < 3 else "rgba(0,0,0,0.6)"
    return [f'background-color: {row_color}; color: white; font-weight:bold; text-align:center; font-size:18px;' if col in df.columns else '' for col in df.columns]

# --- Display leaderboard ---
st.dataframe(df.style.apply(style_rows, axis=1), height=400)

# --- Close container div ---
st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p style='text-align:center; color: white; text-shadow: 2px 2px 8px #FF00FF; font-size:20px;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
