"""Página 4 — variáveis de referência: qual família responde a cada uma, e com que força."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import catalogo, charts_story, data, style, ui
from tcc2_dashboard.config import ALPHA, REG_VARS_PRINCIPAL

ESCOLHAS = {v: catalogo.REFERENCIAS[v]["nome"] for v in REG_VARS_PRINCIPAL}


def _nivel(forca: float) -> str:
    return "forte" if forca >= 0.5 else "moderada" if forca >= 0.2 else "fraca"


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
    n_resp = int((reg[f"pvalue_{var}"] < ALPHA).sum())
    st.markdown("#### Quem responde a este indicador?")
    st.markdown(
        f"**{n_resp} de {len(reg)} famílias** respondem de forma clara a "
        f"**{ref['nome'].lower()}**. As demais ficam em cinza."
    )
    style.html(
        '<span class="pill" style="color:#4F46E5">■ anda no mesmo sentido</span> '
        '<span class="pill" style="color:#D97706">■ anda no sentido oposto</span> '
        '<span class="pill">■ sem resposta clara (a relação não passou no teste estatístico)</span>'
    )
    ui.plot(
        charts_story.mapa_variavel(reg, REG_VARS_PRINCIPAL, var, ALPHA, rot),
        key=f"tiles_{var}",
    )
    ui.guia("variaveis_mapa", aberto=True, titulo="Como ler este mapa")

    # ranking em linguagem simples
    d = reg.set_index("cluster")
    ok = d[d[f"pvalue_{var}"] < ALPHA].copy()
    ok["forca"] = ok[f"coef_{var}"].abs()
    top = ok.sort_values("forca", ascending=False).head(3)
    st.markdown("#### As que mais respondem")
    st.caption(
        "A barra mostra a força da resposta (de 0 a 0,9). Resposta “forte” é acima de 0,5; "
        "“moderada”, entre 0,2 e 0,5; “fraca”, abaixo de 0,2. O selo abaixo de cada família diz se "
        "a relação é um achado ou apenas uma conferência do método (relação óbvia)."
    )
    if top.empty:
        st.info("Nenhuma família responde de forma clara a este indicador.")
    else:
        rotulo = dict(zip(rot["cluster"].astype(int), rot["rotulo_curto"], strict=True))
        classe = dict(zip(rot["cluster"].astype(int), rot["classe"], strict=True))
        cols = st.columns(len(top))
        for col, (cid, r) in zip(cols, top.iterrows(), strict=True):
            sentido = "mesmo sentido" if r[f"coef_{var}"] > 0 else "sentido oposto"
            with col:
                style.html(
                    f"""
                    <div class="card rise">
                      <div class="kicker-s">Família {int(cid)}</div>
                      <h4>{style.esc(rotulo[int(cid)])}</h4>
                      <p>Acompanha no <b>{sentido}</b>. Resposta <b>{_nivel(r["forca"])}</b>
                      ({r["forca"]:.2f}).</p>
                      <div class="bar"><i style="width:{min(r["forca"] / 0.9, 1) * 100:.0f}%"></i></div>
                      <p style="margin-top:.6rem">{style.pill(classe[int(cid)], "ok" if classe[int(cid)] == "Achado genuíno" else "")}</p>
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
