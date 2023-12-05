import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from helper_methods import find_target_folder

def _extract_date_range(series: dict, date_from, date_to):
    if date_from is None:
        date_from = max([series_data.index[0] for series_data in series.values()])

    if date_to is None:
        date_to = min([series_data.index[-1] for series_data in series.values()])

    return pd.to_datetime(date_from), pd.to_datetime(date_to)


def _normalize_series(price_series, method):
    if method == 'first':
        return price_series / price_series.iloc[0]
    elif method == 'last':
        return price_series / price_series.iloc[-1]
    elif method == 'max':
        return price_series / price_series.max()
    elif method == 'min':
        return price_series / price_series.min()
    elif method == 'avg':
        return price_series / price_series.mean()
    elif method == 'change':
        return price_series.pct_change().fillna(0)
    else:
        return price_series


def _plot_series(aligned_series, kind, normalize, date_from, date_to):
    for series_name, price_series in aligned_series.items():
        price_series.plot(kind=kind, label=series_name)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(
        f'Price History\nNormalization: {normalize}, Date Range: {date_from.strftime("%Y-%m-%d")} to {date_to.strftime("%Y-%m-%d")}')
    plt.legend()


def _save_chart(normalize, date_from, date_to, asset_names):
    output_directory = find_target_folder(target_folder='asset_returns', inner_path='outputs')

    asset_names_str = '_'.join(asset_names)
    file_name = f"{output_directory}/Price_History_{normalize}_{asset_names_str}_{date_from.strftime('%Y-%m-%d')}_{date_to.strftime('%Y-%m-%d')}.png"
    plt.savefig(file_name)


def multi_plot(series_original: dict, date_from=None, date_to=None, kind: str = 'line', normalize: str = None) -> None:
    series = {k: v.copy() for k, v in series_original.items()}  # Make a copy of the original series

    date_from, date_to = _extract_date_range(series, date_from, date_to)

    asset_names = list(series.keys())  # Extract asset names

    # Normalize the data based on the specified method
    if normalize:
        for series_name, price_series in series.items():
            series[series_name] = _normalize_series(price_series.loc[date_from:date_to], normalize)

    # Align indexes for all series within the specified date range
    aligned_series = {name: price_series.loc[date_from:date_to] for name, price_series in series.items()}

    # Plotting the aligned series
    _plot_series(aligned_series, kind, normalize, date_from, date_to)

    # Save the chart as a PNG file with asset names included in the file name
    _save_chart(normalize, date_from, date_to, asset_names)

    plt.show()


def _create_daily_change_series(series):
    daily_change_series = {}
    for series_name, price_series in series.items():
        daily_change_series[series_name] = price_series.pct_change().fillna(0)
    return daily_change_series


def correlation_chart(series: dict, date_from=None, date_to=None) -> None:
    date_from, date_to = _extract_date_range(series, date_from, date_to)

    # Convert series to daily changes
    daily_change_series = _create_daily_change_series(series)

    # Convert daily changes to a DataFrame
    df = pd.DataFrame(daily_change_series)

    # Create a pairplot matrix using Seaborn
    sns.pairplot(df)
    plt.title(f'Pairplot Matrix\nDate Range: {date_from.strftime("%Y-%m-%d")} to {date_to.strftime("%Y-%m-%d")}')

    # Save the chart as a PNG file
    _save_chart('Pairplot Matrix', date_from, date_to, series.keys())

    plt.show()
