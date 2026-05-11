from datetime import datetime, timedelta
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações das cidades — nome, latitude e longitude
CIDADES = [
    {"nome": "São Paulo",       "lat": -23.55, "lon": -46.63},
    {"nome": "Rio de Janeiro",  "lat": -22.91, "lon": -43.17},
    {"nome": "Curitiba",        "lat": -25.43, "lon": -49.27},
    {"nome": "Salvador",        "lat": -12.97, "lon": -38.50},
    {"nome": "Manaus",          "lat": -3.10,  "lon": -60.02},
]


def obter_dias_historico() -> int:
    """
    Lê DIAS_HISTORICO do ambiente e garante um valor inteiro positivo.
    """
    try:
        dias = int(os.getenv("DIAS_HISTORICO", "7"))
    except ValueError as exc:
        raise ValueError("DIAS_HISTORICO deve ser um número inteiro.") from exc

    if dias < 1:
        raise ValueError("DIAS_HISTORICO deve ser maior que zero.")

    return dias


def buscar_clima(cidade: dict, dias: int) -> pd.DataFrame:
    """
    Busca dados de clima de uma cidade na API Open-Meteo.
    Retorna um DataFrame com os dados brutos horários.
    """
    data_fim = datetime.today().strftime("%Y-%m-%d")
    data_inicio = (datetime.today() - timedelta(days=dias)).strftime("%Y-%m-%d")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": cidade["lat"],
        "longitude": cidade["lon"],
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "start_date": data_inicio,
        "end_date": data_fim,
        "timezone": "America/Sao_Paulo",
    }

    try:
        resposta = requests.get(url, params=params, timeout=10)
        resposta.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Erro ao buscar clima de {cidade['nome']}: {exc}") from exc

    dados = resposta.json()
    hourly = dados.get("hourly")
    if not hourly:
        motivo = dados.get("reason", "resposta sem dados horários")
        raise RuntimeError(f"Erro ao buscar clima de {cidade['nome']}: {motivo}")

    df = pd.DataFrame({
        "cidade": cidade["nome"],
        "coletado_em": hourly["time"],
        "temperatura": hourly["temperature_2m"],
        "chuva_mm": hourly["precipitation"],
        "vento_kmh": hourly["wind_speed_10m"],
    })

    return df


def extrair_todas_cidades() -> None:
    """
    Percorre todas as cidades, coleta os dados e salva em CSV.
    """
    todos = []
    dias_historico = obter_dias_historico()

    for cidade in CIDADES:
        print(f"Coletando: {cidade['nome']}...")
        df = buscar_clima(cidade, dias_historico)
        todos.append(df)

    df_final = pd.concat(todos, ignore_index=True)

    # Garante que a pasta existe
    os.makedirs("data/raw", exist_ok=True)

    # Nome do arquivo com a data de hoje
    hoje = datetime.today().strftime("%Y-%m-%d")
    caminho = f"data/raw/clima_raw_{hoje}.csv"

    df_final.to_csv(caminho, index=False, encoding="utf-8")
    print(f"\nArquivo salvo em: {caminho}")
    print(f"Total de registros: {len(df_final)}")


if __name__ == "__main__":
    extrair_todas_cidades()
