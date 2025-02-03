import psycopg2
from dotenv import load_dotenv
import os
from .table_models import create_log_table, create_file_upload_table, create_ai_activity_table, create_token_table


load_dotenv()

db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME')
}

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        print('*DB-Connect*')
        return conn
    except Exception as e:
        print(f'Error: {e}')
    return None

def get_import_db_table():
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            create_token_table(conn)
            create_log_table(conn)  
            create_file_upload_table(conn)
            create_ai_activity_table(conn)
            print('▬ DB → Tables Created! ▬')
        else:
            print("Connection could not be established.")
    except Exception as e:
        print(f'Error during table creation: {e}')
    return None
