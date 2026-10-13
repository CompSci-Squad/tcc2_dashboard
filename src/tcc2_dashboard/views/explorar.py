"""Página 3 — explorar as famílias: escolha uma e veja suas séries e seu perfil no tempo."""

from __future__ import annotations

import streamlit as st

from tcc2_dashboard import charts, charts_story, data, style, textos, ui
from tcc2_dashboard.config import K


def render() -> None:
    ui.cabecalho(
        "Explorar as famílias",
        "Escolha uma das 19 famílias para ver quais séries a formam e como ela se comportou "
        "de 1965 até hoje.",
        kicker="Explore",
    )

    # filtro no topo: lista + botões anterior/próxima
    a, b, c = st.columns([1, 6, 1], vertical_alignment="bottom")
    foco = ui.foco()
    if a.button("←", help="Família anterior", width="stretch"):
        ui.definir_foco((foco - 1) % K)
        st.rerun()
    if c.button("→", help="Próxima família", width="stretch"):
        ui.definir_foco((foco + 1) % K)
        st.rerun()
    with b:
        foco = ui.seletor_foco(label="Escolha uma família", key="expl")

    info = textos.info_familia(foco)
    cor = "ok" if info["r2"] >= 0.4 else ""
    style.html(
        f"""
        <div class="card rise">
          <div class="kicker-s">Família {foco} · {style.esc(info["classe"])}</div>
          <h3>{style.esc(info["rotulo"])}</h3>
          <p>{style.esc(textos.resumo_composicao(info))}</p>
          <p style="color:var(--ink)">{style.esc(info["leitura"])}</p>
          <div>{style.pill("Relação " + textos.forca(info["r2"]), cor)}</div>
        </div>
        """
    )
    st.write("")

    cen = data.centroides()
    rot = data.rotulo_curto()
    c1, c2, c3 = st.columns([3, 1, 1])
    modo = c1.segmented_control(
        "Como mostrar",
        ["Gráfico", "Animação ao longo do tempo"],
        default="Gráfico",
        label_visibility="collapsed",
    )
    recess = c2.toggle(
        "Mostrar recessões", value=True, help="Faixas cinza = recessões dos EUA (NBER)."
    )
    zoom = c3.toggle(
        "Ampliar",
        value=True,
        help="Ignora picos extremos (como o da pandemia, em 2020) para enxergar o resto da história.",
    )
    outras = st.multiselect(
        "Comparar com outras famílias",
        [k for k in range(K) if k != foco],
        format_func=data.nome_cluster,
        max_selections=3,
        placeholder="Opcional: escolha até 3",
    )
    cids = [foco, *outras]
    st.markdown("#### Perfil médio da família ao longo do tempo")
    st.caption(
        "Mostra a variação mensal média das séries da família, em desvios-padrão. "
        "Picos e vales coincidem com crises e recuperações."
    )
    if modo == "Animação ao longo do tempo":
        ui.plot(charts_story.centroide_animado(cen, cids, rot, recess), key=f"anim_{foco}")
    else:
        janela = (cen.index[0], cen.index[-1])
        ui.plot(
            charts.centroides(cen, cids, rot, janela, 1, recess, False, zoom), key=f"cen_{foco}"
        )

    st.markdown("#### As séries desta família")
    m = info["membros"]
    tipica = m.iloc[0]
    st.caption(
        f"Série mais típica: **{tipica['serie']}** — {tipica['descricao']}. "
        "“Quão típica” mostra o quanto cada série acompanha o perfil médio."
    )
    tab = m[["serie", "descricao", "categoria", "corr_centroide"]].rename(
        columns={
            "serie": "Código",
            "descricao": "O que mede",
            "categoria": "Tema",
            "corr_centroide": "Quão típica",
        }
    )
    st.dataframe(
        tab,
        hide_index=True,
        width="stretch",
        column_config={
            "Quão típica": st.column_config.ProgressColumn(
                "Quão típica", min_value=0, max_value=1, format="%.2f"
            )
        },
    )
    with st.expander("Ver cada série da família no tempo"):
        esc = st.multiselect(
            "Séries",
            m["serie"].tolist(),
            default=m["serie"].tolist()[:6],
            format_func=lambda s: f"{s} · {m.set_index('serie').loc[s, 'descricao']}",
        )
        if esc:
            ui.plot(
                charts.membros(
                    data.padronizado(), esc, cen[foco], foco, (cen.index[0], cen.index[-1]), recess
                ),
                key=f"mem_{foco}",
            )
