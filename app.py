# app.py
import streamlit as st
import pandas as pd
import gspread
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Pac-Man Leaderboard", page_icon="🕹️", layout="wide")

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=5000, key="leaderboard_refresh")

# --- Cached Google Sheet connection ---
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"  # <- replace if needed
    sheet = client.open_by_key(SHEET_KEY).sheet1
    return sheet

# Try to get sheet; if there's a problem, we'll fall back to placeholder data
try:
    sheet = get_sheet()
except Exception:
    sheet = None
    st.warning("Couldn't connect to Google Sheets — showing placeholder data.")

# ----------------- Styling block (font, title glow, ghosts, container) -----------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        /* App background color (page) */
        .stApp {
            background-color: #120019;  /* deep purple page background */
            color: white;
        }

        /* Floating container (this holds the maze background and the leaderboard) */
        .leaderboard-container {
            background-image: url('https://i.pinimg.com/1200x/9f/c9/93/9fc99302c35961da24f02dcf74fc854d.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 18px;
            padding: 28px;
            width: 80%;
            margin: 36px auto;
            text-align: center;
            box-shadow: 0 0 40px rgba(255, 200, 0, 0.12);
            backdrop-filter: blur(3px);
        }

        /* Press Start 2P pixel title with pulsing glow */
        .glow-title {
            font-family: 'Press Start 2P', cursive;
            font-size: 44px;
            color: #ffea00;
            margin: 6px 0 6px 0;
            animation: pulseGlow 2.2s infinite;
        }
        @keyframes pulseGlow {
            0% { text-shadow: 0 0 6px #ffea00; }
            50% { text-shadow: 0 0 26px #ffea00; }
            100% { text-shadow: 0 0 6px #ffea00; }
        }

        /* Ghosts under title (floating) */
        .ghost-container {
            text-align: center;
            margin-top: -6px;
            margin-bottom: 6px;
        }
        .ghost {
            font-size: 40px;
            display: inline-block;
            margin: 0 18px;
            animation: floatGhost 3.4s ease-in-out infinite;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.06));
        }
        .ghost:nth-child(2) { animation-delay: 0.6s; }
        .ghost:nth-child(3) { animation-delay: 1.2s; }
        .ghost:nth-child(4) { animation-delay: 1.8s; }
        @keyframes floatGhost {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        /* Pixel-style subtext and footer */
        .subglow {
            font-family: 'Press Start 2P', cursive;
            font-size: 20px;
            color: #ffffff;
            text-shadow: 0 0 10px #9933ff;
            margin: 6px 0 14px 0;
        }
        .footer-text {
            font-family: 'Press Start 2P', cursive;
            font-size: 20px;
            color: #ffea00;
            text-shadow: 0 0 12px #ffea00;
            margin-top: 14px;
            margin-bottom: 6px;
        }

        /* Make pandas/st.dataframe table text centered and larger */
        div[data-testid="stDataFrameContainer"] table tbody tr td {
            text-align: center !important;
            font-size: 16px !important;
            vertical-align: middle !important;
        }
        div[data-testid="stDataFrameContainer"] table thead tr th {
            text-align: center !important;
            font-size: 16px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Container start -----------------
st.markdown('<div class="leaderboard-container">', unsafe_allow_html=True)

# Title + ghosts + subtext
st.markdown("<div class='glow-title'>🕹️👾 Pac-Man Leaderboard 🕹️👾</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='ghost-container'>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
        <span class='ghost'>👻</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<div class='subglow'>TOP TEAMS UPDATED LIVE DURING THE LGD!</div>", unsafe_allow_html=True)

# ----------------- Fetch and prepare data -----------------
if sheet is not None:
    try:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
    except Exception:
        st.error("Error reading sheet — showing placeholder data.")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

# Placeholder if empty
if df.empty:
    df = pd.DataFrame({
        "team": ["Team A", "Team B", "Team C", "Team D"],
        "score": [120, 95, 80, 60],
        "icon": ["🟡", "👻", "🍒", "⭐"]
    })

# Normalize and sort
df.columns = df.columns.str.lower()
if "score" in df.columns:
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

# ----------------- Safe CSS highlighting for top 3 -----------------
def highlight_row_css(row):
    if row.name == 0:
        css = 'background-color: rgba(255,215,0,0.13); color: #FFD700; font-weight: 700;'
    elif row.name == 1:
        css = 'background-color: rgba(192,192,192,0.11); color: #C0C0C0; font-weight: 700;'
    elif row.name == 2:
        css = 'background-color: rgba(205,127,50,0.11); color: #CD7F32; font-weight: 700;'
    else:
        css = 'background-color: rgba(0,0,0,0.18); color: #FFFFFF;'
    return [css] * len(row)

styled = df.style.apply(highlight_row_css, axis=1)

# Prepare display_df with nicer headers
display_df = df.copy().rename(columns=lambda x: x.capitalize())

# ---------- RENDER STYLED TABLE: use components.html for compatibility ----------
# Get HTML from the Styler. Use to_html() which is broadly available.
try:
    styled_html = styled.to_html()
except Exception:
    # fallback: render plain dataframe HTML
    styled_html = display_df.to_html(classes="dataframe", index=False)

# Wrap the table HTML in a container that ensures proper sizing and background transparency
table_wrapper = f"""
<div style="background-color: rgba(0,0,0,0.18); padding: 12px; border-radius: 10px;">
{styled_html}
</div>
"""

# Render the HTML table (scrolling enabled)
components.html(table_wrapper, height=420, scrolling=True)

# Footer text
st.markdown("<div class='footer-text'>🍒 KEEP SCORING — POWER PELLETS AWAIT! 🍒</div>", unsafe_allow_html=True)

# ----------------- Close container -----------------
st.markdown('</div>', unsafe_allow_html=True)
