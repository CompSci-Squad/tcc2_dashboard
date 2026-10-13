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

## Páginas

Pensado para quem não conhece o assunto: linguagem simples, toda série tem descrição em português
(passe o mouse sobre os códigos) e há tema claro/escuro (menu ⋮ → Settings → Theme; segue o
sistema por padrão).

| Grupo | Página | O que tem |
|---|---|---|
| Comece por aqui | Visão geral | cartão com os números do estudo (animados), séries por tema, o que é o FRED-MD |
| | Os quatro achados | um cartão por achado genuíno (famílias 3, 4, 14, 18) com frase de leitura, R², estabilidade e gráfico família × indicador |
| | Explorar famílias | filtro das 19 famílias, séries com descrição, perfil no tempo (gráfico ou animação ano a ano), comparação |
| | Variáveis de referência | filtro de 6 indicadores e mapa de calor em quadrados, sem tabela de coeficientes (animável) |
| | O projeto | o que é, para que serve, 6 passos em linguagem simples, glossário, autores e fontes (baseado no artigo CONIC) |
| Aprofunde | Mapa das séries | animação das categorias oficiais para as famílias descobertas, mapa PCA 2D/3D |
| | Comparar famílias | várias famílias no mesmo gráfico, recessões NBER, animação |
| | Explorador de séries | comparação de dois indicadores, correlação móvel, mapa de semelhanças |
| | Rede de semelhanças | limiar ajustável, três disposições |
| Detalhes técnicos | Regressão, Estabilidade, Metodologia | regressão HAC refeita ao vivo (6 variáveis), bootstrap em blocos, Ward, limitações |

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

- O câmbio (6ª variável) é reconstruído do CSV bruto (Δlog + z-score) e reproduz exatamente o
  coeficiente salvo da regressão principal (ver ).
- O bootstrap ao vivo usa  (rápido); o resultado oficial é o do notebook (B = 500).
- Os resultados herdam o bug conhecido de convergência do  (ver página Metodologia).
