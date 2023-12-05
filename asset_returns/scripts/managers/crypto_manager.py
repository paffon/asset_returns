import pandas as pd
import requests

from scripts.managers._asset_manager import AssetManager
from scripts.helper_methods import days_since_2008


class CryptoManager(AssetManager):
    def __init__(self):
        super().__init__(config_name='crypto_config')

    def _get_prices_data_from_api(self, asset: str) -> pd.Series:
        """
        Fetches historical price data for the given asset from the CoinGecko API.

        :param asset: A string representing the asset whose historical price data is to be fetched.
        :return: A pandas Series with index of type datetime64[ns] containing daily prices.
                 The series name is 'prices'.
        """
        # API request to fetch data
        url = f'https://api.coingecko.com/api/v3/coins/{asset}/market_chart?' \
              f'vs_currency=usd&interval=daily&days={days_since_2008()}'
        response = requests.get(url)
        data = response.json()['prices']

        # Convert the time from milliseconds to datetime and create a DataFrame
        df = pd.DataFrame(data, columns=['time', 'price'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')

        # Set 'time' column as index and resample to get one price per day (using the last entry of each day)
        df.set_index('time', inplace=True)
        series = df.resample('D').last()['price']

        # Assign name to the series
        series.name = 'prices'

        return series


if __name__ == '__main__':
    print("Crypto")
