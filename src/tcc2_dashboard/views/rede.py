"""Rede de semelhanças: quais séries estão fortemente ligadas entre si."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import analysis, catalogo, charts, data, ui
from tcc2_dashboard.config import LIMIAR_CORR_PADRAO, K

LAYOUTS = ["Circular (por cluster)", "Agrupado por cluster", "Força (spring)"]
NOMES_LAYOUT = {
    LAYOUTS[0]: "Em círculo, por família",
    LAYOUTS[1]: "Famílias em ilhas",
    LAYOUTS[2]: "Por atração (fios puxam)",
}


@st.cache_data(show_spinner=False)
def _posicoes(layout: str, limiar: float):
    corr = data.correlacao_series()
    arestas = analysis.arestas_correlacao(corr, limiar)
    return analysis.posicoes_rede(list(corr.columns), data.cluster_de(), arestas, layout)


def render() -> None:
    ui.cabecalho(
        "Rede de semelhanças",
        "Cada bolinha é uma série; cada fio liga duas séries que andam muito juntas. "
        "A cor da bolinha é a sua família.",
        kicker="Aprofunde",
    )
    corr = data.correlacao_series()
    cl_de = data.cluster_de()
    nomes = data.rotulo_curto()

    c1, c2, c3 = st.columns([3, 2, 2])
    limiar = c1.slider(
        "Quão parecidas devem ser para ganhar um fio?",
        0.30,
        0.95,
        LIMIAR_CORR_PADRAO,
        0.01,
        help="Quanto maior, menos fios. O valor de referência do estudo é 0,50.",
    )
    layout = c2.radio("Disposição", LAYOUTS, format_func=NOMES_LAYOUT.get)
    with c3:
        pos_on = st.checkbox("Fios de séries que andam juntas (verdes)", True)
        neg_on = st.checkbox("Fios de séries opostas (vermelhos)", True)
    destacar = st.multiselect("Destacar famílias", list(range(K)), format_func=data.nome_cluster)

    arestas = analysis.arestas_correlacao(corr, limiar)
    if destacar:
        so = arestas["a"].map(cl_de).isin(destacar) | arestas["b"].map(cl_de).isin(destacar)
        arestas = arestas[so]
    pos = _posicoes(layout, limiar)

    r = analysis.resumo_rede(arestas, cl_de, corr.shape[0])
    m = st.columns(4)
    m[0].metric("Fios", f"{r['n_arestas']:,}".replace(",", "."))
    m[1].metric("Entre séries da mesma família", f"{r['pct_dentro']:.0f}%")
    m[2].metric("Séries sem nenhum fio", r["isolados"])
    m[3].metric("Fios que são de séries que andam juntas", f"{r['pct_positivas']:.0f}%")

    if arestas.empty:
        st.warning("Nenhum fio com esse critério. Diminua o limiar.")
    ui.plot(
        charts.rede(pos, arestas, cl_de, nomes, pos_on, neg_on, destacar, False),
        key="rede",
    )
    st.caption(
        "Se a maioria dos fios liga séries da mesma família, o agrupamento está capturando "
        "estrutura real. Passe o mouse em uma bolinha para ver o que a série mede. Mostra "
        "semelhança, não causa e efeito."
    )

    st.markdown("#### Séries mais conectadas")
    grau = (
        arestas.melt(value_vars=["a", "b"])["value"]
        .value_counts()
        .rename_axis("Código")
        .reset_index(name="Ligações")
    )
    grau.insert(1, "O que mede", [catalogo.nome(s) for s in grau["Código"]])
    grau["Família"] = grau["Código"].map(cl_de)
    st.dataframe(grau.head(12), hide_index=True, width="stretch")
    ui.csv_download(arestas, "ligacoes.csv", "Baixar as ligações", key="dl_rede")
