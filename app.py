import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

# Wrap the client + sheet opening in a cached function
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # Replace with your actual sheet ID
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

# Use the cached sheet object everywhere else in your app
sheet = get_sheet()

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="👾", layout="wide")

# --- Page styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2c003e;  /* Dark purple */
        color: white;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.markdown("<h1 class='title'>👾🕹️ Pac-Man Leaderboard 🕹️👾</h1>", unsafe_allow_html=True)

# --- Fetch data ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Placeholder if sheet is empty ---
if df.empty:
    df = pd.DataFrame({
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "score": [0, 0, 0, 0],
        "icon": ["🟡", "👻", "🍒", "⭐"]
    })

# --- Sort by Score descending ---
df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

# --- Display leaderboard ---
st.markdown("<h3 style='text-align:center;'>Current Scores</h3>", unsafe_allow_html=True)
st.dataframe(df.style.set_properties(**{
    'text-align': 'center',
    'font-weight': 'bold'
}), height=400)

# --- Footer ---
st.markdown("<p style='text-align:center;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
