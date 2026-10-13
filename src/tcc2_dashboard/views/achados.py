"""Página 2 — os quatro achados genuínos, contados em poucas frases."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tcc2_dashboard import catalogo, charts_story, data, style, textos, ui
from tcc2_dashboard.config import CLUSTERS_ACHADO


def _suave(s: pd.Series, k: int) -> pd.Series:
    return s.rolling(k, min_periods=1).mean() if k > 1 else s


def _cartao(i: int, cid: int) -> str:
    info = textos.info_familia(cid)
    ach = catalogo.ACHADOS[cid]
    m = info["membros"]
    chips = "".join(
        style.chip_serie(s, d) for s, d in zip(m["serie"][:8], m["descricao"][:8], strict=True)
    )
    if len(m) > 8:
        chips += f'<span class="serie-chip">+{len(m) - 8}</span>'
    est = ""
    if info["estabilidade"]:
        rot, tipo = info["estabilidade"]
        est = style.pill(f"Grupo {rot}", tipo)
    return f"""
    <div class="card achado rise d{i}">
      <div class="top">
        <div><span class="badge">Achado {i}</span><h3>{style.esc(ach["titulo"])}</h3></div>
        {style.anel(info["r2"] * 100, "explicado")}
      </div>
      <div class="leitura">{style.esc(ach["leitura"])}</div>
      <div class="meta">
        <div><span>Responde a</span><b>{style.esc(info["var_nome"])}</b></div>
        <div><span>Séries na família</span><b>{info["n"]}</b></div>
      </div>
      <div>{chips}</div>
      <div>{est}</div>
    </div>
    """


def render() -> None:
    ui.cabecalho(
        "Os quatro achados",
        "Entre as 19 famílias, quatro respondem a um indicador conhecido de um jeito que não era "
        "óbvio de antemão. São as descobertas do estudo.",
        kicker="O que encontramos",
    )

    style.html(
        '<div class="callout"><b>O que é um achado genuíno?</b> É uma relação que não nasce da '
        "forma como as séries são calculadas. Por exemplo: é óbvio que os subíndices da produção "
        "industrial acompanhem a produção industrial. Já descobrir que o desemprego de curto prazo "
        "também a acompanha é uma informação nova.</div>"
    )

    style.html(
        '<div class="cards-2">'
        + "".join(_cartao(i + 1, c) for i, c in enumerate(CLUSTERS_ACHADO))
        + "</div>"
    )
    st.caption("Passe o mouse sobre um código de série para ver o que ele mede.")
    ui.guia("achados_cartoes", aberto=True, titulo="Como ler estes cartões")

    st.divider()
    st.subheader("Veja com os próprios olhos")
    st.caption(
        "Escolha um achado. A linha cheia é a família; a pontilhada é o indicador de referência."
    )
    ui.guia("achados_grafico")
    abas = st.tabs([f"Achado {i + 1}" for i in range(len(CLUSTERS_ACHADO))])
    reg_x = data.regressores()
    cen = data.centroides()
    for aba, cid in zip(abas, CLUSTERS_ACHADO, strict=True):
        with aba:
            info = textos.info_familia(cid)
            ach = catalogo.ACHADOS[cid]
            var = info["var"]
            st.markdown(f"**{ach['titulo']}** · responde a **{info['var_nome']}**")
            suav = st.slider(
                "Suavizar (meses)",
                1,
                24,
                6,
                key=f"suav_{cid}",
                help="Média móvel: deixa as linhas menos nervosas.",
            )
            x = reg_x[var].dropna()
            y = cen.loc[x.index, cid]
            c1, c2 = st.columns([3, 2], gap="large")
            with c1:
                ui.plot(
                    charts_story.sobreposicao(
                        _suave(y, suav), _suave(x, suav), f"Família {cid}", info["var_nome"], cid
                    ),
                    key=f"sobre_{cid}",
                )
                if info["coef"] < 0:
                    st.caption(
                        "Atenção: aqui as duas linhas tendem a andar em sentidos **opostos**."
                    )
                st.caption(
                    "A escala está ampliada: os extremos de 2020 (pandemia) saem da tela. Dê duplo "
                    "clique no gráfico para ver tudo."
                )
            with c2:
                st.markdown("##### Séries da família")
                tab = info["membros"][["serie", "descricao", "corr_centroide"]].rename(
                    columns={
                        "serie": "Código",
                        "descricao": "O que mede",
                        "corr_centroide": "Quão típica",
                    }
                )
                st.dataframe(
                    tab,
                    hide_index=True,
                    width="stretch",
                    column_config={
                        "Quão típica": st.column_config.ProgressColumn(
                            "Quão típica",
                            min_value=0,
                            max_value=1,
                            format="%.2f",
                            help="O quanto a série acompanha o perfil médio da família.",
                        )
                    },
                )
                if info["jaccard"] is not None:
                    rot, _ = info["estabilidade"]
                    st.caption(
                        f"Estabilidade da família: {info['jaccard']:.0%} ({rot}). Mede se o grupo "
                        "se repete quando refazemos a análise embaralhando os meses."
                    )
            style.html(
                f"""
                <div class="guia">
                  <div class="g"><span>O que isso quer dizer</span><p>{style.esc(textos.interpretacao_numerica(info))}</p></div>
                  <div class="g c"><span>Por que pode fazer sentido (hipótese)</span><p>{style.esc(ach["hipotese"])}</p></div>
                  <div class="g w"><span>Cuidado nesta leitura</span><p>{style.esc(ach["cuidado"])}</p></div>
                </div>
                """
            )

    st.divider()
    with st.expander("E os outros grupos com relação forte?"):
        rot = data.rotulados()
        sanidade = rot[(rot["forte"]) & (~rot["achado"])]
        st.markdown(
            "Três famílias também têm relação forte, mas ela é **óbvia** pela forma como as séries "
            "são construídas. Elas servem como *conferência do método*: se ele funciona, deveria "
            "encontrá-las, e encontrou."
        )
        for r in sanidade.itertuples():
            st.markdown(
                f"- **Família {r.cluster} · {r.rotulo_curto}**: explicada em {r.r_squared:.0%}."
            )
    st.info(
        "Duas ressalvas: indicadores que andam juntos não são necessariamente causa um do outro, e "
        "uma família estável é mais confiável do que uma instável. Os detalhes estão em "
        "*Detalhes técnicos*.",
        icon=":material/info:",
    )
