"""Página 1 — visão geral: o que são os dados e como as séries se dividem por tema."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import catalogo, charts, charts_story, data, style, textos, ui


def render() -> None:
    meta = data.series_meta()
    rot = data.rotulados()
    df = data.padronizado()
    anos = df.index[-1].year - df.index[0].year

    ui.hero(
        "118 séries macroeconômicas dos EUA, de 1965 a 2026, agrupadas em 19 famílias",
        "Reunimos indicadores da economia americana (emprego, preços, juros, produção, câmbio…) "
        "e deixamos os próprios dados mostrarem quais deles se movem juntos.",
        [
            (df.shape[1], "", "indicadores econômicos mensais"),
            (anos, "anos", f"de história ({df.index[0].year} a {df.index[-1].year})"),
            (int(rot.shape[0]), "", "famílias de indicadores parecidos"),
        ],
        kicker="TCC2 · CICD06 · Instituto Mauá de Tecnologia",
    )

    st.markdown("#### Três ideias para ler este painel")
    style.html(
        """
        <div class="cards-3">
          <div class="card rise d1"><div class="kicker-s">Ideia 1</div>
            <h4>Olhamos a variação, não o valor</h4>
            <p>Em vez do nível do desemprego, usamos quanto ele mudou de um mês para o outro.
            Assim dá para comparar indicadores de naturezas diferentes, como preços e empregos.</p></div>
          <div class="card rise d2"><div class="kicker-s">Ideia 2</div>
            <h4>Família não é categoria</h4>
            <p>As 8 categorias oficiais são etiquetas de especialistas. As 19 famílias foram
            formadas pelo comportamento dos dados e podem misturar categorias.</p></div>
          <div class="card rise d3"><div class="kicker-s">Ideia 3</div>
            <h4>Andar junto não é causar</h4>
            <p>Mostramos que indicadores se movem juntos. Isso não prova que um provoca o outro.</p></div>
        </div>
        """
    )
    st.write("")

    esq, dir_ = st.columns([2, 3], gap="large")
    with esq:
        style.html(
            """
            <div class="card">
              <div class="kicker-s">Os dados</div>
              <h3>O que é o FRED-MD?</h3>
              <p>É uma base pública com mais de cem indicadores mensais da economia dos Estados
              Unidos, criada por McCracken e Ng (2016) e atualizada todos os meses pelo banco
              central de St. Louis.</p>
              <p>Cada indicador é uma <b>série</b>: uma linha do tempo, como a taxa de desemprego
              ou o preço do petróleo. Pesquisadores do mundo todo a usam para acompanhar a
              economia.</p>
              <p>Aqui usamos <b>118 séries</b>, de janeiro de 1965 a março de 2026.</p>
            </div>
            """
        )
        st.write("")
        ui.link("projeto", "Entenda o projeto do começo ao fim", ":material/menu_book:")
    with dir_:
        st.markdown("#### Séries por tema")
        st.caption(
            "As 8 categorias oficiais do FRED-MD. Escolha uma logo abaixo para ver as séries."
        )
        ui.plot(charts_story.categorias(meta, st.session_state.get("cat_pills")), key="cat_bars")
        ui.guia("categorias")

    sel = st.pills(
        "Ver as séries de um tema",
        catalogo.CATEGORIAS,
        selection_mode="single",
        key="cat_pills",
    )
    if sel:
        st.markdown(f"##### Séries de **{sel}**")
        d = meta[meta["categoria"] == sel][["serie", "descricao", "cluster", "rotulo"]].copy()
        d["família"] = d["cluster"].astype(str) + " · " + d["rotulo"]
        st.dataframe(
            d[["serie", "descricao", "família"]].rename(
                columns={"serie": "Código", "descricao": "O que mede"}
            ),
            hide_index=True,
            width="stretch",
        )

    st.divider()
    st.subheader("Como chegamos às 19 famílias")
    style.html(
        """
        <div class="cards-3">
          <div class="card rise d1"><div class="step"><div class="n">1</div><div>
            <h4>Juntamos os indicadores</h4>
            <p>118 séries mensais, todas colocadas na mesma escala para poderem ser comparadas.</p>
          </div></div></div>
          <div class="card rise d2"><div class="step"><div class="n">2</div><div>
            <h4>Agrupamos os parecidos</h4>
            <p>Séries que sobem e descem nos mesmos meses ficam na mesma <b>família</b>.</p>
          </div></div></div>
          <div class="card rise d3"><div class="step"><div class="n">3</div><div>
            <h4>Descobrimos o que move cada uma</h4>
            <p>Comparamos cada família com seis indicadores conhecidos: produção, inflação, juros,
            bolsa e câmbio.</p>
          </div></div></div>
        </div>
        """
    )

    st.divider()
    st.subheader("Para onde ir agora")
    c = st.columns(4)
    with c[0]:
        ui.link("achados", "Os quatro achados", ":material/emoji_objects:")
    with c[1]:
        ui.link("explorar", "Explorar uma família", ":material/travel_explore:")
    with c[2]:
        ui.link("variaveis", "Variáveis de referência", ":material/thermostat:")
    with c[3]:
        ui.link("mapa", "Mapa das séries", ":material/scatter_plot:")

    st.divider()
    st.subheader("As 19 famílias e suas séries")
    n_mistas, n_total, _ = textos.mistura_categorias()
    st.caption(
        f"{n_mistas} das {n_total} famílias reúnem séries de mais de uma categoria oficial: "
        "os dados ligam indicadores que a classificação tradicional separa."
    )
    ui.plot(charts.treemap(data.clusters(), rot), key="treemap")
    ui.guia("treemap")
