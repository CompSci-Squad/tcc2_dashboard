"""Testes das funções estatísticas: reproduzem os números salvos pelo notebook."""

import numpy as np
import pandas as pd
import pytest

from tcc2_dashboard import analysis
from tcc2_dashboard.config import DATA_DIR, K


@pytest.fixture(scope="module")
def df() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "fred_md_standardized.csv", index_col=0, parse_dates=True)


@pytest.fixture(scope="module")
def originais(df: pd.DataFrame) -> np.ndarray:
    c = pd.read_csv(DATA_DIR / "clusters.csv").set_index("serie")
    return c.loc[df.columns, "cluster"].to_numpy()


def test_kmeans_reproduz_particao_do_notebook(df, originais):
    labels, _ = analysis.kmeans_series(df, K)
    ari, nmi = analysis.concordancia(originais, labels)
    assert ari == pytest.approx(1.0)
    assert nmi == pytest.approx(1.0)


def test_criterio_70_por_cento_da_k_19(df):
    cum = analysis.variancia_acumulada(df)
    assert int(np.argmax(cum >= 0.70)) + 1 == K


def test_regressao_robustez_bate_com_tabela(df, originais):
    reg = pd.read_csv(DATA_DIR / "regressao.csv", index_col=0, parse_dates=True)
    saved = pd.read_csv(DATA_DIR / "regressao_resultados_5series.csv").set_index("cluster")
    for cid in (1, 3, 18):
        y = df.loc[:, originais == cid].mean(axis=1)
        r = analysis.regressao_hac(y, reg)
        assert r.r2 == pytest.approx(saved.loc[cid, "r_squared"], abs=1e-4)
        assert r.dw == pytest.approx(saved.loc[cid, "durbin_watson"], abs=1e-3)
        assert r.tabela.loc["INDPRO", "p_valor"] == pytest.approx(
            saved.loc[cid, "pvalue_INDPRO"], rel=1e-2, abs=1e-6
        )


def test_alinhar_rotulos_recupera_permutacao(originais):
    permutado = (originais + 7) % K
    assert np.array_equal(analysis.alinhar_rotulos(originais, permutado), originais)


def test_bloco_bootstrap_preserva_forma_e_blocos(df):
    x = df.T.to_numpy()
    xb = analysis.bloco_bootstrap(x, 12, np.random.default_rng(0))
    assert xb.shape == x.shape
    # primeiro bloco é um trecho contíguo do original
    assert any(np.allclose(xb[:, :12], x[:, i : i + 12]) for i in range(x.shape[1] - 11))


def test_rede_limiar_monotono(df):
    corr = df.corr()
    n_baixo = len(analysis.arestas_correlacao(corr, 0.4))
    n_alto = len(analysis.arestas_correlacao(corr, 0.7))
    assert n_baixo > n_alto > 0


def test_jaccard_identico_vale_um(df, originais):
    nomes = df.columns.tolist()
    membros = {nomes[i] for i in np.where(originais == 3)[0]}
    assert analysis.jaccard_melhor(membros, originais, nomes) == pytest.approx(1.0)
