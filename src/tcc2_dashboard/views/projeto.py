"""Página 5 — o projeto explicado para quem não é da área."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import catalogo, explicacoes, style, ui

PASSOS = [
    (
        "Preparar os dados",
        "Usamos a variação de cada mês (não o valor absoluto), preenchemos os poucos buracos "
        "(0,24% das células) e colocamos todas as séries na mesma escala.",
    ),
    (
        "Conferir se vale a pena agrupar",
        "Dois testes estatísticos confirmaram que as séries têm padrões em comum. Sem isso, "
        "qualquer agrupamento seria arbitrário.",
    ),
    (
        "Decidir quantos grupos formar",
        "Não chutamos: o número (19) veio de um critério que preserva 70% da informação dos dados.",
    ),
    (
        "Agrupar as séries",
        "Um algoritmo de agrupamento (K-Means) junta as séries que se comportam de forma parecida.",
    ),
    (
        "Explicar cada grupo",
        "Comparamos o perfil médio de cada família com seis indicadores conhecidos: produção "
        "industrial, inflação, juros, curva de juros, bolsa e câmbio.",
    ),
    (
        "Separar o óbvio do novo",
        "Dos grupos com relação forte, alguns são óbvios pela forma como são construídos. Ficamos "
        "com os quatro que trazem informação nova: os achados.",
    ),
]


def render() -> None:
    ui.cabecalho(
        "O projeto",
        "Como organizar mais de cem indicadores econômicos em poucos grupos que fazem sentido, "
        "e descobrir o que move cada um?",
        kicker="Sobre o trabalho",
    )

    style.html(
        """
        <div class="cards-3">
          <div class="card rise d1"><div class="kicker-s">O problema</div><h3>Indicadores demais</h3>
            <p>Para acompanhar a economia é preciso olhar centenas de números por mês: produção,
            preços, emprego, juros. É difícil saber quais se movem juntos.</p></div>
          <div class="card rise d2"><div class="kicker-s">A ideia</div><h3>Deixar os dados agruparem</h3>
            <p>Em vez de classificar os indicadores à mão, deixamos o computador juntar os que
            sobem e descem nos mesmos momentos, como termômetros que marcam o mesmo calor.</p></div>
          <div class="card rise d3"><div class="kicker-s">Para que serve</div><h3>Enxergar a estrutura</h3>
            <p>Mostra quais partes da economia andam juntas, revela ligações que não eram óbvias e
            pode ser repetido quando a base for atualizada.</p></div>
        </div>
        """
    )

    st.divider()
    st.subheader("Como fizemos, em seis passos")
    st.caption(
        "Seguimos o método de Santos et al. (2021), criado para ativos financeiros e adaptado aqui para indicadores macroeconômicos."
    )
    linhas = "".join(
        f'<div class="card rise d{min(i + 1, 6)}"><div class="step"><div class="n">{i + 1}</div>'
        f"<div><h4>{style.esc(t)}</h4><p>{style.esc(d)}</p></div></div></div>"
        for i, (t, d) in enumerate(PASSOS)
    )
    style.html(f'<div class="cards-2">{linhas}</div>')

    st.divider()
    st.subheader("O que encontramos")
    style.html(
        """
        <div class="cards-3">
          <div class="card"><div class="kicker-s">Famílias</div><h3>19</h3>
            <p>de 2 a 24 séries cada uma, formadas só pelo comportamento no tempo.</p></div>
          <div class="card"><div class="kicker-s">Com relação forte</div><h3>7</h3>
            <p>têm um indicador de referência que explica boa parte do seu vai e vem.</p></div>
          <div class="card"><div class="kicker-s">Achados genuínos</div><h3>4</h3>
            <p>relações que não eram óbvias: desemprego e crédito, juros, emprego e consumo, câmbio.</p></div>
        </div>
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        ui.link("achados", "Ver os quatro achados", ":material/emoji_objects:")
    with c2:
        ui.link("explorar", "Explorar as famílias", ":material/travel_explore:")

    st.divider()
    st.subheader("Perguntas que costumam aparecer")
    for pergunta, resposta in explicacoes.FAQ:
        with st.expander(pergunta):
            st.markdown(resposta)

    st.divider()
    st.subheader("O que o trabalho não diz")
    st.markdown(
        "- **Andar junto não é causar.** Mostramos que os indicadores se movem juntos, não que um "
        "provoca o outro.\n"
        "- **Alguns grupos são menos firmes que outros.** Quando refazemos a análise embaralhando "
        "os meses, parte das famílias se repete só em parte (veja a estabilidade em cada achado).\n"
        "- **Três famílias não têm relação clara** com nenhum dos seis indicadores, o que é "
        "esperado quando se testam tantas combinações.\n"
        "- **Há limitações técnicas** na preparação dos dados, descritas com transparência na "
        "página *Detalhes técnicos*."
    )

    st.divider()
    st.subheader("Quem fez")
    style.html(
        """
        <div class="card">
          <p style="color:var(--ink)"><b>Douglas Puglisi Aldred, Gustavo Affonso Duran, Guilherme
          Costa Figueiredo Pereira e Léo Vieira Gracio Peixoto</b></p>
          <p>Ciência da Computação · Centro Universitário do Instituto Mauá de Tecnologia (IMT)
          · Orientador: Prof. Dr. Evandro Catelani Ferraz</p>
          <p>Código aberto: <a href="https://github.com/CompSci-Squad/tcc2" target="_blank">github.com/CompSci-Squad/tcc2</a></p>
        </div>
        """
    )

    st.divider()
    st.subheader("Fontes")
    st.markdown(
        "- McCracken, M. W. e Ng, S. (2016). *FRED-MD: A Monthly Database for Macroeconomic "
        "Research*. Journal of Business & Economic Statistics, 34(4), 574–589.\n"
        "- Santos, D. R. et al. (2021). *Clusterização de ativos e suas relações com variáveis "
        "macroeconômicas e índices financeiros*. Research, Society and Development, 10(2)."
    )

    with st.expander("Glossário: palavras que aparecem no painel"):
        for termo, texto in catalogo.GLOSSARIO.items():
            st.markdown(f"**{termo}**: {texto}")
