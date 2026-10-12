"""Página 1 — visão geral dos 19 clusters (clique em uma barra para colocar o cluster em foco)."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import charts, data, ui
from tcc2_dashboard.config import R2_FORTE


def render() -> None:
    ui.cabecalho(
        "Agrupamento de séries do FRED-MD",
        "K-Means sobre 118 séries macroeconômicas mensais. Cada ponto é uma série inteira, "
        "descrita pelo seu comportamento no tempo, não uma observação mensal.",
        kicker="TCC2 · CICD06 · Santos et al. (2021)",
        chips=["FRED-MD 2026-04", "1965 → 2026", "k = 19", "Regressão HAC", "Bootstrap em blocos"],
    )
    rot = data.rotulados()
    cl = data.clusters()
    df = data.padronizado()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Séries agrupadas", df.shape[1])
    c2.metric(
        "Meses", df.shape[0], f"{df.index[0]:%m/%Y} → {df.index[-1]:%m/%Y}", delta_color="off"
    )
    c3.metric("Clusters (k)", rot.shape[0])
    c4.metric("Clusters fortes", int(rot["forte"].sum()), f"R² > {R2_FORTE}", delta_color="off")
    c5.metric(
        "Achados genuínos", int(rot["achado"].sum()), "clusters 3, 4, 14, 18", delta_color="off"
    )

    corte = st.slider(
        "Corte de R² para “cluster forte”",
        0.0,
        1.0,
        R2_FORTE,
        0.05,
        help="Reclassifica visualmente a barra; a classificação oficial usa 0,4.",
    )
    foco = ui.foco()

    esq, dir_ = st.columns(2)
    with esq:
        st.subheader("Tamanho dos clusters")
        ev = ui.plot(
            charts.tamanhos(rot, foco),
            on_select="rerun",
            selection_mode="points",
            key="ev_tamanhos",
            width="stretch",
        )
        ui.clique_em_cluster(ev, "ult_tamanhos")
    with dir_:
        st.subheader("Poder explicativo da regressão (R²)")
        ev = ui.plot(
            charts.r2_por_cluster(rot, corte, foco),
            on_select="rerun",
            selection_mode="points",
            key="ev_r2",
            width="stretch",
        )
        ui.clique_em_cluster(ev, "ult_r2")
    st.caption(
        f"{int((rot['r_squared'] > corte).sum())} clusters acima do corte de R² = {corte:.2f}. "
        "Clique em uma barra para detalhar abaixo."
    )

    st.divider()
    st.subheader("Cluster em foco")
    ui.seletor_foco(label="Escolha (ou clique nos gráficos acima)", key="vg")
    foco = ui.foco()
    linha = rot.loc[rot["cluster"] == foco].iloc[0]
    membros = cl.loc[cl["cluster"] == foco, "serie"].tolist()

    a, b = st.columns([3, 2])
    with a:
        st.markdown(f"#### Cluster {foco} · {linha['rotulo_curto']}")
        if linha["rotulo_proposto"] != linha["rotulo_curto"]:
            st.markdown(linha["rotulo_proposto"])
        st.markdown("**Séries-membro:** " + ", ".join(f"`{s}`" for s in membros))
    with b:
        m1, m2 = st.columns(2)
        m1.metric("R²", f"{linha['r_squared']:.3f}")
        m2.metric("Variável dominante", linha["variavel_dominante"])
        m1.metric("Durbin-Watson", f"{linha['durbin_watson']:.2f}")
        m2.metric("Classe", linha["classe"])
    cen = data.centroides()
    ui.plot(
        charts.centroides(
            cen, [foco], data.rotulo_curto(), (cen.index[0], cen.index[-1]), 1, True, False
        )
    )

    st.divider()
    st.subheader("Mapa hierárquico: cluster → séries")
    st.caption("Área proporcional ao nº de séries; cor = R². Clique para dar zoom em um cluster.")
    ui.plot(charts.treemap(cl, rot), width="stretch")

    with st.expander("Tabela completa dos clusters"):
        mostra = rot[
            [
                "cluster",
                "n_series",
                "rotulo_curto",
                "variavel_dominante",
                "r_squared",
                "durbin_watson",
                "classe",
            ]
        ]
        st.dataframe(mostra, hide_index=True, width="stretch")
        ui.csv_download(mostra, "clusters_resumo.csv", key="dl_vg")
