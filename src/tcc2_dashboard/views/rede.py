"""Página 4 — rede de correlação entre séries com limiar ajustável."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import analysis, charts, data, ui
from tcc2_dashboard.config import LIMIAR_CORR_PADRAO, K

LAYOUTS = ["Circular (por cluster)", "Agrupado por cluster", "Força (spring)"]


@st.cache_data(show_spinner=False)
def _posicoes(layout: str, limiar: float):
    corr = data.correlacao_series()
    arestas = analysis.arestas_correlacao(corr, limiar)
    return analysis.posicoes_rede(list(corr.columns), data.cluster_de(), arestas, layout)


def render() -> None:
    ui.cabecalho(
        "Rede de correlação",
        "Nó = série (cor = cluster). Aresta = |r de Pearson| acima do limiar. "
        "Mostra co-movimento contemporâneo, não causalidade.",
    )
    corr = data.correlacao_series()
    cl_de = data.cluster_de()
    nomes = data.rotulo_curto()

    with st.sidebar:
        st.header("Rede")
        limiar = st.slider("Limiar |r|", 0.30, 0.95, LIMIAR_CORR_PADRAO, 0.01)
        pos_on = st.checkbox("Arestas positivas", True)
        neg_on = st.checkbox("Arestas negativas", True)
        layout = st.radio("Layout", LAYOUTS)
        destacar = st.multiselect(
            "Destacar clusters", list(range(K)), format_func=data.nome_cluster
        )
        rotular = st.toggle("Rótulos nos nós", value=False)

    arestas = analysis.arestas_correlacao(corr, limiar)
    if destacar:
        so = arestas["a"].map(cl_de).isin(destacar) | arestas["b"].map(cl_de).isin(destacar)
        arestas = arestas[so]
    pos = _posicoes(layout, limiar)

    r = analysis.resumo_rede(arestas, cl_de, corr.shape[0])
    c = st.columns(5)
    c[0].metric("Arestas", f"{r['n_arestas']:,}".replace(",", "."))
    c[1].metric("% positivas", f"{r['pct_positivas']:.0f} %")
    c[2].metric("% dentro do cluster", f"{r['pct_dentro']:.0f} %")
    c[3].metric("Densidade dentro", f"{r['densidade_dentro']:.2f}")
    c[4].metric("Densidade entre", f"{r['densidade_entre']:.3f}")

    if arestas.empty:
        st.warning("Nenhuma aresta acima do limiar com os filtros atuais.")
    ui.plot(
        charts.rede(pos, arestas, cl_de, nomes, pos_on, neg_on, destacar, rotular),
        width="stretch",
    )
    st.caption(
        f"{r['isolados']} séries sem nenhuma aresta. Se a densidade dentro dos clusters for muito maior "
        "que entre eles, o K-Means está capturando a estrutura de correlação. "
        "Limiar de referência do roteiro: 0,5."
    )

    st.divider()
    st.subheader("Séries mais conectadas")
    grau = (
        arestas.melt(value_vars=["a", "b"])["value"]
        .value_counts()
        .rename_axis("serie")
        .reset_index(name="grau")
    )
    grau["cluster"] = grau["serie"].map(cl_de)
    st.dataframe(grau.head(15), hide_index=True, width="stretch")
    ui.csv_download(arestas, "arestas_rede.csv", "Baixar arestas", key="dl_rede")
