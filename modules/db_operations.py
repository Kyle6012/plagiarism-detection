import sqlite3

db_path = "plagiarism_detection.db"

# Initialization of database with indexes
def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, content TEXT, embedding TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, hash TEXT, embedding TEXT)''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_content ON documents(content)")
    conn.commit()
    conn.close()

# Connection Pool Example
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

def insert_document(content, embedding):
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO documents (content, embedding) VALUES (?, ?)", (content, embedding))

def insert_image(image_hash, embedding):
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (hash, embedding) VALUES (?, ?)", (image_hash, embedding))