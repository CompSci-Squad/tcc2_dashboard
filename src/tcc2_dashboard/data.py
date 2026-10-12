"""Carregamento (cacheado) das tabelas geradas pelo notebook do TCC2."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from tcc2_dashboard.config import (
    CLASSIFICACAO_ROTULO,
    CLUSTERS_ACHADO,
    DATA_DIR,
    R2_FORTE,
    REG_VARS_PRINCIPAL,
    REG_VARS_ROBUSTEZ,
)


def _csv(nome: str, **kw) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / nome, **kw)


@st.cache_data(show_spinner=False)
def padronizado() -> pd.DataFrame:
    """735 meses × 118 séries padronizadas (entrada do K-Means, após transformação e EM-PCA)."""
    df = _csv("fred_md_standardized.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    df.index.name = "data"
    return df


@st.cache_data(show_spinner=False)
def clusters() -> pd.DataFrame:
    """Série → cluster (K-Means, k=19)."""
    return _csv("clusters.csv")


@st.cache_data(show_spinner=False)
def cluster_de() -> dict[str, int]:
    c = clusters()
    return dict(zip(c["serie"], c["cluster"].astype(int), strict=True))


@st.cache_data(show_spinner=False)
def rotulados() -> pd.DataFrame:
    """Uma linha por cluster: R², DW, variável dominante, classificação e rótulo (Etapa 6)."""
    df = _csv("clusters_rotulados.csv")
    df["rotulo_curto"] = df["rotulo_proposto"].str.split(" \\(").str[0]
    df["classificacao_familia"] = df["classificacao_familia"].fillna("sem_classificacao")
    df["classe"] = df["classificacao_familia"].map(CLASSIFICACAO_ROTULO)
    df["forte"] = df["r_squared"] > R2_FORTE
    df["achado"] = df["cluster"].isin(CLUSTERS_ACHADO)
    return df


@st.cache_data(show_spinner=False)
def rotulo_curto() -> dict[int, str]:
    r = rotulados()
    return dict(zip(r["cluster"].astype(int), r["rotulo_curto"], strict=True))


def nome_cluster(cid: int) -> str:
    return f"{cid} — {rotulo_curto()[int(cid)]}"


@st.cache_data(show_spinner=False)
def centroides() -> pd.DataFrame:
    """Centroide de cada cluster no tempo (média das séries-membro = centro do K-Means)."""
    df = padronizado()
    c = clusters()
    cen = {int(cid): df[g["serie"].tolist()].mean(axis=1) for cid, g in c.groupby("cluster")}
    return pd.DataFrame(cen)


@st.cache_data(show_spinner=False)
def descritiva() -> pd.DataFrame:
    return _csv("descritiva_clusters.csv")


@st.cache_data(show_spinner=False)
def regressao(especificacao: str = "principal") -> pd.DataFrame:
    """Resultados da regressão por cluster (HAC). 'principal' = 6 variáveis, 'robustez' = 5."""
    nome = (
        "regressao_resultados.csv"
        if especificacao == "principal"
        else ("regressao_resultados_5series.csv")
    )
    return _csv(nome)


@st.cache_data(show_spinner=False)
def regressores() -> pd.DataFrame:
    """As 5 variáveis de referência disponíveis para a janela cheia (1965-2026)."""
    df = _csv("regressao.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    df.index.name = "data"
    return df


@st.cache_data(show_spinner=False)
def comparacao_ols_hac() -> pd.DataFrame:
    return _csv("regressao_comparacao_ols_hac.csv")


@st.cache_data(show_spinner=False)
def vif() -> pd.DataFrame:
    return _csv("vif_referencia.csv")


@st.cache_data(show_spinner=False)
def bootstrap_jaccard() -> pd.DataFrame:
    return _csv("bootstrap_jaccard_clusters.csv")


@st.cache_data(show_spinner=False)
def ward_comparacao() -> pd.DataFrame:
    return _csv("hierarquico_comparacao.csv")


@st.cache_data(show_spinner=False)
def contingencia() -> pd.DataFrame:
    return _csv("hierarquico_contingencia.csv", index_col=0)


@st.cache_data(show_spinner=False)
def series_meta() -> pd.DataFrame:
    """Metadados por série: cluster, tcode do FRED-MD e estatísticas básicas."""
    raw = pd.read_csv(DATA_DIR / "fred_md_raw.csv", nrows=1, index_col=0)
    tcodes = raw.iloc[0].astype(int)
    c = clusters().set_index("serie")
    df = padronizado()
    meta = pd.DataFrame({"cluster": c["cluster"].astype(int)})
    meta["tcode"] = tcodes.reindex(meta.index).astype("Int64")
    corr_cen = {
        s: float(np.corrcoef(df[s], centroides()[meta.loc[s, "cluster"]])[0, 1]) for s in meta.index
    }
    meta["corr_centroide"] = pd.Series(corr_cen)
    meta["rotulo"] = meta["cluster"].map(rotulo_curto())
    return meta.reset_index(names="serie")


@st.cache_data(show_spinner=False)
def correlacao_series() -> pd.DataFrame:
    return padronizado().corr()


def reg_vars(especificacao: str) -> list[str]:
    return REG_VARS_PRINCIPAL if especificacao == "principal" else REG_VARS_ROBUSTEZ
