import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

# --- Cache the Google Sheet connection ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # Your sheet ID
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

sheet = get_sheet()

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🟡", layout="wide")

# --- Background + glowing + animations ---
st.markdown(
    """
    <style>
        .stApp {
            background-color: #1a002b;  /* Deep dark purple */
            color: white;
        }

        /* ---- ANIMATED GLOW TITLE ---- */
        .glow-title {
            text-align: center;
            font-size: 52px;
            font-weight: bold;
            color: #ffea00;
            animation: pulseGlow 2s infinite;
        }

        @keyframes pulseGlow {
            0% { text-shadow: 0 0 8px #ffea00; }
            50% { text-shadow: 0 0 22px #ffea00; }
            100% { text-shadow: 0 0 8px #ffea00; }
        }

        /* ---- FLOATING GHOSTS ---- */
        .ghost-container {
            text-align: center;
            margin-top: -20px;
            margin-bottom: 10px;
        }

        .ghost {
            font-size: 40px;
            display: inline-block;
            margin: 0px 25px;
            animation: floatGhost 3.5s ease-in-out infinite;
        }

        .ghost:nth-child(2) { animation-delay: 0.7s; }
        .ghost:nth-child(3) { animation-delay: 1.4s; }
        .ghost:nth-child(4) { animation-delay: 2.1s; }

        @keyframes floatGhost {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
            100% { transform: translateY(0px); }
        }

        /* Subtext glow */
        .subglow {
            text-align: center;
            font-size: 22px;
            color: #ffffff;
            text-shadow: 0 0 8px #9933ff;
        }

        /* Gold / Silver / Bronze rows */
        .gold {
            background-color: #FFD70022 !important;
            color: #FFD700 !important;
            font-weight: bold;
        }
        .silver {
            background-color: #C0C0C022 !important;
            color: #C0C0C0 !important;
            font-weight: bold;
        }
        .bronze {
            background-color: #CD7F3222 !important;
            color: #CD7F32 !important;
            font-weight: bold;
        }

        table tbody tr td {
            text-align: center !important;
            font-size: 18px;
        }
        table thead tr th {
            text-align: center !important;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.markdown("<h1 class='glow-title'>🕹️👾 Pac-Man Leaderboard 🕹️👾</h1>", unsafe_allow_html=True)

# --- Floating ghosts under the title ---
st.markdown(
    """
    <div class='ghost-container'>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<p class='subglow'>Top teams updated live during the LGD!</p>", unsafe_allow_html=True)

# --- Fetch data ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Default teams for empty sheet
if df.empty:
    df = pd.DataFrame({
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "score": [0, 0, 0, 0],
        "icon": ["🟡", "👻", "🍒", "⭐"]
    })

# Sort
df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

# Color top 3
def highlight_row(row):
    if row.name == 0:
        return ['gold'] * len(row)
    elif row.name == 1:
        return ['silver'] * len(row)
    elif row.name == 2:
        return ['bronze'] * len(row)
    else:
        return [''] * len(row)

styled_df = df.style.apply(highlight_row, axis=1)

# Show table
st.dataframe(styled_df, height=450)

# Footer
st.markdown("<p class='subglow'>🍒 Keep scoring — power pellets await! 🍒</p>", unsafe_allow_html=True)
