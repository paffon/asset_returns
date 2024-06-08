# asset_returns
Easily compare the returns of tickers and crypto assets.


## How to use
1. Add assets to the config files. Keys are convenient names for you to refer to the assets, values are the actual symbols.
2. Add the (convenient) names to the main() function. For example:

  crypto_manager = CryptoManager()
  crypto_assets = {asset: crypto_manager.load_single(asset) for asset in ['bitcoin']}
  
  ticker_manager = TickerManager()
  ticker_assets = {asset: ticker_manager.load_single(asset) for asset in ['nvidia']}

## Example
**Comparing performances of Nvidia to bitcooin, with 1 day shift**
![Price_History_Pairplot Matrix_bitcoin_nvidia_bitcoin-1-shift_nvidia-1-shift_2024-01-02_2024-06-06](https://github.com/paffon/asset_returns/assets/45170837/7dc9ee4c-b6dd-4ae3-8e6a-5dd9baf67b36)
![Price_History_first_bitcoin_nvidia_bitcoin-1-shift_nvidia-1-shift_2024-01-02_2024-06-06](https://github.com/paffon/asset_returns/assets/45170837/e14f34a2-95db-40a8-8468-fd6468278f47)
