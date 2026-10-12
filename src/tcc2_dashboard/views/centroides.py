"""Página 3 — centroides no tempo e séries-membro, com janela de datas e recessões NBER."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tcc2_dashboard import charts, data, ui
from tcc2_dashboard.config import CLUSTERS_ACHADO, K

ATALHOS = {
    "Achados genuínos": lambda rot: CLUSTERS_ACHADO,
    "Clusters fortes": lambda rot: rot.loc[rot["forte"], "cluster"].tolist(),
    "Todos": lambda rot: list(range(K)),
    "Limpar": lambda rot: [],
}


def _aplicar_atalho() -> None:
    # só roda quando o usuário clica na pílula; edições manuais do multiselect não são sobrescritas
    escolha = st.session_state.get("cen_atalho")
    if escolha:
        st.session_state["cen_sel"] = ATALHOS[escolha](data.rotulados())


def render() -> None:
    ui.cabecalho(
        "Centroides no tempo",
        "O centroide de um cluster é a média padronizada de suas séries-membro mês a mês.",
    )
    cen = data.centroides()
    nomes = data.rotulo_curto()
    idx = cen.index

    with st.sidebar:
        st.header("Centroides")
        st.session_state.setdefault("cen_sel", [ui.foco()])
        st.pills(
            "Atalho",
            list(ATALHOS),
            selection_mode="single",
            key="cen_atalho",
            on_change=_aplicar_atalho,
        )
        sel = st.multiselect(
            "Clusters", list(range(K)), key="cen_sel", format_func=data.nome_cluster
        )
        janela = st.slider(
            "Janela de datas",
            idx[0].to_pydatetime(),
            idx[-1].to_pydatetime(),
            (idx[0].to_pydatetime(), idx[-1].to_pydatetime()),
            format="MM/YYYY",
        )
        suavizar = st.slider("Média móvel (meses)", 1, 24, 1)
        recessoes = st.toggle("Sombrear recessões (NBER)", value=True)
        paineis = st.toggle("Um painel por cluster", value=False)

    if not sel:
        st.info("Escolha ao menos um cluster na barra lateral.")
        return

    j = (pd.Timestamp(janela[0]), pd.Timestamp(janela[1]))
    ui.plot(charts.centroides(cen, sel, nomes, j, suavizar, recessoes, paineis), width="stretch")

    d = cen.loc[j[0] : j[1], sel]
    resumo = d.agg(["mean", "std", "min", "max"]).T.rename(
        columns={"mean": "média", "std": "desvio-padrão", "min": "mínimo", "max": "máximo"}
    )
    resumo.index = [data.nome_cluster(c) for c in resumo.index]
    a, b = st.columns([3, 2])
    with a:
        st.markdown("**Estatística descritiva na janela escolhida**")
        st.dataframe(resumo.round(3), width="stretch")
    with b:
        if len(sel) > 1:
            st.markdown("**Correlação entre centroides**")
            st.dataframe(
                d.corr().round(2).style.background_gradient(cmap="RdBu_r", vmin=-1, vmax=1),
                width="stretch",
            )
    ui.csv_download(d, "centroides_janela.csv", "Baixar centroides da janela", key="dl_cen")

    st.divider()
    st.subheader("Séries-membro de um cluster")
    foco = ui.seletor_foco(key="cen")
    membros = data.clusters().query("cluster == @foco")["serie"].tolist()
    escolhidas = st.multiselect("Séries exibidas", membros, default=membros[:8], key=f"mem_{foco}")
    if escolhidas:
        ui.plot(
            charts.membros(data.padronizado(), escolhidas, cen[foco], foco, j, recessoes),
            width="stretch",
        )
    meta = data.series_meta().query("cluster == @foco")[["serie", "tcode", "corr_centroide"]]
    st.dataframe(
        meta.sort_values("corr_centroide", ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "corr_centroide": st.column_config.ProgressColumn(
                "Correlação com o centroide", min_value=-1, max_value=1, format="%.2f"
            )
        },
    )
