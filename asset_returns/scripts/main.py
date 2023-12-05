from scripts.managers.crypto_manager import CryptoManager
from scripts.managers.ticker_manager import TickerManager
from scripts.plotter import multi_plot, correlation_chart
from scripts.helper_methods import enrich_series


def main():
    crypto_manager = CryptoManager()
    crypto_assets = {asset: crypto_manager.load_single(asset) for asset in ['bitcoin']}

    ticker_manager = TickerManager()
    ticker_assets = {asset: ticker_manager.load_single(asset) for asset in ['nvidia']}

    assets = {}
    assets.update(crypto_assets)
    assets.update(ticker_assets)

    assets = enrich_series(assets, step_size=1, steps=4)

    max_len = max(len(asset) for asset in assets.keys())
    for asset_name, asset in assets.items():
        print(f'{asset_name.ljust(max_len)}    {asset.index[0]}    {asset.index[-1]}')

    multi_plot(series_original=assets, normalize=None)
    correlation_chart(series=assets)


if __name__ == '__main__':
    main()
