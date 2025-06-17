import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    with open('sql/create_tables.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
