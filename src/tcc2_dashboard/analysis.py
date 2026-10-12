"""Funções estatísticas puras (sem Streamlit), reaproveitando as escolhas do notebook.

Cada objeto agrupado é uma SÉRIE (linha de X), não um mês: X tem forma (séries × meses).
"""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson

from tcc2_dashboard.config import HAC_MAXLAGS, KMEANS_N_INIT, KMEANS_SEED

# --------------------------------------------------------------------------- PCA


@dataclass(frozen=True)
class PcaResultado:
    coords: pd.DataFrame  # séries × componentes
    variancia: np.ndarray  # razão de variância explicada por componente


def pca_series(df: pd.DataFrame, n_componentes: int = 3) -> PcaResultado:
    """PCA sobre as séries (cada série é um ponto no espaço dos meses)."""
    pca = PCA(n_components=n_componentes, random_state=KMEANS_SEED)
    z = pca.fit_transform(df.T.to_numpy())
    cols = [f"PC{i + 1}" for i in range(n_componentes)]
    return PcaResultado(
        pd.DataFrame(z, index=df.columns, columns=cols), pca.explained_variance_ratio_
    )


def variancia_acumulada(df: pd.DataFrame, n_max: int = 40) -> np.ndarray:
    """Variância explicada acumulada pelos componentes do PCA do notebook (meses × séries)."""
    pca = PCA(n_components=min(n_max, df.shape[1]), random_state=KMEANS_SEED)
    pca.fit(df.to_numpy())
    return np.cumsum(pca.explained_variance_ratio_)


# ------------------------------------------------------------------------ K-Means


def kmeans_series(
    df: pd.DataFrame,
    k: int,
    seed: int = KMEANS_SEED,
    n_init: int = KMEANS_N_INIT,
) -> tuple[np.ndarray, float]:
    km = KMeans(n_clusters=k, init="k-means++", n_init=n_init, max_iter=500, random_state=seed)
    km.fit(df.T.to_numpy())
    return km.labels_, float(km.inertia_)


def alinhar_rotulos(referencia: np.ndarray, novos: np.ndarray) -> np.ndarray:
    """Renomeia os rótulos de `novos` para maximizar a coincidência com `referencia` (húngaro)."""
    ref_ids = np.unique(referencia)
    novo_ids = np.unique(novos)
    m = np.zeros((len(novo_ids), len(ref_ids)))
    for i, n in enumerate(novo_ids):
        for j, r in enumerate(ref_ids):
            m[i, j] = np.sum((novos == n) & (referencia == r))
    linhas, colunas = linear_sum_assignment(-m)
    mapa = {novo_ids[i]: ref_ids[j] for i, j in zip(linhas, colunas, strict=True)}
    proximo = int(max(ref_ids.max(), novo_ids.max())) + 1
    for n in novo_ids:
        if n not in mapa:
            mapa[n] = proximo
            proximo += 1
    return np.array([mapa[n] for n in novos])


def varredura_k(df: pd.DataFrame, ks: range, n_init: int = 5) -> pd.DataFrame:
    """Inércia e silhueta para vários k (n_init reduzido para ficar interativo)."""
    x = df.T.to_numpy()
    linhas = []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=n_init, random_state=KMEANS_SEED).fit(x)
        linhas.append({"k": k, "inercia": km.inertia_, "silhueta": silhouette_score(x, km.labels_)})
    return pd.DataFrame(linhas)


