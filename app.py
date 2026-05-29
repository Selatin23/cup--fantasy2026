import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQb50AHXthD0sqfUUDaUoauxiUPZEJH2Dgf7PQg93K1ljiW6jKR8KMEK9rgKRfaEZJcNdb1NU4cJ76Q"
    "/pub?output=csv"
)

st.set_page_config(
    page_title="Syndicate Fantasy ЧМ-2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #0d1117; color: #e6edf3; }

  /* ── sidebar ── */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111916 0%, #0d1117 100%);
    border-right: 1px solid #1a2e22;
  }
  section[data-testid="stSidebar"] * { color: #e6edf3 !important; }

  /* ── radio nav — flexbox fix ── */
  div[data-testid="stSidebarContent"] .stRadio > div { gap: 4px; }
  div[data-testid="stSidebarContent"] .stRadio label {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 2px;
    cursor: pointer;
    transition: background .15s;
    min-height: 42px;
    line-height: 1.2;
  }
  div[data-testid="stSidebarContent"] .stRadio label:hover {
    background: rgba(0,223,122,0.10);
  }
  div[data-testid="stSidebarContent"] .stRadio label > div:first-child {
    display: flex !important; align-items: center !important;
    justify-content: center !important; flex-shrink: 0; margin-top: 0 !important;
  }
  div[data-testid="stSidebarContent"] .stRadio label[data-checked="true"],
  div[data-testid="stSidebarContent"] .stRadio [aria-checked="true"] ~ div {
    background: rgba(0,223,122,0.12); border-left: 3px solid #00DF7A;
  }

  /* ── hero ── */
  .hero {
    background: linear-gradient(135deg,#0d2018 0%,#0d1a14 50%,#0d1117 100%);
    border: 1px solid #00DF7A; border-radius: 16px;
    padding: 40px 48px; margin-bottom: 32px;
    position: relative; overflow: hidden;
  }
  .hero::before {
    content:"⚽"; font-size:180px; position:absolute;
    right:-20px; top:-20px; opacity:.06;
  }
  .hero h1 { font-size:2.6rem; font-weight:800; margin:0 0 8px; color:#fff; }
  .hero h1 span { color:#00DF7A; }
  .hero .sub { color:#8b949e; font-size:1.05rem; margin-bottom:24px; }
  .hero .prize-badge {
    display:inline-block;
    background:linear-gradient(90deg,#f5a623,#f0c040);
    color:#0d1117; font-weight:700; font-size:1.3rem;
    border-radius:50px; padding:8px 28px;
  }

  /* ── stat cards ── */
  .stat-row { display:flex; gap:16px; margin-bottom:28px; flex-wrap:wrap; }
  .stat-card {
    flex:1; min-width:140px; background:#111916;
    border:1px solid #1a2e22; border-radius:12px;
    padding:20px 24px; text-align:center;
  }
  .stat-card .val { font-size:2rem; font-weight:800; color:#00DF7A; }
  .stat-card .lbl { font-size:0.82rem; color:#8b949e; margin-top:4px; }

  /* ── section title ── */
  .sec-title {
    font-size:1.15rem; font-weight:700; color:#e6edf3;
    border-left:3px solid #00DF7A; padding-left:12px;
    margin:28px 0 14px;
  }

  /* ── info cards ── */
  .info-grid { display:flex; flex-wrap:wrap; gap:16px; }
  .info-card {
    flex:1; min-width:260px; background:#111916;
    border:1px solid #1a2e22; border-radius:12px; padding:20px 22px;
  }
  .info-card h4 { font-size:1rem; font-weight:700; color:#00DF7A; margin:0 0 10px; }
  .info-card ul { margin:0; padding-left:18px; color:#c9d1d9; font-size:.9rem; line-height:1.8; }

  /* ── group tables ── */
  .group-header {
    display:inline-block;
    background:linear-gradient(90deg,#00DF7A,#00b862);
    color:#0d1117; font-weight:800; font-size:1rem;
    border-radius:8px 8px 0 0; padding:6px 18px;
    margin-bottom:0; letter-spacing:.3px;
  }
  .group-table {
    width:100%; border-collapse:collapse; background:#111916;
    border-radius:0 8px 8px 8px; overflow:hidden;
    font-size:.88rem; border:1px solid #1a2e22; margin-bottom:20px;
  }
  .group-table th {
    background:#141f18; color:#8b949e; font-weight:600;
    padding:8px 12px; text-align:left; border-bottom:1px solid #1a2e22;
  }
  .group-table td { padding:8px 12px; border-bottom:1px solid #172015; color:#e6edf3; }
  .group-table tr:last-child td { border-bottom:none; }

  /* clickable name */
  .mgr-link {
    color:#e6edf3; text-decoration:none; font-weight:700;
    border-bottom:1px dashed #3d5c47; cursor:pointer;
    transition:color .15s;
  }
  .mgr-link:hover { color:#00DF7A; border-bottom-color:#00DF7A; }

  .rank-badge {
    display:inline-flex; align-items:center; justify-content:center;
    width:22px; height:22px; border-radius:50%;
    font-weight:700; font-size:.8rem;
  }
  .rank-1 { background:#f5a623; color:#000; }
  .rank-2 { background:#00DF7A; color:#000; }
  .rank-3 { background:#3d444d; color:#e6edf3; }
  .rank-4 { background:#21262d; color:#8b949e; }
  .green-row td { background:rgba(0,223,122,.10) !important; }
  .green-row td:first-child { border-left:3px solid #00DF7A; }
  .highlight-row td { background:rgba(0,223,122,.18) !important; }
  .highlight-row td:first-child { border-left:3px solid #00ff8a; }

  /* form dots */
  .dot {
    display:inline-block; width:11px; height:11px;
    border-radius:50%; margin:0 2px; vertical-align:middle;
  }
  .dot-g { background:#00DF7A; box-shadow:0 0 5px rgba(0,223,122,.5); }
  .dot-y { background:#f5a623; }
  .dot-r { background:#f85149; }
  .dot-x { background:#3d444d; }

  /* ── playoff bracket ── */
  .match-card {
    background:#111916; border:1px solid #1a2e22;
    border-left:4px solid #00DF7A; border-radius:10px;
    overflow:hidden; margin-bottom:10px;
    transition:border-color .2s,box-shadow .2s;
  }
  .match-card:hover {
    border-color:#00DF7A; box-shadow:0 0 12px rgba(0,223,122,.15);
  }
  .match-player {
    display:flex; justify-content:space-between; align-items:center;
    padding:9px 14px; font-size:.88rem; color:#c9d1d9;
  }
  .match-player + .match-player { border-top:1px solid #172015; }
  .match-player.winner {
    background:rgba(0,223,122,.15); font-weight:700; color:#00DF7A;
  }
  .match-player.pending { color:#8b949e; font-style:italic; }
  .match-score {
    font-weight:800; font-size:1rem; color:#00DF7A;
    background:#0d1117; border-radius:6px;
    padding:2px 8px; min-width:38px; text-align:center;
  }
  .match-score.no-score { color:#3d444d; }

  /* ── prize tables ── */
  .prize-table { width:100%; border-collapse:collapse; font-size:.9rem; }
  .prize-table th {
    background:#141f18; color:#8b949e; font-weight:600;
    padding:10px 14px; text-align:left; border-bottom:1px solid #1a2e22;
  }
  .prize-table td { padding:10px 14px; border-bottom:1px solid #172015; color:#e6edf3; }
  .prize-table tr:hover td { background:#141f18; }
  .gold  { color:#f5a623; font-weight:700; }
  .neon  { color:#00DF7A; font-weight:700; }
  .silver{ color:#c9d1d9; font-weight:700; }

  /* ── prize breakdown ── */
  .prize-grid { display:flex; flex-wrap:wrap; gap:16px; margin-bottom:28px; }
  .prize-cat {
    flex:1; min-width:220px; background:#111916;
    border:1px solid #1a2e22; border-top:3px solid #00DF7A;
    border-radius:12px; padding:18px 20px;
  }
  .prize-cat h4 { font-size:.95rem; font-weight:700; color:#00DF7A; margin:0 0 12px; }
  .prize-cat ul { margin:0; padding-left:0; list-style:none; color:#c9d1d9; font-size:.88rem; line-height:2; }
  .prize-cat ul li { display:flex; justify-content:space-between; border-bottom:1px solid #172015; }
  .prize-cat ul li:last-child { border-bottom:none; }
  .prize-cat ul li span { color:#f5a623; font-weight:700; }

  /* ── waiting badge ── */
  .waiting {
    display:inline-block; background:#141f18; color:#8b949e;
    border:1px dashed #1a2e22; border-radius:6px;
    padding:2px 10px; font-size:.8rem;
  }

  /* ── profile card ── */
  .profile-hero {
    background:linear-gradient(135deg,#0d2018,#111916);
    border:1px solid #00DF7A; border-radius:16px;
    padding:28px 32px; margin-bottom:24px;
    display:flex; gap:28px; align-items:flex-start; flex-wrap:wrap;
  }
  .profile-hero .name { font-size:1.8rem; font-weight:800; color:#fff; margin-bottom:4px; }
  .profile-hero .meta { color:#8b949e; font-size:.9rem; }
  .profile-hero .meta span { color:#00DF7A; font-weight:700; }
  .profile-stats { display:flex; gap:12px; flex-wrap:wrap; margin-top:16px; }
  .p-stat {
    background:#0d1117; border:1px solid #1a2e22; border-radius:10px;
    padding:12px 18px; text-align:center; min-width:80px;
  }
  .p-stat .pv { font-size:1.4rem; font-weight:800; color:#00DF7A; }
  .p-stat .pl { font-size:.75rem; color:#8b949e; margin-top:2px; }
  .gw-bar-wrap {
    background:#111916; border:1px solid #1a2e22; border-radius:12px;
    padding:20px 24px; margin-bottom:16px;
  }
  .gw-bar-wrap h4 { font-size:.9rem; color:#8b949e; font-weight:600; margin:0 0 14px; }
  .bar-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
  .bar-label { width:46px; font-size:.8rem; color:#8b949e; text-align:right; flex-shrink:0; }
  .bar-track {
    flex:1; height:20px; background:#172015; border-radius:6px; overflow:hidden;
  }
  .bar-fill {
    height:100%; background:linear-gradient(90deg,#00DF7A,#00b862);
    border-radius:6px; transition:width .4s;
  }
  .bar-val { width:36px; font-size:.82rem; font-weight:700; color:#e6edf3; text-align:left; flex-shrink:0; }

  /* ── playoff path ── */
  .path-stage {
    display:inline-flex; align-items:center; gap:8px;
    background:#111916; border:1px solid #1a2e22; border-radius:8px;
    padding:7px 14px; margin:4px 4px 4px 0; font-size:.85rem;
  }
  .path-stage.won  { border-color:#00DF7A; color:#00DF7A; }
  .path-stage.lost { border-color:#f85149; color:#8b949e; text-decoration:line-through; }
  .path-stage.tbd  { border-color:#3d444d; color:#8b949e; font-style:italic; }

  /* ── auto-refresh bar ── */
  .refresh-bar {
    height:3px; background:linear-gradient(90deg,#00DF7A,#00b862);
    border-radius:2px; margin-bottom:6px;
  }

  /* ── button override ── */
  .stButton > button {
    background:rgba(0,223,122,.12); border:1px solid #00DF7A;
    color:#00DF7A !important; font-weight:600;
    border-radius:8px; transition:background .15s;
  }
  .stButton > button:hover { background:rgba(0,223,122,.22); }

  /* ── group insights ── */
  .group-rank-card {
    background:#111916; border:1px solid #1a2e22; border-radius:12px;
    padding:16px 20px; margin-bottom:10px;
    display:flex; align-items:center; gap:16px;
    transition:border-color .2s;
  }
  .group-rank-card:hover { border-color:#00DF7A; }
  .group-rank-card.death  { border-left:4px solid #f85149; background:rgba(248,81,73,.07); }
  .group-rank-card.easy   { border-left:4px solid #3fb950; background:rgba(63,185,80,.07); }
  .group-rank-card .g-num {
    font-size:1.5rem; font-weight:800; min-width:32px; text-align:center;
    color:#8b949e;
  }
  .group-rank-card .g-letter {
    background:linear-gradient(90deg,#00DF7A,#00b862);
    color:#0d1117; font-weight:800; font-size:1.1rem;
    border-radius:8px; width:38px; height:38px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
  }
  .group-rank-card.death .g-letter { background:linear-gradient(90deg,#f85149,#da3633); color:#fff; }
  .group-rank-card.easy  .g-letter { background:linear-gradient(90deg,#3fb950,#2ea043); color:#fff; }
  .group-rank-card .g-info { flex:1; }
  .group-rank-card .g-info .g-total {
    font-size:1.25rem; font-weight:800; color:#e6edf3;
  }
  .group-rank-card .g-info .g-sub { font-size:.8rem; color:#8b949e; margin-top:2px; }
  .group-rank-card .g-badge {
    font-size:.75rem; font-weight:700; border-radius:20px;
    padding:3px 10px; white-space:nowrap;
  }
  .badge-death { background:rgba(248,81,73,.2); color:#f85149; border:1px solid #f85149; }
  .badge-easy  { background:rgba(63,185,80,.2);  color:#3fb950; border:1px solid #3fb950; }
  .g-mini-bar-wrap { flex:2; min-width:120px; }
  .g-mini-bar-track {
    height:8px; background:#172015; border-radius:4px; overflow:hidden; margin-top:4px;
  }
  .g-mini-bar-fill {
    height:100%; border-radius:4px;
    background:linear-gradient(90deg,#00DF7A,#00b862);
  }
  .group-rank-card.death .g-mini-bar-fill { background:linear-gradient(90deg,#f85149,#da3633); }
  .group-rank-card.easy  .g-mini-bar-fill { background:linear-gradient(90deg,#3fb950,#2ea043); }

  /* ── insights stat strip ── */
  .insight-strip {
    display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px;
  }
  .insight-chip {
    background:#111916; border:1px solid #1a2e22; border-radius:10px;
    padding:12px 18px; flex:1; min-width:140px; text-align:center;
  }
  .insight-chip .ic-val { font-size:1.5rem; font-weight:800; color:#00DF7A; }
  .insight-chip .ic-lbl { font-size:.78rem; color:#8b949e; margin-top:3px; }

  /* ── financial report ── */
  .fin-hero {
    background:linear-gradient(135deg,#1a1400,#141000,#0d1117);
    border:1px solid #f5a623; border-radius:16px;
    padding:28px 36px; margin-bottom:24px; position:relative; overflow:hidden;
  }
  .fin-hero::before {
    content:"₸"; font-size:160px; font-weight:900;
    position:absolute; right:-10px; top:-20px; opacity:.05; color:#f5a623;
  }
  .fin-hero h2 { font-size:1.8rem; font-weight:800; color:#fff; margin:0 0 6px; }
  .fin-hero h2 span { color:#f5a623; }
  .fin-hero .fh-sub { color:#8b949e; font-size:.9rem; }

  .fin-leaderboard { width:100%; border-collapse:collapse; font-size:.9rem; }
  .fin-leaderboard th {
    background:#141f18; color:#8b949e; font-weight:600;
    padding:10px 14px; text-align:left; border-bottom:1px solid #1a2e22;
  }
  .fin-leaderboard td {
    padding:11px 14px; border-bottom:1px solid #172015; color:#e6edf3;
    vertical-align:middle;
  }
  .fin-leaderboard tr:hover td { background:#141f18; }
  .fin-leaderboard .top-earner td { background:rgba(0,223,122,.08) !important; }
  .fin-leaderboard .top-earner td:first-child { border-left:3px solid #00DF7A; }
  .earning-bar {
    display:flex; align-items:center; gap:8px;
  }
  .earning-track {
    flex:1; height:6px; background:#172015; border-radius:3px; overflow:hidden; min-width:60px;
  }
  .earning-fill {
    height:100%; border-radius:3px;
    background:linear-gradient(90deg,#f5a623,#f0c040);
  }
  .mvp-dot {
    display:inline-block; width:8px; height:8px;
    background:#00DF7A; border-radius:50%;
    margin:0 1px; vertical-align:middle;
    box-shadow:0 0 4px rgba(0,223,122,.6);
  }
  .mvp-dot-half {
    display:inline-block; width:8px; height:8px;
    background:linear-gradient(90deg,#00DF7A 50%,#172015 50%);
    border-radius:50%; margin:0 1px; vertical-align:middle;
    border:1px solid #00DF7A;
  }
  .gw-detail-table { width:100%; border-collapse:collapse; font-size:.85rem; }
  .gw-detail-table th {
    background:#0d1117; color:#8b949e; font-weight:600;
    padding:7px 12px; text-align:left; border-bottom:1px solid #1a2e22;
  }
  .gw-detail-table td {
    padding:7px 12px; border-bottom:1px solid #172015; color:#c9d1d9;
  }
  .gw-detail-table tr:last-child td { border-bottom:none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
GW_COLS   = ["gw1","gw2","gw3","gw4","gw5","gw6","gw7","gw8"]
GW_LABELS = {f"gw{i}": f"Тур {i}" for i in range(1, 9)}
STAGE_GW  = {"r16":"gw4","r8":"gw5","r4":"gw6","r2":"gw7","final":"gw8"}
STAGE_LABELS = {
    "r16":"1/16 Финала","r8":"1/8 Финала",
    "r4":"Четвертьфинал","r2":"Полуфинал","final":"Финал",
}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_URL)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in GW_COLS:
        df[col] = pd.to_numeric(df.get(col, np.nan), errors="coerce")
    df["group_letter"] = df["group_letter"].str.strip().str.upper()
    df["manager_name"]  = df["manager_name"].str.strip()
    return df

# ─────────────────────────────────────────────
# TOURNAMENT LOGIC
# ─────────────────────────────────────────────
def get_group_stage(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["group_pts"] = d[["gw1","gw2","gw3"]].sum(axis=1, min_count=1)
    d = d.sort_values(["group_letter","group_pts"], ascending=[True,False])
    d["rank"] = d.groupby("group_letter")["group_pts"].rank(
        method="min", ascending=False).astype(int)
    return d

def get_third_place_ranking(gs: pd.DataFrame) -> pd.DataFrame:
    t = gs[gs["rank"]==3].copy().sort_values("group_pts",ascending=False).reset_index(drop=True)
    t["third_rank"] = t.index + 1
    return t

def get_playoff_qualifiers(gs: pd.DataFrame) -> pd.DataFrame:
    top2   = gs[gs["rank"] <= 2].copy()
    thirds = get_third_place_ranking(gs)
    t8     = thirds.head(8).copy(); t8["rank"] = 3
    q = pd.concat([top2, t8], ignore_index=True)
    q["seed"] = 0
    groups = sorted(q["group_letter"].unique())
    seed = 1
    for rk in [1, 2]:
        for g in groups:
            mask = (q["group_letter"]==g) & (q["rank"]==rk)
            q.loc[mask,"seed"] = seed; seed += 1
    for i, idx in enumerate(q.loc[q["rank"]==3].index):
        q.loc[idx,"seed"] = 25 + i
    return q.sort_values("seed").reset_index(drop=True)

def build_r16_matchups(q: pd.DataFrame) -> list[dict]:
    p = q.sort_values("seed")["manager_id"].tolist()
    n = len(p)
    return [{"p1_id": p[i], "p2_id": p[n-1-i]} for i in range(n//2)]

def score_val(df, mid, gw):
    r = df[df["manager_id"]==mid]
    if r.empty: return np.nan
    v = r[gw].values[0]
    return np.nan if pd.isna(v) else v

def match_result(df, p1, p2, gw):
    s1, s2 = score_val(df,p1,gw), score_val(df,p2,gw)
    if pd.isna(s1) or pd.isna(s2): return s1, s2, None
    if s1 > s2: return s1, s2, p1
    if s2 > s1: return s1, s2, p2
    gp1 = df.loc[df["manager_id"]==p1,"group_pts"].values[0] if "group_pts" in df else 0
    gp2 = df.loc[df["manager_id"]==p2,"group_pts"].values[0] if "group_pts" in df else 0
    return s1, s2, p1 if gp1 >= gp2 else p2

def simulate_bracket(df, r16):
    gs  = get_group_stage(df)
    dfw = df.merge(gs[["manager_id","group_pts"]], on="manager_id", how="left")
    stages, cur = {}, [(m["p1_id"],m["p2_id"]) for m in r16]
    for stage in ["r16","r8","r4","r2","final"]:
        gw = STAGE_GW[stage]; sms = []
        for p1, p2 in cur:
            s1,s2,w = match_result(dfw,p1,p2,gw)
            n1 = dfw.loc[dfw["manager_id"]==p1,"manager_name"].values[0] if not dfw[dfw["manager_id"]==p1].empty else str(p1)
            n2 = dfw.loc[dfw["manager_id"]==p2,"manager_name"].values[0] if not dfw[dfw["manager_id"]==p2].empty else str(p2)
            sms.append({"p1_id":p1,"p1_name":n1,"p1_score":s1,
                        "p2_id":p2,"p2_name":n2,"p2_score":s2,"winner":w,"gw":gw})
        stages[stage] = sms
        ws = [m["winner"] for m in sms]
        cur = [(ws[i] or "TBD", ws[i+1] if i+1<len(ws) else "TBD") for i in range(0,len(ws),2)]
        if stage == "final": break
    return stages

# ─────────────────────────────────────────────
# GROUP INSIGHTS LOGIC
# ─────────────────────────────────────────────
def get_group_insights(gs: pd.DataFrame) -> pd.DataFrame:
    """Aggregate group-stage stats per group letter."""
    grp = gs.groupby("group_letter").agg(
        total_pts   = ("group_pts", "sum"),
        avg_pts     = ("group_pts", "mean"),
        max_pts     = ("group_pts", "max"),
        min_pts     = ("group_pts", "min"),
        player_count= ("manager_id", "count"),
    ).reset_index()
    grp = grp.sort_values("total_pts", ascending=False).reset_index(drop=True)
    grp["g_rank"] = grp.index + 1
    return grp

# ─────────────────────────────────────────────
# FINANCIAL REPORT LOGIC
# ─────────────────────────────────────────────
def calc_mvp_earnings(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each played GW find the max scorer(s).
    Prize = 20 000 ₸ split equally among tied winners.
    Returns a DataFrame with manager_id, manager_name,
    mvp_wins (float, counts halves), total_earned (₸).
    """
    MVP_PRIZE = 20_000
    # init earnings dict  manager_id -> {name, wins, earned}
    earnings: dict = {}
    for mid, name in zip(df["manager_id"], df["manager_name"]):
        earnings[mid] = {"manager_name": name, "mvp_wins": 0.0, "total_earned": 0.0,
                         "gw_detail": {}}  # gw -> earned in that gw

    for gw in GW_COLS:
        col = df[["manager_id", "manager_name", gw]].dropna(subset=[gw])
        col = col[col[gw] > 0]          # ignore gws with all zeros / no data
        if col.empty:
            continue
        max_score = col[gw].max()
        winners   = col[col[gw] == max_score]
        n_winners = len(winners)
        share     = MVP_PRIZE / n_winners
        win_share = 1.0 / n_winners     # fractional win credit

        for _, wrow in winners.iterrows():
            mid = wrow["manager_id"]
            earnings[mid]["mvp_wins"]    += win_share
            earnings[mid]["total_earned"] += share
            earnings[mid]["gw_detail"][gw] = {
                "score":    int(wrow[gw]),
                "earned":   share,
                "n_shared": n_winners,
                "max_score": int(max_score),
            }

    rows = []
    for mid, data in earnings.items():
        rows.append({
            "manager_id":   mid,
            "manager_name": data["manager_name"],
            "mvp_wins":     data["mvp_wins"],
            "total_earned": data["total_earned"],
            "gw_detail":    data["gw_detail"],
        })
    result = pd.DataFrame(rows).sort_values("total_earned", ascending=False).reset_index(drop=True)
    return result

# ─────────────────────────────────────────────
# FORM DOTS HELPER
# ─────────────────────────────────────────────
def form_dots(df: pd.DataFrame, manager_id, played_gws: list[str]) -> str:
    """Return 3 most-recent form dots based on rank within each played gw."""
    recent = played_gws[-3:] if len(played_gws) >= 3 else played_gws
    dots = []
    for gw in recent:
        col = df[["manager_id", gw]].dropna(subset=[gw])
        if col.empty:
            dots.append("<span class='dot dot-x'></span>")
            continue
        total = len(col)
        rank  = col[gw].rank(ascending=False, method="min")
        pid_rank = rank[df["manager_id"] == manager_id]
        if pid_rank.empty:
            dots.append("<span class='dot dot-x'></span>"); continue
        r = pid_rank.values[0]
        pct = r / total
        if pct <= 0.33:
            dots.append("<span class='dot dot-g'></span>")
        elif pct <= 0.66:
            dots.append("<span class='dot dot-y'></span>")
        else:
            dots.append("<span class='dot dot-r'></span>")
    return "".join(dots)

# ─────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────
def rank_badge(r: int) -> str:
    cls = {1:"rank-1",2:"rank-2",3:"rank-3",4:"rank-4"}.get(r,"rank-4")
    return f"<span class='rank-badge {cls}'>{r}</span>"

def render_match_card(m: dict) -> str:
    def row(name, score, win, pend):
        cls = "match-player" + (" pending" if pend else " winner" if win else "")
        sc  = ("<span class='match-score no-score'>?</span>" if pend else
               f"<span class='match-score' style='color:#00DF7A'>{int(score)}</span>" if win else
               f"<span class='match-score' style='color:#8b949e'>{int(score)}</span>")
        trophy = " 🏆" if win and not pend else ""
        return f"<div class='{cls}'><span>{name}{trophy}</span>{sc}</div>"
    pend = m["winner"] is None
    return (f"<div class='match-card'>"
            f"{row(m['p1_name'],m['p1_score'],m['winner']==m['p1_id'],pend)}"
            f"{row(m['p2_name'],m['p2_score'],m['winner']==m['p2_id'],pend)}"
            f"</div>")

def render_group_table(gdf: pd.DataFrame, thirds_top8: set,
                       played_gws: list[str], df_full: pd.DataFrame) -> str:
    html = "<table class='group-table'>"
    html += "<tr><th>#</th><th>Менеджер</th><th>GW1</th><th>GW2</th><th>GW3</th><th>Форма</th><th>Сумма</th></tr>"
    for _, row in gdf.iterrows():
        r   = int(row["rank"])
        pts = row["group_pts"]
        pts_str = f"{int(pts)}" if not pd.isna(pts) else "<span class='waiting'>ожидание</span>"
        def gc(col):
            v = row[col]; return f"{int(v)}" if not pd.isna(v) else "<span class='waiting'>–</span>"
        row_cls = ("green-row" if r <= 2 else
                   "highlight-row" if row["manager_id"] in thirds_top8 else "")
        dots = form_dots(df_full, row["manager_id"], played_gws)
        # clickable name → uses st query_params via JS-free approach (name as param)
        safe_name = str(row["manager_name"]).replace("'", "&#39;")
        mid = row["manager_id"]
        name_cell = (
            f"<span class='mgr-link' "
            f"onclick=\"window.location.search='?profile={mid}'\">"
            f"{safe_name}</span>"
        )
        html += (f"<tr class='{row_cls}'><td>{rank_badge(r)}</td>"
                 f"<td>{name_cell}</td>"
                 f"<td>{gc('gw1')}</td><td>{gc('gw2')}</td><td>{gc('gw3')}</td>"
                 f"<td>{dots}</td>"
                 f"<td><strong>{pts_str}</strong></td></tr>")
    html += "</table>"
    return html

# ─────────────────────────────────────────────
# PLAYER PROFILE PAGE
# ─────────────────────────────────────────────
def page_profile(df: pd.DataFrame, gs: pd.DataFrame,
                 bracket: dict, played_gws: list[str], manager_id):
    row = gs[gs["manager_id"] == manager_id]
    if row.empty:
        st.error("Участник не найден.")
        return
    row = row.iloc[0]
    name  = row["manager_name"]
    group = row["group_letter"]
    rank  = int(row["rank"])
    gpts  = row["group_pts"]

    # ── back button ──
    if st.button("← Вернуться к группам"):
        st.query_params.clear()
        st.rerun()

    # total points across all played gws
    total_pts = df.loc[df["manager_id"]==manager_id, played_gws].sum(axis=1).values
    total_pts = int(total_pts[0]) if len(total_pts) else 0

    # overall rank
    overall = df.copy()
    overall["total_pts"] = overall[played_gws].sum(axis=1, min_count=1)
    overall = overall.sort_values("total_pts", ascending=False).reset_index(drop=True)
    overall["ov_rank"] = overall.index + 1
    ov_rank = overall.loc[overall["manager_id"]==manager_id, "ov_rank"].values
    ov_rank = int(ov_rank[0]) if len(ov_rank) else "–"

    # ── profile hero ──
    st.markdown(f"""
    <div class='profile-hero'>
      <div>
        <div class='name'>{name}</div>
        <div class='meta'>
          Группа <span>{group}</span> · Место <span>#{rank}</span> в группе ·
          Очков в группе <span>{int(gpts) if not pd.isna(gpts) else '–'}</span>
        </div>
        <div class='profile-stats'>
          <div class='p-stat'><div class='pv'>{total_pts}</div><div class='pl'>Всего очков</div></div>
          <div class='p-stat'><div class='pv'>#{ov_rank}</div><div class='pl'>Общий рейтинг</div></div>
          <div class='p-stat'><div class='pv'>{len(played_gws)}/8</div><div class='pl'>Туров сыграно</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    # ── bar chart ──
    with col_left:
        st.markdown("<div class='sec-title'>📈 Очки по турам</div>", unsafe_allow_html=True)
        all_scores = []
        for gw in GW_COLS:
            v = df.loc[df["manager_id"]==manager_id, gw].values
            all_scores.append(float(v[0]) if len(v) and not pd.isna(v[0]) else None)
        max_sc = max((s for s in all_scores if s is not None), default=1)
        bars_html = "<div class='gw-bar-wrap'><h4>Очки за каждый тур</h4>"
        for i, gw in enumerate(GW_COLS):
            sc = all_scores[i]
            if sc is None:
                bars_html += (f"<div class='bar-row'>"
                              f"<div class='bar-label'>{GW_LABELS[gw]}</div>"
                              f"<div class='bar-track'><div class='bar-fill' style='width:0%'></div></div>"
                              f"<div class='bar-val' style='color:#3d444d;'>–</div></div>")
            else:
                pct = int(sc / max_sc * 100)
                bars_html += (f"<div class='bar-row'>"
                              f"<div class='bar-label'>{GW_LABELS[gw]}</div>"
                              f"<div class='bar-track'><div class='bar-fill' style='width:{pct}%'></div></div>"
                              f"<div class='bar-val'>{int(sc)}</div></div>")
        bars_html += "</div>"
        st.markdown(bars_html, unsafe_allow_html=True)

        # ── group rivals ──
        st.markdown("<div class='sec-title'>👥 Соперники по группе</div>", unsafe_allow_html=True)
        rivals = gs[gs["group_letter"]==group].copy()
        html = "<table class='group-table'>"
        html += "<tr><th>#</th><th>Менеджер</th><th>GW1</th><th>GW2</th><th>GW3</th><th>Сумма</th></tr>"
        for _, rv in rivals.iterrows():
            is_me = rv["manager_id"] == manager_id
            me_style = "background:rgba(0,223,122,.06);" if is_me else ""
            rnk = int(rv["rank"])
            rpts = rv["group_pts"]
            rpts_str = f"{int(rpts)}" if not pd.isna(rpts) else "–"
            def gc2(col):
                v = rv[col]; return f"{int(v)}" if not pd.isna(v) else "–"
            name_str = f"<strong style='color:#00DF7A;'>{rv['manager_name']} ←</strong>" if is_me else rv["manager_name"]
            html += (f"<tr style='{me_style}'><td>{rank_badge(rnk)}</td>"
                     f"<td>{name_str}</td>"
                     f"<td>{gc2('gw1')}</td><td>{gc2('gw2')}</td><td>{gc2('gw3')}</td>"
                     f"<td><strong>{rpts_str}</strong></td></tr>")
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

    # ── playoff path ──
    with col_right:
        st.markdown("<div class='sec-title'>🏆 Путь в плей-офф</div>", unsafe_allow_html=True)
        path_html = ""
        for stage in ["r16","r8","r4","r2","final"]:
            matches = bracket.get(stage, [])
            player_match = next(
                (m for m in matches if m["p1_id"]==manager_id or m["p2_id"]==manager_id),
                None
            )
            if player_match is None:
                path_html += (f"<div class='path-stage tbd'>"
                              f"<span>{STAGE_LABELS[stage]}</span>"
                              f"<span style='font-size:.8rem;'>⏳</span></div>")
                continue
            gw = player_match["gw"]
            is_p1 = player_match["p1_id"] == manager_id
            opp_name = player_match["p2_name"] if is_p1 else player_match["p1_name"]
            my_score = player_match["p1_score"] if is_p1 else player_match["p2_score"]
            opp_score= player_match["p2_score"] if is_p1 else player_match["p1_score"]
            winner   = player_match["winner"]

            if winner is None:
                sc_str = "vs"
                cls = "tbd"
                extra = f"<span style='font-size:.8rem;color:#8b949e;'>⏳ {GW_LABELS[gw]}</span>"
            elif winner == manager_id:
                sc = f"{int(my_score)}–{int(opp_score)}" if not pd.isna(my_score) else "–"
                sc_str = sc; cls = "won"
                extra = f"<span style='font-size:.8rem;'>✅ победа</span>"
            else:
                sc = f"{int(my_score)}–{int(opp_score)}" if not pd.isna(my_score) else "–"
                sc_str = sc; cls = "lost"
                extra = f"<span style='font-size:.8rem;color:#f85149;'>❌ выбыл</span>"

            path_html += (f"<div class='path-stage {cls}'>"
                          f"<div><div style='font-weight:700;font-size:.88rem;'>{STAGE_LABELS[stage]}</div>"
                          f"<div style='font-size:.78rem;color:#8b949e;'>vs {opp_name} · {sc_str}</div></div>"
                          f"{extra}</div><br>")

        st.markdown(path_html or "<span class='waiting'>Не вышел в плей-офф</span>",
                    unsafe_allow_html=True)

        # ── per-gw ranking ──
        st.markdown("<div class='sec-title'>📊 Рейтинг по каждому туру</div>", unsafe_allow_html=True)
        rank_html = "<table class='prize-table'>"
        rank_html += "<tr><th>Тур</th><th>Очки</th><th>Место</th></tr>"
        for gw in played_gws:
            col = df[["manager_id", gw]].dropna(subset=[gw])
            my_val = df.loc[df["manager_id"]==manager_id, gw].values
            if len(my_val) == 0 or pd.isna(my_val[0]):
                rank_html += f"<tr><td class='neon'>{GW_LABELS[gw]}</td><td>–</td><td>–</td></tr>"
                continue
            v = my_val[0]
            gw_rank = int(col[gw].rank(ascending=False, method="min")[df["manager_id"]==manager_id].values[0])
            total_n = len(col)
            medal = "🥇" if gw_rank==1 else ("🥈" if gw_rank==2 else ("🥉" if gw_rank==3 else ""))
            rank_html += (f"<tr><td class='neon'>{GW_LABELS[gw]}</td>"
                          f"<td><strong>{int(v)}</strong></td>"
                          f"<td>{medal} #{gw_rank} / {total_n}</td></tr>")
        rank_html += "</table>"
        st.markdown(rank_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True)
    except Exception:
        st.markdown("<div style='text-align:center;font-size:2.4rem;padding:8px 0 4px;'>⚽</div>",
                    unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;padding:8px 0 20px;'>
      <div style='font-weight:800;font-size:1.05rem;color:#00DF7A;letter-spacing:.5px;'>Syndicate Fantasy</div>
      <div style='font-size:.78rem;color:#8b949e;'>ЧМ-2026 · Турнир</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav", ["🏠  Главная и Регламент","📊  Групповой этап",
                "🏆  Сетка Кубка (Плей-офф)","💰  Призовой фонд и Награды",
                "🔬  Аналитика групп","💳  Финансовый отчёт"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if st.button("🔄 Обновить данные", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown(
        "<div style='color:#3d5c47;font-size:.75rem;text-align:center;padding-top:8px;'>"
        "Кэш обновляется каждые 2 мин</div>",
        unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
data_ok = False
df = pd.DataFrame()
err_msg = ""

try:
    with st.spinner("Загрузка данных..."):
        df = load_data()
    data_ok = True
except Exception as e:
    err_msg = str(e)

if data_ok:
    gs          = get_group_stage(df)
    thirds      = get_third_place_ranking(gs)
    thirds_top8 = set(thirds.head(8)["manager_id"].tolist())
    played_gws  = [g for g in GW_COLS if df[g].notna().any()]
    try:
        qualifiers  = get_playoff_qualifiers(gs)
        r16_matchups= build_r16_matchups(qualifiers)
        bracket     = simulate_bracket(gs, r16_matchups)
        bracket_ok  = True
    except Exception as e:
        bracket_ok = False; bracket_err = str(e)
        bracket = {}
else:
    gs = thirds = pd.DataFrame()
    thirds_top8 = set()
    played_gws  = []
    bracket_ok  = False; bracket_err = err_msg
    bracket     = {}

# ─────────────────────────────────────────────
# PROFILE PAGE (via query param ?profile=<id>)
# ─────────────────────────────────────────────
params = st.query_params
profile_id_raw = params.get("profile", None)
if profile_id_raw is not None and data_ok:
    try:
        # manager_id might be int or str depending on sheet
        pid = int(profile_id_raw) if str(profile_id_raw).isdigit() else profile_id_raw
        page_profile(df, gs, bracket, played_gws, pid)
    except Exception as e:
        st.error(f"Ошибка профиля: {e}")
    # stop rendering other pages
    st.stop()

# ─────────────────────────────────────────────
# PAGE: ГЛАВНАЯ
# ─────────────────────────────────────────────
if "Главная" in page:
    col_logo, col_hero = st.columns([1, 4])
    with col_logo:
        try: st.image("logo.jpg", use_column_width=True)
        except: pass
    with col_hero:
        st.markdown("""
        <div class='hero'>
          <h1>⚽ <span>Syndicate</span> Fantasy ЧМ-2026</h1>
          <div class='sub'>Syndicate турнир среди 48 менеджеров · Чемпионат Мира 2026</div>
          <div class='prize-badge'>🏆 Призовой фонд: 480 000 ₸</div>
        </div>
        """, unsafe_allow_html=True)

    if data_ok:
        total   = len(df)
        groups  = df["group_letter"].nunique()
        gws_n   = len(played_gws)
        max_pts = int(df[played_gws].sum(axis=1).max()) if played_gws else 0
    else:
        total, groups, gws_n, max_pts = 48, 12, 0, 0

    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-card'><div class='val'>{total}</div><div class='lbl'>Участников</div></div>
      <div class='stat-card'><div class='val'>{groups}</div><div class='lbl'>Групп</div></div>
      <div class='stat-card'><div class='val'>{gws_n} / 8</div><div class='lbl'>Туров сыграно</div></div>
      <div class='stat-card'><div class='val'>{max_pts}</div><div class='lbl'>Рекорд очков</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>📋 Регламент турнира</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-grid'>
      <div class='info-card'>
        <h4>🔵 Групповой этап (Туры 1–3)</h4>
        <ul>
          <li>48 игроков → 12 групп (A–L) по 4 человека</li>
          <li>Очных матчей нет — считается сумма GW1+GW2+GW3</li>
          <li>Топ-2 каждой группы → 1/16 финала (24 игрока)</li>
          <li>Лучшие 8 из 3-х мест → 1/16 финала</li>
          <li>Итого 32 участника в плей-офф</li>
        </ul>
      </div>
      <div class='info-card'>
        <h4>🔴 Плей-офф (Туры 4–8)</h4>
        <ul>
          <li><strong>1/16 финала</strong> — Тур 4 (GW4)</li>
          <li><strong>1/8 финала</strong> — Тур 5 (GW5)</li>
          <li><strong>Четвертьфинал</strong> — Тур 6 (GW6)</li>
          <li><strong>Полуфинал</strong> — Тур 7 (GW7)</li>
          <li><strong>Финал</strong> — Тур 8 (GW8)</li>
          <li>Head-to-Head: кто больше очков в туре — проходит</li>
        </ul>
      </div>
      <div class='info-card'>
        <h4>💰 Призовой фонд 480 000 ₸</h4>
        <ul>
          <li>🏆 Кубок (1 место): <strong>110 000 ₸</strong></li>
          <li>🥈 Кубок (2 место): <strong>50 000 ₸</strong></li>
          <li>🥉 Кубок (3 место): <strong>25 000 ₸</strong></li>
          <li>🎯 Classic (1 место): <strong>75 000 ₸</strong></li>
          <li>🎯 Classic (2 место): <strong>40 000 ₸</strong></li>
          <li>🎯 Classic (3 место): <strong>20 000 ₸</strong></li>
          <li>⚡ MVP тура × 8 туров: <strong>20 000 ₸</strong> каждый</li>
        </ul>
      </div>
      <div class='info-card'>
        <h4>ℹ️ Общие правила</h4>
        <ul>
          <li>При ничьей в плей-офф — преимущество по сумме группового этапа</li>
          <li>3-е места из групп: выбор топ-8 строго по очкам</li>
          <li>Жеребьёвка 1/16: сид 1 vs сид 32, сид 2 vs сид 31…</li>
          <li>Результаты обновляются автоматически из таблицы</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ Не удалось загрузить данные.\n\n`{err_msg}`")

# ─────────────────────────────────────────────
# PAGE: ГРУППОВОЙ ЭТАП
# ─────────────────────────────────────────────
elif "Групповой" in page:
    st.markdown("<div class='sec-title'>📊 Групповой этап — Таблицы групп</div>", unsafe_allow_html=True)
    if not data_ok:
        st.error(f"⚠️ {err_msg}")
    else:
        st.markdown(
            "<p style='color:#8b949e;font-size:.85rem;margin-bottom:16px;'>"
            "💡 Нажмите на имя менеджера чтобы открыть его профиль</p>",
            unsafe_allow_html=True)

        groups_sorted = sorted(gs["group_letter"].unique())
        for row_start in range(0, len(groups_sorted), 2):
            cols = st.columns(2)
            for ci, g in enumerate(groups_sorted[row_start:row_start+2]):
                gdf = gs[gs["group_letter"]==g].copy()
                with cols[ci]:
                    st.markdown(f"<div class='group-header'>Группа {g}</div>", unsafe_allow_html=True)
                    st.markdown(
                        render_group_table(gdf, thirds_top8, played_gws, df),
                        unsafe_allow_html=True)

        st.markdown("""
        <div style='margin:8px 0 28px;font-size:.82rem;color:#8b949e;display:flex;gap:20px;flex-wrap:wrap;'>
          <span><span style='display:inline-block;width:12px;height:12px;
            background:rgba(0,223,122,.2);border-left:3px solid #00DF7A;
            margin-right:6px;vertical-align:middle;'></span>Проходит напрямую (топ-2)</span>
          <span><span style='display:inline-block;width:12px;height:12px;
            background:rgba(0,223,122,.35);border-left:3px solid #00ff8a;
            margin-right:6px;vertical-align:middle;'></span>Проходит как лучшее 3-е место</span>
          <span><span class='dot dot-g'></span> топ-33%
           <span class='dot dot-y'></span> середина
           <span class='dot dot-r'></span> аутсайдер (форма за 3 тура)</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>📋 Рейтинг 3-х мест</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8b949e;font-size:.88rem;margin-bottom:16px;'>Топ-8 из 12 третьих мест выходят в плей-офф</p>", unsafe_allow_html=True)
        html = "<table class='group-table' style='max-width:620px;'>"
        html += "<tr><th>#</th><th>Группа</th><th>Менеджер</th><th>Очки</th><th>Статус</th></tr>"
        for _, row in thirds.iterrows():
            rk = int(row["third_rank"])
            pts = row["group_pts"]
            pts_str = f"{int(pts)}" if not pd.isna(pts) else "–"
            is_q = rk <= 8
            row_cls = "highlight-row" if is_q else ""
            status = ("<span style='color:#00DF7A;font-weight:700;'>✅ В плей-офф</span>"
                      if is_q else "<span style='color:#8b949e;'>❌ Выбывает</span>")
            html += (f"<tr class='{row_cls}'><td><strong>#{rk}</strong></td>"
                     f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;"
                     f"padding:1px 8px;font-weight:700;'>{row['group_letter']}</span></td>"
                     f"<td>{row['manager_name']}</td>"
                     f"<td><strong>{pts_str}</strong></td><td>{status}</td></tr>")
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: СЕТКА ПЛЕЙ-ОФФ
# ─────────────────────────────────────────────
elif "Плей-офф" in page or "Кубка" in page:
    st.markdown("<div class='sec-title'>🏆 Сетка Кубка — Плей-офф</div>", unsafe_allow_html=True)
    if not data_ok:
        st.error(f"⚠️ {err_msg}")
    elif not bracket_ok:
        st.error(f"⚠️ Ошибка построения сетки: `{bracket_err}`")
    else:
        for stage in ["r16","r8","r4","r2","final"]:
            label   = STAGE_LABELS[stage]
            gw      = STAGE_GW[stage]
            matches = bracket.get(stage, [])
            st.markdown(f"""
            <div style='margin:28px 0 12px;'>
              <span style='background:linear-gradient(90deg,#00DF7A,#00b862);color:#0d1117;
                font-weight:800;font-size:.95rem;border-radius:8px;padding:6px 20px;
                letter-spacing:.5px;'>{label} · {GW_LABELS[gw]}</span>
            </div>""", unsafe_allow_html=True)
            if not matches:
                st.markdown("<span class='waiting'>⏳ Ожидание предыдущего раунда</span>",
                            unsafe_allow_html=True); continue
            any_scores = any(
                not pd.isna(m["p1_score"]) or not pd.isna(m["p2_score"])
                for m in matches if m["p1_id"]!="TBD" and m["p2_id"]!="TBD")
            cols_n = 4 if stage in ("r16","r8","r4") else (2 if stage=="r2" else 1)
            cols = st.columns(min(cols_n, len(matches)))
            for i, m in enumerate(matches):
                with cols[i % len(cols)]:
                    if m["p1_id"]=="TBD" or m["p2_id"]=="TBD":
                        st.markdown("""<div class='match-card'>
                          <div class='match-player pending'><span>⏳ Ожидание</span>
                            <span class='match-score no-score'>?</span></div>
                          <div class='match-player pending'><span>⏳ Ожидание</span>
                            <span class='match-score no-score'>?</span></div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(render_match_card(m), unsafe_allow_html=True)
            if not any_scores:
                st.markdown(
                    f"<p style='color:#8b949e;font-size:.83rem;margin-top:6px;'>"
                    f"⏳ Результаты {GW_LABELS[gw]} ещё не заполнены</p>",
                    unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: ПРИЗОВОЙ ФОНД
# ─────────────────────────────────────────────
elif "Призовой" in page:
    st.markdown("<div class='sec-title'>💰 Призовой фонд и Награды</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#111916;border:1px solid #1a2e22;border-top:3px solid #00DF7A;
                border-radius:12px;padding:24px 28px;margin-bottom:28px;'>
      <div style='font-size:1.6rem;font-weight:800;color:#f5a623;margin-bottom:4px;'>🏆 480 000 ₸</div>
      <div style='color:#8b949e;font-size:.9rem;'>Общий призовой фонд Syndicate Fantasy ЧМ-2026</div>
    </div>
    <div class='prize-grid'>
      <div class='prize-cat'><h4>🏆 Кубок (Плей-офф)</h4><ul>
        <li><span>🥇 1 место</span><span>110 000 ₸</span></li>
        <li><span>🥈 2 место</span><span>50 000 ₸</span></li>
        <li><span>🥉 3 место</span><span>25 000 ₸</span></li>
      </ul></div>
      <div class='prize-cat'><h4>📊 Общий зачет (Classic)</h4><ul>
        <li><span>🥇 1 место</span><span>75 000 ₸</span></li>
        <li><span>🥈 2 место</span><span>40 000 ₸</span></li>
        <li><span>🥉 3 место</span><span>20 000 ₸</span></li>
      </ul></div>
      <div class='prize-cat'><h4>⚡ MVP туров</h4><ul>
        <li><span>Лучший тур × 8</span><span>20 000 ₸</span></li>
        <li><span style='color:#8b949e;font-size:.82rem;'>Итого</span><span style='color:#8b949e;'>160 000 ₸</span></li>
      </ul></div>
    </div>
    """, unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ {err_msg}")
    else:
        # MVP per gw
        st.markdown("<div class='sec-title'>⚡ MVP туров — 20 000 ₸ за каждый тур</div>",
                    unsafe_allow_html=True)
        html = "<table class='prize-table'>"
        html += "<tr><th>Тур</th><th>MVP — Лучший менеджер</th><th>Очки</th><th>Приз</th></tr>"
        for gw in GW_COLS:
            col_data = df[["manager_name",gw]].dropna(subset=[gw])
            if col_data.empty:
                html += (f"<tr><td class='neon'>{GW_LABELS[gw]}</td>"
                         f"<td><span class='waiting'>⏳ Ожидание</span></td>"
                         f"<td>–</td><td class='gold'>20 000 ₸</td></tr>")
            else:
                mp = col_data[gw].max()
                ws = " / ".join(col_data[col_data[gw]==mp]["manager_name"].tolist())
                html += (f"<tr><td class='neon'>{GW_LABELS[gw]}</td>"
                         f"<td><strong>{ws}</strong></td>"
                         f"<td class='gold'><strong>{int(mp)}</strong></td>"
                         f"<td class='gold'>20 000 ₸</td></tr>")
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

        # Classic overall
        st.markdown("<div class='sec-title'>📊 Общий зачёт (Classic) — топ-3 получают призы</div>",
                    unsafe_allow_html=True)
        classic_prizes = {1:"75 000 ₸", 2:"40 000 ₸", 3:"20 000 ₸"}
        if played_gws:
            overall = df.copy()
            overall["total_pts"] = overall[played_gws].sum(axis=1, min_count=1)
            overall = overall.sort_values("total_pts", ascending=False).reset_index(drop=True)
            html2 = "<table class='prize-table'><tr><th>#</th><th>Менеджер</th><th>Группа</th>"
            for g in played_gws: html2 += f"<th>{GW_LABELS[g]}</th>"
            html2 += "<th>Всего</th><th>Приз</th></tr>"
            for i, row in overall.head(10).iterrows():
                rk = i+1
                bm = {1:"🥇",2:"🥈",3:"🥉"}.get(rk,f"#{rk}")
                html2 += (f"<tr><td style='font-weight:700;color:#f5a623;'>{bm}</td>"
                          f"<td><strong>{row['manager_name']}</strong></td>"
                          f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;"
                          f"padding:1px 7px;font-size:.8rem;font-weight:700;'>{row['group_letter']}</span></td>")
                for g in played_gws:
                    v = row[g]; html2 += f"<td>{'–' if pd.isna(v) else int(v)}</td>"
                t = row["total_pts"]
                html2 += (f"<td><strong style='color:#00DF7A;'>{int(t) if not pd.isna(t) else '–'}</strong></td>"
                          f"<td class='gold'>{classic_prizes.get(rk,'—')}</td></tr>")
            html2 += "</table>"
            st.markdown(html2, unsafe_allow_html=True)
            if len(overall) > 10:
                with st.expander("Показать всех участников"):
                    rows_all = []
                    for i, row in overall.iterrows():
                        rk = i+1
                        entry = {"#":rk,"Менеджер":row["manager_name"],"Группа":row["group_letter"]}
                        for g in played_gws:
                            entry[GW_LABELS[g]] = int(row[g]) if not pd.isna(row[g]) else "–"
                        t = row["total_pts"]
                        entry["Всего"] = int(t) if not pd.isna(t) else "–"
                        rows_all.append(entry)
                    st.dataframe(pd.DataFrame(rows_all), use_container_width=True, hide_index=True)
        else:
            st.markdown("<span class='waiting'>⏳ Ожидание результатов первого тура</span>",
                        unsafe_allow_html=True)

        # Cup prizes
        st.markdown("<div class='sec-title'>🏆 Кубок — Итоговые призы плей-офф</div>",
                    unsafe_allow_html=True)
        cup = [("🥇","Победитель финала","110 000 ₸"),
               ("🥈","Финалист (2 место)","50 000 ₸"),
               ("🥉","Проигравший полуфиналист (3 место)","25 000 ₸")]
        html3 = "<table class='prize-table' style='max-width:520px;'>"
        html3 += "<tr><th>Место</th><th>Описание</th><th>Приз</th></tr>"
        for md, desc, prize in cup:
            html3 += f"<tr><td style='font-size:1.2rem;'>{md}</td><td>{desc}</td><td class='gold'>{prize}</td></tr>"
        html3 += "</table>"
        st.markdown(html3, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: АНАЛИТИКА ГРУПП
# ─────────────────────────────────────────────
elif "Аналитика" in page:
    st.markdown("<div class='sec-title'>🔬 Аналитика групп — Групповой этап</div>",
                unsafe_allow_html=True)
    if not data_ok:
        st.error(f"⚠️ {err_msg}")
    elif not played_gws or not any(g in played_gws for g in ["gw1","gw2","gw3"]):
        st.markdown("<span class='waiting'>⏳ Ожидание результатов группового этапа</span>",
                    unsafe_allow_html=True)
    else:
        gi = get_group_insights(gs)
        max_total = gi["total_pts"].max()
        min_total = gi["total_pts"].min()
        avg_total = gi["total_pts"].mean()
        death_grp = gi.iloc[0]["group_letter"]
        easy_grp  = gi.iloc[-1]["group_letter"]

        # ── top stat strip ──
        played_group_gws = [g for g in ["gw1","gw2","gw3"] if g in played_gws]
        st.markdown(f"""
        <div class='insight-strip'>
          <div class='insight-chip'>
            <div class='ic-val'>{int(max_total)}</div>
            <div class='ic-lbl'>Макс. сумма группы</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val'>{int(avg_total)}</div>
            <div class='ic-lbl'>Средняя сумма группы</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val'>{int(min_total)}</div>
            <div class='ic-lbl'>Мин. сумма группы</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val'>{len(played_group_gws)}/3</div>
            <div class='ic-lbl'>Туров группового этапа</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── explanation ──
        st.markdown(f"""
        <p style='color:#8b949e;font-size:.88rem;margin-bottom:20px;line-height:1.7;'>
          Рейтинг групп по <strong style='color:#e6edf3;'>суммарным очкам</strong>
          всех четырёх участников за туры 1–3.
          <span style='color:#f85149;font-weight:700;'>☠️ Группа смерти</span> —
          Группа <strong style='color:#f85149;'>{death_grp}</strong> (наибольшая сумма очков,
          самые сильные соперники). &nbsp;
          <span style='color:#3fb950;font-weight:700;'>✅ Проходная</span> —
          Группа <strong style='color:#3fb950;'>{easy_grp}</strong> (наименьшая сумма).
        </p>
        """, unsafe_allow_html=True)

        col_main, col_side = st.columns([3, 2])

        with col_main:
            st.markdown("<div class='sec-title'>📊 Рейтинг групп по силе</div>",
                        unsafe_allow_html=True)
            for _, row in gi.iterrows():
                g_letter = row["group_letter"]
                g_total  = row["total_pts"]
                g_avg    = row["avg_pts"]
                g_rank   = int(row["g_rank"])
                is_death = g_letter == death_grp
                is_easy  = g_letter == easy_grp
                card_cls = "death" if is_death else ("easy" if is_easy else "")
                bar_pct  = int(g_total / max_total * 100) if max_total > 0 else 0

                badge_html = ""
                if is_death:
                    badge_html = "<span class='g-badge badge-death'>☠️ Группа смерти</span>"
                elif is_easy:
                    badge_html = "<span class='g-badge badge-easy'>✅ Проходная</span>"

                # players list for tooltip
                g_players = gs[gs["group_letter"]==g_letter].sort_values(
                    "group_pts", ascending=False)
                players_str = " · ".join(
                    f"{r['manager_name']} ({int(r['group_pts']) if not pd.isna(r['group_pts']) else '–'})"
                    for _, r in g_players.iterrows()
                )

                st.markdown(f"""
                <div class='group-rank-card {card_cls}'>
                  <div class='g-num'>#{g_rank}</div>
                  <div class='g-letter'>{g_letter}</div>
                  <div class='g-info'>
                    <div class='g-total'>{int(g_total) if not pd.isna(g_total) else '–'} очков</div>
                    <div class='g-sub'>Среднее: {g_avg:.1f} · {players_str}</div>
                    <div class='g-mini-bar-wrap' style='margin-top:6px;'>
                      <div class='g-mini-bar-track'>
                        <div class='g-mini-bar-fill' style='width:{bar_pct}%'></div>
                      </div>
                    </div>
                  </div>
                  {badge_html}
                </div>
                """, unsafe_allow_html=True)

        with col_side:
            st.markdown("<div class='sec-title'>🏅 Топ-игроки группового этапа</div>",
                        unsafe_allow_html=True)
            top_players = gs.sort_values("group_pts", ascending=False).head(10)
            html_tp = "<table class='group-table'>"
            html_tp += "<tr><th>#</th><th>Менеджер</th><th>Группа</th><th>Очки</th></tr>"
            for i, (_, rw) in enumerate(top_players.iterrows()):
                rk  = i + 1
                bm  = {1:"🥇",2:"🥈",3:"🥉"}.get(rk, f"#{rk}")
                pts = rw["group_pts"]
                pts_str = f"{int(pts)}" if not pd.isna(pts) else "–"
                html_tp += (f"<tr><td style='font-weight:700;color:#f5a623;'>{bm}</td>"
                            f"<td><strong>{rw['manager_name']}</strong></td>"
                            f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;"
                            f"padding:1px 6px;font-weight:700;font-size:.8rem;'>{rw['group_letter']}</span></td>"
                            f"<td class='neon'><strong>{pts_str}</strong></td></tr>")
            html_tp += "</table>"
            st.markdown(html_tp, unsafe_allow_html=True)

            # ── group strength scatter: avg vs spread ──
            st.markdown("<div class='sec-title'>📈 Средние очки по группам</div>",
                        unsafe_allow_html=True)
            max_avg = gi["avg_pts"].max()
            html_avg = "<table class='group-table'>"
            html_avg += "<tr><th>Группа</th><th>Среднее</th><th>Макс</th><th>Мин</th></tr>"
            for _, rw in gi.iterrows():
                g = rw["group_letter"]
                avg_v = rw["avg_pts"]; max_v = rw["max_pts"]; min_v = rw["min_pts"]
                bar_w = int(avg_v / max_avg * 100) if max_avg > 0 else 0
                is_d = g == death_grp; is_e = g == easy_grp
                col_style = ("color:#f85149;font-weight:800;" if is_d else
                             "color:#3fb950;font-weight:800;" if is_e else "font-weight:700;")
                html_avg += (f"<tr>"
                             f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;"
                             f"padding:1px 7px;font-weight:800;'>{g}</span></td>"
                             f"<td style='{col_style}'>{avg_v:.1f}</td>"
                             f"<td style='color:#8b949e;'>{int(max_v) if not pd.isna(max_v) else '–'}</td>"
                             f"<td style='color:#8b949e;'>{int(min_v) if not pd.isna(min_v) else '–'}</td>"
                             f"</tr>")
            html_avg += "</table>"
            st.markdown(html_avg, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: ФИНАНСОВЫЙ ОТЧЁТ
# ─────────────────────────────────────────────
elif "Финансовый" in page:
    st.markdown("""
    <div class='fin-hero'>
      <h2>💳 Финансовый отчёт <span>MVP-призовых</span></h2>
      <div class='fh-sub'>
        Динамический расчёт заработанных призовых по MVP туров · При ничьей приз делится поровну
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ {err_msg}")
    elif not played_gws:
        st.markdown("<span class='waiting'>⏳ Ожидание результатов первого тура</span>",
                    unsafe_allow_html=True)
    else:
        earnings_df = calc_mvp_earnings(df)
        total_distributed = earnings_df["total_earned"].sum()
        remaining_pot     = 20_000 * (8 - len(played_gws))
        n_earners         = (earnings_df["total_earned"] > 0).sum()
        top_earner_name   = earnings_df.iloc[0]["manager_name"] if len(earnings_df) else "–"

        # ── summary chips ──
        st.markdown(f"""
        <div class='insight-strip'>
          <div class='insight-chip'>
            <div class='ic-val'>{int(total_distributed):,} ₸</div>
            <div class='ic-lbl'>Уже распределено</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val'>{int(remaining_pot):,} ₸</div>
            <div class='ic-lbl'>Ещё в игре (MVP)</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val'>{n_earners}</div>
            <div class='ic-lbl'>Менеджеров с призами</div>
          </div>
          <div class='insight-chip'>
            <div class='ic-val' style='font-size:1rem;'>{top_earner_name}</div>
            <div class='ic-lbl'>Лидер по MVP-призам</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        max_earned = earnings_df["total_earned"].max()
        top_earned_val = earnings_df.iloc[0]["total_earned"] if len(earnings_df) else 0

        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("<div class='sec-title'>🏆 Лидерборд MVP-заработка</div>",
                        unsafe_allow_html=True)
            st.markdown(
                "<p style='color:#8b949e;font-size:.83rem;margin-bottom:14px;'>"
                "Победа в туре = 1 очко (при ничьей — 0.5). "
                "Сумма призовых рассчитана с учётом долей при разделе.</p>",
                unsafe_allow_html=True)

            html_lb = "<table class='fin-leaderboard'>"
            html_lb += ("<tr><th>#</th><th>Менеджер</th><th>Группа</th>"
                        "<th>Побед в турах</th><th>Заработано</th><th>Доля от фонда</th></tr>")

            for i, row in earnings_df.iterrows():
                rk   = i + 1
                earned = row["total_earned"]
                wins   = row["mvp_wins"]
                bm     = {1:"🥇",2:"🥈",3:"🥉"}.get(rk, f"#{rk}")
                is_top = earned == top_earned_val and earned > 0
                row_cls = "top-earner" if is_top else ""

                # earn bar
                bar_w  = int(earned / max_earned * 100) if max_earned > 0 else 0
                share_pct = earned / 160_000 * 100 if earned > 0 else 0

                # mvp dots (full win = filled dot, half = half dot)
                dots_html = ""
                full_wins = int(wins)
                half_win  = (wins - full_wins) >= 0.4  # 0.5 share ≈ 0.5
                for _ in range(full_wins):
                    dots_html += "<span class='mvp-dot'></span>"
                if half_win:
                    dots_html += "<span class='mvp-dot-half'></span>"

                wins_display = f"{wins:.1f}".rstrip("0").rstrip(".")
                earned_str   = f"{int(earned):,} ₸" if earned > 0 else "—"
                earned_color = "#00DF7A" if is_top else ("#f5a623" if earned > 0 else "#3d444d")

                html_lb += (f"<tr class='{row_cls}'>"
                            f"<td style='font-weight:700;color:#f5a623;'>{bm}</td>"
                            f"<td><strong>{row['manager_name']}</strong></td>"
                            f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;"
                            f"padding:1px 6px;font-weight:700;font-size:.8rem;'>"
                            f"{df.loc[df['manager_id']==row['manager_id'],'group_letter'].values[0] if not df[df['manager_id']==row['manager_id']].empty else '–'}"
                            f"</span></td>"
                            f"<td>{dots_html} <span style='color:#8b949e;font-size:.8rem;margin-left:4px;'>{wins_display}</span></td>"
                            f"<td>"
                            f"<div class='earning-bar'>"
                            f"<span style='color:{earned_color};font-weight:800;min-width:80px;'>{earned_str}</span>"
                            f"<div class='earning-track'><div class='earning-fill' style='width:{bar_w}%'></div></div>"
                            f"</div></td>"
                            f"<td style='color:#8b949e;font-size:.82rem;'>{share_pct:.1f}%</td>"
                            f"</tr>")
            html_lb += "</table>"
            st.markdown(html_lb, unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='sec-title'>⚡ Детализация по турам</div>",
                        unsafe_allow_html=True)
            # Per-gw MVP detail table
            html_gw = "<table class='gw-detail-table'>"
            html_gw += "<tr><th>Тур</th><th>MVP</th><th>Очки</th><th>Приз</th></tr>"
            for gw in GW_COLS:
                col_data = df[["manager_id","manager_name",gw]].dropna(subset=[gw])
                col_data = col_data[col_data[gw] > 0]
                if col_data.empty:
                    html_gw += (f"<tr><td class='neon'>{GW_LABELS[gw]}</td>"
                                f"<td><span class='waiting'>⏳</span></td>"
                                f"<td>–</td><td style='color:#3d444d;'>20 000 ₸</td></tr>")
                    continue
                max_sc  = col_data[gw].max()
                winners = col_data[col_data[gw] == max_sc]
                n_w     = len(winners)
                share   = 20_000 // n_w
                names   = " / ".join(winners["manager_name"].tolist())
                tie_note = f"<span style='color:#f5a623;font-size:.75rem;'> ÷{n_w}</span>" if n_w > 1 else ""
                html_gw += (f"<tr>"
                            f"<td class='neon'>{GW_LABELS[gw]}</td>"
                            f"<td><strong>{names}</strong>{tie_note}</td>"
                            f"<td style='color:#00DF7A;font-weight:700;'>{int(max_sc)}</td>"
                            f"<td style='color:#f5a623;font-weight:700;'>{share:,} ₸</td>"
                            f"</tr>")
            html_gw += "</table>"
            st.markdown(html_gw, unsafe_allow_html=True)

            # ── methodology note ──
            st.markdown("""
            <div style='background:#111916;border:1px solid #1a2e22;border-radius:10px;
                        padding:14px 16px;margin-top:16px;font-size:.82rem;color:#8b949e;
                        line-height:1.7;'>
              <strong style='color:#e6edf3;'>Методология расчёта:</strong><br>
              • Каждый тур: победитель получает <strong style='color:#f5a623;'>20 000 ₸</strong><br>
              • При ничьей приз делится поровну между всеми лидерами тура<br>
              • Дробные победы отображаются как
                <span class='mvp-dot-half'></span> (половинная)<br>
              • Итого MVP-фонд: <strong style='color:#f5a623;'>160 000 ₸</strong> (8 × 20 000 ₸)
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px;padding:16px;text-align:center;
            color:#1a2e22;font-size:.78rem;border-top:1px solid #111916;'>
  Syndicate Fantasy ЧМ-2026 · Данные из Google Sheets
</div>
""", unsafe_allow_html=True)
