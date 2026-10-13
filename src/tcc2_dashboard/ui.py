"""Helpers de interface: estado compartilhado entre páginas e componentes reutilizáveis."""

from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from tcc2_dashboard import data, explicacoes, style
from tcc2_dashboard.config import CLUSTERS_ACHADO, K

FOCO = "cluster_foco"


def foco() -> int:
    """Cluster em foco, compartilhado entre todas as páginas."""
    return int(st.session_state.setdefault(FOCO, CLUSTERS_ACHADO[0]))


def definir_foco(cid: int) -> None:
    st.session_state[FOCO] = int(cid)


def seletor_foco(container=None, label: str = "Cluster em foco", key: str = "w") -> int:
    """Selectbox que lê/escreve o cluster em foco (persiste ao trocar de página)."""
    c = container or st
    opcoes = list(range(K))
    wkey = f"{FOCO}_{key}"
    # sincroniza o widget com o estado global (outra página pode ter mudado o foco)
    st.session_state[wkey] = foco()

    def _on_change() -> None:
        st.session_state[FOCO] = st.session_state[wkey]

    return int(
        c.selectbox(label, opcoes, key=wkey, format_func=data.nome_cluster, on_change=_on_change)
    )


def cabecalho(
    titulo: str, subtitulo: str, kicker: str = "TCC2 · CICD06", chips: list[str] | None = None
) -> None:
    """Cabeçalho da página; com `chips` vira o banner (hero) de abertura."""
    if chips:
        tags = "".join(f'<span class="chip">{c}</span>' for c in chips)
        st.markdown(
            f'<div class="hero"><div class="kicker">{kicker}</div><h1>{titulo}</h1>'
            f'<p>{subtitulo}</p><div class="chips">{tags}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="pagehead"><div class="kicker">{kicker}</div><h1>{titulo}</h1>'
            f"<p>{subtitulo}</p></div>",
            unsafe_allow_html=True,
        )


def plot(fig, card: bool = True, **kw):
    """Plotly dentro de um cartão, com o template do dashboard (theme=None) e barra enxuta."""
    kw.setdefault("width", "stretch")
    kw.setdefault(
        "config",
        {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "autoScale2d"]},
    )
    if not card:
        return st.plotly_chart(fig, theme=None, **kw)
    with st.container(border=True):
        return st.plotly_chart(fig, theme=None, **kw)


def csv_download(
    df: pd.DataFrame, nome: str, label: str = "Baixar CSV", key: str | None = None
) -> None:
    st.download_button(
        label,
        df.to_csv(index=True).encode("utf-8"),
        file_name=nome,
        mime="text/csv",
        key=key or f"dl_{nome}",
        icon=":material/download:",
    )


def star(p: float) -> str:
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"


# ------------------------------------------------------------------ guias de leitura


def md(s: str) -> str:
    """Escapa o texto e converte **negrito** em <b>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", style.esc(s))


def guia(chave: str, aberto: bool = False, titulo: str = "Como ler este gráfico") -> None:
    """Bloco "o que você está vendo / como ler / cuidado" (textos em explicacoes.py)."""
    g = explicacoes.GUIAS[chave]
    itens = "".join(f"<li>{md(x)}</li>" for x in g["como_ler"])
    corpo = (
        f'<div class="guia"><div class="g"><span>O que você está vendo</span><p>{md(g["o_que"])}</p></div>'
        f'<div class="g c"><span>Como ler</span><ul>{itens}</ul></div>'
        f'<div class="g w"><span>Cuidado com a interpretação</span><p>{md(g["cuidado"])}</p></div></div>'
    )
    with st.expander(titulo, expanded=aberto, icon=":material/menu_book:"):
        style.html(corpo)


# ------------------------------------------------------------------ navegação / hero

PAGINAS: dict[str, st.Page] = {}  # preenchido em app.py (st.page_link precisa de um st.Page)


def link(chave: str, label: str, icon: str | None = None) -> None:
    """Botão de navegação para outra página (ignorado fora do app completo, ex.: testes)."""
    pagina = PAGINAS.get(chave)
    if pagina is not None:
        st.page_link(pagina, label=label, icon=icon, width="stretch")


def hero(titulo: str, texto: str, estatisticas: list[tuple[int, str, str]], kicker: str) -> None:
    """Cartão grande de abertura com números que contam até o valor final."""
    blocos = "".join(
        f'<div class="hero-stat"><div class="num" style="--n:{n}">'
        f"{f'<small>{suf}</small>' if suf else ''}</div>"
        f'<div class="lab">{style.esc(rot)}</div></div>'
        for n, suf, rot in estatisticas
    )
    style.html(
        f'<div class="hero"><div class="kicker">{style.esc(kicker)}</div><h1>{titulo}</h1>'
        f'<p>{texto}</p><div class="hero-stats">{blocos}</div></div>'
    )
