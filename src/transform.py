import pandas as pd
from datetime import datetime
import os


def carregar_dados_brutos(data: str = None) -> pd.DataFrame:
    """
    Carrega o CSV bruto do dia informado.
    Se não informar data, usa a de hoje.
    """
    if data is None:
        data = datetime.today().strftime("%Y-%m-%d")

    caminho = f"data/raw/clima_raw_{data}.csv"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, parse_dates=["coletado_em"])
    return df


def validar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica e trata problemas comuns nos dados brutos.
    """
    # Remove linhas onde cidade está vazia
    df = df.dropna(subset=["cidade"])

    # Remove duplicatas exatas
    df = df.drop_duplicates()

    # Preenche temperatura ausente com a média da cidade naquele dia
    df["data"] = df["coletado_em"].dt.date
    df["temperatura"] = df.groupby(["cidade", "data"])["temperatura"]\
                          .transform(lambda x: x.fillna(x.mean()))

    # Preenche chuva e vento ausentes com zero
    df["chuva_mm"] = df["chuva_mm"].fillna(0)
    df["vento_kmh"] = df["vento_kmh"].fillna(0)

    return df


def agregar_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega os dados horários em resumo diário por cidade.
    """
    df["data"] = df["coletado_em"].dt.date

    resumo = df.groupby(["cidade", "data"]).agg(
        temp_max=("temperatura", "max"),
        temp_min=("temperatura", "min"),
        temp_media=("temperatura", "mean"),
        chuva_total_mm=("chuva_mm", "sum"),
        vento_max_kmh=("vento_kmh", "max"),
    ).reset_index()

    # Arredonda para 1 casa decimal
    cols_numericas = ["temp_max", "temp_min", "temp_media",
                      "chuva_total_mm", "vento_max_kmh"]
    resumo[cols_numericas] = resumo[cols_numericas].round(1)

    # Ordena por data e cidade
    resumo = resumo.sort_values(["data", "cidade"]).reset_index(drop=True)

    return resumo


def salvar_dados_transformados(df: pd.DataFrame, data: str = None) -> None:
    """
    Salva o DataFrame transformado em data/processed/.
    """
    if data is None:
        data = datetime.today().strftime("%Y-%m-%d")

    os.makedirs("data/processed", exist_ok=True)
    caminho = f"data/processed/clima_processado_{data}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"Arquivo salvo em: {caminho}")
    print(f"Total de registros: {len(df)}")


def transformar(data: str = None) -> pd.DataFrame:
    """
    Orquestra todas as etapas de transformação.
    """
    print("Carregando dados brutos...")
    df = carregar_dados_brutos(data)

    print("Validando dados...")
    df = validar_dados(df)

    print("Agregando por dia...")
    df = agregar_por_dia(df)

    salvar_dados_transformados(df, data)
    return df


if __name__ == "__main__":
    df = transformar()
    print("\nAmostra do resultado:")
    print(df.head(10).to_string(index=False))