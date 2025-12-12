import streamlit as st
import pandas as pd
import gspread
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🟡", layout="wide")

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="leaderboard_refresh")

# --- Full-page background image CSS ---
st.markdown("""
<style>
body {
    background-image: url("https://i.pinimg.com/1200x/9f/c9/93/9fc99302c35961da24f02dcf74fc854d.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.leaderboard-container {
    background-color: rgba(0,0,0,0.6);  /* semi-transparent overlay */
    padding: 20px;
    border-radius: 15px;
    width: 60%;
    margin: 50px auto;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='color: yellow; text-shadow: 2px 2px 10px #FFFF00;'>🟡 Pac-Man Leaderboard 🟡</h1>", unsafe_allow_html=True)

# --- Cached Google Sheet connection ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # replace with your Sheet ID
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
    
    # normalize column names
    df.columns = df.columns.str.lower()
    df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return df

df = fetch_leaderboard(sheet)

# --- Style leaderboard rows ---
def style_rows(row):
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
    row_color = colors[row.name] if row.name < 3 else "rgba(0,0,0,0.6)"
    return [f'background-color: {row_color}; color: white; font-weight:bold; text-align:center' if col in df.columns else '' for col in df.columns]

# --- Floating leaderboard container ---
st.markdown('<div class="leaderboard-container">', unsafe_allow_html=True)

st.markdown("<h3 style='color: white; text-shadow: 1px 1px 5px #00FFFF;'>Current Scores</h3>", unsafe_allow_html=True)
st.dataframe(df.style.apply(style_rows, axis=1), height=400)

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p style='text-align:center; color: white; text-shadow: 1px 1px 5px #FF00FF;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
