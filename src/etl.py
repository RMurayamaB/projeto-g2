"""Pipeline ETL – Estatísticas de Segurança Pública do RJ (ISP-RJ).

Lê os CSVs brutos (latin-1, separador ';', decimal ',', ausente '-'),
padroniza tipos, cria métricas derivadas e salva em data/processed/
(.csv.gz). Nenhum dado bruto é sobrescrito; descartes ficam registrados em log.
Uso:  python -m src.etl
"""
from __future__ import annotations
import logging
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC = ROOT / "data" / "raw", ROOT / "data" / "processed"
ANUAL_RAW = RAW / "isp_anual_municipio_2014_2020.csv"
MENSAL_RAW = RAW / "isp_mensal_municipio_2014_2026.csv"
ID_COLS = ["fmun_cod", "fmun", "ano", "mes", "mes_ano", "regiao", "fase"]
REGIOES = ["Capital", "Baixada Fluminense", "Grande Niterói", "Interior"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("etl")


def ler_csv_isp(path: Path) -> pd.DataFrame:
    """Leitura robusta do formato ISP."""
    df = pd.read_csv(path, sep=";", encoding="latin-1", decimal=",",
                     na_values=["-", ""], low_memory=False)
    df.columns = df.columns.str.strip().str.lower()
    num = [c for c in df.columns if c not in ID_COLS]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce").astype("float64")
    df["fmun_cod"] = df["fmun_cod"].astype("int64")
    df["fmun"] = df["fmun"].str.strip()
    df["regiao"] = pd.Categorical(df["regiao"].str.strip(), categories=REGIOES)
    return df


def indicadores(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in ID_COLS + ["data", "sem_dados", "periodo"]]


def tratar_anual(df: pd.DataFrame) -> pd.DataFrame:
    ind = indicadores(df)
    df["sem_dados"] = df[ind].isna().all(axis=1)
    mun_sem = df.loc[df["sem_dados"], "fmun"].unique()
    log.info("Anual: %d linhas; %d municípios sem nenhum dado publicado (descartados): %s",
             len(df), len(mun_sem), ", ".join(sorted(mun_sem)[:5]) + " ...")
    out = df.loc[~df["sem_dados"]].drop(columns=["sem_dados"]).copy()
    # Métrica derivada: participação da polícia na letalidade violenta (%)
    out["pct_interv_policial"] = (100 * out["hom_por_interv_policial"]
                                  / out["letalidade_violenta"].where(out["letalidade_violenta"] > 0))
    return out.reset_index(drop=True)


def tratar_mensal(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = pd.to_datetime(dict(year=df["ano"], month=df["mes"], day=1))
    df["periodo"] = pd.cut(df["data"], bins=pd.to_datetime(["2013-12-31", "2020-02-29", "2021-12-31", "2100-01-01"]),
                           labels=["pré-pandemia", "pandemia (mar/20–dez/21)", "pós-pandemia"])
    log.info("Mensal: %d linhas, %d municípios, %s a %s, nulos em indicadores: %d",
             len(df), df["fmun"].nunique(), df["data"].min().date(), df["data"].max().date(),
             int(df[indicadores(df)].isna().sum().sum()))
    return df.sort_values(["fmun_cod", "data"]).reset_index(drop=True)


def run() -> tuple[pd.DataFrame, pd.DataFrame]:
    PROC.mkdir(parents=True, exist_ok=True)
    anual = tratar_anual(ler_csv_isp(ANUAL_RAW))
    mensal = tratar_mensal(ler_csv_isp(MENSAL_RAW))
    anual.to_csv(PROC / "isp_anual_tratado.csv.gz", index=False, compression="gzip")
    mensal.to_csv(PROC / "isp_mensal_tratado.csv.gz", index=False, compression="gzip")
    log.info("Arquivos salvos em %s", PROC)
    return anual, mensal


if __name__ == "__main__":
    run()
