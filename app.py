import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Debug: check loaded secrets
st.write("Available secret keys:", st.secrets.keys())

# Load your GCP service account from Streamlit secrets
try:
    creds_dict = st.secrets["gcp_service_account"]
    st.write("Service account loaded:", creds_dict['client_email'])
except KeyError:
    st.error("Secret 'gcp_service_account' not found!")
    st.stop()

# Define the scopes required for Sheets and Drive access
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    # Create credentials object from secret
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

    # Authorize gspread client
    client = gspread.authorize(creds)
    st.success("gspread client authorized!")

    # Replace with your sheet name
    SHEET_NAME = "Your Sheet Name Here"
    sheet = client.open(SHEET_NAME).sheet1
    st.success(f"Opened sheet: {SHEET_NAME}")

    # Fetch first row for testing
    first_row = sheet.row_values(1)
    st.write("First row of sheet:", first_row)

except Exception as e:
    st.error("Failed to connect to Google Sheet!")
    st.error(e)
    
import streamlit as st

# Debug: check which secrets are loaded
st.write(st.secrets.keys())  # Should show ['gcp_service_account']

# Debug: check that your JSON is correctly parsed
creds_dict = st.secrets["gcp_service_account"]
st.write(creds_dict['client_email'])
import streamlit as st

st.title("Debug Streamlit Secrets 🔍")

# List all available secret keys
st.write("Available secret keys:", list(st.secrets.keys()))

# Try to access your specific key
try:
    creds = st.secrets["gcp_service_account"]
    st.success("✅ Found 'gcp_service_account' secret!")
    st.json(creds)  # Displays the contents safely (except for private_key)
except KeyError:
    st.error("❌ 'gcp_service_account' secret not found!")
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="refresh")

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
sheet = client.open(SHEET_NAME).sheet1

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
