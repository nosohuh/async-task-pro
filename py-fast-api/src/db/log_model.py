# AI Etkileşim Tablosu
def create_ai_activity_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_activity (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255),
                    file_format VARCHAR(50),
                    model_name VARCHAR(255),
                    ip_address VARCHAR(255),
                    chat_history TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
            print("►► AI Activity Table - Ok ◄◄")
    except Exception as e:
        print(f"Error creating ai_activity table: {e}")


# AI etkinlikleri
def log_ai_activity(conn, file_name, file_format, model_name, ip_address, chat_history):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ai_activity (file_name, file_format, model_name, ip_address, chat_history)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (file_name, file_format, model_name, ip_address, chat_history),
            )
            conn.commit()
            print(f"Logged AI Activity for {file_name}")
    except Exception as e:
        print(f"Error logging AI activity: {e}")
