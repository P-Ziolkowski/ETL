import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

num_rows = 100
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
sources = ['FreeCurrencyAPI', 'ECB']

data = {
    'deal_currency': np.random.choice(currencies, num_rows),
    'value': np.round(np.random.uniform(1000, 100000, num_rows), 2),
    'source': np.random.choice(sources, num_rows),
    'date_of_transaction': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)]
}

trade_deals_df = pd.DataFrame(data)

file_path = 'dummy_trade_deals.csv'
trade_deals_df.to_csv(file_path, index=False)

print(f"Dummy dataset saved to {file_path}")
