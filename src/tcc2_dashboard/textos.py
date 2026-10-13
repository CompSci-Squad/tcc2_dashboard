"""Frases em linguagem simples geradas a partir dos números (sem jargão estatístico)."""

from __future__ import annotations

from tcc2_dashboard import catalogo, data


def forca(r2: float) -> str:
    if r2 >= 0.6:
        return "forte"
    if r2 >= 0.4:
        return "razoável"
    if r2 >= 0.1:
        return "fraca"
    return "praticamente nula"


def estabilidade(jaccard: float) -> tuple[str, str]:
    """(rótulo, tipo de pílula) para a estabilidade do grupo sob reamostragem."""
    if jaccard >= 0.7:
        return "estável", "ok"
    if jaccard >= 0.5:
        return "estabilidade média", "warn"
    return "estabilidade baixa", "low"


def info_familia(cid: int) -> dict:
    """Tudo que as páginas precisam saber sobre uma família, já em palavras simples."""
    rot = data.rotulados().set_index("cluster").loc[cid]
    reg = data.regressao("principal").set_index("cluster").loc[cid]
    meta = data.series_meta()
    membros = meta[meta["cluster"] == cid].sort_values("corr_centroide", ascending=False)
    var = rot["variavel_dominante"]
    ref = catalogo.REFERENCIAS[var]
    coef = float(reg[f"coef_{var}"])
    p_valor = float(reg[f"pvalue_{var}"])
    r2 = float(rot["r_squared"])
    top_cats = membros["categoria"].value_counts().head(2).index.tolist()
    if r2 < 0.1:
        leitura = "Nenhuma das seis variáveis de referência explica bem o vai e vem desta família."
    else:
        sentido = "sobe" if coef > 0 else "cai"
        leitura = (
            f"Acompanha {ref['nome'].lower()}: quando {ref['sobe']}, a família tende a {sentido}. "
            f"A relação é {forca(r2)} ({r2:.0%} do vai e vem explicado)."
        )
    boot = data.bootstrap_jaccard().set_index("cluster")
    est = None
    if cid in boot.index:
        est = estabilidade(float(boot.loc[cid, "jaccard_medio"]))
    return {
        "cid": cid,
        "rotulo": rot["rotulo_curto"],
        "n": len(membros),
        "membros": membros,
        "var": var,
        "var_nome": ref["nome"],
        "coef": coef,
        "p": p_valor,
        "r2": r2,
        "leitura": leitura,
        "categorias": top_cats,
        "classe": rot["classe"],
        "achado": bool(rot["achado"]),
        "estabilidade": est,
        "jaccard": float(boot.loc[cid, "jaccard_medio"]) if cid in boot.index else None,
    }


def resumo_composicao(info: dict) -> str:
    n = info["n"]
    cats = info["categorias"]
    base = f"{n} série" + ("s" if n != 1 else "")
    if len(cats) == 1:
        return f"{base}, todas de {cats[0].lower()}."
    return f"{base}, principalmente de {cats[0].lower()} e {cats[1].lower()}."


def interpretacao_numerica(info: dict) -> str:
    """O que o coeficiente e o R² querem dizer, em palavras e com os números reais."""
    ref = catalogo.REFERENCIAS[info["var"]]
    c, r2, p = info["coef"], info["r2"], info["p"]
    sentido = "sobe" if c > 0 else "cai"
    p_txt = "menor que 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")
    return (
        f"Em média, quando {ref['sobe']} 1 desvio-padrão acima do normal, a família {sentido} "
        f"cerca de {abs(c):.2f} desvio-padrão, descontados os outros cinco indicadores. "
        f"A relação passou no teste estatístico (p = {p_txt}). Os seis indicadores juntos "
        f"explicam {r2:.0%} do vai e vem da família; os outros {1 - r2:.0%} vêm de fatores que "
        "o estudo não mede."
    )


def mistura_categorias() -> tuple[int, int, list[tuple[int, int]]]:
    """(famílias que juntam 2+ categorias oficiais, total, as 3 mais misturadas)."""
    meta = data.series_meta()
    n_cat = meta.groupby("cluster")["categoria"].nunique()
    mistas = n_cat[n_cat > 1]
    topo = mistas.sort_values(ascending=False).head(3)
    return len(mistas), len(n_cat), [(int(c), int(n)) for c, n in topo.items()]
