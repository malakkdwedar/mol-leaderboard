import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

# Wrap the client + sheet opening in a cached function
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # replace with your actual sheet ID
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

# Use the cached sheet object everywhere else in your app
sheet = get_sheet()

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🟡", layout="wide")

# --- Title ---
st.markdown("<h1 style='text-align:center; color: yellow;'>🟡 Pac-Man Leaderboard 🟡</h1>", unsafe_allow_html=True)

# --- Authenticate Google Sheets via Streamlit Secrets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# --- Open the sheet ---
SHEET_NAME = "Scoreboard"  # <-- Replace with your Google Sheet name
SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # <-- your actual Sheet ID
sheet = client.open_by_key(SHEET_KEY).sheet1

# --- Fetch data ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Placeholder if sheet is empty ---
if df.empty:
    df = pd.DataFrame({
        "Team": ["Team A", "Team B", "Team C", "Team D"],
        "Score": [0, 0, 0, 0],
        "Color": ["#FFD700", "#FF6347", "#00BFFF", "#32CD32"],  # Gold, Tomato, DeepSkyBlue, LimeGreen
        "Icon": ["🟡", "👻", "🍒", "⭐"]
    })

# --- Sort by Score descending ---
df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

# --- Function to apply row colors ---
def color_rows(row):
    return [f'background-color: {row.Color}; color: black; font-weight:bold' if col in ["Team", "Score", "Icon"] else '' for col in df.columns]

# --- Display leaderboard ---
st.markdown("<h3 style='text-align:center; color: white;'>Current Scores</h3>", unsafe_allow_html=True)
st.dataframe(df.style.apply(color_rows, axis=1), height=400)

# --- Footer ---
st.markdown("<p style='text-align:center; color: white;'>🍒 Keep munching those points! 🍒</p>", unsafe_allow_html=True)
