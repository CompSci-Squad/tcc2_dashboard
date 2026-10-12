# tcc2_dashboard

Dashboard interativo (Streamlit) do TCC2 do grupo CICD06: agrupamento de séries do FRED-MD
(McCracken & Ng, 2016) seguindo o pipeline de Santos et al. (2021). Cada ponto é uma **série**
macroeconômica inteira, não uma observação mensal.

Os dados vêm das tabelas exportadas pelo notebook do repositório `tcc2` e ficam versionados em
`src/tcc2_dashboard/dados/`, então o app roda sem o notebook.

## Rodar

```bash
uv sync
uv run streamlit run src/tcc2_dashboard/app.py   # ou: make run / uv run tcc2-dashboard
```

## O que dá para explorar

| Página | Interações |
|---|---|
| Visão geral | clique nas barras para focar um cluster; corte de R² ajustável; treemap cluster → séries |
| Mapa das séries | PCA 2D/3D, escolha de componentes, cor por cluster/tcode/correlação, destaque e busca |
| Centroides no tempo | seleção múltipla, janela de datas, média móvel, recessões NBER, painéis, séries-membro |
| Explorador de séries | comparação par a par com correlação móvel, vizinhas mais correlacionadas, heatmap |
| Rede de correlação | limiar \|r\| ao vivo, sinais, 3 layouts, estatísticas dentro × entre clusters |
| Regressão | principal (6 var.) × robustez (5 var.), nível de significância, OLS × HAC, **regressão refeita ao vivo** |
| Estabilidade | bootstrap em blocos (tabela do notebook + execução ao vivo), dendrograma Ward com corte, e se k fosse outro |
| Metodologia | pipeline, limitações conhecidas (bug do EM-PCA, autocorrelação), figuras e downloads |

O cluster em foco é compartilhado entre as páginas.

## Desenvolvimento

```bash
make check        # ruff + mypy + pytest
make fmt          # ruff --fix + format
uv run pre-commit install
```

Os testes (`tests/`) conferem que o K-Means reproduz a partição do notebook (ARI = 1), que a
regressão HAC bate com as tabelas salvas e que cada página renderiza (`streamlit.testing`).

Stack: uv, ruff (lint + format), mypy, pytest, pre-commit, GitHub Actions, Docker.

## Limites

- A regressão ao vivo usa as 5 variáveis de janela cheia; o câmbio (6ª variável) não está nas
  tabelas exportadas. A especificação principal de 6 variáveis aparece só a partir dos resultados salvos.
- O bootstrap ao vivo usa `n_init = 3` (rápido); o resultado oficial é o do notebook (B = 500).
- Os resultados herdam o bug conhecido de convergência do `em_pca_impute` (ver página Metodologia).
