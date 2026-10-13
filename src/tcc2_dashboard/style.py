"""Identidade visual: tokens claro/escuro, CSS global e componentes HTML (cartões, anel, chips).

O tema ativo vem do próprio Streamlit (menu ⋮ → Settings → Theme, ou o tema do sistema).
`tema()` lê `st.context.theme.type`, e tanto o CSS quanto o template do Plotly se adaptam.
"""

from __future__ import annotations

import html as _html

import streamlit as st

LIGHT = {
    "bg": "#F6F7FB",
    "card": "#FFFFFF",
    "ink": "#0F172A",
    "muted": "#64748B",
    "line": "#E2E8F0",
    "primary": "#4F46E5",
    "primary_soft": "#EEF2FF",
    "primary_ink": "#3730A3",
    "accent": "#0EA5E9",
    "danger": "#E11D48",
    "ok": "#059669",
    "warn": "#D97706",
    "shadow": "rgba(15,23,42,.05)",
    "grid": "#EEF1F6",
    "hero_a": "#312E81",
    "hero_b": "#4F46E5",
    "hero_c": "#0EA5E9",
}
DARK = {
    "bg": "#0B1020",
    "card": "#141B2F",
    "ink": "#E8ECF8",
    "muted": "#94A3B8",
    "line": "#26304A",
    "primary": "#818CF8",
    "primary_soft": "#1E2547",
    "primary_ink": "#C7D2FE",
    "accent": "#38BDF8",
    "danger": "#FB7185",
    "ok": "#34D399",
    "warn": "#FBBF24",
    "shadow": "rgba(0,0,0,.35)",
    "grid": "#222B44",
    "hero_a": "#1E1B4B",
    "hero_b": "#4338CA",
    "hero_c": "#0369A1",
}


def tema() -> str:
    """'light' ou 'dark', conforme o tema ativo do Streamlit."""
    try:
        t = st.context.theme.type
    except Exception:
        return "light"
    return "dark" if t == "dark" else "light"


def tokens() -> dict[str, str]:
    return DARK if tema() == "dark" else LIGHT


def _css(t: dict[str, str]) -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {{
  --bg:{t["bg"]}; --card:{t["card"]}; --ink:{t["ink"]}; --muted:{t["muted"]}; --line:{t["line"]};
  --primary:{t["primary"]}; --primary-soft:{t["primary_soft"]}; --primary-ink:{t["primary_ink"]};
  --accent:{t["accent"]}; --danger:{t["danger"]}; --ok:{t["ok"]}; --warn:{t["warn"]};
  --shadow:{t["shadow"]};
}}
@property --n {{ syntax: '<integer>'; initial-value: 0; inherits: false; }}
@property --pct {{ syntax: '<number>'; initial-value: 0; inherits: false; }}

html, body, .stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp textarea, .stApp button,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, [data-testid="stMetric"] *, [data-baseweb] {{
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif; }}
[data-testid="stIconMaterial"], .material-symbols-rounded, span[class*="material"] {{
  font-family: 'Material Symbols Rounded' !important; }}

footer, [data-testid="stDecoration"], .stAppDeployButton {{ display: none; }}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 1240px; }}

h1, h2, h3, h4 {{ letter-spacing: -0.015em; }}
h3 {{ font-size: 1.15rem !important; font-weight: 650; margin-top: .4rem; }}
h4 {{ font-size: 1rem !important; font-weight: 650; }}
[data-testid="stCaptionContainer"] {{ color: var(--muted); }}
hr {{ border-color: var(--line); margin: 2rem 0 1.5rem; }}
code {{ background: var(--primary-soft); color: var(--primary-ink); border-radius: 6px;
  padding: .08rem .35rem; font-size: .85em; }}

