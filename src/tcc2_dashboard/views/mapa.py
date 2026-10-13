"""Mapa das séries: animação categorias → famílias e mapa interativo (PCA)."""

from __future__ import annotations

import numpy as np
import streamlit as st

from tcc2_dashboard import analysis, catalogo, charts, charts_story, data, ui
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
        "Cada ponto é uma série. Pontos próximos se comportam de forma parecida ao longo dos anos.",
        kicker="Aprofunde",
    )
    meta = data.series_meta()
    nomes = data.rotulo_curto()

    aba1, aba2 = st.tabs(["Das categorias às famílias", "Mapa interativo"])

    with aba1:
        st.markdown(
            "Os especialistas organizam o FRED-MD em **8 categorias** (produção, trabalho, preços…). "
            "Nosso método ignora essas etiquetas e agrupa só pelo comportamento. "
            "Aperte o botão **2** e veja os pontos se reorganizarem."
        )
        pca = _pca(3)
        ui.plot(charts_story.mapa_morph(pca.coords, meta, nomes), key="morph")
        chips = " ".join(
            f'<span class="pill" style="color:{catalogo.CATEGORIA_COR[c]}">● {c}</span>'
            for c in catalogo.CATEGORIAS
        )
        st.markdown(chips, unsafe_allow_html=True)
        st.caption(
            "Na vista 1, a cor é a categoria oficial. Na vista 2, a posição vem do comportamento "
            "das séries e a cor mostra a família. Passe o mouse em qualquer ponto para saber o que "
            "a série mede."
        )

    with aba2:
        with st.expander("Opções do mapa", expanded=True):
            c1, c2, c3 = st.columns(3)
            dim = c1.radio("Visualização", ["2D", "3D"], horizontal=True)
            cor_por = c2.radio(
                "Colorir por",
                ["cluster", "categoria", "corr_centroide"],
                format_func={
                    "cluster": "Família",
                    "categoria": "Categoria oficial",
                    "corr_centroide": "Quão típica na família",
                }.get,
                horizontal=False,
            )
            destacar = c3.multiselect(
                "Destacar famílias",
                list(range(K)),
                format_func=data.nome_cluster,
                help="As demais ficam esmaecidas.",
            )
            buscar = st.multiselect(
                "Procurar séries", sorted(meta["serie"]), format_func=catalogo.rotulo
            )
        pca = _pca(3)
        eixos = list(pca.coords.columns) if dim == "3D" else ["PC1", "PC2"]
        fig = charts.pca_dispersao(pca.coords, meta, eixos, cor_por, destacar, nomes, buscar)
        ui.plot(fig, key="pca_map")
        st.caption(
            "Arraste para girar (3D) ou dar zoom; clique em uma família na legenda para escondê-la "
            "ou isolá-la."
        )

    with st.expander("Detalhes técnicos: como o número de famílias foi escolhido"):
        st.markdown(
            "O número de famílias (19) veio de uma análise de componentes principais: foram "
            "necessários 19 componentes para guardar 70% da variação dos dados."
        )
        ui.plot(charts.scree(np.array(_variancia()), K), key="scree")
