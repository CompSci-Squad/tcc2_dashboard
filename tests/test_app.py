"""Smoke tests: cada página renderiza sem exceção (streamlit.testing)."""

import pytest
from streamlit.testing.v1 import AppTest

PAGINAS = [
    "visao_geral",
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


@pytest.mark.parametrize("pagina", PAGINAS)
def test_pagina_renderiza(pagina):
    at = AppTest.from_function(_roda, args=(pagina,), default_timeout=60).run()
    assert not at.exception, [e.value for e in at.exception]


def test_foco_compartilhado_entre_paginas():
    at = AppTest.from_function(_roda, args=("visao_geral",), default_timeout=60).run()
    at.selectbox[0].select(14).run()
    assert at.session_state["cluster_foco"] == 14
    assert not at.exception


def test_rede_limiar_interativo():
    at = AppTest.from_function(_roda, args=("rede",), default_timeout=60).run()
    at.slider[0].set_value(0.8).run()
    assert not at.exception


def test_mapa_3d_e_cor_por_tcode():
    at = AppTest.from_function(_roda, args=("mapa",), default_timeout=60).run()
    at.radio[0].set_value("3D").run()
    assert not at.exception
    at.radio[1].set_value("tcode").run()
    assert not at.exception


def test_centroides_todos_em_paineis():
    at = AppTest.from_function(_roda, args=("centroides",), default_timeout=60).run()
    at.multiselect[0].set_value(list(range(19))).run()
    at.toggle[1].set_value(True).run()
    assert not at.exception


def test_regressao_robustez_e_ols_classico():
    at = AppTest.from_function(_roda, args=("regressao",), default_timeout=60).run()
    at.radio[0].set_value("robustez").run()
    assert not at.exception
    assert any("0,743" in i.value for i in at.info) is False  # aviso só aparece na principal
