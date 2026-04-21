import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os


load_dotenv()

def conexao():
    conn = None  
    try:
        conn = psycopg2.connect(
            user=os.getenv('DB_USUARIO'),
            password=os.getenv('DB_SENHA'),
            port='5432',
            host='localhost',
            database='BANCOV2'
        )
        return conn
    except Exception as erro:
        print('Erro na conexão:', erro)
        return None 