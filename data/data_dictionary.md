# Dicionário de Dados

**Fonte:** Instituto de Segurança Pública do Estado do Rio de Janeiro (ISP-RJ) – Dados Abertos (<https://www.ispdados.rj.gov.br/>).
**Unidade das taxas:** ocorrências registradas por 100 mil habitantes do município.
**Licença dos dados processados:** CC BY 4.0.

## Arquivos

| Arquivo | Granularidade | Período | Linhas | Formato |
|---|---|---|---|---|
| `raw/isp_anual_municipio_2014_2020.csv` | município × ano | 2014–2020 | 644 | CSV latin-1, `;`, decimal `,`, ausente `-` |
| `raw/isp_mensal_municipio_2014_2026.csv` | município × mês | jan/2014–jul/2026 | 13.892 | CSV latin-1, `;`, decimal `,` |
| `processed/isp_anual_tratado.csv.gz` | município × ano | 2014–2020 | 266 (38 municípios) | CSV UTF-8, `,`, decimal `.` |
| `processed/isp_mensal_tratado.csv.gz` | município × mês | jan/2014–jul/2026 | 13.892 (92 municípios) | CSV UTF-8, `,`, decimal `.` |

## Variáveis de identificação

| Variável | Tipo | Formato | Descrição |
|---|---|---|---|
| `fmun_cod` | int64 | 7 dígitos | Código IBGE do município |
| `fmun` | string | texto | Nome do município |
| `ano` | int64 | AAAA | Ano de referência |
| `mes` | int64 | 1–12 | Mês (somente série mensal) |
| `mes_ano` | string | `AAAAmMM` | Rótulo original do mês (somente mensal) |
| `regiao` | category | Capital / Baixada Fluminense / Grande Niterói / Interior | Região de agregação do ISP |
| `fase` | int64 | 3 | Fase de validação dos dados (somente anual; 3 = consolidado) |

## Variáveis derivadas (criadas no ETL)

| Variável | Tipo | Descrição |
|---|---|---|
| `data` | datetime | Primeiro dia do mês (`ano`, `mes`) – série mensal |
| `periodo` | category | `pré-pandemia` (até fev/2020), `pandemia (mar/20–dez/21)`, `pós-pandemia` |
| `pct_interv_policial` | float64 | % da letalidade violenta atribuída a morte por intervenção de agente do Estado; nulo quando `letalidade_violenta` = 0 |

## Indicadores (float64, taxa por 100 mil hab.)

| Variável | Significado |
|---|---|
| `hom_doloso` | Homicídio doloso |
| `lesao_corp_morte` | Lesão corporal seguida de morte |
| `latrocinio` | Roubo seguido de morte |
| `cvli` | Crimes violentos letais intencionais (hom. doloso + lesão c/ morte + latrocínio) |
| `hom_por_interv_policial` | Morte por intervenção de agente do Estado |
| `feminicidio` / `tentativa_feminicidio` | Feminicídio e tentativa (somente mensal; nulo antes da tipificação nos registros) |
| `letalidade_violenta` | CVLI + morte por intervenção de agente do Estado |
| `tentat_hom` | Tentativa de homicídio |
| `lesao_corp_dolosa` / `lesao_corp_culposa` | Lesão corporal dolosa / culposa |
| `estupro` | Estupro |
| `hom_culposo` | Homicídio culposo |
| `roubo_transeunte`, `roubo_celular`, `roubo_em_coletivo` | Roubos a transeunte, de celular e em coletivo |
| `roubo_rua` | Roubos de rua (soma dos três acima) |
| `roubo_veiculo` | Roubo de veículo (somente mensal) |
| `roubo_carga`, `roubo_comercio`, `roubo_residencia`, `roubo_banco`, `roubo_cx_eletronico`, `roubo_conducao_saque`, `roubo_apos_saque`, `roubo_bicicleta`, `outros_roubos` | Demais modalidades de roubo |
| `total_roubos` | Total de roubos |
| `furto_veiculos`, `furto_transeunte`, `furto_coletivo`, `furto_celular`, `furto_bicicleta`, `outros_furtos` | Modalidades de furto |
| `total_furtos` | Total de furtos |
| `sequestro`, `extorsao`, `sequestro_relampago`, `estelionato` | Crimes contra o patrimônio/liberdade |
| `apreensao_drogas`, `posse_drogas`, `trafico_drogas`, `apreensao_drogas_sem_autor` | Ocorrências com drogas |
| `recuperacao_veiculos` | Veículos recuperados |
| `apf` | Autos de prisão em flagrante |
| `aaapai` | Autos de apreensão de adolescente por ato infracional |
| `cmp` / `cmba` | Cumprimento de mandado de prisão / de busca e apreensão de adolescente |
| `ameaca` | Ameaça |
| `pessoas_desaparecidas`, `encontro_cadaver`, `encontro_ossada` | Desaparecimentos e encontros de cadáver/ossada |
| `pol_militares_mortos_serv`, `pol_civis_mortos_serv` | Policiais militares/civis mortos em serviço |
| `registro_ocorrencias` | Total de registros de ocorrência (somente anual) |

## Tratamentos aplicados

1. Leitura com `encoding="latin-1"`, `sep=";"`, `decimal=","`; o símbolo `-` é convertido em nulo (`NaN`).
2. Na série anual, **54 municípios** do Interior não têm nenhum indicador publicado (todas as colunas `-`) em 2014–2020; essas linhas são **descartadas** e o descarte é registrado em log. Restam 38 municípios.
3. Na série mensal não há descarte; nulos restantes estão apenas em `feminicidio`, `tentativa_feminicidio` e nas colunas de policiais mortos, que não são usadas nas análises.
4. Os arquivos brutos nunca são sobrescritos.