/* ---------- animações ---------- */
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes grow {{ from {{ width: 0; }} }}
@keyframes count {{ from {{ --n: 0; }} }}
@keyframes ringfill {{ from {{ --pct: 0; }} }}
.rise {{ animation: rise .6s cubic-bezier(.2,.7,.2,1) both; }}
.d1 {{ animation-delay: .08s; }} .d2 {{ animation-delay: .16s; }} .d3 {{ animation-delay: .24s; }}
.d4 {{ animation-delay: .32s; }} .d5 {{ animation-delay: .40s; }} .d6 {{ animation-delay: .48s; }}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation: none !important; transition: none !important; }} }}

/* ---------- hero ---------- */
.hero {{ position: relative; padding: 2rem 2.2rem 1.8rem; border-radius: 22px; margin-bottom: 1.4rem; color: #fff;
  background: linear-gradient(125deg, {t["hero_a"]} 0%, {t["hero_b"]} 50%, {t["hero_c"]} 125%);
  box-shadow: 0 18px 40px -18px rgba(79,70,229,.6); overflow: hidden; animation: rise .6s both; }}
.hero::before {{ content: ""; position: absolute; inset: 0; opacity: .5; pointer-events: none;
  background: radial-gradient(circle at 85% 15%, rgba(255,255,255,.28), transparent 38%),
              radial-gradient(circle at 5% 110%, rgba(255,255,255,.14), transparent 40%); }}
.hero .kicker {{ font-size: .72rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; opacity: .8; }}
.hero h1 {{ color: #fff !important; font-size: 2.3rem; font-weight: 800; margin: .3rem 0 .5rem; padding: 0; line-height: 1.15; }}
.hero p {{ margin: 0; font-size: 1.05rem; opacity: .93; max-width: 60ch; color: #fff !important; }}
.hero-stats {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 1rem; margin-top: 1.6rem; }}
.hero-stat {{ background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.25); border-radius: 16px;
  padding: .9rem 1.1rem; backdrop-filter: blur(6px); }}
.hero-stat .num {{ font-size: 2.7rem; font-weight: 800; line-height: 1; letter-spacing: -0.03em;
  animation: count 1.6s cubic-bezier(.2,.7,.2,1) both; counter-reset: n var(--n); }}
.hero-stat .num::before {{ content: counter(n); }}
.hero-stat .num small {{ font-size: 1rem; font-weight: 600; opacity: .85; margin-left: .25rem; }}
.hero-stat .lab {{ font-size: .85rem; opacity: .88; margin-top: .35rem; }}
.chips {{ margin-top: 1rem; display: flex; gap: .5rem; flex-wrap: wrap; }}
.chip {{ background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28); color: #fff;
  padding: .22rem .65rem; border-radius: 999px; font-size: .76rem; font-weight: 600; }}

.pagehead {{ margin-bottom: 1.3rem; padding-bottom: 1rem; border-bottom: 1px solid var(--line); animation: rise .5s both; }}
.pagehead .kicker {{ font-size: .7rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--primary); }}
.pagehead h1 {{ font-size: 1.9rem; font-weight: 800; margin: .1rem 0 .3rem; padding: 0; }}
.pagehead p {{ margin: 0; color: var(--muted); font-size: 1rem; max-width: 80ch; }}

/* ---------- cartões ---------- */
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 1.2rem 1.35rem;
  box-shadow: 0 1px 2px var(--shadow); transition: transform .25s, box-shadow .25s, border-color .25s; animation: rise .6s both; }}
.card:hover {{ transform: translateY(-3px); box-shadow: 0 14px 30px -14px var(--shadow); border-color: var(--primary); }}
.card h3, .card h4 {{ margin: 0 0 .35rem; }}
.card p {{ margin: .25rem 0; color: var(--muted); }}
.kicker-s {{ font-size: .68rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }}

.cards-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 1.1rem; }}
.cards-3 {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 1.1rem; }}
.cards-4 {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1rem; }}
@media (max-width: 900px) {{ .cards-2, .cards-3, .cards-4, .hero-stats {{ grid-template-columns: 1fr; }} }}

