import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="FM24 Role Calculator", layout="wide")

st.title("⚽ Football Manager 2024 Player Role Calculator")
st.markdown("Gunakan kalkulator ini untuk menemukan pemain terbaik berdasarkan atribut dan koefisien role.")

# 1. Definisi Bobot Role
ROLES = {
    "Mezzala (Attack)": {
        "core": ['Pas', 'Dri', 'Tec', 'Dec', 'OtB'],
        "important": ['Fir', 'Lon', 'Vis', 'Acc', 'Agi', 'Bal', 'Cons'],
        "standard": ['Ant', 'Cmp', 'Fla', 'Wor', 'Sta', 'Fin', 'Imp M']
    },
    "Inverted Winger (Support)": {
        "core": ['Acc', 'Pac', 'Dri', 'Tec', 'Pas'],
        "important": ['Fir', 'Vis', 'Dec', 'OtB', 'Agi', 'Fla'],
        "standard": ['Cmp', 'Wor', 'Sta', 'Ant', 'Cons']
    }
}

# 2. Fungsi Kalkulasi
def calculate_score(df, role_name):
    weights = ROLES[role_name]
    core_w, imp_w, std_w = 1.0, 0.7, 0.4
    
    score_col = f"{role_name} Score"
    df[score_col] = 0.0
    total_w = 0.0
    
    for attr in weights['core']:
        df[score_col] += df[attr] * core_w
        total_w += core_w
    for attr in weights['important']:
        df[score_col] += df[attr] * imp_w
        total_w += imp_w
    for attr in weights['standard']:
        df[score_col] += df[attr] * std_w
        total_w += std_w
        
    # Normalisasi ke 100
    df[score_col] = (df[score_col] / (total_w * 20)) * 100
    return df[score_col].round(2)

# 3. Sidebar untuk Upload & Filter
st.sidebar.header("Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Database Excel/CSV Anda", type=['csv', 'xlsx'])

if uploaded_file:
    # Membaca data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    selected_role = st.sidebar.selectbox("Pilih Role Pemain", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal CA", 0, 200, 100)
    
    # Proses Kalkulasi
    df['Calculated_Score'] = calculate_score(df, selected_role)
    
    # Filter & Sort
    filtered_df = df[df['CA'] >= min_ca].sort_values(by='Calculated_Score', ascending=False)
    
    # Tampilan Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemain", len(df))
    col2.metric("Role Terpilih", selected_role)
    col3.metric("Skor Tertinggi", f"{filtered_df.iloc[0]['Calculated_Score']}%")
    
    st.subheader(f"Top Players for: {selected_role}")
    display_cols = ['Name', 'Position', 'Calculated_Score', 'CA', 'PA', 'Cons', 'Imp M']
    st.dataframe(filtered_df[display_cols], use_container_width=True)

else:
    st.info("Silakan upload file database Excel Anda di sidebar untuk memulai.")