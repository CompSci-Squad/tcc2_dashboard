"""Catálogo em português: o que cada série do FRED-MD mede e em qual categoria oficial ela cai.

As 8 categorias seguem o Apêndice de McCracken & Ng (2016). Cada entrada é (descrição, categoria).
"""

from __future__ import annotations

PROD = "Produção e renda"
TRAB = "Mercado de trabalho"
HAB = "Habitação"
CONS = "Consumo e estoques"
MOEDA = "Moeda e crédito"
JUROS = "Juros e câmbio"
PRECOS = "Preços"
BOLSA = "Bolsa de valores"

CATEGORIAS = [PROD, TRAB, HAB, CONS, MOEDA, JUROS, PRECOS, BOLSA]

CATEGORIA_COR = {
    PROD: "#4F46E5",
    TRAB: "#0EA5E9",
    HAB: "#F59E0B",
    CONS: "#10B981",
    MOEDA: "#8B5CF6",
    JUROS: "#E11D48",
    PRECOS: "#F97316",
    BOLSA: "#64748B",
}

SERIES: dict[str, tuple[str, str]] = {
    # --- Produção e renda
    "RPI": ("Renda pessoal real das famílias", PROD),
    "W875RX1": ("Renda pessoal real, sem transferências do governo", PROD),
    "INDPRO": ("Produção industrial (índice geral)", PROD),
    "IPFPNSS": ("Produção industrial: produtos finais e suprimentos", PROD),
    "IPFINAL": ("Produção industrial: produtos finais", PROD),
    "IPCONGD": ("Produção industrial: bens de consumo", PROD),
    "IPDCONGD": ("Produção industrial: bens de consumo duráveis", PROD),
    "IPNCONGD": ("Produção industrial: bens de consumo não duráveis", PROD),
    "IPBUSEQ": ("Produção industrial: equipamentos para empresas", PROD),
    "IPMAT": ("Produção industrial: materiais", PROD),
    "IPDMAT": ("Produção industrial: materiais duráveis", PROD),
    "IPNMAT": ("Produção industrial: materiais não duráveis", PROD),
    "IPMANSICS": ("Produção industrial: manufatura", PROD),
    "IPB51222S": ("Produção industrial: eletricidade e gás residenciais", PROD),
    "IPFUELS": ("Produção industrial: combustíveis", PROD),
    "CUMFNS": ("Uso da capacidade instalada na manufatura", PROD),
    # --- Mercado de trabalho
    "HWI": ("Índice de anúncios de vagas de emprego", TRAB),
    "HWIURATIO": ("Vagas anunciadas por desempregado", TRAB),
    "CLF16OV": ("Força de trabalho (pessoas empregadas ou procurando emprego)", TRAB),
    "CE16OV": ("Pessoas empregadas", TRAB),
    "UNRATE": ("Taxa de desemprego", TRAB),
    "UEMPMEAN": ("Duração média do desemprego", TRAB),
    "UEMPLT5": ("Desempregados há menos de 5 semanas", TRAB),
    "UEMP5TO14": ("Desempregados há 5 a 14 semanas", TRAB),
    "UEMP15OV": ("Desempregados há 15 semanas ou mais", TRAB),
    "UEMP15T26": ("Desempregados há 15 a 26 semanas", TRAB),
    "UEMP27OV": ("Desempregados há 27 semanas ou mais", TRAB),
    "CLAIMSx": ("Pedidos novos de seguro-desemprego", TRAB),
    "PAYEMS": ("Total de empregos fora da agricultura", TRAB),
    "USGOOD": ("Empregos na produção de bens", TRAB),
    "CES1021000001": ("Empregos em mineração e extração", TRAB),
    "USCONS": ("Empregos na construção civil", TRAB),
    "MANEMP": ("Empregos na manufatura", TRAB),
    "DMANEMP": ("Empregos na manufatura de bens duráveis", TRAB),
    "NDMANEMP": ("Empregos na manufatura de bens não duráveis", TRAB),
    "SRVPRD": ("Empregos em serviços", TRAB),
    "USTPU": ("Empregos em comércio, transporte e utilidades", TRAB),
    "USWTRADE": ("Empregos no comércio atacadista", TRAB),
    "USTRADE": ("Empregos no comércio varejista", TRAB),
    "USFIRE": ("Empregos em finanças, seguros e imóveis", TRAB),
    "USGOVT": ("Empregos no governo", TRAB),
    "CES0600000007": ("Horas semanais trabalhadas na produção de bens", TRAB),
    "AWOTMAN": ("Horas extras semanais na manufatura", TRAB),
    "AWHMAN": ("Horas semanais trabalhadas na manufatura", TRAB),
    "CES0600000008": ("Salário por hora na produção de bens", TRAB),
    "CES2000000008": ("Salário por hora na construção civil", TRAB),
    "CES3000000008": ("Salário por hora na manufatura", TRAB),
    # --- Habitação
    "HOUST": ("Início de construção de moradias (EUA)", HAB),
    "HOUSTNE": ("Início de construção de moradias: Nordeste", HAB),
    "HOUSTMW": ("Início de construção de moradias: Centro-Oeste", HAB),
    "HOUSTS": ("Início de construção de moradias: Sul", HAB),
    "HOUSTW": ("Início de construção de moradias: Oeste", HAB),
    "PERMIT": ("Licenças para construir moradias (EUA)", HAB),
    "PERMITNE": ("Licenças para construir moradias: Nordeste", HAB),
    "PERMITMW": ("Licenças para construir moradias: Centro-Oeste", HAB),
    "PERMITS": ("Licenças para construir moradias: Sul", HAB),
    "PERMITW": ("Licenças para construir moradias: Oeste", HAB),
    # --- Consumo e estoques
    "DPCERA3M086SBEA": ("Consumo real das famílias", CONS),
    "CMRMTSPLx": ("Vendas reais da indústria e do comércio", CONS),
    "RETAILx": ("Vendas reais no varejo", CONS),
    "UMCSENTx": ("Confiança do consumidor (Univ. de Michigan)", CONS),
    "ACOGNO": ("Novos pedidos de bens de consumo", CONS),
    "AMDMNOx": ("Novos pedidos de bens duráveis", CONS),
    "ANDENOx": ("Novos pedidos de bens de capital", CONS),
    "AMDMUOx": ("Pedidos de bens duráveis ainda não atendidos", CONS),
    "BUSINVx": ("Estoques totais das empresas", CONS),
    "ISRATIOx": ("Estoques em relação às vendas", CONS),
    # --- Moeda e crédito
    "M1SL": ("Dinheiro em circulação e depósitos à vista (M1)", MOEDA),
    "M2SL": ("Oferta de moeda ampla (M2)", MOEDA),
    "M2REAL": ("Oferta de moeda ampla (M2), descontada a inflação", MOEDA),
    "BOGMBASE": ("Base monetária", MOEDA),
    "TOTRESNS": ("Reservas totais dos bancos", MOEDA),
    "NONBORRES": ("Reservas dos bancos que não vieram de empréstimo do Fed", MOEDA),
    "BUSLOANS": ("Empréstimos dos bancos às empresas", MOEDA),
    "REALLN": ("Empréstimos dos bancos para imóveis", MOEDA),
    "NONREVSL": ("Crédito ao consumidor não rotativo", MOEDA),
    "CONSPI": ("Dívida do consumidor em relação à renda", MOEDA),
    "DTCOLNVHFNM": ("Financiamento de veículos pelas famílias", MOEDA),
    "DTCTHFNM": ("Total de empréstimos e arrendamentos ao consumidor", MOEDA),
    "INVEST": ("Títulos e investimentos em poder dos bancos", MOEDA),
    # --- Juros e câmbio
    "FEDFUNDS": ("Taxa básica de juros dos EUA (Fed Funds)", JUROS),
    "CP3Mx": ("Juros do papel comercial de 3 meses", JUROS),
    "TB3MS": ("Juros do título do Tesouro de 3 meses", JUROS),
    "TB6MS": ("Juros do título do Tesouro de 6 meses", JUROS),
    "GS1": ("Juros do título do Tesouro de 1 ano", JUROS),
    "GS5": ("Juros do título do Tesouro de 5 anos", JUROS),
    "GS10": ("Juros do título do Tesouro de 10 anos", JUROS),
    "AAA": ("Juros de títulos de empresas de risco baixo (AAA)", JUROS),
    "BAA": ("Juros de títulos de empresas de risco maior (BAA)", JUROS),
    "COMPAPFFx": ("Papel comercial de 3 meses menos a taxa básica", JUROS),
    "TB3SMFFM": ("Tesouro de 3 meses menos a taxa básica", JUROS),
    "TB6SMFFM": ("Tesouro de 6 meses menos a taxa básica", JUROS),
    "T1YFFM": ("Tesouro de 1 ano menos a taxa básica", JUROS),
    "T5YFFM": ("Tesouro de 5 anos menos a taxa básica", JUROS),
    "T10YFFM": ("Tesouro de 10 anos menos a taxa básica (inclinação da curva de juros)", JUROS),
    "AAAFFM": ("Título AAA menos a taxa básica", JUROS),
    "BAAFFM": ("Título BAA menos a taxa básica", JUROS),
    "TWEXAFEGSMTHx": ("Câmbio: valor do dólar frente às moedas dos parceiros comerciais", JUROS),
    "EXSZUSx": ("Câmbio: francos suíços por dólar", JUROS),
    "EXJPUSx": ("Câmbio: ienes por dólar", JUROS),
    "EXUSUKx": ("Câmbio: dólares por libra esterlina", JUROS),
    "EXCAUSx": ("Câmbio: dólares canadenses por dólar", JUROS),
    # --- Preços
    "WPSFD49207": ("Preços ao produtor: bens finais", PRECOS),
    "WPSFD49502": ("Preços ao produtor: bens de consumo finais", PRECOS),
    "WPSID61": ("Preços ao produtor: insumos intermediários", PRECOS),
    "WPSID62": ("Preços ao produtor: matérias-primas", PRECOS),
    "OILPRICEx": ("Preço do petróleo", PRECOS),
    "PPICMM": ("Preços ao produtor: metais", PRECOS),
    "CPIAUCSL": ("Inflação ao consumidor (índice de preços CPI)", PRECOS),
    "CPIAPPSL": ("Preços ao consumidor: vestuário", PRECOS),
    "CPITRNSL": ("Preços ao consumidor: transporte", PRECOS),
    "CPIMEDSL": ("Preços ao consumidor: saúde", PRECOS),
    "CUSR0000SAC": ("Preços ao consumidor: bens", PRECOS),
    "CUUR0000SAD": ("Preços ao consumidor: bens duráveis", PRECOS),
    "CUSR0000SAD": ("Preços ao consumidor: bens duráveis", PRECOS),
    "CUSR0000SAS": ("Preços ao consumidor: serviços", PRECOS),
    "CPIULFSL": ("Preços ao consumidor: tudo menos alimentos", PRECOS),
    "CUSR0000SA0L2": ("Preços ao consumidor: tudo menos moradia", PRECOS),
    "CUSR0000SA0L5": ("Preços ao consumidor: tudo menos saúde", PRECOS),
    "PCEPI": ("Preços do consumo pessoal (índice PCE)", PRECOS),
    "DDURRG3M086SBEA": ("Preços do consumo pessoal: bens duráveis", PRECOS),
    "DNDGRG3M086SBEA": ("Preços do consumo pessoal: bens não duráveis", PRECOS),
    "DSERRG3M086SBEA": ("Preços do consumo pessoal: serviços", PRECOS),
    # --- Bolsa
    "S&P 500": ("Bolsa de valores: índice S&P 500", BOLSA),
    "S&P: indust": ("Bolsa de valores: índice S&P das indústrias", BOLSA),
    "S&P div yield": ("Bolsa: dividendos pagos em relação ao preço das ações", BOLSA),
    "S&P PE ratio": ("Bolsa: preço das ações em relação ao lucro", BOLSA),
    "VIXCLSx": ("Índice de medo do mercado (volatilidade VIX)", BOLSA),
}

