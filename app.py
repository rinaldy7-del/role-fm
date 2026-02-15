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

# --- DATABASE SELURUH ROLE (LENGKAP DENGAN PENALTY POSISI) ---
ROLES = {
    # GOALKEEPERS
    "🧤 GK: Goalkeeper (Defend)": {
        "pos_key": ["GK"],
        "core": ['Ref', '1v1', 'Han', 'Pos', 'Cnt'],
        "important": ['Aer', 'Cmd', 'Dec'],
        "standard": ['Kic', 'Com']
    },
    "🧤 GK: Sweeper Keeper (Su/At)": {
        "pos_key": ["GK"],
        "core": ['Fir', 'Pas', 'Cmp', 'Dec', 'TRO'],
        "important": ['Ref', 'Pos', 'Acc'],
        "standard": ['Kic', 'Vis']
    },
    # DEFENDERS
    "🛡 CB: Central Defender (Defend)": {
        "pos_key": ["D (C)"],
        "core": ['Mar', 'Tck', 'Pos', 'Str', 'Jum', 'Ant'],
        "important": ['Acc', 'Pac', 'Cnt', 'Dec'],
        "standard": ['Hea', 'Cmp', 'Sta']
    },
    "🛡 CB: Central Defender (Cover)": {
        "pos_key": ["D (C)"],
        "core": ['Acc', 'Pac', 'Ant', 'Pos'],
        "important": ['Mar', 'Tck', 'Dec', 'Cnt'],
        "standard": ['Str', 'Hea']
    },
    "🛡 CB: Ball Playing Defender (Defend)": {
        "pos_key": ["D (C)"],
        "core": ['Pas', 'Cmp', 'Pos', 'Dec', 'Ant'],
        "important": ['Acc', 'Pac', 'Mar', 'Tck'],
        "standard": ['Tec', 'Fir', 'Str']
    },
    # FULLBACKS / WINGBACKS
    "🏃 FB: Full Back (Defend)": {
        "pos_key": ["D (RL)"],
        "core": ['Acc', 'Pac', 'Tck', 'Pos', 'Sta'],
        "important": ['Mar', 'Wor', 'Dec'],
        "standard": ['Cro', 'Str']
    },
    "🏃 WB: Wing Back (Support)": {
        "pos_key": ["D (RL)", "WB"],
        "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro'],
        "important": ['Dri', 'OtB', 'Dec'],
        "standard": ['Pas', 'Tec', 'Tck']
    },
    "🏃 WB: Wing Back (Attack)": {
        "pos_key": ["D (RL)", "WB"],
        "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'],
        "important": ['Tec', 'Wor', 'Dec'],
        "standard": ['Pas', 'Cmp']
    },
    "🏃 IWB: Inverted Wing Back (Support)": {
        "pos_key": ["D (RL)", "WB"],
        "core": ['Acc', 'Pac', 'Pas', 'Dec', 'Pos'],
        "important": ['Fir', 'Cmp', 'Tck'],
        "standard": ['Vis', 'Sta']
    },
    # DEFENSIVE MIDFIELDERS
    "🧱 DM: Anchor": {
        "pos_key": ["DM"],
        "core": ['Pos', 'Ant', 'Tck', 'Str', 'Cnt'],
        "important": ['Acc', 'Pac', 'Dec'],
        "standard": ['Pas', 'Sta']
    },
    "🧱 DM: Segundo Volante (Attack)": {
        "pos_key": ["DM"],
        "core": ['Acc', 'Sta', 'OtB', 'Fin', 'Wor'],
        "important": ['Lon', 'Dec', 'Ant', 'Pac'],
        "standard": ['Pas', 'Tec']
    },
    "🧱 DM: Regista": {
        "pos_key": ["DM", "M (C)"],
        "core": ['Pas', 'Vis', 'Cmp', 'Dec'],
        "important": ['Fir', 'Acc', 'Ant'],
        "standard": ['Tec', 'Sta']
    },
    # CENTRAL MIDFIELDERS
    "⚙ CM: Box to Box": {
        "pos_key": ["M (C)", "DM"],
        "core": ['Sta', 'Wor', 'Acc', 'Ant', 'OtB'],
        "important": ['Pas', 'Tck', 'Dec', 'Pac'],
        "standard": ['Fin', 'Str']
    },
    "⚙ CM: Ball Winning Midfielder": {
        "pos_key": ["M (C)", "DM"],
        "core": ['Tck', 'Agg', 'Wor', 'Acc', 'Sta'],
        "important": ['Ant', 'Str', 'Pos'],
        "standard": ['Pas', 'Dec']
    },
    "⚙ CM: Mezzala (Attack)": {
        "pos_key": ["M (C)"],
        "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'],
        "important": ['Pas', 'Vis', 'Dec'],
        "standard": ['Fin', 'Lon']
    },
    # ATTACKING MIDFIELDERS
    "🎯 AMC: Shadow Striker": {
        "pos_key": ["AM (C)"],
        "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Ant'],
        "important": ['Pac', 'Dec', 'Fir'],
        "standard": ['Dri', 'Lon']
    },
    "🎯 AMC: Advanced Playmaker (Attack)": {
        "pos_key": ["AM (C)", "M (C)"],
        "core": ['Pas', 'Vis', 'Tec', 'Dec', 'Cmp'],
        "important": ['Acc', 'OtB'],
        "standard": ['Dri', 'Lon']
    },
    # WINGERS
    "🪽 WING: Winger (Attack)": {
        "pos_key": ["AM (RL)", "M (RL)"],
        "core": ['Acc', 'Pac', 'Dri', 'Cro', 'OtB'],
        "important": ['Tec', 'Dec'],
        "standard": ['Fin', 'Fir']
    },
    "🪽 WING: Inside Forward (Attack)": {
        "pos_key": ["AM (RL)"],
        "core": ['Acc', 'Pac', 'Fin', 'OtB', 'Dri'],
        "important": ['Cmp', 'Ant'],
        "standard": ['Tec', 'Fir']
    },
    "🪽 WING: Inverted Winger (Attack)": {
        "pos_key": ["AM (RL)", "M (RL)"],
        "core": ['Acc', 'Pac', 'Dri', 'Tec', 'OtB'],
        "important": ['Pas', 'Dec'],
        "standard": ['Fin', 'Lon']
    },
    "🪽 WING: Raumdeuter": {
        "pos_key": ["AM (L)", "AM (R)"],
        "core": ['Acc', 'OtB', 'Ant', 'Fin'],
        "important": ['Pac', 'Cmp'],
        "standard": ['Fir']
    },
    # STRIKERS
    "⚽ ST: Advanced Forward": {
        "pos_key": ["ST (C)"],
        "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'],
        "important": ['Fir', 'Dec'],
        "standard": ['Dri', 'Tec']
    },
    "⚽ ST: Pressing Forward (Attack)": {
        "pos_key": ["ST (C)"],
        "core": ['Acc', 'Wor', 'Sta', 'OtB', 'Fin'],
        "important": ['Pac', 'Agg', 'Ant'],
        "standard": ['Str', 'Fir']
    },
    "⚽ ST: Complete Forward": {
        "pos_key": ["ST (C)"],
        "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Str'],
        "important": ['Pac', 'Fir', 'Hea'],
        "standard": ['Tec', 'Pas']
    },
    "⚽ ST: Target Forward": {
        "pos_key": ["ST (C)"],
        "core": ['Str', 'Jum', 'Hea', 'Bra'],
        "important": ['Fin', 'OtB', 'Acc'],
        "standard": ['Cmp', 'Ant']
    },
    "⚽ ST: Poacher": {
        "pos_key": ["ST (C)"],
        "core": ['Acc', 'OtB', 'Fin', 'Ant'],
        "important": ['Pac', 'Cmp'],
        "standard": ['Fir']
    }
}

