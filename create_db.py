import sqlite3

def initialize_db():
    conn = sqlite3.connect('exchange_rates.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rates (
            date TEXT,
            currency TEXT,
            rate REAL,
            source TEXT,
            PRIMARY KEY (date, currency, source)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
