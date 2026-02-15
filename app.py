import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="FM24 Master Meta Calculator", layout="wide")

@st.cache_data
def load_database():
    file_name = "database.xlsx"
    if os.path.exists(file_name):
        try:
            return pd.read_excel(file_name)
        except:
            return pd.read_csv(file_name)
    return None

df_raw = load_database()

# --- DATABASE SELURUH ROLE (GABUNGAN LAMA & BARU) ---
ROLES = {
    # --- 1) FULLBACK / WINGBACK / WIDE CB ---
    "🏃 FB: No-Nonsense Full Back (Defend)": {"pos_key": ["D (RL)", "D (L)", "D (R)"], "core": ['Tck', 'Mar', 'Pos', 'Str', 'Cnt'], "important": ['Acc', 'Pac', 'Ant', 'Bra'], "standard": ['Sta', 'Wor', 'Hea', 'Jum']},
    "🏃 WB: Complete Wing Back (Support)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro', 'Dri'], "important": ['Tec', 'OtB', 'Pas', 'Dec', 'Fir'], "standard": ['Cmp', 'Ant', 'Agi', 'Bal']},
    "🏃 WB: Wing Back (Attack)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Tec', 'Wor', 'Dec', 'Ant'], "standard": ['Pas', 'Cmp']},
    "🛡 WCB: Wide Centre Back (Attack)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Wor', 'Pas', 'Tec', 'Dec', 'Cmp'], "standard": ['Pos', 'Tck', 'Ant']},

    # --- 2) CENTRE BACK ---
    "🛡 CB: Ball Playing Defender (Defend)": {"pos_key": ["D (C)"], "core": ['Pas', 'Cmp', 'Pos', 'Dec', 'Ant'], "important": ['Acc', 'Pac', 'Mar', 'Tck'], "standard": ['Tec', 'Fir', 'Str']},
    "🛡 CB: No-Nonsense Centre Back (Defend)": {"pos_key": ["D (C)"], "core": ['Mar', 'Tck', 'Hea', 'Jum', 'Str', 'Pos'], "important": ['Acc', 'Pac', 'Cnt', 'Bra', 'Ant'], "standard": ['Dec', 'Cmp', 'Agg', 'Sta']},
    "🛡 LIB: Libero (Support)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Pas', 'Fir', 'Cmp', 'Dec', 'Pos'], "important": ['Tec', 'Vis', 'Ant', 'Tck', 'Mar'], "standard": ['Dri', 'Sta', 'Wor', 'Hea']},

    # --- 3) MIDFIELDERS ---
    "🧱 DLP: Deep-Lying Playmaker (Defend)": {"pos_key": ["DM", "M (C)"], "core": ['Pas', 'Vis', 'Dec', 'Cmp', 'Pos'], "important": ['Fir', 'Tec', 'Ant', 'Tea', 'Acc'], "standard": ['Pac', 'Sta', 'Tck', 'Cnt']},
    "⚙ RP: Roaming Playmaker (Support)": {"pos_key": ["DM", "M (C)"], "core": ['Acc', 'Sta', 'Wor', 'Pas', 'Vis', 'Dec', 'Dri'], "important": ['Fir', 'Tec', 'Cmp', 'Ant', 'Pac'], "standard": ['OtB', 'Bal', 'Agi', 'Tea']},
    "⚙ CM: Mezzala (Attack)": {"pos_key": ["M (C)"], "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'], "important": ['Pas', 'Vis', 'Dec', 'Pac'], "standard": ['Fin', 'Lon', 'Fir']},
    "⚙ CM: Box-to-Box Midfielder (Support)": {"pos_key": ["M (C)", "DM"], "core": ['Sta', 'Wor', 'Acc', 'Pac', 'Tea', 'OtB'], "important": ['Pas', 'Tck', 'Dec', 'Ant', 'Str'], "standard": ['Fin', 'Lon', 'Cmp', 'Fir']},
    "⚙ CAR: Carrilero (Support)": {"pos_key": ["M (C)"], "core": ['Sta', 'Wor', 'Tea', 'Pos', 'Acc', 'Pas'], "important": ['Pac', 'Dec', 'Ant', 'Tck'], "standard": ['Fir', 'Tec', 'Cnt', 'Mar']},

    # --- 4) ATTACKING MID & WINGERS ---
    "🎯 AM: Attacking Midfielder (Attack)": {"pos_key": ["AM (C)"], "core": ['Acc', 'OtB', 'Fir', 'Tec', 'Cmp', 'Dec'], "important": ['Pac', 'Fin', 'Vis', 'Ant'], "standard": ['Dri', 'Lon', 'Pas']},
    "🎯 AMC: Shadow Striker": {"pos_key": ["AM (C)"], "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Pac', 'Dec', 'Fir', 'Pas'], "standard": ['Dri', 'Lon', 'Tec']},
    "🪽 WING: Inside Forward (Attack)": {"pos_key": ["AM (RL)"], "core": ['Acc', 'Pac', 'Fin', 'OtB', 'Dri'], "important": ['Cmp', 'Ant', 'Tec', 'Pas'], "standard": ['Fir', 'Dec', 'Vis']},
    "🪽 WTF: Wide Target Forward (Support)": {"pos_key": ["AM (RL)", "M (RL)"], "core": ['Str', 'Jum', 'Hea', 'Bra', 'Bal'], "important": ['Fir', 'OtB', 'Acc', 'Pac', 'Tea'], "standard": ['Fin', 'Pas', 'Cmp', 'Cro']},

    # --- 5) STRIKERS ---
    "⚽ ST: Advanced Forward": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Fir', 'Dec', 'Dri', 'Tec'], "standard": ['Pas', 'Sta', 'Hea']},
    "⚽ ST: Deep-Lying Forward (Support)": {"pos_key": ["ST (C)"], "core": ['Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Acc'], "important": ['Vis', 'OtB', 'Tea', 'Pac'], "standard": ['Str', 'Fin', 'Ant', 'Dri']},
    "⚽ ST: Target Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Str', 'Jum', 'Hea', 'Fin', 'Bra'], "important": ['OtB', 'Cmp', 'Acc', 'Ant'], "standard": ['Fir', 'Pac', 'Bal']},
    "⚽ ST: False Nine (Support)": {"pos_key": ["ST (C)"], "core": ['Fir', 'Pas', 'Tec', 'Vis', 'Cmp', 'Dec', 'Acc'], "important": ['OtB', 'Tea', 'Wor', 'Dri', 'Pac'], "standard": ['Lon', 'Fin', 'Ant']},
    "⚽ ST: Pressing Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'Wor', 'Sta', 'OtB', 'Fin'], "important": ['Ant', 'Str', 'Agg', 'Cmp'], "standard": ['Fir', 'Dec']}
}

def calculate_role_score(row, role_name):
    cfg = ROLES[role_name]
    # 1. Penalty Posisi
    player_pos = str(row['Position'])
    is_compatible = any(key in player_pos for key in cfg['pos_key'])
    pos_multiplier = 1.0 if is_compatible else 0.3
    
    # 2. Rumus Hitung Meta (x5, x3, x2)
    s_core = sum(row[a] for a in cfg['core'] if a in row) * 5
    s_imp = sum(row[a] for a in cfg['important'] if a in row) * 3
    s_std = sum(row[a] for a in cfg['standard'] if a in row) * 2
    
    max_score = (len(cfg['core']) * 20 * 5) + (len(cfg['important']) * 20 * 3) + (len(cfg['standard']) * 20 * 2)
    base_norm = (s_core + s_imp + s_std) / max_score * 100
    
    # 3. Hidden Modifier (Consistency & Important Matches)
    dev_cons = row['Cons'] - 10
    dev_imp = row['Imp M'] - 10
    hidden_pct = (dev_cons * 0.008) + (dev_imp * 0.005)
    hidden_pct = max(-0.10, min(0.10, hidden_pct)) # Clamp ±10%
    
    return round(base_norm * pos_multiplier * (1 + hidden_pct), 2)

# --- UI ---
st.title("🏆 FM24 Ultimate Meta Calculator")

if df_raw is not None:
    st.sidebar.header("Konfigurasi Taktik")
    selected_role = st.sidebar.selectbox("Pilih Role Pemain", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Filter Minimal Ability (Internal)", 0, 200, 130)
    
    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    res = df_calc[df_calc['CA'] >= min_ca].sort_values(by='Score', ascending=False)

    if not res.empty:
        st.subheader(f"Rekomendasi Terbaik untuk {selected_role}")
        c1, c2, c3 = st.columns(3)
        c1.metric("🥇 Rank 1", res.iloc[0]['Name'], f"{res.iloc[0]['Score']}%")
        if len(res) > 1: c2.metric("🥈 Rank 2", res.iloc[1]['Name'], f"{res.iloc[1]['Score']}%")
        if len(res) > 2: c3.metric("🥉 Rank 3", res.iloc[2]['Name'], f"{res.iloc[2]['Score']}%")

    st.divider()
    # Tampilkan tabel (Kolom CA disembunyikan sesuai permintaan)
    st.dataframe(res[['Name', 'Position', 'Score', 'PA', 'Cons', 'Imp M']], use_container_width=True, hide_index=True)
else:
    st.error("Database 'database.xlsx' tidak ditemukan!")
