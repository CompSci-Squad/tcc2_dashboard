"""Ponto de entrada do Streamlit: `streamlit run src/tcc2_dashboard/app.py`."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard.views import (
    centroides,
    estabilidade,
    mapa,
    metodologia,
    rede,
    regressao,
    series,
    visao_geral,
)


def main() -> None:
    st.set_page_config(
        page_title="TCC2 · FRED-MD",
        page_icon=":material/hub:",
        layout="wide",
        menu_items={
            "About": "TCC2 CICD06 — agrupamento de séries do FRED-MD (Santos et al., 2021)."
        },
    )
    paginas = {
        "Resultados": [
            st.Page(
                visao_geral.render,
                title="Visão geral",
                icon=":material/dashboard:",
                url_path="visao-geral",
                default=True,
            ),
            st.Page(
                mapa.render,
                title="Mapa das séries",
                icon=":material/scatter_plot:",
                url_path="mapa",
            ),
            st.Page(
                centroides.render,
                title="Centroides no tempo",
                icon=":material/show_chart:",
                url_path="centroides",
            ),
            st.Page(
                series.render,
                title="Explorador de séries",
                icon=":material/compare_arrows:",
                url_path="series",
            ),
            st.Page(
                rede.render, title="Rede de correlação", icon=":material/hub:", url_path="rede"
            ),
        ],
        "Inferência": [
            st.Page(
                regressao.render,
                title="Regressão",
                icon=":material/functions:",
                url_path="regressao",
            ),
            st.Page(
                estabilidade.render,
                title="Estabilidade",
                icon=":material/verified:",
                url_path="estabilidade",
            ),
        ],
        "Sobre": [
            st.Page(
                metodologia.render,
                title="Metodologia",
                icon=":material/menu_book:",
                url_path="metodologia",
            ),
        ],
    }
    st.navigation(paginas).run()


main()
