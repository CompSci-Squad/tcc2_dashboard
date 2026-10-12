"""Constantes do projeto: caminhos, parâmetros do pipeline, paleta e recessões."""

from __future__ import annotations

from pathlib import Path

DATA_DIR = Path(__file__).parent / "dados"
FIG_DIR = DATA_DIR / "figuras"
ASSETS_DIR = Path(__file__).parent / "assets"

# Parâmetros fixados no notebook (Santos et al., 2021 aplicado ao FRED-MD)
K = 19
KMEANS_SEED = 42
KMEANS_N_INIT = 20
HAC_MAXLAGS = 4
BLOCK_SIZE = 12
ALPHA = 0.05
R2_FORTE = 0.4
LIMIAR_CORR_PADRAO = 0.5

REG_VARS_PRINCIPAL = ["INDPRO", "CPIAUCSL", "FEDFUNDS", "T10YFFM", "S&P 500", "TWEXAFEGSMTHx"]
REG_VARS_ROBUSTEZ = REG_VARS_PRINCIPAL[:5]
CLUSTERS_ACHADO = [3, 4, 14, 18]

CLASSIFICACAO_ROTULO = {
    "mesma_familia": "Sanidade: mesma família",
    "mesma_familia_construcao": "Sanidade: construção",
    "familia_diferente": "Achado genuíno",
    "sem_classificacao": "Fraco (R² ≤ 0,4)",
}
CLASSIFICACAO_COR = {
    "Sanidade: mesma família": "#64748B",
    "Sanidade: construção": "#A8B3C4",
    "Achado genuíno": "#E11D48",
    "Fraco (R² ≤ 0,4)": "#C7D2FE",
}

# tab20, igual às figuras do notebook (cor do cluster = cid % 20)
TAB20 = [
    "#1f77b4",
    "#aec7e8",
    "#ff7f0e",
    "#ffbb78",
    "#2ca02c",
    "#98df8a",
    "#d62728",
    "#ff9896",
    "#9467bd",
    "#c5b0d5",
    "#8c564b",
    "#c49c94",
    "#e377c2",
    "#f7b6d2",
    "#7f7f7f",
    "#c7c7c7",
    "#bcbd22",
    "#dbdb8d",
    "#17becf",
    "#9edae5",
]

# Recessões NBER (pico → vale) dentro da janela 1965-2026
RECESSOES_NBER = [
    ("1969-12-01", "1970-11-30"),
    ("1973-11-01", "1975-03-31"),
    ("1980-01-01", "1980-07-31"),
    ("1981-07-01", "1982-11-30"),
    ("1990-07-01", "1991-03-31"),
    ("2001-03-01", "2001-11-30"),
    ("2007-12-01", "2009-06-30"),
    ("2020-02-01", "2020-04-30"),
]

TCODE_ROTULO = {
    1: "nível (sem transformação)",
    2: "Δxₜ",
    3: "Δ²xₜ",
    4: "log(xₜ)",
    5: "Δlog(xₜ)",
    6: "Δ²log(xₜ)",
    7: "Δ(xₜ/xₜ₋₁ − 1)",
}


def cor_cluster(cid: int) -> str:
    return TAB20[int(cid) % 20]
