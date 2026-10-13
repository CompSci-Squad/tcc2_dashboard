"""Página 8 — metodologia, limitações conhecidas, figuras do artigo e downloads."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import data, ui
from tcc2_dashboard.config import DATA_DIR, FIG_DIR, TCODE_ROTULO

ETAPAS = [
    (
        "1 · Preparação",
        "Transformação por tcode (McCracken & Ng, 2016) para estacionariedade e "
        "imputação EM-PCA dos buracos internos.",
    ),
    (
        "2 · Padronização",
        "Cada série com média 0 e desvio-padrão 1. Entram 118 séries × 735 meses; "
        "as 6 variáveis de referência ficam fora do agrupamento.",
    ),
    ("3 · Fatorabilidade", "Teste de esfericidade de Bartlett e KMO sobre a matriz de correlação."),
    (
        "4 · Agrupamento",
        "PCA define k = 19 (critério de 70 % de variância); K-Means (k-means++, "
        "n_init = 20, seed 42) sobre as séries.",
    ),
    (
        "5 · Regressão",
        "Centroide de cada cluster ~ INDPRO, CPIAUCSL, FEDFUNDS, T10YFFM, S&P 500 e "
        "câmbio (TWEXAFEGSMTHx); DW e Breusch-Godfrey; erro-padrão HAC (Newey-West, 4 lags).",
    ),
    (
        "6 · Rotulagem",
        "Variável dominante por cluster, classificação “mesma família” × "
        "“família diferente”; validada pelo orientador em 31/07.",
    ),
]

FIGURAS = {
    "centroides_por_cluster.png": "Centroides por cluster",
    "centroides_clusters_fortes.png": "Centroides dos clusters fortes",
    "clusters_pca_scatter.png": "Dispersão PCA",
    "rede_clusters.png": "Rede de correlação",
    "dendrograma_ward.png": "Dendrograma Ward",
    "coeficientes_heatmap.png": "Heatmap de coeficientes",
    "r2_por_cluster.png": "R² por cluster",
    "durbin_watson_por_cluster.png": "Durbin-Watson por cluster",
    "scree_plot.png": "Scree plot",
    "correlation_heatmap.png": "Heatmap de correlação",
    "cluster_sizes.png": "Tamanho dos clusters",
}


def render() -> None:
    ui.cabecalho(
        "Metodologia e limitações",
        "O método passo a passo e o que ainda precisa ser resolvido, com transparência.",
        kicker="Detalhes técnicos",
    )

    st.subheader("Pipeline")
    for titulo, texto in ETAPAS:
        st.markdown(f"**{titulo}** — {texto}")

    st.divider()
    st.subheader("Limitações conhecidas (reportar na banca)")
    st.warning(
        "**Imputação EM-PCA**: o critério de convergência tem um bug conhecido — `prev_norm` começa "
        "em infinito e a checagem dispara na 1ª iteração, então o EM roda uma única passada. A "
        "versão corrigida não convergiu de forma estável e mudou a composição dos clusters "
        "(ARI = 0,586 contra a versão atual), inclusive dois dos achados já validados. Mantivemos o "
        "comportamento original por consistência e documentamos a pendência.",
        icon=":material/warning:",
    )
    st.info(
        "**Autocorrelação**: Breusch-Godfrey rejeita H₀ em todos os 19 clusters; por isso o modelo "
        "usa erro-padrão HAC. 9 de 114 pares (cluster, variável) mudaram de significância em relação "
        "ao OLS clássico.",
        icon=":material/info:",
    )
    st.info(
        "**Estabilidade**: Jaccard médio no bootstrap em blocos fica entre ~0,40 e ~0,72 para os "
        "clusters de achado genuíno — estabilidade moderada, a ser descrita como tal.",
        icon=":material/info:",
    )
    st.info(
        "**Dashboard**: a regressão ao vivo usa as 5 variáveis de janela cheia; a série de câmbio "
        "não está nos dados exportados. O bootstrap ao vivo usa n_init reduzido.",
        icon=":material/info:",
    )

    st.divider()
    st.subheader("Códigos de transformação (tcode)")
    st.dataframe(
        [{"tcode": k, "transformação": v} for k, v in TCODE_ROTULO.items()],
        hide_index=True,
        width="stretch",
    )

    st.divider()
    st.subheader("Figuras do notebook")
    disponiveis = [f for f in FIGURAS if (FIG_DIR / f).exists()]
    escolha = st.selectbox("Figura", disponiveis, format_func=lambda f: FIGURAS[f])
    if escolha:
        st.image(str(FIG_DIR / escolha), width="stretch")

    st.divider()
    st.subheader("Downloads")
    tabelas = sorted(p for p in DATA_DIR.glob("*.csv") if p.name != "fred_md_raw.csv")
    cols = st.columns(3)
    for i, p in enumerate(tabelas):
        cols[i % 3].download_button(
            p.name,
            p.read_bytes(),
            file_name=p.name,
            mime="text/csv",
            key=f"dl_{p.name}",
            icon=":material/download:",
            width="stretch",
        )
    st.caption(f"Fonte dos dados: FRED-MD (2026-04). {len(data.series_meta())} séries agrupadas.")
