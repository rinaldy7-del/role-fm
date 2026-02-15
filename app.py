import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="FM24 Master Meta Calculator", layout="wide")

@st.cache_data
def load_database():
    file_name = "db.xlsx"
    if os.path.exists(file_name):
        try:
            return pd.read_excel(file_name)
        except:
            try:
                return pd.read_csv(file_name)
            except:
                return None
    return None

df_raw = load_database()

# --- DATABASE SELURUH ROLE (GABUNGAN LENGKAP 50+ ROLE) ---
ROLES = {
    # 🧤 GOALKEEPERS
    "🧤 GK: Goalkeeper (Defend)": {"pos_key": ["GK"], "core": ['Ref', '1v1', 'Han', 'Pos', 'Cnt'], "important": ['Aer', 'Cmd', 'Dec'], "standard": ['Kic', 'Com']},
    "🧤 GK: Sweeper Keeper (Su/At)": {"pos_key": ["GK"], "core": ['Fir', 'Pas', 'Cmp', 'Dec', 'TRO'], "important": ['Ref', 'Pos', 'Acc'], "standard": ['Kic', 'Vis']},
    
    # 🛡 CENTRE BACKS
    "🛡 CB: Central Defender (Defend)": {"pos_key": ["D (C)"], "core": ['Mar', 'Tck', 'Pos', 'Str', 'Jum', 'Ant'], "important": ['Acc', 'Pac', 'Cnt', 'Dec'], "standard": ['Hea', 'Cmp', 'Sta']},
    "🛡 CB: Central Defender (Cover)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Ant', 'Pos'], "important": ['Mar', 'Tck', 'Dec', 'Cnt'], "standard": ['Str', 'Hea']},
    "🛡 CB: Ball Playing Defender (Defend)": {"pos_key": ["D (C)"], "core": ['Pas', 'Cmp', 'Pos', 'Dec', 'Ant'], "important": ['Acc', 'Pac', 'Mar', 'Tck'], "standard": ['Tec', 'Fir', 'Str']},
    "🛡 CB: Ball Playing Defender (Cover)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Pas', 'Ant', 'Pos'], "important": ['Dec', 'Cmp', 'Mar'], "standard": ['Tck', 'Tec']},
    "🛡 CB: No-Nonsense Centre Back (Defend)": {"pos_key": ["D (C)"], "core": ['Mar', 'Tck', 'Hea', 'Jum', 'Str', 'Pos'], "important": ['Acc', 'Pac', 'Cnt', 'Bra', 'Ant'], "standard": ['Dec', 'Cmp', 'Agg', 'Sta']},
    "🛡 LIB: Libero (Support)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Pas', 'Fir', 'Cmp', 'Dec', 'Pos'], "important": ['Tec', 'Vis', 'Ant', 'Tck', 'Mar'], "standard": ['Dri', 'Sta', 'Wor', 'Hea']},
    "🛡 LIB: Libero (Attack)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Dri', 'Pas', 'Fir', 'Cmp', 'Dec'], "important": ['Tec', 'Vis', 'OtB', 'Ant'], "standard": ['Sta', 'Wor', 'Fin', 'Lon', 'Pos']},
    "🛡 WCB: Wide Centre Back (Defend)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Pos', 'Tck', 'Mar', 'Sta'], "important": ['Ant', 'Dec', 'Cro', 'Pas', 'Wor'], "standard": ['Str', 'Hea', 'Jum', 'Cmp']},
    "🛡 WCB: Wide Centre Back (Support)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro', 'Pas'], "important": ['Dri', 'OtB', 'Dec', 'Ant', 'Pos'], "standard": ['Tck', 'Mar', 'Cmp']},
    "🛡 WCB: Wide Centre Back (Attack)": {"pos_key": ["D (C)"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Wor', 'Pas', 'Tec', 'Dec', 'Cmp'], "standard": ['Pos', 'Tck', 'Ant']},

    # 🏃 FULLBACKS / WINGBACKS
    "🏃 FB: No-Nonsense Full Back (Defend)": {"pos_key": ["D (RL)", "D (L)", "D (R)"], "core": ['Tck', 'Mar', 'Pos', 'Str', 'Cnt'], "important": ['Acc', 'Pac', 'Ant', 'Bra'], "standard": ['Sta', 'Wor', 'Hea', 'Jum']},
    "🏃 FB: Full Back (Defend)": {"pos_key": ["D (RL)", "D (L)", "D (R)"], "core": ['Acc', 'Pac', 'Tck', 'Pos', 'Sta'], "important": ['Mar', 'Wor', 'Dec'], "standard": ['Cro', 'Str']},
    "🏃 WB: Wing Back (Support)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro'], "important": ['Dri', 'OtB', 'Dec'], "standard": ['Pas', 'Tec', 'Tck']},
    "🏃 WB: Wing Back (Attack)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Tec', 'Wor', 'Dec'], "standard": ['Pas', 'Cmp']},
    "🏃 WB: Complete Wing Back (Support)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro', 'Dri'], "important": ['Tec', 'OtB', 'Pas', 'Dec', 'Fir'], "standard": ['Cmp', 'Ant', 'Agi', 'Bal']},
    "🏃 WB: Complete Wing Back (Attack)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Sta', 'Cro', 'Dri', 'OtB'], "important": ['Wor', 'Tec', 'Pas', 'Dec', 'Fir', 'Cmp'], "standard": ['Ant', 'Agi', 'Bal']},
    "🏃 IWB: Inverted Wing Back (Support)": {"pos_key": ["D (RL)", "WB"], "core": ['Acc', 'Pac', 'Pas', 'Dec', 'Pos'], "important": ['Fir', 'Cmp', 'Tck'], "standard": ['Vis', 'Sta']},

    # 🧱 DEFENSIVE MIDFIELDERS
    "🧱 DM: Anchor": {"pos_key": ["DM"], "core": ['Pos', 'Ant', 'Tck', 'Str', 'Cnt'], "important": ['Acc', 'Pac', 'Dec'], "standard": ['Pas', 'Sta']},
    "🧱 DM: Defensive Midfielder (Support)": {"pos_key": ["DM"], "core": ['Pos', 'Pas', 'Dec', 'Ant'], "important": ['Acc', 'Pac', 'Tck', 'Cmp'], "standard": ['Sta', 'Str']},
    "🧱 DM: Segundo Volante (Attack)": {"pos_key": ["DM"], "core": ['Acc', 'Sta', 'OtB', 'Fin', 'Wor'], "important": ['Lon', 'Dec', 'Ant', 'Pac'], "standard": ['Pas', 'Tec']},
    "🧱 DM: Regista": {"pos_key": ["DM", "M (C)"], "core": ['Pas', 'Vis', 'Cmp', 'Dec'], "important": ['Fir', 'Acc', 'Ant'], "standard": ['Tec', 'Sta']},
    "🧱 DLP: Deep-Lying Playmaker (Defend)": {"pos_key": ["DM", "M (C)"], "core": ['Pas', 'Vis', 'Dec', 'Cmp', 'Pos'], "important": ['Fir', 'Tec', 'Ant', 'Tea', 'Acc'], "standard": ['Pac', 'Sta', 'Tck', 'Cnt']},
    "🧱 DLP: Deep-Lying Playmaker (Support)": {"pos_key": ["DM", "M (C)"], "core": ['Pas', 'Vis', 'Dec', 'Fir', 'Cmp'], "important": ['Tec', 'Ant', 'Tea', 'Acc'], "standard": ['Pac', 'Sta', 'Pos', 'OtB']},

    # ⚙ CENTRAL MIDFIELDERS
    "⚙ CM: Central Midfielder (Defend)": {"pos_key": ["M (C)"], "core": ['Pos', 'Tck', 'Dec', 'Tea', 'Sta', 'Acc'], "important": ['Pac', 'Ant', 'Wor', 'Pas', 'Cnt'], "standard": ['Str', 'Cmp', 'Mar']},
    "⚙ CM: Central Midfielder (Support)": {"pos_key": ["M (C)"], "core": ['Pas', 'Dec', 'Tea', 'Sta', 'Acc'], "important": ['Vis', 'Fir', 'Wor', 'Ant', 'Pac'], "standard": ['OtB', 'Cmp', 'Tck', 'Tec']},
    "⚙ CM: Central Midfielder (Attack)": {"pos_key": ["M (C)"], "core": ['Acc', 'OtB', 'Sta', 'Pas', 'Dec', 'Cmp'], "important": ['Pac', 'Tec', 'Fir', 'Ant'], "standard": ['Fin', 'Lon', 'Dri', 'Vis']},
    "⚙ CM: Box to Box": {"pos_key": ["M (C)", "DM"], "core": ['Sta', 'Wor', 'Acc', 'Pac', 'Tea', 'OtB'], "important": ['Pas', 'Tck', 'Dec', 'Ant', 'Str'], "standard": ['Fin', 'Lon', 'Cmp', 'Fir']},
    "⚙ CM: Ball Winning Midfielder": {"pos_key": ["M (C)", "DM"], "core": ['Tck', 'Agg', 'Wor', 'Acc', 'Sta'], "important": ['Ant', 'Str', 'Pos'], "standard": ['Pas', 'Dec']},
    "⚙ CM: Mezzala (Attack)": {"pos_key": ["M (C)"], "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'], "important": ['Pas', 'Vis', 'Dec', 'Pac'], "standard": ['Fin', 'Lon', 'Fir']},
    "⚙ CAR: Carrilero (Support)": {"pos_key": ["M (C)"], "core": ['Sta', 'Wor', 'Tea', 'Pos', 'Acc', 'Pas'], "important": ['Pac', 'Dec', 'Ant', 'Tck'], "standard": ['Fir', 'Tec', 'Cnt', 'Mar']},
    "⚙ RP: Roaming Playmaker (Support)": {"pos_key": ["DM", "M (C)"], "core": ['Acc', 'Sta', 'Wor', 'Pas', 'Vis', 'Dec', 'Dri'], "important": ['Fir', 'Tec', 'Cmp', 'Ant', 'Pac'], "standard": ['OtB', 'Bal', 'Agi', 'Tea']},

    # 🪽 WIDE ROLES / WINGERS
    "🪽 WING: Winger (Attack)": {"pos_key": ["AM (RL)", "M (RL)"], "core": ['Acc', 'Pac', 'Dri', 'Cro', 'OtB'], "important": ['Tec', 'Dec'], "standard": ['Fin', 'Fir']},
    "🪽 WING: Inside Forward (Attack)": {"pos_key": ["AM (RL)"], "core": ['Acc', 'Pac', 'Fin', 'OtB', 'Dri'], "important": ['Cmp', 'Ant'], "standard": ['Tec', 'Fir']},
    "🪽 WING: Inverted Winger (Attack)": {"pos_key": ["AM (RL)", "M (RL)"], "core": ['Acc', 'Pac', 'Dri', 'Tec', 'OtB'], "important": ['Pas', 'Dec'], "standard": ['Fin', 'Lon']},
    "🪽 WING: Raumdeuter": {"pos_key": ["AM (RL)"], "core": ['Acc', 'OtB', 'Ant', 'Fin'], "important": ['Pac', 'Cmp'], "standard": ['Fir']},
    "🪽 WM: Wide Midfielder (Defend)": {"pos_key": ["M (RL)"], "core": ['Sta', 'Wor', 'Tea', 'Pos', 'Acc'], "important": ['Pac', 'Tck', 'Ant', 'Dec'], "standard": ['Cro', 'Pas', 'Dri', 'Mar']},
    "🪽 WM: Wide Midfielder (Support)": {"pos_key": ["M (RL)"], "core": ['Acc', 'Pac', 'Sta', 'Wor', 'Cro', 'Tea'], "important": ['Dri', 'Pas', 'OtB', 'Dec'], "standard": ['Tec', 'Ant', 'Fir']},
    "🪽 WM: Wide Midfielder (Attack)": {"pos_key": ["M (RL)"], "core": ['Acc', 'Pac', 'Dri', 'Cro', 'OtB'], "important": ['Sta', 'Wor', 'Tec', 'Fir', 'Dec'], "standard": ['Fin', 'Pas', 'Ant']},
    "🪽 DW: Defensive Winger (Support)": {"pos_key": ["M (RL)", "AM (RL)"], "core": ['Sta', 'Wor', 'Tea', 'Pos', 'Acc'], "important": ['Pac', 'Tck', 'Ant', 'Cro', 'Dec'], "standard": ['Dri', 'Pas', 'Mar', 'OtB']},
    "🪽 WTF: Wide Target Forward (Su/At)": {"pos_key": ["AM (RL)", "M (RL)"], "core": ['Str', 'Jum', 'Hea', 'Bra', 'Bal'], "important": ['Fir', 'OtB', 'Acc', 'Pac', 'Tea'], "standard": ['Fin', 'Pas', 'Cmp', 'Cro']},

    # 🎯 AMC ROLES
    "🎯 AMC: Shadow Striker": {"pos_key": ["AM (C)"], "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Pac', 'Dec', 'Fir'], "standard": ['Dri', 'Lon']},
    "🎯 AMC: Advanced Playmaker (Attack)": {"pos_key": ["AM (C)", "M (C)"], "core": ['Pas', 'Vis', 'Tec', 'Dec', 'Cmp'], "important": ['Acc', 'OtB'], "standard": ['Dri', 'Lon']},
    "🎯 AM: Attacking Midfielder (Support)": {"pos_key": ["AM (C)"], "core": ['Pas', 'Fir', 'Tec', 'Dec', 'Cmp', 'Acc'], "important": ['Vis', 'OtB', 'Ant', 'Pac'], "standard": ['Dri', 'Sta', 'Wor', 'Lon']},
    "🎯 AM: Attacking Midfielder (Attack)": {"pos_key": ["AM (C)"], "core": ['Acc', 'OtB', 'Fir', 'Tec', 'Cmp', 'Dec'], "important": ['Pac', 'Fin', 'Vis', 'Ant'], "standard": ['Dri', 'Long', 'Pas']},

    # ⚽ STRIKER ROLES
    "⚽ ST: Advanced Forward": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Fir', 'Dec'], "standard": ['Dri', 'Tec']},
    "⚽ ST: Pressing Forward (Defend)": {"pos_key": ["ST (C)"], "core": ['Wor', 'Sta', 'Acc', 'Tea', 'Agg'], "important": ['Pac', 'Ant', 'Str', 'OtB'], "standard": ['Fin', 'Fir', 'Dec']},
    "⚽ ST: Pressing Forward (Support)": {"pos_key": ["ST (C)"], "core": ['Wor', 'Sta', 'Acc', 'Tea', 'OtB'], "important": ['Pac', 'Fir', 'Str', 'Ant'], "standard": ['Pas', 'Fin', 'Dec']},
    "⚽ ST: Pressing Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'Wor', 'Sta', 'OtB', 'Fin'], "important": ['Ant', 'Str', 'Agg', 'Cmp'], "standard": ['Fir', 'Dec']},
    "⚽ ST: Complete Forward (Support)": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'Fin', 'Fir', 'Pas', 'Str', 'Cmp'], "important": ['Tec', 'Hea', 'OtB', 'Dec', 'Ant'], "standard": ['Dri', 'Jum', 'Tea', 'Sta']},
    "⚽ ST: Complete Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Acc', 'OtB', 'Fin', 'Cmp', 'Str', 'Pac'], "important": ['Fir', 'Tec', 'Hea', 'Ant'], "standard": ['Pas', 'Dri', 'Jum', 'Sta']},
    "⚽ ST: Target Forward (Support)": {"pos_key": ["ST (C)"], "core": ['Str', 'Jum', 'Hea', 'Fir', 'Bra'], "important": ['Tea', 'OtB', 'Cmp', 'Acc'], "standard": ['Pas', 'Fin', 'Ant', 'Bal']},
    "⚽ ST: Target Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Str', 'Jum', 'Hea', 'Fin', 'Bra'], "important": ['OtB', 'Cmp', 'Acc', 'Ant'], "standard": ['Fir', 'Pac', 'Bal']},
    "⚽ ST: Poacher": {"pos_key": ["ST (C)"], "core": ['Acc', 'OtB', 'Fin', 'Ant'], "important": ['Pac', 'Cmp'], "standard": ['Fir']},
    "⚽ ST: Deep-Lying Forward (Support)": {"pos_key": ["ST (C)"], "core": ['Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Acc'], "important": ['Vis', 'OtB', 'Tea', 'Pac'], "standard": ['Str', 'Fin', 'Ant', 'Dri']},
    "⚽ ST: Deep-Lying Forward (Attack)": {"pos_key": ["ST (C)"], "core": ['Acc', 'OtB', 'Fir', 'Cmp', 'Fin'], "important": ['Pac', 'Pas', 'Tec', 'Dec', 'Ant'], "standard": ['Str', 'Dri', 'Vis']},
    "⚽ ST: False Nine (Support)": {"pos_key": ["ST (C)"], "core": ['Fir', 'Pas', 'Tec', 'Vis', 'Cmp', 'Dec', 'Acc'], "important": ['OtB', 'Tea', 'Wor', 'Dri', 'Pac'], "standard": ['Lon', 'Fin', 'Ant']}
}

def calculate_role_score(row, role_name):
    cfg = ROLES.get(role_name)
    if not cfg: return 0
    player_pos = str(row['Position'])
    is_compatible = any(key in player_pos for key in cfg['pos_key'])
    pos_multiplier = 1.0 if is_compatible else 0.3
    
    s_core = sum(row[a] for a in cfg['core'] if a in row) * 5
    s_imp = sum(row[a] for a in cfg['important'] if a in row) * 3
    s_std = sum(row[a] for a in cfg['standard'] if a in row) * 2
    
    max_score = (len(cfg['core']) * 20 * 5) + (len(cfg['important']) * 20 * 3) + (len(cfg['standard']) * 20 * 2)
    base_norm = (s_core + s_imp + s_std) / max_score * 100
    
    dev_cons, dev_imp = row['Cons'] - 10, row['Imp M'] - 10
    hidden_pct = (dev_cons * 0.008) + (dev_imp * 0.005)
    hidden_pct = max(-0.10, min(0.10, hidden_pct))
    
    return round(base_norm * pos_multiplier * (1 + hidden_pct), 2)

# --- UI STREAMLIT ---
st.title("🏆 FM24 Ultimate Role Calculator")

if df_raw is not None:
    st.sidebar.header("Taktik & Filter")
    selected_role = st.sidebar.selectbox("Pilih Role", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal Ability (CA Filter)", 0, 200, 130)
    search_q = st.sidebar.text_input("Cari Nama Pemain")

    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    
    # Filter CA dan Urutkan
    res_sorted = df_calc[df_calc['CA'] >= min_ca].sort_values(by='Score', ascending=False).reset_index(drop=True)
    res_sorted['No'] = res_sorted.index + 1
    
    # Filter Pencarian Nama
    res_display = res_sorted.copy()
    if search_q:
        res_display = res_display[res_display['Name'].str.contains(search_q, case=False)]

    # --- TABEL UTAMA ---
    st.markdown("### 📋 Player List (Klik Baris untuk Detail)")
    display_cols = ['No', 'Name', 'Position', 'Score', 'CA', 'PA', 'Cons', 'Imp M']
    
    event = st.dataframe(
        res_display[display_cols],
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single_row"
    )

    # --- DETAIL ANALISIS PEMAIN (SAAT DIKLIK) ---
    selected_rows = event.get("selection", {}).get("rows", [])
    if selected_rows:
        idx = selected_rows[0]
        p = res_display.iloc[idx]
        
        st.divider()
        st.header(f"🔍 Detail Analysis: {p['Name']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Role Score", f"{p['Score']}%")
        m2.metric("Current Ability (CA)", p['CA'])
        m3.metric("Potential Ability (PA)", p['PA'])
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader("⭐ Top 5 Best Roles")
            all_scores = []
            for r_name in ROLES.keys():
                all_scores.append({"Role": r_name, "Score": calculate_role_score(p, r_name)})
            
            df_best = pd.DataFrame(all_scores).sort_values(by="Score", ascending=False).head(5)
            st.table(df_best)

        with col_right:
            st.subheader("🕵️ Hidden Attributes")
            hidden_list = {
                "Consistency": p.get('Cons', 'N/A'),
                "Important Matches": p.get('Imp M', 'N/A'),
                "Ambition": p.get('Amb', 'N/A'),
                "Professionalism": p.get('Prof', 'N/A'),
                "Injury Proneness": p.get('Inj Pr', 'N/A'),
                "Adaptability": p.get('Ada', 'N/A')
            }
            
            h_col1, h_col2 = st.columns(2)
            for i, (label, val) in enumerate(hidden_list.items()):
                if i % 2 == 0:
                    h_col1.write(f"**{label}:** {val}")
                else:
                    h_col2.write(f"**{label}:** {val}")
            
            st.write("")
            st.subheader("🏃 Key Attributes")
            st.write(f"**Acc:** {p.get('Acc', '-')} | **Pac:** {p.get('Pac', '-')} | **Sta:** {p.get('Sta', '-')} | **Dec:** {p.get('Dec', '-')} | **Ant:** {p.get('Ant', '-')}")

    elif not res_display.empty:
        st.divider()
        c1, c2, c3 = st.columns(3)
        # Menampilkan Top 3 asli berdasarkan CA filter
        top3 = res_sorted.head(3)
        c1.metric("🥇 Rank 1", top3.iloc[0]['Name'], f"{top3.iloc[0]['Score']}%")
        if len(top3) > 1: c2.metric("🥈 Rank 2", top3.iloc[1]['Name'], f"{top3.iloc[1]['Score']}%")
        if len(top3) > 2: c3.metric("🥉 Rank 3", top3.iloc[2]['Name'], f"{top3.iloc[2]['Score']}%")

else:
    st.error("File 'db.xlsx' tidak ditemukan di GitHub!")
