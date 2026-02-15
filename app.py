import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="FM24 Master Role Calculator", layout="wide")

# --- DATABASE ENGINE ---
@st.cache_data
def load_database():
    # Nama file baru sesuai yang Anda ubah
    file_name = "database.xlsx"
    
    if os.path.exists(file_name):
        try:
            return pd.read_excel(file_name)
        except Exception as e:
            # Jika excel error, coba baca sebagai CSV (jaga-jaga jika format tertukar)
            try:
                return pd.read_csv(file_name)
            except:
                st.error(f"Gagal membaca file: {e}")
                return None
    return None

df_raw = load_database()

# --- DEFINISI SEMUA ROLE (GLOBAL META RULE) ---
ROLES = {
    "🧤 GK: Goalkeeper (Defend)": {
        "core": ['Ref', '1v1', 'Han', 'Pos', 'Cnt'],
        "important": ['Aer', 'Cmd', 'Dec'],
        "standard": ['Kic', 'Com']
    },
    "🧤 GK: Sweeper Keeper (Su/At)": {
        "core": ['Fir', 'Pas', 'Cmp', 'Dec', 'TRO'],
        "important": ['Ref', 'Pos', 'Acc'],
        "standard": ['Kic', 'Vis']
    },
    "🛡 CB: Central Defender (Defend)": {
        "core": ['Mar', 'Tck', 'Pos', 'Str', 'Jum', 'Ant'],
        "important": ['Acc', 'Pac', 'Cnt', 'Dec'],
        "standard": ['Hea', 'Cmp', 'Sta']
    },
    "🛡 CB: Central Defender (Cover)": {
        "core": ['Acc', 'Pac', 'Ant', 'Pos'],
        "important": ['Mar', 'Tck', 'Dec', 'Cnt'],
        "standard": ['Str', 'Hea']
    },
    "🛡 CB: Ball Playing Defender (Defend)": {
        "core": ['Pas', 'Cmp', 'Pos', 'Dec', 'Ant'],
        "important": ['Acc', 'Pac', 'Mar', 'Tck'],
        "standard": ['Tec', 'Fir', 'Str']
    },
    "🛡 CB: Ball Playing Defender (Cover)": {
        "core": ['Acc', 'Pac', 'Pas', 'Ant', 'Pos'],
        "important": ['Dec', 'Cmp', 'Mar'],
        "standard": ['Tck', 'Tec']
    },
    "🏃 FB: Full Back (Defend)": {
        "core": ['Acc', 'Pac', 'Tck', 'Pos', 'Sta'],
        "important": ['Mar', 'Wor', 'Dec'],
        "standard": ['Cro', 'Str']
    },
    "🏃 WB: Wing Back (Support)": {
        "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro'],
        "important": ['Dri', 'OtB', 'Dec'],
        "standard": ['Pas', 'Tec', 'Tck']
    },
    "🏃 WB: Wing Back (Attack)": {
        "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'],
        "important": ['Tec', 'Wor', 'Dec'],
        "standard": ['Pas', 'Cmp']
    },
    "🏃 IWB: Inverted Wing Back (Support)": {
        "core": ['Acc', 'Pac', 'Pas', 'Dec', 'Pos'],
        "important": ['Fir', 'Cmp', 'Tck'],
        "standard": ['Vis', 'Sta']
    },
    "🧱 DM: Anchor": {
        "core": ['Pos', 'Ant', 'Tck', 'Str', 'Cnt'],
        "important": ['Acc', 'Pac', 'Dec'],
        "standard": ['Pas', 'Sta']
    },
    "🧱 DM: Defensive Midfielder (Support)": {
        "core": ['Pos', 'Pas', 'Dec', 'Ant'],
        "important": ['Acc', 'Pac', 'Tck', 'Cmp'],
        "standard": ['Sta', 'Str']
    },
    "🧱 DM: Segundo Volante (Attack)": {
        "core": ['Acc', 'Sta', 'OtB', 'Fin', 'Wor'],
        "important": ['Lon', 'Dec', 'Ant', 'Pac'],
        "standard": ['Pas', 'Tec']
    },
    "🧱 DM: Regista": {
        "core": ['Pas', 'Vis', 'Cmp', 'Dec'],
        "important": ['Fir', 'Acc', 'Ant'],
        "standard": ['Tec', 'Sta']
    },
    "⚙ CM: Box to Box": {
        "core": ['Sta', 'Wor', 'Acc', 'Ant', 'OtB'],
        "important": ['Pas', 'Tck', 'Dec', 'Pac'],
        "standard": ['Fin', 'Str']
    },
    "⚙ CM: Ball Winning Midfielder": {
        "core": ['Tck', 'Agg', 'Wor', 'Acc', 'Sta'],
        "important": ['Ant', 'Str', 'Pos'],
        "standard": ['Pas', 'Dec']
    },
    "⚙ CM: Mezzala (Attack)": {
        "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'],
        "important": ['Pas', 'Vis', 'Dec'],
        "standard": ['Fin', 'Lon']
    },
    "🎯 AMC: Shadow Striker": {
        "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Ant'],
        "important": ['Pac', 'Dec', 'Fir'],
        "standard": ['Dri', 'Lon']
    },
    "🎯 AMC: Advanced Playmaker (Attack)": {
        "core": ['Pas', 'Vis', 'Tec', 'Dec', 'Cmp'],
        "important": ['Acc', 'OtB'],
        "standard": ['Dri', 'Lon']
    },
    "🪽 WING: Winger (Attack)": {
        "core": ['Acc', 'Pac', 'Dri', 'Cro', 'OtB'],
        "important": ['Tec', 'Dec'],
        "standard": ['Fin', 'Fir']
    },
    "🪽 WING: Inside Forward (Attack)": {
        "core": ['Acc', 'Pac', 'Fin', 'OtB', 'Dri'],
        "important": ['Cmp', 'Ant'],
        "standard": ['Tec', 'Fir']
    },
    "🪽 WING: Inverted Winger (Attack)": {
        "core": ['Acc', 'Pac', 'Dri', 'Tec', 'OtB'],
        "important": ['Pas', 'Dec'],
        "standard": ['Fin', 'Lon']
    },
    "🪽 WING: Raumdeuter": {
        "core": ['Acc', 'OtB', 'Ant', 'Fin'],
        "important": ['Pac', 'Cmp'],
        "standard": ['Fir']
    },
    "⚽ ST: Advanced Forward": {
        "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'],
        "important": ['Fir', 'Dec'],
        "standard": ['Dri', 'Tec']
    },
    "⚽ ST: Pressing Forward (Attack)": {
        "core": ['Acc', 'Wor', 'Sta', 'OtB', 'Fin'],
        "important": ['Pac', 'Agg', 'Ant'],
        "standard": ['Str', 'Fir']
    },
    "⚽ ST: Complete Forward": {
        "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Str'],
        "important": ['Pac', 'Fir', 'Hea'],
        "standard": ['Tec', 'Pas']
    },
    "⚽ ST: Target Forward": {
        "core": ['Str', 'Jum', 'Hea', 'Bra'],
        "important": ['Fin', 'OtB', 'Acc'],
        "standard": ['Cmp', 'Ant']
    },
    "⚽ ST: Poacher": {
        "core": ['Acc', 'OtB', 'Fin', 'Ant'],
        "important": ['Pac', 'Cmp'],
        "standard": ['Fir']
    }
}

