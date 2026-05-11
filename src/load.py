import pandas as pd
from datetime import datetime
import os


def carregar_dados_processados(data: str = None) -> pd.DataFrame:
    """
    Carrega o CSV processado do dia informado.
    """
    if data is None:
        data = datetime.today().strftime("%Y-%m-%d")

    caminho = f"data/processed/clima_processado_{data}.csv"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, parse_dates=["data"])
    return df


def gerar_relatorio_qualidade(df: pd.DataFrame, data: str = None) -> None:
    """
    Gera um relatório de qualidade dos dados carregados.
    """
    if data is None:
        data = datetime.today().strftime("%Y-%m-%d")

    os.makedirs("data/processed", exist_ok=True)
    caminho = f"data/processed/relatorio_qualidade_{data}.txt"

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DE QUALIDADE — {data}\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total de registros: {len(df)}\n")
        f.write(f"Cidades cobertas: {df['cidade'].nunique()}\n")
        f.write(f"Período: {df['data'].min().date()} a {df['data'].max().date()}\n")
        f.write(f"Valores nulos: {df.isnull().sum().sum()}\n\n")
        f.write("Resumo por cidade:\n")
        f.write("-" * 40 + "\n")

        for cidade in sorted(df["cidade"].unique()):
            subset = df[df["cidade"] == cidade]
            f.write(f"\n{cidade}:\n")
            f.write(f"  Dias coletados : {len(subset)}\n")
            f.write(f"  Temp máx média : {subset['temp_max'].mean():.1f}°C\n")
            f.write(f"  Chuva total    : {subset['chuva_total_mm'].sum():.1f}mm\n")

    print(f"Relatório de qualidade salvo em: {caminho}")


def exibir_resumo(df: pd.DataFrame) -> None:
    """
    Exibe resumo final no terminal.
    """
    print("\n" + "=" * 50)
    print("RESUMO DO CARREGAMENTO")
    print("=" * 50)
    print(f"Registros carregados : {len(df)}")
    print(f"Cidades              : {', '.join(sorted(df['cidade'].unique()))}")
    print(f"Período              : {df['data'].min().date()} a {df['data'].max().date()}")
    print(f"Valores nulos        : {df.isnull().sum().sum()}")
    print("=" * 50)


def carregar(data: str = None) -> None:
    """
    Orquestra o carregamento e geração de relatório.
    """
    print("Carregando dados processados...")
    df = carregar_dados_processados(data)

    exibir_resumo(df)
    gerar_relatorio_qualidade(df, data)

    print("\nCarregamento concluído com sucesso.")


if __name__ == "__main__":
    carregar()