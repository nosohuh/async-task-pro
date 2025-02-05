import psycopg2  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os  # type: ignore
from .log_model import (
    create_ai_activity_table,
)


load_dotenv()

db_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME"),
}


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        print("*DB-Connect*")
        return conn
    except Exception as e:
        print(f"Error: {e}")
    return None


def get_import_db_table():
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            create_ai_activity_table(conn)
            print("▬ DB → Tables Created! ▬")
        else:
            print("Connection not be established.")
    except Exception as e:
        print(f"Error during table creation: {e}")
    return None
