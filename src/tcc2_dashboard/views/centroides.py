"""Comparar famílias: perfis médios no tempo lado a lado, com recessões e animação."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tcc2_dashboard import charts, charts_story, data, ui
from tcc2_dashboard.config import CLUSTERS_ACHADO, K

ATALHOS = {
    "Os quatro achados": lambda rot: CLUSTERS_ACHADO,
    "Famílias fortes": lambda rot: rot.loc[rot["forte"], "cluster"].tolist(),
    "Todas": lambda rot: list(range(K)),
    "Limpar": lambda rot: [],
}


def _aplicar_atalho() -> None:
    # só roda quando a pessoa clica na pílula: edições manuais do multiselect não são sobrescritas
    escolha = st.session_state.get("cen_atalho")
    if escolha:
        st.session_state["cen_sel"] = ATALHOS[escolha](data.rotulados())


def render() -> None:
    ui.cabecalho(
        "Comparar famílias",
        "Coloque várias famílias no mesmo gráfico e veja quais reagem às mesmas crises.",
        kicker="Aprofunde",
    )
    cen = data.centroides()
    nomes = data.rotulo_curto()
    idx = cen.index

    st.session_state.setdefault("cen_sel", [ui.foco()])
    st.pills(
        "Atalhos",
        list(ATALHOS),
        selection_mode="single",
        key="cen_atalho",
        on_change=_aplicar_atalho,
    )
    sel = st.multiselect("Famílias", list(range(K)), key="cen_sel", format_func=data.nome_cluster)

    c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 2, 1], vertical_alignment="bottom")
    janela = c1.slider(
        "Período",
        idx[0].to_pydatetime(),
        idx[-1].to_pydatetime(),
        (idx[0].to_pydatetime(), idx[-1].to_pydatetime()),
        format="MM/YYYY",
    )
    suavizar = c2.slider(
        "Suavizar (meses)", 1, 24, 1, help="Média móvel: deixa a linha menos nervosa."
    )
    recessoes = c3.toggle("Recessões", value=True, help="Faixas cinza = recessões dos EUA (NBER).")
    zoom = c5.toggle(
        "Ampliar",
        value=True,
        help="Ignora picos extremos (como a pandemia de 2020) para dar zoom no resto.",
    )
    paineis = c4.toggle("Um gráfico por família", value=False)

    if not sel:
        st.info("Escolha ao menos uma família acima.")
        return

    j = (pd.Timestamp(janela[0]), pd.Timestamp(janela[1]))
    aba1, aba2 = st.tabs(["Gráfico", "Animação ano a ano"])
    with aba1:
        ui.plot(
            charts.centroides(cen, sel, nomes, j, suavizar, recessoes, paineis, zoom),
            key="cen_main",
        )
    with aba2:
        st.caption("Aperte ▶ Reproduzir para ver a linha se desenhar de 1965 até hoje.")
        ui.plot(charts_story.centroide_animado(cen, sel, nomes, recessoes), key="cen_anim")
    ui.guia("comparar")

    d = cen.loc[j[0] : j[1], sel]
    if len(sel) > 1:
        st.markdown("#### Quais famílias andam juntas?")
        ui.plot(charts.heatmap_familias(d.corr(), nomes), key="corr_fam")
        ui.guia("comparar_corr", titulo="Como ler esta grade")
    ui.csv_download(d, "perfis_das_familias.csv", "Baixar os dados do gráfico", key="dl_cen")
