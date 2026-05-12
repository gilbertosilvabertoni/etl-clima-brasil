import os
import psycopg2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
load_dotenv("docker/.env.db")


def get_connection():
    """
    Retorna uma conexão com o PostgreSQL.
    Dentro do Docker usa o nome do container, fora usa localhost.
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", "5432"))

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=os.getenv("POSTGRES_DB", "clima_brasil"),
        user=os.getenv("POSTGRES_USER", "clima_user"),
        password=os.getenv("POSTGRES_PASSWORD", "clima_pass"),
    )


def criar_tabela() -> None:
    """
    Lê o SQL e cria a tabela no banco se não existir.
    """
    with open("sql/001_create_tables.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("Tabela clima_diario criada ou já existente.")


def carregar_csv_no_banco(data: str = None) -> None:
    """
    Carrega o CSV processado na tabela clima_diario.
    Ignora duplicatas (mesma cidade e data).
    """
    if data is None:
        data = datetime.today().strftime("%Y-%m-%d")

    caminho = f"data/processed/clima_processado_{data}.csv"

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho)

    inseridos = 0
    ignorados = 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                try:
                    cur.execute("""
                        INSERT INTO clima_diario
                            (cidade, data, temp_max, temp_min, temp_media,
                             chuva_total_mm, vento_max_kmh)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (cidade, data) DO NOTHING
                    """, (
                        row["cidade"],
                        row["data"],
                        row["temp_max"],
                        row["temp_min"],
                        row["temp_media"],
                        row["chuva_total_mm"],
                        row["vento_max_kmh"],
                    ))
                    if cur.rowcount > 0:
                        inseridos += 1
                    else:
                        ignorados += 1
                except Exception as e:
                    print(f"Erro na linha {row['cidade']} {row['data']}: {e}")
        conn.commit()

    print(f"Carregamento concluído: {inseridos} inseridos, {ignorados} ignorados.")


def executar(data: str = None) -> None:
    """
    Orquestra criação da tabela e carregamento dos dados.
    """
    print("Criando tabela...")
    criar_tabela()

    print("Carregando dados no banco...")
    carregar_csv_no_banco(data)


if __name__ == "__main__":
    executar()