# Variáveis de referência usadas na regressão, em linguagem de todo dia
REFERENCIAS: dict[str, dict[str, str]] = {
    "INDPRO": {
        "nome": "Produção industrial",
        "o_que": "Quanto as fábricas, minas e usinas dos EUA estão produzindo.",
        "por_que": "É o termômetro mais usado da atividade real: sobe nas expansões e cai nas recessões.",
        "sobe": "a produção industrial sobe",
    },
    "CPIAUCSL": {
        "nome": "Inflação ao consumidor",
        "o_que": "Quanto os preços que as famílias pagam estão subindo.",
        "por_que": "Mostra o custo de vida e pesa nas decisões do banco central.",
        "sobe": "a inflação sobe",
    },
    "FEDFUNDS": {
        "nome": "Taxa básica de juros",
        "o_que": "A taxa de juros de referência definida pelo banco central dos EUA (Fed).",
        "por_que": "Todos os outros juros da economia se ajustam a ela, cedo ou tarde.",
        "sobe": "a taxa básica de juros sobe",
    },
    "T10YFFM": {
        "nome": "Inclinação da curva de juros",
        "o_que": "A diferença entre os juros de longo prazo (10 anos) e a taxa básica.",
        "por_que": "Quando fica negativa, historicamente antecede recessões.",
        "sobe": "a inclinação da curva de juros sobe",
    },
    "S&P 500": {
        "nome": "Bolsa de valores",
        "o_que": "A variação mensal do índice S&P 500, que reúne as 500 maiores empresas listadas.",
        "por_que": "Reflete as expectativas dos investidores sobre a economia.",
        "sobe": "a bolsa sobe",
    },
    "TWEXAFEGSMTHx": {
        "nome": "Câmbio (valor do dólar)",
        "o_que": "A variação do valor do dólar frente às moedas dos principais parceiros comerciais.",
        "por_que": "Afeta exportações, importações e o preço de tudo que cruza a fronteira.",
        "sobe": "o dólar se valoriza",
    },
}

