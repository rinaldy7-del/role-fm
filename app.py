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

# --- DATABASE SELURUH ROLE ---
ROLES = {
    "🧤 GK: Goalkeeper (Defend)": {"pos_key": ["GK"], "core": ['Ref', '1v1', 'Han', 'Pos', 'Cnt'], "important": ['Aer', 'Cmd', 'Dec'], "standard": ['Kic', 'Com']},
    "🧤 GK: Sweeper Keeper (Su/At)": {"pos_key": ["GK"], "core": ['Fir', 'Pas', 'Cmp', 'Dec', 'TRO'], "important": ['Ref', 'Pos', 'Acc'], "standard": ['Kic', 'Vis']},
    "🛡 CB: Central Defender (Defend)": {"pos_key": ["D (C)"], "core": ['Mar', 'Tck', 'Pos', 'Str', 'Jum', 'Ant'], "important": ['Acc', 'Pac', 'Cnt', 'Dec'], "standard": ['Hea', 'Cmp', 'Sta']},
    "🛡 CB: Central Defender (Cover)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Ant', 'Pos'], "important": ['Mar', 'Tck', 'Dec', 'Cnt'], "standard": ['Str', 'Hea']},
    "🛡 CB: Ball Playing Defender (Defend)": {"pos_key": ["D (C)"], "core": ['Pas', 'Cmp', 'Pos', 'Dec', 'Ant'], "important": ['Acc', 'Pac', 'Mar', 'Tck'], "standard": ['Tec', 'Fir', 'Str']},
    "🏃 FB: Full Back (Defend)": {"pos_key": ["D (RL)"], "core": ['Acc', 'Pac', 'Tck', 'Pos', 'Sta'], "important": ['Mar', 'Wor', 'Dec'], "standard": ['Cro', 'Str']},
    "🏃 WB: Wing Back (Attack)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Tec', 'Wor', 'Dec'], "standard": ['Pas', 'Cmp']},
    "🏃 IWB: Inverted Wing Back (Support)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Pas', 'Dec', 'Pos'], "important": ['Fir', 'Cmp', 'Tck'], "standard": ['Vis', 'Sta']},
    "🧱 DM: Segundo Volante (Attack)": {"pos_key": ["DM"], "core": ['Acc', 'Sta', 'OtB', 'Fin', 'Wor'], "important": ['Lon', 'Dec', 'Ant', 'Pac'], "standard": ['Pas', 'Tec']},
    "⚙ CM: Box to Box": {"pos_key": ["M (C)", "DM"], "core": ['Sta', 'Wor', 'Acc', 'Ant', 'OtB'], "important": ['Pas', 'Tck', 'Dec', 'Pac'], "standard": ['Fin', 'Str']},
    "⚙ CM: Mezzala (Attack)": {"pos_key": ["M (C)"], "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'], "important": ['Pas', 'Vis', 'Dec'], "standard": ['Fin', 'Lon']},
    "🎯 AMC: Shadow Striker": {"pos_key": ["AM (C)"], "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Pac', 'Dec', 'Fir'], "standard": ['Dri', 'Lon']},
    "🪽 WING: Inside Forward (Attack)": {"pos_key": ["AM (RL)"], "core": ['Acc', 'Pac', 'Fin', 'OtB', 'Dri'], "important": ['Cmp', 'Ant'], "standard": ['Tec', 'Fir']},
    "🪽 WING: Inverted Winger (Attack)": {"pos_key": ["AM (RL)", "M (RL)"], "core": ['Acc', 'Pac', 'Dri', 'Tec', 'OtB'], "important": ['Pas', 'Dec'], "standard": ['Fin', 'Lon']},
    "⚽ ST: Advanced Forward": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Fir', 'Dec'], "standard": ['Dri', 'Tec']},
    "⚽ ST: Complete Forward": {"pos_key": ["ST (C)"], "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Str'], "important": ['Pac', 'Fir', 'Hea'], "standard": ['Tec', 'Pas']}
}

def calculate_role_score(row, role_name):
    cfg = ROLES[role_name]
    player_pos = str(row['Position'])
    is_compatible = any(key in player_pos for key in cfg['pos_key'])
    pos_multiplier = 1.0 if is_compatible else 0.3
    
    s_core = sum(row[a] for a in cfg['core']) * 5
    s_imp = sum(row[a] for a in cfg['important']) * 3
    s_std = sum(row[a] for a in cfg['standard']) * 2
    
    max_score = (len(cfg['core']) * 20 * 5) + (len(cfg['important']) * 20 * 3) + (len(cfg['standard']) * 20 * 2)
    base_norm = (s_core + s_imp + s_std) / max_score * 100
    
    dev_cons, dev_imp = row['Cons'] - 10, row['Imp M'] - 10
    hidden_pct = max(-0.10, min(0.10, (dev_cons * 0.008) + (dev_imp * 0.005)))
    return round(base_norm * pos_multiplier * (1 + hidden_pct), 2)

# --- UI ---
st.title("🏆 FM24 Pro Role Calculator")

if df_raw is not None:
    st.sidebar.header("Taktik")
    selected_role = st.sidebar.selectbox("Pilih Role", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal Ability (Internal)", 0, 200, 120)
    search_q = st.sidebar.text_input("Cari Nama")

    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    res = df_calc[df_calc['CA'] >= min_ca].sort_values(by='Score', ascending=False)
    if search_q: res = res[res['Name'].str.contains(search_q, case=False)]

    # --- KEMBALIKAN HIGHLIGHT TOP 3 ---
    if not res.empty:
        st.subheader("High Recommendation")
        c1, c2, c3 = st.columns(3)
        c1.metric("🥇 Rank 1", res.iloc[0]['Name'], f"{res.iloc[0]['Score']}%")
        if len(res) > 1:
            c2.metric("🥈 Rank 2", res.iloc[1]['Name'], f"{res.iloc[1]['Score']}%")
        if len(res) > 2:
            c3.metric("🥉 Rank 3", res.iloc[2]['Name'], f"{res.iloc[2]['Score']}%")

    st.divider()
    # Tampilkan tabel tanpa kolom CA
    st.dataframe(res[['Name', 'Position', 'Score', 'PA', 'Cons', 'Imp M']], use_container_width=True, hide_index=True)
else:
    st.error("File 'database.xlsx' tidak ditemukan!")
