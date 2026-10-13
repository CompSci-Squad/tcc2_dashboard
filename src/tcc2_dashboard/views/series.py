"""Explorador de séries: compare dois indicadores e veja os mais parecidos com cada um."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import catalogo, charts, data, style, ui
from tcc2_dashboard.config import K


def render() -> None:
    ui.cabecalho(
        "Explorador de séries",
        "Compare dois indicadores quaisquer e descubra quais outros se parecem com eles.",
        kicker="Aprofunde",
    )
    df = data.padronizado()
    corr = data.correlacao_series()
    cl_de = data.cluster_de()
    rot = data.rotulo_curto()

    aba1, aba2 = st.tabs(["Comparar dois indicadores", "Mapa de semelhanças"])

    with aba1:
        todas = sorted(df.columns)
        c1, c2 = st.columns(2)
        a = c1.selectbox(
            "Primeiro indicador",
            todas,
            format_func=catalogo.rotulo,
            index=todas.index("UNRATE"),
        )
        outras = [s for s in todas if s != a]
        vizinha = corr[a].drop(a).abs().idxmax()
        b = c2.selectbox(
            "Segundo indicador",
            outras,
            format_func=catalogo.rotulo,
            index=outras.index(vizinha),
            help="Já vem escolhido o indicador mais parecido com o primeiro.",
        )
        janela = st.slider(
            "Janela da comparação (meses)",
            12,
            120,
            60,
            6,
            help="A linha de baixo mostra o quanto os dois andam juntos nesse período móvel.",
        )

        ui.plot(charts.par_series(df, a, b, janela), key="par")
        r = corr.loc[a, b]
        forca = (
            "muito parecidos"
            if abs(r) > 0.7
            else "parecidos"
            if abs(r) > 0.4
            else "pouco parecidos"
        )
        sentido = "no mesmo sentido" if r > 0 else "em sentidos opostos"
        style.html(
            f'<div class="callout"><b>{style.esc(a)}</b> e <b>{style.esc(b)}</b> são {forca} '
            f"({style.esc(sentido)}). Estão em {'a mesma família' if cl_de[a] == cl_de[b] else 'famílias diferentes'}: "
            f"{cl_de[a]} · {style.esc(rot[cl_de[a]])}"
            f"{'' if cl_de[a] == cl_de[b] else f' e {cl_de[b]} · {style.esc(rot[cl_de[b]])}'}.</div>"
        )

        st.markdown(f"##### Indicadores mais parecidos com **{a}**")
        n = st.slider("Quantos mostrar", 5, 30, 10, key="n_viz")
        viz = corr[a].drop(a)
        top = viz.reindex(viz.abs().sort_values(ascending=False).index).head(n)
        tabela = top.rename("Semelhança").to_frame()
        tabela.insert(0, "O que mede", [catalogo.nome(s) for s in tabela.index])
        tabela["Família"] = [f"{cl_de[s]} · {rot[cl_de[s]]}" for s in tabela.index]
        tabela.index.name = "Código"
        st.dataframe(
            tabela,
            width="stretch",
            column_config={
                "Semelhança": st.column_config.ProgressColumn(
                    "Semelhança",
                    min_value=-1,
                    max_value=1,
                    format="%.2f",
                    help="De -1 (opostos) a 1 (idênticos).",
                )
            },
        )

    with aba2:
        st.markdown(
            "Cada quadradinho compara duas séries: **azul** = andam juntas, **vermelho** = em "
            "sentidos opostos. Os blocos azuis na diagonal são as famílias."
        )
        escolha = st.multiselect(
            "Mostrar só algumas famílias (vazio = todas)",
            list(range(K)),
            format_func=data.nome_cluster,
        )
        series = sorted(
            [s for s in df.columns if not escolha or cl_de[s] in escolha],
            key=lambda s: (cl_de[s], s),
        )
        ui.plot(charts.heatmap_correlacao(corr.loc[series, series], cl_de), key="heat_corr")
        st.caption("Passe o mouse em um quadrado para ver o que cada série mede.")
