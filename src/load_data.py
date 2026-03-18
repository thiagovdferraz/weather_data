from sqlalchemy import create_engine, text
# biblioteca para conectar com o banco de dados PostgreSQL
# create engine para criar a conexão com o banco de dados
# text fazer comandos SQL usando text

from urllib.parse import quote_plus
# biblioteca para codificar a senha do banco de dados, caso haja caracteres especiais

import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# resolve para obter o caminho absoluto do arquivo .env, 
# parent.parent para subir dois níveis na hierarquia de diretórios, 
# e depois acessar a pasta config e o arquivo .env 

load_dotenv(env_path)
# carrega as variáveis de ambiente do arquivo .env

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
# host = 'localhost'  # Usando localhost para acessar o banco de dados localmente,
host = 'host.docker.internal'  # Usando host.docker.internal para acessar o banco de 
#dados no host a partir do container Docker

def get_engine():
    logging.info(f"Conectando em {host}:5432/{database}...")
    return create_engine(f'postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}')
# função para criar a engine de conexão com o banco de dados PostgreSQL,
# usando a biblioteca SQLAlchemy e a função quote_plus para codificar a senha

engine = get_engine() # cria a engine de conexão com o banco de dados

def load_weather_data(table_name:str, df:pd.DataFrame):
    df.to_sql(
        name = table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info(f"\nDados carregados na tabela {table_name} com sucesso!")

    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    logging.info(f"\nTotal de registros na tabela {table_name}:{len(df_check)}")