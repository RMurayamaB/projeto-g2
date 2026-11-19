# Violência letal, roubos de rua e pandemia no Estado do Rio de Janeiro (2014–2020)

[![Licença: MIT](https://img.shields.io/badge/código-MIT-blue.svg)](LICENSE)
[![Licença: CC BY 4.0](https://img.shields.io/badge/dados%20e%20texto-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.pt-br)
![Python](https://img.shields.io/badge/python-3.12-informational)
[![Artigo](https://img.shields.io/badge/artigo-GitHub%20Pages-success)](https://SEU-USUARIO.github.io/NOME-DO-REPO/)

**Autores:** [Nome 1], [Nome 2], [Nome 3]
**Instituição:** [Instituição] — Bacharelado em Sistemas de Informação, 6º período
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python) — [semestre/ano]
**Professor orientador:** [Nome completo]

## Resumo
Pipeline reprodutível em Python que trata as séries históricas anual e mensal de indicadores criminais
do ISP-RJ (taxas por 100 mil habitantes) e responde a três perguntas de pesquisa:

- **RQ1** — Como evoluíram a letalidade violenta e as mortes por intervenção policial por região (2014–2020)?
- **RQ2** — Municípios com mais roubos de rua têm maior letalidade violenta?
- **RQ3** — Qual foi o efeito da pandemia de 2020 sobre roubos, furtos e letalidade em relação ao padrão sazonal de 2014–2019?

**Palavras-chave:** segurança pública; letalidade violenta; intervenção policial; roubos de rua; COVID-19; Rio de Janeiro.

## Fonte dos dados
Instituto de Segurança Pública do Estado do Rio de Janeiro (ISP-RJ) — Dados Abertos:
<https://www.ispdados.rj.gov.br/estatistica.html>
Arquivos: *Série histórica anual por município desde 2014* e *Série histórica mensal por município desde 01/2014* (taxas por 100 mil habitantes).

## Estrutura
```
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── raw/                  # CSVs originais do ISP (não modificados)
│   ├── processed/            # dados tratados (.csv.gz)
│   └── data_dictionary.md
├── notebooks/analise_exploratoria.ipynb
├── src/
│   ├── etl.py                # leitura, limpeza, métricas derivadas
│   └── analise.py            # agregações, testes e figuras (Plotly)
└── docs/                     # artigo (GitHub Pages)
    ├── index.html
    └── assets/               # figuras interativas e tabelas exportadas
```

## Como reproduzir
```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPO.git
cd NOME-DO-REPO
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.etl                # gera data/processed/
python -m src.analise            # gera docs/assets/ (figuras e tabelas)
jupyter notebook notebooks/analise_exploratoria.ipynb
```
No VS Code, selecione como kernel do notebook o mesmo ambiente Python em que as dependências foram instaladas. Se o Plotly ainda informar que `nbformat` está ausente, execute `python -m pip install -r requirements.txt` nesse ambiente e reinicie o kernel.

## Publicação (GitHub Pages)
*Settings → Pages → Source: Deploy from a branch → Branch `main`, pasta `/docs`.*

## Licenças
Código: **MIT**. Dados processados e texto do artigo: **CC BY 4.0**. Dados brutos: ISP-RJ.
