import sqlite3
from get_exchange_rates import fetch_and_combine_rates


def load_data_to_sqlite(df):
    conn = sqlite3.connect('exchange_rates.db')
    c = conn.cursor()
    
    for index, row in df.iterrows():
        c.execute('''
            INSERT OR REPLACE INTO rates (date, currency, rate, source)
            VALUES (?, ?, ?, ?)
        ''', (row['date'], row['currency'], row['rate'], row['source']))
    
    conn.commit()
    conn.close()
    print(f"Loaded {len(df)} rows into the SQLite database.")
    
if __name__ == "__main__":
    combined_exchange_rates = fetch_and_combine_rates()
    load_data_to_sqlite(combined_exchange_rates)
