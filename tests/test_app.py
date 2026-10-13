"""Smoke tests: cada página renderiza sem exceção (streamlit.testing)."""

import pytest
from streamlit.testing.v1 import AppTest

PAGINAS = [
    "visao_geral",
    "achados",
    "explorar",
    "variaveis",
    "projeto",
    "mapa",
    "centroides",
    "series",
    "rede",
    "regressao",
    "estabilidade",
    "metodologia",
]


def _roda(modulo: str) -> None:
    # AppTest.from_function só serializa o corpo: o import precisa ficar aqui dentro
    import importlib  # noqa: PLC0415

    importlib.import_module(f"tcc2_dashboard.views.{modulo}").render()


def _app(pagina: str) -> AppTest:
    return AppTest.from_function(_roda, args=(pagina,), default_timeout=90).run()


@pytest.mark.parametrize("pagina", PAGINAS)
def test_pagina_renderiza(pagina):
    at = _app(pagina)
    assert not at.exception, [e.value for e in at.exception]


def test_explorar_troca_de_familia():
    at = _app("explorar")
    at.selectbox[0].select(14).run()
    assert at.session_state["cluster_foco"] == 14
    assert not at.exception


def test_explorar_modo_animacao_e_comparacao():
    at = _app("explorar")
    at.multiselect[0].set_value([3, 4]).run()
    assert not at.exception


def test_variaveis_troca_indicador():
    at = _app("variaveis")
    for v in ("CPIAUCSL", "TWEXAFEGSMTHx", "S&P 500"):
        at.segmented_control[0].set_value(v).run()
        assert not at.exception


def test_rede_limiar_interativo():
    at = _app("rede")
    at.slider[0].set_value(0.8).run()
    assert not at.exception


def test_mapa_3d_e_cor_por_categoria():
    at = _app("mapa")
    at.radio[0].set_value("3D").run()
    assert not at.exception
    at.radio[1].set_value("categoria").run()
    assert not at.exception


def test_comparar_todas_em_paineis():
    at = _app("centroides")
    at.multiselect[0].set_value(list(range(19))).run()
    at.toggle[1].set_value(True).run()
    assert not at.exception


def test_regressao_robustez():
    at = _app("regressao")
    at.radio[0].set_value("robustez").run()
    assert not at.exception