def calculate_role_score(row, role_name):
    cfg = ROLES[role_name]
    
    # 1. POSITION PENALTY (Logic Baru)
    player_pos = str(row['Position'])
    is_compatible = any(key in player_pos for key in cfg['pos_key'])
    pos_multiplier = 1.0 if is_compatible else 0.3 # Penalti 70% jika tidak cocok
    
    # 2. ATTRIBUTE SCORE (x5, x3, x2)
    s_core = sum(row[a] for a in cfg['core']) * 5
    s_imp = sum(row[a] for a in cfg['important']) * 3
    s_std = sum(row[a] for a in cfg['standard']) * 2
    
    current_score = s_core + s_imp + s_std
    max_score = (len(cfg['core']) * 20 * 5) + (len(cfg['important']) * 20 * 3) + (len(cfg['standard']) * 20 * 2)
    base_norm = (current_score / max_score) * 100
    
    # 3. HIDDEN MODIFIER
    dev_cons = row['Cons'] - 10
    dev_imp = row['Imp M'] - 10
    hidden_pct = (dev_cons * 0.008) + (dev_imp * 0.005)
    hidden_pct = max(-0.10, min(0.10, hidden_pct))
    
    # 4. FINAL ASSEMBLY
    final_score = base_norm * pos_multiplier * (1 + hidden_pct)
    return round(final_score, 2)

# --- UI ---
st.title("🏆 FM24 Meta Role Calculator")
st.info("Pemain di luar posisi natural akan menerima penalti skor yang signifikan.")

if df_raw is not None:
    st.sidebar.header("Taktik & Filter")
    selected_role = st.sidebar.selectbox("Pilih Role", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal CA", 0, 200, 120)
    search_query = st.sidebar.text_input("Cari Pemain")

    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    
    res = df_calc[df_calc['CA'] >= min_ca].sort_values(by='Score', ascending=False)
    
    if search_query:
        res = res[res['Name'].str.contains(search_query, case=False)]

    st.subheader(f"Daftar Pemain Terbaik: {selected_role}")
    st.dataframe(res[['Name', 'Position', 'Score', 'CA', 'PA', 'Cons']], use_container_width=True, hide_index=True)
else:
    st.error("Database tidak ditemukan!")
