"""Ponto de entrada do Streamlit: `streamlit run src/tcc2_dashboard/app.py`."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import style, ui
from tcc2_dashboard.config import ASSETS_DIR
from tcc2_dashboard.views import (
    achados,
    centroides,
    estabilidade,
    explorar,
    mapa,
    metodologia,
    projeto,
    rede,
    regressao,
    series,
    variaveis,
    visao_geral,
)

# (chave, módulo, título, ícone, url) agrupados como aparecem no menu
MENU = {
    "Comece por aqui": [
        ("visao", visao_geral, "Visão geral", ":material/dashboard:", "visao-geral"),
        ("achados", achados, "Os quatro achados", ":material/emoji_objects:", "achados"),
        ("explorar", explorar, "Explorar famílias", ":material/travel_explore:", "explorar"),
        ("variaveis", variaveis, "Variáveis de referência", ":material/thermostat:", "variaveis"),
        ("projeto", projeto, "O projeto", ":material/menu_book:", "projeto"),
    ],
    "Aprofunde": [
        ("mapa", mapa, "Mapa das séries", ":material/scatter_plot:", "mapa"),
        ("comparar", centroides, "Comparar famílias", ":material/show_chart:", "comparar"),
        ("series", series, "Explorador de séries", ":material/compare_arrows:", "series"),
        ("rede", rede, "Rede de semelhanças", ":material/hub:", "rede"),
    ],
    "Detalhes técnicos": [
        ("regressao", regressao, "Regressão", ":material/functions:", "regressao"),
        ("estabilidade", estabilidade, "Estabilidade", ":material/verified:", "estabilidade"),
        ("metodologia", metodologia, "Metodologia", ":material/science:", "metodologia"),
    ],
}


def main() -> None:
    st.set_page_config(
        page_title="TCC2 · FRED-MD",
        page_icon=":material/hub:",
        layout="wide",
        menu_items={
            "About": "TCC2 CICD06 — agrupamento de séries do FRED-MD (Santos et al., 2021)."
        },
    )
    style.aplicar()
    logo = "logo-dark.svg" if style.tema() == "dark" else "logo.svg"
    st.logo(str(ASSETS_DIR / logo), icon_image=str(ASSETS_DIR / "icon.svg"), size="large")

    paginas: dict[str, list] = {}
    for grupo, itens in MENU.items():
        paginas[grupo] = []
        for chave, modulo, titulo, icone, url in itens:
            pagina = st.Page(
                modulo.render, title=titulo, icon=icone, url_path=url, default=chave == "visao"
            )
            ui.PAGINAS[chave] = pagina
            paginas[grupo].append(pagina)

    st.navigation(paginas).run()
    with st.sidebar:
        st.caption("Tema claro ou escuro: menu ⋮ no canto superior direito → Settings → Theme.")


main()
