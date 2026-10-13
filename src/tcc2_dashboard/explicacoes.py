"""Textos de apoio à leitura: o que cada gráfico mostra, como lê-lo e como NÃO o interpretar.

Linguagem simples, de propósito. Cada guia tem: o_que (uma frase), como_ler (lista curta) e
cuidado (o erro de leitura mais comum). `**texto**` vira negrito.
"""

from __future__ import annotations

GUIAS: dict[str, dict] = {
    # ---------------------------------------------------------------- visão geral
    "categorias": {
        "o_que": "Quantas séries existem em cada uma das 8 categorias oficiais do FRED-MD.",
        "como_ler": [
            "Barra maior = mais indicadores naquele tema.",
            "Escolha um tema nos botões ao lado para listar as séries dele.",
        ],
        "cuidado": "Categoria não é família. As categorias são etiquetas feitas por especialistas; "
        "as 19 famílias do estudo foram formadas pelo comportamento dos dados e misturam categorias.",
    },
    "treemap": {
        "o_que": "As 19 famílias achadas pelo estudo e as séries que ficaram dentro de cada uma.",
        "como_ler": [
            "Cada bloco grande é uma família; o tamanho mostra quantas séries ela tem.",
            "A cor mostra quanto do vai e vem da família os indicadores de referência explicam: "
            "quanto mais escuro, maior a parte explicada.",
            "Clique em um bloco para ampliar e na barra de cima para voltar.",
        ],
        "cuidado": "Cor clara não quer dizer família ruim. Quer dizer só que nenhum dos seis "
        "indicadores de referência a explica bem.",
    },
    # --------------------------------------------------------------------- achados
    "achados_cartoes": {
        "o_que": "Um resumo de cada achado: que família é, a que indicador ela responde e quão "
        "firme é o resultado.",
        "como_ler": [
            "**Círculo**: a parte do vai e vem da família explicada pelos seis indicadores de "
            "referência (o R²). 48% é quase metade; o resto vem de fatores que o estudo não mede.",
            "**Responde a**: o indicador cuja relação com a família foi a mais forte e convincente.",
            "**Selo**: refizemos o agrupamento 500 vezes embaralhando blocos de 12 meses. "
            "**Estável** (70% ou mais): o grupo quase sempre reaparece. **Média** (50 a 70%). "
            "**Baixa** (menos de 50%): a composição do grupo muda bastante.",
        ],
        "cuidado": "“Responde a” descreve uma associação estatística, não prova que um indicador "
        "causa o outro. Selo de estabilidade baixa não derruba o achado, mas pede cautela.",
    },
    "achados_grafico": {
        "o_que": "A família (linha cheia) e o indicador de referência (linha pontilhada), mês a mês.",
        "como_ler": [
            "As duas linhas mostram a **variação mensal**, padronizada: 0 é um mês normal; "
            "picos são meses fora do comum.",
            "Relação positiva: as linhas sobem e descem juntas. Negativa: em sentidos opostos.",
            "Use **Suavizar** para ver a tendência sem o ruído e a barra abaixo do gráfico para "
            "dar zoom em uma época.",
        ],
        "cuidado": "Não é o valor do indicador (como a taxa de desemprego em %), e sim o quanto "
        "ele mudou de um mês para o outro. Os picos de 2020 (pandemia) são os maiores da história.",
    },
    # -------------------------------------------------------------------- explorar
    "explorar_perfil": {
        "o_que": "O perfil médio da família: a média das variações mensais de todas as suas séries.",
        "como_ler": [
            "O eixo vertical está em desvios-padrão: 0 é um mês normal; 2 ou -2 já é um mês bem "
            "fora do comum.",
            "As faixas cinza são recessões dos EUA (datadas pelo NBER). Veja se a família reage a elas.",
            "Em “Comparar com outras famílias” dá para ver quais reagem às mesmas crises.",
        ],
        "cuidado": "Isto não é o nível do indicador, e sim sua variação de um mês para o outro. "
        "“Ampliar” esconde meses extremos (como abril de 2020) para dar zoom no resto.",
    },
    "explorar_series": {
        "o_que": "As séries que formam a família e o que cada uma mede.",
        "como_ler": [
            "**Quão típica** vai de 0 a 1: perto de 1, a série acompanha de perto o perfil médio "
            "da família; perto de 0, é a mais diferente do grupo.",
            "A primeira da lista é a mais representativa da família.",
        ],
        "cuidado": "Uma série pouco típica continua pertencendo à família, só é a menos "
        "representativa dela.",
    },
    # ------------------------------------------------------------------- variáveis
    "variaveis_mapa": {
        "o_que": "Para o indicador escolhido, quais famílias reagem a ele e com que força.",
        "como_ler": [
            "Cada quadrado é uma família. **Índigo** = anda no mesmo sentido do indicador; "
            "**âmbar** = no sentido oposto. Cor mais intensa = resposta mais forte.",
            "**Cinza** = sem resposta clara: a relação não passou no teste estatístico.",
            "A força é quanto a família muda (em desvios-padrão) quando o indicador muda 1 "
            "desvio-padrão: acima de 0,5 é forte; entre 0,2 e 0,5, moderada; abaixo de 0,2, fraca.",
            "Passe o mouse para ler o resultado em uma frase; o botão ▶ percorre os seis indicadores.",
        ],
        "cuidado": "Cada indicador é avaliado junto com os outros cinco, então a cor mostra o efeito "
        "dele depois de descontar os demais. Cinza não prova que não há relação, só que os dados "
        "não a sustentam. E, como testamos 114 combinações, de 5 a 6 respostas “significativas” "
        "poderiam aparecer só por acaso.",
    },
    # ------------------------------------------------------------------------ mapa
    "mapa_morph": {
        "o_que": "Cada ponto é uma série. Na vista 1 elas estão separadas pelas 8 categorias "
        "oficiais; na vista 2, pela semelhança de comportamento ao longo dos 61 anos.",
        "como_ler": [
            "Na vista 2, pontos próximos se comportam de forma parecida.",
            "As cores da vista 2 são as 19 famílias.",
            "Se cada família fosse de uma única categoria, as etiquetas oficiais já bastariam. "
            "Quando uma cor aparece junto de séries de várias categorias, o método achou uma "
            "ligação que a classificação oficial não mostra.",
        ],
        "cuidado": "O mapa é uma foto em 2 dimensões de algo com 735 dimensões (os meses). Ele "
        "resume só uma parte da informação, então pontos que parecem juntos podem estar mais "
        "distantes do que aparentam.",
    },
    "mapa_pca": {
        "o_que": "O mesmo mapa, agora interativo: dá para girar, destacar famílias e procurar séries.",
        "como_ler": [
            "Pontos próximos = séries que se movem de forma parecida.",
            "“Quão típica na família” colore pela proximidade de cada série ao perfil médio da sua família.",
            "Clique na legenda para esconder ou isolar uma família.",
        ],
        "cuidado": "Os eixos (PC1, PC2, PC3) não têm unidade nem significado econômico: só a "
        "distância entre os pontos importa.",
    },
    # ----------------------------------------------------------------------- comparar
    "comparar": {
        "o_que": "Os perfis médios de várias famílias no mesmo gráfico.",
        "como_ler": [
            "Linhas que sobem e descem juntas indicam famílias com o mesmo ritmo.",
            "As faixas cinza são recessões: veja quais famílias reagem a elas.",
            "**Suavizar** mostra a tendência; **Ampliar** esconde picos extremos como 2020.",
        ],
        "cuidado": "O gráfico mostra variações mensais padronizadas, não os valores dos "
        "indicadores. Duas famílias podem ter perfis parecidos e significar coisas diferentes.",
    },
    "comparar_corr": {
        "o_que": "O quanto os perfis de cada par de famílias se parecem, de -1 a 1.",
        "como_ler": [
            "Azul escuro = andam juntas; vermelho = em sentidos opostos; branco = sem relação.",
            "A diagonal é sempre 1: cada família é idêntica a si mesma.",
        ],
        "cuidado": "As famílias foram formadas para serem diferentes entre si. Correlação alta "
        "entre duas delas mostra que partilham o mesmo ciclo da economia, não que o agrupamento "
        "esteja errado.",
    },
    # ------------------------------------------------------------------------ séries
    "series_par": {
        "o_que": "Dois indicadores na mesma escala e, embaixo, o quanto andam juntos em cada época.",
        "como_ler": [
            "A linha de baixo (correlação móvel) vai de -1 a 1: perto de 1, os dois estão alinhados "
            "naquele período; perto de 0, não há relação; negativa, vão em sentidos opostos.",
            "Ela pode mudar com o tempo: duas séries parecidas hoje podem não ter sido no passado.",
        ],
        "cuidado": "Andar junto não é causar. Dois indicadores podem reagir a um terceiro fator, "
        "como o ciclo da economia. Os dados são variações mensais, não níveis.",
    },
    "series_heat": {
        "o_que": "Uma grade que compara todas as séries entre si, duas a duas.",
        "como_ler": [
            "Azul = andam juntas; vermelho = em sentidos opostos; branco = sem relação.",
            "Séries ordenadas por família: os blocos azuis na diagonal são as próprias famílias.",
        ],
        "cuidado": "A semelhança medida é a contemporânea, de um mesmo mês. Efeitos que demoram "
        "meses para aparecer não entram aqui.",
    },
    # -------------------------------------------------------------------------- rede
    "rede": {
        "o_que": "Cada bolinha é uma série; cada fio liga duas séries que andam muito juntas.",
        "como_ler": [
            "Fio entre bolinhas da mesma cor = ligação dentro da família (o esperado).",
            "“Vezes mais comum dentro” compara a frequência de fios dentro das famílias com a de "
            "fios entre famílias: quanto maior, mais coeso é o agrupamento.",
            "Fios **verdes** ligam séries que andam juntas; **vermelhos**, séries opostas.",
        ],
        "cuidado": "A posição das bolinhas não tem significado econômico, só os fios. Muitos fios "
        "entre famílias diferentes mostram que a economia tem fatores comuns a vários setores.",
    },
    # ------------------------------------------------------------------ estabilidade
    "boot": {
        "o_que": "Se a família se repete quando refazemos o agrupamento com os meses embaralhados.",
        "como_ler": [
            "O **Jaccard** vai de 0 a 1: 1 = a família reaparece idêntica; 0,5 = metade das séries "
            "reaparece juntas; perto de 0 = a família se desfaz.",
            "Reamostramos blocos de 12 meses, para preservar a persistência dos dados, e refizemos "
            "o agrupamento 500 vezes.",
            "As barras de erro mostram o quanto o resultado varia de uma reamostragem para outra.",
        ],
        "cuidado": "Jaccard médio entre 0,4 e 0,7 é estabilidade moderada: os achados dizem algo "
        "real, mas a composição exata de cada família pode mudar. Isso deve ser dito junto com "
        "o resultado.",
    },
    "ward": {
        "o_que": "A comparação com um segundo método de agrupamento (hierárquico de Ward).",
        "como_ler": [
            "**ARI** mede a concordância entre os dois agrupamentos: 0 = como ao acaso, 1 = idênticos. "
            "**NMI** é parecido, de 0 a 1.",
            "No dendrograma, cada folha é uma série colorida pela família do K-Means; cores iguais "
            "juntas indicam que os dois métodos concordam.",
        ],
        "cuidado": "Dois métodos nunca concordam em tudo. O que importa é se os achados aparecem "
        "nos dois. Mudar o corte do dendrograma muda o número de grupos e o ARI.",
    },
    "what_if": {
        "o_que": "O que aconteceria com as famílias se usássemos outro número de grupos (k).",
        "como_ler": [
            "ARI e NMI comparam o novo agrupamento com o oficial (k = 19).",
            "A **silhueta** vai de -1 a 1: acima de 0,5 = grupos bem separados; abaixo de 0,25 = "
            "grupos que se sobrepõem bastante.",
        ],
        "cuidado": "Exploratório: o k do estudo foi fixado antes de olhar os resultados. Escolher "
        "outro k depois de ver o resultado seria ajustar a análise ao gosto. Aqui a silhueta fica "
        "perto de 0,19: as famílias se sobrepõem em parte, algo comum em dados econômicos.",
    },
    # ---------------------------------------------------------------------- regressão
    "regressao_mapa": {
        "o_que": "A mesma análise da página Variáveis de referência, com os números e níveis de confiança.",
        "como_ler": [
            "O número é o coeficiente: quanto a família muda (em desvios-padrão) quando o "
            "indicador muda 1 desvio-padrão. O asterisco marca relação estatisticamente convincente.",
            "“Só significativos” esconde o que não passou no teste.",
        ],
        "cuidado": "Significativo não é o mesmo que importante: com muitos meses, até efeitos "
        "pequenos passam no teste. Olhe também o tamanho do coeficiente.",
    },
    "regressao_vivo": {
        "o_que": "A regressão refeita aqui, com os indicadores e o período que você escolher.",
        "como_ler": [
            "Com os 6 indicadores e período a partir de 02/1973, o resultado é o da análise principal.",
            "Os resíduos (gráfico de baixo) mostram o que a regressão não explicou; a ACF mede se "
            "eles têm memória.",
        ],
        "cuidado": "Mudar indicadores ou período depois de ver o resultado é exploração, não "
        "teste. O resultado oficial é o fixado antes, no notebook.",
    },
}

