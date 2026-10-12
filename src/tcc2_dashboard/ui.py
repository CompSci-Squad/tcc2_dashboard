"""Helpers de interface: estado compartilhado entre páginas e componentes reutilizáveis."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tcc2_dashboard import data
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


def clique_em_cluster(evento, chave_ultimo: str) -> None:
    """Aplica um clique do Plotly (on_select) ao foco, ignorando eventos já processados."""
    pontos = evento.get("selection", {}).get("points", []) if evento else []
    if not pontos:
        st.session_state.pop(chave_ultimo, None)
        return
    p = pontos[0]
    bruto = p.get("x")
    try:
        cid = int(bruto)
    except (TypeError, ValueError):
        return
    assinatura = (cid, p.get("curve_number"), p.get("point_index"))
    if st.session_state.get(chave_ultimo) != assinatura:
        st.session_state[chave_ultimo] = assinatura
        definir_foco(cid)
        st.rerun()


def cabecalho(titulo: str, subtitulo: str) -> None:
    st.title(titulo)
    st.caption(subtitulo)


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
