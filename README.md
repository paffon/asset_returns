# asset_returns
Easily compare the returns of tickers and crypto assets.


## How to use
1. Add assets to the config files. Keys are convenient names for you to refer to the assets, values are the actual symbols.
2. Add the (convenient) names to the main() function. For example:

  crypto_manager = CryptoManager()
  crypto_assets = {asset: crypto_manager.load_single(asset) for asset in ['bitcoin']}
  
  ticker_manager = TickerManager()
  ticker_assets = {asset: ticker_manager.load_single(asset) for asset in ['nvidia']}
