"""Identidade visual: CSS global e tokens de cor (usados também pelo template do Plotly)."""

from __future__ import annotations

import streamlit as st

INK = "#0F172A"
MUTED = "#64748B"
LINE = "#E2E8F0"
BG = "#F6F7FB"
PRIMARY = "#4F46E5"
ACCENT = "#0EA5E9"
DANGER = "#E11D48"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp textarea, .stApp button,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, [data-testid="stMetric"] *, [data-baseweb] {{
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif; }}
/* não sobrescrever a fonte de ícones do Streamlit */
[data-testid="stIconMaterial"], .material-symbols-rounded, span[class*="material"] {{ font-family: 'Material Symbols Rounded' !important; }}
.stApp {{ background: {BG}; }}

/* esconde o cromo padrão do Streamlit */
#MainMenu, footer, [data-testid="stDecoration"] {{ display: none; }}
[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{ padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1280px; }}

/* tipografia */
h1, h2, h3, h4 {{ color: {INK}; letter-spacing: -0.015em; }}
h2, h3 {{ font-weight: 650; }}
h3 {{ font-size: 1.12rem !important; margin-top: .4rem; }}
h4 {{ font-size: 1rem !important; font-weight: 650; }}
[data-testid="stCaptionContainer"] {{ color: {MUTED}; }}
hr {{ border-color: {LINE}; margin: 2rem 0 1.5rem; }}
code {{ background: #EEF2FF; color: #3730A3; border-radius: 6px; padding: .08rem .35rem; font-size: .85em; }}

/* hero */
.hero {{ position: relative; padding: 1.6rem 1.8rem 1.5rem; border-radius: 18px; margin-bottom: 1.4rem;
  background: linear-gradient(120deg, #312E81 0%, {PRIMARY} 48%, {ACCENT} 120%); color: #fff;
  box-shadow: 0 10px 30px -12px rgba(79,70,229,.55); overflow: hidden; }}
.hero::after {{ content: ""; position: absolute; right: -60px; top: -80px; width: 280px; height: 280px;
  border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.22), transparent 65%); }}
.hero .kicker {{ font-size: .72rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; opacity: .8; }}
.hero h1 {{ color: #fff; font-size: 2.1rem; font-weight: 800; margin: .25rem 0 .35rem; padding: 0; }}
.hero p {{ margin: 0; font-size: 1rem; opacity: .92; max-width: 62ch; }}
.hero .chips {{ margin-top: 1rem; display: flex; gap: .5rem; flex-wrap: wrap; }}
.chip {{ background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28); color: #fff;
  padding: .22rem .65rem; border-radius: 999px; font-size: .76rem; font-weight: 600; backdrop-filter: blur(4px); }}

.pagehead {{ margin-bottom: 1.2rem; padding-bottom: .9rem; border-bottom: 1px solid {LINE}; }}
.pagehead .kicker {{ font-size: .7rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: {PRIMARY}; }}
.pagehead h1 {{ font-size: 1.85rem; font-weight: 800; margin: .1rem 0 .25rem; padding: 0; }}
.pagehead p {{ margin: 0; color: {MUTED}; font-size: .97rem; max-width: 80ch; }}

/* cartões: métricas e containers com borda */
[data-testid="stMetric"] {{ background: #fff; border: 1px solid {LINE}; border-radius: 14px; padding: .9rem 1rem .8rem;
  box-shadow: 0 1px 2px rgba(15,23,42,.04); position: relative; }}
[data-testid="stMetric"]::before {{ content: ""; position: absolute; left: 0; top: 14px; bottom: 14px; width: 3px;
  border-radius: 0 3px 3px 0; background: linear-gradient(180deg, {PRIMARY}, {ACCENT}); }}
[data-testid="stMetricLabel"] p {{ font-size: .72rem !important; font-weight: 650; letter-spacing: .06em;
  text-transform: uppercase; color: {MUTED}; }}
[data-testid="stMetricValue"] {{ font-size: 1.7rem; font-weight: 750; color: {INK}; letter-spacing: -0.02em; }}
[data-testid="stMetricDelta"] {{ font-size: .75rem; }}
[data-testid="stMetricValue"] > div, [data-testid="stMetricLabel"] p {{ white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }}
[data-testid="stMetricValue"] {{ font-size: 1.5rem !important; overflow-wrap: anywhere; line-height: 1.25; }}

div[data-testid="stVerticalBlockBorderWrapper"] {{ background: #fff; border-color: {LINE}; box-shadow: 0 1px 2px rgba(15,23,42,.04); }}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {{ box-shadow: none; }}

/* abas */
.stTabs [data-baseweb="tab-list"] {{ gap: .25rem; border-bottom: 1px solid {LINE}; }}
.stTabs [data-baseweb="tab"] {{ height: 2.6rem; padding: 0 1rem; border-radius: 10px 10px 0 0; font-weight: 600; color: {MUTED}; }}
.stTabs [aria-selected="true"] {{ color: {PRIMARY}; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {PRIMARY}; height: 3px; border-radius: 3px 3px 0 0; }}

/* sidebar */
[data-testid="stSidebar"] {{ background: #fff; border-right: 1px solid {LINE}; }}
[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {{ padding-top: 1.1rem; }}
[data-testid="stSidebarNavLink"] {{ border-radius: 10px; font-weight: 550; }}
[data-testid="stSidebarNavLink"][aria-current="page"] {{ background: #EEF2FF; color: {PRIMARY}; font-weight: 650; }}
[data-testid="stSidebarNavSeparator"] {{ color: {MUTED}; }}
[data-testid="stSidebar"] h2 {{ font-size: .72rem !important; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: {MUTED}; }}

/* botões e inputs */
.stButton > button, .stDownloadButton > button {{ border-radius: 10px; font-weight: 600; border: 1px solid {LINE}; }}
.stButton > button[kind="primary"] {{ background: linear-gradient(120deg, {PRIMARY}, #6366F1); border: 0; box-shadow: 0 6px 16px -8px rgba(79,70,229,.8); }}
[data-baseweb="select"] > div, [data-baseweb="input"] > div {{ border-radius: 10px; }}

/* avisos */
[data-testid="stAlert"] {{ border-radius: 12px; border: 1px solid {LINE}; }}

/* tabelas */
[data-testid="stDataFrame"] {{ border: 1px solid {LINE}; border-radius: 12px; overflow: hidden; }}

/* expanders */
[data-testid="stExpander"] {{ background: #fff; border: 1px solid {LINE}; border-radius: 12px; }}
</style>
"""


def aplicar() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