FAQ: list[tuple[str, str]] = [
    (
        "Isso serve para prever a economia?",
        "Não. O estudo organiza e descreve: mostra quais indicadores se movem juntos e a quais "
        "referências cada grupo responde. Não faz previsões.",
    ),
    (
        "Qual a diferença entre categoria e família?",
        "Categoria é a etiqueta oficial do FRED-MD (ex.: “Preços”, “Mercado de trabalho”), feita "
        "por especialistas. Família é o grupo que os dados formaram sozinhos, por comportamento "
        "parecido. Uma família pode misturar categorias.",
    ),
    (
        "Por que usar a variação mensal e não o valor do indicador?",
        "Porque muitos indicadores crescem com o tempo (como os preços) e isso faria quase tudo "
        "parecer ligado a tudo. A variação mensal remove essa tendência e compara o que realmente "
        "muda. Em economia isso se chama tornar a série estacionária.",
    ),
    (
        "O que significa explicar “48% do vai e vem”?",
        "É o R². Se os seis indicadores de referência explicam 48% da oscilação de uma família, "
        "os outros 52% vêm de fatores que o estudo não mede. 0% = nada, 100% = tudo.",
    ),
    (
        "Por que 19 famílias?",
        "O número não foi escolhido à mão. Foi o menor que preserva 70% da informação dos dados, "
        "um critério definido antes de ver os resultados.",
    ),
    (
        "O que é um “achado genuíno” e o que é “conferência do método”?",
        "Achado genuíno é uma relação forte e que não vem da forma como as séries são construídas. "
        "Conferência do método é uma relação forte, mas óbvia (ex.: subíndices da produção "
        "industrial acompanham a produção industrial). Elas mostram que o método funciona.",
    ),
    (
        "Os resultados são definitivos?",
        "São resultados preliminares, de um trabalho em andamento. A estabilidade dos grupos é "
        "moderada, os achados são associações (não provas de causa) e há uma limitação conhecida "
        "na preparação dos dados, descrita na página Metodologia.",
    ),
]

CLASSE_EXPLICACAO: dict[str, str] = {
    "Achado genuíno": "Relação forte com um indicador de referência e que **não** vem da forma "
    "como as séries são construídas: é uma informação nova.",
    "Sanidade: mesma família": "Relação forte, mas **óbvia**: as séries da família são subíndices "
    "do próprio indicador. Serve para conferir que o método funciona.",
    "Sanidade: construção": "Relação forte, mas **óbvia pela fórmula**: as séries e o indicador "
    "compartilham o mesmo cálculo. Também é conferência do método.",
    "Fraco (R² ≤ 0,4)": "Nenhum dos seis indicadores de referência explica bem esta família. "
    "Isso é um resultado possível, não um defeito.",
}
