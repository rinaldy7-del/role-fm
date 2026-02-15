Tentu, ini adalah pembaruan yang sangat penting untuk keperluan *scouting* yang lebih mendalam. Sekarang, ketika Anda mengeklik seorang pemain, sistem tidak hanya menampilkan role terbaiknya, tetapi juga membuka "kotak rahasia" pemain tersebut: **CA, PA, dan seluruh Hidden Attributes** yang ada di database Anda.

Berikut adalah kode **`app.py`** yang telah diperbarui:

```python
import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
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

# --- DATABASE SELURUH ROLE (LENGKAP) ---
# (Daftar ROLES tetap sama dengan versi sebelumnya untuk menghemat ruang, pastikan tetap ada di file Anda)
ROLES = {
    "⚽ ST: Advanced Forward": {"pos_key": ["ST (C)"], "core": ['Acc', 'Pac', 'OtB', 'Fin', 'Cmp', 'Ant'], "important": ['Fir', 'Dec'], "standard": ['Dri', 'Tec']},
    "⚙ CM: Mezzala (Attack)": {"pos_key": ["M (C)"], "core": ['Acc', 'OtB', 'Dri', 'Tec', 'Sta'], "important": ['Pas', 'Vis', 'Dec', 'Pac'], "standard": ['Fin', 'Lon', 'Fir']},
    # ... (Tambahkan semua role lain di sini)
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
    hidden_pct = max(-0.10, min(0.10, (dev_cons * 0.008) + (dev_imp * 0.005)))
    return round(base_norm * pos_multiplier * (1 + hidden_pct), 2)

# --- UI ---
st.title("🏆 FM24 Ultimate Role Calculator")

if df_raw is not None:
    st.sidebar.header("Taktik & Filter")
    selected_role = st.sidebar.selectbox("Pilih Role", list(ROLES.keys()))
    min_ca = st.sidebar.slider("Minimal Ability (CA Filter)", 0, 200, 130)
    search_q = st.sidebar.text_input("Cari Nama Pemain")

    # Kalkulasi Score
    df_calc = df_raw.copy()
    df_calc['Score'] = df_calc.apply(lambda r: calculate_role_score(r, selected_role), axis=1)
    
    res = df_calc[df_calc['CA'] >= min_ca].sort_values(by='Score', ascending=False)
    res = res.reset_index(drop=True)
    res['No'] = res.index + 1
    
    # Simpan hasil urutan asli untuk referensi Top 3
    full_res_for_no = res.copy()

    if search_q:
        res = res[res['Name'].str.contains(search_q, case=False)]

    # --- TABEL UTAMA ---
    st.markdown("### 📋 Player List (Klik Baris untuk Detail Hidden)")
    display_cols = ['No', 'Name', 'Position', 'Score', 'CA', 'PA', 'Cons', 'Imp M']
    
    event = st.dataframe(
        res[display_cols],
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single_row"
    )

    # --- DETAIL ANALISIS PEMAIN (SAAT DIKLIK) ---
    selected_rows = event.get("selection", {}).get("rows", [])
    if selected_rows:
        idx = selected_rows[0]
        p = res.iloc[idx]
        
        st.divider()
        st.header(f"🔍 Detail Analysis: {p['Name']}")
        
        # Row 1: Kemampuan Utama (CA/PA/Score)
        m1, m2, m3 = st.columns(3)
        m1.metric("Role Score", f"{p['Score']}%")
        m2.metric("Current Ability (CA)", p['CA'])
        m3.metric("Potential Ability (PA)", p['PA'])
        
        st.write("")
        
        # Row 2: Roles & Hidden Attributes
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
            # Daftar Hidden Attributes dari Excel Anda
            hidden_list = {
                "Consistency": p['Cons'],
                "Important Matches": p['Imp M'],
                "Ambition": p['Amb'],
                "Professionalism": p['Prof'],
                "Injury Proneness": p['Inj Pr'],
                "Adaptability": p['Ada']
            }
            
            # Tampilkan dalam bentuk kolom kecil yang rapi
            h_col1, h_col2 = st.columns(2)
            for i, (label, val) in enumerate(hidden_list.items()):
                if i % 2 == 0:
                    h_col1.write(f"**{label}:** {val}")
                else:
                    h_col2.write(f"**{label}:** {val}")
            
            st.write("")
            st.subheader("🏃 Key Physicals")
            st.write(f"**Acc:** {p['Acc']} | **Pac:** {p['Pac']} | **Sta:** {p['Sta']} | **Ant:** {p['Ant']}")

    elif not res.empty:
        # Jika tidak ada yang diklik, tampilkan Top 3 biasa
        st.divider()
        c1, c2, c3 = st.columns(3)
        top3 = full_res_for_no.head(3)
        c1.metric("🥇 Rank 1", top3.iloc[0]['Name'], f"{top3.iloc[0]['Score']}%")
        if len(top3) > 1: c2.metric("🥈 Rank 2", top3.iloc[1]['Name'], f"{top3.iloc[1]['Score']}%")
        if len(top3) > 2: c3.metric("🥉 Rank 3", top3.iloc[2]['Name'], f"{top3.iloc[2]['Score']}%")

else:
    st.error("Database 'database.xlsx' tidak ditemukan!")

```

### Apa yang Baru di Versi Ini?

1. **Metric Header:** Begitu pemain diklik, nilai **CA** dan **PA** langsung muncul besar di paling atas bagian detail.
2. **Seksi Hidden Attributes:** Saya menambahkan tabel khusus di sebelah kanan yang menampilkan:
* **Ambition** (Amb)
* **Professionalism** (Prof)
* **Injury Proneness** (Inj Pr)
* **Adaptability** (Ada)
* Serta **Consistency** dan **Important Matches** yang lebih mendetail.


3. **Key Physicals:** Menampilkan atribut fisik krusial (Kecepatan & Stamina) sebagai referensi cepat di bawah data hidden.
4. **Tetap Interaktif:** Jika Anda menutup pilihan atau mengeklik baris lain, datanya akan langsung berganti secara *real-time*.

Silakan update GitHub Anda. Sekarang Anda punya alat *scouting* lengkap yang bisa melihat sampai ke "jeroan" statistik pemain!