.achado {{ position: relative; overflow: hidden; display: flex; flex-direction: column; gap: .7rem; }}
.achado::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px;
  background: linear-gradient(180deg, var(--primary), var(--accent)); }}
.achado .top {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }}
.badge {{ display: inline-block; font-size: .7rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  background: var(--primary-soft); color: var(--primary-ink); padding: .2rem .55rem; border-radius: 999px; }}
.achado h3 {{ font-size: 1.25rem !important; margin: .45rem 0 .1rem; }}
.achado .leitura {{ font-size: 1.02rem; color: var(--ink); line-height: 1.5; margin: .2rem 0; }}
.achado .meta {{ display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }}
.achado .meta div {{ background: var(--primary-soft); border-radius: 12px; padding: .55rem .75rem; }}
.achado .meta b {{ display: block; font-size: .95rem; color: var(--ink); }}
.achado .meta span {{ font-size: .7rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}

.ring {{ --pct: 0; flex: none; width: 92px; height: 92px; border-radius: 50%;
  background: conic-gradient(var(--primary) calc(var(--pct) * 1%), var(--line) 0);
  display: grid; place-items: center; animation: ringfill 1.4s cubic-bezier(.2,.7,.2,1) both; position: relative; }}
.ring::before {{ content: ""; position: absolute; inset: 9px; border-radius: 50%; background: var(--card); }}
.ring > div {{ position: relative; text-align: center; line-height: 1.1; }}
.ring b {{ font-size: 1.25rem; font-weight: 800; color: var(--ink); }}
.ring small {{ display: block; font-size: .6rem; color: var(--muted); font-weight: 600; }}

.pill {{ display: inline-flex; align-items: center; gap: .3rem; font-size: .74rem; font-weight: 650; padding: .2rem .6rem;
  border-radius: 999px; border: 1px solid var(--line); color: var(--muted); }}
.pill.ok {{ color: var(--ok); border-color: color-mix(in srgb, var(--ok) 40%, transparent); background: color-mix(in srgb, var(--ok) 10%, transparent); }}
.pill.warn {{ color: var(--warn); border-color: color-mix(in srgb, var(--warn) 40%, transparent); background: color-mix(in srgb, var(--warn) 10%, transparent); }}
.pill.low {{ color: var(--danger); border-color: color-mix(in srgb, var(--danger) 40%, transparent); background: color-mix(in srgb, var(--danger) 10%, transparent); }}

.serie-chip {{ display: inline-block; margin: 0 .3rem .3rem 0; padding: .18rem .55rem; border-radius: 8px; font-size: .78rem;
  background: var(--primary-soft); color: var(--primary-ink); cursor: help; border: 1px solid transparent; transition: border-color .2s; }}
.serie-chip:hover {{ border-color: var(--primary); }}
.serie-chip b {{ font-weight: 700; }}

.step {{ display: flex; gap: 1rem; align-items: flex-start; }}
.step .n {{ flex: none; width: 2.4rem; height: 2.4rem; border-radius: 12px; display: grid; place-items: center; font-weight: 800;
  color: #fff; background: linear-gradient(135deg, var(--primary), var(--accent)); box-shadow: 0 8px 18px -8px var(--primary); }}
.step h4 {{ margin: .1rem 0 .15rem; }}
.step p {{ margin: 0; color: var(--muted); }}

.bar {{ height: 8px; border-radius: 999px; background: var(--line); overflow: hidden; }}
.bar > i {{ display: block; height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--primary), var(--accent));
  animation: grow 1.1s cubic-bezier(.2,.7,.2,1) both; }}

.callout {{ border-left: 4px solid var(--primary); background: var(--primary-soft); border-radius: 0 14px 14px 0;
  padding: .9rem 1.1rem; margin: .6rem 0 1rem; color: var(--ink); }}
.callout b {{ color: var(--primary-ink); }}

/* ---------- widgets ---------- */
[data-testid="stMetric"] {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem .8rem;
  box-shadow: 0 1px 2px var(--shadow); position: relative; }}
