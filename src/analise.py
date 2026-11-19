"""Métricas agregadas e figuras para as perguntas de pesquisa (RQ1–RQ3)."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
PROC, ASSETS = ROOT / "data" / "processed", ROOT / "docs" / "assets"
REGIOES = ["Capital", "Baixada Fluminense", "Grande Niterói", "Interior"]
CORES = dict(zip(REGIOES, ["#1f4e79", "#c0392b", "#e67e22", "#27ae60"]))
TEMA = dict(template="plotly_white", font=dict(family="Georgia, serif", size=13))


def carregar():
    anual = pd.read_csv(PROC / "isp_anual_tratado.csv.gz")
    mensal = pd.read_csv(PROC / "isp_mensal_tratado.csv.gz", parse_dates=["data"])
    return anual, mensal


# ---------------- RQ1 ----------------
def rq1_tabela(anual):
    """Média (não ponderada) das taxas municipais por região e ano."""
    return (anual.groupby(["regiao", "ano"], observed=True)
            [["letalidade_violenta", "hom_por_interv_policial", "cvli"]].mean().round(2).reset_index())


def rq1_figura(t):
    long = t.melt(id_vars=["regiao", "ano"], value_vars=["letalidade_violenta", "hom_por_interv_policial"],
                  var_name="indicador", value_name="taxa")
    long["indicador"] = long["indicador"].map({"letalidade_violenta": "Letalidade violenta",
                                               "hom_por_interv_policial": "Morte por intervenção policial"})
    fig = px.line(long, x="ano", y="taxa", color="regiao", facet_col="indicador", markers=True,
                  color_discrete_map=CORES, category_orders={"regiao": REGIOES},
                  labels={"taxa": "Taxa por 100 mil hab.", "ano": "Ano", "regiao": "Região"})
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.update_layout(height=430, legend=dict(orientation="h", y=-0.2), **TEMA)
    return fig


# ---------------- RQ2 ----------------
def rq2_base(anual):
    return (anual.groupby(["fmun", "regiao"], observed=True)
            [["roubo_rua", "letalidade_violenta", "total_roubos"]].mean().reset_index())


def rq2_correlacoes(base):
    linhas = []
    for nome, g in [("Todos", base)] + [(r, base[base.regiao == r]) for r in REGIOES]:
        if len(g) >= 3:
            rho, p = stats.spearmanr(g["roubo_rua"], g["letalidade_violenta"])
            r, pp = stats.pearsonr(g["roubo_rua"], g["letalidade_violenta"])
            linhas.append(dict(grupo=nome, n=len(g), pearson_r=round(r, 3), p_pearson=round(pp, 4),
                               spearman_rho=round(rho, 3), p_spearman=round(p, 4)))
    return pd.DataFrame(linhas)


def rq2_figura(base):
    fig = px.scatter(base, x="roubo_rua", y="letalidade_violenta", color="regiao", hover_name="fmun",
                     trendline="ols", trendline_scope="overall", trendline_color_override="#555",
                     color_discrete_map=CORES, category_orders={"regiao": REGIOES},
                     labels={"roubo_rua": "Roubos de rua (média 2014–2020, por 100 mil)",
                             "letalidade_violenta": "Letalidade violenta (média 2014–2020, por 100 mil)",
                             "regiao": "Região"})
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color="white")), selector=dict(mode="markers"))
    fig.update_layout(height=470, **TEMA)
    return fig


# ---------------- RQ3 ----------------
IND_RQ3 = {"roubo_rua": "Roubos de rua", "total_furtos": "Total de furtos",
           "letalidade_violenta": "Letalidade violenta"}


def rq3_tabela(mensal):
    """Desvio % de cada mês de 2020 vs. média do mesmo mês em 2014–2019 (média estadual dos municípios)."""
    est = mensal.groupby(["ano", "mes"])[list(IND_RQ3)].mean().reset_index()
    base = est[est.ano.between(2014, 2019)].groupby("mes")[list(IND_RQ3)].mean()
    a2020 = est[est.ano == 2020].set_index("mes")[list(IND_RQ3)]
    return ((a2020 / base - 1) * 100).round(1)


def rq3_figura(mensal):
    est = mensal[mensal.ano.between(2014, 2020)].groupby(["ano", "mes"])[list(IND_RQ3)].mean().reset_index()
    base = est[est.ano <= 2019].groupby("mes")[list(IND_RQ3)].agg(["mean", "min", "max"])
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=3, subplot_titles=list(IND_RQ3.values()))
    for i, (c, nome) in enumerate(IND_RQ3.items(), start=1):
        fig.add_trace(go.Scatter(x=meses + meses[::-1], y=list(base[(c, "max")]) + list(base[(c, "min")])[::-1],
                                 fill="toself", fillcolor="rgba(31,78,121,.15)", line=dict(width=0),
                                 name="Faixa 2014–2019", showlegend=i == 1, hoverinfo="skip"), 1, i)
        fig.add_trace(go.Scatter(x=meses, y=base[(c, "mean")], line=dict(color="#1f4e79", dash="dash"),
                                 name="Média 2014–2019", showlegend=i == 1), 1, i)
        fig.add_trace(go.Scatter(x=meses, y=est[est.ano == 2020][c], line=dict(color="#c0392b", width=3),
                                 name="2020", showlegend=i == 1), 1, i)
    fig.add_vrect(x0="mar", x1="mai", fillcolor="gray", opacity=.08, line_width=0, row="all", col="all")
    fig.update_yaxes(title_text="Taxa mensal por 100 mil", col=1)
    fig.update_layout(height=420, legend=dict(orientation="h", y=-0.15), **TEMA)
    return fig


def serie_longa_figura(mensal):
    s = mensal.groupby("data")[["roubo_rua", "letalidade_violenta"]].mean().rolling(12).mean().dropna().reset_index()
    fig = px.line(s, x="data", y=["roubo_rua", "letalidade_violenta"],
                  labels={"value": "Taxa mensal (média móvel 12m)", "data": "", "variable": "Indicador"})
    fig.add_vrect(x0="2020-03-01", x1="2021-12-31", fillcolor="gray", opacity=.12, line_width=0,
                  annotation_text="pandemia", annotation_position="top left")
    fig.update_layout(height=380, **TEMA)
    return fig


def gerar_tudo():
    ASSETS.mkdir(parents=True, exist_ok=True)
    anual, mensal = carregar()
    t1 = rq1_tabela(anual); base2 = rq2_base(anual); c2 = rq2_correlacoes(base2); t3 = rq3_tabela(mensal)
    t1.to_csv(ASSETS / "rq1_regiao_ano.csv", index=False)
    c2.to_csv(ASSETS / "rq2_correlacoes.csv", index=False)
    t3.to_csv(ASSETS / "rq3_desvio_2020.csv")
    figs = {"rq1": rq1_figura(t1), "rq2": rq2_figura(base2), "rq3": rq3_figura(mensal),
            "serie": serie_longa_figura(mensal)}
    for k, f in figs.items():
        f.write_html(ASSETS / f"fig_{k}.html", include_plotlyjs="cdn")
    return dict(anual=anual, mensal=mensal, t1=t1, base2=base2, c2=c2, t3=t3, figs=figs)


if __name__ == "__main__":
    r = gerar_tudo()
    print(r["t1"].to_string()); print(r["c2"].to_string()); print(r["t3"].to_string())
