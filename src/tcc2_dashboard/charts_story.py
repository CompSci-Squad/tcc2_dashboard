"""Gráficos narrativos e animados (Plotly com frames) para as páginas voltadas ao público geral."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from tcc2_dashboard import catalogo, style
from tcc2_dashboard.charts import _base, _recessoes
from tcc2_dashboard.config import cor_cluster


def _play_style() -> dict:
    t = style.tokens()
    return {
        "bgcolor": t["primary_soft"],
        "bordercolor": t["line"],
        "active": -1,
        "borderwidth": 1,
        "font": {"color": t["ink"], "size": 12},
    }


def _wrap(texto: str, largura: int = 16, linhas: int = 3) -> str:
    """Quebra um rótulo em linhas curtas para caber dentro de um quadrado do mapa."""
    palavras, atual, saida = texto.split(), "", []
    for p in palavras:
        if len(atual) + len(p) + 1 > largura and atual:
            saida.append(atual)
            atual = p
        else:
            atual = f"{atual} {p}".strip()
    if atual:
        saida.append(atual)
    if len(saida) > linhas:
        saida = [*saida[: linhas - 1], saida[linhas - 1] + "…"]
    return "<br>".join(saida)


# ---------------------------------------------------------------- visão geral


def categorias(meta: pd.DataFrame, selecionada: str | None = None) -> go.Figure:
    """Quantas séries existem em cada categoria oficial do FRED-MD (barras clicáveis)."""
    cont = meta["categoria"].value_counts().reindex(catalogo.CATEGORIAS).dropna().sort_values()
    cats = cont.index.tolist()
    fig = go.Figure(
        go.Bar(
            x=cont.to_numpy(),
            y=cats,
            orientation="h",
            marker={
                "color": [catalogo.CATEGORIA_COR[c] for c in cats],
                "opacity": [1.0 if (selecionada in (None, c)) else 0.35 for c in cats],
                "cornerradius": 8,
            },
            text=[f"<b>{n}</b>" for n in cont],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x} séries<extra></extra>",
        )
    )
    fig.update_xaxes(visible=False, range=[0, cont.max() * 1.15])
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_layout(transition={"duration": 500})
    return _base(fig, 380, showlegend=False)


# --------------------------------------------------------------------- mapa


def mapa_morph(coords: pd.DataFrame, meta: pd.DataFrame, nome_cluster: dict[int, str]) -> go.Figure:
    """Animação: das categorias oficiais (colunas) para as famílias achadas pelos dados (mapa PCA)."""
    t = style.tokens()
    d = coords[["PC1", "PC2"]].join(meta.set_index("serie")).copy()
    d["serie"] = d.index
    for c in ("PC1", "PC2"):
        d[c] = (d[c] - d[c].min()) / (d[c].max() - d[c].min())
    cats = catalogo.CATEGORIAS
    rng = np.random.default_rng(3)
    idx = d["categoria"].map({c: i for i, c in enumerate(cats)}).to_numpy()
    d["sx"] = (idx + 0.5) / len(cats) + rng.uniform(-0.04, 0.04, len(d))
    d["sy"] = rng.uniform(0.05, 0.88, len(d))

    texto = [
        f"<b>{s}</b><br>{r.descricao}<br>Categoria oficial: {r.categoria}"
        f"<br>Família {r.cluster}: {nome_cluster[int(r.cluster)]}"
        for s, r in zip(d["serie"], d.itertuples(), strict=True)
    ]
    cor_cat = [catalogo.CATEGORIA_COR[c] for c in d["categoria"]]
    cor_fam = [cor_cluster(c) for c in d["cluster"]]
    marker = {"size": 13, "line": {"width": 1, "color": t["card"]}, "opacity": 0.95}

    def anot_cats() -> list[dict]:
        return [
            {
                "x": (i + 0.5) / len(cats),
                "y": 0.98,
                "text": f"<b>{c.replace(' e ', ' e<br>', 1) if len(c) > 14 else c}</b>",
                "showarrow": False,
                "font": {"size": 11, "color": catalogo.CATEGORIA_COR[c]},
                "yanchor": "bottom",
            }
            for i, c in enumerate(cats)
        ]

    f_cat = go.Frame(
        name="categorias",
        data=[go.Scatter(x=d["sx"], y=d["sy"], marker={"color": cor_cat})],
        layout={"annotations": anot_cats()},
    )
    f_fam = go.Frame(
        name="familias",
        data=[go.Scatter(x=d["PC1"], y=d["PC2"], marker={"color": cor_fam})],
        layout={"annotations": []},
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=d["sx"],
                y=d["sy"],
                mode="markers",
                marker={**marker, "color": cor_cat},
                text=texto,
                hovertemplate="%{text}<extra></extra>",
            )
        ],
        frames=[f_cat, f_fam],
    )
    anim = {
        "frame": {"duration": 1300, "redraw": True},
        "transition": {"duration": 1300, "easing": "cubic-in-out"},
        "mode": "immediate",
    }
    fig.update_layout(
        annotations=anot_cats(),
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0.0,
                "y": -0.04,
                "xanchor": "left",
                "yanchor": "top",
                "pad": {"r": 6, "t": 4},
                "buttons": [
                    {
                        "label": "1 · Categorias oficiais",
                        "method": "animate",
                        "args": [["categorias"], anim],
                    },
                    {
                        "label": "2 · Famílias descobertas pelos dados",
                        "method": "animate",
                        "args": [["familias"], anim],
                    },
                ],
                **_play_style(),
            }
        ],
    )
    fig.update_xaxes(visible=False, range=[-0.03, 1.03])
    fig.update_yaxes(visible=False, range=[-0.05, 1.12])
    return _base(fig, 560, showlegend=False)


# -------------------------------------------------------------- centroide animado


def centroide_animado(
    cen: pd.DataFrame, cids: list[int], rotulos: dict[int, str], recessoes: bool
) -> go.Figure:
    """Linha do tempo que se desenha ano a ano (botão Reproduzir + barra deslizante)."""
    cids = list(cids)
    anos = sorted({ts.year for ts in cen.index})
    fins = {a: cen.index[cen.index.year == a][-1] for a in anos}
    ymin, ymax = (float(v) for v in np.nanquantile(cen[cids].to_numpy(), [0.005, 0.995]))
    pad = 0.06 * (ymax - ymin)

    def traces(ate: pd.Timestamp) -> list[go.Scatter]:
        parte = cen.loc[:ate, cids]
        return [
            go.Scatter(
                x=parte.index,
                y=parte[c],
                mode="lines",
                line={"color": cor_cluster(c), "width": 1.8},
                name=f"{c} — {rotulos[c][:30]}",
            )
            for c in cids
        ]

    fig = go.Figure(data=traces(fins[anos[-1]]))
    fig.frames = [go.Frame(name=str(a), data=traces(fins[a])) for a in anos]
    quadro = {
        "frame": {"duration": 120, "redraw": False},
        "transition": {"duration": 0},
        "mode": "immediate",
    }
    fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0.0,
                "y": -0.12,
                "xanchor": "left",
                "yanchor": "top",
                "buttons": [
                    {
                        "label": "▶ Reproduzir",
                        "method": "animate",
                        "args": [[str(a) for a in anos], quadro],
                    },
                    {
                        "label": "⏸ Pausar",
                        "method": "animate",
                        "args": [[None], {"mode": "immediate", "frame": {"duration": 0}}],
                    },
                ],
                **_play_style(),
            }
        ],
        sliders=[
            {
                "x": 0.22,
                "len": 0.78,
                "y": -0.06,
                "currentvalue": {"prefix": "Até ", "font": {"size": 12}},
                "steps": [
                    {
                        "label": str(a),
                        "method": "animate",
                        "args": [
                            [str(a)],
                            {
                                "mode": "immediate",
                                "frame": {"duration": 0, "redraw": False},
                                "transition": {"duration": 0},
                            },
                        ],
                    }
                    for a in anos
                ],
            }
        ],
    )
    if recessoes:
        _recessoes(fig, cen.index[0], cen.index[-1])
    fig.add_hline(y=0, line_width=0.6, line_color="grey")
    fig.update_xaxes(range=[cen.index[0], cen.index[-1]])
    fig.update_yaxes(range=[ymin - pad, ymax + pad], title="Perfil do grupo (desvios-padrão)")
    return _base(
        fig, 520, legend={"orientation": "h", "y": 1.1}, margin={"b": 90, "t": 28, "l": 14, "r": 14}
    )


def sobreposicao(
    centro: pd.Series, variavel: pd.Series, nome_centro: str, nome_var: str, cid: int
) -> go.Figure:
    """O grupo e a variável de referência na mesma escala, com seletor de período."""
    t = style.tokens()
    fig = go.Figure()
    fig.add_scatter(
        x=centro.index,
        y=centro,
        name=nome_centro,
        line={"color": cor_cluster(cid), "width": 1.8},
        hovertemplate="%{x|%b %Y}: %{y:.2f}<extra>" + nome_centro[:28] + "</extra>",
    )
    fig.add_scatter(
        x=variavel.index,
        y=variavel,
        name=nome_var,
        line={"color": t["accent"], "width": 1.4, "dash": "dot"},
        hovertemplate="%{x|%b %Y}: %{y:.2f}<extra>" + nome_var[:28] + "</extra>",
    )
    fig.update_xaxes(
        rangeslider={"visible": True, "thickness": 0.07},
        rangeselector={
            "buttons": [
                {"count": 10, "label": "10 anos", "step": "year", "stepmode": "backward"},
                {"count": 25, "label": "25 anos", "step": "year", "stepmode": "backward"},
                {"step": "all", "label": "Tudo"},
            ],
            "bgcolor": style.tokens()["primary_soft"],
            "font": {"color": style.tokens()["ink"]},
        },
    )
    fig.update_yaxes(title="Variação mensal (desvios-padrão)")
    lo, hi = np.nanquantile(
        np.concatenate([centro.to_numpy(), variavel.to_numpy()]), [0.005, 0.995]
    )
    pad = 0.25 * (hi - lo)
    fig.update_yaxes(range=[lo - pad, hi + pad])
    return _base(fig, 430, hovermode="x unified", legend={"orientation": "h", "y": 1.14})


# ---------------------------------------------------------- variáveis de referência

_ESCALA_FORCA = [[0.0, "#F59E0B"], [0.5, "#E2E8F0"], [1.0, "#4F46E5"]]
_LIM = 0.9


def frase_resposta(var: str, coef: float, p: float, alpha: float) -> str:
    """Resultado da regressão dito em palavras (sem tabela de coeficientes)."""
    sobe = catalogo.REFERENCIAS[var]["sobe"]
    if p >= alpha:
        return "Sem resposta clara a esta variável."
    forca = "forte" if abs(coef) >= 0.5 else "moderada" if abs(coef) >= 0.2 else "fraca"
    sentido = "sobe" if coef > 0 else "cai"
    return f"Quando {sobe}, esta família tende a {sentido}. Resposta {forca}."


def mapa_variavel(
    reg: pd.DataFrame,
    variaveis: list[str],
    inicial: str,
    alpha: float,
    rot: pd.DataFrame,
) -> go.Figure:
    """19 quadrados (um por família) coloridos pela força da resposta a UMA variável.

    Há um frame por variável: o filtro da página define o inicial; o botão percorre todas.
    """
    t = style.tokens()
    n, cols = 19, 4
    linhas = int(np.ceil(n / cols))
    reg = reg.set_index("cluster")
    rotulos = dict(zip(rot["cluster"].astype(int), rot["rotulo_curto"], strict=True))

    def grade(var: str) -> tuple[np.ndarray, np.ndarray]:
        z = np.full((linhas, cols), np.nan)
        h = np.full((linhas, cols), "", dtype=object)
        for cid in range(n):
            r, c = divmod(cid, cols)
            coef, p = float(reg.loc[cid, f"coef_{var}"]), float(reg.loc[cid, f"pvalue_{var}"])
            if p < alpha:
                z[r, c] = coef
            h[r, c] = (
                f"<b>Família {cid}</b> · {rotulos[cid]}<br>{frase_resposta(var, coef, p, alpha)}"
            )
        return z, h

    base_z = np.zeros((linhas, cols))
    base_z[-1, -1] = np.nan  # quadrado vazio
    z0, h0 = grade(inicial)
    fundo = go.Heatmap(
        z=base_z,
        colorscale=[[0, t["line"]], [1, t["line"]]],
        showscale=False,
        hoverinfo="skip",
        xgap=6,
        ygap=6,
    )
    topo = go.Heatmap(
        z=z0,
        hovertext=h0,
        hovertemplate="%{hovertext}<extra></extra>",
        colorscale=_ESCALA_FORCA,
        zmin=-_LIM,
        zmax=_LIM,
        xgap=6,
        ygap=6,
        colorbar={
            "title": {"text": "Resposta", "side": "right"},
            "thickness": 12,
            "len": 0.8,
            "tickvals": [-_LIM, 0, _LIM],
            "ticktext": ["oposta", "nenhuma", "mesmo sentido"],
        },
    )
    fig = go.Figure(data=[fundo, topo])
    frames = []
    for v in variaveis:
        z, h = grade(v)
        frames.append(
            go.Frame(
                name=v,
                data=[go.Heatmap(z=z, hovertext=h)],
                traces=[1],
                layout={"title": {"text": f"<b>{catalogo.REFERENCIAS[v]['nome']}</b>", "x": 0.0}},
            )
        )
    fig.frames = frames

    anot = []
    for cid in range(n):
        r, c = divmod(cid, cols)
        anot.append(
            {
                "x": c,
                "y": r,
                "xref": "x",
                "yref": "y",
                "showarrow": False,
                "text": f"<b>{cid}</b><br><span style='font-size:10px'>{_wrap(rotulos[cid])}</span>",
                "font": {"size": 12, "color": t["ink"]},
                "bgcolor": "rgba(255,255,255,.62)"
                if style.tema() == "light"
                else "rgba(11,16,32,.62)",
                "borderpad": 3,
            }
        )
    anim = {
        "frame": {"duration": 1400, "redraw": True},
        "transition": {"duration": 600, "easing": "cubic-in-out"},
        "mode": "immediate",
    }
    fig.update_layout(
        annotations=anot,
        title={"text": f"<b>{catalogo.REFERENCIAS[inicial]['nome']}</b>", "x": 0.0},
        updatemenus=[
            {
                "type": "buttons",
                "x": 1.0,
                "y": 1.12,
                "xanchor": "right",
                "yanchor": "top",
                "buttons": [
                    {
                        "label": "▶ Passar pelas 6 variáveis",
                        "method": "animate",
                        "args": [variaveis, anim],
                    },
                ],
                **_play_style(),
            }
        ],
    )
    fig.update_xaxes(visible=False, autorange=True)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor=None)
    return _base(fig, 130 * linhas + 60, margin={"t": 60, "l": 10, "r": 10, "b": 10})


def mapa_geral(
    reg: pd.DataFrame, variaveis: list[str], alpha: float, rot: pd.DataFrame
) -> go.Figure:
    """Visão completa 19 × 6: só cor, sem números."""
    reg = reg.sort_values("cluster")
    rotulos = dict(zip(rot["cluster"].astype(int), rot["rotulo_curto"], strict=True))
    z = np.full((len(reg), len(variaveis)), np.nan)
    hover = np.empty(z.shape, dtype=object)
    for j, v in enumerate(variaveis):
        for i, (cid, coef, p) in enumerate(
            zip(reg["cluster"], reg[f"coef_{v}"], reg[f"pvalue_{v}"], strict=True)
        ):
            if p < alpha:
                z[i, j] = coef
            hover[i, j] = (
                f"<b>Família {int(cid)}</b> · {rotulos[int(cid)]}<br>{frase_resposta(v, coef, p, alpha)}"
            )
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=[catalogo.REFERENCIAS[v]["nome"] for v in variaveis],
            y=[f"{int(c)} · {rotulos[int(c)][:34]}" for c in reg["cluster"]],
            hovertext=hover,
            hovertemplate="%{hovertext}<extra></extra>",
            colorscale=_ESCALA_FORCA,
            zmin=-_LIM,
            zmax=_LIM,
            xgap=3,
            ygap=3,
            colorbar={
                "thickness": 10,
                "tickvals": [-_LIM, 0, _LIM],
                "ticktext": ["oposta", "nenhuma", "mesmo sentido"],
            },
        )
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(side="top")
    return _base(fig, 620, margin={"t": 70, "l": 10, "r": 10, "b": 10})
