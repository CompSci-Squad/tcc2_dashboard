"""Figuras Plotly do dashboard. Funções puras: recebem dados, devolvem go.Figure."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import dendrogram

from tcc2_dashboard.config import (
    CLASSIFICACAO_COR,
    RECESSOES_NBER,
    cor_cluster,
)

_LAYOUT = {"margin": {"l": 10, "r": 10, "t": 40, "b": 10}, "legend": {"title": None}}


def _base(fig: go.Figure, altura: int = 460, **kw) -> go.Figure:
    fig.update_layout(height=altura, **{**_LAYOUT, **kw})
    return fig


def _recessoes(fig: go.Figure, inicio: pd.Timestamp, fim: pd.Timestamp, **kw) -> None:
    for ini, fi in RECESSOES_NBER:
        a, b = pd.Timestamp(ini), pd.Timestamp(fi)
        if b < inicio or a > fim:
            continue
        fig.add_vrect(
            x0=max(a, inicio), x1=min(b, fim), fillcolor="grey", opacity=0.18, line_width=0, **kw
        )


# ------------------------------------------------------------------ visão geral


def tamanhos(rot: pd.DataFrame, selecionado: int | None = None) -> go.Figure:
    fig = go.Figure()
    for classe, g in rot.groupby("classe"):
        fig.add_bar(
            x=g["cluster"],
            y=g["n_series"],
            name=classe,
            marker_color=CLASSIFICACAO_COR[classe],
            marker_line_width=[3 if c == selecionado else 0 for c in g["cluster"]],
            marker_line_color="black",
            customdata=np.stack([g["rotulo_curto"], g["r_squared"]], axis=-1),
            hovertemplate="<b>Cluster %{x}</b> — %{customdata[0]}<br>"
            "%{y} séries<br>R² = %{customdata[1]:.3f}<extra></extra>",
        )
    fig.update_xaxes(title="Cluster", dtick=1)
    fig.update_yaxes(title="Nº de séries")
    fig.update_layout(clickmode="event+select")
    return _base(fig, 400, barmode="stack")


def r2_por_cluster(rot: pd.DataFrame, corte: float, selecionado: int | None = None) -> go.Figure:
    g = rot.sort_values("r_squared", ascending=False)
    fig = go.Figure(
        go.Bar(
            x=g["cluster"].astype(str),
            y=g["r_squared"],
            marker_color=[CLASSIFICACAO_COR[c] for c in g["classe"]],
            marker_line_width=[3 if c == selecionado else 0 for c in g["cluster"]],
            marker_line_color="black",
            text=g["variavel_dominante"],
            textposition="outside",
            customdata=g["rotulo_curto"],
            hovertemplate="<b>Cluster %{x}</b> — %{customdata}<br>R² = %{y:.3f}<br>"
            "dominante: %{text}<extra></extra>",
        )
    )
    fig.add_hline(y=corte, line_dash="dash", annotation_text=f"corte R² = {corte:.2f}")
    fig.update_xaxes(title="Cluster", type="category")
    fig.update_yaxes(title="R² (regressão principal, HAC)", range=[0, 1.08])
    return _base(fig, 400, showlegend=False)


def treemap(clusters: pd.DataFrame, rot: pd.DataFrame) -> go.Figure:
    d = clusters.merge(rot[["cluster", "rotulo_curto", "r_squared"]], on="cluster")
    d["cluster_nome"] = "Cluster " + d["cluster"].astype(str) + " — " + d["rotulo_curto"].str[:38]
    fig = px.treemap(
        d,
        path=["cluster_nome", "serie"],
        color="r_squared",
        color_continuous_scale="Blues",
        range_color=(0, 1),
        labels={"r_squared": "R²"},
    )
    fig.update_traces(root_color="rgba(0,0,0,0)")
    return _base(fig, 520, coloraxis_colorbar={"title": "R²"})


# ----------------------------------------------------------------------- mapa PCA


def pca_dispersao(
    coords: pd.DataFrame,
    meta: pd.DataFrame,
    eixos: list[str],
    cor_por: str,
    destacar: list[int],
    nome_cluster: dict[int, str],
    buscar: list[str],
) -> go.Figure:
    d = coords.join(meta.set_index("serie"))
    d["cluster_nome"] = d["cluster"].map(lambda c: f"{c} — {nome_cluster[c][:32]}")
    d["serie"] = d.index
    d["opaco"] = d["cluster"].isin(destacar) if destacar else True
    if buscar:
        d["opaco"] = d["opaco"] | d.index.isin(buscar)
    hover = {"serie": True, "cluster_nome": True, "tcode": True, "corr_centroide": ":.2f"}
    kwargs = {"x": eixos[0], "y": eixos[1], "hover_name": "serie", "hover_data": hover}
    if cor_por == "cluster":
        d["cor"] = d["cluster"].astype(str)
        kwargs |= {
            "color": "cor",
            "color_discrete_map": {str(c): cor_cluster(c) for c in d["cluster"].unique()},
            "category_orders": {"cor": [str(c) for c in sorted(d["cluster"].unique())]},
        }
    elif cor_por == "tcode":
        d["cor"] = d["tcode"].astype(str)
        kwargs |= {"color": "cor"}
    else:
        kwargs |= {"color": "corr_centroide", "color_continuous_scale": "RdYlBu_r"}
    if len(eixos) == 3:
        fig = px.scatter_3d(d, z=eixos[2], **kwargs)
        fig.update_traces(marker={"size": 4, "line": {"width": 0.5, "color": "black"}})
    else:
        fig = px.scatter(d, **kwargs)
        fig.update_traces(marker={"size": 11, "line": {"width": 0.6, "color": "black"}})
    por_serie = d.set_index("serie")["opaco"]
    for tr in fig.data:
        # esmaece o que não foi destacado (por traço, mantendo a legenda interativa)
        op = por_serie.loc[np.array(tr.hovertext)].to_numpy()
        if len(eixos) == 3:  # scatter3d não aceita opacidade por ponto: usa o tamanho
            tr.marker.opacity = 0.9
            tr.marker.size = np.where(op, 5, 2)
        else:
            tr.marker.opacity = np.where(op, 0.95, 0.15)
    if buscar and len(eixos) == 2:
        s = d.loc[d.index.isin(buscar)]
        fig.add_trace(
            go.Scatter(
                x=s[eixos[0]],
                y=s[eixos[1]],
                mode="text",
                text=s.index,
                textposition="top center",
                showlegend=False,
                hoverinfo="skip",
            )
        )
    return _base(fig, 620)


def scree(cum: np.ndarray, k: int, alvo: float = 0.70) -> go.Figure:
    x = np.arange(1, len(cum) + 1)
    fig = go.Figure()
    fig.add_scatter(x=x, y=cum, mode="lines+markers", name="Variância acumulada")
    fig.add_hline(y=alvo, line_dash="dash", annotation_text="70 %")
    fig.add_vline(x=k, line_dash="dot", annotation_text=f"k = {k}")
    fig.update_xaxes(title="Nº de componentes")
    fig.update_yaxes(title="Variância explicada acumulada", tickformat=".0%")
    return _base(fig, 320, showlegend=False)


# --------------------------------------------------------------------- centroides


def centroides(
    cen: pd.DataFrame,
    cids: Iterable[int],
    rotulos: dict[int, str],
    janela: tuple[pd.Timestamp, pd.Timestamp],
    suavizar: int,
    recessoes: bool,
    painel_proprio: bool,
) -> go.Figure:
    cids = list(cids)
    d = cen.loc[janela[0] : janela[1], cids]
    if suavizar > 1:
        d = d.rolling(suavizar, min_periods=1).mean()
    if painel_proprio and len(cids) > 1:
        cols = 2 if len(cids) <= 6 else 3
        linhas = int(np.ceil(len(cids) / cols))
        fig = make_subplots(
            rows=linhas,
            cols=cols,
            shared_xaxes=True,
            subplot_titles=[f"Cluster {c}" for c in cids],
            vertical_spacing=0.08,
        )
        for i, c in enumerate(cids):
            r, k = divmod(i, cols)
            fig.add_scatter(
                x=d.index,
                y=d[c],
                name=f"{c} — {rotulos[c][:30]}",
                line_color=cor_cluster(c),
                row=r + 1,
                col=k + 1,
                showlegend=False,
            )
            if recessoes:
                _recessoes(fig, d.index[0], d.index[-1], row=r + 1, col=k + 1)
        return _base(fig, 230 * linhas + 60)
    fig = go.Figure()
    for c in cids:
        fig.add_scatter(
            x=d.index,
            y=d[c],
            name=f"{c} — {rotulos[c][:34]}",
            line_color=cor_cluster(c),
            hovertemplate="%{x|%b %Y}: %{y:.2f}<extra>" + f"cluster {c}" + "</extra>",
        )
    if recessoes:
        _recessoes(fig, d.index[0], d.index[-1])
    fig.add_hline(y=0, line_color="grey", line_width=0.6)
    fig.update_yaxes(title="Centroide (desvios-padrão)")
    return _base(fig, 520, hovermode="x unified", legend={"orientation": "h", "y": -0.18})


def membros(
    df: pd.DataFrame,
    series: list[str],
    centro: pd.Series,
    cid: int,
    janela: tuple[pd.Timestamp, pd.Timestamp],
    recessoes: bool,
) -> go.Figure:
    d = df.loc[janela[0] : janela[1]]
    fig = go.Figure()
    for s in series:
        fig.add_scatter(
            x=d.index,
            y=d[s],
            name=s,
            line={"width": 1},
            opacity=0.55,
            hovertemplate=f"<b>{s}</b> %{{x|%b %Y}}: %{{y:.2f}}<extra></extra>",
        )
    fig.add_scatter(
        x=d.index,
        y=centro.loc[janela[0] : janela[1]],
        name=f"centroide {cid}",
        line={"color": "black", "width": 3},
    )
    if recessoes:
        _recessoes(fig, d.index[0], d.index[-1])
    fig.update_yaxes(title="Valor padronizado")
    return _base(fig, 440, hovermode="x unified")


# ------------------------------------------------------------------------ correlação


def heatmap_correlacao(corr: pd.DataFrame, cluster_de: dict[str, int]) -> go.Figure:
    rot = [f"{s} ({cluster_de[s]})" for s in corr.index]
    fig = go.Figure(
        go.Heatmap(
            z=corr.to_numpy(),
            x=rot,
            y=rot,
            zmin=-1,
            zmax=1,
            colorscale="RdBu_r",
            hovertemplate="%{y}<br>%{x}<br>r = %{z:.2f}<extra></extra>",
            colorbar={"title": "r"},
        )
    )
    fig.update_yaxes(autorange="reversed", showticklabels=len(rot) <= 40)
    fig.update_xaxes(showticklabels=len(rot) <= 40)
    return _base(fig, 640)


def par_series(df: pd.DataFrame, a: str, b: str, janela_roll: int) -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.4],
        vertical_spacing=0.06,
        subplot_titles=("Séries padronizadas", f"Correlação móvel ({janela_roll} meses)"),
    )
    fig.add_scatter(x=df.index, y=df[a], name=a, row=1, col=1)
    fig.add_scatter(x=df.index, y=df[b], name=b, row=1, col=1)
    rolling = df[a].rolling(janela_roll).corr(df[b])
    fig.add_scatter(x=df.index, y=rolling, name="r móvel", line_color="#d62728", row=2, col=1)
    fig.add_hline(y=0, line_color="grey", line_width=0.6, row=2, col=1)
    fig.update_yaxes(range=[-1, 1], row=2, col=1)
    return _base(fig, 520, hovermode="x unified")


# ---------------------------------------------------------------------------- rede


def rede(
    pos: dict[str, tuple[float, float]],
    arestas: pd.DataFrame,
    cluster_de: dict[str, int],
    nomes_cluster: dict[int, str],
    mostrar_pos: bool,
    mostrar_neg: bool,
    destacar: list[int],
    rotular: bool,
) -> go.Figure:
    fig = go.Figure()
    grau = pd.concat([arestas["a"], arestas["b"]]).value_counts() if len(arestas) else pd.Series()
    for sinal, cor, ativo in (
        (1, "rgba(44,160,44,0.30)", mostrar_pos),
        (-1, "rgba(214,39,40,0.30)", mostrar_neg),
    ):
        if not ativo or arestas.empty:
            continue
        e = arestas[np.sign(arestas["r"]) == sinal]
        xs: list[float | None] = []
        ys: list[float | None] = []
        for a, b in zip(e["a"], e["b"], strict=True):
            xs += [pos[a][0], pos[b][0], None]
            ys += [pos[a][1], pos[b][1], None]
        fig.add_scatter(
            x=xs,
            y=ys,
            mode="lines",
            line={"color": cor, "width": 1},
            hoverinfo="skip",
            name="correlação positiva" if sinal > 0 else "correlação negativa",
        )
    nos = list(pos)
    fig.add_scatter(
        x=[pos[s][0] for s in nos],
        y=[pos[s][1] for s in nos],
        mode="markers+text" if rotular else "markers",
        text=nos if rotular else None,
        textposition="top center",
        textfont={"size": 9},
        marker={
            "size": [9 + 2.2 * np.sqrt(grau.get(s, 0)) for s in nos],
            "color": [cor_cluster(cluster_de[s]) for s in nos],
            "line": {"width": 0.8, "color": "black"},
            "opacity": [1.0 if (not destacar or cluster_de[s] in destacar) else 0.15 for s in nos],
        },
        customdata=np.stack(
            [[nomes_cluster[cluster_de[s]] for s in nos], [int(grau.get(s, 0)) for s in nos]],
            axis=-1,
        ),
        hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>grau: %{customdata[1]}<extra></extra>"
        if rotular
        else "%{customdata[0]}<br>grau: %{customdata[1]}<extra></extra>",
        name="séries",
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x")
    return _base(fig, 720, legend={"orientation": "h", "y": 1.04})


# ---------------------------------------------------------------------- regressão


def heatmap_coeficientes(
    reg: pd.DataFrame,
    variaveis: list[str],
    alpha: float,
    so_significativos: bool,
    rot: pd.DataFrame,
) -> go.Figure:
    z = reg[[f"coef_{v}" for v in variaveis]].to_numpy().copy()
    p = reg[[f"pvalue_{v}" for v in variaveis]].to_numpy()
    sig = p < alpha
    if so_significativos:
        z = np.where(sig, z, np.nan)
    texto = np.where(sig, np.char.add(np.round(z, 2).astype(str), "*"), "")
    ylab = [
        f"{int(c)} — {rot.loc[rot['cluster'] == c, 'rotulo_curto'].iloc[0][:28]}"
        for c in reg["cluster"]
    ]
    lim = float(np.nanmax(np.abs(z))) if np.isfinite(z).any() else 1.0
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=variaveis,
            y=ylab,
            zmid=0,
            zmin=-lim,
            zmax=lim,
            colorscale="RdBu_r",
            text=texto,
            texttemplate="%{text}",
            customdata=p,
            hovertemplate="%{y}<br><b>%{x}</b><br>coef = %{z:.3f}<br>p = %{customdata:.3g}<extra></extra>",
            colorbar={"title": "coef"},
        )
    )
    fig.update_yaxes(autorange="reversed")
    return _base(fig, 640)


def coeficientes_cluster(tabela: pd.DataFrame, alpha: float) -> go.Figure:
    t = tabela.drop(index="const", errors="ignore")
    cor = np.where(t["p_valor"] < alpha, "#d62728", "#7f8c8d")
    fig = go.Figure(
        go.Scatter(
            x=t["coef"],
            y=t.index,
            mode="markers",
            marker={"color": cor, "size": 11},
            error_x={
                "type": "data",
                "symmetric": False,
                "array": t["ic_sup"] - t["coef"],
                "arrayminus": t["coef"] - t["ic_inf"],
            },
            customdata=t["p_valor"],
            hovertemplate="%{y}<br>coef = %{x:.3f}<br>p = %{customdata:.3g}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_color="grey")
    fig.update_xaxes(title="Coeficiente (IC 95 %, vermelho = significativo)")
    return _base(fig, 320, showlegend=False)


def residuos(res: pd.Series) -> go.Figure:
    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.65, 0.35], subplot_titles=("Resíduos", "ACF")
    )
    fig.add_scatter(x=res.index, y=res, line_color="#1f77b4", name="resíduo", row=1, col=1)
    n = len(res)
    ac = [res.autocorr(lag) for lag in range(1, 25)]
    fig.add_bar(x=list(range(1, 25)), y=ac, marker_color="#1f77b4", name="ACF", row=1, col=2)
    banda = 1.96 / np.sqrt(n)
    for s in (banda, -banda):
        fig.add_hline(y=s, line_dash="dash", line_color="grey", row=1, col=2)
    return _base(fig, 300, showlegend=False)


# ------------------------------------------------------------------- estabilidade


def bootstrap(boot: pd.DataFrame, extra: pd.DataFrame | None = None) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(
        x=boot["cluster"].astype(str),
        y=boot["jaccard_medio"],
        error_y={"type": "data", "array": boot["jaccard_std"]},
        marker_color=[cor_cluster(c) for c in boot["cluster"]],
        name="Notebook (B = 500)",
        hovertemplate="Cluster %{x}<br>Jaccard médio = %{y:.3f}<extra></extra>",
    )
    if extra is not None and not extra.empty:
        fig.add_scatter(
            x=extra["cluster"].astype(str),
            y=extra["jaccard_medio"],
            mode="markers",
            marker={"symbol": "diamond", "size": 13, "color": "black"},
            name="Execução ao vivo",
        )
    fig.add_hline(y=0.5, line_dash="dash", annotation_text="0,5")
    fig.update_xaxes(title="Cluster (achado genuíno)", type="category")
    fig.update_yaxes(title="Jaccard médio", range=[0, 1.05])
    return _base(fig, 380)


def hist_jaccard(valores: dict[int, list[float]]) -> go.Figure:
    fig = go.Figure()
    for cid, v in valores.items():
        fig.add_histogram(
            x=v,
            name=f"cluster {cid}",
            marker_color=cor_cluster(cid),
            opacity=0.7,
            xbins={"start": 0, "end": 1.0001, "size": 0.05},
        )
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title="Jaccard por reamostragem")
    return _base(fig, 340)


def contingencia(tab: pd.DataFrame, rotulo_linhas: str, rotulo_colunas: str) -> go.Figure:
    fig = go.Figure(
        go.Heatmap(
            z=tab.to_numpy(),
            x=[str(c) for c in tab.columns],
            y=[str(i) for i in tab.index],
            colorscale="Blues",
            text=np.where(tab.to_numpy() > 0, tab.to_numpy(), ""),
            texttemplate="%{text}",
            hovertemplate=f"{rotulo_linhas} %{{y}} × {rotulo_colunas} %{{x}}: %{{z}} séries<extra></extra>",
            showscale=False,
        )
    )
    fig.update_xaxes(title=rotulo_colunas, type="category")
    fig.update_yaxes(title=rotulo_linhas, type="category", autorange="reversed")
    return _base(fig, 520)


def dendrograma(
    z: np.ndarray, nomes: list[str], cluster_de: dict[str, int], k: int | None
) -> go.Figure:
    d = dendrogram(z, no_plot=True, labels=nomes)
    fig = go.Figure()
    for ic, dc in zip(d["icoord"], d["dcoord"], strict=True):
        fig.add_scatter(
            x=ic,
            y=dc,
            mode="lines",
            line={"color": "#888", "width": 1},
            hoverinfo="skip",
            showlegend=False,
        )
    folhas = d["ivl"]
    xs = [5 + 10 * i for i in range(len(folhas))]
    fig.add_scatter(
        x=xs,
        y=[0] * len(folhas),
        mode="markers",
        marker={
            "size": 9,
            "color": [cor_cluster(cluster_de[s]) for s in folhas],
            "line": {"width": 0.6, "color": "black"},
        },
        text=folhas,
        customdata=[cluster_de[s] for s in folhas],
        hovertemplate="<b>%{text}</b><br>cluster K-Means: %{customdata}<extra></extra>",
        showlegend=False,
    )
    if k and 1 < k <= len(nomes):
        altura = (z[-(k - 1), 2] + z[-k, 2]) / 2
        fig.add_hline(
            y=altura, line_dash="dash", line_color="#d62728", annotation_text=f"corte em k = {k}"
        )
    fig.update_xaxes(
        tickmode="array", tickvals=xs, ticktext=folhas, tickangle=-90, tickfont={"size": 8}
    )
    fig.update_yaxes(title="Distância de Ward")
    return _base(fig, 560)


def varredura_k(v: pd.DataFrame, k_atual: int) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_scatter(
        x=v["k"], y=v["inercia"], name="Inércia", mode="lines+markers", secondary_y=False
    )
    fig.add_scatter(
        x=v["k"],
        y=v["silhueta"],
        name="Silhueta",
        mode="lines+markers",
        line_color="#d62728",
        secondary_y=True,
    )
    fig.add_vline(x=k_atual, line_dash="dot", annotation_text=f"k = {k_atual}")
    fig.update_xaxes(title="k")
    fig.update_yaxes(title="Inércia", secondary_y=False)
    fig.update_yaxes(title="Silhueta", secondary_y=True)
    return _base(fig, 360, legend={"orientation": "h", "y": 1.12})
