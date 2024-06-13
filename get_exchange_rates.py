import requests
import pandas as pd
import freecurrencyapi
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from settings import base_currency, freecurrencyapi_key


def get_latest_freecurrencyapi_rates():
    source = 'FreeCurrencyAPI'
    try:
        client = freecurrencyapi.Client(freecurrencyapi_key)
        response = client.latest(base_currency=base_currency)
        rates = response.get('data', {})
        meta = response.get('meta', {})
        
        if rates:
            date = meta.get('last_updated_at', pd.Timestamp.now().strftime('%Y-%m-%d'))
            df = pd.DataFrame([
                {'source': source, 'date': date, 'currency': k, 'rate': v}
                for k, v in rates.items()
            ])
            return df
        else:
            return pd.DataFrame()
        
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return pd.DataFrame()



def fetch_ecb_rates():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(url)
    source = "ECB"
    
    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        
        ecb_data = []
        for cube in root.findall('.//ns:Cube[@time]', namespaces):
            date = cube.get('time')
            for rate in cube.findall('.//ns:Cube[@currency]', namespaces):
                currency = rate.get('currency')
                value = float(rate.get('rate'))
                ecb_data.append({'source': source, 'date': date, 'currency': currency, 'rate': value})
        
        return pd.DataFrame(ecb_data)
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()


def get_latest_ecb_rates(date):
    df = fetch_ecb_rates()
    if df.empty:
        # If no data for the given date, look back for the last available data
        current_date = datetime.strptime(date, "%Y-%m-%d")
        while df.empty:
            current_date -= timedelta(days=1)
            df = fetch_ecb_rates()

    if base_currency != "EUR": #base currency of ECB
        conver_ratio =  df[df['currency'] == base_currency]['rate'].values[0]
        df['rate'] = df['rate'].apply(lambda x: x/conver_ratio)

    return df


def fetch_and_combine_rates():
    today = pd.Timestamp.now().strftime('%Y-%m-%d')

    ecb_rates = get_latest_ecb_rates(today)
    freecurrencyapi_rates = get_latest_freecurrencyapi_rates()
    combined_rates = pd.concat([ecb_rates, freecurrencyapi_rates])
    
    return combined_rates