def concordancia(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """(ARI, NMI) entre duas partições; independem dos ids dos rótulos."""
    return float(adjusted_rand_score(a, b)), float(normalized_mutual_info_score(a, b))


# -------------------------------------------------------------------------- Ward


def ward(df: pd.DataFrame) -> np.ndarray:
    return linkage(df.T.to_numpy(), method="ward", metric="euclidean")


def ward_cortar(z: np.ndarray, k: int) -> np.ndarray:
    return fcluster(z, t=k, criterion="maxclust") - 1


# -------------------------------------------------------------------- Bootstrap


def bloco_bootstrap(x: np.ndarray, bloco: int, rng: np.random.Generator) -> np.ndarray:
    """Reamostra o tempo em blocos contíguos (mesmos blocos para todas as séries)."""
    n_tempo = x.shape[1]
    n_blocos = int(np.ceil(n_tempo / bloco))
    inicios = rng.integers(0, n_tempo - bloco + 1, size=n_blocos)
    return np.concatenate([x[:, i : i + bloco] for i in inicios], axis=1)[:, :n_tempo]


def jaccard_melhor(membros: set[str], labels: np.ndarray, nomes: list[str]) -> float:
    melhor = 0.0
    for cid in np.unique(labels):
        outro = {nomes[i] for i in np.where(labels == cid)[0]}
        uniao = membros | outro
        if uniao:
            melhor = max(melhor, len(membros & outro) / len(uniao))
    return melhor


# ------------------------------------------------------------------------- Rede


def arestas_correlacao(corr: pd.DataFrame, limiar: float) -> pd.DataFrame:
    """Pares (a, b) com |r| > limiar."""
    nomes = corr.columns.to_numpy()
    iu = np.triu_indices(len(nomes), k=1)
    r = corr.to_numpy()[iu]
    mask = np.abs(r) > limiar
    return pd.DataFrame({"a": nomes[iu[0]][mask], "b": nomes[iu[1]][mask], "r": r[mask]})


def posicoes_rede(
    nos: list[str], cluster_de: dict[str, int], arestas: pd.DataFrame, layout: str
) -> dict[str, tuple[float, float]]:
    if layout == "Circular (por cluster)":
        ordenados = sorted(nos, key=lambda s: (cluster_de[s], s))
        ang = np.linspace(0, 2 * np.pi, len(ordenados), endpoint=False)
        return {
            s: (float(np.cos(a)), float(np.sin(a))) for s, a in zip(ordenados, ang, strict=True)
        }
    g = nx.Graph()
    g.add_nodes_from(nos)
    g.add_weighted_edges_from(
        (a, b, abs(r)) for a, b, r in arestas[["a", "b", "r"]].itertuples(index=False)
    )
    if layout == "Força (spring)":
        pos = nx.spring_layout(g, weight="weight", seed=42, k=0.6 / np.sqrt(max(len(nos), 1)))
    else:  # agrupado por cluster: centros em círculo, membros em torno
        k = max(set(cluster_de.values())) + 1
        pos = {}
        for cid in range(k):
            membros = [s for s in nos if cluster_de[s] == cid]
            cx, cy = 1.0 * np.cos(2 * np.pi * cid / k), 1.0 * np.sin(2 * np.pi * cid / k)
            for i, s in enumerate(membros):
                a = 2 * np.pi * i / max(len(membros), 1)
                raio = 0.0 if len(membros) == 1 else 0.12 + 0.02 * len(membros)
                pos[s] = (cx + raio * np.cos(a), cy + raio * np.sin(a))
    return {s: (float(p[0]), float(p[1])) for s, p in pos.items()}


def resumo_rede(arestas: pd.DataFrame, cluster_de: dict[str, int], n_nos: int) -> dict[str, float]:
    """Mesmas estatísticas da função resumo_rede do notebook."""
    tamanhos = pd.Series(cluster_de).value_counts()
    pares_dentro = int((tamanhos * (tamanhos - 1) // 2).sum())
    pares_total = n_nos * (n_nos - 1) // 2
    n = len(arestas)
    if n:
        dentro = int((arestas["a"].map(cluster_de) == arestas["b"].map(cluster_de)).sum())
        pos = int((arestas["r"] > 0).sum())
    else:
        dentro = pos = 0
    nos_com_aresta = set(arestas["a"]) | set(arestas["b"]) if n else set()
    return {
        "n_arestas": n,
        "pct_positivas": 100 * pos / n if n else float("nan"),
        "pct_dentro": 100 * dentro / n if n else float("nan"),
        "densidade_dentro": dentro / pares_dentro if pares_dentro else float("nan"),
        "densidade_entre": (n - dentro) / (pares_total - pares_dentro),
        "isolados": n_nos - len(nos_com_aresta),
    }


# ---------------------------------------------------------------------- Regressão


@dataclass(frozen=True)
class RegressaoResultado:
    tabela: pd.DataFrame  # coef, erro-padrão, p, IC95 por termo
    r2: float
    f_p: float
    dw: float
    bg_p: float
    n_obs: int
    residuos: pd.Series


def regressao_hac(
    y: pd.Series, x: pd.DataFrame, maxlags: int = HAC_MAXLAGS, hac: bool = True
) -> RegressaoResultado:
    """OLS do centroide contra as variáveis de referência, com erro-padrão HAC (Newey-West)."""
    modelo = sm.OLS(y, sm.add_constant(x))
    res = modelo.fit(cov_type="HAC", cov_kwds={"maxlags": maxlags}) if hac else modelo.fit()
    ic = res.conf_int()
    tabela = pd.DataFrame(
        {
            "coef": res.params,
            "erro_padrao": res.bse,
            "p_valor": res.pvalues,
            "ic_inf": ic[0],
            "ic_sup": ic[1],
        }
    )
    bg_p = acorr_breusch_godfrey(res, nlags=maxlags, result_object=True).lmpval
    return RegressaoResultado(
        tabela=tabela,
        r2=float(res.rsquared),
        f_p=float(res.f_pvalue),
        dw=float(durbin_watson(res.resid)),
        bg_p=float(bg_p),
        n_obs=int(res.nobs),
        residuos=res.resid,
    )
