"""Testes dos dados: catálogo completo e câmbio reconstruído idêntico ao do notebook."""

import pandas as pd
import pytest

from tcc2_dashboard import analysis, catalogo, data
from tcc2_dashboard.config import DATA_DIR


def test_toda_serie_tem_descricao_e_categoria():
    for s in data.padronizado().columns:
        assert catalogo.nome(s) != s, f"sem descrição: {s}"
        assert catalogo.categoria(s) in catalogo.CATEGORIAS, s


def test_toda_referencia_tem_texto_leigo():
    for v in ("INDPRO", "CPIAUCSL", "FEDFUNDS", "T10YFFM", "S&P 500", "TWEXAFEGSMTHx"):
        assert {"nome", "o_que", "por_que", "sobe"} <= set(catalogo.REFERENCIAS[v])


def test_cambio_reconstruido_reproduz_regressao_principal():
    reg = data.regressores().loc["1973-02-01":].dropna()
    assert len(reg) == 638
    cen = data.centroides()[18].loc[reg.index]
    r = analysis.regressao_hac(cen, reg)
    saved = pd.read_csv(DATA_DIR / "regressao_resultados.csv").set_index("cluster").loc[18]
    assert r.r2 == pytest.approx(saved["r_squared"], abs=1e-6)
    assert r.tabela.loc["TWEXAFEGSMTHx", "coef"] == pytest.approx(
        saved["coef_TWEXAFEGSMTHx"], abs=1e-6
    )


def test_achados_tem_frase_de_leitura():
    assert set(catalogo.ACHADOS) == {3, 4, 14, 18}
