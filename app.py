import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Syndicate Fantasy ЧМ-2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  — фирменный цвет #00DF7A
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ---------- base ---------- */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background: #0d1117; color: #e6edf3; }

  /* ---------- sidebar ---------- */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111916 0%, #0d1117 100%);
    border-right: 1px solid #1a2e22;
  }
  section[data-testid="stSidebar"] * { color: #e6edf3 !important; }

  /* ---------- radio nav fix — flexbox alignment ---------- */
  div[data-testid="stSidebarContent"] .stRadio > div {
    gap: 4px;
  }
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
    background: rgba(0, 223, 122, 0.10);
  }
  /* The radio circle button */
  div[data-testid="stSidebarContent"] .stRadio label > div:first-child {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0;
    margin-top: 0 !important;
  }
  /* Checked state — neon green accent */
  div[data-testid="stSidebarContent"] .stRadio label[data-checked="true"],
  div[data-testid="stSidebarContent"] .stRadio [aria-checked="true"] ~ div {
    background: rgba(0, 223, 122, 0.12);
    border-left: 3px solid #00DF7A;
  }

  /* ---------- hero ---------- */
  .hero {
    background: linear-gradient(135deg, #0d2018 0%, #0d1a14 50%, #0d1117 100%);
    border: 1px solid #00DF7A;
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: "⚽";
    font-size: 180px;
    position: absolute;
    right: -20px;
    top: -20px;
    opacity: 0.06;
  }
  .hero h1 { font-size: 2.6rem; font-weight: 800; margin: 0 0 8px; color: #fff; }
  .hero h1 span { color: #00DF7A; }
  .hero .sub { color: #8b949e; font-size: 1.05rem; margin-bottom: 24px; }
  .hero .prize-badge {
    display: inline-block;
    background: linear-gradient(90deg, #f5a623, #f0c040);
    color: #0d1117;
    font-weight: 700;
    font-size: 1.3rem;
    border-radius: 50px;
    padding: 8px 28px;
  }

  /* ---------- stat cards ---------- */
  .stat-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
  .stat-card {
    flex: 1; min-width: 140px;
    background: #111916;
    border: 1px solid #1a2e22;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
  }
  .stat-card .val { font-size: 2rem; font-weight: 800; color: #00DF7A; }
  .stat-card .lbl { font-size: 0.82rem; color: #8b949e; margin-top: 4px; }

  /* ---------- section title — neon green underline ---------- */
  .sec-title {
    font-size: 1.15rem; font-weight: 700; color: #e6edf3;
    border-left: 3px solid #00DF7A;
    padding-left: 12px;
    margin: 28px 0 14px;
  }

  /* ---------- info cards (регламент) ---------- */
  .info-grid { display: flex; flex-wrap: wrap; gap: 16px; }
  .info-card {
    flex: 1; min-width: 260px;
    background: #111916;
    border: 1px solid #1a2e22;
    border-radius: 12px;
    padding: 20px 22px;
  }
  .info-card h4 { font-size: 1rem; font-weight: 700; color: #00DF7A; margin: 0 0 10px; }
  .info-card ul { margin: 0; padding-left: 18px; color: #c9d1d9; font-size: 0.9rem; line-height: 1.8; }

  /* ---------- group tables ---------- */
  .group-header {
    display: inline-block;
    background: linear-gradient(90deg, #00DF7A, #00b862);
    color: #0d1117;
    font-weight: 800;
    font-size: 1rem;
    border-radius: 8px 8px 0 0;
    padding: 6px 18px;
    margin-bottom: 0;
    letter-spacing: 0.3px;
  }
  .group-table {
    width: 100%;
    border-collapse: collapse;
    background: #111916;
    border-radius: 0 8px 8px 8px;
    overflow: hidden;
    font-size: 0.88rem;
    border: 1px solid #1a2e22;
    margin-bottom: 20px;
  }
  .group-table th {
    background: #141f18;
    color: #8b949e;
    font-weight: 600;
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid #1a2e22;
  }
  .group-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #172015;
    color: #e6edf3;
  }
  .group-table tr:last-child td { border-bottom: none; }
  .rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px;
    border-radius: 50%;
    font-weight: 700; font-size: 0.8rem;
  }
  .rank-1 { background: #f5a623; color: #000; }
  .rank-2 { background: #00DF7A; color: #000; }
  .rank-3 { background: #3d444d; color: #e6edf3; }
  .rank-4 { background: #21262d; color: #8b949e; }

  /* neon green rows for qualifiers */
  .green-row td { background: rgba(0, 223, 122, 0.10) !important; }
  .green-row td:first-child { border-left: 3px solid #00DF7A; }
  .highlight-row td { background: rgba(0, 223, 122, 0.18) !important; }
  .highlight-row td:first-child { border-left: 3px solid #00ff8a; }

  /* ---------- playoff bracket ---------- */
  .match-card {
    background: #111916;
    border: 1px solid #1a2e22;
    border-left: 4px solid #00DF7A;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
    transition: border-color .2s, box-shadow .2s;
  }
  .match-card:hover {
    border-color: #00DF7A;
    box-shadow: 0 0 12px rgba(0, 223, 122, 0.15);
  }
  .match-player {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 14px;
    font-size: 0.88rem;
    color: #c9d1d9;
  }
  .match-player + .match-player { border-top: 1px solid #172015; }
  .match-player.winner {
    background: rgba(0, 223, 122, 0.15);
    font-weight: 700;
    color: #00DF7A;
  }
  .match-player.pending { color: #8b949e; font-style: italic; }
  .match-score {
    font-weight: 800;
    font-size: 1rem;
    color: #00DF7A;
    background: #0d1117;
    border-radius: 6px;
    padding: 2px 8px;
    min-width: 38px;
    text-align: center;
  }
  .match-score.no-score { color: #3d444d; }

  /* ---------- prize table ---------- */
  .prize-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  .prize-table th {
    background: #141f18;
    color: #8b949e;
    font-weight: 600;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #1a2e22;
  }
  .prize-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #172015;
    color: #e6edf3;
  }
  .prize-table tr:hover td { background: #141f18; }
  .gold { color: #f5a623; font-weight: 700; }
  .silver { color: #c9d1d9; font-weight: 700; }
  .neon { color: #00DF7A; font-weight: 700; }

  /* ---------- waiting badge ---------- */
  .waiting {
    display: inline-block;
    background: #141f18;
    color: #8b949e;
    border: 1px dashed #1a2e22;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.8rem;
  }

  /* ---------- prize breakdown cards ---------- */
  .prize-grid { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 28px; }
  .prize-cat {
    flex: 1; min-width: 220px;
    background: #111916;
    border: 1px solid #1a2e22;
    border-top: 3px solid #00DF7A;
    border-radius: 12px;
    padding: 18px 20px;
  }
  .prize-cat h4 { font-size: 0.95rem; font-weight: 700; color: #00DF7A; margin: 0 0 12px; }
  .prize-cat ul { margin: 0; padding-left: 0; list-style: none; color: #c9d1d9; font-size: 0.88rem; line-height: 2; }
  .prize-cat ul li { display: flex; justify-content: space-between; border-bottom: 1px solid #172015; }
  .prize-cat ul li:last-child { border-bottom: none; }
  .prize-cat ul li span { color: #f5a623; font-weight: 700; }

  /* Streamlit button override */
  .stButton > button {
    background: rgba(0, 223, 122, 0.12);
    border: 1px solid #00DF7A;
    color: #00DF7A !important;
    font-weight: 600;
    border-radius: 8px;
    transition: background .15s;
  }
  .stButton > button:hover {
    background: rgba(0, 223, 122, 0.22);
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
GW_COLS = ["gw1", "gw2", "gw3", "gw4", "gw5", "gw6", "gw7", "gw8"]
GW_LABELS = {
    "gw1": "Тур 1", "gw2": "Тур 2", "gw3": "Тур 3",
    "gw4": "Тур 4", "gw5": "Тур 5", "gw6": "Тур 6",
    "gw7": "Тур 7", "gw8": "Тур 8",
}

@st.cache_data(ttl=120, show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    """Load tournament data from a Google Sheets CSV export URL."""
    df = pd.read_csv(url)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in GW_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = np.nan
    df["group_letter"] = df["group_letter"].str.strip().str.upper()
    df["manager_name"] = df["manager_name"].str.strip()
    return df


def get_group_stage(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["group_pts"] = d[["gw1", "gw2", "gw3"]].sum(axis=1, min_count=1)
    d = d.sort_values(["group_letter", "group_pts"], ascending=[True, False])
    d["rank"] = d.groupby("group_letter")["group_pts"].rank(
        method="min", ascending=False
    ).astype(int)
    return d


def get_third_place_ranking(gs: pd.DataFrame) -> pd.DataFrame:
    thirds = gs[gs["rank"] == 3].copy()
    thirds = thirds.sort_values("group_pts", ascending=False).reset_index(drop=True)
    thirds["third_rank"] = thirds.index + 1
    return thirds


def get_playoff_qualifiers(gs: pd.DataFrame) -> pd.DataFrame:
    top2 = gs[gs["rank"] <= 2].copy()
    thirds = get_third_place_ranking(gs)
    thirds_qualified = thirds.head(8).copy()
    thirds_qualified["rank"] = 3
    qualifiers = pd.concat([top2, thirds_qualified], ignore_index=True)
    qualifiers["seed"] = 0
    groups_sorted = sorted(qualifiers["group_letter"].unique())
    seed = 1
    for rk in [1, 2]:
        for g in groups_sorted:
            mask = (qualifiers["group_letter"] == g) & (qualifiers["rank"] == rk)
            qualifiers.loc[mask, "seed"] = seed
            seed += 1
    third_ids = qualifiers.loc[qualifiers["rank"] == 3].index
    for i, idx in enumerate(third_ids):
        qualifiers.loc[idx, "seed"] = 25 + i
    qualifiers = qualifiers.sort_values("seed").reset_index(drop=True)
    return qualifiers


def build_r16_matchups(qualifiers: pd.DataFrame) -> list[dict]:
    q = qualifiers.sort_values("seed").reset_index(drop=True)
    players = q["manager_id"].tolist()
    n = len(players)
    matchups = []
    for i in range(n // 2):
        matchups.append({"p1_id": players[i], "p2_id": players[n - 1 - i]})
    return matchups


# ─────────────────────────────────────────────
# PLAYOFF ENGINE
# ─────────────────────────────────────────────
STAGE_GW = {
    "r16": "gw4", "r8": "gw5", "r4": "gw6", "r2": "gw7", "final": "gw8",
}
STAGE_LABELS = {
    "r16": "1/16 Финала", "r8": "1/8 Финала",
    "r4": "Четвертьфинал", "r2": "Полуфинал", "final": "Финал",
}


def score_val(df: pd.DataFrame, manager_id, gw: str):
    row = df[df["manager_id"] == manager_id]
    if row.empty:
        return np.nan
    v = row[gw].values[0]
    return v if not pd.isna(v) else np.nan


def match_result(df, p1_id, p2_id, gw):
    s1 = score_val(df, p1_id, gw)
    s2 = score_val(df, p2_id, gw)
    if pd.isna(s1) or pd.isna(s2):
        return s1, s2, None
    if s1 > s2:
        return s1, s2, p1_id
    elif s2 > s1:
        return s1, s2, p2_id
    else:
        gp1 = df.loc[df["manager_id"] == p1_id, "group_pts"].values[0] if "group_pts" in df.columns else 0
        gp2 = df.loc[df["manager_id"] == p2_id, "group_pts"].values[0] if "group_pts" in df.columns else 0
        return s1, s2, p1_id if gp1 >= gp2 else p2_id


def simulate_bracket(df, r16_matchups):
    gs = get_group_stage(df)
    df = df.merge(gs[["manager_id", "group_pts"]], on="manager_id", how="left")
    stages = {}
    current_matchups = [(m["p1_id"], m["p2_id"]) for m in r16_matchups]
    for stage in ["r16", "r8", "r4", "r2", "final"]:
        gw = STAGE_GW[stage]
        stage_matches = []
        for p1_id, p2_id in current_matchups:
            s1, s2, winner = match_result(df, p1_id, p2_id, gw)
            p1_name = df.loc[df["manager_id"] == p1_id, "manager_name"].values[0] if not df[df["manager_id"] == p1_id].empty else str(p1_id)
            p2_name = df.loc[df["manager_id"] == p2_id, "manager_name"].values[0] if not df[df["manager_id"] == p2_id].empty else str(p2_id)
            stage_matches.append({
                "p1_id": p1_id, "p1_name": p1_name, "p1_score": s1,
                "p2_id": p2_id, "p2_name": p2_name, "p2_score": s2,
                "winner": winner, "gw": gw,
            })
        stages[stage] = stage_matches
        winners = [m["winner"] for m in stage_matches]
        next_matchups = []
        for i in range(0, len(winners), 2):
            w1 = winners[i]
            w2 = winners[i + 1] if i + 1 < len(winners) else None
            next_matchups.append((w1 or "TBD", w2 or "TBD"))
        current_matchups = next_matchups
        if stage == "final":
            break
    return stages


# ─────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────
def render_match_card(match: dict) -> str:
    def player_row(name, score, is_winner, pending):
        cls = "match-player"
        if pending:
            cls += " pending"
        elif is_winner:
            cls += " winner"
        if pending:
            score_html = "<span class='match-score no-score'>?</span>"
        elif is_winner:
            score_html = f"<span class='match-score' style='color:#00DF7A'>{int(score)}</span>"
        else:
            score_html = f"<span class='match-score' style='color:#8b949e'>{int(score)}</span>"
        trophy = " 🏆" if is_winner and not pending else ""
        return f"<div class='{cls}'><span>{name}{trophy}</span>{score_html}</div>"

    pending = match["winner"] is None
    p1_win = (match["winner"] == match["p1_id"])
    p2_win = (match["winner"] == match["p2_id"])
    html = "<div class='match-card'>"
    html += player_row(match["p1_name"], match["p1_score"], p1_win, pending)
    html += player_row(match["p2_name"], match["p2_score"], p2_win, pending)
    html += "</div>"
    return html


def rank_badge(r: int) -> str:
    cls_map = {1: "rank-1", 2: "rank-2", 3: "rank-3", 4: "rank-4"}
    cls = cls_map.get(r, "rank-4")
    return f"<span class='rank-badge {cls}'>{r}</span>"


def render_group_table(group_df: pd.DataFrame, thirds_top8_ids: set) -> str:
    html = "<table class='group-table'>"
    html += "<tr><th>#</th><th>Менеджер</th><th>GW1</th><th>GW2</th><th>GW3</th><th>Сумма</th></tr>"
    for _, row in group_df.iterrows():
        r = int(row["rank"])
        pts = row["group_pts"]
        pts_str = f"{int(pts)}" if not pd.isna(pts) else "<span class='waiting'>ожидание</span>"

        def gw_cell(col):
            v = row[col]
            return f"{int(v)}" if not pd.isna(v) else "<span class='waiting'>–</span>"

        row_cls = ""
        if r <= 2:
            row_cls = "green-row"
        elif row["manager_id"] in thirds_top8_ids:
            row_cls = "highlight-row"

        html += f"<tr class='{row_cls}'>"
        html += f"<td>{rank_badge(r)}</td>"
        html += f"<td><strong>{row['manager_name']}</strong></td>"
        html += f"<td>{gw_cell('gw1')}</td>"
        html += f"<td>{gw_cell('gw2')}</td>"
        html += f"<td>{gw_cell('gw3')}</td>"
        html += f"<td><strong>{pts_str}</strong></td>"
        html += "</tr>"
    html += "</table>"
    return html


# ─────────────────────────────────────────────
# SIDEBAR NAV
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo
    try:
        st.image("logo.jpg", use_column_width=True)
    except Exception:
        st.markdown("""
        <div style='text-align:center;padding:8px 0 4px;'>
          <div style='font-size:2.4rem;'>⚽</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 8px 0 20px;'>
      <div style='font-weight:800; font-size:1.05rem; color:#00DF7A; letter-spacing:0.5px;'>Syndicate Fantasy</div>
      <div style='font-size:0.78rem; color:#8b949e;'>ЧМ-2026 · Турнир</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Навигация",
        ["🏠  Главная и Регламент",
         "📊  Групповой этап",
         "🏆  Сетка Кубка (Плей-офф)",
         "💰  Призовой фонд и Награды"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    csv_url = st.text_input(
        "🔗 URL таблицы (CSV)",
        value="https://docs.google.com/spreadsheets/d/e/2PACX-1vQb50AHXthD0sqfUUDaUoauxiUPZEJH2Dgf7PQg93K1ljiW6jKR8KMEK9rgKRfaEZJcNdb1NU4cJ76Q/pub?output=csv",
        help="Ссылка на Google Sheets в формате CSV (pub?output=csv)",
    )
    if st.button("🔄 Обновить данные", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(
        "<div style='color:#3d5c47;font-size:0.75rem;text-align:center;padding-top:8px;'>"
        "Данные обновляются каждые 2 мин</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
data_ok = False
df = pd.DataFrame()
err_msg = ""

try:
    with st.spinner("Загрузка данных..."):
        df = load_data(csv_url)
    data_ok = True
except Exception as e:
    err_msg = str(e)

if data_ok:
    gs = get_group_stage(df)
    thirds = get_third_place_ranking(gs)
    thirds_top8_ids = set(thirds.head(8)["manager_id"].tolist())
    try:
        qualifiers = get_playoff_qualifiers(gs)
        r16_matchups = build_r16_matchups(qualifiers)
        bracket = simulate_bracket(gs, r16_matchups)
        bracket_ok = True
    except Exception as e:
        bracket_ok = False
        bracket_err = str(e)
else:
    gs = pd.DataFrame()
    thirds = pd.DataFrame()
    thirds_top8_ids = set()
    bracket_ok = False
    bracket_err = err_msg


# ─────────────────────────────────────────────
# PAGE: ГЛАВНАЯ
# ─────────────────────────────────────────────
if "Главная" in page:
    # Logo on main page
    col_logo, col_hero = st.columns([1, 4])
    with col_logo:
        try:
            st.image("logo.jpg", use_column_width=True)
        except Exception:
            pass

    with col_hero:
        st.markdown("""
        <div class='hero'>
          <h1>⚽ <span>Syndicate</span> Fantasy ЧМ-2026</h1>
          <div class='sub'>Syndicate турнир среди 48 менеджеров · Чемпионат Мира 2026</div>
          <div class='prize-badge'>🏆 Призовой фонд: 480 000 ₸</div>
        </div>
        """, unsafe_allow_html=True)

    # Stat cards
    if data_ok:
        total = len(df)
        groups = df["group_letter"].nunique()
        gws_played = sum(1 for g in GW_COLS if df[g].notna().any())
        played_cols = [c for c in GW_COLS if df[c].notna().any()]
        max_pts = int(df[played_cols].sum(axis=1).max()) if played_cols else 0
    else:
        total, groups, gws_played, max_pts = 48, 12, 0, 0

    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-card'><div class='val'>{total}</div><div class='lbl'>Участников</div></div>
      <div class='stat-card'><div class='val'>{groups}</div><div class='lbl'>Групп</div></div>
      <div class='stat-card'><div class='val'>{gws_played} / 8</div><div class='lbl'>Туров сыграно</div></div>
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
        st.error(f"⚠️ Не удалось загрузить данные. Проверьте URL таблицы в боковом меню.\n\n`{err_msg}`")


# ─────────────────────────────────────────────
# PAGE: ГРУППОВОЙ ЭТАП
# ─────────────────────────────────────────────
elif "Групповой" in page:
    st.markdown("<div class='sec-title'>📊 Групповой этап — Таблицы групп</div>", unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ Не удалось загрузить данные: `{err_msg}`")
    else:
        groups_sorted = sorted(gs["group_letter"].unique())
        cols_per_row = 3
        for row_start in range(0, len(groups_sorted), cols_per_row):
            cols = st.columns(cols_per_row)
            for ci, g in enumerate(groups_sorted[row_start:row_start + cols_per_row]):
                group_df = gs[gs["group_letter"] == g].copy()
                with cols[ci]:
                    st.markdown(f"<div class='group-header'>Группа {g}</div>", unsafe_allow_html=True)
                    st.markdown(render_group_table(group_df, thirds_top8_ids), unsafe_allow_html=True)

        st.markdown("""
        <div style='margin: 8px 0 28px; font-size:0.82rem; color:#8b949e; display:flex; gap:20px; flex-wrap:wrap;'>
          <span><span style='display:inline-block;width:12px;height:12px;background:rgba(0,223,122,0.2);border-left:3px solid #00DF7A;margin-right:6px;vertical-align:middle;'></span>Проходит напрямую (топ-2)</span>
          <span><span style='display:inline-block;width:12px;height:12px;background:rgba(0,223,122,0.35);border-left:3px solid #00ff8a;margin-right:6px;vertical-align:middle;'></span>Проходит как лучшее 3-е место (топ-8)</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>📋 Рейтинг 3-х мест</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#8b949e;font-size:0.88rem;margin-bottom:16px;'>Топ-8 из 12 третьих мест выходят в плей-офф</p>", unsafe_allow_html=True)

        html = "<table class='group-table' style='max-width:600px;'>"
        html += "<tr><th>Рейтинг</th><th>Группа</th><th>Менеджер</th><th>Очки</th><th>Статус</th></tr>"
        for _, row in thirds.iterrows():
            rk = int(row["third_rank"])
            pts = row["group_pts"]
            pts_str = f"{int(pts)}" if not pd.isna(pts) else "–"
            is_qual = rk <= 8
            row_cls = "highlight-row" if is_qual else ""
            status = "<span style='color:#00DF7A;font-weight:700;'>✅ В плей-офф</span>" if is_qual else "<span style='color:#8b949e;'>❌ Выбывает</span>"
            html += f"<tr class='{row_cls}'>"
            html += f"<td><strong>#{rk}</strong></td>"
            html += f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;padding:1px 8px;font-weight:700;'>{row['group_letter']}</span></td>"
            html += f"<td>{row['manager_name']}</td>"
            html += f"<td><strong>{pts_str}</strong></td>"
            html += f"<td>{status}</td>"
            html += "</tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: СЕТКА ПЛЕЙ-ОФФ
# ─────────────────────────────────────────────
elif "Плей-офф" in page or "Кубка" in page:
    st.markdown("<div class='sec-title'>🏆 Сетка Кубка — Плей-офф</div>", unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ Не удалось загрузить данные: `{err_msg}`")
    elif not bracket_ok:
        st.error(f"⚠️ Ошибка построения сетки: `{bracket_err}`")
    else:
        for stage in ["r16", "r8", "r4", "r2", "final"]:
            label = STAGE_LABELS[stage]
            gw = STAGE_GW[stage]
            matches = bracket.get(stage, [])

            st.markdown(f"""
            <div style='margin: 28px 0 12px;'>
              <span style='background:linear-gradient(90deg,#00DF7A,#00b862);color:#0d1117;
                font-weight:800;font-size:0.95rem;border-radius:8px;padding:6px 20px;
                letter-spacing:0.5px;'>
                {label} · {GW_LABELS[gw]}
              </span>
            </div>
            """, unsafe_allow_html=True)

            if not matches:
                st.markdown("<span class='waiting'>⏳ Ожидание результатов предыдущего раунда</span>", unsafe_allow_html=True)
                continue

            any_scores = any(
                not pd.isna(m["p1_score"]) or not pd.isna(m["p2_score"])
                for m in matches if m["p1_id"] != "TBD" and m["p2_id"] != "TBD"
            )

            cols_n = 4 if stage in ("r16", "r8", "r4") else (2 if stage == "r2" else 1)
            cols = st.columns(min(cols_n, len(matches)))
            for i, match in enumerate(matches):
                with cols[i % len(cols)]:
                    if match["p1_id"] == "TBD" or match["p2_id"] == "TBD":
                        st.markdown("""
                        <div class='match-card'>
                          <div class='match-player pending'><span>⏳ Ожидание</span><span class='match-score no-score'>?</span></div>
                          <div class='match-player pending'><span>⏳ Ожидание</span><span class='match-score no-score'>?</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(render_match_card(match), unsafe_allow_html=True)

            if not any_scores:
                st.markdown(
                    f"<p style='color:#8b949e;font-size:0.83rem;margin-top:6px;'>"
                    f"⏳ Результаты {GW_LABELS[gw]} ещё не заполнены</p>",
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────
# PAGE: ПРИЗОВОЙ ФОНД
# ─────────────────────────────────────────────
elif "Призовой" in page:
    st.markdown("<div class='sec-title'>💰 Призовой фонд и Награды</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#111916;border:1px solid #1a2e22;border-top:3px solid #00DF7A;
                border-radius:12px;padding:24px 28px;margin-bottom:28px;'>
      <div style='font-size:1.6rem;font-weight:800;color:#f5a623;margin-bottom:4px;'>🏆 480 000 ₸</div>
      <div style='color:#8b949e;font-size:0.9rem;'>Общий призовой фонд Syndicate Fantasy ЧМ-2026</div>
    </div>
    """, unsafe_allow_html=True)

    # Prize breakdown cards
    st.markdown("""
    <div class='prize-grid'>
      <div class='prize-cat'>
        <h4>🏆 Кубок (Плей-офф)</h4>
        <ul>
          <li><span>🥇 1 место</span><span>110 000 ₸</span></li>
          <li><span>🥈 2 место</span><span>50 000 ₸</span></li>
          <li><span>🥉 3 место</span><span>25 000 ₸</span></li>
        </ul>
      </div>
      <div class='prize-cat'>
        <h4>📊 Общий зачет (Classic)</h4>
        <ul>
          <li><span>🥇 1 место</span><span>75 000 ₸</span></li>
          <li><span>🥈 2 место</span><span>40 000 ₸</span></li>
          <li><span>🥉 3 место</span><span>20 000 ₸</span></li>
        </ul>
      </div>
      <div class='prize-cat'>
        <h4>⚡ MVP туров</h4>
        <ul>
          <li><span>Лучший тур × 8</span><span>20 000 ₸</span></li>
          <li><span style='color:#8b949e;font-size:0.82rem;'>Итого</span><span style='color:#8b949e;'>160 000 ₸</span></li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not data_ok:
        st.error(f"⚠️ Не удалось загрузить данные: `{err_msg}`")
    else:
        # Per-gameweek MVP
        st.markdown("<div class='sec-title'>⚡ MVP туров — 20 000 ₸ за каждый тур</div>", unsafe_allow_html=True)

        prize_rows = []
        for gw in GW_COLS:
            col_data = df[["manager_name", gw]].dropna(subset=[gw])
            if col_data.empty:
                prize_rows.append({"Тур": GW_LABELS[gw], "Менеджер": "—", "Очки": "—",
                                   "Приз": "20 000 ₸", "Статус": "pending"})
            else:
                max_pts = col_data[gw].max()
                winners = col_data[col_data[gw] == max_pts]["manager_name"].tolist()
                prize_rows.append({"Тур": GW_LABELS[gw], "Менеджер": " / ".join(winners),
                                   "Очки": int(max_pts), "Приз": "20 000 ₸", "Статус": "done"})

        html = "<table class='prize-table'>"
        html += "<tr><th>Тур</th><th>MVP — Лучший менеджер</th><th>Очки</th><th>Приз</th></tr>"
        for r in prize_rows:
            if r["Статус"] == "pending":
                html += (f"<tr><td class='neon'>{r['Тур']}</td>"
                         f"<td><span class='waiting'>⏳ Ожидание результатов</span></td>"
                         f"<td>—</td><td class='gold'>{r['Приз']}</td></tr>")
            else:
                html += (f"<tr><td class='neon'>{r['Тур']}</td>"
                         f"<td><strong>{r['Менеджер']}</strong></td>"
                         f"<td class='gold'><strong>{r['Очки']}</strong></td>"
                         f"<td class='gold'>{r['Приз']}</td></tr>")
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

        # Classic overall leaderboard
        st.markdown("<div class='sec-title'>📊 Общий зачёт (Classic) — топ-3 получают призы</div>", unsafe_allow_html=True)

        played_gws = [g for g in GW_COLS if df[g].notna().any()]
        classic_prizes = {1: "75 000 ₸", 2: "40 000 ₸", 3: "20 000 ₸"}

        if played_gws:
            overall = df.copy()
            overall["total_pts"] = overall[played_gws].sum(axis=1, min_count=1)
            overall = overall.sort_values("total_pts", ascending=False).reset_index(drop=True)

            html2 = "<table class='prize-table'>"
            html2 += "<tr><th>#</th><th>Менеджер</th><th>Группа</th>"
            for g in played_gws:
                html2 += f"<th>{GW_LABELS[g]}</th>"
            html2 += "<th>Всего</th><th>Приз</th></tr>"

            for i, row in overall.head(10).iterrows():
                rk = i + 1
                badge_map = {1: "🥇", 2: "🥈", 3: "🥉"}
                rk_str = badge_map.get(rk, f"#{rk}")
                prize_str = classic_prizes.get(rk, "—")
                html2 += "<tr>"
                html2 += f"<td style='font-weight:700;color:#f5a623;'>{rk_str}</td>"
                html2 += f"<td><strong>{row['manager_name']}</strong></td>"
                html2 += f"<td><span style='background:#00DF7A;color:#0d1117;border-radius:4px;padding:1px 7px;font-size:0.8rem;font-weight:700;'>{row['group_letter']}</span></td>"
                for g in played_gws:
                    v = row[g]
                    html2 += f"<td>{'–' if pd.isna(v) else int(v)}</td>"
                total = row["total_pts"]
                html2 += f"<td><strong style='color:#00DF7A;'>{int(total) if not pd.isna(total) else '–'}</strong></td>"
                html2 += f"<td class='gold'>{prize_str}</td>"
                html2 += "</tr>"
            html2 += "</table>"
            st.markdown(html2, unsafe_allow_html=True)

            if len(overall) > 10:
                with st.expander("Показать всех участников"):
                    rows_all = []
                    for i, row in overall.iterrows():
                        rk = i + 1
                        entry = {"#": rk, "Менеджер": row["manager_name"], "Группа": row["group_letter"]}
                        for g in played_gws:
                            entry[GW_LABELS[g]] = int(row[g]) if not pd.isna(row[g]) else "–"
                        total = row["total_pts"]
                        entry["Всего"] = int(total) if not pd.isna(total) else "–"
                        rows_all.append(entry)
                    st.dataframe(pd.DataFrame(rows_all), use_container_width=True, hide_index=True)
        else:
            st.markdown("<span class='waiting'>⏳ Ожидание результатов первого тура</span>", unsafe_allow_html=True)

        # Cup (playoff) prizes
        st.markdown("<div class='sec-title'>🏆 Кубок — Итоговые призы плей-офф</div>", unsafe_allow_html=True)
        cup_prizes = [
            ("🥇", "Победитель финала (1 место)", "110 000 ₸"),
            ("🥈", "Финалист (2 место)", "50 000 ₸"),
            ("🥉", "Проигравший полуфиналист (3 место)", "25 000 ₸"),
        ]
        html3 = "<table class='prize-table' style='max-width:520px;'>"
        html3 += "<tr><th>Место</th><th>Описание</th><th>Приз</th></tr>"
        for medal, desc, prize in cup_prizes:
            html3 += f"<tr><td style='font-size:1.2rem;'>{medal}</td><td>{desc}</td><td class='gold'>{prize}</td></tr>"
        html3 += "</table>"
        st.markdown(html3, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px;padding:16px;text-align:center;color:#1a2e22;font-size:0.78rem;border-top:1px solid #111916;'>
  Syndicate Fantasy ЧМ-2026 · Обновляется каждые 2 минуты · Данные из Google Sheets
</div>
""", unsafe_allow_html=True)