# Frase de leitura escrita à mão para cada achado genuíno (cada uma checada contra os números)
ACHADOS: dict[int, dict[str, str]] = {
    3: {
        "titulo": "Desemprego de curto prazo e crédito às empresas",
        "leitura": (
            "Quando a produção industrial cresce, os pedidos de seguro-desemprego, o desemprego "
            "de curta duração e os empréstimos às empresas tendem a recuar."
        ),
    },
    4: {
        "titulo": "Juros de mercado e custo do crédito",
        "leitura": (
            "Os juros dos títulos do Tesouro, do papel comercial e das empresas andam junto com "
            "a taxa básica definida pelo banco central."
        ),
    },
    14: {
        "titulo": "Emprego e consumo em geral",
        "leitura": (
            "A maior família do estudo (24 séries de empregos, consumo e vendas) sobe e desce "
            "junto com a produção industrial: é a economia real se movendo em bloco."
        ),
    },
    18: {
        "titulo": "Câmbio e reservas dos bancos",
        "leitura": (
            "O valor do dólar é o único indicador que acompanha este grupo, e explica cerca de três "
            "quartos do seu vai e vem. Ele reúne taxas de câmbio (iene, franco suíço, dólar "
            "canadense) e reservas bancárias."
        ),
    },
}

GLOSSARIO: dict[str, str] = {
    "Série": "Um indicador medido todo mês, como a taxa de desemprego. É o que o estudo agrupa.",
    "Cluster (família)": "Grupo de séries que sobem e descem nos mesmos momentos.",
    "Centróide": "O perfil médio de uma família: a média das suas séries, mês a mês.",
    "Variável de referência": "Um indicador conhecido (produção, inflação, juros, bolsa, câmbio) "
    "usado como régua para entender o que move cada família.",
    "R²": "Quanto do vai e vem de uma família é explicado pela variável de referência. "
    "0% = nada, 100% = tudo.",
    "Padronização": "Colocar todas as séries na mesma escala para poderem ser comparadas.",
    "Achado genuíno": "Relação que não é óbvia só olhando como as séries são construídas.",
    "Sanidade do método": "Relação óbvia (ex.: sub-índices da produção industrial acompanham a "
    "produção industrial) que serve para conferir se o método funciona.",
}


def nome(serie: str) -> str:
    return SERIES.get(serie, (serie, ""))[0]


def categoria(serie: str) -> str:
    return SERIES.get(serie, ("", "Outras"))[1]


def rotulo(serie: str) -> str:
    """Código + descrição, para listas e seletores."""
    n = nome(serie)
    return serie if n == serie else f"{serie} · {n}"
