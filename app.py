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
        "important": ['
