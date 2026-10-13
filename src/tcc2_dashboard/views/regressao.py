"""Página 6 — regressão do centroide de cada cluster contra as variáveis de referência."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tcc2_dashboard import analysis, catalogo, charts, data, ui
from tcc2_dashboard.config import ALPHA, HAC_MAXLAGS, REG_VARS_PRINCIPAL


def render() -> None:
    ui.cabecalho(
        "Regressão (análise estatística)",
        "Versão detalhada do que a página Variáveis de referência mostra de forma visual: para cada "
        "família, quais indicadores a explicam e com que confiança.",
        kicker="Detalhes técnicos",
    )
    rot = data.rotulados()

    with st.sidebar:
        st.header("Regressão")
        espec = st.radio(
            "Especificação",
            ["principal", "robustez"],
            format_func={
                "principal": "Principal — 6 variáveis (1973-2026, com câmbio)",
                "robustez": "Robustez — 5 variáveis (1965-2026, sem câmbio)",
            }.get,
        )
        alpha = st.select_slider("Nível de significância", [0.001, 0.01, 0.05, 0.10], value=ALPHA)
        so_sig = st.toggle("Mostrar só coeficientes significativos", value=False)

    reg = data.regressao(espec)
    variaveis = data.reg_vars(espec)
    if espec == "principal":
        st.info(
            "**Análise principal**: 6 variáveis, janela 1973-2026 (638 obs). A de 5 variáveis "
            "(janela cheia) é checagem de **robustez**, não uma segunda análise de peso igual — "
            "perder 8 anos vale a pena porque sustenta o achado do cluster 18 (câmbio), cujo R² "
            "cai de 0,743 para 0,038 sem a variável.",
            icon=":material/info:",
        )

    aba1, aba2, aba3, aba4 = st.tabs(
        ["Mapa de coeficientes", "Detalhe do cluster", "Regressão ao vivo", "OLS clássico × HAC"]
    )

    with aba1:
        ui.plot(charts.heatmap_coeficientes(reg, variaveis, alpha, so_sig, rot), width="stretch")
        ui.guia("regressao_mapa", titulo="Como ler este mapa")
        v = data.vif()
        with st.expander("VIF das variáveis de referência (multicolinearidade)"):
            st.dataframe(v, hide_index=True, width="stretch")
            st.caption("Todos os VIF ≈ 1: as seis variáveis são praticamente ortogonais.")

    with aba2:
        foco = ui.seletor_foco(key="reg")
        linha = reg.loc[reg["cluster"] == foco].iloc[0]
        m = st.columns(5)
        m[0].metric(
            "R²",
            f"{linha['r_squared']:.3f}",
            help="Parte do vai e vem da família explicada (0 a 1).",
        )
        m[1].metric("Observações", int(linha["n_obs"]), help="Meses usados na regressão.")
        m[2].metric(
            "Durbin-Watson",
            f"{linha['durbin_watson']:.2f}",
            help="Perto de 2: os erros do modelo não têm memória. Bem abaixo de 2: um erro tende a "
            "repetir no mês seguinte (autocorrelação).",
        )
        m[3].metric(
            "Breusch-Godfrey p",
            f"{linha['bg_pvalue']:.1e}",
            help="p pequeno = há autocorrelação nos erros. Por isso usamos erro-padrão robusto (HAC).",
        )
        m[4].metric(
            "Teste F (p)",
            f"{linha['f_pvalue']:.1e}",
            help="p pequeno = os seis indicadores, juntos, explicam algo além do acaso.",
        )
        tab = pd.DataFrame(
            {
                "coef": [linha[f"coef_{v}"] for v in variaveis],
                "p_valor": [linha[f"pvalue_{v}"] for v in variaveis],
            },
            index=variaveis,
        )
        tab["significância"] = tab["p_valor"].map(ui.star)
        st.dataframe(tab, width="stretch")
        st.caption(
            "Breusch-Godfrey rejeita H₀ (resíduos sem autocorrelação) nos 19 clusters — por isso o "
            "erro-padrão é HAC e não o do OLS clássico."
        )

    with aba3:
        _regressao_ao_vivo()

    with aba4:
        comp = data.comparacao_ols_hac()
        n_mudou = int(comp["mudou_significancia"].sum())
        st.metric(
            "Pares (cluster, variável) que mudaram de significância", f"{n_mudou} de {len(comp)}"
        )
        so_mudou = st.toggle("Mostrar só os que mudaram", value=True)
        mostra = comp[comp["mudou_significancia"]] if so_mudou else comp
        st.dataframe(mostra, hide_index=True, width="stretch")
        ui.csv_download(comp, "ols_vs_hac.csv", key="dl_olshac")
        st.caption(
            "O OLS clássico subestima o erro-padrão sob autocorrelação; HAC corrige. Mudar de "
            "significância é o resultado esperado, não um erro."
        )


def _regressao_ao_vivo() -> None:
    st.markdown(
        "Refaça a regressão escolhendo os indicadores e o período. Com os 6 indicadores e o período "
        "a partir de 02/1973, o resultado bate com a análise principal; com os 5 primeiros e o "
        "período inteiro, bate com a checagem de robustez."
    )
    reg_x = data.regressores()
    cen = data.centroides()
    c1, c2 = st.columns([1, 2])
    with c1:
        foco = ui.seletor_foco(key="reg_vivo")
        vars_ = st.multiselect(
            "Indicadores",
            REG_VARS_PRINCIPAL,
            default=REG_VARS_PRINCIPAL,
            format_func=lambda v: catalogo.REFERENCIAS[v]["nome"],
        )
        lags = st.slider("Defasagens HAC (maxlags)", 1, 24, HAC_MAXLAGS)
        hac = st.toggle("Erro-padrão HAC", value=True, help="Desligue para ver o OLS clássico.")
    with c2:
        idx = reg_x.index
        janela = st.slider(
            "Janela da amostra",
            idx[0].to_pydatetime(),
            idx[-1].to_pydatetime(),
            (idx[0].to_pydatetime(), idx[-1].to_pydatetime()),
            format="MM/YYYY",
            key="jan_reg",
        )
    if not vars_:
        st.warning("Selecione ao menos um regressor.")
        return
    i0, i1 = pd.Timestamp(janela[0]), pd.Timestamp(janela[1])
    x = reg_x.loc[i0:i1, vars_].dropna()
    y = cen.loc[x.index, foco]
    if len(x) < len(vars_) + 20:
        st.warning("Janela curta demais para estimar.")
        return
    r = analysis.regressao_hac(y, x, lags, hac)
    m = st.columns(4)
    m[0].metric("R²", f"{r.r2:.3f}")
    m[1].metric("Observações", r.n_obs)
    m[2].metric("Durbin-Watson", f"{r.dw:.2f}")
    m[3].metric("Breusch-Godfrey p", f"{r.bg_p:.1e}")
    ui.plot(charts.coeficientes_cluster(r.tabela, ALPHA), width="stretch")
    ui.plot(charts.residuos(r.residuos), width="stretch")
    ui.guia("regressao_vivo", titulo="Como ler esta regressão")
    st.dataframe(r.tabela, width="stretch")
