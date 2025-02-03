# Token Tablosu
def create_token_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS token (
                    id SERIAL PRIMARY KEY,
                    token_value VARCHAR(255) NOT NULL,
                    creation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
            print("►► Token Table - Ok ◄◄")
    except Exception as e:
        print(f"Error creating token table: {e}")
        
# Log Tablosu
def create_log_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS log (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    level VARCHAR(10) NOT NULL,
                    message TEXT NOT NULL
                );
                """
            )
            conn.commit()
            print("►► Log Table - Ok ◄◄")
    except Exception as e:
        print(f"Error creating log table: {e}")

# Dosya Yükleme Tablosu
def create_file_upload_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS file_upload (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    upload_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(50) NOT NULL DEFAULT 'pending',
                    token_id INT REFERENCES token(id),  
                    file_type VARCHAR(50) NOT NULL DEFAULT 'pdf'
                );
                """
            )
            conn.commit()
            print("►► File Table - Ok ◄◄")
    except Exception as e:
        print(f"Error creating file upload table: {e}")

# AI Etkileşim Tablosu
def create_ai_activity_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_activity (
                    id SERIAL PRIMARY KEY,
                    token_id INT REFERENCES token(id),  
                    message TEXT NOT NULL,
                    response TEXT,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
            print("►► AI Activity Table - Ok ◄◄")
    except Exception as e:
        print(f"Error creating ai_activity table: {e}")
