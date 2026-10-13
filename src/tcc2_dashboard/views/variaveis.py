"""Página 4 — variáveis de referência: qual família responde a cada uma, e com que força."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import catalogo, charts_story, data, style, ui
from tcc2_dashboard.config import ALPHA, REG_VARS_PRINCIPAL

ESCOLHAS = {v: catalogo.REFERENCIAS[v]["nome"] for v in REG_VARS_PRINCIPAL}


def render() -> None:
    ui.cabecalho(
        "Variáveis de referência",
        "Escolha um indicador conhecido da economia e veja quais famílias reagem a ele. "
        "Quanto mais forte a cor, mais a família acompanha o indicador.",
        kicker="O que move cada família",
    )

    var = st.segmented_control(
        "Indicador",
        list(ESCOLHAS),
        format_func=lambda v: ESCOLHAS[v],
        default="INDPRO",
        selection_mode="single",
    )
    var = var or "INDPRO"
    ref = catalogo.REFERENCIAS[var]
    style.html(
        f"""
        <div class="card rise">
          <div class="kicker-s">Indicador escolhido</div>
          <h3>{style.esc(ref["nome"])}</h3>
          <p style="color:var(--ink)">{style.esc(ref["o_que"])}</p>
          <p>{style.esc(ref["por_que"])}</p>
        </div>
        """
    )
    st.write("")

    reg = data.regressao("principal")
    rot = data.rotulados()
    st.markdown("#### Quem responde a este indicador?")
    style.html(
        '<span class="pill" style="color:#4F46E5">■ mesmo sentido</span> '
        '<span class="pill" style="color:#D97706">■ sentido oposto</span> '
        '<span class="pill">■ sem resposta clara</span>'
    )
    ui.plot(
        charts_story.mapa_variavel(reg, REG_VARS_PRINCIPAL, var, ALPHA, rot),
        key=f"tiles_{var}",
    )
    st.caption(
        "Cada quadrado é uma família. Passe o mouse para ler o resultado em palavras, ou use o "
        "botão para ver os seis indicadores em sequência."
    )

    # ranking em linguagem simples
    d = reg.set_index("cluster")
    ok = d[d[f"pvalue_{var}"] < ALPHA].copy()
    ok["forca"] = ok[f"coef_{var}"].abs()
    top = ok.sort_values("forca", ascending=False).head(3)
    st.markdown("#### As que mais respondem")
    if top.empty:
        st.info("Nenhuma família responde de forma clara a este indicador.")
    else:
        rotulo = dict(zip(rot["cluster"].astype(int), rot["rotulo_curto"], strict=True))
        cols = st.columns(len(top))
        for col, (cid, r) in zip(cols, top.iterrows(), strict=True):
            sentido = "mesmo sentido" if r[f"coef_{var}"] > 0 else "sentido oposto"
            with col:
                style.html(
                    f"""
                    <div class="card rise">
                      <div class="kicker-s">Família {int(cid)}</div>
                      <h4>{style.esc(rotulo[int(cid)])}</h4>
                      <p>Acompanha no <b>{sentido}</b>.</p>
                      <div class="bar"><i style="width:{min(r["forca"] / 0.9, 1) * 100:.0f}%"></i></div>
                    </div>
                    """
                )
                if st.button("Explorar esta família", key=f"go_{var}_{cid}"):
                    ui.definir_foco(int(cid))
                    if "explorar" in ui.PAGINAS:
                        st.switch_page(ui.PAGINAS["explorar"])

    with st.expander("Ver todas as famílias e todos os indicadores de uma vez"):
        ui.plot(charts_story.mapa_geral(reg, REG_VARS_PRINCIPAL, ALPHA, rot), key="geral_vars")
    st.caption(
        "Análise de 1973 a 2026, com as seis variáveis. As cores só aparecem quando a relação é "
        "estatisticamente convincente."
    )
