import pandas as pd
import yfinance as yf

from scripts.managers._asset_manager import AssetManager


class TickerManager(AssetManager):
    def __init__(self):
        super().__init__(config_name='ticker_config')

    def _get_prices_data_from_api(self, ticker: str) -> pd.Series:
        """
        Fetches historical price data for the given ticker using yfinance.

        :param ticker: A string representing the ticker symbol.
        :return: A pandas Series with index of type datetime64[ns] containing daily prices.
                 The series name is 'prices'.
        """
        # Fetch historical data using yfinance
        ticker_data = yf.download(ticker, interval='1d')

        # Extracting the 'Close' price as a Series
        price_series = ticker_data['Close']

        # Rename the series to 'prices'
        price_series.name = 'prices'

        return price_series


if __name__ == '__main__':
    print("Ticker")