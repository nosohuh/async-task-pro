from db.db import get_db_connection

def log_message(level, message):
    conn = None
    try:
        conn = get_db_connection()        
        cursor = conn.cursor()  
        cursor.execute(
            """
            INSERT INTO log (level, message) 
            VALUES (%s, %s)
            """, 
            (level, message)
        )
        conn.commit()
        
    except Exception as e:
        print(f"Log kaydedilirken hata oluştu: {e}")
    finally:
        if conn:
            conn.close()
            print("DB bağlantısı kapatıldı.")

# Expample usage
def log_error(message):
    log_message('ERROR', message)

def log_info(message):
    log_message('INFO', message)

def log_debug(message):
    log_message('DEBUG', message)

# # Örnek kullanım
# log_info("Program başladı.")
# log_error("Bir hata oluştu.")
# log_debug("Debug mesajı.")
