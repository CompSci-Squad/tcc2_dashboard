"""Página 2 — mapa PCA das séries (2D/3D), com destaque por cluster e busca."""

from __future__ import annotations

import numpy as np
import streamlit as st

from tcc2_dashboard import analysis, charts, data, ui
from tcc2_dashboard.config import K


@st.cache_data(show_spinner=False)
def _pca(n: int) -> analysis.PcaResultado:
    return analysis.pca_series(data.padronizado(), n)


@st.cache_data(show_spinner=False)
def _variancia() -> list[float]:
    return analysis.variancia_acumulada(data.padronizado()).tolist()


def render() -> None:
    ui.cabecalho(
        "Mapa das séries",
        "Projeção PCA das 118 séries (cada série é um ponto no espaço dos 735 meses).",
    )
    meta = data.series_meta()
    nomes = data.rotulo_curto()

    with st.sidebar:
        st.header("Mapa")
        dim = st.radio("Dimensões", ["2D", "3D"], horizontal=True)
        n_pc = 3 if dim == "3D" else st.slider("Componentes disponíveis", 2, 10, 4)
        pca = _pca(max(n_pc, 3) if dim == "3D" else n_pc)
        pcs = list(pca.coords.columns)
        if dim == "3D":
            eixos = pcs[:3]
        else:
            x = st.selectbox("Eixo X", pcs, index=0)
            y = st.selectbox("Eixo Y", pcs, index=1)
            eixos = [x, y]
        cor_por = st.radio(
            "Colorir por",
            ["cluster", "tcode", "corr_centroide"],
            format_func={
                "cluster": "Cluster K-Means",
                "tcode": "Transformação (tcode)",
                "corr_centroide": "Correlação com o centroide",
            }.get,
        )
        destacar = st.multiselect(
            "Destacar clusters",
            list(range(K)),
            format_func=data.nome_cluster,
            help="Os demais ficam esmaecidos.",
        )
        buscar = st.multiselect("Buscar séries", sorted(meta["serie"]))

    fig = charts.pca_dispersao(pca.coords, meta, eixos, cor_por, destacar, nomes, buscar)
    st.plotly_chart(fig, width="stretch")
    var = pca.variancia
    st.caption(
        "Variância explicada pelos eixos: "
        + " · ".join(f"{pc} {v:.1%}" for pc, v in zip(pcs, var, strict=True))
        + ". Dois pontos próximos se movem juntos no tempo."
    )

    st.divider()
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Critério dos 70 % de variância")
        cum = _variancia()
        st.plotly_chart(charts.scree(np.array(cum), K), width="stretch")
    with c2:
        st.subheader("Séries por transformação")
        st.markdown(
            "O **tcode** do FRED-MD indica como a série foi tornada estacionária. "
            "Colorir por tcode mostra se a estrutura do mapa é só efeito de transformação."
        )
        tc = meta["tcode"].value_counts().rename_axis("tcode").reset_index(name="séries")
        st.dataframe(tc, hide_index=True, width="stretch")

    with st.expander("Tabela de séries"):
        st.dataframe(meta, hide_index=True, width="stretch")
        ui.csv_download(meta, "series_meta.csv", key="dl_meta")