[data-testid="stMetric"]::before {{ content: ""; position: absolute; left: 0; top: 14px; bottom: 14px; width: 3px;
  border-radius: 0 3px 3px 0; background: linear-gradient(180deg, var(--primary), var(--accent)); }}
[data-testid="stMetricLabel"] p {{ font-size: .72rem !important; font-weight: 650; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }}
[data-testid="stMetricValue"] {{ font-size: 1.5rem !important; font-weight: 750; letter-spacing: -0.02em; line-height: 1.25; overflow-wrap: anywhere; }}
[data-testid="stMetricValue"] > div, [data-testid="stMetricLabel"] p {{ white-space: normal !important; overflow: visible !important; text-overflow: clip !important; }}

div[data-testid="stVerticalBlockBorderWrapper"] {{ background: var(--card); border-color: var(--line); border-radius: 16px; box-shadow: 0 1px 2px var(--shadow); }}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlockBorderWrapper"] {{ box-shadow: none; }}

.stTabs [data-baseweb="tab-list"] {{ gap: .25rem; border-bottom: 1px solid var(--line); }}
.stTabs [data-baseweb="tab"] {{ height: 2.6rem; padding: 0 1rem; border-radius: 10px 10px 0 0; font-weight: 600; color: var(--muted); }}
.stTabs [aria-selected="true"] {{ color: var(--primary); }}
.stTabs [data-baseweb="tab-highlight"] {{ background: var(--primary); height: 3px; border-radius: 3px 3px 0 0; }}

[data-testid="stSidebar"] {{ border-right: 1px solid var(--line); }}
[data-testid="stSidebarNavLink"] {{ border-radius: 10px; font-weight: 550; }}
[data-testid="stSidebarNavLink"][aria-current="page"] {{ background: var(--primary-soft); color: var(--primary); font-weight: 650; }}
[data-testid="stSidebar"] h2 {{ font-size: .72rem !important; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }}

.stButton > button, .stDownloadButton > button, [data-testid="stPageLink"] a {{ border-radius: 10px; font-weight: 600; }}
.stButton > button[kind="primary"] {{ background: linear-gradient(120deg, var(--primary), var(--accent)); color: #fff; border: 0;
  box-shadow: 0 6px 16px -8px var(--primary); }}
[data-baseweb="select"] > div, [data-baseweb="input"] > div {{ border-radius: 10px; }}
[data-testid="stAlert"] {{ border-radius: 12px; }}
[data-testid="stDataFrame"] {{ border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }}
[data-testid="stExpander"] {{ border: 1px solid var(--line); border-radius: 12px; background: var(--card); }}
[data-testid="stSegmentedControl"] button, [data-testid="stPills"] button {{ border-radius: 999px; }}
</style>
"""


def aplicar() -> None:
    st.markdown(_css(tokens()), unsafe_allow_html=True)


# ---------------------------------------------------------------- componentes HTML


def esc(s: object) -> str:
    return _html.escape(str(s), quote=True)


def html(s: str) -> None:
    """Renderiza HTML sem que o markdown trate linhas indentadas como bloco de código."""
    limpo = " ".join(linha.strip() for linha in s.strip().splitlines())
    st.markdown(limpo, unsafe_allow_html=True)


def chip_serie(codigo: str, descricao: str) -> str:
    return f'<span class="serie-chip" title="{esc(descricao)}"><b>{esc(codigo)}</b></span>'


def anel(pct: float, rotulo: str = "explicado") -> str:
    return (
        f'<div class="ring" style="--pct:{pct:.1f}"><div><b>{pct:.0f}%</b>'
        f"<small>{esc(rotulo)}</small></div></div>"
    )


def pill(texto: str, tipo: str = "") -> str:
    return f'<span class="pill {tipo}">{esc(texto)}</span>'
