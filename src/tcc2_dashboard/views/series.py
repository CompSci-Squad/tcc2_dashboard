"""Página 5 — explorador de séries: heatmap de correlação e comparação par a par."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import charts, data, ui


def render() -> None:
    ui.cabecalho(
        "Explorador de séries",
        "Compare séries individuais, veja vizinhas mais correlacionadas e a correlação móvel.",
    )
    df = data.padronizado()
    corr = data.correlacao_series()
    cl_de = data.cluster_de()
    meta = data.series_meta().set_index("serie")

    aba1, aba2 = st.tabs(["Comparar duas séries", "Heatmap de correlação"])

    with aba1:
        todas = sorted(df.columns)
        c1, c2, c3 = st.columns([2, 2, 1])
        a = c1.selectbox(
            "Série A", todas, index=todas.index("CPIAUCSL") if "CPIAUCSL" in todas else 0
        )
        # sugere a série mais correlacionada como padrão de B
        vizinha = corr[a].drop(a).abs().idxmax()
        b = c2.selectbox(
            "Série B",
            [s for s in todas if s != a],
            index=[s for s in todas if s != a].index(vizinha),
        )
        janela = c3.slider("Janela móvel (meses)", 12, 120, 60, 6)

        st.plotly_chart(charts.par_series(df, a, b, janela), width="stretch")
        m = st.columns(4)
        m[0].metric("r de Pearson", f"{corr.loc[a, b]:.3f}")
        m[1].metric(f"Cluster de {a}", cl_de[a])
        m[2].metric(f"Cluster de {b}", cl_de[b])
        m[3].metric("Mesmo cluster?", "sim" if cl_de[a] == cl_de[b] else "não")

        st.markdown(f"**Séries mais correlacionadas com `{a}`** (|r|)")
        n = st.slider("Quantas mostrar", 5, 30, 10, key="n_viz")
        viz = corr[a].drop(a)
        top = viz.reindex(viz.abs().sort_values(ascending=False).index).head(n)
        tabela = top.rename("r").to_frame()
        tabela["cluster"] = [cl_de[s] for s in tabela.index]
        tabela["rótulo do cluster"] = [meta.loc[s, "rotulo"] for s in tabela.index]
        st.dataframe(
            tabela,
            width="stretch",
            column_config={
                "r": st.column_config.ProgressColumn("r", min_value=-1, max_value=1, format="%.2f")
            },
        )

    with aba2:
        escolha = st.multiselect(
            "Restringir a clusters (vazio = todas as 118 séries)",
            list(range(19)),
            format_func=data.nome_cluster,
        )
        ordem = st.radio("Ordem", ["Por cluster", "Alfabética"], horizontal=True)
        series = [s for s in df.columns if not escolha or cl_de[s] in escolha]
        if ordem == "Por cluster":
            series = sorted(series, key=lambda s: (cl_de[s], s))
        else:
            series = sorted(series)
        st.plotly_chart(charts.heatmap_correlacao(corr.loc[series, series], cl_de), width="stretch")
        st.caption(
            "Em “Por cluster” os blocos quadrados na diagonal mostram clusters coesos. "
            "Com até 40 séries os nomes aparecem nos eixos."
        )
