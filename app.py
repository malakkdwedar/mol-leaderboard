import streamlit as st
import pandas as pd
import gspread
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Pac-Man Leaderboard",
    page_icon="🕹️",
    layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

# ---------------- GOOGLE SHEET ----------------
@st.cache_resource
def get_sheet():
    client = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    SHEET_KEY = "1w39t-QeFhhXxctd5hGxdo-GM2gvKg2WCQOvwkfVB9e0"
    return client.open_by_key(SHEET_KEY).sheet1

try:
    sheet = get_sheet()
    df = pd.DataFrame(sheet.get_all_records())
except Exception:
    df = pd.DataFrame({
        "team": ["Team A", "Team B", "Team C"],
        "score": [120, 95, 80],
        "icon": ["🟡", "👻", "🍒"]
    })

df.columns = df.columns.str.lower()
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
df = df.sort_values("score", ascending=False).reset_index(drop=True)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.stApp {
    background: #1a0028;
    color: white;
}

/* ---------- TITLE ---------- */
.glow-title {
    font-family: 'Press Start 2P', cursive;
    font-size: clamp(36px, 4vw, 52px);
    color: #ffea00;
    text-align: center;
    margin-bottom: 10px;
    animation: pulse 2.5s infinite;
}

@keyframes pulse {
    0% { text-shadow: 0 0 6px #ffea00; }
    50% { text-shadow: 0 0 30px #ffea00; }
    100% { text-shadow: 0 0 6px #ffea00; }
}

/* ---------- GHOSTS ---------- */
.ghost-container {
    text-align: center;
    margin-bottom: 10px;
}
.ghost {
    font-size: clamp(32px, 3vw, 50px);
    margin: 0 18px;
    display: inline-block;
    animation: floaty 3s ease-in-out infinite;
}
.ghost:nth-child(2){animation-delay:.4s}
.ghost:nth-child(3){animation-delay:.8s}
.ghost:nth-child(4){animation-delay:1.2s}

@keyframes floaty {
    0% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0); }
}

/* ---------- SUBTEXT ---------- */
.subtext {
    font-family: 'Press Start 2P', cursive;
    font-size: clamp(16px, 2vw, 24px);
    text-align: center;
    color: #ffb7ff;
    margin-bottom: 18px;
    text-shadow: 0 0 10px #9b4bff;
}

/* ---------- TABLE ---------- */
.pixel-table {
    width: 100%;
    font-family: 'Press Start 2P', cursive;
    font-size: clamp(18px, 2.5vw, 30px);
    border-collapse: collapse;
    text-align: center;
}

.pixel-table th,
.pixel-table td {
    padding: clamp(8px, 1.5vw, 14px);
    border: 3px solid #ffea00;
}

.pixel-table th {
    background: #ffea00;
    color: #1a0028;
}

.pixel-table td {
    color: white;
}

/* ---------- TOP 3 ---------- */
.top1 { background: rgba(255,215,0,0.45); }
.top2 { background: rgba(192,192,192,0.45); }
.top3 { background: rgba(205,127,50,0.45); }

/* ---------- BIG SCREENS ---------- */
@media (min-width: 1600px) {
    .pixel-table {
        font-size: 32px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="glow-title">🕹️👾 Pac-Man Leaderboard 🕹️👾</div>', unsafe_allow_html=True)

st.markdown("""
<div class="ghost-container">
    <span class="ghost">👻</span>
    <span class="ghost">👻</span>
    <span class="ghost">👻</span>
    <span class="ghost">👻</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="subtext">TOP TEAMS UPDATED LIVE DURING THE LGD!</div>', unsafe_allow_html=True)

# ---------------- TABLE ----------------
table_html = """
<table class="pixel-table">
<thead>
<tr><th>Rank</th><th>Team</th><th>Score</th><th>Icon</th></tr>
</thead><tbody>
"""

for i, row in df.iterrows():
    cls = "top1" if i == 0 else "top2" if i == 1 else "top3" if i == 2 else ""
    table_html += f"""
    <tr class="{cls}">
        <td>{i+1}</td>
        <td>{row['team']}</td>
        <td>{row['score']}</td>
        <td>{row['icon']}</td>
    </tr>
    """

table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown('<div class="subtext">🍒 Keep scoring! 🍒</div>', unsafe_allow_html=True)