def calculate_role_score(row, role_name):
    cfg = ROLES[role_name]
    s_core = sum(row[a] for a in cfg['core']) * 5
    s_imp = sum(row[a] for a in cfg['important']) * 3
    s_std = sum(row[a] for a in cfg['standard']) * 2
    
    current_score = s_core + s_imp + s_std
    max_score = (len(cfg['core']) * 20 * 5) + (len(cfg['important']) * 20 * 3) + (len(cfg['standard']) * 20 * 2)
    base_norm = (current_score / max_score) * 100
    
    dev_cons = row['Cons'] - 10
    dev_imp = row['Imp M'] - 10
    hidden_pct = (dev_cons * 0.008) + (dev_imp * 0.005)
    hidden_pct = max(-0.10, min(0.10, hidden_pct))
    
    final_score = base_norm * (1 + hidden_pct)
    return round(final_score, 2)

# --- UI TAMPILAN ---
st.title("🏆 FM24 Pro Role Calculator")

if df_raw is not None:
    st.sidebar.header("Konfigurasi")
    selected_role = st.sidebar.selectbox("Pilih Role Pemain", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal Current Ability (CA)", 0, 200, 140)
    search_query = st.sidebar.text_input("Cari Nama Pemain")

    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    
    res = df_calc[df_calc['CA'] >= min_ca]
    if search_query:
        res = res[res['Name'].str.contains(search_query, case=False)]
    
    res = res.sort_values(by='Score', ascending=False)

    if not res.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("🥇 Best Fit", res.iloc[0]['Name'], f"{res.iloc[0]['Score']}%")
        if len(res) > 1:
            c2.metric("🥈 Second Best", res.iloc[1]['Name'], f"{res.iloc[1]['Score']}%")
        if len(res) > 2:
            c3.metric("🥉 Third Best", res.iloc[2]['Name'], f"{res.iloc[2]['Score']}%")

    st.divider()
    st.dataframe(res[['Name', 'Position', 'Score', 'CA', 'PA', 'Cons', 'Imp M']], use_container_width=True, hide_index=True)
else:
    st.error("Database 'database.xlsx' tidak ditemukan! Pastikan file tersebut sudah di-upload ke GitHub dengan nama yang persis sama.")
