"""Página 7 — robustez: bootstrap em blocos, Ward vs K-Means e what-if de k."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans

from tcc2_dashboard import analysis, charts, data, ui
from tcc2_dashboard.config import BLOCK_SIZE, CLUSTERS_ACHADO, KMEANS_SEED, K


@st.cache_data(show_spinner=False)
def _ward() -> np.ndarray:
    return analysis.ward(data.padronizado())


@st.cache_data(show_spinner=False)
def _labels_originais() -> np.ndarray:
    cl = data.clusters().set_index("serie").loc[data.padronizado().columns, "cluster"]
    return cl.to_numpy()


@st.cache_data(show_spinner=False)
def _varredura(k_min: int, k_max: int) -> pd.DataFrame:
    return analysis.varredura_k(data.padronizado(), range(k_min, k_max + 1))


def render() -> None:
    ui.cabecalho(
        "Estabilidade e robustez",
        "Os quatro achados se repetem quando refazemos a análise com meses embaralhados ou com "
        "outro método de agrupamento?",
        kicker="Detalhes técnicos",
    )
    aba1, aba2, aba3 = st.tabs(["Bootstrap em blocos", "Ward × K-Means", "E se k fosse outro?"])
    with aba1:
        _bootstrap()
    with aba2:
        _ward_vs_kmeans()
    with aba3:
        _what_if_k()


def _bootstrap() -> None:
    boot = data.bootstrap_jaccard()
    st.markdown(
        "Pergunta: **se os dados fossem um pouco diferentes, as mesmas famílias apareceriam?** "
        f"Para testar, embaralhamos o calendário em blocos de {BLOCK_SIZE} meses (para manter a "
        "persistência dos dados), refizemos o agrupamento 500 vezes e medimos, a cada vez, o "
        "quanto cada família original reaparece (índice de Jaccard)."
    )
    ui.guia("boot", aberto=True)
    ao_vivo = st.session_state.get("boot_vivo")
    extra = None
    if ao_vivo is not None:
        extra = pd.DataFrame(
            {"cluster": list(ao_vivo), "jaccard_medio": [np.mean(v) for v in ao_vivo.values()]}
        )
    ui.plot(charts.bootstrap(boot, extra), width="stretch")
    st.dataframe(boot, hide_index=True, width="stretch")

    st.markdown("##### Rodar o bootstrap ao vivo")
    st.caption(
        "Versão rápida (n_init = 3 por reamostra, seed própria): serve para sentir a variabilidade; "
        "o resultado oficial é o do notebook (B = 500, n_init = 20)."
    )
    c1, c2, c3 = st.columns([2, 2, 1])
    alvo = c1.multiselect("Clusters", CLUSTERS_ACHADO, default=CLUSTERS_ACHADO, key="boot_alvo")
    b = c2.slider("Reamostragens (B)", 10, 200, 40, 10)
    bloco = c3.number_input("Bloco (meses)", 3, 36, BLOCK_SIZE)
    if st.button("Executar", type="primary", icon=":material/play_arrow:") and alvo:
        df = data.padronizado()
        x = df.T.to_numpy()
        nomes = df.columns.tolist()
        cl = data.clusters()
        membros = {c: set(cl.loc[cl["cluster"] == c, "serie"]) for c in alvo}
        rng = np.random.default_rng(KMEANS_SEED)
        res: dict[int, list[float]] = {c: [] for c in alvo}
        barra = st.progress(0.0, text="Reamostrando…")
        for i in range(b):
            xb = analysis.bloco_bootstrap(x, int(bloco), rng)
            lab = KMeans(n_clusters=K, n_init=3, max_iter=300, random_state=i).fit(xb).labels_
            for c in alvo:
                res[c].append(analysis.jaccard_melhor(membros[c], lab, nomes))
            barra.progress((i + 1) / b, text=f"Reamostragem {i + 1}/{b}")
        barra.empty()
        st.session_state["boot_vivo"] = res
        st.session_state["boot_vivo_dist"] = res
        st.rerun()
    dist = st.session_state.get("boot_vivo_dist")
    if dist:
        ui.plot(charts.hist_jaccard(dist), width="stretch")
        resumo = pd.DataFrame(
            {
                c: {"Jaccard médio": np.mean(v), "desvio": np.std(v, ddof=1), "B": len(v)}
                for c, v in dist.items()
            }
        ).T
        st.dataframe(resumo.round(3), width="stretch")


def _ward_vs_kmeans() -> None:
    df = data.padronizado()
    cl_de = data.cluster_de()
    z = _ward()
    k = st.slider("Cortar o dendrograma em k grupos", 2, 40, K, key="k_ward")
    ui.plot(charts.dendrograma(z, df.columns.tolist(), cl_de, k), width="stretch")
    st.caption(
        "Cada folha é uma série, colorida pelo cluster do K-Means: folhas da mesma cor "
        "contíguas indicam que os dois métodos concordam."
    )

    lw = analysis.ward_cortar(z, k)
    ari, nmi = analysis.concordancia(_labels_originais(), lw)
    c = st.columns(2)
    c[0].metric("ARI (K-Means × Ward)", f"{ari:.3f}")
    c[1].metric("NMI (K-Means × Ward)", f"{nmi:.3f}")
    tab = pd.crosstab(pd.Series(_labels_originais(), name="kmeans"), pd.Series(lw, name="ward"))
    ui.plot(charts.contingencia(tab, "K-Means", "Ward"), width="stretch")

    st.markdown("##### Onde caem os clusters do K-Means no Ward (k = 19, notebook)")
    wc = data.ward_comparacao()
    so_achado = st.toggle("Só os 4 achados genuínos", value=True)
    for r in wc[wc["achado_genuino"]].itertuples():
        st.markdown(
            f"- **Família {r.cluster_kmeans}** ({r.n_series_kmeans} séries): no Ward, "
            f"{r.membros_kmeans_no_ward} delas ficam no mesmo grupo "
            + (
                "(todas juntas)"
                if r.todos_juntos_no_ward
                else f"e as demais se espalham por {r.n_grupos_ward_que_contem_membros} grupos"
            )
            + f". Semelhança entre os dois grupos (Jaccard): {r.jaccard_ward:.2f}."
        )
    st.dataframe(wc[wc["achado_genuino"]] if so_achado else wc, hide_index=True, width="stretch")
    ui.guia("ward", titulo="Como ler esta comparação")


def _what_if_k() -> None:
    st.markdown(
        "Pergunta: **e se tivéssemos escolhido outro número de famílias?** Refazemos o "
        "agrupamento com o k que você escolher e comparamos com o oficial (k = 19)."
    )
    df = data.padronizado()
    k = st.slider("k", 2, 40, K, key="k_wi")
    labels, inercia = analysis.kmeans_series(df, k)
    ori = _labels_originais()
    ari, nmi = analysis.concordancia(ori, labels)
    alinhado = analysis.alinhar_rotulos(ori, labels)
    m = st.columns(3)
    m[0].metric("ARI vs oficial", f"{ari:.3f}")
    m[1].metric("NMI vs oficial", f"{nmi:.3f}")
    m[2].metric("Inércia", f"{inercia:,.0f}".replace(",", "."))
    if k == K:
        st.success("k = 19 reproduz exatamente a partição do notebook (ARI = 1).")

    ui.plot(charts.varredura_k(_varredura(5, 30), k), width="stretch")
    ui.guia("what_if", aberto=True)

    foco = ui.foco()
    membros = np.where(ori == foco)[0]
    novos = pd.Series(alinhado[membros]).value_counts()
    nomes = df.columns[membros]
    st.markdown(
        f"**Cluster oficial {foco}** ({len(membros)} séries) distribuído nos grupos do novo k:"
    )
    st.dataframe(
        pd.DataFrame({"série": nomes, "novo grupo (alinhado)": alinhado[membros]}),
        hide_index=True,
        width="stretch",
    )
    st.caption(f"{novos.iloc[0]} de {len(membros)} séries ficam juntas no grupo mais frequente.")
